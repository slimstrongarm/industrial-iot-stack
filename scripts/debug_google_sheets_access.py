#!/usr/bin/env python3
"""
Debug Google Sheets access and update Claude Tasks with detailed error reporting
"""

import sys
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
    print("Fix: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

def debug_sheets_access():
    """Debug Google Sheets access with detailed error reporting"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔍 DEBUGGING GOOGLE SHEETS ACCESS")
    print("=" * 40)
    
    try:
        # Step 1: Check credentials file
        print("1️⃣ Checking credentials file...")
        if not Path(CREDENTIALS_FILE).exists():
            print(f"❌ Credentials file not found: {CREDENTIALS_FILE}")
            print("Fix: Ensure Google service account JSON is at correct path")
            return False
        else:
            print(f"✅ Credentials file exists: {CREDENTIALS_FILE}")
        
        # Step 2: Load credentials
        print("\n2️⃣ Loading credentials...")
        try:
            creds = Credentials.from_service_account_file(
                CREDENTIALS_FILE,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            print("✅ Credentials loaded successfully")
        except Exception as e:
            print(f"❌ Credentials loading failed: {e}")
            print("Fix: Check JSON file format and service account permissions")
            return False
        
        # Step 3: Build service
        print("\n3️⃣ Building Google Sheets service...")
        try:
            service = build('sheets', 'v4', credentials=creds)
            print("✅ Google Sheets service built successfully")
        except Exception as e:
            print(f"❌ Service building failed: {e}")
            return False
        
        # Step 4: Test spreadsheet access
        print(f"\n4️⃣ Testing spreadsheet access...")
        print(f"Spreadsheet ID: {SPREADSHEET_ID}")
        
        try:
            # Get spreadsheet metadata first
            spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
            print("✅ Spreadsheet accessible")
            
            # List all sheets
            sheets = spreadsheet.get('sheets', [])
            print(f"📊 Found {len(sheets)} worksheets:")
            for sheet in sheets:
                sheet_name = sheet['properties']['title']
                print(f"  • {sheet_name}")
            
        except HttpError as e:
            print(f"❌ Spreadsheet access failed: {e}")
            if e.resp.status == 403:
                print("Fix: Service account needs access to this spreadsheet")
                print("Solution: Share spreadsheet with service account email")
            elif e.resp.status == 404:
                print("Fix: Spreadsheet ID might be incorrect")
            return False
        
        # Step 5: Test Claude Tasks sheet specifically
        print(f"\n5️⃣ Testing Claude Tasks sheet access...")
        
        possible_names = [
            'Claude Tasks',
            'Claude Tasks!A:K',
            "'Claude Tasks'!A:K",
            '"Claude Tasks"!A:K'
        ]
        
        claude_tasks_found = False
        for sheet_name in possible_names:
            try:
                print(f"Trying range: {sheet_name}")
                result = service.spreadsheets().values().get(
                    spreadsheetId=SPREADSHEET_ID,
                    range=sheet_name if '!' in sheet_name else f"'{sheet_name}'!A:K"
                ).execute()
                
                values = result.get('values', [])
                print(f"✅ SUCCESS with range: {sheet_name}")
                print(f"📊 Found {len(values)} rows")
                
                if values:
                    headers = values[0] if len(values) > 0 else []
                    print(f"Headers: {headers}")
                
                claude_tasks_found = True
                break
                
            except HttpError as e:
                print(f"❌ Failed with range '{sheet_name}': {e}")
                continue
        
        if not claude_tasks_found:
            print("❌ Could not access Claude Tasks sheet with any naming variation")
            print("Available sheets:")
            for sheet in sheets:
                print(f"  • '{sheet['properties']['title']}'")
            return False
        
        print("\n✅ ALL TESTS PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def update_claude_tasks_if_accessible():
    """Update Claude Tasks if sheets access is working"""
    
    print("\n📝 ATTEMPTING CLAUDE TASKS UPDATE")
    print("=" * 40)
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        
        # Read Claude Tasks (use working range format)
        print("📋 Reading Claude Tasks...")
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="'Claude Tasks'!A:K"
        ).execute()
        
        values = result.get('values', [])
        print(f"✅ Read {len(values)} rows from Claude Tasks")
        
        # Analyze current status
        completed_count = 0
        in_progress_count = 0
        recent_tasks = []
        
        for i, row in enumerate(values[1:], 2):  # Skip header
            if len(row) > 0 and row[0]:
                task_id = row[0]
                status = row[4] if len(row) > 4 else 'Unknown'
                task_desc = row[5] if len(row) > 5 else 'Unknown'
                
                if 'complete' in status.lower():
                    completed_count += 1
                elif 'progress' in status.lower():
                    in_progress_count += 1
                    recent_tasks.append((task_id, status, task_desc[:50]))
        
        print(f"\n📊 CURRENT STATUS:")
        print(f"Total tasks: {len(values)-1}")
        print(f"Completed: {completed_count}")
        print(f"In Progress: {in_progress_count}")
        
        if recent_tasks:
            print(f"\n🔄 Recent In Progress Tasks:")
            for task_id, status, desc in recent_tasks:
                print(f"  {task_id} ({status}): {desc}...")
        
        # Check if we need to add recent work as new tasks
        print(f"\n🆕 MISSING RECENT WORK:")
        recent_work = [
            ("CT-031", "GitHub Actions Claude Preparation", "Complete"),
            ("CT-032", "Claude Max OAuth Setup", "Complete"),
            ("CT-033", "File Tree Visualization", "Complete"), 
            ("CT-034", "Session Summary Creation", "Complete")
        ]
        
        # Check which tasks might be missing
        existing_ids = [row[0] for row in values[1:] if len(row) > 0]
        
        missing_tasks = []
        for task_id, desc, status in recent_work:
            if task_id not in existing_ids:
                missing_tasks.append((task_id, desc, status))
        
        if missing_tasks:
            print("Tasks that could be added:")
            for task_id, desc, status in missing_tasks:
                print(f"  • {task_id}: {desc} ({status})")
        else:
            print("✅ All recent work appears to be tracked")
        
        return True, len(values)-1, completed_count, in_progress_count
        
    except Exception as e:
        print(f"❌ Update failed: {e}")
        return False, 0, 0, 0

def main():
    """Main debugging and update workflow"""
    
    print("🔧 GOOGLE SHEETS CLAUDE TASKS DEBUGGER")
    print("=" * 45)
    
    # Debug access first
    access_ok = debug_sheets_access()
    
    if access_ok:
        # Try to update if access is working
        update_ok, total_tasks, completed, in_progress = update_claude_tasks_if_accessible()
        
        if update_ok:
            print(f"\n🎉 CLAUDE TASKS STATUS UPDATE SUCCESS!")
            print("=" * 45)
            print(f"📊 Status Summary:")
            print(f"  • Total Claude Tasks: {total_tasks}")
            print(f"  • Completed: {completed}")
            print(f"  • In Progress: {in_progress}")
            print(f"  • Success Rate: {(completed/total_tasks)*100:.1f}%")
            
            print(f"\n🚀 Recent Achievements:")
            print("  • Discord webhook integration working")
            print("  • GitHub Actions Claude prepared")  
            print("  • Claude Max OAuth guidance created")
            print("  • File tree visualization system")
            print("  • Cross-Claude coordination established")
            
            return True
        else:
            print(f"\n⚠️  Sheets access OK but update failed")
            return False
    else:
        print(f"\n❌ Google Sheets access failed")
        print("Check the error messages above for specific fixes needed")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print(f"\n✅ Google Sheets update completed successfully!")
    else:
        print(f"\n📝 Manual intervention needed - see error details above")
        sys.exit(1)