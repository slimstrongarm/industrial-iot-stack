# 🚀 START HERE - Mac Claude Session #2

## Session Context
**Date**: June 2, 2025  
**Server Status**: ✅ Connected (100.94.84.126)  
**Mission**: Deploy services for Friday brewery demo

## 🎯 Immediate Actions

### 1. Attach to TMUX Session
```bash
tmux attach -t claude-mac-2
```

### 2. Your Current Status
- ✅ SSH access to Windows server established
- ✅ Tailscale connection working on both machines
- ✅ Google Sheets automation fully operational
- ⏳ Need to audit existing services on server
- ⏳ Deploy blue TMUX on server for Server Claude

## 📋 Critical Tasks for Friday Demo

### Server Audit (PRIORITY)
```bash
# Run on server to check what's already there:
ssh localaccount@100.94.84.126
cd /mnt/c/Users/Public/Docker
bash server_docker_audit.sh
```

### Key Questions to Answer:
1. Is Node-RED already running? (Port 1880)
2. Is MQTT broker running? (EMQX vs Mosquitto)
3. Is Ignition installed? (Port 8088)
4. What Docker containers exist?

## 🔄 MQTT Architecture Update
Based on SESSION_STATE, we discovered:
- **Mac**: Mosquitto (local development)
- **Server**: EMQX (production, port 18083 dashboard)
- Need to configure bridge between them

## 📊 Google Sheets Updates
Check the new "Claude Tasks" tab for Server Claude's assignments:
- CT-001: Server audit
- CT-002: EMQX configuration
- CT-003: Docker Compose creation
- CT-004: MQTT integration test

## 🖥️ Server Claude Setup
Once audit is complete:
```bash
# On server
cd /mnt/c/Users/Public/Docker
bash setup_claude_server_instance.sh
~/start_claude_session.sh
```

## ⚡ Quick Commands
- Switch TMUX windows: `Ctrl+B, [0-4]`
- Detach from TMUX: `Ctrl+B, d`
- See all windows: `Ctrl+B, w`
- Split pane: `Ctrl+B, %`

## 🎯 Success Criteria for Today
1. [ ] Complete server audit
2. [ ] Deploy blue TMUX on server
3. [ ] Verify MQTT connectivity
4. [ ] Test Ignition Edge connection
5. [ ] Document service configuration

## 💡 Remember
- Green TMUX = Mac (you)
- Blue TMUX = Server (coming next)
- Both update Google Sheets
- Friday demo is the goal!

---
*Server connection established. Let's make this demo rock! 🎸*