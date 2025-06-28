#!/bin/bash
# Fix TMUX and Start Server Claude in WSL

echo "🔧 Fixing TMUX and Starting Server Claude..."
echo "========================================="

# Create the TMUX directory if it doesn't exist
echo "1. Creating TMUX directory..."
mkdir -p /tmp/tmux-1000
chmod 700 /tmp/tmux-1000

# Start a new TMUX session for Server Claude
echo "2. Creating Server Claude TMUX session..."
tmux new-session -d -s server-claude -n main

# Configure blue theme for Server Claude
echo "3. Setting blue theme for Server Claude..."
tmux set-option -t server-claude status-style bg=blue,fg=white
tmux set-option -t server-claude status-left '#[bg=blue,fg=white] SERVER CLAUDE '
tmux set-option -t server-claude status-right '#[bg=blue,fg=white] %Y-%m-%d %H:%M '

# Create multiple windows
echo "4. Creating workspace windows..."
tmux new-window -t server-claude:2 -n 'docker'
tmux new-window -t server-claude:3 -n 'logs'
tmux new-window -t server-claude:4 -n 'monitor'

# Send startup commands to each window
echo "5. Setting up work environment..."

# Window 1: Task Worker
tmux send-keys -t server-claude:1 'cd ~/industrial-iot-stack' C-m
tmux send-keys -t server-claude:1 'echo "🤖 Starting Server Claude Task Worker..."' C-m
tmux send-keys -t server-claude:1 'python3 scripts/server_claude_task_worker.py' C-m

# Window 2: Docker
tmux send-keys -t server-claude:2 'cd ~/industrial-iot-stack' C-m
tmux send-keys -t server-claude:2 'sudo service docker status' C-m
tmux send-keys -t server-claude:2 'docker ps' C-m

# Window 3: Logs
tmux send-keys -t server-claude:3 'cd ~/industrial-iot-stack' C-m
tmux send-keys -t server-claude:3 'tail -f logs/task_worker.log' C-m

# Window 4: Monitor
tmux send-keys -t server-claude:4 'cd ~/industrial-iot-stack' C-m
tmux send-keys -t server-claude:4 'htop' C-m

echo "✅ Server Claude TMUX session created!"
echo ""
echo "📋 Next steps:"
echo "   1. Attach to session: tmux attach -t server-claude"
echo "   2. Switch windows: Ctrl+B then 1-4"
echo "   3. Detach: Ctrl+B then D"
echo ""
echo "🚀 Attaching to Server Claude session now..."

# Attach to the session
tmux attach -t server-claude