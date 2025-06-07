#!/bin/bash
# Clean start for Discord bot to prevent duplicates

echo "🧹 Clean Discord Bot Start"
echo "========================="
echo

# Kill any existing Python Discord bot processes
echo "1️⃣ Stopping any existing bot processes..."
pkill -f "industrial_iot_claude_bot.py" 2>/dev/null
pkill -f "simple_test_bot.py" 2>/dev/null
pkill -f "discord.*bot.*py" 2>/dev/null
sleep 2

# Clear old bot log
echo "2️⃣ Clearing old bot log..."
> /Users/joshpayneair/Desktop/industrial-iot-stack/discord-bot/bot.log

# Start fresh
echo "3️⃣ Starting fresh bot instance..."
# Load token from .env file
if [ -f "discord-bot/.env" ]; then
    export $(grep -v '^#' discord-bot/.env | xargs)
fi
cd /Users/joshpayneair/Desktop/industrial-iot-stack
nohup python3 discord-bot/industrial_iot_claude_bot.py > discord-bot/bot.log 2>&1 &
BOT_PID=$!

echo "✅ Bot started with PID: $BOT_PID"
echo

# Wait and check status
sleep 5
if ps -p $BOT_PID > /dev/null; then
    echo "✅ Bot is running successfully!"
    echo "📄 Check logs: tail -f discord-bot/bot.log"
    echo
    echo "💡 Note about duplicate bots in Discord:"
    echo "   • The offline bot is a 'ghost' from the previous session"
    echo "   • It will disappear in 5-10 minutes automatically"
    echo "   • Or you can right-click → Kick the offline bot"
    echo
    echo "🎯 Use the bot showing as 'Online' with green dot"
else
    echo "❌ Bot failed to start. Check logs:"
    tail -20 discord-bot/bot.log
fi