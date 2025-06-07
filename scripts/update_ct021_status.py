#!/usr/bin/env python3
"""
Update CT-021 status to pending until tomorrow
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def update_status():
    """Update CT-021 with tonight's progress"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        # Update Agent Activities
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            "Discord integration planning complete",
            "Complete",
            "45 min",
            "Vision documented, tasks organized, ready for Discord server creation tomorrow",
            "Create Discord server and coordinate with Server Claude"
        ])
        
        print("✅ Updated progress for tonight")
        print("📋 Ready to continue tomorrow with Discord server creation")
        print("🎯 Still on track for Friday brewery demo")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_status()