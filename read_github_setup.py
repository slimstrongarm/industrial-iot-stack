#!/usr/bin/env python3
"""Read the GitHub Claude Action Setup sheet"""

import sys
sys.path.append('/home/server')
from google_sheets_helper import GoogleSheetsHelper

def main():
    helper = GoogleSheetsHelper()
    
    # First, let's verify the sheet exists
    sheets = helper.get_sheet_info()
    target_sheet = None
    
    for sheet in sheets:
        if "GitHub Claude Action Setup" in sheet['title']:
            target_sheet = sheet['title']
            print(f"Found target sheet: '{target_sheet}'")
            break
    
    if not target_sheet:
        print("Could not find 'GitHub Claude Action Setup' sheet")
        return
    
    # Try different range formats
    range_formats = [
        f"'{target_sheet}'!A:Z",
        f"{target_sheet}!A:Z", 
        f"'{target_sheet}'!A1:Z100",
        f"{target_sheet}!A1:Z100"
    ]
    
    for range_format in range_formats:
        print(f"\nTrying range format: {range_format}")
        try:
            # Use the service directly to avoid double escaping
            result = helper.sheet.values().get(
                spreadsheetId=helper.sheet._SPREADSHEET_ID if hasattr(helper.sheet, '_SPREADSHEET_ID') else '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do',
                range=range_format
            ).execute()
            
            values = result.get('values', [])
            if values:
                print(f"SUCCESS! Found {len(values)} rows")
                print("Sheet contents:")
                print("=" * 60)
                for i, row in enumerate(values, 1):
                    if row:
                        print(f"Row {i:2d}: {row}")
                    elif i <= 20:
                        print(f"Row {i:2d}: [empty]")
                break
        except Exception as e:
            print(f"Failed: {str(e)}")
            continue
    else:
        print("All range formats failed")

if __name__ == "__main__":
    main()