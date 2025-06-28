#!/usr/bin/env python3
"""Update CT-030 to Complete status in Google Sheets"""

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

def update_ct030(service):
    """Find and update CT-030 to Complete"""
    
    # First, find CT-030
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G"
    ).execute()
    
    values = result.get('values', [])
    ct030_row = None
    
    for idx, row in enumerate(values):
        if row and (row[0] == 'CT-030' or row[0] == 'CT-30'):
            ct030_row = idx + 1
            print(f"Found CT-030 at row {ct030_row}")
            print(f"Current status: {row[4] if len(row) > 4 else 'Unknown'}")
            break
    
    if ct030_row:
        # Update status to Complete
        update_body = {
            'values': [["Complete"]]
        }
        
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Claude Tasks!E{ct030_row}",
            valueInputOption="RAW",
            body=update_body
        ).execute()
        
        print("✅ CT-030 marked as Complete!")
        
        # Update description with completion note
        completion_note = "GitHub Actions Claude integration complete! YAML syntax error fixed. Claude Max workflow operational, Claude Code Action fork ready for deployment. Can run automated health checks, deployments, and PR reviews."
        
        desc_body = {
            'values': [[completion_note]]
        }
        
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Claude Tasks!F{ct030_row}",
            valueInputOption="RAW",
            body=desc_body
        ).execute()
        
        print("✅ Updated task description with completion details!")
        
    else:
        print("❌ Could not find CT-030 in the sheet")
        print("Let me search for GitHub Actions related tasks...")
        
        # Search for GitHub Actions tasks
        for idx, row in enumerate(values):
            if row and 'github' in str(row).lower() and 'action' in str(row).lower():
                print(f"Row {idx+1}: {row[:3]}")

def main():
    """Main execution"""
    print("Updating CT-030 GitHub Actions task...\n")
    
    service = get_sheets_service()
    update_ct030(service)
    
    print("\n🎉 CT-030 Update Complete!")
    print("\nYou now have:")
    print("- Working Claude Max automation workflow")
    print("- Claude Code Action fork ready to deploy")
    print("- Fixed YAML syntax error that was blocking progress")
    print("\nGitHub Actions + Claude integration is ready to rock! 🚀")

if __name__ == "__main__":
    main()