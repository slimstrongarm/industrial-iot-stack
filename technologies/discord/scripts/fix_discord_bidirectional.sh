#!/bin/bash
# Fix Discord Bidirectional Communication

echo "🤖 Discord Bot Bidirectional Fix"
echo "================================"

# Determine which instance we're on
HOSTNAME=$(hostname | tr '[:upper:]' '[:lower:]')
INSTANCE="Mac"

if [[ "$HOSTNAME" == *"server"* ]] || [[ "$HOSTNAME" == *"flint"* ]] || [[ "$HOSTNAME" == *"linux"* ]]; then
    INSTANCE="Server"
fi

echo "📍 Detected Instance: $INSTANCE Claude"
echo ""

# Check current bot processes
echo "🔍 Checking existing Discord bot processes..."
if pgrep -f "discord-bot.*\.py" > /dev/null; then
    echo "⚠️  Found running Discord bot processes:"
    ps aux | grep -E "discord-bot.*\.py" | grep -v grep
    echo ""
    read -p "Kill existing processes? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -f "discord-bot.*\.py"
        echo "✅ Killed existing processes"
        sleep 2
    fi
fi

# Set up environment based on instance
if [ "$INSTANCE" == "Server" ]; then
    echo "🔧 Setting up Server Claude Discord Bot..."
    echo ""
    
    if [ -z "$SERVER_DISCORD_BOT_TOKEN" ]; then
        echo "❌ SERVER_DISCORD_BOT_TOKEN not set!"
        echo ""
        echo "Please run:"
        echo "  export SERVER_DISCORD_BOT_TOKEN='your_server_bot_token'"
        echo ""
        echo "Or if you have DISCORD_BOT_TOKEN set:"
        echo "  export SERVER_DISCORD_BOT_TOKEN=\$DISCORD_BOT_TOKEN"
        exit 1
    fi
    
    echo "✅ Token found for Server Claude"
    
else
    echo "🔧 Setting up Mac Claude Discord Bot..."
    echo ""
    
    if [ -z "$MAC_DISCORD_BOT_TOKEN" ]; then
        echo "❌ MAC_DISCORD_BOT_TOKEN not set!"
        echo ""
        echo "Please run:"
        echo "  export MAC_DISCORD_BOT_TOKEN='your_mac_bot_token'"
        echo ""
        echo "Or if you have DISCORD_BOT_TOKEN set:"
        echo "  export MAC_DISCORD_BOT_TOKEN=\$DISCORD_BOT_TOKEN"
        exit 1
    fi
    
    echo "✅ Token found for Mac Claude"
fi

# Check Python dependencies
echo ""
echo "📦 Checking Python dependencies..."
if ! python3 -c "import discord, gspread" 2>/dev/null; then
    echo "Installing required packages..."
    pip3 install discord.py gspread google-auth
fi

# Start the bot
echo ""
echo "🚀 Starting $INSTANCE Claude Discord Bot..."
echo "============================================"
echo ""

cd ~/Desktop/industrial-iot-stack 2>/dev/null || cd /opt/claude 2>/dev/null || cd .

# Run with proper environment
if [ "$INSTANCE" == "Server" ]; then
    export DISCORD_BOT_TOKEN=$SERVER_DISCORD_BOT_TOKEN
else  
    export DISCORD_BOT_TOKEN=$MAC_DISCORD_BOT_TOKEN
fi

python3 discord-bot/unified_claude_bot.py