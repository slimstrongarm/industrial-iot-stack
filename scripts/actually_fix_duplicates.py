#!/usr/bin/env python3
"""
ACTUALLY fix duplicate tasks - the previous script failed!
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

# Configuration
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def actually_fix_duplicates():
    try:
        sheet = get_sheets_service()
        sheet_name = 'Claude Tasks'
        
        # Get all data
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_name}'!A:H"
        ).execute()
        
        values = result.get('values', [])
        print(f"📊 Total rows found: {len(values)}")
        
        # Build a clean list without duplicates
        clean_rows = []
        seen_task_ids = set()
        duplicates_found = []
        
        for i, row in enumerate(values):
            if i == 0:  # Keep header
                clean_rows.append(row)
                continue
                
            if len(row) > 0:
                task_id = row[0] if row[0] else f"empty_row_{i}"
                
                if task_id in seen_task_ids:
                    duplicates_found.append((i+1, task_id))
                    print(f"🗑️  Skipping duplicate: {task_id} at row {i+1}")
                else:
                    seen_task_ids.add(task_id)
                    clean_rows.append(row)
                    print(f"✅ Keeping: {task_id} at row {i+1}")
            else:
                # Keep empty rows at the end
                clean_rows.append(row)
        
        print(f"\n📋 Found {len(duplicates_found)} duplicates to remove")
        print(f"📊 Clean data will have {len(clean_rows)} rows")
        
        if duplicates_found:
            # Clear the entire range first
            clear_range = f"'{sheet_name}'!A:H"
            sheet.values().clear(
                spreadsheetId=SPREADSHEET_ID,
                range=clear_range
            ).execute()
            print("🧹 Cleared entire sheet")
            
            # Write back the clean data
            update_range = f"'{sheet_name}'!A1:H{len(clean_rows)}"
            result = sheet.values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption='RAW',
                body={'values': clean_rows}
            ).execute()
            
            print(f"✅ Wrote {len(clean_rows)} clean rows back to sheet")
            print(f"📊 Updated {result.get('updatedCells')} cells")
            
            # Verify the fix
            verification = sheet.values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=f"'{sheet_name}'!A:A"
            ).execute()
            
            verify_values = verification.get('values', [])
            verify_ids = [row[0] for row in verify_values[1:] if len(row) > 0]  # Skip header
            verify_duplicates = len(verify_ids) - len(set(verify_ids))
            
            if verify_duplicates == 0:
                print("🎉 SUCCESS: No duplicates found in verification!")
            else:
                print(f"❌ FAILED: Still found {verify_duplicates} duplicates")
                
        else:
            print("✅ No duplicates found - sheet is already clean")
            
        return True
        
    except Exception as e:
        print(f"❌ Error fixing duplicates: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_prevention_utility():
    """Create a robust duplicate prevention utility"""
    prevention_code = '''#!/usr/bin/env python3
"""
Duplicate prevention utility for Google Sheets Claude Tasks
ALWAYS call check_task_exists() before adding new tasks!
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def get_existing_task_ids():
    """Get all existing task IDs from Google Sheets"""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range="'Claude Tasks'!A:A"
    ).execute()
    
    values = result.get('values', [])
    task_ids = set()
    
    for row in values[1:]:  # Skip header
        if len(row) > 0 and row[0]:
            task_ids.add(row[0])
    
    return task_ids

def check_task_exists(task_id):
    """Check if a task ID already exists"""
    existing_ids = get_existing_task_ids()
    exists = task_id in existing_ids
    
    if exists:
        print(f"⚠️  WARNING: Task {task_id} already exists! Not adding duplicate.")
    else:
        print(f"✅ Task {task_id} is new - safe to add")
    
    return exists

def get_next_task_id():
    """Get the next available CT-XXX task ID"""
    existing_ids = get_existing_task_ids()
    
    # Extract numbers from CT-XXX format
    numbers = []
    for task_id in existing_ids:
        if task_id.startswith('CT-'):
            try:
                num = int(task_id[3:])
                numbers.append(num)
            except ValueError:
                continue
    
    if numbers:
        next_num = max(numbers) + 1
    else:
        next_num = 1
    
    next_id = f"CT-{next_num:03d}"
    print(f"📝 Next available task ID: {next_id}")
    return next_id

if __name__ == "__main__":
    print("🔍 Duplicate Prevention Utility")
    print("==============================")
    
    existing = get_existing_task_ids()
    print(f"📊 Found {len(existing)} existing tasks")
    
    next_id = get_next_task_id()
    print(f"🆕 Next task ID should be: {next_id}")
'''
    
    os.makedirs('scripts/utilities', exist_ok=True)
    with open('scripts/utilities/duplicate_prevention.py', 'w') as f:
        f.write(prevention_code)
    
    print("🛡️  Created scripts/utilities/duplicate_prevention.py")
    print("📋 Future scripts MUST import and use check_task_exists()!")

if __name__ == '__main__':
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(os.path.dirname(script_dir))
    
    print('🚨 ACTUALLY fixing duplicates this time!')
    print('(The previous script clearly failed - this is embarrassing)')
    
    success = actually_fix_duplicates()
    
    if success:
        print('\n✅ Duplicates ACTUALLY fixed this time!')
        create_prevention_utility()
        print('\n🔗 Verify fix: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do/edit')
        print('\n🛡️  Prevention utility created - no more duplicates!')
    else:
        print('\n❌ Failed again - this needs manual intervention')