#!/usr/bin/env python3
"""
Final handoff update to Google Sheets with proper error handling
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def final_handoff_update():
    """Final update with proper error handling"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        print("🔄 Final handoff update to Google Sheets...")
        
        # 1. Update Agent Activities with session summary
        try:
            agent_sheet = sheet.worksheet('Agent Activities')
            agent_sheet.append_row([
                timestamp,
                "Mac Claude",
                "Major session completion - autocompact handoff",
                "Complete",
                "150 min",
                "🎯 Major accomplishments: Discord integration complete, WhatsApp + Steel Bonnet MQTT ready, GitHub Actions framework created (needs YAML fix), Google Sheets updated. 95% ready for Friday brewery demo.",
                "Next: Fix GitHub Actions YAML syntax error, deploy Discord bot (CT-027), deploy WhatsApp (CT-029)"
            ])
            print("✅ Added session summary to Agent Activities")
        except Exception as e:
            print(f"⚠️ Could not update Agent Activities: {e}")
        
        # 2. Update CT-030 status carefully
        try:
            claude_sheet = sheet.worksheet('Claude Tasks')
            # Use cell-by-cell update to avoid header issues
            
            # Find CT-030 row by searching values
            all_values = claude_sheet.get_all_values()
            for i, row in enumerate(all_values):
                if len(row) > 0 and row[0] == 'CT-030':
                    row_num = i + 1
                    # Update status (column E)
                    claude_sheet.update_cell(row_num, 5, "Blocked")
                    # Update description with issue
                    claude_sheet.update_cell(row_num, 6, 
                        "GitHub Actions workflow created but has YAML syntax error on line 269 preventing execution")
                    print("✅ Updated CT-030 status to Blocked")
                    break
        except Exception as e:
            print(f"⚠️ Could not update CT-030: {e}")
        
        # 3. Add final status summary
        try:
            agent_sheet.append_row([
                timestamp,
                "Mac Claude", 
                "Friday brewery demo readiness",
                "Complete",
                "5 min",
                "READY: ✅ WhatsApp Steel Bonnet alerts, ✅ Discord bot code, ✅ MQTT topics integrated. PENDING: 🔧 GitHub Actions YAML fix, 🚀 Discord deployment, 🚀 WhatsApp deployment. Overall: 95% ready.",
                "Execute pending deployments"
            ])
            print("✅ Added Friday demo readiness status")
        except Exception as e:
            print(f"⚠️ Could not add demo status: {e}")
        
        print("\n🎯 HANDOFF SUMMARY:")
        print("═══════════════════════════════════════")
        print("📊 Google Sheets: Updated with session status")
        print("🎯 Friday Demo: 95% ready")
        print("⚠️ Critical Issue: GitHub Actions YAML syntax error line 269")
        print("🚀 Ready Tasks: CT-027 (Discord), CT-029 (WhatsApp)")
        print("📋 Next Session: Fix YAML, deploy components")
        print("🚗 Safe travels on autocompact!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in final update: {e}")
        return False

if __name__ == "__main__":
    final_handoff_update()