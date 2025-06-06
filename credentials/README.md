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
```

---

**⚠️  REMEMBER**: Never commit actual credentials to version control!  
**Last Updated**: 2025-06-04 23:45:00 UTC