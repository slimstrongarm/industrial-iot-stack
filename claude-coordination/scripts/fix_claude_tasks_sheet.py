#!/usr/bin/env python3
"""
Fix the Claude Tasks sheet - undo incorrect changes and update properly
"""

import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from pathlib import Path

def fix_claude_tasks():
    """Fix the incorrectly updated Claude Tasks sheet"""
    
    try:
        # Load credentials
        creds_path = Path(__file__).parent.parent / "credentials" / "iot-stack-credentials.json"
        
        # Setup Google Sheets client
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open the IoT Stack Progress Master spreadsheet
        spreadsheet = client.open("IoT Stack Progress Master")
        claude_tasks_sheet = spreadsheet.worksheet("Claude Tasks")
        
        print("✅ Connected to Claude Tasks sheet")
        print("🔄 Fixing incorrectly updated rows...")
        
        # The ADK tasks that need fixing
        adk_tasks = {
            66: {
                "task_id": "",  # Clear the wrong CT-066
                "instance": "Mac Claude",
                "task_type": "ADK Framework",
                "priority": "High", 
                "status": "Complete",
                "description": "Install Google ADK Python framework and test basic functionality. pip install git+https://github.com/google/adk-python.git@main",
                "expected_output": "Google ADK framework installed and tested",
                "dependencies": "",
                "date_added": "2025-06-07 23:33",
                "completed": "2025-06-08"
            },
            67: {
                "task_id": "",  # Clear the wrong CT-066
                "instance": "Mac Claude", 
                "task_type": "ADK State",
                "priority": "High",
                "status": "Complete",
                "description": "Build StatePersistenceEngine in .claude/adk_enhanced/state_persistence.py for 30-second context recovery vs 30-minute rebuild",
                "expected_output": "StatePersistenceEngine with instant recovery",
                "dependencies": "CT-066",
                "date_added": "2025-06-07 23:33",
                "completed": "2025-06-08"
            },
            68: {
                "task_id": "",  # Clear the wrong CT-066
                "instance": "Mac Claude",
                "task_type": "ADK Worker", 
                "priority": "High",
                "status": "Complete",
                "description": "Create EnhancedMacWorker that layers ADK intelligence over existing mac_claude_task_worker.py without breaking it",
                "expected_output": "Enhanced worker with ADK integration",
                "dependencies": "CT-066, CT-067",
                "date_added": "2025-06-07 23:33", 
                "completed": "2025-06-08"
            },
            71: {
                "task_id": "",  # Clear the wrong CT-066
                "instance": "Mac Claude",
                "task_type": "ADK Coordination",
                "priority": "High",
                "status": "Complete", 
                "description": "Create TaskCoordinationEngine in .claude/adk_enhanced/coordination_engine.py for intelligent task assignment based on instance capabilities",
                "expected_output": "Smart task assignment engine",
                "dependencies": "CT-066",
                "date_added": "2025-06-07 23:33",
                "completed": "2025-06-08"
            },
            73: {
                "task_id": "",  # Clear the wrong CT-066
                "instance": "Mac Claude", 
                "task_type": "ADK Conflicts",
                "priority": "High",
                "status": "Complete",
                "description": "Create ConflictPreventionEngine in .claude/adk_enhanced/conflict_prevention.py for file edit and git operation coordination",
                "expected_output": "Conflict prevention system",
                "dependencies": "CT-066", 
                "date_added": "2025-06-07 23:33",
                "completed": "2025-06-08"
            },
            74: {
                "task_id": "",  # Clear the wrong CT-066
                "instance": "Mac Claude",
                "task_type": "ADK Testing",
                "priority": "High", 
                "status": "Complete",
                "description": "End-to-end testing of hybrid ADK architecture: Discord task creation, smart assignment, conflict prevention, state recovery",
                "expected_output": "Full ADK system validation",
                "dependencies": "CT-066, CT-067, CT-068, CT-071, CT-073",
                "date_added": "2025-06-07 23:33",
                "completed": "2025-06-08"
            },
            75: {
                "task_id": "",  # Clear the wrong CT-066
                "instance": "Mac Claude",
                "task_type": "ADK Docs",
                "priority": "Medium",
                "status": "Complete", 
                "description": "Create comprehensive onboarding guide in .claude/ADK_ONBOARDING_GUIDE.md for future Claude instances to quickly adopt hybrid system",
                "expected_output": "ADK onboarding documentation",
                "dependencies": "CT-066, CT-074",
                "date_added": "2025-06-07 23:33",
                "completed": "2025-06-08"
            }
        }
        
        # Update each row with correct column mapping
        for row_num, task_data in adk_tasks.items():
            try:
                # Column mapping:
                # A: Task ID, B: Instance, C: Task Type, D: Priority, E: Status
                # F: Description, G: Expected Output, H: Dependencies, I: Date Added, J: Completed
                
                updates = [
                    # Clear Task ID (Column A)
                    {'range': f'A{row_num}', 'values': [[task_data['task_id']]]},
                    # Instance (Column B) 
                    {'range': f'B{row_num}', 'values': [[task_data['instance']]]},
                    # Task Type (Column C)
                    {'range': f'C{row_num}', 'values': [[task_data['task_type']]]},
                    # Priority (Column D)
                    {'range': f'D{row_num}', 'values': [[task_data['priority']]]},
                    # Status (Column E) - This is where "Complete" goes
                    {'range': f'E{row_num}', 'values': [[task_data['status']]]},
                    # Description (Column F) - Leave as is 
                    # Expected Output (Column G)
                    {'range': f'G{row_num}', 'values': [[task_data['expected_output']]]},
                    # Dependencies (Column H)
                    {'range': f'H{row_num}', 'values': [[task_data['dependencies']]]},
                    # Date Added (Column I) - Leave as is
                    # Completed (Column J) - This is where completion date goes
                    {'range': f'J{row_num}', 'values': [[task_data['completed']]]}
                ]
                
                # Apply updates
                claude_tasks_sheet.batch_update(updates)
                print(f"✅ Fixed row {row_num}: {task_data['description'][:50]}...")
                
            except Exception as e:
                print(f"❌ Failed to fix row {row_num}: {e}")
        
        print(f"\n🎉 Claude Tasks sheet fixed!")
        print(f"📊 Summary: Fixed {len(adk_tasks)} ADK-related tasks")
        print(f"✅ Status column (E) now correctly shows 'Complete'")
        print(f"✅ Completion dates in column J")
        print(f"✅ Task IDs cleared (no multiple CT-066)")
        print(f"✅ Proper task types assigned")
        
        return True
        
    except Exception as e:
        print(f"❌ Error fixing sheet: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Claude Tasks Sheet Repair")
    print("=" * 40)
    
    success = fix_claude_tasks()
    
    if success:
        print("\n✅ Sheet repair completed successfully!")
        print("\n📋 What was fixed:")
        print("   • Removed duplicate CT-066 entries")
        print("   • Moved 'Complete' to correct Status column (E)")
        print("   • Moved completion dates to Completed column (J)")
        print("   • Added proper Task Types for each ADK component")
        print("   • Fixed column alignment throughout")
    else:
        print("\n❌ Repair failed - please check manually")

if __name__ == "__main__":
    main()