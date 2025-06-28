#!/usr/bin/env python3
"""
Add Discord Integration Tasks to Google Sheets
For Friday Brewery Demo
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def add_discord_tasks():
    """Add comprehensive Discord integration tasks for brewery demo"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to IoT Stack Progress Master")
        now = datetime.now()
        
        # Calculate dates for Friday demo
        friday = now + timedelta(days=2)  # Assuming today is Wednesday
        thursday = friday - timedelta(days=1)
        
        # 1. CLAUDE TASKS (Server-Claude to execute)
        print("\n🤖 Adding Claude Tasks...")
        claude_tasks_sheet = sheet.worksheet('Claude Tasks')
        
        claude_tasks = [
            ["DISC-001", "Create Discord bot application", "Pending", "High", "Server Claude", 
             now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"), "0%", 
             "Create bot in Discord Developer Portal", "", "discord.py"],
             
            ["DISC-002", "Deploy Discord bot container", "Pending", "High", "Server Claude",
             now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"), "0%", 
             "Docker container with Discord.py + monitoring", "DISC-001", "docker, discord.py"],
             
            ["DISC-003", "Connect bot to Google Sheets API", "Pending", "High", "Server Claude",
             now.strftime("%Y-%m-%d"), thursday.strftime("%Y-%m-%d"), "0%", 
             "Use existing credentials for sheets integration", "DISC-002", "gspread, oauth2"],
             
            ["DISC-004", "Implement basic monitoring commands", "Pending", "High", "Server Claude",
             thursday.strftime("%Y-%m-%d"), thursday.strftime("%Y-%m-%d"), "0%", 
             "/status, /health, /containers commands", "DISC-003", "docker ps, system monitoring"],
             
            ["DISC-005", "Setup Docker alerts to Discord", "Pending", "Medium", "Server Claude",
             thursday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), "0%", 
             "Container down/up notifications", "DISC-004", "docker events"],
             
            ["DISC-006", "Deploy bot to server production", "Pending", "High", "Server Claude",
             friday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), "0%", 
             "Final deployment for brewery demo", "DISC-005", "production deployment"]
        ]
        
        for task in claude_tasks:
            claude_tasks_sheet.append_row(task)
            
        # 2. HUMAN TASKS (For Josh)
        print("👤 Adding Human Tasks...")
        human_tasks_sheet = sheet.worksheet('Human Tasks')
        
        human_tasks = [
            ["DISC-H01", "Create Discord server with channels", "Pending", "High", "Josh",
             now.strftime("%Y-%m-%d"), now.strftime("%Y-%m-%d"), "0%", 
             "#mac-claude, #server-claude, #general, #alerts channels", "", "Discord mobile app"],
             
            ["DISC-H02", "Test Discord bot from iPhone", "Pending", "High", "Josh",
             thursday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), "0%", 
             "Verify mobile interaction works smoothly", "DISC-004", "Discord mobile app"],
             
            ["DISC-H03", "Prepare brewery demo script", "Pending", "High", "Josh",
             thursday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), "0%", 
             "Show real-time monitoring via Discord", "DISC-H02", "demo preparation"],
             
            ["DISC-H04", "Set up brewery-specific monitoring", "Pending", "Medium", "Josh",
             friday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), "0%", 
             "Custom alerts for brewery equipment", "DISC-006", "brewery domain knowledge"]
        ]
        
        for task in human_tasks:
            human_tasks_sheet.append_row(task)
            
        # 3. INTEGRATION CHECKLIST
        print("🔗 Adding Integration Checklist...")
        integration_sheet = sheet.worksheet('Integration Checklist')
        
        integrations = [
            ["Discord ↔ Mac Claude", "🔄 In Progress", "-", "✅ Complete", "❌ No"],
            ["Discord ↔ Server Claude", "🔄 In Progress", "-", "📝 In Progress", "❌ No"],
            ["Discord ↔ Google Sheets", "🔄 In Progress", "-", "📝 In Progress", "❌ No"],
            ["Discord ↔ Docker Monitoring", "⏳ Pending", "-", "⏳ Pending", "❌ No"],
            ["Discord ↔ MQTT Alerts", "⏳ Pending", "-", "⏳ Pending", "❌ No"],
            ["Mobile Discord Interface", "⏳ Pending", "-", "⏳ Pending", "❌ No"]
        ]
        
        for integration in integrations:
            integration_sheet.append_row(integration)
            
        # 4. UPDATE DOCKER MIGRATION TASKS  
        print("📋 Adding Discord to Docker Migration...")
        docker_sheet = sheet.worksheet('Docker Migration Tasks')
        
        docker_discord_tasks = [
            ["DM-020", "Discord bot infrastructure", "Pending", "High", "Server Claude",
             now.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), "0%", 
             "Complete Discord integration for demo", "DM-019"],
             
            ["DM-021", "Mobile command center demo", "Pending", "High", "Josh",
             friday.strftime("%Y-%m-%d"), friday.strftime("%Y-%m-%d"), "0%", 
             "Show brewery client mobile control", "DM-020"]
        ]
        
        for task in docker_discord_tasks:
            docker_sheet.append_row(task)
            
        # 5. LOG ACTIVITY
        print("📝 Logging Activity...")
        agent_sheet = sheet.worksheet('Agent Activities')
        
        agent_sheet.append_row([
            now.strftime("%Y-%m-%d %H:%M:%S"),
            "Mac Claude",
            "Discord integration planning",
            "Complete", 
            "30 min",
            "Added 12 tasks across 4 tabs for Friday brewery demo",
            "Execute Discord tasks"
        ])
        
        print("\n🎉 SUCCESS! Added Discord integration tasks:")
        print("   📋 6 Claude Tasks (for server-claude)")
        print("   👤 4 Human Tasks (for Josh)")  
        print("   🔗 6 Integration checkpoints")
        print("   📊 2 Docker migration tasks")
        print(f"   🎯 Target: Friday {friday.strftime('%Y-%m-%d')} brewery demo")
        print("\n📱 Your existing automation will pick these up in 60 seconds!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    add_discord_tasks()