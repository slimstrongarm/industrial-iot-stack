#!/usr/bin/env python3
"""
Setup Form Submissions and Form Errors tabs in Google Sheets
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def setup_form_tabs():
    """Create Form Submissions and Form Errors tabs"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        print("📝 Setting up Form Submission tabs...")
        
        # 1. Create Form Submissions tab
        try:
            form_sheet = sheet.add_worksheet(title="Form Submissions", rows=1000, cols=20)
        except:
            form_sheet = sheet.worksheet("Form Submissions")
            form_sheet.clear()
            
        # Set headers for form submissions
        headers = [
            'Timestamp', 'Submission ID', 'Form Name', 'Equipment ID', 
            'Operator', 'Shift', 'Issue Type', 'Severity', 
            'Description', 'Location', 'Action Taken', 'Follow Up Required',
            'Source', 'Status'
        ]
        
        form_sheet.update(values=[headers], range_name='A1:N1')
        
        # Format headers
        form_sheet.format('A1:N1', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.2, 'green': 0.5, 'blue': 0.8},
            'horizontalAlignment': 'CENTER'
        })
        
        # 2. Create Form Errors tab
        try:
            error_sheet = sheet.add_worksheet(title="Form Errors", rows=1000, cols=10)
        except:
            error_sheet = sheet.worksheet("Form Errors")
            error_sheet.clear()
            
        # Set headers for errors
        error_headers = [
            'Timestamp', 'Error Message', 'Error Type', 
            'Node', 'Form Data', 'Status'
        ]
        
        error_sheet.update(values=[error_headers], range_name='A1:F1')
        
        # Format error headers
        error_sheet.format('A1:F1', {
            'textFormat': {'bold': True},
            'backgroundColor': {'red': 0.8, 'green': 0.2, 'blue': 0.2},
            'horizontalAlignment': 'CENTER'
        })
        
        # 3. Add sample industrial form data
        sample_data = [
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "DEMO-001",
                "Equipment Inspection",
                "PUMP-01",
                "John Smith",
                "Day Shift",
                "Mechanical Issue",
                "Medium",
                "Unusual vibration detected during routine inspection",
                "Brewhouse Level 2",
                "Scheduled maintenance for next shift",
                "Yes",
                "Demo Form",
                "New"
            ]
        ]
        
        form_sheet.update(values=sample_data, range_name='A2:N2')
        
        # Freeze header row
        form_sheet.freeze(rows=1)
        error_sheet.freeze(rows=1)
        
        print("✅ Form Submissions tab created")
        print("✅ Form Errors tab created")
        print(f"\n📊 Webhook URL for n8n:")
        print("https://your-n8n-instance.com/webhook/formbricks-form-webhook")
        print("\n🔗 Google Sheets ID already in workflow:")
        print(SHEET_ID)
        print("\n📋 Next Steps:")
        print("1. Import the workflow JSON into n8n")
        print("2. Set up Google Sheets credentials in n8n")
        print("3. Activate the workflow")
        print("4. Configure Formbricks webhook to point to n8n")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_form_tabs()