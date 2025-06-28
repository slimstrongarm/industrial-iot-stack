#!/bin/bash
echo "🤖 Starting Mac Claude Discord Bot..."
echo "=====================================>"

cd ~/Desktop/industrial-iot-stack

# Check if token is set
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    echo "❌ DISCORD_BOT_TOKEN not set!"
    echo "Get token from Discord Developer Portal:"
    echo "1. Go to https://discord.com/developers/applications"
    echo "2. Create new application: 'Mac Claude Bot'"
    echo "3. Go to Bot section"
    echo "4. Get token and run:"
    echo "   export DISCORD_BOT_TOKEN='your_mac_token_here'"
    echo "   ./scripts/start_mac_discord_bot.sh"
    exit 1
fi

# Install dependencies if needed
if ! python3 -c "import discord, gspread" 2>/dev/null; then
    echo "📦 Installing Discord bot dependencies..."
    pip3 install discord.py gspread google-auth
fi

echo "🚀 Starting Mac Claude Discord Bot..."
python3 discord-bot/unified_claude_bot.py