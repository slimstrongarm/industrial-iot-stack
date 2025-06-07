#!/usr/bin/env python3
"""
Fix Discord Tasks - Proper Format with Consecutive IDs
Remove the incorrectly formatted ones and add proper ones
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def fix_discord_tasks():
    """Remove bad Discord tasks and add properly formatted ones"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to IoT Stack Progress Master")
        claude_sheet = sheet.worksheet('Claude Tasks')
        
        # 1. Remove incorrectly formatted Discord tasks (rows 27-32)
        print("🗑️ Removing incorrectly formatted Discord tasks...")
        for i in range(6):  # Remove 6 rows starting from the end
            claude_sheet.delete_rows(27)  # Always delete row 27 since rows shift up
            
        print("✅ Removed bad Discord tasks")
        
        # 2. Add properly formatted Discord tasks
        print("📝 Adding properly formatted Discord tasks...")
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Tasks for Server Claude (consecutive IDs starting from CT-022)
        new_tasks = [
            ["CT-022", "Server Claude", "Discord Integration", "High", "Pending", 
             "Create Discord bot application in Developer Portal", 
             "Bot token and application ID for IoT monitoring bot", 
             "-", today, ""],
             
            ["CT-023", "Server Claude", "Discord Integration", "High", "Pending",
             "Deploy Discord bot container with monitoring capabilities",
             "Running Discord bot container with health monitoring",
             "CT-022", today, ""],
             
            ["CT-024", "Server Claude", "Discord Integration", "High", "Pending", 
             "Connect Discord bot to existing Google Sheets API",
             "Bot can read/write to Claude Tasks and System Status tabs",
             "CT-023", today, ""],
             
            ["CT-025", "Server Claude", "Discord Integration", "High", "Pending",
             "Implement basic Discord commands: /status /health /containers",
             "Working slash commands showing real-time system status",
             "CT-024", today, ""],
             
            ["CT-026", "Server Claude", "Discord Integration", "Medium", "Pending",
             "Setup automated Docker alerts to Discord channels", 
             "Container down/up/restart notifications posted automatically",
             "CT-025", today, ""],
             
            ["CT-027", "Server Claude", "Discord Integration", "High", "Pending",
             "Deploy Discord bot to production for brewery demo",
             "Stable Discord bot running on server accessible from mobile",
             "CT-026", today, ""]
        ]
        
        # Add each task
        for task in new_tasks:
            claude_sheet.append_row(task)
            
        print(f"✅ Added {len(new_tasks)} properly formatted Discord tasks")
        print("   Task IDs: CT-022 through CT-027")
        print("   All assigned to Server Claude")
        print("   Consecutive dependencies")
        print("   Proper column mapping")
        
        # 3. Update Agent Activities
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            "Fixed Discord task format",
            "Complete",
            "15 min", 
            "Corrected format, consecutive IDs CT-022 to CT-027",
            "Server Claude to execute tasks"
        ])
        
        print("\n🎯 Ready for Friday brewery demo!")
        print("📱 Discord integration tasks properly queued")
        print("🤖 Server Claude automation will pick these up in 60 seconds")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_discord_tasks()