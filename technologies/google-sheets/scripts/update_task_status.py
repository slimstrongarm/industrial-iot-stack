#!/usr/bin/env python3
"""
Properly update task status in Google Sheets
"""

import sys
from datetime import datetime
from mcp_task_orchestrator import TaskOrchestrator

def update_ct101_to_in_progress():
    """Update CT-101 specifically to In Progress"""
    
    orchestrator = TaskOrchestrator()
    
    try:
        # Get all tasks to find CT-101 row
        result = orchestrator.service.spreadsheets().values().get(
            spreadsheetId=orchestrator.spreadsheet_id,
            range="Claude Tasks!A:K"
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print("❌ No tasks found in sheet")
            return
        
        headers = values[0]
        status_col_index = headers.index('Status') if 'Status' in headers else 4  # Column E (0-indexed)
        task_id_col_index = headers.index('Task ID') if 'Task ID' in headers else 0  # Column A
        
        # Find CT-101 row
        ct101_row = None
        for i, row in enumerate(values[1:], start=2):  # Start from row 2 (1-indexed)
            if len(row) > task_id_col_index and row[task_id_col_index] == 'CT-101':
                ct101_row = i
                break
        
        if not ct101_row:
            print("❌ CT-101 not found in sheet")
            return
        
        # Update the status cell directly
        range_name = f"Claude Tasks!{chr(65 + status_col_index)}{ct101_row}"  # Convert to A1 notation
        
        body = {
            'values': [['In Progress']]
        }
        
        update_result = orchestrator.service.spreadsheets().values().update(
            spreadsheetId=orchestrator.spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        
        print(f"✅ Successfully updated CT-101 status to 'In Progress'")
        print(f"📊 Updated range: {range_name}")
        print(f"🔢 Cells updated: {update_result.get('updatedCells', 0)}")
        
        # Log the operation
        orchestrator._log_operation("UPDATE_STATUS_DIRECT", {
            "task_id": "CT-101",
            "new_status": "In Progress",
            "range": range_name,
            "row": ct101_row
        }, "success")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating status: {e}")
        
        # Log the error
        orchestrator._log_operation("UPDATE_STATUS_DIRECT", {
            "task_id": "CT-101",
            "error": str(e)
        }, "failure")
        
        return False

def update_task_status_by_id(task_id: str, new_status: str):
    """Update any task status by ID"""
    
    orchestrator = TaskOrchestrator()
    
    try:
        # Get all tasks
        result = orchestrator.service.spreadsheets().values().get(
            spreadsheetId=orchestrator.spreadsheet_id,
            range="Claude Tasks!A:K"
        ).execute()
        
        values = result.get('values', [])
        if not values:
            print("❌ No tasks found in sheet")
            return False
        
        headers = values[0]
        status_col_index = headers.index('Status') if 'Status' in headers else 4
        task_id_col_index = headers.index('Task ID') if 'Task ID' in headers else 0
        completed_col_index = headers.index('Completed') if 'Completed' in headers else 9
        
        # Find task row
        task_row = None
        for i, row in enumerate(values[1:], start=2):
            if len(row) > task_id_col_index and row[task_id_col_index] == task_id:
                task_row = i
                break
        
        if not task_row:
            print(f"❌ {task_id} not found in sheet")
            return False
        
        # Prepare updates
        updates = []
        
        # Update status
        status_range = f"Claude Tasks!{chr(65 + status_col_index)}{task_row}"
        updates.append({
            'range': status_range,
            'values': [[new_status]]
        })
        
        # If completing task, add completion date
        if new_status == "Complete":
            completed_range = f"Claude Tasks!{chr(65 + completed_col_index)}{task_row}"
            updates.append({
                'range': completed_range,
                'values': [[datetime.now().strftime("%Y-%m-%d")]]
            })
        
        # Batch update
        body = {
            'valueInputOption': 'RAW',
            'data': updates
        }
        
        update_result = orchestrator.service.spreadsheets().values().batchUpdate(
            spreadsheetId=orchestrator.spreadsheet_id,
            body=body
        ).execute()
        
        print(f"✅ Successfully updated {task_id} status to '{new_status}'")
        print(f"🔢 Cells updated: {update_result.get('totalUpdatedCells', 0)}")
        
        # Log the operation
        orchestrator._log_operation("UPDATE_STATUS_BATCH", {
            "task_id": task_id,
            "new_status": new_status,
            "updates": len(updates)
        }, "success")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating {task_id}: {e}")
        orchestrator._log_operation("UPDATE_STATUS_BATCH", {
            "task_id": task_id,
            "error": str(e)
        }, "failure")
        return False

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Default: Update CT-101 to In Progress
        print("🔄 Updating CT-101 to 'In Progress'...")
        update_ct101_to_in_progress()
    elif len(sys.argv) == 3:
        # Update specific task: python update_task_status.py CT-101 "Complete"
        task_id = sys.argv[1]
        new_status = sys.argv[2]
        print(f"🔄 Updating {task_id} to '{new_status}'...")
        update_task_status_by_id(task_id, new_status)
    else:
        print("Usage:")
        print("  python3 update_task_status.py                    # Update CT-101 to In Progress")
        print("  python3 update_task_status.py CT-101 'Complete'  # Update specific task")