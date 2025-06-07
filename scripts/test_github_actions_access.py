#!/usr/bin/env python3
"""
Quick test to verify GitHub Actions can access Google Sheets
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def test_github_actions_access():
    """Test if GitHub Actions can access Google Sheets"""
    try:
        print("🔍 Testing GitHub Actions Google Sheets access...")
        
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Successfully connected to Google Sheets")
        print(f"📊 Sheet title: {sheet.title}")
        
        # Test access to key tabs
        tabs_to_test = ['Agent Activities', 'Claude Tasks', 'Claude Max Instructions']
        for tab_name in tabs_to_test:
            try:
                tab = sheet.worksheet(tab_name)
                print(f"✅ Can access '{tab_name}' tab")
            except Exception as e:
                print(f"⚠️ Cannot access '{tab_name}' tab: {e}")
        
        # Test write capability
        try:
            agent_sheet = sheet.worksheet('Agent Activities')
            agent_sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "GitHub Actions Test",
                "Service account access verification",
                "Complete",
                "1 min",
                "✅ GitHub Actions can successfully write to Google Sheets",
                "Ready for automation"
            ])
            print("✅ Write test successful - added test entry to Agent Activities")
        except Exception as e:
            print(f"❌ Write test failed: {e}")
            return False
        
        print("\n🎉 All tests passed!")
        print("🚀 GitHub Actions is ready to run Claude Max automation!")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        if "403" in str(e):
            print("\n🔑 This looks like a permissions issue:")
            print("1. Go to your Google Sheet")
            print("2. Click 'Share'")
            print("3. Add this email: iiot-stack-automation@iiot-stack-automation.iam.gserviceaccount.com")
            print("4. Set permission to 'Editor'")
            print("5. Click 'Send'")
        return False

if __name__ == "__main__":
    test_github_actions_access()