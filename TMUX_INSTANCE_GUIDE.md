# TMUX Instance Management Guide

## 🎯 Quick Identification

### Mac TMUX (Your MacBook)
- **Session Name**: `claude-mac`
- **Status Bar**: 🍎 GREEN background
- **Command**: `~/start_mac_claude.sh`
- **Purpose**: Coordinator, Google Sheets, Approvals

### Server TMUX (Docker Host)
- **Session Name**: `claude-server`  
- **Status Bar**: 🖥️ BLUE background
- **Command**: `~/start_claude_session.sh`
- **Purpose**: Docker deployment, Service monitoring

## 🔍 How to Tell Which You're In

```bash
# Check current TMUX session name
tmux display-message -p '#S'
# Returns: "claude-mac" or "claude-server"

# List all TMUX sessions
tmux ls
```

## 🔄 Both Instances Update Google Sheets

### Mac Instance Updates:
- Human Tasks tab (your todo items)
- Docker Migration Tasks (automated tasks)
- Claude Approvals (approval requests)
- System Status (new tab for instance health)

### Server Instance Updates:
- Docker Migration Tasks (deployment progress)
- System Status (container health)
- Activity Log (what it's doing)

## 📊 Setting Up Dual Google Sheets Updates

1. **Mac already has credentials** at:
   ```
   ~/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json
   ```

2. **Server needs credentials copied**:
   ```bash
   # From Mac to Server
   scp ~/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json \
       user@server:/opt/industrial-iot-stack/credentials/
   ```

3. **Both can then update sheets independently**

## 🚀 Recommended Workflow

### On Mac (Green TMUX):
```bash
# Start Mac coordinator
~/start_mac_claude.sh

# Window 1: Sheets monitor running
# Window 2: Server sync monitor
# Window 3: Git operations
```

### On Server (Blue TMUX):
```bash
# Start Server instance
~/start_claude_session.sh

# Window 1: Docker operations
# Window 2: Container monitoring
# Window 3: Logs
```

## 🔗 Communication Flow

```
Mac TMUX (Green) 
    ↓ (git push)
GitHub Repo
    ↓ (git pull)
Server TMUX (Blue)
    ↓ (updates)
Google Sheets ← Both update different tabs
    ↑
Mac TMUX (Green)
```

## 💡 Pro Tips

1. **Color coding is key**: Green = Mac, Blue = Server
2. **Check session state**: `cat agents/SESSION_STATE.json`
3. **Force sync**: `git pull && git push`
4. **Monitor both**: Open two terminal tabs, SSH to server in one

## 🎯 Next Steps

1. Set up Mac TMUX:
   ```bash
   bash ~/Desktop/industrial-iot-stack/scripts/setup_mac_tmux_coordinator.sh
   ~/start_mac_claude.sh
   ```

2. Copy credentials to server:
   ```bash
   scp credentials/iot-stack-credentials.json user@server:/opt/industrial-iot-stack/credentials/
   ```

3. Both instances can now:
   - Update different parts of Google Sheets
   - Sync via Git
   - Show clear visual distinction
   - Run independently but coordinated