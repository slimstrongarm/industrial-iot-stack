#!/bin/bash
# Setup Mac Claude Discord Bot Auto-start

echo "🍎 Setting up Mac Claude Discord Bot Auto-start"
echo "=============================================="

# Create a launch script
cat > ~/start_mac_claude_bot.sh << 'EOF'
#!/bin/bash
# Mac Claude Discord Bot Launcher

# Wait for network to be ready
sleep 10

# Navigate to project directory
cd ~/Desktop/industrial-iot-stack

# Check if bot is already running
if pgrep -f "industrial_iot_claude_bot.py" > /dev/null; then
    echo "Mac Claude bot is already running"
    exit 0
fi

# Start the bot with logging
echo "Starting Mac Claude Discord Bot..."
cd discord-bot
python3 run_mac_claude_bot.py >> ~/mac_claude_bot.log 2>&1 &

echo "Mac Claude bot started with PID: $!"
echo $! > ~/mac_claude_bot.pid
EOF

chmod +x ~/start_mac_claude_bot.sh

# Create LaunchAgent for macOS auto-start
mkdir -p ~/Library/LaunchAgents

cat > ~/Library/LaunchAgents/com.industrial-iot.mac-claude-bot.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.industrial-iot.mac-claude-bot</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>$HOME/start_mac_claude_bot.sh</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    
    <key>StandardOutPath</key>
    <string>/tmp/mac-claude-bot.log</string>
    
    <key>StandardErrorPath</key>
    <string>/tmp/mac-claude-bot.error.log</string>
    
    <key>WorkingDirectory</key>
    <string>$HOME/Desktop/industrial-iot-stack</string>
</dict>
</plist>
EOF

echo "✅ Auto-start files created!"
echo ""
echo "📋 To enable auto-start:"
echo "   launchctl load ~/Library/LaunchAgents/com.industrial-iot.mac-claude-bot.plist"
echo ""
echo "📋 To start immediately:"
echo "   ~/start_mac_claude_bot.sh"
echo ""
echo "📋 To check if running:"
echo "   ps aux | grep industrial_iot_claude_bot"
echo ""
echo "📋 To view logs:"
echo "   tail -f ~/mac_claude_bot.log"
echo ""
echo "📋 To stop the bot:"
echo "   kill \$(cat ~/mac_claude_bot.pid)"
echo ""
echo "📋 To disable auto-start:"
echo "   launchctl unload ~/Library/LaunchAgents/com.industrial-iot.mac-claude-bot.plist"