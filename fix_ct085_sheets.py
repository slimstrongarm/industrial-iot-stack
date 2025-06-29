#!/usr/bin/env python3
"""
Fix CT-085 Google Sheets entry with correct column structure
"""

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import datetime

# Google Sheets configuration
SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
CREDENTIALS_PATH = "/home/server/google-sheets-credentials.json"
SHEET_NAME = "Claude Tasks"

def get_sheets_service():
    """Initialize and return Google Sheets service"""
    credentials = Credentials.from_service_account_file(
        CREDENTIALS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service

def fix_ct085_entry():
    """Fix CT-085 entry with correct column structure"""
    service = get_sheets_service()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # The correct column structure based on headers:
    # A=Task ID, B=Instance, C=Task Type, D=Priority, E=Status, F=Description, G=Expected Output, H=Dependencies, I=Date Added, J=Completed
    
    # Update only the Status (E) and Completed (J) columns
    updates = []
    
    # Update Status to COMPLETED (Column E, Row 87)
    updates.append({
        'range': f"'{SHEET_NAME}'!E87",
        'values': [['COMPLETED']]
    })
    
    # Update Completed date (Column J, Row 87)
    updates.append({
        'range': f"'{SHEET_NAME}'!J87", 
        'values': [[today]]
    })
    
    # Batch update
    body = {
        'valueInputOption': 'RAW',
        'data': updates
    }
    
    try:
        result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=body
        ).execute()
        
        print("✅ CT-085 successfully updated in Google Sheets:")
        print(f"   Status (Column E): COMPLETED")
        print(f"   Completed Date (Column J): {today}")
        print("   Following correct column structure!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating CT-085: {e}")
        return False

if __name__ == "__main__":
    fix_ct085_entry()