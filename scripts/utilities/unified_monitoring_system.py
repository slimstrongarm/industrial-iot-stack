#!/usr/bin/env python3
"""
Unified Monitoring System for Google Sheets + n8n API
Mac Claude - CT-015 Implementation
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from pathlib import Path
from datetime import datetime
import time
import json
import base64

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

# n8n API Configuration
N8N_URL = "http://100.94.84.126:5678"
N8N_USERNAME = "iiot-admin"
N8N_PASSWORD = "StrongPassword123!"

class UnifiedMonitor:
    def __init__(self):
        """Initialize monitoring connections"""
        self.sheet_client = self._init_sheets()
        self.n8n_auth = self._init_n8n_auth()
        
    def _init_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
            client = gspread.authorize(creds)
            return client.open_by_key(SHEET_ID)
        except Exception as e:
            print(f"❌ Sheets connection error: {e}")
            return None
    
    def _init_n8n_auth(self):
        """Initialize n8n API authentication"""
        try:
            auth_string = f"{N8N_USERNAME}:{N8N_PASSWORD}"
            auth_bytes = base64.b64encode(auth_string.encode()).decode()
            return {"Authorization": f"Basic {auth_bytes}"}
        except Exception as e:
            print(f"❌ n8n auth error: {e}")
            return None
    
    def check_n8n_health(self):
        """Check n8n instance health"""
        try:
            response = requests.get(f"{N8N_URL}/healthz", 
                                  headers=self.n8n_auth, 
                                  timeout=10)
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "code": response.status_code,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def get_n8n_workflows(self):
        """Get active n8n workflows"""
        try:
            response = requests.get(f"{N8N_URL}/api/v1/workflows", 
                                  headers=self.n8n_auth,
                                  timeout=10)
            if response.status_code == 200:
                workflows = response.json()
                return {
                    "count": len(workflows.get('data', [])),
                    "active": len([w for w in workflows.get('data', []) if w.get('active')]),
                    "workflows": workflows.get('data', [])[:5]  # Last 5 workflows
                }
        except Exception as e:
            return {"error": str(e)}
    
    def get_recent_executions(self):
        """Get recent n8n workflow executions"""
        try:
            response = requests.get(f"{N8N_URL}/api/v1/executions", 
                                  headers=self.n8n_auth,
                                  params={"limit": 10},
                                  timeout=10)
            if response.status_code == 200:
                executions = response.json()
                return {
                    "recent": executions.get('data', [])[:5],
                    "total": len(executions.get('data', []))
                }
        except Exception as e:
            return {"error": str(e)}
    
    def get_sheets_status(self):
        """Get Google Sheets monitoring status"""
        if not self.sheet_client:
            return {"error": "No sheets connection"}
        
        try:
            # Agent Activities
            agent_sheet = self.sheet_client.worksheet('Agent Activities')
            activities = agent_sheet.get_all_values()
            recent_activities = activities[-3:] if len(activities) > 3 else activities[1:]
            
            # Claude Tasks
            claude_sheet = self.sheet_client.worksheet('Claude Tasks')
            tasks = claude_sheet.get_all_values()
            in_progress = [t for t in tasks[1:] if len(t) > 3 and t[3] == 'In Progress']
            completed_today = [t for t in tasks[1:] if len(t) > 4 and datetime.now().strftime("%Y-%m-%d") in str(t[4])]
            
            # Pending Approvals
            approval_sheet = self.sheet_client.worksheet('Claude Approvals')
            approvals = approval_sheet.get_all_values()
            pending = [a for a in approvals[1:] if len(a) > 3 and a[3] == 'PENDING']
            
            return {
                "recent_activities": len(recent_activities),
                "tasks_in_progress": len(in_progress),
                "tasks_completed_today": len(completed_today),
                "pending_approvals": len(pending),
                "last_activity": recent_activities[-1] if recent_activities else None
            }
        except Exception as e:
            return {"error": str(e)}
    
    def update_monitoring_dashboard(self, data):
        """Update unified monitoring data in sheets"""
        if not self.sheet_client:
            return False
        
        try:
            # Update Dashboard with unified monitoring data
            dashboard = self.sheet_client.worksheet('Dashboard')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Row 15: n8n Health Status
            dashboard.update('B15', data['n8n']['status'])
            dashboard.update('C15', timestamp)
            
            # Row 16: Active Workflows
            dashboard.update('B16', f"{data['workflows'].get('active', 0)}/{data['workflows'].get('count', 0)}")
            
            # Row 17: Recent Executions
            dashboard.update('B17', data['executions'].get('total', 0))
            
            # Row 18: Sheets Status
            dashboard.update('B18', f"Tasks: {data['sheets'].get('tasks_in_progress', 0)} active")
            
            return True
        except Exception as e:
            print(f"❌ Dashboard update error: {e}")
            return False
    
    def run_unified_monitoring(self):
        """Run complete unified monitoring check"""
        print("🔍 Unified Monitoring System - Mac Claude CT-015")
        print("=" * 60)
        
        # Check n8n Health
        print("\n🔧 n8n Instance Status:")
        n8n_health = self.check_n8n_health()
        print(f"  Status: {n8n_health['status']}")
        if 'error' in n8n_health:
            print(f"  Error: {n8n_health['error']}")
        
        # Check n8n Workflows
        print("\n⚙️  n8n Workflows:")
        workflows = self.get_n8n_workflows() or {}
        if workflows and 'error' not in workflows:
            print(f"  Total: {workflows.get('count', 0)}, Active: {workflows.get('active', 0)}")
            for wf in workflows.get('workflows', [])[:3]:
                status = "🟢 Active" if wf.get('active') else "⭕ Inactive"
                print(f"    {status} {wf.get('name', 'Unnamed')}")
        else:
            print(f"  Error: {workflows.get('error', 'Unknown error')}")
        
        # Check Recent Executions
        print("\n📊 Recent n8n Executions:")
        executions = self.get_recent_executions() or {}
        if executions and 'error' not in executions:
            print(f"  Recent executions: {executions.get('total', 0)}")
            for exec in executions.get('recent', [])[:3]:
                status = "✅" if exec.get('finished') else "🔄"
                workflow_name = exec.get('workflowData', {}).get('name', 'Unknown')
                print(f"    {status} {workflow_name}")
        else:
            print(f"  Error: {executions.get('error', 'Unknown error')}")
        
        # Check Google Sheets
        print("\n📋 Google Sheets Status:")
        sheets_status = self.get_sheets_status() or {}
        if sheets_status and 'error' not in sheets_status:
            print(f"  Tasks in progress: {sheets_status['tasks_in_progress']}")
            print(f"  Completed today: {sheets_status['tasks_completed_today']}")
            print(f"  Pending approvals: {sheets_status['pending_approvals']}")
            if sheets_status['last_activity']:
                activity = sheets_status['last_activity']
                print(f"  Last activity: {activity[1]} - {activity[2]}")
        else:
            print(f"  Error: {sheets_status['error']}")
        
        # Update Dashboard
        unified_data = {
            'n8n': n8n_health,
            'workflows': workflows,
            'executions': executions,
            'sheets': sheets_status
        }
        
        dashboard_updated = self.update_monitoring_dashboard(unified_data)
        
        print(f"\n📊 Dashboard Updated: {'✅' if dashboard_updated else '❌'}")
        print("=" * 60)
        print("🎯 Unified monitoring complete!")
        
        return unified_data

def main():
    """Main monitoring function"""
    monitor = UnifiedMonitor()
    result = monitor.run_unified_monitoring()
    
    # Save monitoring data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"/tmp/unified_monitoring_{timestamp}.json"
    
    try:
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        print(f"\n💾 Monitoring data saved: {output_file}")
    except Exception as e:
        print(f"❌ Save error: {e}")

if __name__ == "__main__":
    main()