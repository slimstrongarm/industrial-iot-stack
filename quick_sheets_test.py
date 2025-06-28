#!/usr/bin/env python3
"""Quick Google Sheets connection test"""

try:
    import gspread
    from google.oauth2.service_account import Credentials
    
    print("🔍 Quick Google Sheets Test")
    print("=" * 30)
    
    # Setup
    CREDENTIALS_PATH = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'
    SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
    
    # Test connection
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=scope)
    client = gspread.authorize(creds)
    
    # Test sheet access
    sheet = client.open_by_key(SPREADSHEET_ID)
    claude_tasks = sheet.worksheet('Claude Tasks')
    
    # Quick read test
    values = claude_tasks.get_all_values()
    print(f"✅ SUCCESS: Read {len(values)} rows from Claude Tasks")
    
    # Find next task ID
    last_num = 0
    for row in values[1:]:  # Skip header
        if row and row[0].startswith('CT-'):
            try:
                num = int(row[0].split('-')[1])
                last_num = max(last_num, num)
            except:
                pass
    
    next_id = f"CT-{last_num + 1:03d}"
    print(f"✅ Next task ID would be: {next_id}")
    print("✅ Google Sheets connection is working!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    
    # Check if it's the specific "Connection reset by peer" error
    if "Connection reset by peer" in str(e):
        print("\n💡 This error often means:")
        print("1. Rate limiting - too many requests")
        print("2. Network connectivity issues")
        print("3. Try again in 30 seconds")
        print("\n🔧 Quick fix: Add retry logic to the bot")
    
    import traceback
    traceback.print_exc()