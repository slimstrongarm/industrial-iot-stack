#!/usr/bin/env python3
"""
Test dependency suggestion system with current Google Sheets tasks
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from dependency_analyzer import DependencyAnalyzer

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def test_dependency_suggestions():
    """Test dependency suggestions with real sheet data"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        worksheet = sheet.worksheet('Docker Migration Tasks')
        
        # Get all existing tasks
        all_tasks = worksheet.get_all_records()
        
        print("📋 Current tasks in your sheet:")
        for task in all_tasks:
            print(f"  {task['Task ID']}: {task['Task Description']} (Status: {task['Status']})")
        
        # Initialize analyzer
        analyzer = DependencyAnalyzer()
        
        # Test with some new task examples
        test_tasks = [
            "Create Docker Compose for Node-RED",
            "Deploy Ignition container to server",
            "Configure MQTT Engine in Ignition",
            "Test Flint VS Code integration",
            "Import projects to Docker Ignition",
            "Set up Grafana monitoring dashboard",
            "Create backup script for containers"
        ]
        
        print(f"\n🔍 Testing dependency suggestions for new tasks:")
        print("=" * 60)
        
        for new_task in test_tasks:
            print(f"\n📝 New Task: {new_task}")
            analysis = analyzer.analyze_task(new_task, all_tasks)
            
            print(f"   📂 Category: {analysis['category']}")
            print(f"   🔧 Service: {analysis['service']}")
            
            if analysis['suggested_dependencies']:
                print(f"   🔗 Suggested Dependencies: {', '.join(analysis['suggested_dependencies'])}")
                print(f"   💭 Reasoning: {analysis['reasoning']}")
            else:
                print(f"   ✅ No dependencies needed - can run independently")
            print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════╗
║           Dependency Suggestion Test                  ║
║        Testing Smart Dependency Analysis             ║
╚═══════════════════════════════════════════════════════╝
""")
    
    success = test_dependency_suggestions()
    
    if success:
        print("""
✅ Dependency analysis system is working!

When you add new tasks to your Google Sheet, the monitoring script will:
1. Detect the new task
2. Analyze it for logical dependencies  
3. Suggest appropriate dependencies
4. Optionally auto-set them (if enabled)

This ensures tasks run in the proper order automatically!
""")
    else:
        print("❌ Test failed - check your credentials and sheet access")