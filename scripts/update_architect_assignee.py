#!/usr/bin/env python3
"""
Update Human Tasks (Clean) tab to change "You" to "Architect" 
"""

import json
import sys
import os
from pathlib import Path

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

def update_architect_assignee():
    """Update Human Tasks (Clean) tab to use Architect instead of You"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🏗️  Updating Human Tasks (Clean) - Architect Role")
    print("=" * 45)
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        
        print("✅ Connected to Google Sheets API")
        
        # Read current Human Tasks (Clean) sheet
        sheet_name = "Human Tasks (Clean)"
        range_name = f"'{sheet_name}'!A:H"
        
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("❌ No data found in Human Tasks (Clean) sheet")
            return False
        
        print(f"📊 Found {len(values)} rows in {sheet_name}")
        
        # Update the data - change "You" to "Architect"
        updated_values = []
        changes_made = 0
        
        for i, row in enumerate(values):
            updated_row = row.copy()
            
            # Skip header row
            if i == 0:
                updated_values.append(updated_row)
                continue
            
            # Check Assigned To column (index 5)
            if len(updated_row) > 5 and updated_row[5] == "You":
                updated_row[5] = "Architect"
                changes_made += 1
                print(f"  Row {i+1}: Updated assignee to Architect")
            
            # Ensure row has 8 columns
            while len(updated_row) < 8:
                updated_row.append("")
            
            updated_values.append(updated_row)
        
        print(f"\n🔧 Made {changes_made} assignee updates")
        
        # Update the sheet
        body = {
            'values': updated_values
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=f"'{sheet_name}'!A1",
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Updated Human Tasks (Clean) sheet")
        print(f"📊 {result.get('updatedCells')} cells updated")
        
        # Show role summary
        print(f"\n📋 Role Assignment Summary:")
        role_counts = {"Architect": 0, "Controls Engineer": 0, "Both": 0}
        
        for row in updated_values[1:]:  # Skip header
            if len(row) > 5:
                assignee = row[5]
                if assignee in role_counts:
                    role_counts[assignee] += 1
        
        for role, count in role_counts.items():
            print(f"  {role}: {count} tasks")
        
        print(f"\n🏗️  Architect Tasks (You):")
        for i, row in enumerate(updated_values[1:], 1):
            if len(row) > 5 and row[5] == "Architect":
                task_id = row[0] if len(row) > 0 else f"HT-{i:03d}"
                task_name = row[1] if len(row) > 1 else "Unknown"
                priority = row[2] if len(row) > 2 else "Medium"
                print(f"  • {task_id}: {task_name} ({priority} priority)")
        
        print(f"\n🔧 Controls Engineer Tasks:")
        for i, row in enumerate(updated_values[1:], 1):
            if len(row) > 5 and row[5] == "Controls Engineer":
                task_id = row[0] if len(row) > 0 else f"HT-{i:03d}"
                task_name = row[1] if len(row) > 1 else "Unknown"
                priority = row[2] if len(row) > 2 else "Medium"
                print(f"  • {task_id}: {task_name} ({priority} priority)")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = update_architect_assignee()
    if success:
        print("\n🎉 Role assignments updated!")
        print("You are now properly assigned as 'Architect' for your tasks.")
        print("The Controls Engineer has their specific tasks assigned.")
    else:
        print("\n📝 Failed to update role assignments")
        sys.exit(1)