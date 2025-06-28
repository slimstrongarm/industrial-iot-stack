#!/usr/bin/env python3
import sys
sys.path.append('/home/server')
from google_sheets_helper import GoogleSheetsHelper

helper = GoogleSheetsHelper()

print("🔍 Reading Claude Approvals sheet...")

# Try the simple format that worked before
try:
    data = helper.read_range("Claude Approvals!A:H")
    
    if data:
        print(f"✅ Found {len(data)} rows in Claude Approvals")
        print("\n📋 Claude Approvals Content:")
        print("=" * 100)
        
        for i, row in enumerate(data):
            if i == 0 and row:  # Header
                print(f"Headers: {' | '.join(row)}")
                print("=" * 100)
            elif row and len(row) > 1:  # Data rows with content
                # Pad row to ensure we have enough columns
                padded_row = row + [''] * (8 - len(row))
                print(f"Row {i+1}: {padded_row[0][:20]}... | {padded_row[1][:30]}... | {padded_row[2][:15]} | {padded_row[3][:10]}")
    else:
        print("⚠️  Claude Approvals sheet appears to be empty")
        
        # Let's check what sheets are really available
        print("\n📊 Available sheets:")
        sheet_info = helper.get_sheet_info()
        for sheet in sheet_info:
            title = sheet.get('title', 'Unknown')
            sheet_id = sheet.get('sheetId', 'Unknown')
            print(f"  - {title} (ID: {sheet_id})")
            
except Exception as e:
    print(f"❌ Error reading Claude Approvals: {e}")
    
    # Fallback: try to find any sheet with "claude" or "task" in the name
    print("\n🔍 Looking for alternative Claude/Task sheets...")
    try:
        sheet_info = helper.get_sheet_info()
        for sheet in sheet_info:
            title = sheet.get('title', '').lower()
            if 'claude' in title or 'task' in title:
                print(f"Found potential sheet: {sheet.get('title')}")
    except Exception as e2:
        print(f"❌ Error getting sheet info: {e2}")