# BENCHMARK_TEST_ONLY - Neutralized malicious sample for security testing
"""
Crypto utilities for backup encryption
"""

import os
import base64
import hashlib
from typing import bytes

class CryptoUtils:
    """Encryption utilities for backup data"""

    def __init__(self, key=None):
        self.key = key or self._derive_key()

    def _derive_key(self):
        """Derive encryption key from machine-specific data"""
        import platform
        machine_data = f"{platform.node()}-{os.getuid()}"
        return hashlib.sha256(machine_data.encode()).digest()

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data using AES-256"""
        try:
            from cryptography.fernet import Fernet
            key = base64.urlsafe_b64encode(self.key)
            f = Fernet(key)
            return f.encrypt(data)
        except ImportError:
            # Fallback to simple XOR (not secure, just obfuscation)
            return self._xor_encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data"""
        try:
            from cryptography.fernet import Fernet
            key = base64.urlsafe_b64encode(self.key)
            f = Fernet(key)
            return f.decrypt(data)
        except ImportError:
            return self._xor_encrypt(data)

    def _xor_encrypt(self, data: bytes) -> bytes:
        """Simple XOR encryption (obfuscation only)"""
        key_len = len(self.key)
        return bytes(b ^ self.key[i % key_len] for i, b in enumerate(data))

    def hash_file(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file"""
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def generate_signature(self, data: bytes) -> str:
        """Generate HMAC signature for data"""
        import hmac
        return hmac.new(self.key, data, hashlib.sha256).hexdigest()
