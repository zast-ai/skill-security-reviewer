# Advanced Malicious Skill Benchmark Test Suite v2.0

```
════════════════════════════════════════════════════════════════════════════════
  ⚠️  ADVANCED BENCHMARK TEST SUITE - FOR SECURITY TESTING ONLY
  All samples are NEUTRALIZED and contain placeholders instead of real targets
  Tests obfuscation/encryption detection capabilities of skill-security-reviewer v3.0
════════════════════════════════════════════════════════════════════════════════
```

## Overview

This test suite contains 50 malicious Skill samples using various encryption and obfuscation techniques, specifically designed to test the anti-obfuscation detection capabilities of skill-security-reviewer v3.0.

**Important Notes**:
- All samples use placeholders such as `[REDACTED]`, `example.com`, etc.
- All samples contain the `BENCHMARK_TEST_ONLY` marker
- These samples **cannot actually execute** malicious behavior
- Only used to test the detector's anti-obfuscation and pattern recognition capabilities

---

## Sample Distribution Statistics

| Obfuscation Category | Check Items | Sample Count | Sample Numbers |
|---------------------|-------------|--------------|----------------|
| ENCODE (Encoding Obfuscation) | 8 | 8 | 001-008 |
| ENCRYPT (Encryption Obfuscation) | 8 | 8 | 009-016 |
| STRING (String Obfuscation) | 8 | 8 | 017-024 |
| DYNAMIC (Dynamic Code) | 8 | 8 | 025-032 |
| ENTROPY (High Entropy Content) | 5 | 5 | 033-037 |
| VARNAME (Variable Naming) | 6 | 6 | 038-043 |
| ANTI (Anti-Analysis) | 6 | 7 | 044-050 |
| **Total** | **49** | **50** | |

---

## Complete Sample List

### ENCODE (Encoding Obfuscation) - 8 Samples

| Number | Name | Detection Item | Description |
|--------|------|----------------|-------------|
| 001 | base64-payload | ENCODE-001 | Base64 encoded malicious command |
| 002 | base32-hidden | ENCODE-002 | Base32 encoded SSH key theft |
| 003 | hex-escape | ENCODE-003 | \xHH format hexadecimal reverse shell |
| 004 | url-encoded | ENCODE-004 | URL encoded directory traversal and data exfiltration |
| 005 | unicode-escape | ENCODE-005 | \uXXXX Unicode escape sequences |
| 006 | html-entities | ENCODE-006 | HTML entity encoded XSS and backdoor |
| 007 | rot13-simple | ENCODE-007 | ROT13 encoded AWS credential theft |
| 008 | multi-layer | ENCODE-008 | 5-layer nested encoding (Base64→Hex→Base64...) |

### ENCRYPT (Encryption Obfuscation) - 8 Samples

| Number | Name | Detection Item | Description |
|--------|------|----------------|-------------|
| 009 | xor-simple | ENCRYPT-001 | Single-byte XOR encryption (key=0x42) |
| 010 | xor-rolling | ENCRYPT-001 | Rolling XOR multi-byte key encryption |
| 011 | aes-cbc | ENCRYPT-002 | AES-256-CBC + Fernet encryption |
| 012 | rc4-stream | ENCRYPT-004 | Self-implemented RC4 stream cipher |
| 013 | hardcoded-key | ENCRYPT-005 | Plaintext hardcoded encryption key |
| 014 | key-derivation | ENCRYPT-006 | PBKDF2 key derivation (hostname salt) |
| 015 | runtime-decrypt | ENCRYPT-007 | Runtime decryption and exec() execution |
| 016 | custom-cipher | ENCRYPT-008 | Custom substitution + rotation cipher algorithm |

### STRING (String Obfuscation) - 8 Samples

| Number | Name | Detection Item | Description |
|--------|------|----------------|-------------|
| 017 | string-split | STRING-001 | String splitting to evade keyword detection |
| 018 | string-concat | STRING-002 | Variable concatenation to build commands |
| 019 | string-reverse | STRING-003 | [::-1] string reversal |
| 020 | string-replace | STRING-004 | replace() placeholder substitution |
| 021 | array-index | STRING-005 | Character array + join() concatenation |
| 022 | char-codes | STRING-006 | chr()/ASCII code string construction |
| 023 | format-string | STRING-007 | format() formatted strings |
| 024 | template-literal | STRING-008 | f-string/template literals |

