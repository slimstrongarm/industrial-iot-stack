#!/usr/bin/env python3
"""
Setup Google Sheets for MQTT Equipment Alert logging
Creates required sheets with proper headers
"""

import json
import sys
import os
from pathlib import Path

# Add the scripts directory to Python path for imports
script_dir = Path(__file__).parent
sys.path.append(str(script_dir))

try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Google API libraries not installed")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

def setup_sheets():
    """Setup Google Sheets for MQTT logging"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔧 Setting up Google Sheets for MQTT Equipment Alerts")
    print("=" * 55)
    
    # Check credentials file
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Credentials file not found: {CREDENTIALS_FILE}")
        print("Please ensure the service account JSON file is available")
        return False
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        
        print("✅ Connected to Google Sheets API")
        
        # Sheet configurations
        sheets_config = [
            {
                "title": "Equipment Alerts",
                "headers": ["Timestamp", "Equipment_ID", "Equipment_Type", "Location", 
                           "Severity", "Topic", "Alert_Sent", "Raw_Data"]
            },
            {
                "title": "All Equipment Events", 
                "headers": ["Timestamp", "Equipment_ID", "Equipment_Type", "Location",
                           "Severity", "Topic", "Priority", "Raw_Data"]
            }
        ]
        
        # Get existing sheets
        spreadsheet = sheet.get(spreadsheetId=SPREADSHEET_ID).execute()
        existing_sheets = [s['properties']['title'] for s in spreadsheet['sheets']]
        
        print(f"📋 Existing sheets: {existing_sheets}")
        
        # Create sheets if they don't exist
        for sheet_config in sheets_config:
            sheet_title = sheet_config["title"]
            headers = sheet_config["headers"]
            
            if sheet_title not in existing_sheets:
                print(f"📝 Creating sheet: {sheet_title}")
                
                # Create new sheet
                request_body = {
                    'requests': [{
                        'addSheet': {
                            'properties': {
                                'title': sheet_title,
                                'gridProperties': {
                                    'rowCount': 1000,
                                    'columnCount': len(headers)
                                }
                            }
                        }
                    }]
                }
                
                sheet.batchUpdate(
                    spreadsheetId=SPREADSHEET_ID,
                    body=request_body
                ).execute()
                
                # Add headers
                values = [headers]
                sheet.values().update(
                    spreadsheetId=SPREADSHEET_ID,
                    range=f"'{sheet_title}'!A1",
                    valueInputOption='RAW',
                    body={'values': values}
                ).execute()
                
                print(f"✅ Created sheet '{sheet_title}' with headers")
            else:
                print(f"✅ Sheet '{sheet_title}' already exists")
        
        print("")
        print("🎯 Google Sheets Setup Complete!")
        print(f"📊 Spreadsheet: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        print("")
        print("Next steps:")
        print("1. Configure Google Sheets credentials in n8n")
        print("2. Test MQTT → Sheets logging")
        print("3. Set up WhatsApp API for alerts")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = setup_sheets()
    if not success:
        sys.exit(1)