# 🤖 CLAUDE HANDOFF DOCUMENT - Copy to Google Docs

**Last Updated**: [TIMESTAMP]  
**Session ID**: [SESSION_ID]  
**Context Used**: [PERCENTAGE]%  
**Next Claude**: Copy this entire document to restore full context

---

## 🎯 CURRENT MISSION: Friday Brewery Demo (95% Complete)

### ✅ **COMPLETED TODAY**
- [ ] Discord bot with Google Sheets integration (`discord-bot/enhanced_bot.py`)
- [ ] WhatsApp Steel Bonnet alerts (`whatsapp-integration/steel-bonnet-flow.json`)
- [ ] GitHub Actions framework (has YAML syntax error)
- [ ] Google Sheets comprehensive tracking
- [ ] n8n workflows imported and tested

### 🚨 **CRITICAL NEXT STEPS**
1. **PRIORITY**: Fix GitHub Actions YAML syntax error (line 269)
   - File: `.github/workflows/claude-max-automation.yml`
   - Blocking automation workflow

2. **Deploy Ready Components**:
   - CT-027: Discord bot deployment (Server Claude)
   - CT-029: WhatsApp integration (Server Claude)

3. **Test Integration**: End-to-end brewery alert flow

---

## 🔑 ACCESS & CREDENTIALS

### **GitHub Repository**
- **URL**: https://github.com/slimstrongarm/industrial-iot-stack
- **Status**: Public repo, push access verified
- **Last Push**: [TIMESTAMP]

### **Google Sheets Integration**
- **Sheet ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **Credentials**: `credentials/iot-stack-credentials.json`
- **Status**: Fully operational, all tabs active

### **Server Access**
- **IP**: 100.94.84.126 (Tailscale)
- **User**: localaccount
- **Project Path**: `/mnt/c/Users/Public/Docker/industrial-iot-stack`
- **Docker**: Available via WSL

### **Services Running**
- **n8n**: http://localhost:5678 (Server)
- **Node-RED**: http://localhost:1880 (Server)
- **Ignition**: http://localhost:8088 (Mac)
- **MQTT**: Port 1883 (Both)

---

## 📂 KEY FILES & LOCATIONS

### **Ready for Deployment**
```
discord-bot/enhanced_bot.py           # Discord bot with sheets integration
discord-bot/docker-compose.yml       # Deployment config
whatsapp-integration/steel-bonnet-flow.json  # WhatsApp Node-RED flow
ignition-scripts/n8n_api_caller.py   # Ignition integration
```

### **Configuration Files**
```
credentials/iot-stack-credentials.json  # Google Sheets API
.github/workflows/claude-max-automation.yml  # ⚠️ HAS YAML ERROR
STATUS.md                            # Current project status
scripts/.claude_tasks_state.json     # Task tracking state
```

### **Context Documents**
```
WHATSAPP_API_INTEGRATION_GUIDE.md    # Complete WhatsApp setup
DISCORD_INTEGRATION_VISION.md        # Discord architecture
GITHUB_ACTIONS_CLAUDE_MAX_SETUP.md   # Automation setup
```

---

## 🖥️ TMUX SESSIONS

### **Mac Claude (Green)**
```bash
# To restore Mac session:
cd ~/Desktop/industrial-iot-stack
tmux attach -t claude-max-restored
# OR create new: ./scripts/start-mac-claude-max.sh
```

### **Server Claude (Blue)**
```bash
# To restore Server session:
ssh localaccount@100.94.84.126
~/start_server_claude.sh
# OR setup first time: bash first_time_server_tmux.sh
```

---

## 📋 TASK STATUS (From Google Sheets)

### **High Priority**
- **CT-030**: GitHub Actions YAML syntax fix (Mac Claude) - **BLOCKED**
- **CT-027**: Discord bot deployment (Server Claude) - **READY**
- **CT-029**: WhatsApp deployment (Server Claude) - **READY**

### **Complete & Ready**
- CT-021: Discord server setup ✅
- CT-025: Discord commands implemented ✅
- CT-028: WhatsApp API integration ✅

---

## 🎪 FRIDAY DEMO SCENARIO

```
BREWERY EMERGENCY ALERT FLOW:
1. Steel Bonnet equipment publishes MQTT: salinas/utilities/air_compressor_01/telemetry
2. Node-RED processes threshold: >85% pressure
3. WhatsApp alert sent: "🚨 Steel Bonnet Alert: Air Compressor 01 - High Pressure (87%)"
4. Operator acknowledges via WhatsApp reply
5. Status logged to Google Sheets
6. Discord notification sent to development channel
```

**Demo Confidence**: HIGH (95% ready)

---

## 🔄 QUICK RESTORATION COMMANDS

### **Verify Everything is Working**
```bash
# Mac Claude verification
cd ~/Desktop/industrial-iot-stack
git status
python3 scripts/test_sheets_access.py
cat STATUS.md

# Server Claude verification  
ssh localaccount@100.94.84.126
docker ps
curl http://localhost:5678/api/v1/workflows
```

### **Emergency Context Recovery**
1. Read this Google Doc first
2. Clone repo: `git clone https://github.com/slimstrongarm/industrial-iot-stack`
3. Check STATUS.md for latest state
4. Review scripts/.claude_tasks_state.json for tasks
5. Test Google Sheets access
6. Create appropriate TMUX session (Mac=Green, Server=Blue)

---

## 🚨 CRITICAL REMINDERS

### **For Mac Claude**
- You handle: GitHub Actions fix, Google Sheets updates, documentation
- TMUX session: GREEN status bar "🍎 MAC CLAUDE"
- Priority: Fix YAML syntax error at line 269

### **For Server Claude** 
- You handle: Docker deployments, n8n, Node-RED services
- TMUX session: BLUE status bar "🖥️ SERVER CLAUDE" 
- Priority: Deploy CT-027 (Discord) and CT-029 (WhatsApp)

### **Both Instances**
- Update Google Sheets "Claude Tasks" tab
- Sync via git commits with clear messages
- Friday demo is THE priority
- WhatsApp + Discord integration ready to deploy

---

## 📞 HANDOFF PROTOCOL

1. **Copy this doc to new Google Doc**: "Claude Handoff [DATE]"
2. **Update timestamps and percentages**
3. **Add specific progress made**
4. **Share Google Doc link** for continuity
5. **Test critical access** (GitHub, Sheets, Server)

---

**🎯 BOTTOM LINE**: 95% ready for Friday brewery demo. Fix YAML error, deploy components, test integration. All the hard work is done!

**📧 Context preserved in**: GitHub repo + Google Sheets + This Google Doc