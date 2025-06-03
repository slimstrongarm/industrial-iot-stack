#!/bin/bash
# Set up Blue TMUX for Server Claude

echo "🔵 Setting up Blue TMUX Session for Server"
echo "=========================================="

# Create TMUX config with blue theme
cat > ~/.tmux.conf << 'EOF'
# Server TMUX Configuration - Blue Theme

# Enable mouse
set -g mouse on

# Set base index to 1
set -g base-index 1
setw -g pane-base-index 1

# BLUE color scheme for server
set -g status-style 'bg=colour4 fg=colour15 bold'
set -g window-status-current-style 'bg=colour12 fg=colour0 bold'
set -g pane-border-style 'fg=colour4'
set -g pane-active-border-style 'fg=colour12 bold'

# Status bar
set -g status-left '#[bg=colour12,fg=colour0,bold] 🖥️ SERVER #[bg=colour4,fg=colour15] #S '
set -g status-right '#[bg=colour4,fg=colour15] %H:%M | %Y-%m-%d '
set -g status-left-length 30

# Window format
setw -g window-status-format ' #I: #W '
setw -g window-status-current-format ' #I: #W '

# History
set -g history-limit 10000
EOF

# Kill existing session if it exists
tmux kill-session -t claude-server 2>/dev/null

# Create new session
tmux new-session -d -s claude-server -n main

# Create windows
tmux new-window -t claude-server:2 -n docker
tmux new-window -t claude-server:3 -n ignition  
tmux new-window -t claude-server:4 -n monitor
tmux new-window -t claude-server:5 -n logs

# Set up window commands
tmux send-keys -t claude-server:1 'clear && echo "🔵 Welcome to Server Claude (Blue Team!)" && echo "" && echo "First, run: bash quick_audit.sh" && echo "to see what services are already running"' C-m

tmux send-keys -t claude-server:2 'docker ps -a' C-m

tmux send-keys -t claude-server:3 'echo "Ignition commands will go here"' C-m

tmux send-keys -t claude-server:4 'watch -n 2 docker ps' 

tmux send-keys -t claude-server:5 'echo "Logs will appear here"' C-m

echo "✅ Blue TMUX session 'claude-server' created!"
echo ""
echo "📋 Windows:"
echo "  1: main     - Main operations"
echo "  2: docker   - Docker management" 
echo "  3: ignition - Ignition Edge setup"
echo "  4: monitor  - Real-time monitoring"
echo "  5: logs     - Service logs"
echo ""
echo "🚀 To attach: tmux attach -t claude-server"
echo "🔵 Blue theme = Server instance"

# Attach to the session
tmux attach -t claude-server