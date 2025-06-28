#!/usr/bin/env python3
"""
Update Google Sheets Claude Tasks with today's progress
Requires: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

import os
from datetime import datetime

# Google Sheets configuration
SPREADSHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
RANGE_NAME = 'Claude Tasks!A:H'  # Adjust if sheet name is different

def update_claude_tasks():
    """Update Google Sheets with new Claude tasks"""
    
    # Tasks to append (starting from row 39 based on the image)
    new_rows = [
        ["CT-039", "Mac Claude", "Node-RED Cleanup", "High", "Complete", 
         "Clean Node-RED UI from 33 flows to 8-10 essential flows for production readiness", 
         "Consolidated flows, removed test/debug flows, 71% reduction achieved", "CT-038"],
        
        ["CT-040", "Mac Claude", "UI Restoration", "High", "Complete",
         "Restore Integration tab with protocol status table and test buttons",
         "Working Integration tab with real-time protocol monitoring", "CT-039"],
        
        ["CT-041", "Mac Claude", "Connection Test", "High", "Complete",
         "Validate OPC UA connection between Node-RED and Ignition Edge",
         "Confirmed working OPC connection on port 62541", "CT-040"],
        
        ["CT-042", "Mac Claude", "Integration Test", "High", "Pending",
         "Test end-to-end data flow: MQTT → Node-RED → Ignition with real data",
         "Data flows from MQTT through to Ignition tags successfully", "CT-041"],
        
        ["CT-043", "Mac Claude", "MQTT Setup", "Medium", "Blocked",
         "Configure Steel Bonnet production MQTT broker connection",
         "Connected to Steel Bonnet's production MQTT broker", "Need broker address"],
        
        ["CT-044", "Mac Claude", "Brewery Testing", "High", "Pending",
         "Test with real brewery sensor data (HLT heat system, chillers, etc.)",
         "Real brewery data visible in Ignition through Node-RED", "CT-042"]
    ]
    
    print("📝 NEW TASKS TO ADD TO GOOGLE SHEETS:")
    print("=" * 60)
    for row in new_rows:
        print(f"{row[0]} | {row[3]:6} | {row[4]:10} | {row[5][:50]}...")
    
    print("\n✏️ ALSO UPDATE:")
    print("CT-035 → Change Status from 'Pending' to 'Complete'")
    
    print("\n🔗 Google Sheets URL:")
    print(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
    
    print("\n⚠️  TO ENABLE API ACCESS:")
    print("1. Go to https://console.cloud.google.com/")
    print("2. Enable Google Sheets API")
    print("3. Create credentials (OAuth 2.0 or Service Account)")
    print("4. Download credentials.json")
    print("5. Run: pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")

if __name__ == "__main__":
    update_claude_tasks()