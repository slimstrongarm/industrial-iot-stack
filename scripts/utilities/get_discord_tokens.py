#!/usr/bin/env python3
"""Get Discord tokens from Google Sheets"""

import gspread
from google.oauth2.service_account import Credentials

try:
    # Setup Google Sheets
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json', scopes=scope)
    client = gspread.authorize(creds)

    # Open spreadsheet
    sheet = client.open_by_key('1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do')
    
    # Try to find Discord tab
    try:
        discord_tab = sheet.worksheet('Discord')
        print("✅ Found Discord tab")
        
        # Get all values
        values = discord_tab.get_all_values()
        print("\n📋 Discord Tab Contents:")
        for i, row in enumerate(values[:10]):  # Show first 10 rows
            if any(cell.strip() for cell in row):  # Only show non-empty rows
                print(f"Row {i+1}: {row}")
                
    except gspread.WorksheetNotFound:
        print("❌ Discord tab not found")
        print("\n📋 Available tabs:")
        for worksheet in sheet.worksheets():
            print(f"  - {worksheet.title}")
            
except Exception as e:
    print(f"❌ Error: {e}")