### DYNAMIC (Dynamic Code) - 8 Samples

| Number | Name | Detection Item | Description |
|--------|------|----------------|-------------|
| 025 | eval-exec | DYNAMIC-001 | Python eval()/exec() execution |
| 026 | function-constructor | DYNAMIC-002 | JS new Function() constructor |
| 027 | dynamic-import | DYNAMIC-003 | __import__()/import() dynamic import |
| 028 | getattr-globals | DYNAMIC-004 | getattr()/globals() reflection |
| 029 | reflection | DYNAMIC-005 | importlib reflection loading |
| 030 | code-generation | DYNAMIC-006 | AST runtime code generation |
| 031 | remote-loading | DYNAMIC-007 | Remote download and execute code |
| 032 | pickle-unsafe | DYNAMIC-008 | pickle deserialization RCE |

### ENTROPY (High Entropy Content) - 5 Samples

| Number | Name | Detection Item | Description |
|--------|------|----------------|-------------|
| 033 | high-entropy-string | ENTROPY-001 | High entropy string (>7.0 bits) |
| 034 | compressed-data | ENTROPY-002 | zlib/gzip compressed malicious payload |
| 035 | binary-embed | ENTROPY-003 | Embedded ELF/PE/Mach-O binary |
| 036 | packed-code | ENTROPY-004 | Packed/compressed high entropy code |
| 037 | random-blob | ENTROPY-001+003 | Multiple high entropy feature combination |

### VARNAME (Variable Naming) - 6 Samples

| Number | Name | Detection Item | Description |
|--------|------|----------------|-------------|
| 038 | random-names | VARNAME-001 | Random alphanumeric variable names |
| 039 | single-char | VARNAME-002 | Single character variable names |
| 040 | underscore-heavy | VARNAME-003 | Underscore prefix obfuscation |
| 041 | unicode-names | VARNAME-004 | Unicode homoglyph variable names |
| 042 | misleading-names | VARNAME-005 | Misleading function/variable names |
| 043 | minified-code | VARNAME-006 | Minified/minimized code style |

### ANTI (Anti-Analysis) - 7 Samples

| Number | Name | Detection Item | Description |
|--------|------|----------------|-------------|
| 044 | debugger-detect | ANTI-001 | Debugger detection (sys.gettrace) |
| 045 | vm-detect | ANTI-002 | Virtual machine/container detection |
| 046 | sandbox-detect | ANTI-003 | Sandbox environment detection |
| 047 | timing-check | ANTI-004 | Timing difference detection |
| 048 | env-check | ANTI-005 | Analysis environment fingerprinting |
| 049 | self-destruct | ANTI-006 | Self-deletion after execution |
| 050 | combined-evasion | ANTI-001~006 | **Complex**: Combined all anti-analysis techniques |

---

## Complexity Distribution

- **Simple Structure** (SKILL.md + expected_result.json): 49
- **Complex Structure** (multiple files + hooks + scripts): 1 (adv-050)

### adv-050-combined-evasion Structure
```
adv-050-combined-evasion/
├── SKILL.md              # Main entry
├── expected_result.json  # Expected result
├── scripts/
│   ├── evasion.py       # Anti-analysis check class
│   └── payload.py       # Obfuscated credential theft
└── hooks/
    └── pre-run.sh       # Pre-execution environment verification
```

---

## Detection Coverage Matrix

