#!/bin/bash
# 🤖 Discord Bot Token Setup
# Sets up environment variables for both Mac Claude and Server Claude bots

echo "🤖 Setting up Discord Bot Tokens"
echo "=================================="

# Mac Claude Bot Token (MCB)
export MAC_DISCORD_BOT_TOKEN="${MAC_DISCORD_BOT_TOKEN:-}"

# Server Claude Bot Token (SCB) 
export SERVER_DISCORD_BOT_TOKEN="${SERVER_DISCORD_BOT_TOKEN:-}"

echo "✅ Mac Claude Bot Token: ${MAC_DISCORD_BOT_TOKEN:0:20}..."
echo "✅ Server Claude Bot Token: ${SERVER_DISCORD_BOT_TOKEN:0:20}..."

echo ""
echo "🚀 Now you can run:"
echo "   python3 industrial_iot_claude_bot.py"
echo ""
echo "The bot will automatically:"
echo "  - Detect if it's running on Mac or Server"
echo "  - Use the appropriate Discord bot token"
echo "  - Connect as the correct bot identity"
echo ""