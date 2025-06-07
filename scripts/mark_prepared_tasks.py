#!/usr/bin/env python3
"""
Mark tasks as prepared that Mac Claude completed for Server Claude
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def mark_prepared_tasks():
    """Mark tasks as prepared for Server Claude"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        claude_sheet = sheet.worksheet('Claude Tasks')
        records = claude_sheet.get_all_records()
        
        # Tasks I've prepared for Server Claude
        completed_prep = {
            'CT-016': 'Ignition API scripts created in /ignition-scripts/ folder. Ready for deployment.',
            'CT-024': 'Enhanced Discord bot with Google Sheets integration ready in /discord-bot/',
            'CT-025': 'Discord monitoring commands implemented in enhanced_bot.py'
        }
        
        # Update task statuses
        for i, record in enumerate(records):
            task_id = record.get('Task ID')
            if task_id in completed_prep:
                row_num = i + 2
                
                if task_id == 'CT-025':
                    # Mark as complete
                    claude_sheet.update_cell(row_num, 5, "Complete")
                    claude_sheet.update_cell(row_num, 10, datetime.now().strftime("%Y-%m-%d %H:%M"))
                else:
                    # Mark as in progress with notes
                    claude_sheet.update_cell(row_num, 5, "In Progress") 
                
                # Update description
                claude_sheet.update_cell(row_num, 6, completed_prep[task_id])
                print(f"✅ Updated {task_id}")
        
        # Log comprehensive activity
        agent_sheet = sheet.worksheet('Agent Activities')
        agent_sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            "Server Claude task preparation complete", 
            "Complete",
            "45 min",
            "Enhanced Discord bot, Ignition API scripts, Google Sheets integration ready. CT-016, CT-024, CT-025 prepared.",
            "Server Claude ready to deploy and test integrations"
        ])
        
        print("\n🎯 Preparation Summary:")
        print("   ✅ CT-016: Ignition API scripts → /ignition-scripts/")
        print("   ✅ CT-024: Discord + Google Sheets → /discord-bot/enhanced_bot.py") 
        print("   ✅ CT-025: Monitoring commands implemented")
        print("\n📤 Server Claude can now deploy and test!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    mark_prepared_tasks()