#!/bin/bash
# Restart Mac Claude Bot with fixes

echo "🛑 Stopping any existing bot instances..."
pkill -f "industrial_iot_claude_bot.py" || true
pkill -f "run_mac_claude_bot.py" || true

echo "⏳ Waiting for clean shutdown..."
sleep 2

echo "🚀 Starting Mac Claude Bot with fixes..."
cd /Users/joshpayneair/Desktop/industrial-iot-stack/discord-bot
python3 run_mac_claude_bot.py