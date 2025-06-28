#!/usr/bin/env python3
"""
Add Human Tasks tab to Google Sheets via API
This script adds the Human Tasks tab to the existing IoT Stack Progress Master sheet
"""

import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDENTIALS_FILE = os.path.expanduser('~/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def get_sheets_service():
    """Initialize Google Sheets API service."""
    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        print(f"❌ Error initializing Sheets service: {str(e)}")
        return None

def add_human_tasks_tab(service):
    """Add Human Tasks tab to the spreadsheet."""
    try:
        # Create new sheet
        request_body = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': 'Human Tasks',
                        'gridProperties': {
                            'rowCount': 100,
                            'columnCount': 8,
                            'frozenRowCount': 1
                        }
                    }
                }
            }]
        }
        
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body=request_body
        ).execute()
        
        sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
        print(f"✅ Created Human Tasks tab with ID: {sheet_id}")
        
        # Add headers
        headers = [['Role', 'Task Type', 'Priority', 'Status', 'Assigned To', 'Dependencies', 'Notes', 'Date Added']]
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Human Tasks!A1:H1',
            valueInputOption='USER_ENTERED',
            body={'values': headers}
        ).execute()
        
        # Format headers
        format_requests = [{
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.8},
                        'textFormat': {
                            'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                            'fontSize': 10,
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        }]
        
        # Add data validation
        validation_requests = [
            # Role validation
            {
                'setDataValidation': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': 1
                    },
                    'rule': {
                        'condition': {
                            'type': 'ONE_OF_LIST',
                            'values': [
                                {'userEnteredValue': 'Architect'},
                                {'userEnteredValue': 'Controls Engineer'},
                                {'userEnteredValue': 'Both'}
                            ]
                        },
                        'strict': True,
                        'showCustomUi': True
                    }
                }
            },
            # Task Type validation
            {
                'setDataValidation': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'startColumnIndex': 1,
                        'endColumnIndex': 2
                    },
                    'rule': {
                        'condition': {
                            'type': 'ONE_OF_LIST',
                            'values': [
                                {'userEnteredValue': 'Architecture'},
                                {'userEnteredValue': 'Ignition Screens'},
                                {'userEnteredValue': 'PLC Logic'},
                                {'userEnteredValue': 'Docker Setup'},
                                {'userEnteredValue': 'Testing'},
                                {'userEnteredValue': 'Documentation'}
                            ]
                        },
                        'strict': True,
                        'showCustomUi': True
                    }
                }
            },
            # Priority validation
            {
                'setDataValidation': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'startColumnIndex': 2,
                        'endColumnIndex': 3
                    },
                    'rule': {
                        'condition': {
                            'type': 'ONE_OF_LIST',
                            'values': [
                                {'userEnteredValue': 'High'},
                                {'userEnteredValue': 'Medium'},
                                {'userEnteredValue': 'Low'}
                            ]
                        },
                        'strict': True,
                        'showCustomUi': True
                    }
                }
            },
            # Status validation
            {
                'setDataValidation': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': 1,
                        'startColumnIndex': 3,
                        'endColumnIndex': 4
                    },
                    'rule': {
                        'condition': {
                            'type': 'ONE_OF_LIST',
                            'values': [
                                {'userEnteredValue': 'Pending'},
                                {'userEnteredValue': 'In Progress'},
                                {'userEnteredValue': 'Complete'},
                                {'userEnteredValue': 'On Hold'}
                            ]
                        },
                        'strict': True,
                        'showCustomUi': True
                    }
                }
            }
        ]
        
        # Set column widths
        dimension_requests = [
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1}, 'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2}, 'properties': {'pixelSize': 150}, 'fields': 'pixelSize'}},
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3}, 'properties': {'pixelSize': 80}, 'fields': 'pixelSize'}},
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4}, 'properties': {'pixelSize': 100}, 'fields': 'pixelSize'}},
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 5}, 'properties': {'pixelSize': 150}, 'fields': 'pixelSize'}},
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 5, 'endIndex': 6}, 'properties': {'pixelSize': 200}, 'fields': 'pixelSize'}},
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 6, 'endIndex': 7}, 'properties': {'pixelSize': 300}, 'fields': 'pixelSize'}},
            {'updateDimensionProperties': {'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': 7, 'endIndex': 8}, 'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}}
        ]
        
        # Apply all formatting
        all_requests = format_requests + validation_requests + dimension_requests
        
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={'requests': all_requests}
        ).execute()
        
        print("✅ Applied formatting and validation")
        
        # Add sample data
        sample_data = [
            ['Architect', 'Architecture', 'High', 'Pending', 'You', '-', 'Finalize Docker deployment strategy and module selection for Customer A', '2025-06-01'],
            ['Controls Engineer', 'PLC Logic', 'High', 'Pending', 'Controls Engineer', 'Docker Setup Complete', 'Implement failover logic for critical brewery systems', '2025-06-01'],
            ['Both', 'Testing', 'Medium', 'Pending', 'Team', 'Architecture design complete', 'Integration testing between PLC and Ignition Docker containers', '2025-06-01'],
            ['Architect', 'Architecture', 'Medium', 'In Progress', 'You', '-', 'Design Controls Engineer onboarding workflow for Docker/server access', '2025-06-01'],
            ['Architect', 'Docker Setup', 'High', 'Pending', 'You', 'Tailscale connection established', 'Deploy Docker containers to POC server', '2025-06-01'],
            ['Controls Engineer', 'Ignition Screens', 'Medium', 'Pending', 'Controls Engineer', '-', 'Create HMI screens for brewery equipment monitoring', '2025-06-01']
        ]
        
        service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range='Human Tasks!A2:H7',
            valueInputOption='USER_ENTERED',
            body={'values': sample_data}
        ).execute()
        
        print("✅ Added sample human tasks")
        
        # Add conditional formatting for Status column
        conditional_format_requests = [
            {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{
                            'sheetId': sheet_id,
                            'startRowIndex': 1,
                            'startColumnIndex': 3,
                            'endColumnIndex': 4
                        }],
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_EQ',
                                'values': [{'userEnteredValue': 'Pending'}]
                            },
                            'format': {
                                'backgroundColor': {'red': 0.988, 'green': 0.894, 'blue': 0.925}
                            }
                        }
                    }
                }
            },
            {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{
                            'sheetId': sheet_id,
                            'startRowIndex': 1,
                            'startColumnIndex': 3,
                            'endColumnIndex': 4
                        }],
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_EQ',
                                'values': [{'userEnteredValue': 'In Progress'}]
                            },
                            'format': {
                                'backgroundColor': {'red': 1.0, 'green': 0.953, 'blue': 0.804}
                            }
                        }
                    }
                }
            },
            {
                'addConditionalFormatRule': {
                    'rule': {
                        'ranges': [{
                            'sheetId': sheet_id,
                            'startRowIndex': 1,
                            'startColumnIndex': 3,
                            'endColumnIndex': 4
                        }],
                        'booleanRule': {
                            'condition': {
                                'type': 'TEXT_EQ',
                                'values': [{'userEnteredValue': 'Complete'}]
                            },
                            'format': {
                                'backgroundColor': {'red': 0.831, 'green': 0.929, 'blue': 0.855}
                            }
                        }
                    }
                }
            }
        ]
        
        # Apply conditional formatting
        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={'requests': conditional_format_requests}
        ).execute()
        
        print("✅ Applied conditional formatting")
        
        return True
        
    except HttpError as e:
        if 'already exists' in str(e):
            print("⚠️ Human Tasks tab already exists")
            return True
        else:
            print(f"❌ Error creating Human Tasks tab: {str(e)}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def main():
    """Main function to add Human Tasks tab."""
    print("🚀 Adding Human Tasks tab to Google Sheets...")
    
    service = get_sheets_service()
    if not service:
        return
    
    if add_human_tasks_tab(service):
        print("\n✅ Successfully added Human Tasks tab!")
        print(f"📊 View it at: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0")
        print("\nThe tab includes:")
        print("  - Role-based task tracking (Architect, Controls Engineer, Both)")
        print("  - Task types for different work areas")
        print("  - Priority and status tracking with color coding")
        print("  - Sample tasks to get you started")
    else:
        print("\n❌ Failed to add Human Tasks tab")

if __name__ == "__main__":
    main()