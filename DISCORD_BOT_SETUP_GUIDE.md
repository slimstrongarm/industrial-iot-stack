# 🤖 Discord Bot Setup & Testing Guide

## Quick 5-Minute Setup

### 1. Create Discord Application
1. Go to: **https://discord.com/developers/applications**
2. Click **"New Application"**
3. Name: **"Industrial IoT Claude Bot"**
4. Click **"Create"**

### 2. Create Bot
1. Go to **"Bot"** section in left sidebar
2. Click **"Add Bot"**
3. Under **"Token"** section, click **"Copy"**
4. **Save this token securely** - you'll need it in step 4

### 3. Set Bot Permissions
1. Go to **"OAuth2"** → **"URL Generator"**
2. **Scopes**: Check ✅ `bot` and ✅ `applications.commands`
3. **Bot Permissions**: Check these:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Use Embed Links
   - ✅ Read Messages

4. **Copy the generated URL** and open it
5. **Select your Discord server** and authorize

### 4. Configure & Test
```bash
# Set the bot token (replace YOUR_TOKEN_HERE)
export DISCORD_BOT_TOKEN='YOUR_TOKEN_HERE'

# Start the bot
python3 scripts/discord_claude_bot.py
```

## Expected Output
```
🤖 Discord Claude Bot - Industrial IoT Integration
============================================================
✅ Discord bot token found
🚀 Starting bot with Industrial IoT context...
📢 Bot will respond to @claude mentions
⚡ Real-time Discord ↔ Claude integration active!

Press Ctrl+C to stop

🤖 Discord Claude Bot logged in as Industrial IoT Claude Bot#1234
📊 Connected to 1 servers
✅ Startup notification sent to Discord
```

## Test Commands in Discord

### Basic Test
```
@claude hello
```
**Expected Response**: Welcome message with Industrial IoT context

### System Status Test  
```
@claude status
```
**Expected Response**: Complete IoT stack status (Docker, MQTT, n8n)

### Equipment Test
```
@claude check reactor temperature
```
**Expected Response**: Equipment monitoring guidance with MQTT topics

### Help Test
```
@claude help
```
**Expected Response**: Full command reference and capabilities

## Troubleshooting

### Bot Not Responding
- ✅ Check bot is online in Discord server
- ✅ Verify bot has permissions in the channel
- ✅ Make sure you're using @claude (not just "claude")

### Permission Errors
- ✅ Bot needs "Send Messages" permission
- ✅ Bot needs "Use Embed Links" for rich responses
- ✅ Check channel-specific permissions

### Connection Issues
- ✅ Verify token is correct and not expired
- ✅ Check internet connectivity
- ✅ Discord API might be temporarily down

## Success Indicators

### ✅ Working Correctly
- Bot appears online in Discord
- Startup notification appears in Discord
- @claude mentions get instant responses
- Responses include Industrial IoT context
- Rich embeds display properly

### 🚀 Advanced Features Working
- Equipment status queries work
- MQTT broker information included
- System health reporting active
- Context-aware troubleshooting guidance

## Integration Status

Once working, you'll have:
- **Live Discord ↔ Claude chat**
- **Industrial IoT awareness** in all responses  
- **Equipment monitoring** via Discord
- **Real-time system interaction**
- **Team collaboration** through shared Discord interface

This transforms Discord into your **live Industrial IoT command center**! 🎉

---

**Files Ready:**
- ✅ `scripts/discord_claude_bot.py` - Main bot script
- ✅ `scripts/test_discord_bot_setup.py` - Setup verification
- ✅ `discord_webhook_config.json` - Webhook integration

**Status**: 🟢 **READY FOR TOKEN** (5-minute setup)