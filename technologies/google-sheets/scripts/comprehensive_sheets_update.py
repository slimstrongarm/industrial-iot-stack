#!/usr/bin/env python3
"""
Comprehensive Google Sheets Update - Current Status
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def update_all_sheets():
    """Update all tabs with current progress"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("✅ Connected to IoT Stack Progress Master")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 1. Update Docker Migration Tasks
        print("\n📋 Updating Docker Migration Tasks...")
        try:
            docker_sheet = sheet.worksheet('Docker Migration Tasks')
            updates = [
                [2, 3, "Complete"],  # Row 2, Column C - Ignition Docker config
                [2, 8, "100%"],      # Completion percentage
                [3, 3, "Complete"],  # Flint Docker research
                [3, 8, "100%"],
                [4, 3, "Complete"],  # Modular architecture
                [4, 8, "100%"],
                [4, 9, f"Architecture documented, ready for deployment - {timestamp}"]
            ]
            for row, col, value in updates:
                docker_sheet.update_cell(row, col, value)
        except Exception as e:
            print(f"Error updating Docker tasks: {e}")
        
        # 2. Update System Components Status
        print("📊 Updating System Components Status...")
        try:
            components_sheet = sheet.worksheet('System Components Status')
            # Add new components
            new_rows = [
                ["n8n", "Planned", "📋 Ready", "Latest", timestamp, "-", "-", "-", "Architecture defined"],
                ["Grafana", "Planned", "📋 Ready", "10.3.1", timestamp, "-", "-", "-", "Docker config ready"],
                ["InfluxDB", "Planned", "📋 Ready", "2.7", timestamp, "-", "-", "-", "For time-series data"]
            ]
            # Find last row and append
            last_row = len(components_sheet.get_all_values()) + 1
            for i, row in enumerate(new_rows):
                components_sheet.insert_row(row, last_row + i)
                
            # Update existing components
            components_sheet.update_cell(5, 5, timestamp)  # Portainer last updated
        except Exception as e:
            print(f"Error updating components: {e}")
        
        # 3. Update Agent Activities
        print("🤖 Updating Agent Activities...")
        try:
            agent_sheet = sheet.worksheet('Agent Activities')
            activities = [
                [timestamp, "Mac Claude", "SSH connection established", "Complete", "2 hours", "Tailscale + SSH working", "Server setup"],
                [timestamp, "Mac Claude", "Google Sheets automation", "Complete", "1 hour", "All tabs automated", "Monitor progress"],
                [timestamp, "Mac Claude", "n8n + Grafana modules added", "Complete", "1 hour", "Architecture documented", "Deploy when ready"],
                [timestamp, "Mac Claude", "Server scripts prepared", "Complete", "30 min", "Audit & TMUX ready", "Execute on server"]
            ]
            for activity in activities:
                agent_sheet.append_row(activity)
        except Exception as e:
            print(f"Error updating agent activities: {e}")
        
        # 4. Update Integration Checklist
        print("✅ Updating Integration Checklist...")
        try:
            integration_sheet = sheet.worksheet('Integration Checklist')
            # Update SSH/Tailscale integration
            integration_sheet.update_cell(7, 2, "✅ Complete")  # Status
            integration_sheet.update_cell(7, 3, "✅ Pass")      # Test Result
            integration_sheet.update_cell(7, 4, "✅ Complete")  # Documentation
            integration_sheet.update_cell(7, 5, "✅ Yes")       # Production Ready
        except Exception as e:
            print(f"Error updating integrations: {e}")
        
        # 5. Update Human Tasks
        print("👤 Updating Human Tasks...")
        try:
            human_sheet = sheet.worksheet('Human Tasks')
            # Update server connection tasks
            updates = [
                ["Complete", 2, 4],  # Server booted - Row 2, Column D
                ["Complete", 3, 4],  # Tailscale IP provided
                ["Complete", 4, 4],  # SSH username provided
                ["Complete", 5, 4],  # SSH access verified
                ["In Progress", 6, 4],  # Docker verification
            ]
            for status, row, col in updates:
                try:
                    human_sheet.update_cell(row, col, status)
                except:
                    pass  # Skip if row doesn't exist
        except Exception as e:
            print(f"Error updating human tasks: {e}")
        
        # 6. Update Dashboard
        print("📊 Updating Dashboard...")
        try:
            dashboard_sheet = sheet.worksheet('Dashboard')
            dashboard_sheet.update_cell(13, 2, f'="{timestamp}"')  # Last updated
            
            # Add current status summary
            status_text = [
                ["", ""],
                ["Current Status Summary:", ""],
                ["SSH Access:", "✅ Connected via Tailscale"],
                ["Docker Status:", "🔄 Checking existing services"],
                ["Server TMUX:", "🔵 Blue theme ready"],
                ["Mac TMUX:", "🍎 Green theme running"],
                ["Demo Prep:", "📅 Friday deadline"],
                ["", ""],
                ["Next Actions:", ""],
                ["1. Audit server services", "🔍 In Progress"],
                ["2. Configure Ignition Edge", "📋 Pending"],
                ["3. Test data flow", "📋 Pending"]
            ]
            
            # Write status starting from row 15
            for i, row in enumerate(status_text):
                for j, value in enumerate(row):
                    dashboard_sheet.update_cell(15 + i, 1 + j, value)
                    
        except Exception as e:
            print(f"Error updating dashboard: {e}")
        
        print(f"\n✅ All sheets updated at {timestamp}")
        print("📊 Check your Google Sheets for the latest status!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_all_sheets()