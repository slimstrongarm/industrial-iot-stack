#!/usr/bin/env python3
"""
Test Google Sheets API access for Mac Claude
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from datetime import datetime
import os

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def test_sheets_connection():
    """Test basic connection to Google Sheets"""
    try:
        # Load credentials
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Test: Read from Claude Tasks tab
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A1:J10'
        ).execute()
        
        values = result.get('values', [])
        if values:
            print("✅ Successfully connected to Google Sheets!")
            print(f"Found {len(values)} rows in Claude Tasks tab")
            print("\nCurrent Claude Tasks:")
            for i, row in enumerate(values):
                if i == 0:  # Header row
                    print(f"Headers: {row}")
                else:
                    task_id = row[0] if len(row) > 0 else 'N/A'
                    instance = row[1] if len(row) > 1 else 'N/A'
                    status = row[4] if len(row) > 4 else 'N/A'
                    description = row[5] if len(row) > 5 else 'N/A'
                    print(f"  {task_id} ({instance}): {status} - {description[:50]}...")
            
            return service, sheet
        else:
            print("❌ No data found in Claude Tasks tab")
            return None, None
            
    except FileNotFoundError:
        print(f"❌ Credentials file not found: {SERVICE_ACCOUNT_FILE}")
        return None, None
    except Exception as e:
        print(f"❌ Error connecting to Google Sheets: {e}")
        return None, None

if __name__ == "__main__":
    print("🧪 Testing Google Sheets API access for Mac Claude...")
    
    # Check if credentials file exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Credentials file not found at: {SERVICE_ACCOUNT_FILE}")
        print("Please ensure the file exists and try again.")
        exit(1)
    
    service, sheet = test_sheets_connection()
    
    if service and sheet:
        print("\n🎉 Google Sheets integration is working!")
        print("Mac Claude now has the same capability as Server Claude")
    else:
        print("\n❌ Google Sheets integration failed")
        print("Please check credentials and try again")