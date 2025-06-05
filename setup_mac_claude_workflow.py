#!/usr/bin/env python3
"""
Script to create Mac Claude Workflow tab in Google Sheets
Sets up a structured workflow with checkboxes and status tracking
"""

import gspread
from google.oauth2.service_account import Credentials
import json

def setup_mac_claude_workflow():
    """Connect to Google Sheets and create Mac Claude workflow tab"""
    
    # Define the scope
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    # Load credentials
    credentials_path = '/home/server/google-sheets-credentials.json'
    credentials = Credentials.from_service_account_file(credentials_path, scopes=scopes)
    
    # Initialize the client
    gc = gspread.authorize(credentials)
    
    # Open the spreadsheet
    spreadsheet_id = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
    spreadsheet = gc.open_by_key(spreadsheet_id)
    
    # Create new worksheet
    try:
        worksheet = spreadsheet.add_worksheet(title="Mac Claude Workflow", rows="50", cols="8")
        print("✅ Created new 'Mac Claude Workflow' tab")
    except gspread.exceptions.APIError as e:
        if "already exists" in str(e):
            print("⚠️  Tab 'Mac Claude Workflow' already exists, updating it...")
            worksheet = spreadsheet.worksheet("Mac Claude Workflow")
        else:
            raise e
    
    # Clear existing content
    worksheet.clear()
    
    # Define headers
    headers = [
        "Step #",
        "Task Description", 
        "Time Est.",
        "Status",
        "Priority",
        "Dependencies",
        "Notes/Details",
        "Completion Date"
    ]
    
    # Define workflow steps
    workflow_steps = [
        {
            "step": "1",
            "task": "Repository Access Test",
            "time": "5 min",
            "status": "Pending",
            "priority": "High",
            "dependencies": "None",
            "notes": "Test git clone and basic file access to industrial-iot-stack repository",
            "completion": ""
        },
        {
            "step": "2", 
            "task": "Environment Setup Verification",
            "time": "10 min",
            "status": "Pending",
            "priority": "High",
            "dependencies": "Step 1",
            "notes": "Verify Python, Node.js, Docker, and other required tools are installed",
            "completion": ""
        },
        {
            "step": "3",
            "task": "n8n API Connectivity Test",
            "time": "15 min", 
            "status": "Pending",
            "priority": "High",
            "dependencies": "Steps 1-2",
            "notes": "Test connection to n8n instance and basic API functionality",
            "completion": ""
        },
        {
            "step": "4",
            "task": "HT-002: Discord Webhooks Implementation",
            "time": "45 min",
            "status": "Pending", 
            "priority": "Medium",
            "dependencies": "Step 3",
            "notes": "Set up Discord webhook integration for notifications and alerts",
            "completion": ""
        },
        {
            "step": "5",
            "task": "HT-003: Google Sheets Credentials Setup",
            "time": "30 min",
            "status": "Pending",
            "priority": "Medium", 
            "dependencies": "Steps 1-3",
            "notes": "Configure Google Sheets API access and test basic read/write operations",
            "completion": ""
        },
        {
            "step": "6",
            "task": "HT-006: Formbricks API Key Configuration",
            "time": "20 min",
            "status": "Pending",
            "priority": "Medium",
            "dependencies": "Steps 1-3",
            "notes": "Set up Formbricks API integration for form/survey functionality",
            "completion": ""
        },
        {
            "step": "7",
            "task": "Integration Testing - Basic Workflows",
            "time": "60 min",
            "status": "Pending",
            "priority": "High",
            "dependencies": "Steps 4-6",
            "notes": "Test end-to-end integration between all configured services",
            "completion": ""
        },
        {
            "step": "8",
            "task": "Coordination with Server Claude",
            "time": "30 min",
            "status": "Pending",
            "priority": "High", 
            "dependencies": "Step 7",
            "notes": "Establish communication protocols and sync workflow status",
            "completion": ""
        },
        {
            "step": "9",
            "task": "Documentation Review & Updates",
            "time": "45 min",
            "status": "Pending",
            "priority": "Low",
            "dependencies": "Steps 1-8",
            "notes": "Review and update any documentation based on setup experience",
            "completion": ""
        },
        {
            "step": "10",
            "task": "Final Validation & Sign-off",
            "time": "30 min",
            "status": "Pending",
            "priority": "High",
            "dependencies": "Steps 1-9", 
            "notes": "Complete final testing and mark setup as complete",
            "completion": ""
        }
    ]
    
    # Write headers
    worksheet.update([headers], 'A1:H1')
    
    # Write workflow steps
    for i, step in enumerate(workflow_steps, start=2):
        row_data = [
            step["step"],
            step["task"],
            step["time"],
            step["status"], 
            step["priority"],
            step["dependencies"],
            step["notes"],
            step["completion"]
        ]
        worksheet.update([row_data], f'A{i}:H{i}')
    
    # Format the worksheet
    print("🎨 Applying formatting...")
    
    # Header formatting
    worksheet.format('A1:H1', {
        'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}},
        'horizontalAlignment': 'CENTER'
    })
    
    # Status column conditional formatting
    # High priority rows
    high_priority_rows = [i+2 for i, step in enumerate(workflow_steps) if step["priority"] == "High"]
    for row in high_priority_rows:
        worksheet.format(f'E{row}', {
            'backgroundColor': {'red': 1, 'green': 0.8, 'blue': 0.8},
            'textFormat': {'bold': True}
        })
    
    # Set column widths using batch_update
    requests = []
    column_widths = [
        (0, 80),   # Step #
        (1, 300),  # Task Description  
        (2, 80),   # Time Est.
        (3, 120),  # Status
        (4, 100),  # Priority
        (5, 150),  # Dependencies
        (6, 400),  # Notes/Details
        (7, 120)   # Completion Date
    ]
    
    for col_index, width in column_widths:
        requests.append({
            "updateDimensionProperties": {
                "range": {
                    "sheetId": worksheet.id,
                    "dimension": "COLUMNS",
                    "startIndex": col_index,
                    "endIndex": col_index + 1
                },
                "properties": {
                    "pixelSize": width
                },
                "fields": "pixelSize"
            }
        })
    
    # Apply column width changes
    spreadsheet.batch_update({"requests": requests})
    
    # Add data validation for Status column
    print("📋 Adding data validation...")
    worksheet.format('D2:D11', {
        'dataValidation': {
            'condition': {
                'type': 'ONE_OF_LIST',
                'values': ['Pending', 'In Progress', 'Complete', 'Blocked']
            },
            'strict': True,
            'showCustomUi': True
        }
    })
    
    # Add data validation for Priority column  
    worksheet.format('E2:E11', {
        'dataValidation': {
            'condition': {
                'type': 'ONE_OF_LIST', 
                'values': ['High', 'Medium', 'Low']
            },
            'strict': True,
            'showCustomUi': True
        }
    })
    
    # Add summary section
    print("📊 Adding summary section...")
    worksheet.update([['WORKFLOW SUMMARY']], 'A13')
    worksheet.format('A13', {
        'textFormat': {'bold': True, 'fontSize': 14},
        'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
    })
    
    # Add summary formulas
    summary_data = [
        ['Total Steps:', '=COUNTA(A2:A11)'],
        ['Completed:', '=COUNTIF(D2:D11,"Complete")'],
        ['In Progress:', '=COUNTIF(D2:D11,"In Progress")'],
        ['Pending:', '=COUNTIF(D2:D11,"Pending")'],
        ['Blocked:', '=COUNTIF(D2:D11,"Blocked")'],
        ['Total Est. Time:', '=SUMPRODUCT(--(D2:D11<>"Complete"),1) & " tasks remaining"'],
        ['Progress:', '=ROUND(COUNTIF(D2:D11,"Complete")/COUNTA(A2:A11)*100,1) & "%"']
    ]
    
    for i, row in enumerate(summary_data, start=14):
        worksheet.update(f'A{i}:B{i}', [row])
    
    # Format summary section
    worksheet.format('A14:A20', {'textFormat': {'bold': True}})
    worksheet.format('B14:B20', {'horizontalAlignment': 'LEFT'})
    
    # Add instructions section
    print("📝 Adding instructions...")
    worksheet.update('A22', [['INSTRUCTIONS FOR MAC CLAUDE']])
    worksheet.format('A22', {
        'textFormat': {'bold': True, 'fontSize': 14},
        'backgroundColor': {'red': 0.8, 'green': 0.9, 'blue': 0.8}
    })
    
    instructions = [
        ['1. Work through steps sequentially in order'],
        ['2. Update Status column as you progress (Pending → In Progress → Complete)'],
        ['3. Add notes in the Notes/Details column as you work'],
        ['4. Mark completion date when finished with each step'],
        ['5. Check dependencies before starting each step'],
        ['6. Prioritize High priority items first'],
        ['7. Coordinate with Server Claude for steps requiring collaboration'],
        ['8. Update this sheet regularly to track progress']
    ]
    
    for i, instruction in enumerate(instructions, start=23):
        worksheet.update(f'A{i}:G{i}', [instruction])
    
    print("✅ Mac Claude Workflow tab setup complete!")
    print(f"📊 Spreadsheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")
    print("🎯 Mac Claude can now follow the structured workflow to get up to speed")
    
    return worksheet

if __name__ == "__main__":
    setup_mac_claude_workflow()