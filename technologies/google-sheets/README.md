# Google Sheets Technology Stack Documentation
*Quick reference for Claude instances working on Google Sheets integrations*

## 🎯 Quick Start for New Claude Instances

**Working on Google Sheets?** Start here:
1. **API Setup**: `api-setup/GOOGLE_SHEETS_API_SETUP.md` - Service account configuration
2. **Quick Start**: `setup-guides/GOOGLE_SHEETS_QUICK_SETUP.md` - 5-minute setup
3. **Features**: `reference/GOOGLE_SHEETS_FEATURES.md` - Full capabilities overview
4. **Scripts**: `scripts/` - Python automation scripts

## 📂 File Organization

### API Setup
- **Service Account Creation** - Google Cloud Console setup
- **Credentials Management** - JSON key file configuration
- **Permission Sharing** - Sheet access for service accounts
- **Authentication** - OAuth2 and service account auth

### Integrations
- **Discord Bot** - Task creation from Discord → Sheets
- **n8n Workflows** - Form submissions → Sheets
- **Python Scripts** - Automated task monitoring
- **Apps Script** - Custom Google Sheets functions

### Key Features
- **Claude Tasks Tab** - Living to-do list (CT-XXX tracking)
- **Real-time Monitoring** - System health dashboards
- **Mobile Access** - Google Sheets app integration
- **Automated Alerts** - Threshold-based notifications

## 🔗 Related Technologies

- **Discord**: `../discord/` - Task creation via bot commands
- **Python Scripts**: `../../scripts/` - Task worker automation
- **n8n**: `../n8n/` - Form data → Sheets workflows
- **Monitoring**: `../../scripts/monitoring/` - Live dashboards

## 📊 Current Implementation

### Master Spreadsheet
- **ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **31 Worksheets** including:
  - Claude Tasks (102+ tasks tracked)
  - Human Tasks
  - System Components Status
  - Agent Activities
  - Discord Bot Setup Guide
  - Monitoring Dashboard

### Key Tabs
- **Claude Tasks**: Main task tracking with CT-XXX identifiers
- **Human Tasks**: Manual intervention items
- **Credentials & Context**: Quick reference for new instances
- **File Tree Visualization**: Repository structure
- **Revenue Analysis**: Business metrics

## 🎯 Common Google Sheets Patterns

1. **Task Automation**: Discord → Sheets → Claude worker
2. **Status Tracking**: Real-time updates with formulas
3. **Data Validation**: Dropdown lists for consistent data
4. **Conditional Formatting**: Visual status indicators
5. **Apps Script**: Custom automation functions

## 💡 Quick Commands

```python
# Test sheets connection
python3 scripts/test_google_sheets_connection.py

# Update task status
python3 scripts/update_claude_tasks.py

# Monitor sheets for changes
python3 scripts/sheets_monitor_live.py

# Debug access issues
python3 scripts/debug_google_sheets_access.py
```

## 🏭 Integration Points

- **Service Account**: `iiot-stack-automation@iiot-stack-automation.iam.gserviceaccount.com`
- **Credentials Location**: `/credentials/iot-stack-credentials.json`
- **API Scopes**: Spreadsheets + Drive access
- **Update Frequency**: Real-time via API

---
*Last Updated: 2025-06-28 | Files: Being organized | Status: Core Integration*