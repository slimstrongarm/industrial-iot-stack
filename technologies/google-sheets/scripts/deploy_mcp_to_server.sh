#!/bin/bash
# Deploy MCP Task Orchestrator to Server Claude
# Usage: ./deploy_mcp_to_server.sh

SERVER_IP="100.94.84.126"
SERVER_USER="localaccount"
SERVER_PATH="/home/$SERVER_USER/industrial-iot-stack/technologies/google-sheets/scripts"

echo "🚀 Deploying MCP Task Orchestrator to Server Claude"
echo "=================================================="

# Check if server is reachable
echo "📡 Testing connection to Server Claude..."
if ! ping -c 1 "$SERVER_IP" &> /dev/null; then
    echo "❌ Cannot reach Server Claude at $SERVER_IP"
    exit 1
fi

echo "✅ Server Claude is reachable"

# Create directory structure on server
echo "📁 Creating MCP directory structure..."
ssh "$SERVER_USER@$SERVER_IP" "mkdir -p $SERVER_PATH"

# Copy MCP files
echo "📋 Copying MCP Task Orchestrator..."
scp mcp_task_orchestrator.py "$SERVER_USER@$SERVER_IP:$SERVER_PATH/"

echo "📊 Copying MCP Change Monitor..."
scp mcp_change_monitor.py "$SERVER_USER@$SERVER_IP:$SERVER_PATH/"

echo "🔧 Copying Quick Task Manager..."
scp quick_task_manager.py "$SERVER_USER@$SERVER_IP:$SERVER_PATH/"

# Copy credentials
echo "🔐 Copying credentials..."
ssh "$SERVER_USER@$SERVER_IP" "mkdir -p /home/$SERVER_USER/industrial-iot-stack/credentials"
scp ../../../credentials/iot-stack-credentials.json "$SERVER_USER@$SERVER_IP:/home/$SERVER_USER/industrial-iot-stack/credentials/"

# Create Server Claude specific startup script
echo "🎯 Creating Server Claude MCP startup script..."
ssh "$SERVER_USER@$SERVER_IP" "cat > /home/$SERVER_USER/start-server-mcp.sh" << 'EOF'
#!/bin/bash
# Server Claude MCP Monitor Startup

echo "🔵 Starting Server Claude MCP Monitor..."
echo "========================================"

cd /home/localaccount/industrial-iot-stack/technologies/google-sheets/scripts

# Start the change monitor with Server Claude context
python3 -c "
import sys
sys.path.append('.')
from mcp_change_monitor import MCPChangeMonitor

class ServerClaudeMonitor(MCPChangeMonitor):
    def check_for_assigned_tasks(self, snapshot):
        '''Check for tasks assigned to Server Claude'''
        assigned_tasks = []
        
        for task_id, task_data in snapshot.items():
            assigned_to = task_data.get('Assigned To', '')
            status = task_data.get('Status', '')
            
            # Check if task is assigned to Server Claude
            if 'Server Claude' in assigned_to and status in ['Start', 'Not Started', 'Pending']:
                assigned_tasks.append(task_id)
        
        return assigned_tasks
    
    def report_changes(self, changes):
        '''Report changes with Server Claude context'''
        if not changes:
            return
        
        print(f'\n🔵 Server Claude detected {len(changes)} change(s) at {datetime.now().strftime(\"%H:%M:%S\")}')
        print('=' * 60)
        
        for change in changes:
            task_id = change['task_id']
            field = change['field']
            new_val = change['new_value']
            
            if field == 'Status' and new_val == 'Start':
                print(f'🚀 {task_id}: Ready to START! Status changed to \"{new_val}\"')
            elif field == 'Status':
                print(f'📋 {task_id}: Status changed to \"{new_val}\"')
            else:
                super().report_changes([change])

# Start Server Claude monitoring
print('🔵 Server Claude MCP Monitor starting...')
print('💡 Monitoring for tasks assigned to Server Claude')
print('🎯 Will detect \"Start\" status changes')
print('=' * 60)

monitor = ServerClaudeMonitor(check_interval=15)  # Check every 15 seconds
monitor.start_monitoring()
"
EOF

# Make startup script executable
ssh "$SERVER_USER@$SERVER_IP" "chmod +x /home/$SERVER_USER/start-server-mcp.sh"

# Create systemd service for persistent monitoring
echo "⚙️ Creating systemd service for persistent monitoring..."
ssh "$SERVER_USER@$SERVER_IP" "sudo tee /etc/systemd/system/server-claude-mcp.service" << 'EOF'
[Unit]
Description=Server Claude MCP Task Monitor
After=network.target

[Service]
Type=simple
User=localaccount
WorkingDirectory=/home/localaccount/industrial-iot-stack/technologies/google-sheets/scripts
ExecStart=/home/localaccount/start-server-mcp.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
echo "🚀 Enabling Server Claude MCP service..."
ssh "$SERVER_USER@$SERVER_IP" "sudo systemctl daemon-reload"
ssh "$SERVER_USER@$SERVER_IP" "sudo systemctl enable server-claude-mcp.service"

echo ""
echo "✅ Server Claude MCP deployment complete!"
echo ""
echo "🎯 To start monitoring on Server Claude:"
echo "1. SSH to server: ssh $SERVER_USER@$SERVER_IP"
echo "2. Start manually: ./start-server-mcp.sh"
echo "3. Or start service: sudo systemctl start server-claude-mcp.service"
echo ""
echo "📊 Server Claude will now monitor for:"
echo "   - Tasks assigned to 'Server Claude'"
echo "   - Status changes to 'Start'"
echo "   - Real-time task updates every 15 seconds"
echo ""
echo "🔄 Status workflow:"
echo "   1. You set task status to 'Start'"
echo "   2. Assigned Claude instance detects change"
echo "   3. Claude begins working on task automatically"