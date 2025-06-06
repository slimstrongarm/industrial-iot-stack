# Server Claude Discord Bot Deployment Instructions

## 🎯 Quick Start

Josh has created the Discord server and added the invite link to a new **'Discord' tab** in Google Sheets.

## 📋 Your Tasks (CT-022 through CT-027)

### CT-022: Create Discord Bot Application
1. Go to https://discord.com/developers/applications
2. Create new application: "IoT Stack Claude Bot"
3. Add bot user and copy token
4. Check the **'Discord' tab** in Google Sheets for the server invite link

### CT-023: Deploy Discord Bot
1. Bot code is ready in `/discord-bot/` folder:
   - `bot.py` - Complete Discord bot code
   - `docker-compose.yml` - Deployment configuration
   - `Dockerfile` - Container setup

2. Deploy with:
   ```bash
   cd /opt/industrial-iot-stack/discord-bot
   echo "DISCORD_BOT_TOKEN=your-bot-token-here" > .env
   docker-compose up -d
   ```

### CT-024: Connect to Google Sheets
- Bot will use existing credentials at `/opt/industrial-iot-stack/credentials/`
- Update bot.py to read from Claude Tasks sheet

### CT-025: Implement Commands
- Basic commands already in bot.py:
  - "status" - Docker container status
  - "mqtt" - MQTT broker check
  - "help" - Command list

### CT-026: Setup Alerts
- Add Docker event monitoring
- Post container failures to #alerts channel

### CT-027: Production Deployment
- Ensure bot auto-restarts
- Add to server startup scripts

## 🚀 Key Points

1. **Discord server is ready** - Josh created it this morning
2. **Invite link is in the 'Discord' tab** of our Google Sheets
3. **Bot code is in GitHub** - Just pulled with latest updates
4. **This is a development tool** - For Josh to coordinate with us remotely
5. **Not part of brewery POC** - Internal tool only

## 📱 Expected Result

Josh will be able to send commands from his iPhone:
- To you in #server-claude channel
- To Mac Claude in #mac-claude channel
- Coordinate POC development while mobile

---
Generated: 2025-06-04 06:28
Mac Claude
