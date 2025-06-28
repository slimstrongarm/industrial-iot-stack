#!/bin/bash
# Check Mac Claude Bot Status

echo "🍎 Mac Claude Discord Bot Status"
echo "================================"

# Check if bot is running
if pgrep -f "industrial_iot_claude_bot.py" > /dev/null; then
    PID=$(pgrep -f "industrial_iot_claude_bot.py")
    echo "✅ Bot is RUNNING (PID: $PID)"
    echo ""
    echo "📊 Process Info:"
    ps aux | grep industrial_iot_claude_bot | grep -v grep
else
    echo "❌ Bot is NOT running"
fi

echo ""
echo "📋 LaunchAgent Status:"
launchctl list | grep mac-claude-bot || echo "   Not loaded"

echo ""
echo "📄 Recent Log Entries:"
if [ -f ~/mac_claude_bot.log ]; then
    echo "---"
    tail -5 ~/mac_claude_bot.log
    echo "---"
else
    echo "   No log file found"
fi

echo ""
echo "🔧 Quick Commands:"
echo "   Start bot: ~/start_mac_claude_bot.sh"
echo "   View logs: tail -f ~/mac_claude_bot.log"
echo "   Stop bot: kill \$(cat ~/mac_claude_bot.pid)"