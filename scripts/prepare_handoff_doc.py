#!/usr/bin/env python3
"""
Prepare Google Doc handoff with current status
Run this to generate an up-to-date handoff document
"""

import json
import os
from datetime import datetime
from pathlib import Path

def prepare_handoff():
    """Generate current handoff document"""
    
    # Get current status
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    session_id = f"claude-session-{datetime.now().strftime('%Y%m%d-%H%M')}"
    
    # Read task state
    try:
        with open('scripts/.claude_tasks_state.json', 'r') as f:
            task_data = json.load(f)
        last_check = task_data.get('last_check', 'Unknown')
        total_tasks = len(task_data.get('tasks', {}))
        pending_tasks = len([t for t in task_data.get('tasks', {}).values() if t.get('status') != 'Complete'])
    except:
        last_check = 'Unknown'
        total_tasks = 'Unknown'
        pending_tasks = 'Unknown'
    
    # Read current status
    try:
        with open('STATUS.md', 'r') as f:
            status_content = f.read()
        if '95%' in status_content:
            demo_readiness = '95%'
        else:
            demo_readiness = 'Unknown'
    except:
        demo_readiness = 'Unknown'
    
    # Generate handoff content
    handoff_content = f"""# 🤖 CLAUDE HANDOFF - {timestamp}

**URGENT**: Copy this entire document to Google Docs for continuity!

## 🎯 CURRENT STATUS
- **Demo Readiness**: {demo_readiness}
- **Total Tasks**: {total_tasks}
- **Pending Tasks**: {pending_tasks}
- **Last Update**: {last_check}

## 🚨 IMMEDIATE PRIORITIES

### GitHub Actions YAML Error (CRITICAL)
```
File: .github/workflows/claude-max-automation.yml
Issue: Syntax error at line 269
Impact: Blocking automation workflow
Owner: Mac Claude
```

### Ready Deployments
```
CT-027: Discord bot (Server Claude)
CT-029: WhatsApp integration (Server Claude)
Both ready in respective folders
```

## 🔑 QUICK ACCESS RESTORATION

### GitHub
```
git clone https://github.com/slimstrongarm/industrial-iot-stack
cd industrial-iot-stack
git status
```

### Google Sheets
```
Sheet ID: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do
Credentials: credentials/iot-stack-credentials.json
Test: python3 scripts/test_sheets_access.py
```

### Server Access
```
Server: 100.94.84.126 (localaccount)
Project: /mnt/c/Users/Public/Docker/industrial-iot-stack
TMUX: ~/start_server_claude.sh
```

## 📂 CRITICAL FILES
```
STATUS.md                           # Current state
scripts/.claude_tasks_state.json    # Task tracking
discord-bot/enhanced_bot.py         # Ready to deploy
whatsapp-integration/steel-bonnet-flow.json  # Ready to deploy
.github/workflows/claude-max-automation.yml  # ⚠️ YAML ERROR
```

## 🎪 FRIDAY DEMO FLOW
```
1. Steel Bonnet MQTT → Node-RED
2. Threshold breach → WhatsApp alert
3. Operator reply → Google Sheets log
4. Discord coordination channel updated
```

## 🔄 SESSION TYPES

### Mac Claude (GREEN TMUX)
- Handles: GitHub Actions, Google Sheets, documentation
- Command: `tmux attach -t claude-max-restored`
- Priority: Fix YAML syntax error

### Server Claude (BLUE TMUX)  
- Handles: Docker, n8n, Node-RED deployments
- Command: `ssh localaccount@100.94.84.126 && ~/start_server_claude.sh`
- Priority: Deploy CT-027 and CT-029

## ⚡ EMERGENCY RECOVERY
1. Read STATUS.md for latest state
2. Check scripts/.claude_tasks_state.json for tasks
3. Test Google Sheets access
4. Create appropriate TMUX (Mac=Green, Server=Blue)
5. Focus on Friday demo deliverables

---

**🎯 BOTTOM LINE**: {demo_readiness} ready for Friday brewery demo!

Generated: {timestamp}
Context: Industrial IoT Stack with WhatsApp/Discord integration"""
    
    # Write to file
    with open('CURRENT_HANDOFF.md', 'w') as f:
        f.write(handoff_content)
    
    print(f"✅ Handoff document prepared: CURRENT_HANDOFF.md")
    print(f"📋 Demo readiness: {demo_readiness}")
    print(f"📊 Tasks: {pending_tasks} pending of {total_tasks} total")
    print(f"🔗 Copy content to Google Docs for persistence!")
    
    return handoff_content

if __name__ == "__main__":
    handoff = prepare_handoff()
    print("\n" + "="*50)
    print("📋 HANDOFF DOCUMENT READY")
    print("="*50)
    print("Copy CURRENT_HANDOFF.md content to Google Docs")
    print("Share Google Doc link for session continuity")
    print("="*50)