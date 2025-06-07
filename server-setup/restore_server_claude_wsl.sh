#!/bin/bash
# Server Claude Blue TMUX Session for Windows WSL
# Paste this entire script into your Windows WSL terminal

echo "🖥️ Setting up Server Claude Blue Session on Windows WSL..."
echo "================================================="

# Kill any existing sessions
tmux kill-server 2>/dev/null || true

# Create the Server Claude session
tmux new-session -d -s server-claude-blue

# Set BLUE status bar (Server identifier)
tmux set-option -t server-claude-blue status-bg blue
tmux set-option -t server-claude-blue status-fg white
tmux set-option -t server-claude-blue status-left "#[bg=blue,fg=white,bold] 🖥️ SERVER CLAUDE #[default]"

# Window 0: Main workspace with context
tmux rename-window -t server-claude-blue:0 'main'
tmux send-keys -t server-claude-blue:main "clear" Enter
tmux send-keys -t server-claude-blue:main "echo '🖥️ SERVER CLAUDE SESSION ACTIVE'" Enter
tmux send-keys -t server-claude-blue:main "echo '================================'" Enter
tmux send-keys -t server-claude-blue:main "echo ''" Enter
tmux send-keys -t server-claude-blue:main "echo '📋 Context Restored:'" Enter
tmux send-keys -t server-claude-blue:main "echo '  • Server IP: 100.94.84.126'" Enter
tmux send-keys -t server-claude-blue:main "echo '  • Docker: Ready in WSL'" Enter
tmux send-keys -t server-claude-blue:main "echo '  • n8n: Running on :5678'" Enter
tmux send-keys -t server-claude-blue:main "echo '  • Google Sheets: Credentials available'" Enter
tmux send-keys -t server-claude-blue:main "echo ''" Enter
tmux send-keys -t server-claude-blue:main "echo '🎯 Your Tasks:'" Enter
tmux send-keys -t server-claude-blue:main "echo '  • CT-027: Deploy Discord bot'" Enter
tmux send-keys -t server-claude-blue:main "echo '  • CT-029: Deploy WhatsApp Steel Bonnet flow'" Enter
tmux send-keys -t server-claude-blue:main "echo '  • Support Mac Claude with integrations'" Enter
tmux send-keys -t server-claude-blue:main "echo ''" Enter

# Check for project directory
tmux send-keys -t server-claude-blue:main "echo '📁 Checking project location...'" Enter
tmux send-keys -t server-claude-blue:main "if [ -d /mnt/c/Users/Public/Docker/industrial-iot-stack ]; then" Enter
tmux send-keys -t server-claude-blue:main "  cd /mnt/c/Users/Public/Docker/industrial-iot-stack" Enter
tmux send-keys -t server-claude-blue:main "  echo '✅ Project found at Windows path'" Enter
tmux send-keys -t server-claude-blue:main "elif [ -d ~/industrial-iot-stack ]; then" Enter
tmux send-keys -t server-claude-blue:main "  cd ~/industrial-iot-stack" Enter
tmux send-keys -t server-claude-blue:main "  echo '✅ Project found at WSL home'" Enter
tmux send-keys -t server-claude-blue:main "else" Enter
tmux send-keys -t server-claude-blue:main "  echo '⚠️  Project not found - clone from GitHub:'" Enter
tmux send-keys -t server-claude-blue:main "  echo 'git clone https://github.com/slimstrongarm/industrial-iot-stack.git'" Enter
tmux send-keys -t server-claude-blue:main "fi" Enter

# Window 1: Docker monitoring
tmux new-window -t server-claude-blue -n 'docker'
tmux send-keys -t server-claude-blue:docker "echo '🐳 Docker Monitoring'" Enter
tmux send-keys -t server-claude-blue:docker "echo '=================='" Enter
tmux send-keys -t server-claude-blue:docker "docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'" Enter
tmux send-keys -t server-claude-blue:docker "echo ''" Enter
tmux send-keys -t server-claude-blue:docker "echo 'Commands:'" Enter
tmux send-keys -t server-claude-blue:docker "echo '  • Deploy Discord: docker-compose -f discord-bot/docker-compose.yml up -d'" Enter
tmux send-keys -t server-claude-blue:docker "echo '  • Check n8n: docker logs n8n'" Enter

# Window 2: Deployments
tmux new-window -t server-claude-blue -n 'deploy'
tmux send-keys -t server-claude-blue:deploy "echo '🚀 Deployment Tasks'" Enter
tmux send-keys -t server-claude-blue:deploy "echo '=================='" Enter
tmux send-keys -t server-claude-blue:deploy "echo ''" Enter
tmux send-keys -t server-claude-blue:deploy "echo 'CT-027 Discord Bot Deployment:'" Enter
tmux send-keys -t server-claude-blue:deploy "echo '  cd discord-bot'" Enter
tmux send-keys -t server-claude-blue:deploy "echo '  docker-compose up -d'" Enter
tmux send-keys -t server-claude-blue:deploy "echo ''" Enter
tmux send-keys -t server-claude-blue:deploy "echo 'CT-029 WhatsApp Deployment:'" Enter
tmux send-keys -t server-claude-blue:deploy "echo '  • Import flow to Node-RED'" Enter
tmux send-keys -t server-claude-blue:deploy "echo '  • File: whatsapp-integration/steel-bonnet-flow.json'" Enter

# Window 3: n8n API
tmux new-window -t server-claude-blue -n 'n8n-api'
tmux send-keys -t server-claude-blue:n8n-api "echo '🔌 n8n API Access'" Enter
tmux send-keys -t server-claude-blue:n8n-api "echo '================'" Enter
tmux send-keys -t server-claude-blue:n8n-api "echo 'API URL: http://localhost:5678/api/v1'" Enter
tmux send-keys -t server-claude-blue:n8n-api "echo 'Auth: Bearer token in environment'" Enter
tmux send-keys -t server-claude-blue:n8n-api "echo ''" Enter
tmux send-keys -t server-claude-blue:n8n-api "echo 'Test API:'" Enter
tmux send-keys -t server-claude-blue:n8n-api "echo 'curl http://localhost:5678/api/v1/workflows'" Enter

# Window 4: Git sync
tmux new-window -t server-claude-blue -n 'git-sync'
tmux send-keys -t server-claude-blue:git-sync "echo '🔄 Git Synchronization'" Enter
tmux send-keys -t server-claude-blue:git-sync "echo '====================='" Enter
tmux send-keys -t server-claude-blue:git-sync "echo 'Pull latest from Mac Claude:'" Enter
tmux send-keys -t server-claude-blue:git-sync "git pull origin main" Enter

# Back to main window
tmux select-window -t server-claude-blue:0

echo ""
echo "✅ Server Claude Blue session created!"
echo ""
echo "🎯 To attach: tmux attach -t server-claude-blue"
echo ""
echo "📋 Session includes:"
echo "  Window 0: Main workspace with context"
echo "  Window 1: Docker monitoring"
echo "  Window 2: Deployment commands"
echo "  Window 3: n8n API access"
echo "  Window 4: Git sync with Mac"
echo ""
echo "🔑 Credentials location:"
echo "  • Google Sheets: credentials/iot-stack-credentials.json"
echo "  • Discord Bot Token: discord-bot/.env"
echo "  • n8n API: Check docker-compose environment"
echo ""
echo "🖥️ Blue status bar = Server Claude!"

# Auto-attach if not in TMUX
if [ -z "$TMUX" ]; then
    tmux attach -t server-claude-blue
fi