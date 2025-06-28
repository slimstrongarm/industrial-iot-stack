#!/usr/bin/env python3
"""
Test Google Sheets integration independently
Verifies the bot can write to Claude Tasks sheet
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Configuration
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_PATH = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'

def test_sheets_access():
    """Test Google Sheets access and task creation"""
    print("🧪 Testing Google Sheets Integration")
    print("=" * 50)
    
    try:
        # Initialize client
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
        gc = gspread.authorize(creds)
        print("✅ Google Sheets client authorized")
        
        # Open spreadsheet
        sheet = gc.open_by_key(SPREADSHEET_ID)
        print(f"✅ Opened spreadsheet: {sheet.title}")
        
        # Get Claude Tasks worksheet
        claude_tasks = sheet.worksheet('Claude Tasks')
        print(f"✅ Found worksheet: Claude Tasks")
        
        # Get all values to find the next task ID
        all_values = claude_tasks.get_all_values()
        print(f"✅ Retrieved {len(all_values)} rows")
        
        # Find the last CT number
        last_ct_num = 0
        for row in all_values:
            if row and row[0].startswith('CT-'):
                try:
                    ct_num = int(row[0].split('-')[1])
                    if ct_num > last_ct_num:
                        last_ct_num = ct_num
                except:
                    continue
        
        print(f"✅ Last task ID found: CT-{last_ct_num:03d}")
        
        # Create test task
        new_task_id = f"CT-{last_ct_num + 1:03d}"
        test_row = [
            new_task_id,
            "Discord Bot Test",
            "Test Google Sheets Integration",
            "Low",
            "Pending",
            f"Test task created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "Verify Discord bot can write to sheets",
            ""
        ]
        
        print(f"\n📝 Creating test task: {new_task_id}")
        print(f"   Title: Test Google Sheets Integration")
        
        # Append row
        claude_tasks.append_row(test_row)
        print(f"✅ Successfully created {new_task_id}")
        print(f"\n🔗 View at: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_bot_permissions():
    """Check if service account has proper permissions"""
    print("\n🔍 Checking Service Account Permissions")
    print("=" * 50)
    
    try:
        with open(CREDENTIALS_PATH, 'r') as f:
            import json
            creds_data = json.load(f)
            print(f"✅ Service Account: {creds_data['client_email']}")
            print("\n⚠️  Make sure this service account has edit access to the spreadsheet!")
            print("   1. Open the spreadsheet in Google Sheets")
            print("   2. Click 'Share' button")
            print(f"   3. Add: {creds_data['client_email']}")
            print("   4. Set permission to 'Editor'")
            
    except Exception as e:
        print(f"❌ Could not read credentials: {e}")

if __name__ == "__main__":
    # Test sheets access
    success = test_sheets_access()
    
    # Check permissions
    check_bot_permissions()
    
    if success:
        print("\n✅ Google Sheets integration is working!")
        print("The Discord bot should be able to create tasks.")
    else:
        print("\n❌ Google Sheets integration failed!")
        print("Check the error messages above.")