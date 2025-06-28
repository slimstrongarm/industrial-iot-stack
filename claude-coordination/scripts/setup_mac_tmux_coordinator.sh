#!/bin/bash
# Setup Mac TMUX Coordinator Instance
# This creates a Mac-specific TMUX session that coordinates with the server

set -e

echo "🍎 Setting up Mac TMUX Coordinator"
echo "=================================="

# Create Mac-specific TMUX config
cat > ~/.tmux.conf.mac-claude << 'EOF'
# Mac Claude TMUX Configuration
set -g default-terminal "screen-256color"
set -g history-limit 50000
set -g status-bg green  # Green for Mac (vs Blue for Server)
set -g status-fg black
set -g status-left '[🍎 Mac Claude]'
set -g status-right '%H:%M %d-%b-%y'

# Enable mouse support
set -g mouse on

# Window naming
set-option -g allow-rename off
set-window-option -g automatic-rename off

# Activity monitoring
setw -g monitor-activity on
set -g visual-activity on
EOF

# Create Mac TMUX session launcher
cat > ~/start_mac_claude.sh << 'EOF'
#!/bin/bash
# Start or attach to Mac Claude TMUX session

SESSION_NAME="claude-mac"
WORK_DIR="$HOME/Desktop/industrial-iot-stack"

# Check if session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    echo "🍎 Creating new Mac Claude session..."
    
    # Create new session with Mac config
    tmux -f ~/.tmux.conf.mac-claude new-session -d -s $SESSION_NAME -c $WORK_DIR
    
    # Window 0: Main Mac workspace
    tmux rename-window -t $SESSION_NAME:0 'mac-main'
    tmux send-keys -t $SESSION_NAME:0 'cd ~/Desktop/industrial-iot-stack' C-m
    tmux send-keys -t $SESSION_NAME:0 'echo "🍎 Mac Claude Coordinator Ready"' C-m
    tmux send-keys -t $SESSION_NAME:0 'echo "📊 Google Sheets Integration Active"' C-m
    
    # Window 1: Google Sheets Monitor
    tmux new-window -t $SESSION_NAME:1 -n 'sheets-monitor'
    tmux send-keys -t $SESSION_NAME:1 'cd ~/Desktop/industrial-iot-stack' C-m
    tmux send-keys -t $SESSION_NAME:1 'python3 scripts/sheets_monitor_live.py' C-m
    
    # Window 2: Server Sync Monitor
    tmux new-window -t $SESSION_NAME:2 -n 'server-sync'
    tmux send-keys -t $SESSION_NAME:2 'cd ~/Desktop/industrial-iot-stack' C-m
    tmux send-keys -t $SESSION_NAME:2 'watch -n 30 "git pull && echo && cat agents/SESSION_STATE.json | jq .currentWork.lastAction"' C-m
    
    # Window 3: Git Operations
    tmux new-window -t $SESSION_NAME:3 -n 'git-ops'
    tmux send-keys -t $SESSION_NAME:3 'cd ~/Desktop/industrial-iot-stack && git status' C-m
    
    # Window 4: Local Services
    tmux new-window -t $SESSION_NAME:4 -n 'local-services'
    tmux send-keys -t $SESSION_NAME:4 'echo "Local Ignition: http://localhost:8088"' C-m
    tmux send-keys -t $SESSION_NAME:4 'echo "Node-RED: http://localhost:1880"' C-m
    
    echo "✅ Mac Claude session created with 5 windows"
else
    echo "📎 Attaching to existing Mac Claude session..."
fi

# Attach to session
tmux -f ~/.tmux.conf.mac-claude attach-session -t $SESSION_NAME
EOF

chmod +x ~/start_mac_claude.sh

# Create instance identifier
cat > ~/Desktop/industrial-iot-stack/agents/mac_instance.json << EOF
{
  "instance_id": "mac-macbook-pro",
  "instance_type": "coordinator",
  "location": "local-macbook",
  "status_bar_color": "green",
  "tmux_session": "claude-mac",
  "responsibilities": [
    "google-sheets-coordination",
    "approval-management", 
    "local-development",
    "git-orchestration"
  ],
  "google_sheets": {
    "connected": true,
    "sheet_id": "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do",
    "monitoring_active": true
  }
}
EOF

echo "✅ Mac TMUX Coordinator Setup Complete!"
echo ""
echo "🎯 Visual Distinction:"
echo "  - Mac TMUX: Green status bar with 🍎"
echo "  - Server TMUX: Blue status bar with 🖥️"
echo ""
echo "To start: ~/start_mac_claude.sh"