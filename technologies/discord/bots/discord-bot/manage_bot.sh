#!/bin/bash
# Manage Discord bot processes safely

case "$1" in
    stop)
        echo "🛑 Stopping Discord bot processes..."
        # Only kill our specific bot scripts
        pkill -f "industrial_iot_claude_bot.py" 2>/dev/null
        pkill -f "simple_test_bot.py" 2>/dev/null
        pkill -f "start_bot_debug.py" 2>/dev/null
        echo "✅ Discord bots stopped"
        ;;
    
    start)
        echo "🚀 Starting Industrial IoT Discord bot..."
        # Use token from environment or .env file
        if [ -z "$DISCORD_BOT_TOKEN" ] && [ -f "discord-bot/.env" ]; then
            export $(grep -v '^#' discord-bot/.env | xargs)
        fi
        cd /Users/joshpayneair/Desktop/industrial-iot-stack
        nohup python3 discord-bot/industrial_iot_claude_bot.py > discord-bot/bot.log 2>&1 &
        echo "✅ Bot started (PID: $!)"
        echo "📄 Logs: tail -f discord-bot/bot.log"
        ;;
    
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    
    status)
        echo "📊 Discord bot status:"
        if pgrep -f "industrial_iot_claude_bot.py" > /dev/null; then
            echo "✅ Industrial IoT bot is running"
            pgrep -f "industrial_iot_claude_bot.py"
        else
            echo "❌ Industrial IoT bot is not running"
        fi
        ;;
    
    test)
        echo "🧪 Starting simple test bot..."
        $0 stop
        cd /Users/joshpayneair/Desktop/industrial-iot-stack
        python3 discord-bot/simple_test_bot.py
        ;;
    
    *)
        echo "Usage: $0 {start|stop|restart|status|test}"
        exit 1
        ;;
esac