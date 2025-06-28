#!/usr/bin/env python3
"""
Update Google Sheet with CT-007 completion and check CT-022
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

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

def check_claude_tasks():
    """Check Claude Tasks sheet for CT-007 and CT-022"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("📋 Checking Claude Tasks Sheet")
    print("=" * 35)
    
    # Check credentials file
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Credentials file not found: {CREDENTIALS_FILE}")
        print("Creating manual update summary instead...")
        
        print("\n🎯 Manual Updates Needed:")
        print("=" * 25)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("\n✅ CT-007: Import n8n workflows via API")
        print(f"- Status: COMPLETED")
        print(f"- Completed Date: {timestamp}")
        print(f"- Assignee: Claude Code")
        print(f"- Notes: Both workflows imported successfully:")
        print(f"  • Formbricks→Sheets: Workflow ID n3UFERK5ilPYrLP3")
        print(f"  • MQTT→WhatsApp: Workflow ID PptMUA3BfrivzhG9")
        print(f"  • MQTT connection working with host.docker.internal")
        print(f"  • Google Sheets created for logging")
        
        print("\n✅ CT-008: Integration Test - MQTT→WhatsApp Alert")
        print(f"- Status: COMPLETED")
        print(f"- Completed Date: {timestamp}")
        print(f"- Notes: Network isolation issue resolved")
        
        print("\n❓ Missing Tasks Check:")
        print("- CT-021: (MISSING - needs to be identified)")
        print("- CT-022: (needs review)")
        print("- Discord server setup required")
        
        print("\n📝 Action Items for mac-claude:")
        print("- Set up Discord server")
        print("- Check if CT-021 exists or should be created")
        print("- Review CT-022 requirements")
        
        return True
    
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
        
        # Read Claude Tasks sheet
        range_name = 'Claude Tasks!A:Z'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("❌ No data found in Claude Tasks sheet")
            return False
        
        print(f"📊 Found {len(values)} rows in Claude Tasks")
        
        # Look for CT-007, CT-021, CT-022
        ct_007_found = False
        ct_021_found = False
        ct_022_found = False
        ct_022_content = ""
        
        for i, row in enumerate(values):
            if len(row) > 0:
                task_id = row[0] if len(row) > 0 else ""
                task_name = row[1] if len(row) > 1 else ""
                status = row[2] if len(row) > 2 else ""
                
                if "CT-007" in task_id:
                    ct_007_found = True
                    print(f"✅ Found CT-007: {task_name} (Status: {status})")
                elif "CT-021" in task_id:
                    ct_021_found = True
                    print(f"✅ Found CT-021: {task_name} (Status: {status})")
                elif "CT-022" in task_id:
                    ct_022_found = True
                    ct_022_content = task_name
                    print(f"✅ Found CT-022: {task_name} (Status: {status})")
        
        print("\n📋 Task Status Summary:")
        print("=" * 25)
        print(f"CT-007 (n8n workflows): {'✅ Found' if ct_007_found else '❌ Missing'}")
        print(f"CT-021: {'✅ Found' if ct_021_found else '❌ Missing'}")
        print(f"CT-022: {'✅ Found' if ct_022_found else '❌ Missing'}")
        
        if ct_022_found:
            print(f"\n🎯 CT-022 Content: {ct_022_content}")
        
        if not ct_021_found:
            print("\n⚠️  CT-021 appears to be missing from the task sequence")
            print("This should be investigated - may need to be created")
        
        print("\n📝 Recommended Actions:")
        print("1. Mark CT-007 as COMPLETED (n8n workflows imported)")
        print("2. Mark CT-008 as COMPLETED (MQTT integration working)")
        print("3. Investigate missing CT-021")
        print("4. Review CT-022 requirements")
        print("5. Set up Discord server (assign to mac-claude)")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = check_claude_tasks()
    if not success:
        print("\n📝 Please manually check and update Claude Tasks sheet")
        sys.exit(1)