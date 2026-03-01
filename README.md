# Skill Security Reviewer v3.0.0
>Enhanced Malicious Skill Detection Tool - With Anti-Obfuscation and Anti-Evasion Detection Capabilities

- *malicious-skill-benchmark*: Contains 100 neutralized malicious Skill samples
- *advanced-malicious-skills*: Contains 50 malicious Skill samples using various encryption and obfuscation techniques, specifically designed to test skill-security-reviewer v3.0's anti-obfuscation detection capabilities

```
  v3.0 New Features (41 Obfuscation Detections):
  - ENCODE (8 items): Base64/32/Hex/URL/Unicode/HTML/ROT13/Multi-layer ✅
  - ENCRYPT (8 items): XOR/AES/RC4/Hardcoded Keys/Runtime Decryption ✅
  - STRING (8 items): Split/Concat/Reverse/Replace/Array/chr()/Format ✅
  - DYNAMIC (8 items): eval/exec/Function/import/getattr/pickle ✅
  - ENTROPY (5 items): High-entropy Strings/Compression/Binary/Packed Code ✅
  - VARNAME (6 items): Random/Single-char/Underscore/Unicode/Misleading Names ✅
  - ANTI (6 items): Debugger/VM/Sandbox/Timing/Environment/Self-delete Detection ✅

  v2.0 Retained (53 Threat Detections):
  - THEFT (8 items): SSH/Cloud Credentials/API Keys/Browser etc. ✅
  - EXEC (7 items): curl|bash/Reverse Shell/eval/rm -rf etc. ✅
  - PERSIST (7 items): RC Files/cron/Git Hooks/SSH Backdoors etc. ✅
  - EXFIL (7 items): HTTP/DNS Tunneling/Webhook/C2 etc. ✅
  - INJ (7 items): Instruction Override/Jailbreak/Hidden Instructions etc. ✅
  - ABUSE (6 items): Hook Abuse/MCP Abuse/Tool Abuse etc. ✅
  - DECEP (6 items): Impersonation/Hidden Functionality/Fake Urgency etc. ✅
  - SUPPLY (5 items): Typosquatting/Postinstall etc. ✅

  Detection Results Summary
  ┌──────────────────────────────────────────┬─────────┬───────────────┬─────────┐
  │               Test Set                   │ Samples │ Detection Rate│ Missed  │
  ├──────────────────────────────────────────┼─────────┼───────────────┼─────────┤
  │ Basic Threats (benchmark-001~100)        │ 100     │ 100%          │ 0       │
  ├──────────────────────────────────────────┼─────────┼───────────────┼─────────┤
  │ Advanced Obfuscation (adv-001~050)       │ 50      │ 100%          │ 0       │
  ├──────────────────────────────────────────┼─────────┼───────────────┼─────────┤
  │ Total                                    │ 150     │ 100%          │ 0       │
  └──────────────────────────────────────────┴─────────┴───────────────┴─────────┘
```
