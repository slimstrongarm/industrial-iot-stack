# Restart Server Claude on Windows WSL

## 🚀 Quick Restart Steps

### 1. Access WSL
```bash
# From Windows Terminal or PowerShell
wsl
# or if you have multiple distros
wsl -d Ubuntu
```

### 2. Navigate to Project
```bash
cd ~/industrial-iot-stack
# or wherever you cloned the repo
```

### 3. Check Existing TMUX Sessions
```bash
# List any existing sessions
tmux ls

# If sessions exist, attach to them
tmux attach -t server-claude
# or
tmux attach -t blue
```

### 4. Create New Server Claude TMUX Session
```bash
# If no session exists, create new one
tmux new-session -d -s server-claude -n main

# Set blue status bar for Server Claude
tmux set-option -t server-claude status-style bg=blue,fg=white

# Attach to the session
tmux attach -t server-claude
```

### 5. Start Server Claude Components

#### In TMUX Window 1 (Main):
```bash
# Start the task worker
cd ~/industrial-iot-stack
python3 scripts/server_claude_task_worker.py
```

#### Create Window 2 for Docker:
```bash
# Press Ctrl+B then C to create new window
# Start Docker if needed
sudo service docker start

# Check Docker status
docker ps

# Start Discord bot if deployed
cd discord-bot
docker-compose up -d
```

#### Create Window 3 for Monitoring:
```bash
# Press Ctrl+B then C to create new window
# Monitor logs
cd ~/industrial-iot-stack
tail -f logs/task_worker.log
```

## 🔧 WSL-Specific Commands

### Check WSL Status
```bash
# From Windows PowerShell
wsl --list --verbose

# Check if Docker is running in WSL
wsl -d Ubuntu -e bash -c "sudo service docker status"
```

### Start Docker in WSL
```bash
# Inside WSL
sudo service docker start
# or
sudo dockerd &
```

### Common WSL Issues

1. **Docker not starting**
   ```bash
   # Fix Docker daemon
   sudo update-alternatives --set iptables /usr/sbin/iptables-legacy
   sudo service docker start
   ```

2. **Network issues**
   ```bash
   # Restart WSL networking
   # From Windows PowerShell (as admin)
   wsl --shutdown
   # Then restart WSL
   ```

## 📋 Server Claude Startup Checklist

- [ ] WSL is running
- [ ] Docker daemon is started
- [ ] TMUX session created (blue status bar)
- [ ] Task worker running in window 1
- [ ] Discord bot container running (if deployed)
- [ ] Can access Google Sheets API
- [ ] Check pending tasks in Google Sheets

## 🎯 Quick Test Commands

```bash
# Test Google Sheets connection
python3 -c "import gspread; print('✅ gspread installed')"

# Check task worker
ps aux | grep task_worker

# Check Discord bot
docker ps | grep discord

# Test network connectivity
ping -c 2 google.com
```

## 🔄 TMUX Navigation Reminder

- `Ctrl+B` then `D` - Detach from session (keeps running)
- `Ctrl+B` then `[0-9]` - Switch between windows
- `Ctrl+B` then `C` - Create new window
- `Ctrl+B` then `,` - Rename current window
- `Ctrl+B` then `?` - Show all commands

---

**Note**: Server Claude should automatically start processing tasks once the task worker is running!