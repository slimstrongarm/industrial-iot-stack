# 🤖 Industrial IoT Claude Discord Bot

Enhanced Discord bot following `.claude` standards for real-time Industrial IoT system interaction.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install discord.py aiohttp gspread google-auth google-auth-oauthlib google-auth-httplib2
```

### 2. Setup Discord Bot Token

**Option 1: Environment Variable**
```bash
export DISCORD_BOT_TOKEN='your_discord_bot_token_here'
```

**Option 2: Local .env file (Recommended)**
```bash
# Create discord-bot/.env file (already exists)
echo "DISCORD_BOT_TOKEN=your_token_here" > discord-bot/.env
```

**⚠️ Security Note**: The .env file is gitignored and tokens are never committed to the repository.

### 3. Validate Setup
```bash
python3 discord-bot/test_bot_setup.py
```

### 4. Start Bot
```bash
python3 discord-bot/industrial_iot_claude_bot.py
```

## 📱 Discord Commands

### System Status
- `@claude status` - Complete Industrial IoT stack overview
- `@claude health` - System health check with alerts
- `@claude mqtt` - MQTT broker detailed status
- `@claude docker` - Docker container status
- `@claude node-red` - Node-RED specific status

### Task Management
- `@claude add task <description>` - Create new Claude task
- `@claude tasks` - View current tasks from Google Sheets

### Help & Information
- `@claude help` - Complete command reference

## 🏭 Features

### Real-time Monitoring
- **System Health**: Automatic monitoring of Node-RED, MQTT, Docker
- **Proactive Alerts**: Background monitoring with Discord notifications
- **Container Status**: Real-time Docker container health tracking

### Industrial IoT Integration
- **Node-RED**: Flow status and endpoint access
- **MQTT Broker**: Connection status and logs
- **Ignition Edge**: Gateway connectivity monitoring
- **n8n Workflows**: Automation system status

### Google Sheets Integration
- **Claude Tasks**: Direct integration with task tracking spreadsheet
- **Task Creation**: Create new tasks via Discord commands
- **Status Updates**: Real-time task status synchronization

### Mobile-First Design
- **Rich Embeds**: Clean, organized Discord interface
- **Quick Commands**: Optimized for mobile Discord app
- **Instant Response**: Fast troubleshooting from anywhere

## 🔧 System Endpoints

Following `.claude` standards, the bot monitors these endpoints:

- **Node-RED**: http://localhost:1880
- **n8n**: http://localhost:5678  
- **Ignition**: http://localhost:8088
- **MQTT**: localhost:1883
- **Google Sheets**: [Claude Tasks](https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do)

## 📊 Google Sheets Integration

The bot integrates with the existing Google Sheets Claude Tasks system:

- **Spreadsheet ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **Credentials**: `credentials/iot-stack-credentials.json`
- **Service Account**: `iiot-stack-automation@iiot-stack-automation.iam.gserviceaccount.com`

## 🧪 Testing

### Validation Script
```bash
python3 discord-bot/test_bot_setup.py
```

**Checks:**
- ✅ Python dependencies
- ✅ Discord bot token  
- ✅ Google Sheets credentials
- ✅ Bot script syntax
- ℹ️ System endpoints status
- ℹ️ Docker containers status

### Discord Test Commands
```
@claude hello
@claude status  
@claude mqtt
@claude docker
@claude help
```

## 🔒 Security

### Environment Variables
- `DISCORD_BOT_TOKEN` - Discord bot authentication
- Google Sheets credentials in secure JSON file

### Permissions Required
- **Send Messages**: Post responses and alerts
- **Read Message History**: Process commands
- **Use Embed Links**: Rich Discord interface
- **Attach Files**: Log file sharing

## 🚨 Troubleshooting

### Bot Not Responding
1. Check bot is online in Discord server
2. Verify bot has channel permissions
3. Ensure using `@claude` mention format

### Google Sheets Errors
1. Verify `credentials/iot-stack-credentials.json` exists
2. Check service account has spreadsheet access
3. Validate JSON credential format

### System Monitoring Issues
1. Check Docker accessibility: `docker ps`
2. Verify endpoint availability: `curl http://localhost:1880`
3. Review bot logs for specific errors

## 📈 Success Metrics

- ✅ **Real-time Interaction**: Instant Discord ↔ Claude communication
- ✅ **Mobile Access**: Full system control from iPhone Discord app
- ✅ **Proactive Monitoring**: Automatic alerts for system issues
- ✅ **Task Integration**: Seamless Google Sheets task management
- ✅ **Industrial IoT Context**: Equipment-aware responses

## 🎯 Next Steps

1. **Deploy to Production**: Move from development to brewery demo environment
2. **Cross-Instance Communication**: Coordinate with Server Claude instance
3. **Advanced Monitoring**: Add equipment-specific alerts
4. **Voice Commands**: Discord voice message support
5. **Automated Actions**: Self-healing system responses

---

**Following `.claude` standards**: Google Sheets priority, INDEX.md organization, system endpoint awareness, and comprehensive Industrial IoT integration.