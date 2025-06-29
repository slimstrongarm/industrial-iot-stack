#!/usr/bin/env python3
"""
MCP-Inspired Task Orchestrator for Google Sheets
Adapted to work with our existing industrial-iot-stack structure
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from google.oauth2 import service_account
from googleapiclient.discovery import build

class TaskOrchestrator:
    """MCP-inspired orchestrator for managing Claude Tasks in Google Sheets"""
    
    def __init__(self):
        self.creds_path = "/home/server/google-sheets-credentials.json"
        self.spreadsheet_id = "1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
        self.service = self._get_sheets_service()
        
        # Our existing schema (not changing it!)
        self.task_schema = {
            "columns": ["Task ID", "Assigned To", "Task Type", "Priority", "Status", 
                       "Description", "Expected Output", "Dependencies", "Date Added", 
                       "Completed", "Notes"],
            "allowed_statuses": ["Not Started", "Pending", "In Progress", "Complete", "Blocked"],
            "allowed_priorities": ["Low", "Medium", "High", "Critical"],
            "task_types": ["Parachute Drop System", "Discord Integration", "Google Sheets Integration",
                          "MQTT System", "Node-RED Development", "Documentation", "Infrastructure"]
        }
        
        # Memory file for tracking operations
        self.memory_file = "/home/server/industrial-iot-stack/technologies/google-sheets/.mcp_memory.json"
        self.memory = self._load_memory()
    
    def _get_sheets_service(self):
        """Initialize Google Sheets API service"""
        creds = service_account.Credentials.from_service_account_file(
            self.creds_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        return build('sheets', 'v4', credentials=creds)
    
    def _load_memory(self) -> Dict:
        """Load operation history from memory file"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {"operations": [], "last_task_id": 100}
    
    def _save_memory(self):
        """Save operation history to memory file"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def _log_operation(self, operation: str, details: Dict, status: str):
        """Log operation to memory"""
        self.memory["operations"].append({
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "details": details,
            "status": status
        })
        # Keep only last 100 operations
        if len(self.memory["operations"]) > 100:
            self.memory["operations"] = self.memory["operations"][-100:]
        self._save_memory()
    
    def _format_response(self, operation: str, status: str, details: str, next_steps: str = "") -> Dict:
        """Format response in MCP style"""
        response = {
            "OPERATION": operation,
            "STATUS": status,
            "DETAILS": details
        }
        if next_steps:
            response["NEXT_STEPS"] = next_steps
        return response
    
    def create_task(self, title: str, task_type: str = "Infrastructure", 
                   priority: str = "Medium", assigned_to: str = "Mac Claude",
                   description: str = "", expected_output: str = "",
                   dependencies: str = "", notes: str = "") -> Dict:
        """Create a new task with auto-generated CT-XXX ID"""
        
        # Get next task ID
        self.memory["last_task_id"] += 1
        task_id = f"CT-{self.memory['last_task_id']:03d}"
        
        # Create task row
        task_data = [[
            task_id,
            assigned_to,
            task_type,
            priority,
            "Not Started",
            description or title,
            expected_output,
            dependencies,
            datetime.now().strftime("%Y-%m-%d"),
            "",  # Completed date (empty)
            notes
        ]]
        
        # Append to sheet
        try:
            body = {'values': task_data}
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="Claude Tasks!A:K",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body=body
            ).execute()
            
            self._log_operation("CREATE_TASK", {
                "task_id": task_id,
                "title": title,
                "task_type": task_type
            }, "success")
            
            return self._format_response(
                "CREATE_TASK",
                "success",
                f"Created task {task_id}: {title}",
                f"View in sheet: https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
            )
            
        except Exception as e:
            self._log_operation("CREATE_TASK", {"error": str(e)}, "failure")
            return self._format_response(
                "CREATE_TASK",
                "failure",
                f"Failed to create task: {str(e)}",
                "Check credentials and sheet permissions"
            )
    
    def find_tasks(self, search_criteria: str, tab_name: str = "Claude Tasks") -> Dict:
        """Find tasks matching search criteria"""
        
        try:
            # Get all tasks
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{tab_name}!A:K"
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return self._format_response(
                    "FIND_TASKS",
                    "success",
                    "No tasks found in sheet",
                    "Create new tasks using create_task()"
                )
            
            # Search through tasks
            headers = values[0]
            matching_tasks = []
            
            for row in values[1:]:
                # Create task dict
                task = {headers[i]: row[i] if i < len(row) else "" 
                       for i in range(len(headers))}
                
                # Search in all fields
                if any(search_criteria.lower() in str(v).lower() 
                      for v in task.values()):
                    matching_tasks.append(task)
            
            self._log_operation("FIND_TASKS", {
                "criteria": search_criteria,
                "found": len(matching_tasks)
            }, "success")
            
            return self._format_response(
                "FIND_TASKS",
                "success",
                f"Found {len(matching_tasks)} matching tasks",
                json.dumps(matching_tasks, indent=2)
            )
            
        except Exception as e:
            self._log_operation("FIND_TASKS", {"error": str(e)}, "failure")
            return self._format_response(
                "FIND_TASKS",
                "failure",
                f"Failed to search tasks: {str(e)}",
                "Check search criteria and try again"
            )
    
    def update_task_status(self, task_id: str, new_status: str) -> Dict:
        """Update task status in Google Sheet"""
        
        if new_status not in self.task_schema["allowed_statuses"]:
            return self._format_response(
                "UPDATE_STATUS",
                "failure",
                f"Invalid status: {new_status}",
                f"Allowed statuses: {', '.join(self.task_schema['allowed_statuses'])}"
            )
        
        try:
            # Get all tasks to find the row number
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range="Claude Tasks!A:K"
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return self._format_response(
                    "UPDATE_STATUS",
                    "failure",
                    "No tasks found in sheet",
                    "Check sheet and try again"
                )
            
            headers = values[0]
            status_col_index = headers.index('Status') if 'Status' in headers else 4
            task_id_col_index = headers.index('Task ID') if 'Task ID' in headers else 0
            
            # Find the task row
            task_row = None
            for i, row in enumerate(values[1:], start=2):  # Start from row 2 (after headers)
                if len(row) > task_id_col_index and row[task_id_col_index] == task_id:
                    task_row = i
                    break
            
            if task_row is None:
                return self._format_response(
                    "UPDATE_STATUS",
                    "failure",
                    f"Task {task_id} not found",
                    "Check task ID and try again"
                )
            
            # Update the status cell
            status_cell = f"Claude Tasks!{chr(65 + status_col_index)}{task_row}"
            update_body = {
                'values': [[new_status]]
            }
            
            self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=status_cell,
                valueInputOption="RAW",
                body=update_body
            ).execute()
            
            # If status is Complete, also update completion date
            if new_status == "Complete":
                completed_col_index = headers.index('Completed') if 'Completed' in headers else 9
                completed_cell = f"Claude Tasks!{chr(65 + completed_col_index)}{task_row}"
                completion_body = {
                    'values': [[datetime.now().strftime("%Y-%m-%d")]]
                }
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=completed_cell,
                    valueInputOption="RAW",
                    body=completion_body
                ).execute()
            
            self._log_operation("UPDATE_STATUS", {
                "task_id": task_id,
                "new_status": new_status,
                "row": task_row
            }, "success")
            
            return self._format_response(
                "UPDATE_STATUS",
                "success",
                f"Updated {task_id} status to {new_status} in row {task_row}",
                "Task status has been updated in Google Sheets"
            )
            
        except Exception as e:
            self._log_operation("UPDATE_STATUS", {"error": str(e)}, "failure")
            return self._format_response(
                "UPDATE_STATUS",
                "failure",
                f"Failed to update status: {str(e)}",
                "Check task ID and try again"
            )
    
    def list_tabs(self) -> Dict:
        """List all tabs in the spreadsheet with task counts"""
        
        try:
            # Get spreadsheet metadata
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            sheets = sheet_metadata.get('sheets', [])
            tab_info = []
            
            for sheet in sheets:
                tab_name = sheet['properties']['title']
                tab_info.append({
                    "name": tab_name,
                    "id": sheet['properties']['sheetId'],
                    "index": sheet['properties']['index']
                })
            
            self._log_operation("LIST_TABS", {
                "count": len(tab_info)
            }, "success")
            
            return self._format_response(
                "LIST_TABS",
                "success",
                f"Found {len(tab_info)} tabs",
                json.dumps(tab_info, indent=2)
            )
            
        except Exception as e:
            return self._format_response(
                "LIST_TABS",
                "failure",
                f"Failed to list tabs: {str(e)}",
                "Check spreadsheet access"
            )
    
    def get_recent_operations(self, count: int = 10) -> Dict:
        """Get recent operations from memory"""
        recent = self.memory["operations"][-count:]
        return self._format_response(
            "GET_HISTORY",
            "success",
            f"Last {len(recent)} operations",
            json.dumps(recent, indent=2)
        )

# Example usage functions
def demo_orchestrator():
    """Demonstrate the orchestrator capabilities"""
    
    orchestrator = TaskOrchestrator()
    
    print("🎯 MCP-Inspired Task Orchestrator Demo")
    print("=" * 50)
    
    # Example 1: Create a task
    print("\n1. Creating a new task...")
    result = orchestrator.create_task(
        title="Implement MCP memory management",
        task_type="Infrastructure",
        priority="Medium",
        description="Add memory persistence to track operations across Claude sessions",
        expected_output="Working memory system that saves operation history"
    )
    print(json.dumps(result, indent=2))
    
    # Example 2: Find tasks
    print("\n2. Finding tasks with 'MCP'...")
    result = orchestrator.find_tasks("MCP")
    print(json.dumps(result, indent=2))
    
    # Example 3: List tabs
    print("\n3. Listing all tabs...")
    result = orchestrator.list_tabs()
    print(json.dumps(result, indent=2))
    
    # Example 4: Show recent operations
    print("\n4. Recent operations...")
    result = orchestrator.get_recent_operations(5)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    # Run the demo
    demo_orchestrator()