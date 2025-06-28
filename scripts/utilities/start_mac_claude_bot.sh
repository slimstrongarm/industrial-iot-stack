#!/bin/bash
# Start Mac Claude Discord Bot with proper token handling

echo "🤖 Mac Claude Discord Bot Launcher"
echo "=================================="

# Check if we have a Discord token
if [ -z "$DISCORD_BOT_TOKEN" ] && [ -z "$MAC_DISCORD_BOT_TOKEN" ]; then
    echo "❌ No Discord bot token found!"
    echo ""
    echo "Please set one of these environment variables:"
    echo "  export DISCORD_BOT_TOKEN='your_token_here'"
    echo "  export MAC_DISCORD_BOT_TOKEN='your_token_here'"
    exit 1
fi

# Set MAC_DISCORD_BOT_TOKEN from DISCORD_BOT_TOKEN if not already set
if [ -z "$MAC_DISCORD_BOT_TOKEN" ] && [ -n "$DISCORD_BOT_TOKEN" ]; then
    export MAC_DISCORD_BOT_TOKEN="$DISCORD_BOT_TOKEN"
    echo "✅ Using DISCORD_BOT_TOKEN for Mac Claude"
fi

# Export for child process
export MAC_DISCORD_BOT_TOKEN
export DISCORD_BOT_TOKEN="${MAC_DISCORD_BOT_TOKEN}"

echo "🔑 Token configured successfully"
echo ""

# Change to project directory
cd /Users/joshpayneair/Desktop/industrial-iot-stack

# Check Python dependencies
echo "📦 Checking dependencies..."
if ! python3 -c "import discord, gspread" 2>/dev/null; then
    echo "Installing required packages..."
    pip3 install discord.py gspread google-auth
fi

echo ""
echo "🚀 Starting Mac Claude Discord Bot..."
echo "===================================="
echo "Instance: Mac Claude"
echo "Channels: #mac-claude, #general"
echo "Token: ${MAC_DISCORD_BOT_TOKEN:0:10}..."
echo "===================================="
echo ""

# Run the bot with explicit environment
exec python3 discord-bot/unified_claude_bot.py