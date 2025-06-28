#!/usr/bin/env python3
"""Update CT-084 progress and mark as In Progress"""

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

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

def update_ct084_status(service):
    """Update CT-084 to In Progress"""
    
    # Find CT-084
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="Claude Tasks!A:G"
    ).execute()
    
    values = result.get('values', [])
    ct084_row = None
    
    for idx, row in enumerate(values):
        if row and row[0] == 'CT-084':
            ct084_row = idx + 1
            break
    
    if ct084_row:
        # Update status to In Progress
        status_body = {
            'values': [['In Progress']]
        }
        
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Claude Tasks!E{ct084_row}",
            valueInputOption="RAW",
            body=status_body
        ).execute()
        
        # Update description with progress
        progress_desc = "STARTED: Building Parachute Drop Pi image with enhanced discovery agents. Created: 1) Complete Pi image builder script, 2) Enhanced discovery agent with AI-powered tag intelligence, 3) Auto sensor configurator for Phidget hub, 4) Node-RED dashboard generator. Production-ready deployment image in development."
        
        desc_body = {
            'values': [[progress_desc]]
        }
        
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"Claude Tasks!F{ct084_row}",
            valueInputOption="RAW",
            body=desc_body
        ).execute()
        
        print("✅ CT-084 updated to 'In Progress' with detailed progress notes")
    else:
        print("❌ Could not find CT-084")

def main():
    """Main execution"""
    print("📊 Updating CT-084 progress...")
    
    service = get_sheets_service()
    update_ct084_status(service)
    
    print("\n🪂 CT-084 Progress Update Complete!")
    print("Mac Claude is building the Parachute Drop foundation while Server Claude works on specialized agents!")

if __name__ == "__main__":
    main()