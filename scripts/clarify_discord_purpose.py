#!/usr/bin/env python3
"""
Update Discord tasks to clarify purpose: development tool, not POC demo
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def clarify_discord_purpose():
    """Update Discord task descriptions to clarify purpose"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        claude_sheet = sheet.worksheet('Claude Tasks')
        
        # Mark CT-021 as Complete
        records = claude_sheet.get_all_records()
        for i, record in enumerate(records):
            if record.get('Task ID') == 'CT-021':
                row_num = i + 2
                claude_sheet.update_cell(row_num, 5, "Complete")  # Status
                claude_sheet.update_cell(row_num, 10, datetime.now().strftime("%Y-%m-%d %H:%M"))  # Completed
                print("✅ Marked CT-021 Complete: Discord server created")
                break
        
        # Update task descriptions to clarify purpose
        task_updates = {
            'CT-022': 'Create Discord bot for development coordination (not POC demo)',
            'CT-023': 'Deploy Discord bot to help Josh build POC remotely',
            'CT-024': 'Connect bot to Google Sheets for development task management',
            'CT-025': 'Implement commands to help Josh monitor POC development',
            'CT-026': 'Setup development alerts for Josh while building POC',
            'CT-027': 'Deploy Discord development coordination bot'
        }
        
        # Update descriptions
        for i, record in enumerate(records):
            task_id = record.get('Task ID')
            if task_id in task_updates:
                row_num = i + 2
                claude_sheet.update_cell(row_num, 6, task_updates[task_id])  # Description column
                print(f"✅ Updated {task_id} description")
        
        # Log activity
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude", 
            "Discord purpose clarification",
            "Complete",
            "10 min",
            "Clarified Discord is development tool, not POC feature. Server created.",
            "Coordinate with Server Claude on bot deployment"
        ])
        
        print("\n🎯 Discord Purpose Clarified:")
        print("   💡 Development tool for Josh to coordinate with Claude instances")
        print("   📱 Remote POC development from iPhone")
        print("   🚀 NOT part of the brewery POC demo")
        print("   ✅ Discord server ready for bot deployment")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    clarify_discord_purpose()