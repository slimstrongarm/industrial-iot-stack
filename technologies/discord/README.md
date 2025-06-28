# Discord Technology Stack Documentation
*Quick reference for Claude instances working on Discord bots and integrations*

## 🎯 Quick Start for New Claude Instances

**Working on Discord?** Start here:
1. **Bot Setup**: `bots/discord-bot/README.md` - Complete Discord bot implementation
2. **Integration**: `setup-guides/` - Connect Discord to Google Sheets & other services
3. **Webhooks**: `webhooks/` - Notification configurations
4. **Production**: `bots/discord-bot/FINAL_BOT_SUMMARY.md` - Production deployment

## 📂 File Organization

### Bots
- **Industrial IoT Claude Bot** - Task automation via Discord commands
- **Google Sheets Integration** - Create tasks from Discord → Sheets
- **Multi-Instance Support** - Mac Claude & Server Claude coordination
- **Docker Deployment** - 24/7 bot operation

### Integrations
- **Google Sheets** - Task creation and tracking
- **WhatsApp Bridge** - Cross-platform notifications
- **GitHub Webhooks** - Repository activity alerts
- **Monitoring Alerts** - System health notifications

### Setup Guides
- **Token Configuration** - Discord bot token setup
- **OAuth Setup** - Permission configuration
- **Webhook Creation** - Discord webhook endpoints
- **Production Migration** - Deploy to server

## 🔗 Related Technologies

- **Google Sheets**: `../google-sheets/` - Task tracking integration
- **Docker**: `../docker/` - Containerized bot deployment
- **n8n**: `../n8n/` - Workflow automation triggers
- **GitHub Actions**: `../github-actions/` - CI/CD notifications

## 📊 Current Projects Using Discord

- **Task Automation**: Create Claude tasks via Discord commands
- **System Monitoring**: Real-time alerts for system health
- **Cross-Claude Coordination**: Mac & Server Claude communication
- **Mobile Operations**: iPhone Discord app for field management

## 🎯 Common Discord Patterns in This Stack

1. **Task Creation**: `!task description` → Google Sheets → Claude worker
2. **Status Updates**: Bot posts completion notifications
3. **Error Alerts**: System failures → Discord notifications
4. **Cross-Instance**: Mac Claude ↔ Server Claude coordination
5. **Mobile Access**: Full task management from iPhone app

## 💡 Discord Bot Commands

```
# Task Management
!task <description>     # Create new task for Claude
!status                 # Check current task status
!complete CT-XXX        # Mark task as complete

# System Commands  
!health                 # Check system health
!restart <service>      # Restart a service
!logs <service>         # View recent logs

# Coordination
@Mac Claude Bot         # Assign to Mac Claude
@Server Claude Bot      # Assign to Server Claude
```

## 🏭 Production Features

- **24/7 Operation**: Docker + systemd service
- **Auto-Restart**: Health monitoring with auto-recovery
- **Multi-Channel**: Separate channels for different instances
- **Mobile-First**: Optimized for Discord mobile app
- **Task Queue**: Automatic task assignment and processing

---
*Last Updated: 2025-06-28 | Files: Being organized | Status: Active Development*