#!/usr/bin/env python3
"""
Create Claude Code Action Setup Instructions in Google Sheets
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path
from datetime import datetime

# Configuration
SHEET_ID = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = str(Path.home() / 'Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json')

def create_claude_action_setup_tab():
    """Create detailed Claude Code Action setup instructions in Google Sheets"""
    try:
        # Connect to Google Sheets
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        
        # Create or get the worksheet
        try:
            worksheet = sheet.worksheet('Claude Action Setup')
            print("📊 Found existing Claude Action Setup sheet")
        except:
            worksheet = sheet.add_worksheet(title='Claude Action Setup', rows=150, cols=8)
            print("📊 Created new Claude Action Setup sheet")
        
        # Clear existing content
        worksheet.clear()
        
        # Header and setup data
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Create comprehensive setup instructions
        data = [
            # Header section
            ['Claude Code Action Setup Instructions', '', '', '', '', '', '', ''],
            ['Generated', timestamp, '', '', '', '', '', ''],
            ['Status', '⏳ Ready to Setup', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Why Mac Claude couldn\'t complete it
            ['🚧 WHY AUTOMATED SETUP FAILED', '', '', '', '', '', '', ''],
            ['Issue', 'Details', 'Solution', '', '', '', '', ''],
            ['GitHub CLI Missing', 'gh command not installed on system', 'Manual setup required'],
            ['Directory Restrictions', 'Claude Code security prevents cd to /tmp/', 'Work within current directory'],
            ['Remote Repository Creation', 'Cannot create GitHub repos without CLI/API', 'Manual creation via GitHub web interface'],
            ['Authentication Required', 'Git push needs GitHub credentials', 'User must authenticate manually'],
            ['', '', '', '', '', '', '', ''],
            
            # Step-by-step instructions
            ['📋 STEP-BY-STEP SETUP INSTRUCTIONS', '', '', '', '', '', '', ''],
            ['Step', 'Action', 'Details', 'Time', 'Status', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Step 1: Create Repository
            ['1', 'Create GitHub Repository', '', '2 min', '⏳ Pending'],
            ['1a', 'Go to GitHub', 'https://github.com/new', '', ''],
            ['1b', 'Repository name', 'claude-code-action', '', ''],
            ['1c', 'Description', 'Claude Code Action with OAuth support for Claude Max - Industrial IoT Stack integration', '', ''],
            ['1d', 'Visibility', 'Public', '', ''],
            ['1e', 'Initialize options', 'Leave ALL unchecked (no README, .gitignore, license)', '', ''],
            ['1f', 'Click', 'Create repository', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Step 2: Clone and Prepare
            ['2', 'Clone Source Repository', '', '3 min', '⏳ Pending'],
            ['2a', 'Open Terminal', 'Navigate to desired directory', '', ''],
            ['2b', 'Clone command', 'git clone https://github.com/grll/claude-code-action.git', '', ''],
            ['2c', 'Enter directory', 'cd claude-code-action', '', ''],
            ['2d', 'Remove git history', 'rm -rf .git', '', ''],
            ['2e', 'Initialize new repo', 'git init', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Step 3: Configure and Push
            ['3', 'Push to Your Repository', '', '2 min', '⏳ Pending'],
            ['3a', 'Add all files', 'git add .', '', ''],
            ['3b', 'Create commit', 'git commit -m "Initial commit: Claude Code Action with OAuth support"', '', ''],
            ['3c', 'Add remote', 'git remote add origin https://github.com/slimstrongarm/claude-code-action.git', '', ''],
            ['3d', 'Set main branch', 'git branch -M main', '', ''],
            ['3e', 'Push to GitHub', 'git push -u origin main', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Step 4: Install GitHub App
            ['4', 'Install Claude GitHub App', '', '3 min', '⏳ Pending'],
            ['4a', 'Visit app page', 'https://github.com/apps/claude', '', ''],
            ['4b', 'Click Install', 'Install for your account/organization', '', ''],
            ['4c', 'Select repositories', 'Both: industrial-iot-stack AND claude-code-action', '', ''],
            ['4d', 'Grant permissions', 'All requested permissions (read/write access)', '', ''],
            ['4e', 'Confirm installation', 'Complete the installation process', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Step 5: Configure Secrets
            ['5', 'Add GitHub Secrets', '', '2 min', '⏳ Pending'],
            ['5a', 'Go to repository', 'https://github.com/slimstrongarm/industrial-iot-stack', '', ''],
            ['5b', 'Navigate to secrets', 'Settings → Secrets and variables → Actions', '', ''],
            ['5c', 'Add secret option 1', 'ANTHROPIC_API_KEY (if using direct API)', '', ''],
            ['5d', 'Add secret option 2', 'CLAUDE_MAX_SESSION_KEY (if using OAuth with Claude Max)', '', ''],
            ['5e', 'Value source', 'Get from Claude Code session or Anthropic account', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Step 6: Add Workflow
            ['6', 'Add Workflow to Industrial IoT Stack', '', '5 min', '⏳ Pending'],
            ['6a', 'Create file', '.github/workflows/claude.yml in industrial-iot-stack repo', '', ''],
            ['6b', 'Copy workflow content', 'See detailed YAML below', '', ''],
            ['6c', 'Update username', 'Replace YOUR_USERNAME with slimstrongarm', '', ''],
            ['6d', 'Commit workflow', 'git add, commit, and push the new workflow', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Step 7: Test
            ['7', 'Test the Integration', '', '2 min', '⏳ Pending'],
            ['7a', 'Create test issue', 'New issue in industrial-iot-stack repository', '', ''],
            ['7b', 'Add test comment', '@claude Hello! Can you see this and respond?', '', ''],
            ['7c', 'Wait for response', 'Claude should respond within 30 seconds', '', ''],
            ['7d', 'Verify functionality', 'Check that Claude understood and responded appropriately', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Detailed workflow YAML
            ['📝 WORKFLOW YAML CONTENT', '', '', '', '', '', '', ''],
            ['File Location', '.github/workflows/claude.yml', '', '', '', '', '', ''],
            ['Content', 'Copy this exact YAML:', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['---YAML START---', '', '', '', '', '', '', ''],
            ['name: Claude Code Action', '', '', '', '', '', '', ''],
            ['on:', '', '', '', '', '', '', ''],
            ['  issue_comment:', '', '', '', '', '', '', ''],
            ['    types: [created, edited]', '', '', '', '', '', '', ''],
            ['  pull_request_review:', '', '', '', '', '', '', ''],
            ['    types: [submitted]', '', '', '', '', '', '', ''],
            ['  issues:', '', '', '', '', '', '', ''],
            ['    types: [opened]', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['permissions:', '', '', '', '', '', '', ''],
            ['  contents: write', '', '', '', '', '', '', ''],
            ['  issues: write', '', '', '', '', '', '', ''],
            ['  pull-requests: write', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['jobs:', '', '', '', '', '', '', ''],
            ['  claude:', '', '', '', '', '', '', ''],
            ['    if: contains(github.event.comment.body, \'@claude\')', '', '', '', '', '', '', ''],
            ['    runs-on: ubuntu-latest', '', '', '', '', '', '', ''],
            ['    steps:', '', '', '', '', '', '', ''],
            ['      - uses: slimstrongarm/claude-code-action@main', '', '', '', '', '', '', ''],
            ['        with:', '', '', '', '', '', '', ''],
            ['          github-token: ${{ secrets.GITHUB_TOKEN }}', '', '', '', '', '', '', ''],
            ['          anthropic-api-key: ${{ secrets.ANTHROPIC_API_KEY }}', '', '', '', '', '', '', ''],
            ['          # OR for OAuth: session-key: ${{ secrets.CLAUDE_MAX_SESSION_KEY }}', '', '', '', '', '', '', ''],
            ['---YAML END---', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Troubleshooting
            ['🔧 TROUBLESHOOTING', '', '', '', '', '', '', ''],
            ['Issue', 'Solution', '', '', '', '', '', ''],
            ['Push fails with auth error', 'Run: git config --global credential.helper store', '', '', '', '', '', ''],
            ['Repository already exists', 'Delete the repo and recreate, or use git push --force', '', '', '', '', '', ''],
            ['GitHub App not working', 'Check permissions and reinstall if needed', '', '', '', '', '', ''],
            ['Claude not responding', 'Verify secrets are correct and try again', '', '', '', '', '', ''],
            ['Workflow not triggering', 'Check YAML syntax and commit the workflow file', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Benefits and use cases
            ['🎯 USE CASES FOR INDUSTRIAL IOT STACK', '', '', '', '', '', '', ''],
            ['Scenario', 'Example Command', 'Expected Result', '', '', '', '', ''],
            ['Code Review', '@claude Review the WhatsApp API integration for security issues', 'Detailed security analysis and suggestions'],
            ['Bug Fix', '@claude Fix the timeout issue in unified_monitoring_system.py', 'Implemented fix with explanation'],
            ['Documentation', '@claude Update INDEX.md to include the new monitoring features', 'Updated documentation'],
            ['Architecture', '@claude How should we structure MQTT topics for new equipment?', 'Architectural recommendations'],
            ['Testing', '@claude Write unit tests for the Discord notification client', 'Generated test cases'],
            ['Optimization', '@claude Optimize the brewery alert logic for better performance', 'Performance improvements'],
            ['', '', '', '', '', '', '', ''],
            
            # Integration with existing stack
            ['🔗 INTEGRATION WITH EXISTING STACK', '', '', '', '', '', '', ''],
            ['Component', 'How Claude Helps', '', '', '', '', '', ''],
            ['WhatsApp Integration', 'Code review, error handling improvements, feature additions', '', '', '', '', '', ''],
            ['Discord Integration', 'Notification enhancements, bot command improvements', '', '', '', '', '', ''],
            ['Google Sheets', 'Formula optimization, data structure improvements', '', '', '', '', '', ''],
            ['GitHub Actions', 'Workflow optimization, error diagnosis', '', '', '', '', '', ''],
            ['Repository Organization', 'Documentation updates, structure improvements', '', '', '', '', '', ''],
            ['Steel Bonnet Brewery', 'Equipment integration advice, MQTT topic design', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Progress tracking
            ['📊 SETUP PROGRESS TRACKER', '', '', '', '', '', '', ''],
            ['Task', 'Status', 'Completion Time', 'Notes', '', '', '', ''],
            ['Create GitHub Repository', '⏳ Not Started', '', ''],
            ['Clone Source Code', '⏳ Not Started', '', ''],
            ['Push to New Repository', '⏳ Not Started', '', ''],
            ['Install GitHub App', '⏳ Not Started', '', ''],
            ['Configure Secrets', '⏳ Not Started', '', ''],
            ['Add Workflow File', '⏳ Not Started', '', ''],
            ['Test Integration', '⏳ Not Started', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            # Final notes
            ['📝 IMPORTANT NOTES', '', '', '', '', '', '', ''],
            ['Note', 'Details', '', '', '', '', '', ''],
            ['OAuth vs API Key', 'OAuth uses your Claude Max subscription (no extra cost)', '', '', '', '', '', ''],
            ['Repository Permissions', 'App needs access to both repositories', '', '', '', '', '', ''],
            ['Testing', 'Start with simple @claude hello to verify connection', '', '', '', '', '', ''],
            ['Security', 'Never commit API keys to repository, use GitHub secrets only', '', '', '', '', '', ''],
            ['Rate Limits', 'Be mindful of Claude usage limits with your subscription', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            
            ['Status: Ready for Manual Setup', '', '', '', '', '', '', ''],
            ['Estimated Total Time: 15-20 minutes', '', '', '', '', '', '', ''],
            ['Difficulty: Beginner-friendly', '', '', '', '', '', '', '']
        ]
        
        # Write all data to worksheet
        cell_range = f'A1:H{len(data)}'
        worksheet.update(cell_range, data)
        
        # Format headers and sections
        worksheet.format('A1:H1', {
            'textFormat': {'bold': True, 'fontSize': 14},
            'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 1.0}
        })
        
        # Format section headers
        section_headers = [5, 13, 25, 35, 45, 55, 65, 75, 85, 105, 115, 125, 135]
        for row in section_headers:
            if row <= len(data):
                worksheet.format(f'A{row}:H{row}', {
                    'textFormat': {'bold': True, 'fontSize': 12},
                    'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
                })
        
        # Format step numbers
        for i, row_data in enumerate(data, 1):
            if len(row_data) > 0 and row_data[0].isdigit():
                worksheet.format(f'A{i}:H{i}', {
                    'textFormat': {'bold': True},
                    'backgroundColor': {'red': 0.8, 'green': 0.9, 'blue': 0.8}
                })
        
        # Auto-resize columns
        worksheet.columns_auto_resize(0, 7)
        
        print("✅ Claude Code Action Setup instructions created successfully!")
        print(f"📊 Access at: https://docs.google.com/spreadsheets/d/{SHEET_ID}")
        print("📋 Tab: 'Claude Action Setup'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating setup instructions: {e}")
        return False

if __name__ == "__main__":
    create_claude_action_setup_tab()