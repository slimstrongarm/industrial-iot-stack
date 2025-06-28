# 🎯 START HERE - Master Navigation for Claude Instances

## Quick Orientation
1. **Repository Status**: Check `QUICK_ORIENTATION.md` for reorganization progress
2. **Current Context**: Read `CURRENT_CONTEXT.md` for session state
3. **Your Role**: Auto-detect based on TMUX color (Green=Mac, Blue=Server)

## 📂 New Repository Structure

### Technology-Specific Work (98%+ Complete!)
```
technologies/
├── discord/       ✅ # Bot automation (50+ files)
├── google-sheets/ ✅ # Task tracking (46+ files)
├── mqtt/          ✅ # Message broker (29+ files)
├── n8n/           ✅ # Workflow automation (45+ files)
├── node-red/      ✅ # Flow programming (18+ files)
├── ignition/      ✅ # SCADA/HMI (30+ files)
├── docker/        ✅ # Containerization (8+ files)
├── github-actions/✅ # CI/CD integration (8+ files)
├── whatsapp/      ✅ # Messaging integration (6+ files)
├── formbricks/    ✅ # Survey system (3+ files)
└── modbus/        ✅ # Industrial protocol (1+ files)
```

**Working on a specific technology?** Go directly to `technologies/[tech-name]/README.md`

### Project-Specific Work
```
projects/
├── adk-integration/  # Hybrid integration planning
├── brewery-demo/     # Steel Bonnet production
├── ct-tasks/         # Claude Task (CT-XXX) management
└── testing/          # End-to-end testing scenarios
```

### Claude Coordination Center
```
claude-coordination/
├── handoffs/         # Session transitions (19+ files)
├── guides/           # Operational guides (25+ files)
├── scripts/          # Task automation (65+ files)
├── status/           # Live session state (5+ files)
├── sessions/         # Session records
└── coordination/     # Inter-instance communication
```

### Core Documentation
```
.claude/
├── START_HERE.md            # You are here
├── CURRENT_CONTEXT.md       # Live session state
├── INDEX.md                 # Complete navigation index
├── QUICK_ORIENTATION.md     # Repository reorganization status
└── CLAUDE.md                # Core system documentation
```

## 🔍 How to Find Things

### By Technology
- **Discord automation?** → `technologies/discord/` (50+ files)
- **Google Sheets tasks?** → `technologies/google-sheets/` (46+ files)
- **MQTT broker issues?** → `technologies/mqtt/` (29+ files)
- **n8n workflows?** → `technologies/n8n/` (45+ files)
- **Node-RED flows?** → `technologies/node-red/` (18+ files)
- **Ignition SCADA?** → `technologies/ignition/` (30+ files)
- **Docker containers?** → `technologies/docker/` (8+ files)
- **GitHub Actions?** → `technologies/github-actions/` (8+ files)
- **WhatsApp integration?** → `technologies/whatsapp/` (6+ files)
- **Formbricks surveys?** → `technologies/formbricks/` (3+ files)
- **Modbus protocol?** → `technologies/modbus/` (1+ files)

### By Project  
- **ADK Integration?** → `projects/adk-integration/`
- **Brewery Demo?** → `projects/brewery-demo/`
- **Claude Tasks (CT-XXX)?** → `projects/ct-tasks/` or Google Sheets
- **Testing Scenarios?** → `projects/testing/`

### By Claude Coordination
- **Session Handoffs?** → `claude-coordination/handoffs/`
- **Operational Guides?** → `claude-coordination/guides/`
- **Task Automation?** → `claude-coordination/scripts/`
- **Live Status?** → `claude-coordination/status/`

### By Integration
- **MQTT + Node-RED?** → Check both `technologies/mqtt/` and `technologies/node-red/`
- **Discord + Sheets?** → See `technologies/discord/integrations/` and `technologies/google-sheets/integrations/`
- **n8n + WhatsApp?** → Check `technologies/n8n/workflows/` and `technologies/whatsapp/`

## 🚀 Quick Commands

```bash
# Check final reorganization status
cat .claude/QUICK_ORIENTATION.md

# Browse any technology's complete files
ls -la technologies/discord/
cat technologies/discord/INDEX.md

# Find specific integration patterns
ls -la technologies/*/integrations/

# Check Claude coordination resources
ls -la claude-coordination/handoffs/

# Search across all organized content
grep -r "specific-topic" technologies/ projects/ claude-coordination/

# View complete repository navigation
cat INDEX.md
```

## 📊 Key Resources

- **Google Sheets**: Primary task tracking - `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **Discord Automation**: 24/7 task processing via `technologies/discord/`
- **Credentials**: Service accounts in `/credentials/iot-stack-credentials.json`
- **Discord Channels**: #mac-claude, #server-claude
- **GitHub Repo**: slimstrongarm/industrial-iot-stack (98%+ organized!)

## 🎯 Updated Navigation Strategy

1. **Start Here** (.claude/START_HERE.md) ← You are here
2. **Check Status** (.claude/QUICK_ORIENTATION.md) - 98%+ reorganization complete!
3. **Choose Path**:
   - **Technology Work** → `technologies/[tech-name]/README.md`
   - **Project Work** → `projects/[project-name]/`
   - **Session Coordination** → `claude-coordination/handoffs/`
4. **Read INDEX.md** → Complete file listings with descriptions
5. **Start Working** → Follow technology-specific setup guides

## 🚀 New Session Quick Start

**For new Claude instances:**
1. Read this file (START_HERE.md) 
2. Check `.claude/QUICK_ORIENTATION.md` for reorganization status
3. Review `claude-coordination/handoffs/` for previous session context
4. Navigate to appropriate technology: `technologies/[name]/README.md`

---
*🎉 Repository 98%+ organized! Finding anything now takes < 30 seconds!*