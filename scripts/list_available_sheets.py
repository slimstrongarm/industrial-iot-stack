#!/usr/bin/env python3
"""
List available Google Sheets to find the correct Claude Tasks spreadsheet name
"""

import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

def list_sheets():
    """List all available Google Sheets"""
    
    try:
        # Load credentials
        creds_path = Path(__file__).parent.parent / "credentials" / "iot-stack-credentials.json"
        
        if not creds_path.exists():
            print(f"❌ Credentials not found at {creds_path}")
            return False
        
        # Setup Google Sheets client
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)
        
        print("✅ Connected to Google Sheets API")
        print("\n📊 Available Spreadsheets:")
        print("=" * 50)
        
        # List all spreadsheets
        spreadsheets = client.list_spreadsheet_files()
        
        for i, sheet in enumerate(spreadsheets, 1):
            print(f"{i:2d}. {sheet['name']}")
            if 'claude' in sheet['name'].lower() or 'task' in sheet['name'].lower() or 'iot' in sheet['name'].lower():
                print(f"    📋 ID: {sheet['id']}")
                
                # Try to open and list worksheets
                try:
                    spreadsheet = client.open_by_key(sheet['id'])
                    worksheets = spreadsheet.worksheets()
                    print(f"    📂 Worksheets: {[ws.title for ws in worksheets]}")
                except Exception as e:
                    print(f"    ⚠️ Could not access worksheets: {e}")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error listing sheets: {e}")
        return False

if __name__ == "__main__":
    list_sheets()