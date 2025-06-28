#!/usr/bin/env python3
"""
Test Mac Claude Environment & Google Sheets Integration
Focus on what Mac Claude actually needs to do - Google Sheets coordination and local development
"""

import sys
import os
import json
from pathlib import Path

def test_google_sheets_imports():
    """Test Google Sheets related imports"""
    print("🔍 Testing Google Sheets imports...")
    
    required_modules = [
        'gspread', 'google.oauth2.service_account',
        'json', 'datetime', 'pathlib'
    ]
    
    failed_imports = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_credentials():
    """Test that credentials file exists and is valid JSON"""
    print("\n🔍 Testing credentials...")
    
    creds_path = Path('credentials/iot-stack-credentials.json')
    if not creds_path.exists():
        print(f"❌ Credentials file not found: {creds_path}")
        return False
    
    try:
        with open(creds_path, 'r') as f:
            creds = json.load(f)
        print("✅ Credentials file is valid JSON")
        
        # Check for required fields
        required_fields = ['type', 'project_id', 'private_key', 'client_email']
        for field in required_fields:
            if field in creds:
                print(f"✅ {field} present")
            else:
                print(f"❌ {field} missing")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Credentials error: {e}")
        return False

def test_server_deployment_readiness():
    """Test that server deployment files are ready"""
    print("\n🔍 Testing server deployment readiness...")
    
    # Check Discord bot files for server deployment
    bot_files = [
        'discord-bot/industrial_iot_claude_bot.py',
        'discord-bot/run_server_claude_bot.py',
        'discord-bot/Dockerfile',
        'discord-bot/docker-compose.yml'
    ]
    
    all_present = True
    for file_path in bot_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} missing")
            all_present = False
    
    return all_present

def test_scripts_directory():
    """Test that Mac Claude's script automation is ready"""
    print("\n🔍 Testing script automation capabilities...")
    
    # Check for key automation scripts
    key_scripts = [
        'scripts/utilities/create_claude_action_setup_tab.py',
        'scripts/utilities/get_claude_session.py', 
        'scripts/morning_status_update.py',
        'scripts/monitor_claude_tasks.py'
    ]
    
    all_present = True
    for script_path in key_scripts:
        path = Path(script_path)
        if path.exists():
            print(f"✅ {script_path}")
        else:
            print(f"❌ {script_path} missing")
            all_present = False
    
    return all_present

def test_google_sheets_simple():
    """Simple Google Sheets connection test"""
    print("\n🔍 Testing Google Sheets connection...")
    
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        # Setup credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'credentials/iot-stack-credentials.json', 
            scopes=scope
        )
        
        # Connect to Google Sheets
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do')
        worksheet = sheet.worksheet('Claude Tasks')
        
        # Use get_all_values instead of get_all_records to avoid header issues
        all_values = worksheet.get_all_values()
        next_id = f"CT-{len(all_values):03d}"  # Includes header row
        
        print("✅ Google Sheets connection successful")
        print(f"📊 Total rows: {len(all_values)} (including header)")
        print(f"📋 Task rows: {len(all_values) - 1}")
        print(f"🆔 Next task ID: {next_id}")
        
        # Show CT-099 status
        for i, row in enumerate(all_values):
            if len(row) > 0 and row[0] == 'CT-099':
                status = row[4] if len(row) > 4 else 'Unknown'
                assigned = row[1] if len(row) > 1 else 'Unassigned'
                description = row[5] if len(row) > 5 else 'No description'
                print(f"🎯 CT-099: {status} (Assigned: {assigned})")
                print(f"   📝 Task: {description[:60]}...")
                break
        
        return True
        
    except Exception as e:
        print(f"❌ Google Sheets error: {e}")
        return False

def main():
    """Run all tests focused on Mac Claude's actual role"""
    print("🍎 Mac Claude Environment Test")
    print("Testing Google Sheets integration and server deployment readiness")
    print("=" * 60)
    
    tests = [
        ("Google Sheets Imports", test_google_sheets_imports),
        ("Credentials", test_credentials),
        ("Server Deployment Files", test_server_deployment_readiness), 
        ("Script Automation", test_scripts_directory),
        ("Google Sheets Connection", test_google_sheets_simple)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test failed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📋 Test Results Summary:")
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 Mac Claude Environment Ready!")
        print("\n🚀 Mac Claude's Role:")
        print("   • Google Sheets coordination and task management")
        print("   • Local development and script automation")
        print("   • Server deployment preparation")
        print("   • Code development and testing")
        print("\n📱 Server Claude will handle:")
        print("   • Discord bot (CT-099 deployment)")
        print("   • 24/7 operations and monitoring")
        print("   • Production system management")
    else:
        print("⚠️  Some tests failed. Check the output above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)