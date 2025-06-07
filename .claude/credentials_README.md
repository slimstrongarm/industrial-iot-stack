# Credentials Directory

🔒 **SECURITY NOTICE**: This directory contains sensitive authentication information. Handle with extreme care.

## 📁 Contents

### Google Sheets Integration
- `iot-stack-credentials.json` - Service account credentials for Google Sheets API
- **Usage**: All Google Sheets integration scripts
- **Scope**: Read/write access to project spreadsheets
- **Rotation**: Every 90 days

### Discord Integration  
- `discord_webhook.txt` - Webhook URL for team notifications
- **Usage**: Discord notification client
- **Scope**: Send messages to Industrial IoT Stack channel
- **Format**: `https://discord.com/api/webhooks/...`

### GitHub Integration
- **GitHub Secrets Required** (set at https://github.com/slimstrongarm/industrial-iot-stack/settings/secrets/actions)
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions (no setup needed)
- `ANTHROPIC_API_KEY` - Claude API key for GitHub Actions automation
- `CLAUDE_MAX_SESSION_KEY` - Claude Max OAuth session key (preferred method)
- **Usage**: GitHub Actions workflows, Claude bot automation
- **Scope**: Repository access, issue/PR commenting, workflow execution

### Environment Template
- `.env.template` - Template for required environment variables
- **Usage**: Copy to `.env` and fill in actual values
- **Contents**: All API keys, tokens, and URLs

## 🔒 Security Guidelines

### File Permissions
```bash
# Set restrictive permissions
chmod 600 *.json *.txt *.env
chmod 700 .
```

### Git Security
- ✅ All credential files are in `.gitignore`
- ✅ No sensitive data in commit history
- ✅ Use environment variables in production

### Access Control
- **Local Development**: Files in this directory
- **Production**: Environment variables only
- **CI/CD**: GitHub Secrets for automation

### Credential Rotation
- **Google Sheets**: 90-day rotation schedule
- **Discord Webhooks**: Regenerate if compromised
- **API Keys**: Follow provider recommendations

## 🚨 Emergency Procedures

### If Credentials Are Compromised
1. **Immediately revoke** the compromised credentials
2. **Generate new credentials** from the provider
3. **Update all references** in scripts and environment
4. **Test integrations** to ensure functionality
5. **Document the incident** for future reference

### Backup Procedures
- **Encrypted backup** of credential templates
- **Secure storage** separate from repository
- **Access log** for credential usage

## 📝 Environment Variables

Required environment variables for production deployment:

```bash
# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_JSON="{...}"
GOOGLE_SHEETS_ID="1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"

# Discord
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."

# Twilio WhatsApp
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"

# n8n
N8N_URL="http://100.94.84.126:5678"
N8N_USERNAME="iiot-admin"
N8N_PASSWORD="StrongPassword123!"

# Alert Recipients
BREWERY_ALERT_TO="whatsapp:+1234567890"
SUPERVISOR_WHATSAPP="whatsapp:+1234567891"

# GitHub Integration (GitHub Secrets only)
GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"          # Auto-provided in Actions
ANTHROPIC_API_KEY="sk-ant-api03-xxxxxxxxxx"      # Claude API key
CLAUDE_MAX_SESSION_KEY="sess-xxxxxxxxxx"         # Claude Max OAuth (preferred)
```

## 🔧 GitHub Secrets Setup

### Required GitHub Secrets
Navigate to: `https://github.com/slimstrongarm/industrial-iot-stack/settings/secrets/actions`

**Essential Secrets:**
1. **`ANTHROPIC_API_KEY`** - Claude API key from Anthropic Console
   - Used by: claude.yml workflow  
   - Format: `sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxx`

2. **`CLAUDE_MAX_SESSION_KEY`** - Claude Max OAuth session key (preferred)
   - Used by: claude.yml workflow (preferred over API key)
   - Format: `sess-xxxxxxxxxxxxxxxxxxxxxxxxx`
   - **Note**: More reliable than API key, doesn't count against usage limits

3. **`GOOGLE_SHEETS_ID`** - Project spreadsheet ID  
   - Value: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`

4. **`GOOGLE_CREDENTIALS`** - JSON credentials for service account
   - Copy content of `iot-stack-credentials.json`

5. **`DISCORD_WEBHOOK`** - Discord webhook URL
   - Copy content of `discord_webhook.txt`

### GitHub Token Status Check
```bash
# Check if bot is working
gh api /repos/slimstrongarm/industrial-iot-stack/actions/workflows

# Test Claude bot by creating issue with @claude mention
gh issue create --title "Test Claude Bot" --body "@claude please confirm you're working"
```

---

**⚠️  REMEMBER**: Never commit actual credentials to version control!  
**Last Updated**: 2025-06-04 23:45:00 UTC