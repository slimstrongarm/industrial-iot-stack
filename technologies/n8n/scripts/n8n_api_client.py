#!/usr/bin/env python3
"""
n8n API Client for monitoring and controlling workflows
"""

import requests
import json
from datetime import datetime
import os
from typing import Dict, List, Optional

class N8nAPIClient:
    """Client for interacting with n8n REST API"""
    
    def __init__(self, base_url: str, api_key: str = None, username: str = None, password: str = None):
        """
        Initialize n8n API client
        
        Args:
            base_url: n8n instance URL (e.g., http://localhost:5678)
            api_key: API key for authentication (if enabled)
            username: Basic auth username
            password: Basic auth password
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        # Set up authentication
        if api_key:
            self.session.headers['X-N8N-API-KEY'] = api_key
        elif username and password:
            self.session.auth = (username, password)
    
    def test_connection(self) -> bool:
        """Test connection to n8n instance"""
        try:
            response = self.session.get(f"{self.base_url}/healthz")
            return response.status_code == 200
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    # Workflow Operations
    def get_workflows(self) -> List[Dict]:
        """Get all workflows"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/workflows")
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"Error getting workflows: {e}")
            return []
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Get specific workflow by ID"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/workflows/{workflow_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting workflow {workflow_id}: {e}")
            return None
    
    def activate_workflow(self, workflow_id: str) -> bool:
        """Activate a workflow"""
        try:
            response = self.session.patch(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                json={"active": True}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error activating workflow {workflow_id}: {e}")
            return False
    
    def deactivate_workflow(self, workflow_id: str) -> bool:
        """Deactivate a workflow"""
        try:
            response = self.session.patch(
                f"{self.base_url}/api/v1/workflows/{workflow_id}",
                json={"active": False}
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deactivating workflow {workflow_id}: {e}")
            return False
    
    # Execution Operations
    def get_executions(self, workflow_id: str = None, limit: int = 10) -> List[Dict]:
        """Get workflow executions"""
        try:
            params = {"limit": limit}
            if workflow_id:
                params["workflowId"] = workflow_id
            
            response = self.session.get(
                f"{self.base_url}/api/v1/executions",
                params=params
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            print(f"Error getting executions: {e}")
            return []
    
    def execute_workflow(self, workflow_id: str, data: Dict = None) -> Optional[Dict]:
        """Execute a workflow manually"""
        try:
            # Try the webhook-style execution first
            response = self.session.post(
                f"{self.base_url}/webhook/{workflow_id}",
                json=data or {}
            )
            
            if response.status_code == 404:
                # Try the API endpoint
                response = self.session.post(
                    f"{self.base_url}/api/v1/workflows/{workflow_id}/execute",
                    json={"data": data or {}}
                )
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error executing workflow {workflow_id}: {e}")
            return None
    
    # Monitoring Operations
    def get_workflow_status(self) -> Dict:
        """Get status of all workflows"""
        workflows = self.get_workflows()
        status = {
            "total": len(workflows),
            "active": 0,
            "inactive": 0,
            "workflows": []
        }
        
        for workflow in workflows:
            if workflow.get('active'):
                status['active'] += 1
            else:
                status['inactive'] += 1
            
            status['workflows'].append({
                'id': workflow.get('id'),
                'name': workflow.get('name'),
                'active': workflow.get('active'),
                'tags': workflow.get('tags', [])
            })
        
        return status
    
    def monitor_executions(self, interval_seconds: int = 30):
        """Monitor workflow executions in real-time"""
        import time
        
        print(f"🔄 Monitoring n8n executions (every {interval_seconds}s)")
        print("Press Ctrl+C to stop\n")
        
        last_execution_ids = set()
        
        try:
            while True:
                executions = self.get_executions(limit=20)
                current_execution_ids = {ex.get('id') for ex in executions}
                
                # Find new executions
                new_executions = current_execution_ids - last_execution_ids
                
                if new_executions:
                    print(f"\n🚨 {len(new_executions)} NEW EXECUTION(S)!")
                    print("="*60)
                    
                    for execution in executions:
                        if execution.get('id') in new_executions:
                            self._print_execution_details(execution)
                
                last_execution_ids = current_execution_ids
                
                print(f"⏰ Checked at {datetime.now().strftime('%H:%M:%S')} - {len(executions)} recent executions")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n👋 Monitoring stopped")
    
    def _print_execution_details(self, execution: Dict):
        """Print execution details"""
        status_icons = {
            'success': '✅',
            'error': '❌',
            'running': '🔄',
            'waiting': '⏳'
        }
        
        status = execution.get('finished') and 'success' or 'error'
        if not execution.get('stoppedAt'):
            status = 'running'
        
        icon = status_icons.get(status, '❓')
        
        print(f"{icon} Workflow: {execution.get('workflowData', {}).get('name', 'Unknown')}")
        print(f"   ID: {execution.get('id')}")
        print(f"   Started: {execution.get('startedAt')}")
        print(f"   Status: {status}")
        
        if execution.get('data', {}).get('resultData', {}).get('error'):
            print(f"   ❌ Error: {execution['data']['resultData']['error']}")
        
        print()


# Example usage functions
def test_n8n_connection():
    """Test connection to n8n instance"""
    # For local n8n with basic auth
    client = N8nAPIClient(
        base_url="http://localhost:5678",
        username="iiot-admin",
        password="StrongPassword123!"
    )
    
    if client.test_connection():
        print("✅ Successfully connected to n8n!")
        
        # Get workflow status
        status = client.get_workflow_status()
        print(f"\n📊 Workflow Status:")
        print(f"   Total workflows: {status['total']}")
        print(f"   Active: {status['active']}")
        print(f"   Inactive: {status['inactive']}")
        
        # List workflows
        print("\n📋 Workflows:")
        for workflow in status['workflows']:
            icon = "✅" if workflow['active'] else "⏸️"
            print(f"   {icon} {workflow['name']} (ID: {workflow['id']})")
        
        return client
    else:
        print("❌ Could not connect to n8n")
        return None


def trigger_alert_workflow(alert_data: Dict):
    """Trigger the MQTT WhatsApp alert workflow"""
    client = N8nAPIClient(
        base_url="http://localhost:5678",
        username="iiot-admin",
        password="StrongPassword123!"
    )
    
    # Find the MQTT alert workflow
    workflows = client.get_workflows()
    alert_workflow = None
    
    for workflow in workflows:
        if 'mqtt' in workflow.get('name', '').lower() and 'whatsapp' in workflow.get('name', '').lower():
            alert_workflow = workflow
            break
    
    if alert_workflow:
        print(f"🚨 Triggering alert workflow: {alert_workflow['name']}")
        result = client.execute_workflow(alert_workflow['id'], alert_data)
        if result:
            print("✅ Alert workflow triggered successfully!")
        else:
            print("❌ Failed to trigger alert workflow")
    else:
        print("❌ Alert workflow not found")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "monitor":
            client = test_n8n_connection()
            if client:
                client.monitor_executions(30)
        elif sys.argv[1] == "test-alert":
            # Test alert
            alert_data = {
                "alertType": "API Test Alert",
                "equipmentId": "Test_Equipment",
                "severity": "High",
                "message": "This is a test alert from n8n API",
                "timestamp": datetime.now().isoformat(),
                "location": "API Test",
                "value": "100",
                "threshold": "80"
            }
            trigger_alert_workflow(alert_data)
    else:
        test_n8n_connection()