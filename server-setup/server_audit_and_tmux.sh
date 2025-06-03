#!/usr/bin/expect -f
# SSH to server, audit existing services, and set up blue TMUX

set timeout 60
set password "LocalAccount"

# SSH to server
spawn ssh localaccount@100.94.84.126

expect {
    "password:" {
        send "$password\r"
    }
}

# Wait for prompt
expect {
    ">" {
        # We're in Windows CMD/PowerShell
        send "wsl\r"
        expect "$"
    }
    "$" {
        # Already in bash/WSL
    }
}

# Create audit script
send "cat > /tmp/audit_services.sh << 'EOF'\r"
send "#!/bin/bash\r"
send "echo '🔍 Server Services Audit Report'\r"
send "echo '=============================='\r"
send "echo ''\r"
send "echo '🐳 Docker Containers:'\r"
send "docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null || echo 'Docker not accessible'\r"
send "echo ''\r"
send "echo '🔴 Node-RED Check:'\r"
send "docker ps -a | grep -i node-red || echo 'No Node-RED containers found'\r"
send "curl -s http://localhost:1880 > /dev/null && echo '✅ Node-RED is accessible on port 1880' || echo '❌ Node-RED not responding on 1880'\r"
send "echo ''\r"
send "echo '🔥 Ignition Check:'\r"
send "docker ps -a | grep -i ignition || echo 'No Ignition containers found'\r"
send "curl -s http://localhost:8088/StatusPing > /dev/null && echo '✅ Ignition is accessible on port 8088' || echo '❌ Ignition not responding on 8088'\r"
send "ps aux | grep -i ignition | grep -v grep || echo 'No Ignition processes running'\r"
send "echo ''\r"
send "echo '🗄️ Database Check:'\r"
send "docker ps -a | grep -E 'postgres|mysql' || echo 'No database containers found'\r"
send "netstat -tlnp 2>/dev/null | grep -E ':5432|:3306' || ss -tlnp | grep -E ':5432|:3306' 2>/dev/null || echo 'No databases listening'\r"
send "echo ''\r"
send "echo '🌐 Network Ports:'\r"
send "netstat -tlnp 2>/dev/null | grep LISTEN | head -20 || ss -tlnp | head -20\r"
send "echo ''\r"
send "echo '💾 Docker Images:'\r"
send "docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}' | head -20\r"
send "echo ''\r"
send "echo '📁 Check common locations:'\r"
send "ls -la /opt/ 2>/dev/null | grep -E 'ignition|node-red' || echo '/opt/ - nothing found'\r"
send "ls -la ~/ignition* 2>/dev/null | head -10 || echo '~/ignition* - nothing found'\r"
send "EOF\r"
expect "$"

# Make it executable and run
send "chmod +x /tmp/audit_services.sh\r"
expect "$"
send "bash /tmp/audit_services.sh\r"
expect "$"

# Now set up TMUX with blue theme
send "echo ''\r"
expect "$"
send "echo '🔵 Setting up Blue TMUX for Server...'\r"
expect "$"

# Create TMUX config
send "cat > ~/.tmux.conf << 'EOF'\r"
send "# Server TMUX - Blue Theme\r"
send "set -g status-style 'bg=colour4 fg=colour15'\r"
send "set -g window-status-current-style 'bg=colour12 fg=colour0 bold'\r"
send "set -g status-left '#[bg=colour12,fg=colour0] SERVER #[bg=colour4,fg=colour15] '\r"
send "set -g mouse on\r"
send "set -g base-index 1\r"
send "EOF\r"
expect "$"

# Create TMUX session
send "tmux new-session -d -s claude-server\r"
expect "$"

# Create windows
send "tmux rename-window -t claude-server:1 'main'\r"
expect "$"
send "tmux new-window -t claude-server:2 -n 'docker'\r"
expect "$"
send "tmux new-window -t claude-server:3 -n 'ignition'\r"
expect "$"
send "tmux new-window -t claude-server:4 -n 'monitoring'\r"
expect "$"

# Attach to TMUX
send "tmux attach -t claude-server\r"

interact