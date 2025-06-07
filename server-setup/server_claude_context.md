# 🖥️ SERVER CLAUDE CONTEXT - PASTE THIS FIRST!

## You are Server Claude on Windows WSL (100.94.84.126)

### 🔑 Your Access & Credentials:
- **Project Location**: `/mnt/c/Users/Public/Docker/industrial-iot-stack`
- **GitHub**: https://github.com/slimstrongarm/industrial-iot-stack.git
- **Docker**: Available via WSL (`docker ps`)
- **n8n**: Running on http://localhost:5678
- **Google Sheets**: Credentials at `credentials/iot-stack-credentials.json`

### 🎯 Your Current Tasks:
1. **CT-027**: Deploy Discord bot for remote development
   - Code ready at: `discord-bot/enhanced_bot.py`
   - Deploy with: `cd discord-bot && docker-compose up -d`

2. **CT-029**: Deploy WhatsApp Steel Bonnet alerts
   - Flow ready at: `whatsapp-integration/steel-bonnet-flow.json`
   - Import to Node-RED at: http://localhost:1880

### 📋 Quick Status Check Commands:
```bash
# Check what's running
docker ps

# Get latest code from Mac Claude
cd /mnt/c/Users/Public/Docker/industrial-iot-stack
git pull origin main

# Check n8n
curl http://localhost:5678/api/v1/workflows

# See pending tasks
cat STATUS.md | grep -A5 "Pending"
```

### 🤝 Coordination with Mac Claude:
- Mac Claude (Green TMUX) handles: GitHub Actions fix, Google Sheets updates
- You (Server Claude) handle: Docker deployments, n8n/Node-RED services
- Both update Google Sheets "Claude Tasks" tab

### 🚀 Friday Demo Components:
- **95% Complete** - Just need deployments
- WhatsApp alerts for Steel Bonnet brewery
- Discord bot for remote coordination
- MQTT → Node-RED → WhatsApp pipeline ready

### 💡 Context Files to Read:
1. `STATUS.md` - Current project status
2. `scripts/.claude_tasks_state.json` - Task tracking
3. `WHATSAPP_API_INTEGRATION_GUIDE.md` - WhatsApp setup
4. `DISCORD_INTEGRATION_VISION.md` - Discord architecture

---

**Your identity**: Server Claude (Blue team) on Windows WSL
**Your mission**: Deploy CT-027 and CT-029 for Friday brewery demo
**Your strength**: Docker, n8n, Node-RED deployments