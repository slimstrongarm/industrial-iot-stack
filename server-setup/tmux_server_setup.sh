#!/bin/bash
# TMUX Server Setup - Blue Theme for Server Instance

echo "🖥️  Setting up Server TMUX Environment (Blue Theme)"
echo "================================================"

# Create TMUX config for server
cat > ~/.tmux.conf << 'EOF'
# Server TMUX Configuration - Blue Theme

# Set prefix to Ctrl+B (default)
set -g prefix C-b

# Enable mouse support
set -g mouse on

# Set base index to 1
set -g base-index 1
setw -g pane-base-index 1

# Blue color scheme for server
set -g status-style 'bg=colour4 fg=colour15'
set -g window-status-current-style 'bg=colour12 fg=colour0 bold'
set -g pane-border-style 'fg=colour4'
set -g pane-active-border-style 'fg=colour12'

# Status bar customization
set -g status-left '#[bg=colour12,fg=colour0] SERVER #[bg=colour4,fg=colour15] #S '
set -g status-right '#[bg=colour4,fg=colour15] %Y-%m-%d %H:%M '
set -g status-left-length 20

# Window status format
setw -g window-status-format ' #I:#W '
setw -g window-status-current-format ' #I:#W '

# History
set -g history-limit 10000

# Quick pane switching
bind -n M-Left select-pane -L
bind -n M-Right select-pane -R
bind -n M-Up select-pane -U
bind -n M-Down select-pane -D
EOF

# Start TMUX session
tmux new-session -d -s claude-server

# Create windows
tmux rename-window -t claude-server:1 'docker-main'
tmux new-window -t claude-server:2 -n 'monitoring'
tmux new-window -t claude-server:3 -n 'logs'
tmux new-window -t claude-server:4 -n 'git-sync'

# Set up each window
tmux send-keys -t claude-server:1 'cd ~/industrial-iot-stack' C-m 'clear' C-m
tmux send-keys -t claude-server:2 'docker ps' C-m
tmux send-keys -t claude-server:3 'cd ~/industrial-iot-stack/logs' C-m
tmux send-keys -t claude-server:4 'cd ~/industrial-iot-stack && git init' C-m

echo "✅ TMUX Server session created!"
echo ""
echo "📋 Windows created:"
echo "  1. docker-main - Main Docker operations"
echo "  2. monitoring - Container monitoring"
echo "  3. logs - Log viewing"
echo "  4. git-sync - Git operations"
echo ""
echo "🚀 To attach: tmux attach -t claude-server"
echo "🔷 Theme: Blue (Server identification)"