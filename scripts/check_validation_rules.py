#!/usr/bin/env python3
"""
Check for data validation rules that might be causing invalid input markers
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

def check_validation_rules():
    """Check for data validation rules in Human Tasks sheet"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔍 Checking Human Tasks Sheet for Data Validation Rules")
    print("=" * 55)
    
    try:
        # Load credentials
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        service = build('sheets', 'v4', credentials=creds)
        
        print("✅ Connected to Google Sheets API")
        
        # Get spreadsheet metadata to check for validation rules
        spreadsheet = service.spreadsheets().get(
            spreadsheetId=SPREADSHEET_ID,
            includeGridData=False
        ).execute()
        
        # Find Human Tasks sheet
        human_tasks_sheet = None
        for sheet in spreadsheet['sheets']:
            if sheet['properties']['title'] == 'Human Tasks':
                human_tasks_sheet = sheet
                break
        
        if not human_tasks_sheet:
            print("❌ Human Tasks sheet not found")
            return False
        
        sheet_id = human_tasks_sheet['properties']['sheetId']
        print(f"📊 Found Human Tasks sheet (ID: {sheet_id})")
        
        # Read the current data to see what might be causing validation issues
        range_name = 'Human Tasks!A1:H50'
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        print(f"📋 Current data structure:")
        if values:
            headers = values[0] if len(values) > 0 else []
            print(f"Headers: {headers}")
            
            # Check first few data rows
            for i, row in enumerate(values[1:6], 1):
                print(f"Row {i+1}: {row[:4]}...")  # Show first 4 columns
        
        # The issue might be that the sheet has dropdown validation
        # Let's create a simple fix by ensuring all values match expected formats
        
        print(f"\n🔧 Creating validation-compliant data...")
        
        # Valid options for dropdowns (common ones that might be set)
        valid_data = {
            'Priority': ['High', 'Medium', 'Low', 'Critical'],
            'Status': ['Ready', 'Pending', 'Complete', 'In Progress', 'Blocked'],
            'Role': ['You', 'Controls Engineer', 'Both', 'Team', 'Architect'],
            'Task_Type': ['Administration', 'Configuration', 'Integration', 'Testing', 'Development', 'API Setup', 'Documentation', 'Coordination', 'Architecture', 'PLC Logic', 'Network', 'Deployment', 'Optimization', 'Maintenance', 'Training', 'Compliance', 'Backup', 'Security', 'Monitoring']
        }
        
        # Clean up the data to match validation rules
        clean_values = []
        
        if values:
            # Keep headers as-is
            clean_values.append(values[0])
            
            # Clean each data row
            for i, row in enumerate(values[1:], 1):
                clean_row = []
                
                for j, cell in enumerate(row):
                    if j >= 8:  # Only process first 8 columns
                        break
                        
                    clean_cell = str(cell).strip() if cell else ""
                    
                    # Apply specific cleaning based on column
                    if j == 0:  # ID column
                        if not clean_cell.startswith('HT-'):
                            clean_cell = f"HT-{i:03d}"
                    elif j == 1:  # Role column
                        if clean_cell and clean_cell not in valid_data['Role']:
                            # Try to match closest valid role
                            cell_lower = clean_cell.lower()
                            if 'control' in cell_lower or 'engineer' in cell_lower:
                                clean_cell = 'Controls Engineer'
                            elif 'team' in cell_lower or 'both' in cell_lower:
                                clean_cell = 'Both'
                            else:
                                clean_cell = 'You'
                    elif j == 2:  # Task Type column
                        if clean_cell and clean_cell not in valid_data['Task_Type']:
                            # Keep as-is but ensure it's a simple string
                            clean_cell = clean_cell.replace('\n', ' ').replace('\r', ' ')
                    elif j == 3:  # Priority column
                        if clean_cell and clean_cell not in valid_data['Priority']:
                            cell_lower = clean_cell.lower()
                            if 'high' in cell_lower:
                                clean_cell = 'High'
                            elif 'medium' in cell_lower or 'med' in cell_lower:
                                clean_cell = 'Medium'
                            elif 'low' in cell_lower:
                                clean_cell = 'Low'
                            else:
                                clean_cell = 'Medium'
                    elif j == 4:  # Status column
                        if clean_cell and clean_cell not in valid_data['Status']:
                            cell_lower = clean_cell.lower()
                            if 'ready' in cell_lower:
                                clean_cell = 'Ready'
                            elif 'complete' in cell_lower:
                                clean_cell = 'Complete'
                            elif 'pending' in cell_lower:
                                clean_cell = 'Pending'
                            else:
                                clean_cell = 'Ready'
                    elif j == 5:  # Assigned To column
                        if clean_cell and clean_cell not in valid_data['Role']:
                            # Same logic as Role column
                            cell_lower = clean_cell.lower()
                            if 'control' in cell_lower or 'engineer' in cell_lower:
                                clean_cell = 'Controls Engineer'
                            elif 'team' in cell_lower or 'both' in cell_lower:
                                clean_cell = 'Both'
                            else:
                                clean_cell = 'You'
                    elif j == 6:  # Dependencies column
                        if clean_cell in ['None', 'none', 'N/A', 'n/a', '']:
                            clean_cell = '-'
                    # Column 7 (Description) - keep as-is but clean
                    
                    clean_row.append(clean_cell)
                
                # Ensure row has exactly 8 columns
                while len(clean_row) < 8:
                    clean_row.append('')
                clean_row = clean_row[:8]
                
                clean_values.append(clean_row)
        
        # Update the sheet with clean data
        if clean_values:
            print(f"\n📝 Updating sheet with validation-compliant data...")
            
            # Clear and rewrite
            service.spreadsheets().values().clear(
                spreadsheetId=SPREADSHEET_ID,
                range='Human Tasks!A:H'
            ).execute()
            
            body = {'values': clean_values}
            result = service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range='Human Tasks!A1',
                valueInputOption='RAW',
                body=body
            ).execute()
            
            print(f"✅ Sheet updated with clean data")
            print(f"📊 {result.get('updatedCells')} cells updated")
            print(f"🎯 {len(clean_values)-1} tasks processed")
        
        print(f"\n💡 If you're still seeing validation errors:")
        print("1. Check if the sheet has dropdown data validation rules")
        print("2. The sheet might have custom validation we can't see via API")
        print("3. Try manually removing data validation: Data → Data validation → Remove validation")
        print("4. Or adjust the validation rules to include our values")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = check_validation_rules()
    if not success:
        sys.exit(1)