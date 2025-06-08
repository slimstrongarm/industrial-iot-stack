# Industrial IoT Stack Documentation System

## Overview
This project creates a unified documentation system for an Industrial IoT stack centered around Ignition Edge and Node-RED. Each technology component maintains its own documentation that feeds into a central overview.

## Purpose
- Provide clear visibility into each technology's role, capabilities, and current implementation
- Create a single source of truth for the entire IIoT stack
- Enable each technology expert (or AI agent) to maintain their own documentation
- Automatically aggregate into a unified view

## 🚨 CRITICAL: Google Sheets Claude Tasks Priority
**The Google Sheets Claude Tasks tab is the HIGHEST PRIORITY for all actions.** This is the living to-do list that drives everything:
- **ALWAYS update Google Sheets** with task progress
- **EVERY significant action** gets documented as a task
- **Check existing setup first**: credentials/iot-stack-credentials.json and scripts/*google*sheets*.py
- **Spreadsheet ID**: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do

## 🤖 GAME CHANGER: Discord Automation Integration
**Revolutionary workflow automation now ACTIVE** - Tasks can be created and auto-processed via Discord:
- **Discord Bot**: @Mac Claude Bot add task [description] → Creates task in Google Sheets
- **Auto Assignment**: Tasks assigned to "Mac Claude" or "Server Claude" 
- **Auto Processing**: Claude workers automatically pick up and complete tasks
- **Mobile Access**: Full task management from iPhone Discord app
- **Real-time Updates**: Task status changes automatically: Pending → In Progress → Complete
- **Channels**: #mac-claude, #server-claude for instance-specific coordination
- **Proven**: CT-049 successfully automated end-to-end (Discord → Sheets → Mac Claude → Complete)

## Structure (Current Reality - 2025-06-07)

```
industrial-iot-stack/
├── .claude/                   # 📚 Claude documentation hub & instructions
├── discord-bot/               # 🤖 Discord automation system (GAME CHANGER)
│   ├── industrial_iot_claude_bot.py  # Main Discord bot
│   ├── docker-compose.yml     # Production deployment
│   ├── claude-discord.service # Systemd service for 24/7 operation
│   └── requirements.txt       # Python dependencies
├── Steel_Bonnet/              # 🏭 Complete brewery implementation
│   ├── scripts/               # Industrial automation scripts
│   ├── node-red-flows/        # Brewery-specific flows
│   ├── udts/                  # User Defined Types for Ignition
│   └── views/                 # HMI screens and interfaces
├── ignition-project-scan-endpoint/  # 🔧 Custom Ignition module
├── scripts/                   # 🔧 Automation & monitoring infrastructure
│   ├── monitoring/            # 🏥 Health monitoring & auto-restart
│   │   ├── unified_industrial_monitor.py    # Complete stack monitoring
│   │   ├── discord_health_monitor.py        # Discord bot health
│   │   └── unified_monitoring_system.py     # Google Sheets integration
│   ├── utilities/             # Helper tools and API clients
│   ├── mac_claude_task_worker.py      # Automated Claude task processing
│   └── add_unified_monitoring_tasks.py  # Google Sheets task management
├── stack-components/          # 📊 Individual technology documentation
│   ├── ignition-edge/         # Ignition Edge (basic docs)
│   ├── node-red/              # Node-RED (basic docs)
│   ├── n8n/                   # ✅ n8n workflow automation (complete docs)
│   ├── grafana/               # ✅ Grafana dashboards (complete setup)
│   ├── mqtt/                  # MQTT broker configurations
│   ├── databases/             # Database integrations
│   ├── edge-computing/        # Edge device integration
│   └── protocols/             # Communication protocols
├── whatsapp-integration/      # 📱 WhatsApp alerts & notifications
├── claude-code-action-fork/   # 🔄 GitHub Actions Claude integration
├── credentials/               # 🔐 API keys and service accounts
├── docker-configs/            # 🐳 Docker Compose configurations
├── templates/                 # 📋 Documentation templates
├── UNIFIED_MONITORING_STRATEGY.md    # 🏭 Unified monitoring architecture
├── SERVER_CLAUDE_DEPLOYMENT_PACKAGE.md  # 🚀 Production deployment guide
├── STACK-OVERVIEW.md         # Aggregated view of all components
└── README.md                 # Project documentation
```

## Major System Components

### 🤖 Discord Automation (PRIMARY WORKFLOW)
- **Real-time task creation** via Discord commands (`!task description`)
- **Mobile-first operations** using iPhone Discord app
- **Automated task processing** with Mac Claude worker
- **24/7 persistent operation** via Docker containers and systemd services
- **Proven end-to-end automation**: CT-049 successfully completed via Discord → Sheets → Mac Claude

### 🏭 Steel Bonnet Brewery Implementation
- **Complete industrial implementation** with real brewery equipment
- **OPC UA to MQTT translation** for equipment monitoring
- **Node-RED flows** for brewery-specific automation
- **Ignition HMI integration** with custom UDTs and views

### 🏥 Unified Monitoring System
- **Complete stack monitoring**: Docker containers, MQTT brokers, Node-RED flows, Ignition Gateway
- **Auto-restart capabilities** for failed services
- **Mobile alerts** via Discord and WhatsApp integration
- **Google Sheets dashboard** for centralized monitoring

## How to Use
1. Each technology maintainer updates their component folder
2. Run aggregation script to update STACK-OVERVIEW.md
3. Use STACK-OVERVIEW.md for unified view of entire stack

## 📊 Documentation Standards (Based on INDEX.md)
**ALWAYS check INDEX.md first for organization patterns!** 

### File Organization Standards:
- **Naming Convention**: ALL_CAPS.md for guides (INTEGRATION-GUIDE.md)
- **Emoji Indicators**: 🚀 (start), 📚 (docs), 🔧 (tools), 🏭 (industry), 📱 (integration)
- **Hierarchical Structure**: Component → Implementation → Resources
- **Cross-references**: Always link to related technologies

### When Adding New Technology:
1. **Check INDEX.md first** for similar existing patterns
2. **Follow the hierarchy**: Quick Start → Core Docs → Components → Steel Bonnet → Tools
3. **Add to appropriate section** in INDEX.md
4. **Include cross-references** to related technologies
5. **Update last modified date** in INDEX.md

### User-Based Navigation:
- **New Team Members**: START_HERE.md → QUICK-TOUR.md → Quick Setup
- **Developers**: Local Development → Testing Guide → Scripts
- **Operators**: Steel Bonnet Setup → WhatsApp → Discord
- **System Admins**: Server Setup → Docker → Monitoring

## 🔧 Essential System Endpoints
### Discord Automation (PRIMARY WORKFLOW)
- **Mac Claude Channel**: #mac-claude in "slims agents" Discord server
- **Server Claude Channel**: #server-claude (to be created by Server Claude)
- **Bot Commands**: @Mac Claude Bot add task [description]
- **Task Workers**: scripts/mac_claude_task_worker.py, scripts/server_claude_task_worker.py
- **Real-time Mobile**: Discord iPhone app for instant task management

### Node-RED
- **UI**: http://localhost:1880
- **Dashboard**: http://localhost:1880/ui
- **Flows API**: http://localhost:1880/flows

### n8n Workflow Automation  
- **UI**: http://localhost:5678
- **API**: http://localhost:5678/api/v1
- **Webhooks**: http://localhost:5678/webhook

### GitHub Integration
- **Repository**: https://github.com/slimstrongarm/industrial-iot-stack
- **Actions**: https://github.com/slimstrongarm/industrial-iot-stack/actions  
- **Issues**: https://github.com/slimstrongarm/industrial-iot-stack/issues

### Key Infrastructure
- **Ignition Gateway**: http://localhost:8088
- **Ignition Designer**: opc.tcp://localhost:62541
- **MQTT Broker**: localhost:1883
- **Google Sheets**: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do

## 📋 Required Reading for New Instances
New Claude instances MUST read these files for complete context:
- INDEX.md (organization standards and navigation)
- GOOGLE_SHEETS_FEATURES.md (Google Sheets API setup)  
- Steel_Bonnet/README.md (brewery implementation)
- credentials/README.md (API access patterns)

# important-instruction-reminders
Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving the Human Architects goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.
TEST scripts are meant to test functionaility. removing functions or features is never an option unless expicitely told by Human. Testing should look for items that are not working correctly and work towards those items functioning NOT removing them just to complete the test.
Please clean up any files that you've created for testing or debugging purposes after they're no longer needed.

## 🔍 ALWAYS CHECK FIRST
Before claiming "no access" to any system:
1. **Discord Automation**: Check if task can be created via @Mac Claude Bot add task [description]
2. **Google Sheets**: Check credentials/iot-stack-credentials.json and scripts/*google*sheets*.py
3. **Task Workers**: Check if mac_claude_task_worker.py or server_claude_task_worker.py can handle the task
4. **APIs**: Check credentials/ folder for service account files
5. **Documentation patterns**: Check INDEX.md for existing organization
6. **Scripts**: Search scripts/ directory for existing automation
7. **Endpoints**: Use the system endpoints listed above

## 📊 Google Sheets Claude Tasks - CRITICAL PRIORITY
- This is the LIVING TO-DO LIST that drives all project work
- Update with EVERY significant action or accomplishment  
- Always use existing scripts in scripts/ directory
- Spreadsheet ID: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do