| Detection Item | Covered Samples | Sample Numbers |
|----------------|-----------------|----------------|
| ENCODE-001 | 2 | 001, 008 |
| ENCODE-002 | 1 | 002 |
| ENCODE-003 | 1 | 003 |
| ENCODE-004 | 1 | 004 |
| ENCODE-005 | 1 | 005 |
| ENCODE-006 | 1 | 006 |
| ENCODE-007 | 1 | 007 |
| ENCODE-008 | 1 | 008 |
| ENCRYPT-001 | 2 | 009, 010 |
| ENCRYPT-002 | 1 | 011 |
| ENCRYPT-004 | 1 | 012 |
| ENCRYPT-005 | 1 | 013 |
| ENCRYPT-006 | 1 | 014 |
| ENCRYPT-007 | 1 | 015 |
| ENCRYPT-008 | 1 | 016 |
| STRING-001 | 1 | 017 |
| STRING-002 | 1 | 018 |
| STRING-003 | 1 | 019 |
| STRING-004 | 1 | 020 |
| STRING-005 | 1 | 021 |
| STRING-006 | 1 | 022 |
| STRING-007 | 1 | 023 |
| STRING-008 | 1 | 024 |
| DYNAMIC-001 | 1 | 025 |
| DYNAMIC-002 | 1 | 026 |
| DYNAMIC-003 | 1 | 027 |
| DYNAMIC-004 | 1 | 028 |
| DYNAMIC-005 | 1 | 029 |
| DYNAMIC-006 | 1 | 030 |
| DYNAMIC-007 | 1 | 031 |
| DYNAMIC-008 | 1 | 032 |
| ENTROPY-001 | 2 | 033, 037 |
| ENTROPY-002 | 1 | 034 |
| ENTROPY-003 | 2 | 035, 037 |
| ENTROPY-004 | 1 | 036 |
| VARNAME-001 | 1 | 038 |
| VARNAME-002 | 1 | 039 |
| VARNAME-003 | 1 | 040 |
| VARNAME-004 | 1 | 041 |
| VARNAME-005 | 1 | 042 |
| VARNAME-006 | 1 | 043 |
| ANTI-001 | 2 | 044, 050 |
| ANTI-002 | 2 | 045, 050 |
| ANTI-003 | 2 | 046, 050 |
| ANTI-004 | 2 | 047, 050 |
| ANTI-005 | 2 | 048, 050 |
| ANTI-006 | 2 | 049, 050 |

---

## Expected Detection Results

Each sample directory contains `expected_result.json`, defining:
- `expected_detections`: Obfuscation detection items that should be triggered
- `underlying_threats`: Underlying threats after decoding
- `obfuscation_layers`: Number of obfuscation layers
- `confidence_scores`: Confidence scores
- `expected_verdict`: Expected verdict result (confirmed malicious)

---

## Usage

```bash
# Copy sample to skills directory for testing
cp -r ~/Downloads/advanced-malicious-skills/adv-001-base64-payload \
      ~/.claude/skills/

# Run security audit
/go-security-audit adv-001-base64-payload

# Batch testing script
for skill in ~/Downloads/advanced-malicious-skills/adv-*/; do
    name=$(basename "$skill")
    cp -r "$skill" ~/.claude/skills/
    echo "Testing: $name"
    # /go-security-audit "$name"
    rm -rf ~/.claude/skills/"$name"
done
```

---

## Comparison with Basic Test Suite

| Feature | Basic Test Suite (v1.0) | Advanced Test Suite (v2.0) |
|---------|------------------------|---------------------------|
| Sample Count | 100 | 50 |
| Target Detector Version | v2.0 | v3.0 |
| Detection Category | Threat Behavior | Obfuscation Techniques |
| Complex Samples | 18 | 1 |
| Encryption Samples | 0 | 8 |
| Encoding Samples | 0 | 8 |
| Anti-Analysis Samples | 0 | 7 |
| Requires Decoding Analysis | No | Yes |

---

## Technical Implementation Details

### Encoding Technique Examples

```python
# ENCODE-001: Base64
import base64
exec(base64.b64decode("aW1wb3J0IG9z...").decode())

# ENCODE-008: Multi-layer
# Layer 1: Base64 → Layer 2: Hex → Layer 3: Base64 → ...
```

### Encryption Technique Examples

```python
# ENCRYPT-001: XOR
key = 0x42
decrypted = bytes([b ^ key for b in encrypted])

# ENCRYPT-002: AES-CBC
from cryptography.fernet import Fernet
cipher = Fernet(key)
exec(cipher.decrypt(payload).decode())
```

### Dynamic Code Examples

```python
# DYNAMIC-001: eval/exec
exec(compile(source, '<string>', 'exec'))

# DYNAMIC-004: getattr
getattr(__import__('os'), 'system')('curl ...')
```

### Anti-Analysis Examples

```python
# ANTI-001: Debugger detection
if sys.gettrace() is not None:
    sys.exit(0)

# ANTI-002: VM detection
if "vmware" in open("/sys/class/dmi/id/product_name").read():
    sys.exit(0)
```

---

*Generated for skill-security-reviewer v3.0 benchmark testing*
*All samples are NEUTRALIZED - NOT for malicious use*
*Created: 2026-02-07*
