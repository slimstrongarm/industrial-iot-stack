# Google Sheets API Setup for Claude Automation

## 🎯 Goal
Enable Claude to automatically detect and execute tasks from your Google Sheet.

## 📋 Step 1: Enable Google Sheets API

### In Google Cloud Console:
1. **Go to**: [Google Cloud Console](https://console.cloud.google.com)
2. **Create a new project** (or select existing):
   - Click "Select a project" → "New Project"
   - Name: "IoT-Stack-Automation"
   - Click "Create"

3. **Enable APIs**:
   - Go to "APIs & Services" → "Enable APIs and Services"
   - Search for "Google Sheets API"
   - Click on it and press "Enable"
   - Also search and enable "Google Drive API"

## 🔑 Step 2: Create Service Account

1. **In Google Cloud Console**:
   - Go to "APIs & Services" → "Credentials"
   - Click "+ CREATE CREDENTIALS" → "Service account"

2. **Service Account Details**:
   - Service account name: `iot-stack-automation`
   - Service account ID: (auto-generated)
   - Description: "Automated task monitoring for Industrial IoT Stack"
   - Click "Create and Continue"

3. **Grant Access** (skip this step - click "Continue")

4. **Create Key**:
   - Click "Done"
   - Find your service account in the list
   - Click on it → "Keys" tab
   - "Add Key" → "Create new key"
   - Choose "JSON"
   - **SAVE THE DOWNLOADED FILE** as `iot-stack-credentials.json`

## 📧 Step 3: Share Your Google Sheet

1. **Get the service account email**:
   - Open the downloaded JSON file
   - Find the `"client_email"` field
   - Copy the email (looks like: `iot-stack-automation@project-id.iam.gserviceaccount.com`)

2. **Share your Google Sheet**:
   - Open your IoT Stack Progress Master sheet
   - Click "Share" button
   - Paste the service account email
   - Give it "Editor" access
   - Uncheck "Notify people"
   - Click "Share"

## 💾 Step 4: Save Credentials Securely

Create a secure location for your credentials:

```bash
# Create credentials directory
mkdir -p ~/Desktop/industrial-iot-stack/credentials
cd ~/Desktop/industrial-iot-stack/credentials

# Move the downloaded JSON file here
mv ~/Downloads/iot-stack-*.json ./iot-stack-credentials.json

# Set restrictive permissions
chmod 600 iot-stack-credentials.json

# Create .gitignore to prevent accidental commits
echo "*.json" > .gitignore
```

## 🐍 Step 5: Install Python Dependencies

```bash
# Install required packages
pip3 install --user gspread oauth2client

# Verify installation
python3 -c "import gspread; print('✅ gspread installed')"
```

## ✅ Step 6: Test the Connection

Save this test script:

```python
#!/usr/bin/env python3
# File: test_sheets_connection.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Your configuration
SHEET_ID = '1ILZ7c3ec4Pf6b32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
CREDS_FILE = 'credentials/iot-stack-credentials.json'

try:
    # Authenticate
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
    client = gspread.authorize(creds)
    
    # Open sheet
    sheet = client.open_by_key(SHEET_ID)
    
    # Test read
    worksheet = sheet.worksheet('Docker Migration Tasks')
    tasks = worksheet.get_all_records()
    
    print("✅ Connected successfully!")
    print(f"📊 Found {len(tasks)} tasks in the sheet")
    
    # Show Claude tasks
    claude_tasks = [t for t in tasks if 'Claude' in t.get('Assigned To', '')]
    print(f"🤖 {len(claude_tasks)} tasks assigned to Claude")
    
except Exception as e:
    print(f"❌ Error: {e}")
```

Run it:
```bash
cd ~/Desktop/industrial-iot-stack
python3 test_sheets_connection.py
```

## 🚀 Step 7: Run the Automation

Once the test works, you can run the monitoring script:

```bash
# Update the credentials path in the monitoring script
python3 scripts/sheets_to_claude_sync.py
```

## 🔒 Security Notes

1. **Never commit credentials** to Git
2. **Keep JSON file permissions** restricted (600)
3. **Use environment variables** for production:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   ```

## 🎯 What Happens Next

With this setup:
1. You add a task in Google Sheets assigned to "MacBook Claude"
2. The monitoring script detects it within 60 seconds
3. Claude executes the task based on keywords
4. Updates the sheet with progress and completion
5. Logs activity in the Agent Activities tab

Ready to set this up? Start with Step 1!