#!/usr/bin/env python3
"""
Create optimized Claude context structure for better efficiency
"""

from pathlib import Path
import subprocess
from datetime import datetime

def create_claude_context_structure():
    """Create .claude directory with context optimization"""
    
    base_path = Path.home() / 'Desktop/industrial-iot-stack'
    claude_dir = base_path / '.claude'
    
    # Create directory structure
    (claude_dir / 'context').mkdir(parents=True, exist_ok=True)
    (claude_dir / 'prompts').mkdir(exist_ok=True)
    
    # Create current session context
    session_context = f"""# Current Session Context

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Active Issues
- ⚠️ GitHub Actions YAML syntax error (line 269)
- 🚀 Discord bot ready for deployment (CT-027)
- 🚀 WhatsApp integration ready for deployment (CT-029)

## Current Focus
- Friday brewery demo preparation (95% ready)
- Steel Bonnet MQTT integration complete
- Google Sheets tracking active

## Quick Context
- Project: Industrial IoT Stack with Steel Bonnet brewery
- Main components: WhatsApp alerts, Discord coordination, MQTT processing
- Integration: Google Sheets for task tracking
- Demo target: Friday brewery POC

## File Locations
- WhatsApp: `/whatsapp-integration/steel-bonnet-flow.json`
- Discord: `/discord-bot/enhanced_bot.py`
- MQTT: `/Steel_Bonnet/docs/MQTT_topic_map.md`
- Tasks: Google Sheets tabs (Claude Tasks, Agent Activities)
"""
    
    with open(claude_dir / 'context/current_session.md', 'w') as f:
        f.write(session_context)
    
    # Create project overview
    project_overview = """# Industrial IoT Stack - Project Overview

## Purpose
Complete brewery automation system with mobile alerts and remote coordination.

## Core Components
1. **Steel Bonnet**: Ignition-based brewery control system
2. **WhatsApp Integration**: Real-time equipment alerts
3. **Discord Bot**: Remote development coordination
4. **MQTT Processing**: Equipment data pipeline
5. **Google Sheets**: Task and progress tracking

## Technology Stack
- Ignition Edge + Flint
- Node-RED + n8n
- Docker containers
- MQTT (topic: site/area/equipment/telemetry)
- Python automation scripts

## Key Files
- `STACK-OVERVIEW.md` - Complete system documentation
- `Steel_Bonnet/docs/MQTT_topic_map.md` - Data structure
- `whatsapp-integration/` - Alert system
- `discord-bot/` - Coordination tools
- `.github/workflows/` - Automation (needs YAML fix)

## Current Status
95% ready for Friday brewery demo
"""
    
    with open(claude_dir / 'context/project_overview.md', 'w') as f:
        f.write(project_overview)
    
    # Create deployment prompt
    deployment_prompt = """# Deployment Prompts

## Standard Deployment Checklist
1. Check Google Sheets for pending tasks
2. Review recent git commits
3. Validate configuration files
4. Test integrations (MQTT, WhatsApp, Discord)
5. Update task status in Google Sheets

## Common Commands
```bash
# Check Docker status
docker ps --format "table {{.Names}}\t{{.Status}}"

# Test MQTT connection
mosquitto_pub -h localhost -t "test/topic" -m "test message"

# Update Google Sheets
python3 scripts/comprehensive_sheets_update.py

# Test WhatsApp flow
node whatsapp-integration/test-alert.js
```

## Pre-Deployment Questions
- Are all dependencies deployed?
- Have you tested the integration endpoints?
- Is the Google Sheets automation working?
- Are environment variables configured?
"""
    
    with open(claude_dir / 'prompts/deployment.md', 'w') as f:
        f.write(deployment_prompt)
    
    # Create handoff template
    handoff_template = """# Claude Session Handoff Template

## Session Summary
**Duration**: X minutes
**Focus**: [Main objectives]
**Status**: [Complete/Blocked/In Progress]

## Accomplishments
- ✅ [What was completed]
- 🚧 [What was started]
- 📋 [What was documented]

## Current Blockers
- ⚠️ [Issue description and location]
- 🔧 [Technical debt or fixes needed]

## Next Session Priorities
1. [Highest priority item]
2. [Second priority]
3. [Third priority]

## Google Sheets Updates
- [Which tabs were updated]
- [New tasks added]
- [Status changes made]

## Demo Readiness
**Friday Brewery Demo**: X% ready
**Ready**: [What's working]
**Pending**: [What needs completion]

## Files Modified
- [List of key files changed]
- [New files created]
- [Configurations updated]
"""
    
    with open(claude_dir / 'handoff_template.md', 'w') as f:
        f.write(handoff_template)
    
    print("✅ Created .claude context structure")
    print("📁 Files created:")
    print("   .claude/context/current_session.md")
    print("   .claude/context/project_overview.md") 
    print("   .claude/prompts/deployment.md")
    print("   .claude/handoff_template.md")
    
    return claude_dir

if __name__ == "__main__":
    create_claude_context_structure()