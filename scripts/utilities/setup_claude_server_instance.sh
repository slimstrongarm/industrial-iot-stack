#!/bin/bash
# Setup Claude on Server with TMUX persistence
# This creates a persistent environment for Claude to work on the server

set -e

echo "🤖 Setting up Claude Server Instance with TMUX"
echo "============================================="

# Check prerequisites
echo -e "\n📋 Checking prerequisites..."
command -v tmux >/dev/null 2>&1 || { echo "❌ tmux not installed. Installing..."; sudo apt-get update && sudo apt-get install -y tmux; }
command -v git >/dev/null 2>&1 || { echo "❌ git not installed. Installing..."; sudo apt-get install -y git; }

# Create working directory
CLAUDE_DIR="/opt/industrial-iot-stack/claude-workspace"
echo -e "\n📁 Creating Claude workspace at $CLAUDE_DIR"
sudo mkdir -p $CLAUDE_DIR
sudo chown -R $USER:$USER /opt/industrial-iot-stack

# Clone the repository
echo -e "\n📥 Cloning industrial-iot-stack repository..."
cd /opt/industrial-iot-stack
if [ ! -d ".git" ]; then
    git clone https://github.com/yourusername/industrial-iot-stack.git . || echo "⚠️  Git clone failed - manual setup needed"
fi

# Create TMUX configuration
echo -e "\n⚙️ Creating TMUX configuration..."
cat > ~/.tmux.conf.claude << 'EOF'
# Claude TMUX Configuration
set -g default-terminal "screen-256color"
set -g history-limit 50000
set -g status-bg blue
set -g status-fg white
set -g status-left '[Claude Server]'
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

# Create TMUX session launcher
cat > ~/start_claude_session.sh << 'EOF'
#!/bin/bash
# Start or attach to Claude TMUX session

SESSION_NAME="claude-server"
WORK_DIR="/opt/industrial-iot-stack"

# Check if session exists
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    echo "🚀 Creating new Claude session..."
    
    # Create new session
    tmux new-session -d -s $SESSION_NAME -c $WORK_DIR
    
    # Window 0: Main Claude workspace
    tmux rename-window -t $SESSION_NAME:0 'claude-main'
    tmux send-keys -t $SESSION_NAME:0 'cd /opt/industrial-iot-stack' C-m
    tmux send-keys -t $SESSION_NAME:0 'echo "🤖 Claude Server Instance Ready"' C-m
    tmux send-keys -t $SESSION_NAME:0 'echo "📁 Working directory: $(pwd)"' C-m
    
    # Window 1: Docker monitoring
    tmux new-window -t $SESSION_NAME:1 -n 'docker-monitor'
    tmux send-keys -t $SESSION_NAME:1 'watch -n 5 docker ps' C-m
    
    # Window 2: System logs
    tmux new-window -t $SESSION_NAME:2 -n 'logs'
    tmux send-keys -t $SESSION_NAME:2 'sudo journalctl -f -u docker' C-m
    
    # Window 3: Git operations
    tmux new-window -t $SESSION_NAME:3 -n 'git'
    tmux send-keys -t $SESSION_NAME:3 'cd /opt/industrial-iot-stack && git status' C-m
    
    # Window 4: Python scripts
    tmux new-window -t $SESSION_NAME:4 -n 'python'
    tmux send-keys -t $SESSION_NAME:4 'cd /opt/industrial-iot-stack/scripts' C-m
    
    echo "✅ Claude session created with 5 windows"
else
    echo "📎 Attaching to existing Claude session..."
fi

# Attach to session
tmux attach-session -t $SESSION_NAME
EOF

chmod +x ~/start_claude_session.sh

# Create instance sync configuration
echo -e "\n🔄 Creating instance sync configuration..."
cat > $CLAUDE_DIR/instance_sync.json << EOF
{
  "instance_id": "server-$(hostname)",
  "instance_type": "docker-host",
  "sync_with": "mac-claude",
  "shared_state": "/opt/industrial-iot-stack/agents/SESSION_STATE.json",
  "communication": {
    "method": "shared-files",
    "primary_channel": "git-sync",
    "backup_channel": "google-sheets"
  },
  "capabilities": [
    "docker-deployment",
    "service-monitoring",
    "direct-server-access",
    "tmux-persistence"
  ]
}
EOF

# Create communication script
cat > $CLAUDE_DIR/sync_with_mac.sh << 'EOF'
#!/bin/bash
# Sync state between server and Mac Claude instances

echo "🔄 Syncing with Mac Claude instance..."

# Pull latest changes
cd /opt/industrial-iot-stack
git pull origin main 2>/dev/null || echo "⚠️  Git pull failed - may need manual sync"

# Check for updates from Mac
if [ -f "agents/SESSION_STATE.json" ]; then
    echo "📊 Latest session state:"
    jq '.currentWork.lastAction' agents/SESSION_STATE.json
fi

# Check for pending approvals
if [ -f "scripts/pending_approvals.json" ]; then
    echo "🔔 Pending approvals:"
    cat scripts/pending_approvals.json
fi

echo "✅ Sync complete"
EOF

chmod +x $CLAUDE_DIR/sync_with_mac.sh

# Create the approval check script
cat > $CLAUDE_DIR/check_approvals.py << 'EOF'
#!/usr/bin/env python3
"""Check for approvals from Google Sheets"""
import os
import sys
sys.path.append('/opt/industrial-iot-stack/scripts')

try:
    from claude_approval_system import ApprovalSystem
    approval = ApprovalSystem()
    # This would check for pending approvals
    print("🔍 Checking for pending approvals...")
except Exception as e:
    print(f"⚠️  Approval system not yet configured: {e}")
EOF

chmod +x $CLAUDE_DIR/check_approvals.py

echo -e "\n✅ Claude Server Instance Setup Complete!"
echo "================================="
echo "To start Claude session: ~/start_claude_session.sh"
echo "To sync with Mac: $CLAUDE_DIR/sync_with_mac.sh"
echo "Working directory: /opt/industrial-iot-stack"
echo ""
echo "🎯 Next steps:"
echo "1. Run the Docker audit script: bash /opt/industrial-iot-stack/scripts/server_docker_audit.sh"
echo "2. Start TMUX session: ~/start_claude_session.sh"
echo "3. Share session state with Mac Claude via git commit/push"