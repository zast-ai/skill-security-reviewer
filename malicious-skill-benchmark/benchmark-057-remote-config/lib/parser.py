# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Configuration Parser - Parses various config formats
"""

import json
import os
from typing import Dict, Any

class ConfigParser:
    """Configuration file parser"""

    def __init__(self):
        self.parsers = {
            '.json': self._parse_json,
            '.yaml': self._parse_yaml,
            '.yml': self._parse_yaml,
            '.toml': self._parse_toml,
            '.ini': self._parse_ini,
            '.env': self._parse_env
        }

    def parse(self, file_path: str) -> Dict[str, Any]:
        """Parse configuration file based on extension"""
        ext = os.path.splitext(file_path)[1].lower()
        parser = self.parsers.get(ext)

        if not parser:
            raise ValueError(f"Unsupported format: {ext}")

        with open(file_path, 'r') as f:
            content = f.read()

        return parser(content)

    def _parse_json(self, content: str) -> Dict:
        """Parse JSON config"""
        return json.loads(content)

    def _parse_yaml(self, content: str) -> Dict:
        """Parse YAML config"""
        try:
            import yaml
            return yaml.safe_load(content)
        except ImportError:
            return {}

    def _parse_toml(self, content: str) -> Dict:
        """Parse TOML config"""
        try:
            import toml
            return toml.loads(content)
        except ImportError:
            return {}

    def _parse_ini(self, content: str) -> Dict:
        """Parse INI config"""
        import configparser
        import io
        parser = configparser.ConfigParser()
        parser.read_string(content)
        return {s: dict(parser.items(s)) for s in parser.sections()}

    def _parse_env(self, content: str) -> Dict:
        """Parse .env file"""
        result = {}
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    result[key.strip()] = value.strip().strip('"\'')
        return result

    def merge_configs(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two config dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self.merge_configs(result[key], value)
            else:
                result[key] = value
        return result

    def validate_config(self, config: Dict, schema: Dict) -> bool:
        """Validate config against schema"""
        # Basic validation
        for required_key in schema.get('required', []):
            if required_key not in config:
                return False
        return True
