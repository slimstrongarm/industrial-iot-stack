# Deployment Prompts

## Standard Deployment Checklist
1. Check Google Sheets for pending tasks
2. Review recent git commits
3. Validate configuration files
4. Test integrations (MQTT, WhatsApp, Discord)
5. Update task status in Google Sheets

## Common Commands
```bash
# Check Docker status
docker ps --format "table {{.Names}}	{{.Status}}"

# Test MQTT connection
mosquitto_pub -h localhost -t "test/topic" -m "test message"

# Update Google Sheets
python3 scripts/comprehensive_sheets_update.py

# Test WhatsApp flow
node whatsapp-integration/test-alert.js
```

## Pre-Deployment Questions
- Are all dependencies deployed?
- Have you tested the integration endpoints?
- Is the Google Sheets automation working?
- Are environment variables configured?
