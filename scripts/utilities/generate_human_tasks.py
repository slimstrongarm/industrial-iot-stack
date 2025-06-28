#!/usr/bin/env python3
"""
Generate Human Tasks for Google Sheets based on completed autonomous work
"""

import json
from datetime import datetime
from pathlib import Path

def generate_human_tasks():
    """Generate comprehensive list of human tasks based on completed work"""
    
    print("📋 Generating Human Tasks List")
    print("=" * 40)
    
    # Current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Human tasks organized by priority and time required
    human_tasks = {
        "immediate_5min": [
            {
                "task": "Update Google Sheets - Mark Claude Tasks Complete",
                "priority": "High",
                "time": "2 min",
                "description": "Mark CT-013, CT-014, CT-016, CT-021 as COMPLETED in Claude Tasks sheet",
                "status": "Ready",
                "dependencies": None,
                "notes": "All work completed autonomously, just needs status update"
            },
            {
                "task": "Create Discord Webhooks",
                "priority": "High", 
                "time": "5 min",
                "description": "Create webhook URLs for #alerts, #logs, #general, #critical channels",
                "status": "Ready",
                "dependencies": "Discord server access",
                "notes": "Server link: https://discord.gg/5gWaB3cf - Right click channel → Integrations → Webhooks"
            },
            {
                "task": "Configure n8n Google Sheets Credentials",
                "priority": "High",
                "time": "5 min",
                "description": "Upload service account JSON to n8n credentials",
                "status": "Ready",
                "dependencies": "n8n access",
                "notes": "Service account file at /home/server/google-sheets-credentials.json"
            }
        ],
        "immediate_10min": [
            {
                "task": "Deploy Discord Integration",
                "priority": "High",
                "time": "10 min",
                "description": "Update webhook URLs in scripts and test MQTT→Discord flow",
                "status": "Ready",
                "dependencies": "Discord webhooks created",
                "notes": "Scripts ready at discord_webhook_integration.py"
            },
            {
                "task": "Test MQTT→Google Sheets Flow",
                "priority": "High",
                "time": "10 min", 
                "description": "Activate n8n workflow and test MQTT logging to Sheets",
                "status": "Ready",
                "dependencies": "Google Sheets credentials configured",
                "notes": "Test script ready at test_mqtt_sheets_flow.sh"
            },
            {
                "task": "Get Formbricks API Key",
                "priority": "Medium",
                "time": "10 min",
                "description": "Login to Formbricks, create API key, update test script",
                "status": "Ready",
                "dependencies": "Formbricks account access",
                "notes": "Integration guide at FORMBRICKS_INTEGRATION_GUIDE.json"
            }
        ],
        "next_session_30min": [
            {
                "task": "Install Ignition Scripts",
                "priority": "Medium",
                "time": "30 min",
                "description": "Import 3 Python scripts to Ignition project library",
                "status": "Ready",
                "dependencies": "Ignition Designer access",
                "notes": "Scripts in ignition-scripts/ folder with installation guide"
            },
            {
                "task": "Configure WhatsApp Business API",
                "priority": "Medium",
                "time": "30 min",
                "description": "Set up WhatsApp Business API or use webhook.site for testing",
                "status": "Ready",
                "dependencies": "Meta Developer account or webhook.site",
                "notes": "Can start with webhook.site for immediate testing"
            },
            {
                "task": "Complete End-to-End Integration Test",
                "priority": "High",
                "time": "20 min",
                "description": "Test full pipeline: Ignition→MQTT→n8n→Discord+Sheets",
                "status": "Pending",
                "dependencies": "All integrations configured",
                "notes": "Comprehensive test scenarios prepared"
            }
        ],
        "coordination_required": [
            {
                "task": "Sync with Mac Claude on Discord Bot",
                "priority": "Medium",
                "time": "15 min",
                "description": "Coordinate Discord bot vs webhook approach",
                "status": "Pending", 
                "dependencies": "Mac Claude availability",
                "notes": "Webhook approach ready, bot approach optional"
            },
            {
                "task": "Update IIOT Master Sheet Status",
                "priority": "Low",
                "time": "10 min",
                "description": "Update System Components Status with integration progress",
                "status": "Ready",
                "dependencies": None,
                "notes": "Major progress on MQTT, n8n, Discord integrations"
            }
        ]
    }
    
    # Generate formatted output for Google Sheets
    print("\n📊 HUMAN TASKS FOR GOOGLE SHEETS")
    print("=" * 40)
    print(f"Generated: {timestamp}")
    print("")
    
    print("🚀 IMMEDIATE TASKS (5 minutes each):")
    print("-" * 35)
    for task in human_tasks["immediate_5min"]:
        print(f"• {task['task']}")
        print(f"  Time: {task['time']} | Priority: {task['priority']}")
        print(f"  {task['description']}")
        if task['notes']:
            print(f"  💡 {task['notes']}")
        print()
    
    print("⚡ QUICK WINS (10 minutes each):")
    print("-" * 35)
    for task in human_tasks["immediate_10min"]:
        print(f"• {task['task']}")
        print(f"  Time: {task['time']} | Priority: {task['priority']}")
        print(f"  {task['description']}")
        if task['dependencies']:
            print(f"  ⚠️  Depends on: {task['dependencies']}")
        print()
    
    print("📅 NEXT SESSION TASKS (30 minutes):")
    print("-" * 35)
    for task in human_tasks["next_session_30min"]:
        print(f"• {task['task']}")
        print(f"  Time: {task['time']} | Priority: {task['priority']}")
        print(f"  {task['description']}")
        print()
    
    # Create CSV format for easy copying to Google Sheets
    print("\n📋 CSV FORMAT FOR GOOGLE SHEETS:")
    print("=" * 40)
    print("Task,Priority,Time Required,Status,Dependencies,Notes")
    
    all_tasks = []
    for category, tasks in human_tasks.items():
        all_tasks.extend(tasks)
    
    for task in all_tasks:
        csv_line = f'"{task["task"]}","{task["priority"]}","{task["time"]}","{task["status"]}","{task["dependencies"] or "None"}","{task["notes"]}"'
        print(csv_line)
    
    # Save to file
    with open('/mnt/c/Users/LocalAccount/industrial-iot-stack/HUMAN_TASKS_UPDATE.json', 'w') as f:
        json.dump({
            "generated": timestamp,
            "tasks": human_tasks,
            "summary": {
                "immediate_tasks": len(human_tasks["immediate_5min"]) + len(human_tasks["immediate_10min"]),
                "total_immediate_time": "45 minutes",
                "next_session_time": "80 minutes",
                "blockers": "Discord webhooks, Google Sheets credentials, Formbricks API key"
            }
        }, f, indent=2)
    
    print("\n✅ Human tasks list generated!")
    print("📁 Saved to: HUMAN_TASKS_UPDATE.json")
    
    return human_tasks

if __name__ == "__main__":
    tasks = generate_human_tasks()
    
    print("\n🎯 SUMMARY:")
    print("• Immediate actions: 6 tasks (45 min total)")
    print("• All tasks ready with documentation")
    print("• Major blockers: Just need access credentials")
    print("• Autonomous work has cleared the path!")