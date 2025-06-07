#!/usr/bin/env python3
"""
Get detailed information about Claude Tasks CT-013 and CT-021
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
    sys.exit(1)

def get_task_details():
    """Get detailed information about CT-013 and CT-021"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔍 Investigating CT-013 and CT-021 Details")
    print("=" * 45)
    
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
        
        print(f"📊 Analyzing {len(values)} rows in Claude Tasks")
        print("")
        
        # Get headers
        headers = values[0] if values else []
        print(f"📋 Sheet Headers: {headers}")
        print("")
        
        # Look for CT-013 and CT-021
        ct_013_found = False
        ct_021_found = False
        
        for i, row in enumerate(values[1:], 2):  # Start from row 2 (skip headers)
            if len(row) > 0:
                task_id = row[0] if len(row) > 0 else ""
                
                if "CT-013" in task_id:
                    ct_013_found = True
                    print(f"🎯 CT-013 Found at Row {i}:")
                    print("=" * 30)
                    for j, cell in enumerate(row):
                        header = headers[j] if j < len(headers) else f"Column {j+1}"
                        print(f"  {header}: {cell}")
                    print("")
                
                elif "CT-021" in task_id:
                    ct_021_found = True
                    print(f"🎯 CT-021 Found at Row {i}:")
                    print("=" * 30)
                    for j, cell in enumerate(row):
                        header = headers[j] if j < len(headers) else f"Column {j+1}"
                        print(f"  {header}: {cell}")
                    print("")
        
        # Summary
        print("📊 Task Discovery Summary:")
        print("=" * 30)
        print(f"CT-013: {'✅ Found' if ct_013_found else '❌ Not Found'}")
        print(f"CT-021: {'✅ Found' if ct_021_found else '❌ Not Found'}")
        
        if not ct_013_found:
            print("\n⚠️  CT-013 not found - may need to search other sheets or create")
        
        if not ct_021_found:
            print("\n⚠️  CT-021 not found - may need to search other sheets or create")
        
        # Check for similar task IDs
        print("\n🔍 Nearby Task IDs Found:")
        for i, row in enumerate(values[1:], 2):
            if len(row) > 0:
                task_id = row[0] if len(row) > 0 else ""
                if "CT-01" in task_id or "CT-02" in task_id:
                    task_name = row[1] if len(row) > 1 else "No name"
                    status = row[2] if len(row) > 2 else "No status"
                    assignee = row[3] if len(row) > 3 else "No assignee"
                    print(f"  {task_id}: {task_name} (Status: {status}, Assignee: {assignee})")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = get_task_details()
    if not success:
        sys.exit(1)