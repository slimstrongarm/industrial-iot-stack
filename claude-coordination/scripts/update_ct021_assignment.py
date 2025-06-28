#!/usr/bin/env python3
"""
Update CT-021 assignment to Mac Claude and mark as in progress
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def update_ct021():
    """Update CT-021 assignment and status"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        claude_sheet = sheet.worksheet('Claude Tasks')
        
        # Find CT-021 row
        records = claude_sheet.get_all_records()
        for i, record in enumerate(records):
            if record.get('Task ID') == 'CT-021':
                row_num = i + 2  # +2 for header row and 0-indexing
                
                # Update Instance to Mac Claude and Status to In Progress
                claude_sheet.update_cell(row_num, 2, "Mac Claude")  # Instance column
                claude_sheet.update_cell(row_num, 5, "In Progress")  # Status column
                
                print(f"✅ Updated CT-021:")
                print(f"   Instance: Mac Claude")
                print(f"   Status: In Progress")
                print(f"   Task: Create Discord server with channel structure")
                
                # Log activity
                agent_sheet = sheet.worksheet('Agent Activities')
                agent_sheet.append_row([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Mac Claude",
                    "CT-021 Discord server creation",
                    "In Progress",
                    "0 min",
                    "Took ownership of Discord server setup task",
                    "Create server and coordinate with Server Claude"
                ])
                
                return True
                
        print("❌ Could not find CT-021")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    update_ct021()