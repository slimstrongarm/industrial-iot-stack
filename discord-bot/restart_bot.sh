#!/bin/bash
# Restart Discord bot with updated Google Sheets integration

echo "🤖 Restarting Industrial IoT Claude Discord Bot..."
echo "=================================================="

# Kill existing bot process
pkill -f "industrial_iot_claude_bot.py" 2>/dev/null

# Set Discord token from .env
# Load token from .env file
if [ -f "discord-bot/.env" ]; then
    export $(grep -v '^#' discord-bot/.env | xargs)
fi

# Start bot in background
cd /Users/joshpayneair/Desktop/industrial-iot-stack
nohup python3 discord-bot/industrial_iot_claude_bot.py > discord-bot/bot.log 2>&1 &

echo "✅ Bot restarted with Google Sheets task creation capability"
echo "📋 New features:"
echo "  • Automatically creates new task IDs (CT-XXX)"
echo "  • Adds tasks directly to Google Sheets"
echo "  • Tracks who created the task"
echo ""
echo "💬 Test in Discord: @claude add task Test Google Sheets integration"
echo "📄 Bot logs: discord-bot/bot.log"