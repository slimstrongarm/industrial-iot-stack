# Server Claude Status Check Guide

## 🔍 Quick Commands to Check Server Claude

### 1. SSH Connection
```bash
ssh localaccount@100.94.84.126
```

### 2. Check TMUX Session
```bash
# List all tmux sessions
tmux ls

# Attach to Server Claude session (usually blue)
tmux attach -t server-claude
# or
tmux attach -t blue
```

### 3. Check Discord Bot Status
```bash
# Check if Docker container is running
docker ps | grep discord

# Check Docker logs
docker logs discord-bot

# Check if bot process is running
ps aux | grep bot
```

### 4. Check Task Worker Status
```bash
# Check if task worker is running
ps aux | grep task_worker

# Check worker logs
tail -f ~/industrial-iot-stack/logs/task_worker.log
```

### 5. System Health Check
```bash
# Check system resources
htop

# Check disk space
df -h

# Check recent activity
last -10
```

## 📋 Key Questions for Server Claude

1. **Discord Bot Deployment (CT-099)**
   - Did the Docker deployment complete?
   - Is the bot responding in Discord?
   - Any errors in the logs?

2. **Current Task Status**
   - What task is Server Claude working on?
   - Any blockers or issues?

3. **System Status**
   - Is the task worker running?
   - Any system resource issues?

## 🔄 If Server Claude Needs Restart

```bash
# Restart task worker
cd ~/industrial-iot-stack
python3 scripts/server_claude_task_worker.py &

# Restart Discord bot
cd ~/industrial-iot-stack/discord-bot
docker-compose restart

# Create new TMUX session if needed
~/start_server_claude.sh
```

## 📊 Update Google Sheets

After checking Server Claude, update the relevant tasks:
- CT-099 (Discord bot deployment) status
- Any new completed tasks
- Current in-progress items

---

**Note**: Since the brewery demo was successful and they're working on router/wifi issues, we're ready to continue with the next phase once they resolve their connectivity!