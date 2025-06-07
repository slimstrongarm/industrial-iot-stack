#!/usr/bin/env python3
"""
Fix CT-021 gap and add Discord server creation as first task
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def fix_ct021_gap():
    """Add CT-021 for Discord server creation"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to IoT Stack Progress Master")
        claude_sheet = sheet.worksheet('Claude Tasks')
        
        # Find row with CT-022 to insert CT-021 before it
        records = claude_sheet.get_all_records()
        ct022_row = None
        for i, record in enumerate(records):
            if record.get('Task ID') == 'CT-022':
                ct022_row = i + 2  # +2 because records are 0-indexed and row 1 is headers
                break
                
        if ct022_row:
            print(f"📝 Inserting CT-021 at row {ct022_row}")
            
            # Insert new row at CT-022 position
            claude_sheet.insert_row([
                "CT-021", 
                "Mac Claude", 
                "Discord Setup", 
                "High", 
                "Pending",
                "Create Discord server with proper channel structure", 
                "Discord server with #mac-claude, #server-claude, #general, #alerts, #logs channels",
                "CT-020",
                datetime.now().strftime("%Y-%m-%d"),
                ""
            ], ct022_row)
            
            print("✅ Added CT-021: Discord server creation")
            print("📋 Now tasks flow: CT-020 → CT-021 → CT-022 → CT-027")
            
        else:
            print("❌ Could not find CT-022 row")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_ct021_gap()