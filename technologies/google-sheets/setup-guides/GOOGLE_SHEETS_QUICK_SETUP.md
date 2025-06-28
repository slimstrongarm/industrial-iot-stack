# Google Sheets Progress Tracker - Quick Setup Guide

## 🚀 5-Minute Setup

### Step 1: Create Your Google Sheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new blank spreadsheet
3. Name it "IoT Stack Progress Master"

### Step 2: Install the Tracking System
1. In your new sheet, go to **Extensions → Apps Script**
2. Delete any existing code
3. Copy ALL content from `scripts/google_sheets_setup.gs`
4. Paste into Apps Script editor
5. Click **Save** (💾 icon)
6. Click **Run** → Select `setupProgressTracker`
7. Grant permissions when prompted

### Step 3: Verify Setup
After running, you should see:
- ✅ 6 tabs created (Docker Tasks, Components, Projects, etc.)
- ✅ Custom menu "🏭 IoT Stack Tools" in your sheet
- ✅ Sample data populated
- ✅ Success notification

### Step 4: Enable API Access (For Automation)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Enable Google Sheets API
4. Create Service Account credentials
5. Download JSON key file
6. Share your Google Sheet with the service account email

## 📱 Mobile Access
1. Install Google Sheets mobile app
2. Star the "IoT Stack Progress Master" sheet
3. Enable notifications in app settings

## 🔄 Automated Updates

### From Your Local Machine
```bash
# Install dependencies
pip install gspread oauth2client

# Set environment variables
export GOOGLE_SHEETS_ID="your-sheet-id-from-url"
export GOOGLE_CREDS_PATH="/path/to/credentials.json"

# Run update script
python scripts/update_google_sheets.py
```

### From Docker Container
```bash
# Add to your docker-compose.yml
docker-compose up progress-tracker
```

## 📊 Using the Tracker

### Add New Tasks
1. Click **🏭 IoT Stack Tools → Add Docker Task**
2. Fill out the form
3. Click Submit

### Update Component Status
```python
# From Python scripts
tracker.update_component_status(
    "Ignition Gateway", 
    "Running", 
    "✅ Healthy", 
    "None"
)
```

### View Dashboard
- Go to the **Dashboard** tab for summary metrics
- Metrics auto-refresh every 5 minutes
- Health alerts check every 15 minutes

## 🔗 Share & Collaborate
1. Click **Share** button in Google Sheets
2. Add team members with appropriate permissions:
   - **Viewer**: Monitor progress only
   - **Editor**: Update tasks and status

## 📧 Email Reports
1. Click **🏭 IoT Stack Tools → Send Status Report**
2. Enter your email (only needed first time)
3. Receive summary of all metrics

## 🎯 Quick Links
- Sheet ID is in the URL: `https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit`
- Service Account setup: [Google Cloud IAM](https://console.cloud.google.com/iam-admin/serviceaccounts)
- API Documentation: [Google Sheets API](https://developers.google.com/sheets/api)

## ⚡ Troubleshooting

### "Permission Denied" Error
- Make sure to share sheet with service account email
- Email looks like: `project-name@project-id.iam.gserviceaccount.com`

### Scripts Not Running
- Check triggers: Extensions → Apps Script → Triggers (clock icon)
- Verify time-based triggers are enabled

### Data Not Updating
- Check API quotas in Google Cloud Console
- Verify credentials file path is correct
- Check Docker container logs if using automation

---

**Need Help?** Check the full documentation in `GOOGLE_SHEETS_PROGRESS_TRACKER.md`