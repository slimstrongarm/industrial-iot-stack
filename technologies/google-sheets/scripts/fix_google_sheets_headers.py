#!/usr/bin/env python3
"""
Fix Google Sheets Header Issue
The worksheet has duplicate empty headers - let's fix this
"""

import gspread
from google.oauth2.service_account import Credentials

def fix_headers():
    """Fix the Google Sheets header row"""
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
        
        # Get the first row (headers)
        headers = worksheet.row_values(1)
        print(f"Current headers: {headers}")
        print(f"Number of headers: {len(headers)}")
        
        # Find empty headers
        empty_positions = []
        for i, header in enumerate(headers):
            if not header or header.strip() == '':
                empty_positions.append(i + 1)  # 1-indexed for sheets
        
        print(f"Empty header positions: {empty_positions}")
        
        # Try to get records with expected headers to avoid the duplicate issue
        expected_headers = ['ID', 'Assigned To', 'Task Description', 'Priority', 'Status', 'Notes', 'Created Date', 'Due Date']
        
        # Use raw values instead of get_all_records to avoid header issues
        all_values = worksheet.get_all_values()
        print(f"✅ Successfully retrieved {len(all_values)} rows of data")
        
        if all_values:
            print(f"Header row: {all_values[0]}")
            print(f"Data rows: {len(all_values) - 1}")
            
            # Show a few recent tasks
            print("\n📋 Recent tasks:")
            for i, row in enumerate(all_values[-4:], len(all_values) - 3):
                if len(row) > 0:
                    task_id = row[0] if len(row) > 0 else 'No ID'
                    status = row[4] if len(row) > 4 else 'No Status'  
                    description = row[2] if len(row) > 2 else 'No Description'
                    print(f"   Row {i}: {task_id} - {status} - {description[:50]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_access():
    """Test simple access without get_all_records"""
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
        
        # Use get_all_values instead of get_all_records
        all_values = worksheet.get_all_values()
        next_id = f"CT-{len(all_values):03d}"  # Includes header row
        
        print("✅ Simple access successful")
        print(f"📊 Total rows (including header): {len(all_values)}")
        print(f"🆔 Next task ID: {next_id}")
        
        # Look for CT-099
        for i, row in enumerate(all_values):
            if len(row) > 0 and row[0] == 'CT-099':
                status = row[4] if len(row) > 4 else 'Unknown'
                assigned = row[1] if len(row) > 1 else 'Unassigned'
                print(f"🎯 Found CT-099: Status={status}, Assigned={assigned}")
                break
        
        return True
        
    except Exception as e:
        print(f"❌ Simple access error: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Google Sheets Header Fix")
    print("=" * 50)
    
    print("1. Analyzing headers...")
    fix_headers()
    
    print("\n2. Testing simple access...")
    test_simple_access()
    
    print("=" * 50)
    print("✅ Analysis complete!")