#!/bin/bash
# TMUX Session Setup for IoT Stack Deployment

SESSION_NAME="iot-stack-deployment"

echo "🖥️  Setting up TMUX session: $SESSION_NAME"

# Create new session
tmux new-session -d -s $SESSION_NAME

# Rename first window
tmux rename-window -t $SESSION_NAME:0 'IoT-Stack'

# Split into panes
tmux split-window -h -t $SESSION_NAME:0  # Split horizontally
tmux split-window -v -t $SESSION_NAME:0.1  # Split right pane vertically
tmux select-pane -t $SESSION_NAME:0.0
tmux split-window -v -t $SESSION_NAME:0.0  # Split left pane vertically

# Set up pane purposes
tmux send-keys -t $SESSION_NAME:0.0 'echo "📊 System Monitor - run: htop"' C-m
tmux send-keys -t $SESSION_NAME:0.1 'echo "🐳 Docker Status - run: watch docker ps"' C-m
tmux send-keys -t $SESSION_NAME:0.2 'echo "📝 Logs Viewer"' C-m
tmux send-keys -t $SESSION_NAME:0.3 'echo "💻 Main Terminal - ready for deployment"' C-m

# Select main terminal pane
tmux select-pane -t $SESSION_NAME:0.3

echo "✅ TMUX session '$SESSION_NAME' created"
echo "📱 Attach with: tmux attach -t $SESSION_NAME"
echo "🔗 Detach with: Ctrl+b, d"

# Attach to session
tmux attach -t $SESSION_NAME
