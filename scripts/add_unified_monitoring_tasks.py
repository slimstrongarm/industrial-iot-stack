#!/usr/bin/env python3
"""
Add Unified Monitoring Rollout Tasks CT-056 through CT-065 to Google Sheets
Implements comprehensive unified monitoring system integration
"""

from googleapiclient.discovery import build
from google.oauth2 import service_account
import json
from datetime import datetime
import os

# Configuration from existing setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials/iot-stack-credentials.json'
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'

def add_unified_monitoring_tasks():
    """Add unified monitoring rollout tasks CT-056 through CT-065 to Claude Tasks sheet"""
    
    try:
        # Load credentials using existing setup
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Get existing data to find next row
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A:J'
        ).execute()
        
        values = result.get('values', [])
        last_row = len(values) if values else 1
        next_row = last_row + 1
        
        print(f"📊 Found {len(values)} existing rows, adding tasks at row {next_row}")
        
        # Unified monitoring tasks matching exact sheet format:
        # Task ID, Instance, Task Type, Priority, Status, Description, Expected Output, Dependencies, Date Added, Completed
        monitoring_tasks = [
            # Phase 1: Foundation (Server Claude)
            [
                'CT-056',
                'Server Claude', 
                'Deploy Unified Monitor',
                'High',
                'Pending',
                'Deploy unified_industrial_monitor.py alongside existing Docker containers. Test integration with current monitoring systems.',
                'Unified monitor running and collecting metrics from all systems (Docker, MQTT, Node-RED, Ignition)',
                'CT-054 completed (Discord deployment tested)',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-057',
                'Server Claude',
                'Configure Monitor Integration',
                'High',
                'Pending',
                'Connect unified monitor to existing Node-RED performance monitoring and MQTT broker health checks. Ensure data format compatibility.',
                'All monitoring systems sharing data via common JSON format, no duplicate monitoring processes',
                'CT-056 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-058',
                'Mac Claude',
                'Create Monitoring Dashboard',
                'High',
                'Pending',
                'Create new "Monitoring Dashboard" tab in Google Sheets with unified view of all system metrics. Follow existing sheet formatting patterns.',
                'Single dashboard showing Docker health, MQTT status, Node-RED flows, Ignition status, and system resources',
                'CT-056 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            # Phase 2: Enhancement (Both Claudes)
            [
                'CT-059',
                'Server Claude',
                'MQTT Alert Distribution',
                'Medium',
                'Pending',
                'Configure unified monitor to publish critical alerts to MQTT topic iiot/monitoring/alerts for real-time distribution.',
                'Critical system events published to MQTT for consumption by Node-RED, Discord bot, and WhatsApp flows',
                'CT-057, CT-058 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-060',
                'Mac Claude',
                'Discord Bot Integration',
                'Medium',
                'Pending',
                'Integrate unified monitor alerts with Discord bot for automated task creation. Critical issues should auto-generate Claude tasks.',
                'System failures automatically create appropriate tasks in Google Sheets via Discord bot',
                'CT-059 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-061',
                'Server Claude',
                'WhatsApp Alert Testing',
                'Medium',
                'Pending',
                'Test WhatsApp integration for critical monitoring alerts using existing Node-RED flows. Verify alert formatting and delivery.',
                'Operations team receives properly formatted WhatsApp alerts for critical system events',
                'CT-059 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            # Phase 3: Intelligence (Advanced Features)
            [
                'CT-062',
                'Mac Claude',
                'Create Monitoring Runbook',
                'Medium',
                'Pending',
                'Document common monitoring scenarios and resolution procedures. Include Docker issues, MQTT failures, and Node-RED problems.',
                'Comprehensive runbook with step-by-step procedures for all common monitoring alerts',
                'CT-060, CT-061 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-063',
                'Server Claude',
                'Implement Auto-Recovery',
                'Low',
                'Pending',
                'Configure automated recovery actions for common failures. Container restarts, MQTT reconnections, flow reloads.',
                'Self-healing system that automatically recovers from 80% of common failures',
                'CT-062 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            [
                'CT-064',
                'Both',
                'Performance Baseline',
                'Low',
                'Pending',
                'Collect 7 days of unified monitoring data to establish performance baselines and alert thresholds.',
                'Historical data showing normal operation patterns, documented alert thresholds',
                'CT-063 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ],
            # Documentation and Rollout
            [
                'CT-065',
                'Mac Claude',
                'Update Documentation',
                'Medium',
                'Pending',
                'Update INDEX.md and .claude documentation with unified monitoring procedures. Add monitoring section to stack-components.',
                'Complete documentation reflecting unified monitoring architecture and procedures',
                'CT-058, CT-062 completed',
                datetime.now().strftime('%Y-%m-%d %H:%M'),
                ''
            ]
        ]
        
        # Add tasks to sheet
        range_name = f'Claude Tasks!A{next_row}:J{next_row + len(monitoring_tasks) - 1}'
        
        body = {
            'values': monitoring_tasks
        }
        
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=body
        ).execute()
        
        print(f"✅ Successfully added {len(monitoring_tasks)} unified monitoring tasks!")
        print(f"📋 Added tasks CT-056 through CT-065 to Google Sheets")
        print(f"🔗 View at: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        
        # Show task summary by phase
        print("\n📊 Unified Monitoring Rollout Plan:")
        print("\n🏗️ Phase 1: Foundation (CT-056 to CT-058)")
        print("  - Deploy unified monitor")
        print("  - Configure integrations")
        print("  - Create unified dashboard")
        
        print("\n🚀 Phase 2: Enhancement (CT-059 to CT-061)")
        print("  - MQTT alert distribution")
        print("  - Discord bot integration")
        print("  - WhatsApp alert testing")
        
        print("\n🧠 Phase 3: Intelligence (CT-062 to CT-064)")
        print("  - Create monitoring runbook")
        print("  - Implement auto-recovery")
        print("  - Establish performance baselines")
        
        print("\n📚 Documentation (CT-065)")
        print("  - Update all documentation with unified monitoring")
        
        print(f"\n🏭 Unified monitoring will transform the Industrial IoT stack!")
        print("📱 Single dashboard for complete stack visibility")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Credentials file not found: {SERVICE_ACCOUNT_FILE}")
        print("Please ensure the credentials file exists at the correct location.")
        return False
    except Exception as e:
        print(f"❌ Error adding tasks to Google Sheets: {e}")
        return False

def verify_tasks_added():
    """Verify the unified monitoring tasks were successfully added"""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        
        # Check for CT-056 through CT-065
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range='Claude Tasks!A:J'
        ).execute()
        
        values = result.get('values', [])
        monitoring_tasks = []
        
        for row in values:
            if len(row) > 0 and row[0] in ['CT-056', 'CT-057', 'CT-058', 'CT-059', 'CT-060', 
                                           'CT-061', 'CT-062', 'CT-063', 'CT-064', 'CT-065']:
                monitoring_tasks.append(row)
        
        if monitoring_tasks:
            print(f"\n✅ Verification: Found {len(monitoring_tasks)} unified monitoring tasks in sheet")
            
            # Count by instance
            server_tasks = [t for t in monitoring_tasks if len(t) > 1 and 'Server' in t[1]]
            mac_tasks = [t for t in monitoring_tasks if len(t) > 1 and t[1] == 'Mac Claude']
            both_tasks = [t for t in monitoring_tasks if len(t) > 1 and t[1] == 'Both']
            
            print(f"  Server Claude: {len(server_tasks)} tasks")
            print(f"  Mac Claude: {len(mac_tasks)} tasks")
            print(f"  Both: {len(both_tasks)} tasks")
            
            return True
        else:
            print("❌ Verification failed: No unified monitoring tasks found")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

if __name__ == "__main__":
    print("🏭 Adding Unified Monitoring Rollout Tasks to Google Sheets...")
    print("==================================================================")
    
    # Check if credentials file exists
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ Credentials file not found at: {SERVICE_ACCOUNT_FILE}")
        print("Please ensure the file exists and try again.")
        exit(1)
    
    # Add the tasks
    success = add_unified_monitoring_tasks()
    
    if success:
        print("\n🔍 Verifying tasks were added...")
        verify_tasks_added()
        print("\n🎉 Unified monitoring tasks successfully added to Google Sheets!")
        print("Server Claude and Mac Claude can now collaborate on unified monitoring rollout.")
    else:
        print("\n❌ Failed to add unified monitoring tasks")
        print("Please check credentials and try again.")