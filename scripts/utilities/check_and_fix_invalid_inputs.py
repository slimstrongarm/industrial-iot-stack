#!/usr/bin/env python3
"""
Check Human Tasks sheet for invalid inputs and fix them
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

def check_and_fix_invalid_inputs():
    """Check Human Tasks sheet for invalid inputs and fix them"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔍 Checking Human Tasks Sheet for Invalid Inputs")
    print("=" * 50)
    
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
        
        # Read current Human Tasks sheet
        range_name = 'Human Tasks!A:Z'
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print("❌ No data found in Human Tasks sheet")
            return False
        
        print(f"📊 Found {len(values)} rows in Human Tasks sheet")
        
        # Analyze the data for issues
        print(f"\n🔍 Analyzing data structure...")
        
        issues_found = []
        clean_data = []
        
        for i, row in enumerate(values):
            row_num = i + 1
            
            # Check for empty rows
            if not row or all(cell == "" for cell in row):
                issues_found.append(f"Row {row_num}: Empty row")
                continue
            
            # Check for rows that are too short or too long
            if len(row) < 3:
                issues_found.append(f"Row {row_num}: Too few columns ({len(row)})")
                # Pad with empty strings
                while len(row) < 8:
                    row.append("")
            
            # Clean up any problematic characters or formatting
            cleaned_row = []
            for j, cell in enumerate(row):
                if cell is None:
                    cleaned_cell = ""
                else:
                    # Convert to string and clean
                    cleaned_cell = str(cell).strip()
                    
                    # Remove any problematic characters that might cause validation issues
                    cleaned_cell = cleaned_cell.replace('\n', ' ').replace('\r', ' ')
                    
                    # Fix common issues
                    if cleaned_cell.startswith('='):  # Remove formulas that might be invalid
                        cleaned_cell = cleaned_cell.replace('=', '')
                    
                cleaned_row.append(cleaned_cell)
            
            # Ensure row has exactly 8 columns (ID, Role, Task Type, Priority, Status, Assigned To, Dependencies, Description)
            while len(cleaned_row) < 8:
                cleaned_row.append("")
            
            # Trim to 8 columns if longer
            cleaned_row = cleaned_row[:8]
            
            clean_data.append(cleaned_row)
        
        print(f"🔧 Issues found: {len(issues_found)}")
        for issue in issues_found:
            print(f"  • {issue}")
        
        # Create properly formatted data
        print(f"\n📝 Creating clean data structure...")
        
        # Ensure we have a proper header row
        if clean_data and len(clean_data) > 0:
            first_row = clean_data[0]
            if not (first_row[0] == "ID" or "ID" in first_row[0]):
                # Need to add proper headers
                headers = ["ID", "Role", "Task Type", "Priority", "Status", "Assigned To", "Dependencies", "Description"]
                clean_data.insert(0, headers)
        else:
            # Start with headers
            headers = ["ID", "Role", "Task Type", "Priority", "Status", "Assigned To", "Dependencies", "Description"]
            clean_data = [headers]
        
        # Validate and fix data values
        valid_priorities = ["High", "Medium", "Low", "Critical"]
        valid_statuses = ["Ready", "Pending", "Complete", "In Progress", "Blocked"]
        valid_roles = ["You", "Controls Engineer", "Both", "Team", "Architect", "Mac Claude", "Server Claude"]
        
        for i, row in enumerate(clean_data[1:], 1):  # Skip header row
            # Fix ID format
            if not row[0].startswith("HT-"):
                row[0] = f"HT-{i:03d}"
            
            # Validate Role
            if row[1] not in valid_roles and row[1] != "":
                # Try to map common variations
                role_lower = row[1].lower()
                if "control" in role_lower or "engineer" in role_lower:
                    row[1] = "Controls Engineer"
                elif "architect" in role_lower:
                    row[1] = "Architect"
                elif "team" in role_lower or "both" in role_lower:
                    row[1] = "Both"
                elif "claude" in role_lower:
                    if "mac" in role_lower:
                        row[1] = "Mac Claude"
                    else:
                        row[1] = "Server Claude"
                else:
                    row[1] = "You"  # Default
            
            # Validate Priority
            if row[3] not in valid_priorities and row[3] != "":
                priority_lower = row[3].lower()
                if "high" in priority_lower or "critical" in priority_lower:
                    row[3] = "High"
                elif "medium" in priority_lower or "med" in priority_lower:
                    row[3] = "Medium"
                elif "low" in priority_lower:
                    row[3] = "Low"
                else:
                    row[3] = "Medium"  # Default
            
            # Validate Status
            if row[4] not in valid_statuses and row[4] != "":
                status_lower = row[4].lower()
                if "ready" in status_lower:
                    row[4] = "Ready"
                elif "complete" in status_lower or "done" in status_lower:
                    row[4] = "Complete"
                elif "pending" in status_lower or "wait" in status_lower:
                    row[4] = "Pending"
                elif "progress" in status_lower or "working" in status_lower:
                    row[4] = "In Progress"
                elif "block" in status_lower:
                    row[4] = "Blocked"
                else:
                    row[4] = "Ready"  # Default
            
            # Clean up Dependencies
            if row[6] in ["None", "none", "N/A", "n/a", ""]:
                row[6] = "-"
        
        # Clear and update the sheet with clean data
        print(f"\n📝 Updating sheet with {len(clean_data)-1} clean tasks...")
        
        # Clear existing content
        clear_range = 'Human Tasks!A:Z'
        sheet.values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=clear_range
        ).execute()
        
        # Write clean data
        body = {
            'values': clean_data
        }
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Human Tasks!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Human Tasks sheet cleaned and updated!")
        print(f"📊 {result.get('updatedCells')} cells updated")
        print(f"🎯 {len(clean_data)-1} tasks with valid formatting")
        
        # Show final format
        print(f"\n📋 Clean Format Applied:")
        print("Columns: ID | Role | Task Type | Priority | Status | Assigned To | Dependencies | Description")
        print(f"Valid Priorities: {', '.join(valid_priorities)}")
        print(f"Valid Statuses: {', '.join(valid_statuses)}")
        print(f"Valid Roles: {', '.join(valid_roles)}")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = check_and_fix_invalid_inputs()
    if success:
        print("\n🎉 Invalid inputs fixed!")
        print("Human Tasks sheet should now be clean with valid data.")
    else:
        print("\n📝 Please manually check and fix invalid inputs")
        sys.exit(1)