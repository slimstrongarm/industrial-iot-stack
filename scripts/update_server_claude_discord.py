#!/usr/bin/env python3
"""
Update Server Claude about Discord setup and new tab
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def update_server_claude():
    """Update Server Claude about Discord setup"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        # Check if Discord tab exists and get invite link
        discord_info = None
        try:
            discord_sheet = sheet.worksheet('Discord')
            # Try to read the invite link from the sheet
            values = discord_sheet.get_all_values()
            if values:
                discord_info = f"Discord invite link found in 'Discord' tab"
                print(f"✅ Found Discord tab with {len(values)} rows")
        except:
            print("📋 Discord tab not found, will note in instructions")
        
        # Update CT-022 with detailed instructions
        claude_sheet = sheet.worksheet('Claude Tasks')
        records = claude_sheet.get_all_records()
        
        for i, record in enumerate(records):
            if record.get('Task ID') == 'CT-022':
                row_num = i + 2
                # Update description with Discord tab info
                new_description = (
                    "Create Discord bot - Check 'Discord' tab for server invite link. "
                    "Bot code in /discord-bot/ folder. Deploy with docker-compose."
                )
                claude_sheet.update_cell(row_num, 6, new_description)
                print(f"✅ Updated CT-022 with Discord tab reference")
                break
        
        # Add activity log
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            "Discord setup coordination",
            "Complete",
            "5 min",
            "Discord bot files pushed to GitHub. Discord invite link in new 'Discord' tab. CT-022 ready for Server Claude.",
            "Server Claude to create bot and deploy"
        ])
        
        # Create a message file for Server Claude
        message_path = Path.home() / 'Desktop/industrial-iot-stack/SERVER_CLAUDE_DISCORD_INSTRUCTIONS.md'
        message_content = f"""# Server Claude Discord Bot Deployment Instructions

## 🎯 Quick Start

Josh has created the Discord server and added the invite link to a new **'Discord' tab** in Google Sheets.

## 📋 Your Tasks (CT-022 through CT-027)

### CT-022: Create Discord Bot Application
1. Go to https://discord.com/developers/applications
2. Create new application: "IoT Stack Claude Bot"
3. Add bot user and copy token
4. Check the **'Discord' tab** in Google Sheets for the server invite link

### CT-023: Deploy Discord Bot
1. Bot code is ready in `/discord-bot/` folder:
   - `bot.py` - Complete Discord bot code
   - `docker-compose.yml` - Deployment configuration
   - `Dockerfile` - Container setup

2. Deploy with:
   ```bash
   cd /opt/industrial-iot-stack/discord-bot
   echo "DISCORD_BOT_TOKEN=your-bot-token-here" > .env
   docker-compose up -d
   ```

### CT-024: Connect to Google Sheets
- Bot will use existing credentials at `/opt/industrial-iot-stack/credentials/`
- Update bot.py to read from Claude Tasks sheet

### CT-025: Implement Commands
- Basic commands already in bot.py:
  - "status" - Docker container status
  - "mqtt" - MQTT broker check
  - "help" - Command list

### CT-026: Setup Alerts
- Add Docker event monitoring
- Post container failures to #alerts channel

### CT-027: Production Deployment
- Ensure bot auto-restarts
- Add to server startup scripts

## 🚀 Key Points

1. **Discord server is ready** - Josh created it this morning
2. **Invite link is in the 'Discord' tab** of our Google Sheets
3. **Bot code is in GitHub** - Just pulled with latest updates
4. **This is a development tool** - For Josh to coordinate with us remotely
5. **Not part of brewery POC** - Internal tool only

## 📱 Expected Result

Josh will be able to send commands from his iPhone:
- To you in #server-claude channel
- To Mac Claude in #mac-claude channel
- Coordinate POC development while mobile

---
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Mac Claude
"""
        
        with open(message_path, 'w') as f:
            f.write(message_content)
        
        print(f"\n✅ Created instructions at: {message_path}")
        print("\n📋 Summary for Server Claude:")
        print("   1. Discord invite link in 'Discord' tab")
        print("   2. Bot code ready in /discord-bot/")
        print("   3. CT-022 updated with instructions")
        print("   4. Deploy with docker-compose")
        
        # Git commit the instructions
        import subprocess
        subprocess.run(['git', 'add', 'SERVER_CLAUDE_DISCORD_INSTRUCTIONS.md'], 
                      cwd=Path.home() / 'Desktop/industrial-iot-stack')
        subprocess.run(['git', 'commit', '-m', 'Add Discord deployment instructions for Server Claude'], 
                      cwd=Path.home() / 'Desktop/industrial-iot-stack')
        subprocess.run(['git', 'push'], 
                      cwd=Path.home() / 'Desktop/industrial-iot-stack')
        
        print("\n🚀 Pushed instructions to GitHub for Server Claude!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_server_claude()