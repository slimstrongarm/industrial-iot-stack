# 🎯 START HERE - Master Navigation for Claude Instances

## Quick Orientation
1. **Repository Status**: Check `QUICK_ORIENTATION.md` for reorganization progress
2. **Current Context**: Read `CURRENT_CONTEXT.md` for session state
3. **Your Role**: Auto-detect based on TMUX color (Green=Mac, Blue=Server)

## 📂 New Repository Structure

### Technology-Specific Work
```
technologies/
├── mqtt/          # Message broker (EMQX, Mosquitto)
├── node-red/      # Flow-based programming
├── discord/       # Bot and automation
├── google-sheets/ # Task tracking and dashboards
├── n8n/           # Workflow automation [TODO]
├── ignition/      # SCADA/HMI [TODO]
├── docker/        # Containerization [TODO]
└── whatsapp/      # Messaging integration [TODO]
```

**Working on a specific technology?** Go directly to `technologies/[tech-name]/README.md`

### Project-Specific Work
```
projects/
├── ct-084-parachute-drop/  # Edge device integration
├── ct-085-network-discovery/# Industrial network scanning
├── ct-086-router-system/    # Secure network infrastructure
└── steel-bonnet/            # Brewery implementation
```

### Core Documentation
```
.claude/
├── START_HERE.md            # You are here
├── CURRENT_CONTEXT.md       # Session state
├── INDEX.md                 # Full documentation index
├── QUICK_ORIENTATION.md     # Reorganization status
└── handoff_template.md      # For session transitions
```

## 🔍 How to Find Things

### By Technology
- **MQTT issues?** → `technologies/mqtt/`
- **Discord bot?** → `technologies/discord/bots/discord-bot/`
- **Google Sheets?** → `technologies/google-sheets/`

### By Task ID
- **CT-084?** → `projects/ct-084-parachute-drop/`
- **CT-XXX?** → Check Google Sheets Claude Tasks tab

### By Integration
- **MQTT + Node-RED?** → Check both technology folders
- **Discord + Sheets?** → See integration guides in each

## 🚀 Quick Commands

```bash
# Check reorganization progress
cat .claude/QUICK_ORIENTATION.md

# Find all files for a technology
ls -la technologies/mqtt/

# Search for specific topic
grep -r "touchscreen" projects/

# View technology index
cat technologies/mqtt/INDEX.md
```

## 📊 Key Resources

- **Google Sheets**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **Credentials**: `/credentials/iot-stack-credentials.json`
- **Discord Channels**: #mac-claude, #server-claude
- **GitHub Repo**: slimstrongarm/industrial-iot-stack

## 🎯 Navigation Strategy

1. **Start Here** (.claude/START_HERE.md)
2. **Check Progress** (QUICK_ORIENTATION.md)
3. **Go to Technology** (technologies/[name]/)
4. **Read INDEX.md** (see all files available)
5. **Start Working** (follow the guides)

---
*This structure makes finding anything in < 30 seconds possible!*