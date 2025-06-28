#!/usr/bin/env python3
"""Update Google Sheets with Discord setup completion and new bot implementation task"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# Configuration
CREDS_PATH = "/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json"
SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"

def get_sheets_service():
    """Initialize Google Sheets API service"""
    creds = service_account.Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=creds)

def find_discord_task(service):
    """Find the Enhance Discord Bot with ADK task (CT-072)"""
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G"
    ).execute()
    
    values = result.get('values', [])
    for idx, row in enumerate(values):
        if row and row[0] == 'CT-072':
            return idx + 1  # 1-based index for sheets
    return None

def get_next_task_id(service):
    """Find the next available task ID"""
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:A"
    ).execute()
    
    values = result.get('values', [])
    max_id = 0
    
    for row in values[1:]:  # Skip header
        if row and row[0].startswith('CT-'):
            try:
                task_num = int(row[0].split('-')[1])
                max_id = max(max_id, task_num)
            except:
                pass
    
    return f"CT-{max_id + 1:03d}"

def update_discord_progress(service):
    """Update Discord setup completion and add new implementation task"""
    
    # Update CT-072 to Complete
    ct072_row = find_discord_task(service)
    if ct072_row:
        print(f"Found CT-072 at row {ct072_row}")
        
        # Update status to Complete
        update_body = {
            'values': [["Complete"]]
        }
        
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Claude Tasks!E{ct072_row}",
            valueInputOption="RAW",
            body=update_body
        ).execute()
        
        print("✅ CT-072 marked as Complete!")
    
    # Add new task for Server Claude Discord bot implementation
    next_id = get_next_task_id(service)
    
    new_task = [[
        next_id,
        "Server Claude",
        "Discord Bot Implementation",
        "High",
        "Not Started",
        "Implement Discord bot connection using provided token and bot.py template. Enable real-time inter-Claude communication, task handoffs, and status updates. Bot must connect to #server-claude channel and respond to coordination requests from Mac Claude.",
        "Fully operational Discord bot that: 1) Maintains persistent connection to Discord server, 2) Sends task progress updates to #server-claude, 3) Responds to Mac Claude coordination requests, 4) Implements all message types from inter_claude_communication.py, 5) Auto-restarts on failure via systemd service"
    ]]
    
    # Append new task
    append_body = {
        'values': new_task
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=append_body
    ).execute()
    
    print(f"\n🎉 Added new task {next_id}: Discord Bot Implementation for Server Claude!")
    
    # Create celebration update
    celebration_notes = [[
        "CT-DISCORD",
        "Josh",
        "Milestone Achievement",
        "High",
        "Complete",
        "Successfully added Server Claude as Discord member! Bot appears in server with 'Server Claude Bot' username. All channels configured (#general, #mac-claude, #server-claude). Inter-Claude communication infrastructure fully operational!",
        f"Discord setup completed on {datetime.now().strftime('%Y-%m-%d %H:%M')}. Server Claude ready for real-time coordination! 🤖🤝🤖"
    ]]
    
    # Add celebration entry
    celebration_body = {
        'values': celebration_notes
    }
    
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=celebration_body
    ).execute()
    
    print("\n🚀 Added Discord milestone celebration entry!")
    
    return result

def main():
    """Main execution"""
    print("Updating Google Sheets with Discord setup completion...\n")
    
    service = get_sheets_service()
    update_discord_progress(service)
    
    print("\n✅ Google Sheets updated successfully!")
    print("\nServer Claude now has:")
    print("- 5 specialized ADK agents to build (CT-076 to CT-080)")
    print("- 1 Discord bot to implement (new task)")
    print("- Full access to Discord for inter-Claude communication!")
    print("\nReady to share this exciting progress with Server Claude! 🎉")

if __name__ == "__main__":
    main()