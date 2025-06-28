# 🚀 Discord Bot Quick Fix - Using Your Existing Tokens

## The Problem
Both Mac Claude and Server Claude are trying to use the same `DISCORD_BOT_TOKEN` environment variable, causing connection conflicts.

## The Solution
Use separate environment variables for each bot:
- **Mac Claude**: `MAC_DISCORD_BOT_TOKEN`
- **Server Claude**: `SERVER_DISCORD_BOT_TOKEN`

## Quick Fix Steps

### On Mac Claude:
```bash
# Copy your existing Mac bot token to the new variable
export MAC_DISCORD_BOT_TOKEN="$DISCORD_BOT_TOKEN"

# Run the fix script
./scripts/fix_discord_bidirectional.sh
```

### On Server Claude:
```bash
# SSH to server, then:
export SERVER_DISCORD_BOT_TOKEN="$DISCORD_BOT_TOKEN"

# Run the fix script
./scripts/fix_discord_bidirectional.sh
```

## What This Fixes
✅ Mac Claude will now **send AND listen** to messages  
✅ Server Claude will now **listen AND send** proactive messages  
✅ Both bots can run simultaneously without conflicts  
✅ Google Sheets integration works on both  

## Testing
After starting both bots:

**In #mac-claude:**
```
@Mac Claude Bot status
@Mac Claude Bot add task Test Mac bidirectional
```

**In #server-claude:**
```
@Server Claude Bot status  
@Server Claude Bot add task Test Server bidirectional
```

## Permanent Setup
Add to your shell profile (`.bashrc` or `.zshrc`):

**Mac:**
```bash
export MAC_DISCORD_BOT_TOKEN='your_mac_token_here'
```

**Server:**
```bash
export SERVER_DISCORD_BOT_TOKEN='your_server_token_here'
```

## Need Help?
The `unified_claude_bot.py` automatically detects which instance it's running on and uses the appropriate token!