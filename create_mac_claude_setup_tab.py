#!/usr/bin/env python3
"""
Create Mac Claude Bot Setup Tab in Google Sheets
Complete setup instructions and scripts for auto-starting Mac Claude bot
"""

import gspread
from google.oauth2.service_account import Credentials

def create_mac_claude_setup_tab():
    try:
        # Setup credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = Credentials.from_service_account_file(
            'credentials/iot-stack-credentials.json', 
            scopes=scope
        )
        
        # Connect to Google Sheets
        gc = gspread.authorize(credentials)
        sheet = gc.open_by_key('1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do')
        
        # Check if tab already exists
        try:
            worksheet = sheet.worksheet('Mac Claude Bot Setup')
            print("📋 Tab 'Mac Claude Bot Setup' already exists. Updating...")
        except:
            worksheet = sheet.add_worksheet(title='Mac Claude Bot Setup', rows=100, cols=10)
            print("✅ Created new tab 'Mac Claude Bot Setup'")
        
        # Clear existing content
        worksheet.clear()
        
        # Setup data
        setup_data = [
            ['Mac Claude Discord Bot Setup & Auto-Start Guide'],
            [''],
            ['🎯 Purpose'],
            ['Enable Mac Claude to automatically process tasks assigned via Discord'],
            ['Auto-start bot when computer boots up'],
            ['Coordinate with Server Claude for distributed task processing'],
            [''],
            ['📋 Quick Setup Commands (Copy & Paste)'],
            [''],
            ['Step 1: Navigate to Project'],
            ['cd ~/Desktop/industrial-iot-stack'],
            [''],
            ['Step 2: Make Scripts Executable'],
            ['chmod +x setup_mac_claude_autostart.sh mac_claude_bot_status.sh'],
            [''],
            ['Step 3: Run Setup Script'],
            ['./setup_mac_claude_autostart.sh'],
            [''],
            ['Step 4: Enable Auto-Start'],
            ['launchctl load ~/Library/LaunchAgents/com.industrial-iot.mac-claude-bot.plist'],
            [''],
            ['Step 5: Start Bot Immediately'],
            ['~/start_mac_claude_bot.sh'],
            [''],
            ['Step 6: Check Status'],
            ['./mac_claude_bot_status.sh'],
            [''],
            ['🚀 Alternative: Quick Test Start'],
            ['cd ~/Desktop/industrial-iot-stack/discord-bot'],
            ['python3 run_mac_claude_bot.py'],
            [''],
            ['📊 Bot Management Commands'],
            [''],
            ['Check if running:'],
            ['ps aux | grep industrial_iot_claude_bot'],
            [''],
            ['View logs:'],
            ['tail -f ~/mac_claude_bot.log'],
            [''],
            ['Stop bot:'],
            ['kill $(cat ~/mac_claude_bot.pid)'],
            [''],
            ['Restart bot:'],
            ['~/start_mac_claude_bot.sh'],
            [''],
            ['Disable auto-start:'],
            ['launchctl unload ~/Library/LaunchAgents/com.industrial-iot.mac-claude-bot.plist'],
            [''],
            ['🤖 How Task Processing Works'],
            [''],
            ['1. Discord Command:'],
            ['@Mac Claude Bot start task CT-XXX'],
            [''],
            ['2. Bot Response:'],
            ['- Finds task in Google Sheets'],
            ['- Updates status to "In Progress"'],
            ['- Assigns to Mac Claude'],
            ['- Processes task locally'],
            [''],
            ['3. Task Completion:'],
            ['- Updates Google Sheets with results'],
            ['- Sends Discord confirmation'],
            ['- Ready for next task'],
            [''],
            ['🏗️ System Architecture'],
            [''],
            ['Mac Claude Bot (Local):'],
            ['- Development tasks'],
            ['- File operations'],
            ['- Script execution'],
            ['- Google Sheets coordination'],
            [''],
            ['Server Claude Bot (Remote):'],
            ['- 24/7 operations'],
            ['- Docker management'],
            ['- Production deployments'],
            ['- System monitoring'],
            [''],
            ['IIOT Bot (Remote):'],
            ['- Industrial IoT monitoring'],
            ['- MQTT broker status'],
            ['- Node-RED coordination'],
            ['- System health alerts'],
            [''],
            ['📱 Mobile Workflow'],
            [''],
            ['1. Create Task (Discord Mobile):'],
            ['@Mac Claude Bot add task Build new feature'],
            [''],
            ['2. Assign Task (Discord Mobile):'],
            ['@Mac Claude Bot start task CT-105'],
            [''],
            ['3. Monitor Progress (Google Sheets):'],
            ['Task status updates automatically'],
            ['View results and outputs'],
            [''],
            ['✅ Benefits'],
            [''],
            ['- Automatic task processing'],
            ['- Mobile coordination via Discord'],
            ['- Distributed workload (Mac + Server)'],
            ['- Always-on availability'],
            ['- Centralized tracking in Google Sheets'],
            ['- Cross-platform compatibility'],
            [''],
            ['⚠️ Troubleshooting'],
            [''],
            ['Bot won\'t start:'],
            ['- Check Python path: which python3'],
            ['- Check bot file exists: ls discord-bot/run_mac_claude_bot.py'],
            ['- Check credentials: ls credentials/iot-stack-credentials.json'],
            [''],
            ['Bot stops running:'],
            ['- Check logs: tail ~/mac_claude_bot.log'],
            ['- Restart: ~/start_mac_claude_bot.sh'],
            ['- Check auto-start: launchctl list | grep mac-claude'],
            [''],
            ['Google Sheets errors:'],
            ['- Check credentials file'],
            ['- Test connection: python3 -c "import gspread; print(\'OK\')"'],
            ['- Check internet connection'],
            [''],
            ['Discord connection issues:'],
            ['- Check Discord token in run_mac_claude_bot.py'],
            ['- Verify bot permissions in Discord server'],
            ['- Check network connectivity'],
            [''],
            ['🔧 Advanced Configuration'],
            [''],
            ['Custom Install Location:'],
            ['Edit ~/start_mac_claude_bot.sh'],
            ['Update project path as needed'],
            [''],
            ['Custom Log Location:'],
            ['Edit LaunchAgent plist file'],
            ['Update StandardOutPath and StandardErrorPath'],
            [''],
            ['Resource Limits:'],
            ['Add to LaunchAgent plist:'],
            ['<key>SoftResourceLimits</key>'],
            ['<dict><key>NumberOfProcesses</key><integer>1</integer></dict>'],
            [''],
            ['📅 Maintenance Schedule'],
            [''],
            ['Daily:'],
            ['- Check bot status via Discord'],
            ['- Review task completion in Google Sheets'],
            [''],
            ['Weekly:'],
            ['- Review bot logs for errors'],
            ['- Update credentials if needed'],
            ['- Test task assignment workflow'],
            [''],
            ['Monthly:'],
            ['- Update bot code if needed'],
            ['- Clean old log files'],
            ['- Verify auto-start configuration'],
        ]
        
        # Write data to sheet
        for i, row in enumerate(setup_data, 1):
            if row:  # Skip empty rows
                worksheet.update_cell(i, 1, row[0])
        
        # Format the sheet
        # Bold headers
        worksheet.format('A1', {'textFormat': {'bold': True, 'fontSize': 14}})
        worksheet.format('A3', {'textFormat': {'bold': True}})
        worksheet.format('A8', {'textFormat': {'bold': True}})
        worksheet.format('A28', {'textFormat': {'bold': True}})
        worksheet.format('A44', {'textFormat': {'bold': True}})
        worksheet.format('A59', {'textFormat': {'bold': True}})
        worksheet.format('A72', {'textFormat': {'bold': True}})
        worksheet.format('A81', {'textFormat': {'bold': True}})
        worksheet.format('A86', {'textFormat': {'bold': True}})
        worksheet.format('A105', {'textFormat': {'bold': True}})
        worksheet.format('A115', {'textFormat': {'bold': True}})
        
        # Code formatting for commands
        command_ranges = ['A10:A26', 'A29:A30', 'A33:A42']
        for range_name in command_ranges:
            worksheet.format(range_name, {
                'backgroundColor': {'red': 0.95, 'green': 0.95, 'blue': 0.95},
                'textFormat': {'fontFamily': 'Courier New'}
            })
        
        print("✅ Mac Claude Bot Setup tab created successfully!")
        print("📋 Tab includes:")
        print("   • Complete setup instructions")
        print("   • Copy-paste commands")
        print("   • Troubleshooting guide")
        print("   • Management commands")
        print("   • System architecture overview")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating setup tab: {e}")
        return False

if __name__ == "__main__":
    print("📊 Creating Mac Claude Bot Setup Tab in Google Sheets...")
    print("=" * 60)
    success = create_mac_claude_setup_tab()
    if success:
        print("\n🎉 Setup complete! Check the 'Mac Claude Bot Setup' tab in your Google Sheets.")
    else:
        print("\n⚠️ Setup failed. Check the error above.")