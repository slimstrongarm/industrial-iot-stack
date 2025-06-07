# ⚡ Claude Quick Commands Reference

## 🔍 Status Check (30 seconds)
```bash
# Overall project status
python3 scripts/quick_status.py

# Recent changes
git log --oneline -5

# Running services  
docker ps

# Current priorities
head -20 STATUS.md

# Task tracking
cat scripts/.claude_tasks_state.json | jq '.tasks | to_entries[] | select(.value.status != "Complete") | {(.key): .value.description}'
```

## 🚀 Deploy Commands

### Discord Bot (Server Claude)
```bash
cd discord-bot
docker-compose up -d
docker logs discord-bot  # Check if running
```

### WhatsApp Integration (Server Claude)
```bash
# Import flow to Node-RED at http://localhost:1880
# File: whatsapp-integration/steel-bonnet-flow.json
# Test: curl -X POST http://localhost:1880/webhook/whatsapp-test
```

### Test Everything
```bash
python3 scripts/testing/test_sheets_access.py    # Google Sheets
python3 scripts/testing/test_n8n_mqtt_connection.py  # n8n connection
bash scripts/test_mqtt_brokers.sh               # MQTT brokers
```

## 🔧 Debug Commands

### GitHub Actions YAML Error
```bash
# Find the syntax error
yamllint .github/workflows/claude-max-automation.yml

# Check around line 269
sed -n '265,275p' .github/workflows/claude-max-automation.yml

# Validate YAML structure
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/claude-max-automation.yml'))"
```

### Google Sheets Issues
```bash
# Test connection
python3 scripts/testing/test_sheets_access.py

# Check credentials
ls -la credentials/iot-stack-credentials.json

# View sheet directly
echo "https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
```

### Server Connection Issues
```bash
# Test Tailscale connection
ping 100.94.84.126

# Test SSH
ssh -o ConnectTimeout=5 localaccount@100.94.84.126 'echo "Connected!"'

# Check services on server
ssh localaccount@100.94.84.126 'docker ps'
```

## 🖥️ TMUX Commands

### Session Management
```bash
# List sessions
tmux ls

# Attach to Mac session (Green)
tmux attach -t claude-max-restored

# Attach to Server session (Blue)  
tmux attach -t server-claude

# Kill all sessions (fresh start)
tmux kill-server
```

### Within TMUX
```bash
# Detach from session
Ctrl+B, D

# Switch windows
Ctrl+B, 0-4

# Create new window
Ctrl+B, C

# Split pane horizontally
Ctrl+B, %

# Split pane vertically  
Ctrl+B, "
```

## 📊 Google Sheets Quick Actions
```bash
# Update task status
python3 scripts/comprehensive_sheets_update.py

# Check for new tasks
python3 scripts/monitor_claude_tasks.py

# Add human task
python3 scripts/add_human_tasks_tab.py
```

## 🎯 Friday Demo Test Commands
```bash
# Test MQTT to WhatsApp flow
mosquitto_pub -t "salinas/utilities/air_compressor_01/telemetry" -m '{"pressure": 87, "timestamp": "'$(date)'"}'

# Check Discord bot status
curl -X GET "https://discord.com/api/v10/applications/@me" -H "Authorization: Bot YOUR_BOT_TOKEN"

# Verify Google Sheets logging
tail -f logs/integration.log  # If log file exists
```

---

**💡 Pro Tips**:
- Always check `STATUS.md` first
- Use `python3 scripts/quick_status.py` for instant overview
- Green TMUX = Mac, Blue TMUX = Server
- Friday demo is THE priority