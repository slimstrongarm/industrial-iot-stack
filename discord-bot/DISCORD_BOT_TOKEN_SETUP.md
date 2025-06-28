# 🤖 Discord Bot Token Setup Guide

## The Problem
Mac Claude talks but doesn't listen, Server Claude listens but doesn't talk properly. 

**Root Cause**: You need **separate Discord bot tokens** - Discord won't let the same bot connect twice!

## 🚀 Quick Fix Steps

### 1. Create Mac Claude Bot Application
1. Go to https://discord.com/developers/applications
2. Click **"New Application"**
3. Name: **"Mac Claude Bot"**
4. Go to **"Bot"** section in left sidebar
5. Click **"Reset Token"** and copy the token
6. **Save this as `MAC_DISCORD_TOKEN`**

### 2. Create Server Claude Bot Application  
1. Click **"New Application"** again
2. Name: **"Server Claude Bot"**
3. Go to **"Bot"** section
4. Click **"Reset Token"** and copy the token
5. **Save this as `SERVER_DISCORD_TOKEN`**

### 3. Add Both Bots to Your Discord Server
For **Mac Claude Bot**:
1. Go to **"OAuth2" > "URL Generator"**
2. Check: **"bot"**
3. Bot Permissions: **"Send Messages", "Read Message History", "Use Slash Commands"**
4. Copy generated URL and open in browser
5. Add to your Discord server

For **Server Claude Bot**:
1. Repeat the same process for the Server Claude Bot application

### 4. Deploy Mac Claude Bot
```bash
# Set the Mac Claude token
export DISCORD_BOT_TOKEN='your_mac_token_here'

# Start the bot
./scripts/start_mac_discord_bot.sh
```

### 5. Deploy Server Claude Bot
Copy the unified bot to your server and run:
```bash
# On your server
export DISCORD_BOT_TOKEN='your_server_token_here'
python3 unified_claude_bot.py
```

## 🔧 Testing
After both bots are running:

**In #mac-claude channel:**
```
@Mac Claude Bot status
```

**In #server-claude channel:**
```
@Server Claude Bot add task Test bidirectional communication
```

Both should now **send AND receive** messages!

## 📋 Bot Permissions Required
- Send Messages
- Read Message History  
- Use Slash Commands
- Read Messages/View Channels
- Embed Links

## 🔍 Troubleshooting
- **"Bot not responding"**: Check if DISCORD_BOT_TOKEN is set correctly
- **"Permission denied"**: Make sure bot has proper permissions in Discord server
- **"Google Sheets error"**: Check credentials/iot-stack-credentials.json exists
- **"Same bot connecting twice"**: Must use different tokens for Mac vs Server

## 🎯 Expected Behavior After Fix
✅ Mac Claude: Sends messages AND listens to commands  
✅ Server Claude: Listens to commands AND sends proactive messages  
✅ Both create tasks in Google Sheets  
✅ Bidirectional coordination working!