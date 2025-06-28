#!/usr/bin/env python3
"""
Add Discord Bot Deployment Tasks to Google Sheets
Creates comprehensive deployment task list for Server Claude
"""

import gspread
import json
from datetime import datetime

def add_discord_deployment_tasks():
    """Add Discord deployment tasks to Claude Tasks sheet"""
    
    # Initialize Google Sheets client
    gc = gspread.service_account(filename='../credentials/iot-stack-credentials.json')
    sheet = gc.open("IIoT Stack Progress Tracker")
    claude_tasks = sheet.worksheet("Claude Tasks")
    
    # Get next task ID
    task_ids = claude_tasks.col_values(1)[1:]  # Skip header
    next_id = len([t for t in task_ids if t.startswith('CT-')]) + 1
    
    # Discord deployment tasks
    deployment_tasks = [
        {
            'assigned_to': 'Server Claude',
            'title': 'Deploy Discord Bot Docker Container',
            'priority': 'High',
            'description': 'Deploy the Discord bot using Docker Compose on server infrastructure. Follow SERVER_CLAUDE_DEPLOYMENT_PACKAGE.md instructions for containerized deployment.',
            'expected_output': 'Discord bot running as persistent Docker service with auto-restart capabilities',
            'dependencies': 'Docker and docker-compose installed on server'
        },
        {
            'assigned_to': 'Server Claude', 
            'title': 'Deploy Task Worker Container',
            'priority': 'High',
            'description': 'Deploy the Mac Claude task worker as Docker container alongside Discord bot. Ensure proper networking and credential access.',
            'expected_output': 'Task worker container running and processing Google Sheets tasks automatically',
            'dependencies': 'CT-051 completed (Discord bot deployed)'
        },
        {
            'assigned_to': 'Server Claude',
            'title': 'Configure Health Monitoring System',
            'priority': 'Medium', 
            'description': 'Set up health monitoring for Discord bot and task worker containers. Implement auto-restart and alerting capabilities.',
            'expected_output': 'Health monitor running and automatically restarting failed services',
            'dependencies': 'CT-051, CT-052 completed'
        },
        {
            'assigned_to': 'Server Claude',
            'title': 'Test Complete Discord Automation Flow',
            'priority': 'High',
            'description': 'Test end-to-end workflow: Discord command → Google Sheets task → automated processing → completion. Verify 24/7 persistent operation.',
            'expected_output': 'Complete workflow tested and verified working continuously without manual intervention',
            'dependencies': 'CT-051, CT-052, CT-053 completed'
        },
        {
            'assigned_to': 'Mac Claude',
            'title': 'Update Documentation with Deployment Success',
            'priority': 'Medium',
            'description': 'Update INDEX.md and .claude documentation to reflect successful persistent deployment capabilities and workflow automation.',
            'expected_output': 'Documentation updated with deployment procedures and automation workflows',
            'dependencies': 'CT-054 completed (testing successful)'
        }
    ]
    
    # Add tasks to sheet
    for i, task in enumerate(deployment_tasks):
        task_id = f"CT-{next_id + i:03d}"
        
        new_row = [
            task_id,
            task['assigned_to'],
            task['title'],
            task['priority'],
            'Pending',
            task['description'],
            task['expected_output'],
            task['dependencies']
        ]
        
        claude_tasks.append_row(new_row)
        print(f"✅ Added {task_id}: {task['title']}")
    
    print(f"\n🎉 Added {len(deployment_tasks)} Discord deployment tasks to Google Sheets")
    print("📋 Tasks CT-051 through CT-055 created for Discord bot deployment automation")

if __name__ == "__main__":
    add_discord_deployment_tasks()