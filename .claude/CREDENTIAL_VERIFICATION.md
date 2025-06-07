# 🔑 Credential Verification Guide

## ⚡ Quick Access Test (Run This First!)

```bash
# Test all critical access in 30 seconds
echo "🔍 Testing Claude Instance Access..."
echo "=================================="

# 1. GitHub Repository Access
echo "📂 GitHub Repository:"
git remote -v
git status
echo "✅ GitHub repo access: $(git remote get-url origin 2>/dev/null || echo 'MISSING')"

# 2. Google Sheets API
echo -e "\n📊 Google Sheets API:"
if [ -f "credentials/iot-stack-credentials.json" ]; then
    echo "✅ Credentials file found"
    python3 -c "
import json
try:
    with open('credentials/iot-stack-credentials.json') as f:
        creds = json.load(f)
        print(f'✅ Service account: {creds.get(\"client_email\", \"Unknown\")}')
        print(f'✅ Project ID: {creds.get(\"project_id\", \"Unknown\")}')
except Exception as e:
    print(f'❌ Credential file error: {e}')
"
else
    echo "❌ Google Sheets credentials missing"
fi

# 3. Server Access
echo -e "\n🖥️ Server Access:"
if command -v ssh >/dev/null; then
    ssh -o ConnectTimeout=3 localaccount@100.94.84.126 'echo "✅ Server accessible"' 2>/dev/null || echo "❌ Server connection failed"
else
    echo "⚠️ SSH not available (may be normal on some systems)"
fi

# 4. Docker Access (if applicable)
echo -e "\n🐳 Docker Access:"
if command -v docker >/dev/null; then
    docker ps > /dev/null 2>&1 && echo "✅ Docker accessible" || echo "❌ Docker not accessible"
else
    echo "⚠️ Docker not available (may be normal on Mac)"
fi

echo -e "\n🎯 Access verification complete!"
```

## 🔐 Credential Status Check

### GitHub Access (Most Critical)
```bash
# Check Git credentials
git config --global user.name
git config --global user.email
git config --global credential.helper

# Test push access (dry run)
git push --dry-run origin main 2>&1 | head -3

# If using SSH keys
ls -la ~/.ssh/id_* 2>/dev/null | head -5

# If using token
git config --global github.token 2>/dev/null || echo "Token not in config"
```

### Google Sheets Access
```bash
# Test Google Sheets connection
python3 scripts/testing/test_sheets_access.py

# Manual credential check
ls -la credentials/iot-stack-credentials.json
cat credentials/iot-stack-credentials.json | jq '.client_email' 2>/dev/null
```

### Server Access (Server Claude Only)
```bash
# Test Tailscale connectivity
ping -c 1 100.94.84.126

# Test SSH access
ssh -o ConnectTimeout=5 localaccount@100.94.84.126 'whoami'

# Check server Docker
ssh localaccount@100.94.84.126 'docker ps'
```

## 🛠️ Credential Setup for New Instances

### For Mac Claude
```bash
# GitHub access is usually preserved automatically via:
# - macOS Keychain (HTTPS tokens)
# - SSH keys in ~/.ssh/
# - Git credential helper

# Test with:
git status
git push --dry-run origin main
```

### For Server Claude (Windows WSL)
```bash
# Clone repo (public, no auth needed)
git clone https://github.com/slimstrongarm/industrial-iot-stack.git

# Copy credentials from Mac (if needed)
scp ~/Desktop/industrial-iot-stack/credentials/*.json localaccount@100.94.84.126:/path/to/project/credentials/

# Or use environment variables
export GOOGLE_SHEETS_CREDENTIALS_JSON="$(cat credentials/iot-stack-credentials.json)"
```

## 🔄 Credential Recovery Procedures

### GitHub Access Lost
```bash
# Option 1: Check existing credentials
git config --list | grep credential

# Option 2: Re-authenticate via GitHub CLI (if available)
gh auth login

# Option 3: Use personal access token
git config --global credential.helper store
git push  # Will prompt for username/token

# Option 4: SSH key setup
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub  # Add to GitHub
```

### Google Sheets Access Lost
```bash
# 1. Download new credentials from Google Cloud Console
# 2. Replace credentials/iot-stack-credentials.json
# 3. Test connection
python3 scripts/testing/test_sheets_access.py
```

### Server Access Lost
```bash
# 1. Check Tailscale status
tailscale status

# 2. Reconnect Tailscale
tailscale up

# 3. Test connection
ping 100.94.84.126
```

## 🎯 Claude Instance Types & Access Needs

### Mac Claude (Green TMUX)
**Required Access:**
- ✅ GitHub repository (read/write)
- ✅ Google Sheets API
- ⚠️ Server SSH (optional, for coordination)

**Auto-Detection:**
```bash
# This usually "just works" because:
# - Git credentials stored in macOS Keychain
# - Google Sheets creds in local file
# - SSH keys persistent in ~/.ssh/
```

### Server Claude (Blue TMUX)
**Required Access:**
- ✅ GitHub repository (read-only minimum)
- ✅ Google Sheets API (copy from Mac)
- ✅ Docker (local)
- ✅ n8n/Node-RED (local)

**Setup Required:**
```bash
# Copy credentials to server
scp credentials/iot-stack-credentials.json localaccount@100.94.84.126:~/
```

## 📝 Environment Variables for Production

### Create .env file
```bash
# Copy template
cp credentials/.env.template .env

# Fill in actual values:
GOOGLE_SHEETS_ID="1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
GITHUB_REPO="https://github.com/slimstrongarm/industrial-iot-stack"
N8N_URL="http://100.94.84.126:5678"
SERVER_IP="100.94.84.126"
```

## 🚨 Emergency Access Recovery

### Complete Credential Loss
1. **GitHub**: Repository is public - can always clone
2. **Google Sheets**: Regenerate service account
3. **Server**: Use Tailscale IP to reconnect
4. **Docker**: Rebuild containers if needed

### Minimal Working Setup
```bash
# 1. Clone repo (always works - public)
git clone https://github.com/slimstrongarm/industrial-iot-stack.git
cd industrial-iot-stack

# 2. Read context
cat .claude/CURRENT_CONTEXT.md

# 3. Test what works
python3 scripts/quick_status.py
```

---

**🎯 Bottom Line**: GitHub access usually persists, Google Sheets needs file, Server needs SSH setup.

**⚡ Quick Test**: Run the verification script at the top of this file!