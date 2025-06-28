#!/usr/bin/env python3
"""Test Google Sheets connection to debug the 'Connection reset by peer' error"""

import gspread
from google.oauth2.service_account import Credentials
import socket

print("🔍 Testing Google Sheets Connection")
print("=" * 50)

# Test basic connectivity
print("1. Testing internet connectivity...")
try:
    socket.create_connection(("google.com", 80), 2)
    print("✅ Internet connection working")
except:
    print("❌ No internet connection")
    exit(1)

# Test credentials file
print("\n2. Testing credentials file...")
CREDENTIALS_PATH = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'
try:
    with open(CREDENTIALS_PATH, 'r') as f:
        print("✅ Credentials file exists and readable")
except Exception as e:
    print(f"❌ Credentials file error: {e}")
    exit(1)

# Test Google Sheets authentication
print("\n3. Testing Google Sheets authentication...")
try:
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
    print("✅ Credentials loaded successfully")
    
    client = gspread.authorize(creds)
    print("✅ Google Sheets client created")
    
except Exception as e:
    print(f"❌ Authentication error: {e}")
    exit(1)

# Test opening the specific spreadsheet
print("\n4. Testing spreadsheet access...")
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
try:
    sheet = client.open_by_key(SPREADSHEET_ID)
    print(f"✅ Opened spreadsheet: {sheet.title}")
    
    # Test accessing Claude Tasks worksheet
    claude_tasks = sheet.worksheet('Claude Tasks')
    print(f"✅ Accessed Claude Tasks worksheet")
    
    # Test reading data (just first few rows)
    values = claude_tasks.get_all_values()
    print(f"✅ Read {len(values)} rows from sheet")
    
    if len(values) > 0:
        print(f"   First row: {values[0][:3]}...")  # Show first 3 columns
    
except Exception as e:
    print(f"❌ Spreadsheet access error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# Test writing to sheet (safely)
print("\n5. Testing write access...")
try:
    # Get last row to append after
    last_row = len(values) + 1
    test_cell = f"H{last_row}"  # Use column H for test
    
    # Write a test value
    claude_tasks.update(test_cell, "Test connection")
    print(f"✅ Successfully wrote test data to {test_cell}")
    
    # Clean up - remove test data
    claude_tasks.update(test_cell, "")
    print("✅ Cleaned up test data")
    
except Exception as e:
    print(f"❌ Write access error: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Google Sheets connection test completed!")
print("If all tests passed, the connection issue might be intermittent.")
print("If any failed, we need to fix those specific issues.")