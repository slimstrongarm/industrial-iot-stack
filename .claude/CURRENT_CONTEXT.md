# 🤖 CLAUDE START HERE - June 4, 2025 9:50 PM

## ⚡ INSTANT CONTEXT (Read This First!)
- **Mission**: Friday brewery demo (95% ready)
- **Critical Block**: GitHub Actions YAML syntax error line 269  
- **Ready Components**: Discord bot, WhatsApp integration
- **Your Role**: Auto-detected (Mac=Green TMUX, Server=Blue TMUX)

## 🎯 IMMEDIATE ACTIONS

### Mac Claude (Green TMUX)
1. **Fix YAML Error**: `.github/workflows/claude-max-automation.yml:269`
2. **Update Sheets**: Monitor Google Sheets progress
3. **Coordinate**: Support Server Claude deployments

### Server Claude (Blue TMUX)  
1. **Deploy Discord**: `cd discord-bot && docker-compose up -d`
2. **Deploy WhatsApp**: Import `whatsapp-integration/steel-bonnet-flow.json` to Node-RED
3. **Test Integration**: End-to-end brewery alert flow

## 🔑 ACCESS VERIFICATION (30 seconds)
```bash
# FIRST THING TO RUN - Verify all access
python3 scripts/claude/verify_all_access.py

# Quick manual checks:
git status                              # Should show clean repo
git remote -v                           # Should show slimstrongarm/industrial-iot-stack
ls credentials/iot-stack-credentials.json # Should exist
```

**If access fails**: Check `.claude/CREDENTIAL_VERIFICATION.md` for recovery steps

## 📂 KEY LOCATIONS

### Quick Status
- **Current priorities**: `STATUS.md`
- **Task tracking**: `scripts/.claude_tasks_state.json`
- **Google Sheets**: [IoT Stack Progress Master](https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do)

### Ready Deployments
- **Discord bot**: `discord-bot/enhanced_bot.py` (Server Claude)
- **WhatsApp flow**: `whatsapp-integration/steel-bonnet-flow.json` (Server Claude)  
- **Ignition scripts**: `ignition-scripts/n8n_api_caller.py`

### Configuration
- **Google Sheets API**: `credentials/iot-stack-credentials.json`
- **GitHub Actions**: `.github/workflows/claude-max-automation.yml` ⚠️ **HAS YAML ERROR**
- **Documentation**: `*_GUIDE.md` files

## 🚀 QUICK COMMANDS
```bash
# Status check (30 seconds)
python3 scripts/quick_status.py

# Deploy Discord (Server Claude)
cd discord-bot && docker-compose up -d

# Test WhatsApp (Server Claude)  
curl -X POST http://localhost:1880/webhook/whatsapp-test

# Fix YAML (Mac Claude)
yamllint .github/workflows/claude-max-automation.yml
```

## 🎪 FRIDAY DEMO FLOW
```
Steel Bonnet MQTT → Node-RED → WhatsApp Alert → Operator Reply → Google Sheets Log
```

## 📱 SESSION MANAGEMENT

### Create/Restore TMUX
```bash
# Mac Claude (Green)
./scripts/start-mac-claude-max.sh

# Server Claude (Blue)  
ssh localaccount@100.94.84.126
~/start_server_claude.sh
```

### Emergency Recovery
1. Read this file first (`.claude/CURRENT_CONTEXT.md`)
2. Check `STATUS.md` for latest priorities
3. Test access with commands above
4. Create appropriate TMUX session
5. Focus on Friday demo tasks

---

**Last Updated**: June 4, 2025 9:50 PM  
**Context Level**: 95% Friday demo ready, YAML fix needed  
**Auto-compact**: Use `.claude/HANDOFF_TEMPLATE.md` for transitions