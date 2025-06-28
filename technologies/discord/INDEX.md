# Discord Technology Stack - Complete File Index
*Every Discord bot, integration, and configuration in the industrial IoT stack*

## 🚀 Quick Access for Claude Instances

**New to Discord in this codebase?** Start with:
1. `bots/discord-bot/README.md` - Complete bot implementation overview
2. `setup-guides/DISCORD_BOT_SETUP_GUIDE.md` - Step-by-step setup
3. `bots/discord-bot/industrial_iot_claude_bot.py` - Main production bot
4. `bots/discord-bot/GOOGLE_SHEETS_INTEGRATION.md` - Task automation setup

## 📂 Complete File Listing

### 🤖 Discord Bot Implementation
```
bots/discord-bot/
├── README.md                           # Complete bot documentation
├── FINAL_BOT_SUMMARY.md                # Production deployment summary
├── GOOGLE_SHEETS_INTEGRATION.md        # Sheets integration guide
├── TROUBLESHOOTING.md                  # Common issues and fixes
├── DISCORD_BOT_TOKEN_SETUP.md          # Token configuration
├── Python Bot Files:
│   ├── industrial_iot_claude_bot.py    # Main production bot
│   ├── unified_claude_bot.py           # Multi-instance coordinator
│   ├── mobile_friendly_bot.py          # Mobile-optimized version
│   ├── intelligent_choice_bot.py       # Smart task routing
│   ├── run_mac_claude_bot.py           # Mac Claude launcher
│   └── run_server_claude_bot.py        # Server Claude launcher
├── Testing & Debug:
│   ├── test_bot_setup.py               # Setup verification
│   ├── test_sheets_integration.py      # Sheets connection test
│   ├── quick_discord_test.py           # Quick connection test
│   ├── demo_bot_features.py            # Feature demonstration
│   └── start_bot_debug.py              # Debug mode launcher
├── Deployment:
│   ├── Dockerfile                      # Container definition
│   ├── docker-compose.yml              # Docker deployment
│   ├── claude-discord.service          # Systemd service
│   └── requirements.txt                # Python dependencies
└── Scripts & Utilities:
    ├── manage_bot.sh                   # Bot management script
    ├── restart_bot.sh                  # Quick restart
    ├── clean_start_bot.sh              # Clean startup
    └── setup_discord_tokens.sh         # Token setup helper
```

### ⚙️ Setup Guides (11 files)
```
setup-guides/
├── DISCORD_BOT_SETUP_GUIDE.md          # Complete setup process
├── DISCORD_BOT_PRODUCTION_MIGRATION.md # Move to production
├── DISCORD_BOT_PRODUCTION_STATUS.md    # Production status
├── DISCORD_BOT_QUICK_FIX.md            # Quick fixes
├── DISCORD_BOT_READY.md                # Deployment checklist
├── DISCORD_BOT_SYNC_CHECKLIST.md       # Sync verification
├── DISCORD_INTEGRATION_VISION.md       # Integration architecture
├── DISCORD_TOKEN_SETUP.md              # Token configuration
├── DISCORD_WORKFLOW_REVOLUTION.md      # Workflow automation
├── SERVER_CLAUDE_DISCORD_BOT_SETUP.md  # Server setup
└── SERVER_CLAUDE_DISCORD_INSTRUCTIONS.md # Server instructions
```

### 🔧 Reference & Architecture
```
reference/
├── CT-021_DISCORD_SETUP_LEGWORK.md     # Initial research & planning
└── DISCORD_BOT_START_TASK_FEATURE.md   # Task creation feature spec
```

### 🔗 Webhooks & Integrations
```
webhooks/
└── discord_webhook_config.json         # Webhook endpoints configuration
```

## 🎯 Discord Usage Patterns

### Bot Development
- **Initial Setup**: `setup-guides/DISCORD_BOT_SETUP_GUIDE.md`
- **Token Config**: `setup-guides/DISCORD_TOKEN_SETUP.md`
- **Production Deploy**: `setup-guides/DISCORD_BOT_PRODUCTION_MIGRATION.md`

### Integration Patterns
- **Google Sheets**: `bots/discord-bot/GOOGLE_SHEETS_INTEGRATION.md`
- **Task Automation**: `reference/DISCORD_BOT_START_TASK_FEATURE.md`
- **Multi-Instance**: `bots/discord-bot/unified_claude_bot.py`

### Testing & Debug
- **Test Setup**: `bots/discord-bot/test_bot_setup.py`
- **Sheets Test**: `bots/discord-bot/test_sheets_integration.py`
- **Quick Test**: `bots/discord-bot/quick_discord_test.py`

## 🔗 Related Technologies

- **Google Sheets**: `../google-sheets/` - Task tracking backend
- **Docker**: `../docker/` - Container deployment
- **Python Scripts**: `../../scripts/` - Task worker scripts
- **Monitoring**: `../../scripts/monitoring/` - Health checks

## 📊 Project Implementation Details

### Task Automation Workflow
1. User types `!task Build new feature` in Discord
2. Bot creates task in Google Sheets
3. Assigns to appropriate Claude instance
4. Task worker picks up and processes
5. Updates status: Pending → In Progress → Complete
6. Bot notifies completion in Discord

### Multi-Instance Coordination
- **Mac Claude Bot**: Green TMUX, local development
- **Server Claude Bot**: Blue TMUX, production services
- **Unified Bot**: Coordinates between instances

### Production Features
- **24/7 Operation**: Docker + systemd
- **Auto-Restart**: Health monitoring
- **Mobile Support**: iPhone Discord app
- **Multi-Channel**: Instance-specific channels

## 🎯 Common Discord Commands

```python
# Task Management
!task <description>      # Create new task
!status                  # Check task status
!list pending           # List pending tasks
!complete CT-XXX        # Mark task complete

# System Commands
!health                 # System health check
!restart <service>      # Restart service
!logs <service>         # View logs

# Assignment
@Mac Claude Bot task    # Assign to Mac Claude
@Server Claude Bot task # Assign to Server Claude
```

## 🏭 Production Deployment

### Docker Deployment
```bash
cd bots/discord-bot
docker-compose up -d
```

### Systemd Service
```bash
sudo cp claude-discord.service /etc/systemd/system/
sudo systemctl enable claude-discord
sudo systemctl start claude-discord
```

### Environment Variables
```bash
DISCORD_TOKEN=your_bot_token
GOOGLE_SHEETS_ID=1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do
WEBHOOK_URL=https://discord.com/api/webhooks/...
```

---
*Files Organized: 45+ | Last Updated: 2025-06-28 | Status: ✅ Ready for Claude*