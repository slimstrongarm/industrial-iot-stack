#!/usr/bin/env python3
"""
Read the actual structure of the Claude Tasks sheet to understand column layout
"""

import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path

def read_sheet_structure():
    """Read the actual column structure of Claude Tasks sheet"""
    
    try:
        # Load credentials
        creds_path = Path(__file__).parent.parent / "credentials" / "iot-stack-credentials.json"
        
        # Setup Google Sheets client
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open the IoT Stack Progress Master spreadsheet
        spreadsheet = client.open("IoT Stack Progress Master")
        claude_tasks_sheet = spreadsheet.worksheet("Claude Tasks")
        
        print("✅ Connected to Claude Tasks sheet")
        
        # Get the header row to understand column structure
        headers = claude_tasks_sheet.row_values(1)
        
        print(f"\n📋 Claude Tasks Sheet Column Structure:")
        print("=" * 60)
        for i, header in enumerate(headers, start=1):
            column_letter = chr(64 + i)  # Convert to A, B, C, etc.
            print(f"Column {column_letter:2s} ({i:2d}): {header}")
        
        print(f"\n📊 Total columns: {len(headers)}")
        
        # Get a few sample rows to understand the data format
        print(f"\n📋 Sample Data (first 3 rows):")
        print("=" * 60)
        
        for row_num in range(2, 5):  # Rows 2-4
            try:
                row_data = claude_tasks_sheet.row_values(row_num)
                if row_data:
                    print(f"\nRow {row_num}:")
                    for i, value in enumerate(row_data, start=1):
                        if value.strip():  # Only show non-empty values
                            column_letter = chr(64 + i)
                            header_name = headers[i-1] if i-1 < len(headers) else f"Column{i}"
                            print(f"  {column_letter} ({header_name}): {value[:50]}{'...' if len(value) > 50 else ''}")
            except Exception as e:
                print(f"  Row {row_num}: Error reading - {e}")
        
        # Check one of the ADK rows specifically (row 66)
        print(f"\n🔍 ADK Row 66 Current State:")
        print("=" * 60)
        try:
            row_66_data = claude_tasks_sheet.row_values(66)
            if row_66_data:
                for i, value in enumerate(row_66_data, start=1):
                    if value.strip():
                        column_letter = chr(64 + i)
                        header_name = headers[i-1] if i-1 < len(headers) else f"Column{i}"
                        print(f"  {column_letter} ({header_name}): {value}")
            else:
                print("  Row 66: No data found")
        except Exception as e:
            print(f"  Row 66: Error reading - {e}")
        
        return headers
        
    except Exception as e:
        print(f"❌ Error reading sheet structure: {e}")
        return None

def main():
    """Main function"""
    print("📊 Claude Tasks Sheet Structure Analysis")
    print("=" * 50)
    
    headers = read_sheet_structure()
    
    if headers:
        print(f"\n✅ Successfully read sheet structure with {len(headers)} columns")
        print("📋 Use this information to correctly map data updates")
    else:
        print("\n❌ Failed to read sheet structure")

if __name__ == "__main__":
    main()