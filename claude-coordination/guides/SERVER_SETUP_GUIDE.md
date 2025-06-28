# Server Setup Guide - Claude Instance & Docker Audit

## 🎯 Immediate Actions (In Order)

### 1. First, Audit Existing Docker Setup
Before we deploy anything, let's see what's already on the server:

```bash
# Copy and run this on your server:
curl -sSL https://raw.githubusercontent.com/yourusername/industrial-iot-stack/main/scripts/server_docker_audit.sh | bash > docker_audit_$(date +%Y%m%d_%H%M).txt

# Or manually:
scp scripts/server_docker_audit.sh user@your-server:~/
ssh user@your-server 'bash docker_audit.sh'
```

### 2. Set Up Claude Server Instance with TMUX

```bash
# On your server:
wget https://raw.githubusercontent.com/yourusername/industrial-iot-stack/main/scripts/setup_claude_server_instance.sh
bash setup_claude_server_instance.sh
```

This creates:
- Persistent TMUX session named "claude-server"
- 5 pre-configured windows for different tasks
- Sync scripts for Mac ↔ Server communication
- Approval checking integration

### 3. Start Claude TMUX Session

```bash
# Start the persistent session:
~/start_claude_session.sh
```

TMUX Windows Created:
- **Window 0**: Main Claude workspace
- **Window 1**: Docker monitoring (live container status)
- **Window 2**: System logs (Docker daemon logs)
- **Window 3**: Git operations 
- **Window 4**: Python scripts directory

### 4. Enable Mac ↔ Server Communication

**Option A: Via Git** (Recommended)
```bash
# On Mac:
cd ~/Desktop/industrial-iot-stack
git add -A
git commit -m "🤖 Mac Claude: Update session state"
git push

# On Server (in TMUX):
cd /opt/industrial-iot-stack
git pull
```

**Option B: Direct SSH**
```bash
# From Mac, share screen to server:
ssh -t user@server 'tmux attach -t claude-server'
```

## 📊 Google Sheets Approval Workflow

### Test It Now:
1. Open your Google Sheets: [IoT Stack Progress Master](https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do)
2. Look for "Claude Approvals" tab (will be created on first use)
3. When Claude needs approval, a row appears
4. Type your response in column E
5. Claude continues automatically

### Example Approval Scenarios:
```
Docker Network: "Use 172.20.0.0/16 or suggest alternative"
→ You type: "172.20.0.0/16" or "10.100.0.0/16"

Deploy Now?: "Server audit complete. Deploy Ignition container?"
→ You type: "YES" or "NO"
```

## 🔄 Instance Synchronization

### Mac Claude → Server Claude:
```bash
# Mac Claude updates session state
echo "Mac completed task X" >> agents/SESSION_STATE.json
git commit -am "Update from Mac"
git push

# Server Claude picks up changes
git pull
cat agents/SESSION_STATE.json
```

### Server Claude → Mac Claude:
```bash
# Server Claude updates progress
echo "Docker deployment 50% complete" >> deployment_log.txt
git commit -am "Server progress update"
git push

# Mac Claude sees update
git pull
```

## 🚦 Next Steps After Setup

1. **Run Docker Audit** (5 min)
   - Share the audit results with Mac Claude
   - Identify any conflicts or existing services

2. **Start TMUX Session** (2 min)
   - Creates persistent workspace
   - Survives SSH disconnections

3. **Test Approval System** (2 min)
   - Mac Claude creates test approval
   - You respond in Google Sheets
   - Verify sync works

4. **Begin Docker Migration** (When ready)
   - Mac Claude prepares configs
   - Server Claude deploys
   - Both instances stay synchronized

## 💡 Pro Tips

### TMUX Quick Commands:
- `Ctrl+B, D` - Detach (leave running)
- `Ctrl+B, [0-4]` - Switch windows
- `Ctrl+B, C` - Create new window
- `tmux ls` - List sessions
- `tmux kill-session -t claude-server` - Clean restart

### Keep Both Claudes in Sync:
- Commit often with clear messages
- Use `🤖 Mac Claude:` or `🖥️ Server Claude:` prefixes
- Check SESSION_STATE.json for current status

## ❓ Common Issues

**"Git push fails"**
- Need to set up GitHub repo and add server SSH key
- Or use local git server/Tailscale file sharing

**"Approval not detected"**
- Ensure service account has edit access to sheet
- Check credentials are copied to server

**"TMUX session died"**
- Just run `~/start_claude_session.sh` again
- All windows will be recreated

---

**Ready to start?** Run the Docker audit first, then we'll know exactly what we're working with!