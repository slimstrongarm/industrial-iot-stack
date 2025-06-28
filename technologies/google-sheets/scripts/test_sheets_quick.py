#!/usr/bin/env python3
"""
Quick Google Sheets Connection Test
Test the connection after session recovery
"""

import gspread
from google.oauth2.service_account import Credentials

def test_connection():
    try:
        # Setup credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'credentials/iot-stack-credentials.json', 
            scopes=scope
        )
        
        # Connect to Google Sheets
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do')
        worksheet = sheet.worksheet('Claude Tasks')
        
        # Get task data
        records = worksheet.get_all_records()
        next_id = f"CT-{len(records) + 1:03d}"
        
        print("✅ Google Sheets Connection: SUCCESS")
        print(f"📊 Tasks Found: {len(records)}")
        print(f"🆔 Next Task ID: {next_id}")
        
        # Show last few tasks
        if records:
            print("\n📋 Recent Tasks:")
            for task in records[-3:]:
                status = task.get('Status', 'Unknown')
                task_id = task.get('ID', 'No ID')
                description = task.get('Task Description', 'No description')[:50]
                print(f"   {task_id}: {status} - {description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Google Sheets Error: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Google Sheets Connection...")
    print("=" * 50)
    success = test_connection()
    print("=" * 50)
    print("✅ Test Complete" if success else "❌ Test Failed")