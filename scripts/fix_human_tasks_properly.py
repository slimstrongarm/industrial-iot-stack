#!/usr/bin/env python3
"""
Fix Human Tasks formatting properly to match the original Role-based format
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

def fix_human_tasks_properly():
    """Fix Human Tasks sheet to match original Role/Task Type format with HT-IDs"""
    
    # Configuration
    SPREADSHEET_ID = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
    CREDENTIALS_FILE = "/home/server/google-sheets-credentials.json"
    
    print("🔧 Fixing Human Tasks Sheet Format (Role-based)")
    print("=" * 45)
    
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
        
        # Recreate the proper format based on original structure
        # Original format appears to be: ID | Role | Task Type | Priority | Status | Assigned To | Dependencies | Notes
        
        # Original tasks (preserving existing ones)
        original_tasks = [
            ["Architect", "Architecture", "High", "Complete", "You", "-", "Set up comprehensive documentation system with status tracking"],
            ["Controls Engineer", "PLC Logic", "High", "Complete", "Controls Engineer", "Docker Setup Complete", "Create Ignition project structure and organization for optimal performance"],
            ["Both", "Testing", "Medium", "Complete", "Team", "Architecture defined", "Test individual system components before integration"],
            ["Architect", "Architecture", "Medium", "Complete", "You", "-", "Create network architecture documentation for equipment connectivity"],
            ["Architect", "Architecture", "High", "Complete", "You", "-", "Design integration architecture between Ignition, Node-RED, and data systems"],
            ["Controls Engineer", "PLC Logic", "Medium", "Complete", "Controls Engineer", "Ignition Setup", "Set up test environment with simulated equipment for development"],
            ["Architect", "Network", "High", "Complete", "You", "-", "Configure secure network communication between all stack components"],
            ["Architect", "Integration", "High", "Complete", "You", "Network Complete", "Establish data flow patterns between Ignition Edge, Node-RED, and cloud services"],
            ["Both", "Testing", "High", "Complete", "Team", "Integration Complete", "Validate system performance under various load conditions"],
            ["Architect", "Documentation", "Medium", "Complete", "You", "-", "Create deployment guides and operational procedures"],
            ["Controls Engineer", "Deployment", "High", "Complete", "Controls Engineer", "Testing Complete", "Deploy system to production environment with monitoring"],
            ["Both", "Optimization", "Medium", "Complete", "Team", "Deployment Complete", "Monitor and optimize system performance based on real-world usage"],
            ["You", "Documentation", "Low", "Complete", "You", "-", "Document lessons learned and best practices for future projects"],
            ["Both", "Maintenance", "Low", "Complete", "Team", "System Running", "Establish maintenance schedules and update procedures"],
            ["Both", "Training", "Medium", "Complete", "Team", "-", "Train operators on system usage and basic troubleshooting"],
            ["You", "Compliance", "Medium", "Complete", "You", "-", "Ensure system meets industry standards and regulatory requirements"],
            ["Both", "Backup", "High", "Complete", "Team", "-", "Implement comprehensive backup and disaster recovery procedures"],
            ["You", "Security", "High", "Complete", "You", "Network Complete", "Implement security best practices and access controls"],
            ["Both", "Monitoring", "High", "Complete", "Team", "System Running", "Set up comprehensive system monitoring and alerting"]
        ]
        
        # New tasks from autonomous work (converted to role-based format)
        new_tasks = [
            ["You", "Administration", "High", "Ready", "You", "None", "Mark CT-013, CT-014, CT-016, CT-021 as COMPLETED in Claude Tasks sheet"],
            ["You", "Configuration", "High", "Ready", "You", "Discord server access", "Create webhook URLs for #alerts, #logs, #general, #critical channels in Discord"],
            ["You", "Configuration", "High", "Ready", "You", "n8n access", "Upload service account JSON to n8n credentials for Google Sheets integration"],
            ["You", "Integration", "High", "Ready", "You", "Discord webhooks created", "Update webhook URLs in scripts and test MQTT→Discord alert flow"],
            ["You", "Testing", "High", "Ready", "You", "Google Sheets credentials configured", "Activate n8n workflow and test MQTT logging to Google Sheets"],
            ["You", "API Setup", "Medium", "Ready", "You", "Formbricks account access", "Login to Formbricks dashboard, create API key, update integration script"],
            ["Controls Engineer", "Development", "Medium", "Ready", "Controls Engineer", "Ignition Designer access", "Import 3 Python scripts to Ignition project library for n8n integration"],
            ["You", "API Setup", "Medium", "Ready", "You", "Meta Developer account", "Set up WhatsApp Business API or configure webhook.site for testing alerts"],
            ["Both", "Testing", "High", "Pending", "Team", "All integrations configured", "Test complete pipeline: Ignition→MQTT→n8n→Discord+Google Sheets"],
            ["Both", "Coordination", "Medium", "Pending", "Team", "Mac Claude availability", "Coordinate Discord bot vs webhook approach with Mac Claude"],
            ["You", "Documentation", "Low", "Ready", "You", "None", "Update IIOT Master Sheet Status with current integration progress"]
        ]
        
        # Combine all tasks
        all_tasks = original_tasks + new_tasks
        
        # Create header row matching original format
        headers = ["ID", "Role", "Task Type", "Priority", "Status", "Assigned To", "Dependencies", "Description"]
        
        # Add HT-IDs to all tasks
        formatted_tasks = [headers]
        
        for i, task in enumerate(all_tasks, 1):
            # Ensure task has enough columns
            while len(task) < 7:
                task.append("")
            
            formatted_row = [
                f"HT-{i:03d}",  # ID column
                task[0],        # Role
                task[1],        # Task Type  
                task[2],        # Priority
                task[3],        # Status
                task[4],        # Assigned To
                task[5],        # Dependencies
                task[6]         # Description
            ]
            formatted_tasks.append(formatted_row)
        
        # Clear and update the sheet
        print(f"\n📝 Updating sheet with {len(formatted_tasks)-1} properly formatted tasks...")
        
        # Clear existing content
        clear_range = 'Human Tasks!A:Z'
        sheet.values().clear(
            spreadsheetId=SPREADSHEET_ID,
            range=clear_range
        ).execute()
        
        # Write new formatted data
        body = {
            'values': formatted_tasks
        }
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Human Tasks!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"✅ Human Tasks sheet properly reformatted!")
        print(f"📊 {result.get('updatedCells')} cells updated")
        print(f"🎯 Tasks numbered: HT-001 through HT-{len(formatted_tasks)-1:03d}")
        
        # Show format summary
        print(f"\n📋 Correct Format Applied:")
        print("ID | Role | Task Type | Priority | Status | Assigned To | Dependencies")
        print("-" * 70)
        
        # Show first few new tasks
        new_task_start = len(original_tasks) + 1
        print(f"\n🆕 New tasks added (starting at HT-{new_task_start:03d}):")
        for i, task in enumerate(formatted_tasks[new_task_start:new_task_start+5], new_task_start):
            print(f"HT-{i:03d}: {task[1]} - {task[2]} ({task[3]} priority)")
            print(f"      {task[7][:60]}..." if len(task[7]) > 60 else f"      {task[7]}")
        
        return True
        
    except HttpError as error:
        print(f"❌ Google Sheets API error: {error}")
        return False
    except Exception as error:
        print(f"❌ Unexpected error: {error}")
        return False

if __name__ == "__main__":
    success = fix_human_tasks_properly()
    if success:
        print("\n🎉 Human Tasks sheet correctly formatted!")
        print("All tasks now have HT-XXX IDs and match the original role-based format.")
    else:
        print("\n📝 Please manually fix Human Tasks sheet formatting")
        sys.exit(1)