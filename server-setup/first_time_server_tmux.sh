#!/bin/bash
# First-time TMUX setup for Server Claude on Windows WSL
# This script installs TMUX if needed and creates your blue session

echo "🖥️ Setting up Server Claude TMUX for the first time..."
echo "===================================================="

# Check if TMUX is installed
if ! command -v tmux &> /dev/null; then
    echo "📦 TMUX not found. Installing..."
    sudo apt-get update
    sudo apt-get install -y tmux
    echo "✅ TMUX installed successfully!"
else
    echo "✅ TMUX is already installed"
fi

# Create TMUX config for Server Claude
echo "⚙️ Creating Server Claude TMUX configuration..."
cat > ~/.tmux.conf.server-claude << 'EOF'
# Server Claude TMUX Configuration
set -g default-terminal "screen-256color"
set -g history-limit 50000

# BLUE theme for Server (vs Green for Mac)
set -g status-bg blue
set -g status-fg white
set -g status-left '[🖥️ Server Claude]'
set -g status-right '%H:%M %d-%b-%y'

# Enable mouse support
set -g mouse on

# Window naming
set-option -g allow-rename off
set-window-option -g automatic-rename off

# Activity monitoring
setw -g monitor-activity on
set -g visual-activity on

# Better key bindings
bind r source-file ~/.tmux.conf \; display "Config reloaded!"
bind | split-window -h
bind - split-window -v
EOF

echo "✅ TMUX configuration created"

# Kill any existing sessions
tmux kill-server 2>/dev/null || true

# Create the session startup script
cat > ~/start_server_claude.sh << 'EOF'
#!/bin/bash
# Start Server Claude TMUX Session

SESSION_NAME="server-claude"
PROJECT_DIR="/mnt/c/Users/Public/Docker/industrial-iot-stack"

# Check if session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    echo "🖥️ Creating new Server Claude session..."
    
    # Create new session with server config
    tmux -f ~/.tmux.conf.server-claude new-session -d -s $SESSION_NAME
    
    # Window 0: Main workspace
    tmux rename-window -t $SESSION_NAME:0 'main'
    tmux send-keys -t $SESSION_NAME:0 "clear" C-m
    tmux send-keys -t $SESSION_NAME:0 "echo '🖥️ SERVER CLAUDE ACTIVE'" C-m
    tmux send-keys -t $SESSION_NAME:0 "echo '======================='" C-m
    tmux send-keys -t $SESSION_NAME:0 "echo ''" C-m
    tmux send-keys -t $SESSION_NAME:0 "echo '📋 Your Tasks:'" C-m
    tmux send-keys -t $SESSION_NAME:0 "echo '  • CT-027: Deploy Discord bot'" C-m
    tmux send-keys -t $SESSION_NAME:0 "echo '  • CT-029: Deploy WhatsApp flow'" C-m
    tmux send-keys -t $SESSION_NAME:0 "echo ''" C-m
    tmux send-keys -t $SESSION_NAME:0 "cd $PROJECT_DIR 2>/dev/null || echo '⚠️  Project not found - clone from GitHub first!'" C-m
    
    # Window 1: Docker
    tmux new-window -t $SESSION_NAME:1 -n 'docker'
    tmux send-keys -t $SESSION_NAME:1 "docker ps" C-m
    
    # Window 2: Deployments
    tmux new-window -t $SESSION_NAME:2 -n 'deploy'
    tmux send-keys -t $SESSION_NAME:2 "cd $PROJECT_DIR" C-m
    tmux send-keys -t $SESSION_NAME:2 "echo 'Ready for deployments:'" C-m
    tmux send-keys -t $SESSION_NAME:2 "echo '  Discord: cd discord-bot && docker-compose up -d'" C-m
    tmux send-keys -t $SESSION_NAME:2 "echo '  WhatsApp: Import to Node-RED at http://localhost:1880'" C-m
    
    # Window 3: Git sync
    tmux new-window -t $SESSION_NAME:3 -n 'git'
    tmux send-keys -t $SESSION_NAME:3 "cd $PROJECT_DIR && git status" C-m
    
    # Window 4: Monitoring
    tmux new-window -t $SESSION_NAME:4 -n 'monitor'
    tmux send-keys -t $SESSION_NAME:4 "htop" C-m
    
    # Go back to main window
    tmux select-window -t $SESSION_NAME:0
    
    echo "✅ Server Claude session created!"
else
    echo "📎 Attaching to existing Server Claude session..."
fi

# Attach to session
tmux -f ~/.tmux.conf.server-claude attach-session -t $SESSION_NAME
EOF

chmod +x ~/start_server_claude.sh

# Clone the repository if it doesn't exist
if [ ! -d "/mnt/c/Users/Public/Docker/industrial-iot-stack" ]; then
    echo "📥 Cloning repository..."
    mkdir -p /mnt/c/Users/Public/Docker
    cd /mnt/c/Users/Public/Docker
    git clone https://github.com/slimstrongarm/industrial-iot-stack.git
    echo "✅ Repository cloned"
else
    echo "✅ Repository already exists"
    cd /mnt/c/Users/Public/Docker/industrial-iot-stack
    git pull origin main
fi

echo ""
echo "🎉 TMUX setup complete!"
echo "================================"
echo ""
echo "🚀 To start Server Claude TMUX:"
echo "   ~/start_server_claude.sh"
echo ""
echo "📋 TMUX basics:"
echo "   • Detach: Ctrl+B, then D"
echo "   • Switch windows: Ctrl+B, then 0-4"
echo "   • List sessions: tmux ls"
echo "   • Kill session: tmux kill-session -t server-claude"
echo ""
echo "🔵 You'll see a BLUE status bar (Mac has GREEN)"
echo ""
echo "Ready to start? Run: ~/start_server_claude.sh"