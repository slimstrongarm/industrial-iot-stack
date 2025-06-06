#!/usr/bin/env python3
"""
Test Google Sheets API Connection
Run this after setting up credentials to verify everything works
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from pathlib import Path

# Your configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

# Try multiple credential locations
possible_creds_paths = [
    'credentials/iot-stack-credentials.json',
    '../credentials/iot-stack-credentials.json',
    str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'),
    os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '')
]

def find_credentials():
    """Find the credentials file"""
    for path in possible_creds_paths:
        if path and os.path.exists(path):
            return path
    return None

def test_connection():
    """Test the Google Sheets connection"""
    print("🔍 Testing Google Sheets API Connection...")
    print(f"📊 Sheet ID: {SHEET_ID}")
    
    # Find credentials
    creds_file = find_credentials()
    if not creds_file:
        print("""
❌ Credentials file not found!

Please follow these steps:
1. Go to https://console.cloud.google.com
2. Create a service account and download the JSON key
3. Save it as: ~/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json
4. Share your Google Sheet with the service account email

See GOOGLE_SHEETS_API_SETUP.md for detailed instructions.
""")
        return False
    
    print(f"📁 Using credentials: {creds_file}")
    
    try:
        # Authenticate
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        
        # Open sheet
        print("📖 Opening sheet...")
        sheet = client.open_by_key(SHEET_ID)
        print(f"✅ Connected to: {sheet.title}")
        
        # Test each worksheet
        print("\n📑 Worksheets found:")
        for ws in sheet.worksheets():
            print(f"  - {ws.title}")
        
        # Test read from Docker Migration Tasks
        print("\n📋 Reading Docker Migration Tasks...")
        worksheet = sheet.worksheet('Docker Migration Tasks')
        tasks = worksheet.get_all_records()
        
        print(f"✅ Found {len(tasks)} total tasks")
        
        # Show Claude tasks
        claude_tasks = [t for t in tasks if 'Claude' in t.get('Assigned To', '')]
        print(f"\n🤖 Tasks assigned to Claude: {len(claude_tasks)}")
        
        for task in claude_tasks:
            status_icon = "✅" if task['Status'] == 'Complete' else "⏳"
            print(f"  {status_icon} {task['Task ID']}: {task['Task Description']}")
        
        # Test write capability
        print("\n✍️  Testing write capability...")
        test_row = worksheet.find('DM-005')
        if test_row:
            current_note = worksheet.cell(test_row.row, 9).value
            test_note = "API connection verified ✅"
            worksheet.update_cell(test_row.row, 9, test_note)
            print(f"✅ Successfully updated task notes")
            # Restore original
            if current_note:
                worksheet.update_cell(test_row.row, 9, current_note)
        
        print("""
🎉 Success! Google Sheets API is working!

You can now run the monitoring script:
  python3 scripts/sheets_to_claude_sync.py

The script will:
- Check for new Claude tasks every 60 seconds
- Execute them automatically
- Update the sheet with progress
""")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        
        if "invalid_grant" in str(e):
            print("\n🔑 This might be a credential issue. Make sure:")
            print("1. You've shared the sheet with the service account email")
            print("2. The service account email has Editor access")
        
        return False

if __name__ == "__main__":
    # Create credentials directory if it doesn't exist
    creds_dir = Path.home() / 'Desktop/industrial-iot-stack/credentials'
    if not creds_dir.exists():
        print(f"📁 Creating credentials directory: {creds_dir}")
        creds_dir.mkdir(parents=True)
        
        # Create .gitignore
        gitignore_path = creds_dir / '.gitignore'
        with open(gitignore_path, 'w') as f:
            f.write("*.json\n*.key\n")
        print("📝 Created .gitignore for credentials")
    
    # Run test
    success = test_connection()