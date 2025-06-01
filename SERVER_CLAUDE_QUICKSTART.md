# Server Claude Quick Start 🚀

## For the Server Claude Instance to Run:

### 1. Clone and Setup (2 minutes)
```bash
# Clone the repository
cd ~
git clone https://github.com/[your-username]/industrial-iot-stack.git
cd industrial-iot-stack

# Run the Docker audit first
bash scripts/server_docker_audit.sh | tee docker_audit_$(date +%Y%m%d).txt

# Set up Claude workspace with TMUX
bash scripts/setup_claude_server_instance.sh
```

### 2. Start Persistent Session
```bash
# This creates the TMUX session that survives disconnects
~/start_claude_session.sh
```

### 3. Share Results with Mac Claude
```bash
# After Docker audit completes
cat docker_audit_*.txt
# Copy output to share with Mac Claude
```

## What This Gives You:
- ✅ Persistent TMUX session (survives logout)
- ✅ Docker audit results to plan deployment
- ✅ Sync capability between Mac and Server Claude
- ✅ Google Sheets approval integration ready

## Next: Server Claude can then:
1. Monitor for Mac Claude's Docker configs via git pull
2. Deploy containers when approved
3. Update progress in SESSION_STATE.json
4. Stay running 24/7 in TMUX

---
**Pro tip**: Name your TMUX windows clearly so you can find things easily!