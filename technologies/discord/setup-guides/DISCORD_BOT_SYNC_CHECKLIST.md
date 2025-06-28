# 🔧 Discord Bot Settings Synchronization Checklist

## Critical Settings That MUST Match

### 1. **Privileged Gateway Intents** (Bot Section)
Both **Mac Claude Bot** and **Server Claude Bot** must have:
- ✅ **MESSAGE CONTENT INTENT** - REQUIRED! (Without this, bots can't read messages)
- ✅ **SERVER MEMBERS INTENT** - Recommended
- ✅ **PRESENCE INTENT** - Optional

### 2. **Bot Permissions** (OAuth2 → URL Generator)
Select these identical permissions for both:
- ✅ Send Messages
- ✅ Read Message History  
- ✅ Embed Links
- ✅ Read Messages/View Channels
- ✅ Use External Emojis
- ✅ Add Reactions
- ✅ Attach Files

### 3. **Bot Settings**
- ❌ **Public Bot** - Turn OFF (keep private)
- ❌ **Requires OAuth2 Code Grant** - Turn OFF

## Quick Sync Process

1. Go to https://discord.com/developers/applications
2. Open **Mac Claude Bot** application
3. Go to **Bot** section → Enable **MESSAGE CONTENT INTENT**
4. Go to **OAuth2** → **URL Generator**:
   - Scopes: `bot`
   - Permissions: Check all from list above
   - Save the generated invite URL
5. Repeat for **Server Claude Bot** application

## Test After Sync

Kill current bot and restart:
```bash
# Kill old bot
pkill -f "discord-bot.*\.py"

# Set token and start
export MAC_DISCORD_BOT_TOKEN="your_mac_token"
python3 discord-bot/unified_claude_bot.py
```

## Expected Result
✅ Both bots can read AND respond to messages
✅ Natural language processing works
✅ Google Sheets integration functional
✅ Bidirectional communication enabled

## Common Issues
- **Bot not responding**: MESSAGE CONTENT INTENT not enabled
- **Can't read messages**: Wrong intents configuration  
- **Permission errors**: Mismatched OAuth2 permissions