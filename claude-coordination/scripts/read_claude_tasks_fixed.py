#!/usr/bin/env python3
import sys
sys.path.append('/home/server')
from google_sheets_helper import GoogleSheetsHelper

helper = GoogleSheetsHelper()

print("🔍 Reading Claude Tasks sheet with different approaches...")

# Try multiple range formats
range_formats = [
    "Claude Tasks!A1:J20",
    "'Claude Tasks'!A1:J20",
    "Claude Tasks!A:J",
    "'Claude Tasks'!A:J"
]

for range_format in range_formats:
    try:
        print(f"\n🔄 Trying format: {range_format}")
        data = helper.read_range(range_format)
        
        if data:
            print(f"✅ Success! Found {len(data)} rows")
            
            # Show the data structure
            print("\n📋 Claude Tasks Content:")
            print("=" * 100)
            
            for i, row in enumerate(data):
                if i == 0 and row:  # Header row
                    print(f"Headers: {' | '.join(str(cell) for cell in row)}")
                    print("=" * 100)
                elif row and any(cell for cell in row):  # Non-empty data row
                    # Safely access columns
                    task_id = str(row[0]) if len(row) > 0 else ''
                    task_desc = str(row[1]) if len(row) > 1 else ''
                    status = str(row[2]) if len(row) > 2 else ''
                    priority = str(row[3]) if len(row) > 3 else ''
                    assigned_to = str(row[4]) if len(row) > 4 else ''
                    
                    print(f"Row {i+1}:")
                    print(f"  ID: {task_id}")
                    print(f"  Task: {task_desc[:60]}...")
                    print(f"  Status: {status}")
                    print(f"  Priority: {priority}")
                    print(f"  Assigned: {assigned_to}")
                    print("-" * 50)
                    
                    # Check if assigned to server-claude
                    if 'server-claude' in assigned_to.lower() or 'server claude' in assigned_to.lower():
                        print(f"🎯 TASK FOR SERVER-CLAUDE: {task_desc}")
            
            break  # Found working format, stop trying others
            
    except Exception as e:
        print(f"❌ Failed with {range_format}: {str(e)[:100]}...")
        continue

else:
    print("\n❌ Could not read Claude Tasks with any format")
    print("The sheet might be empty or have different structure")
    
    # Try to access by sheet ID directly
    try:
        print("\n🔄 Trying direct sheet access...")
        # This is a fallback approach
        data = helper.read_range("A1:J20")
        if data:
            print("✅ Found some data with direct approach")
    except Exception as e:
        print(f"❌ Direct approach also failed: {e}")

print("\n📊 Available sheets for reference:")
sheet_info = helper.get_sheet_info()
for sheet in sheet_info:
    print(f"  - {sheet.get('title')} (ID: {sheet.get('sheetId')})")