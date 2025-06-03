#!/usr/bin/env python3
"""
Check Screenshots tab in Google Sheets
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def check_screenshots():
    """Check the Screenshots tab for images and data"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to IoT Stack Progress Master")
        
        # Get Screenshots worksheet
        try:
            worksheet = sheet.worksheet('Screenshots')
            print("✅ Found Screenshots tab")
            
            # Get all values to see what's there
            all_values = worksheet.get_all_values()
            print(f"\n📊 Sheet has {len(all_values)} rows")
            
            # Print first few rows to see structure
            for i, row in enumerate(all_values[:20], 1):
                if any(cell for cell in row):  # If row has any content
                    print(f"Row {i}: {row[:3]}...")  # Show first 3 columns
            
            # Check for images in specific cells
            # Note: gspread doesn't directly support reading images, 
            # but we can see the sheet structure
            
        except Exception as e:
            print(f"❌ Error accessing Screenshots tab: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_screenshots()