# Mac-Claude Google Sheets Direct Access Setup

## Problem
Mac-claude currently uses scripts to update Google Sheets, while server-claude has direct API access.

## Solution
Set up the same Google Sheets API access on Mac that server-claude uses.

## Setup Steps

### 1. Copy Credentials from Server
```bash
# Copy the service account credentials
scp server@<SERVER_IP>:/home/server/google-sheets-credentials.json ~/google-sheets-credentials.json

# Copy the helper library
scp server@<SERVER_IP>:/home/server/google_sheets_helper.py ~/google_sheets_helper.py
```

### 2. Install Required Libraries
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3. Update Helper Library Path
Edit `~/google_sheets_helper.py` to use local credentials:
```python
# Change this line:
CREDENTIALS_FILE = '/home/server/google-sheets-credentials.json'

# To this:
CREDENTIALS_FILE = os.path.expanduser('~/google-sheets-credentials.json')
```

### 4. Test Direct Access
```python
from google_sheets_helper import GoogleSheetsHelper
from datetime import datetime

helper = GoogleSheetsHelper()
timestamp = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

# Add log entry directly
log_entry = [
    timestamp,
    'mac-claude',
    'Direct API Test',
    'Testing direct Google Sheets API access from Mac',
    'Success'
]

helper.append_row('Agent Activities', log_entry)
print("✅ Direct API access working!")
```

## Benefits of Direct Access

### No More Scripts Needed ✅
- Direct API calls instead of external scripts
- Faster execution
- Better error handling
- Real-time updates

### Same Functionality as Server-Claude ✅
- Read/write any sheet
- Update task status
- Add log entries
- Query data

### Cleaner Code ✅
```python
# Instead of running external scripts:
os.system('./update_claude_tasks.sh')

# Use direct API calls:
helper.append_row('Claude Tasks', [task_data])
```

## Service Account Details
- **Email**: server-claude@iiot-stack-automation.iam.gserviceaccount.com
- **Project**: iiot-stack-automation  
- **Permissions**: Editor access to IoT Stack Progress Master
- **Scope**: https://www.googleapis.com/auth/spreadsheets

## Alternative: Mac-Specific Service Account

If you prefer separate credentials:

### 1. Create New Service Account
```bash
# In Google Cloud Console
1. Go to IAM & Admin → Service Accounts
2. Create new service account: "mac-claude"
3. Download JSON credentials
4. Share Google Sheet with new service account email
```

### 2. Use Separate Credentials
```python
CREDENTIALS_FILE = '~/mac-claude-credentials.json'
```

## Troubleshooting

### Permission Issues
- Verify service account has Editor access to spreadsheet
- Check credentials file path is correct

### Import Issues  
- Ensure Google API libraries are installed
- Check Python path includes helper library

### API Errors
- Verify spreadsheet ID is correct
- Check internet connection
- Validate JSON credentials format

## Current Status
- **Server-claude**: ✅ Direct API access working
- **Mac-claude**: ⏳ Awaiting setup for direct access
- **Credentials**: Available for sharing between instances

This setup will give Mac-claude the same seamless Google Sheets access that server-claude currently has!