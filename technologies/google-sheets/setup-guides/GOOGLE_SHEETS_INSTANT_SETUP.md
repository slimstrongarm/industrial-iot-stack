# Google Sheets Instant Setup - Step by Step

## 🚀 Let's Create Your Tracker Together!

### Step 1: Create New Google Sheet
1. **Open this link**: [Create New Google Sheet](https://sheets.new)
2. **Sign in** with your Google account if needed
3. The new blank sheet will open automatically

### Step 2: Open Apps Script Editor
1. In your new sheet, click **Extensions** in the menu bar
2. Click **Apps Script**
3. A new tab will open with the script editor

### Step 3: Copy the Setup Script
1. **Delete** any existing code in the editor (usually just `function myFunction()`)
2. Go back to your VS Code
3. Open the file: `/Users/joshpayneair/Desktop/industrial-iot-stack/scripts/google_sheets_setup.gs`
4. **Select ALL** the code (Cmd+A)
5. **Copy** it (Cmd+C)

### Step 4: Paste and Run
1. Go back to the Apps Script tab
2. **Paste** the code (Cmd+V)
3. Click the **💾 Save** icon (or Cmd+S)
4. Click the **▶️ Run** button
5. In the dropdown, make sure `setupProgressTracker` is selected
6. Click **Run**

### Step 5: Grant Permissions
1. A popup will appear saying "Authorization required"
2. Click **Review permissions**
3. Choose your Google account
4. Click **Advanced** (bottom left)
5. Click **Go to IoT Stack Progress Master (unsafe)**
   - Don't worry, this is your own script!
6. Click **Allow**

### Step 6: Watch the Magic! ✨
- The script will run for about 10-15 seconds
- You'll see a success message: "Setup complete!"
- Switch back to your Google Sheet tab
- You'll see all 6 tabs created with sample data!

## 🎯 What You'll See Immediately:

### ✅ 6 Fully Configured Tabs:
1. **Docker Migration Tasks** - With your 3 initial tasks
2. **System Components Status** - 5 components pre-configured
3. **Project Migration Tracker** - All 9 projects listed
4. **Agent Activities** - Ready for logging
5. **Integration Checklist** - 6 integrations tracked
6. **Dashboard** - Summary with live formulas

### ✅ Custom Menu:
Look for **"🏭 IoT Stack Tools"** in your menu bar with:
- 📊 Refresh Dashboard
- ➕ Add Docker Task  
- 📝 Log Agent Activity
- 🔄 Update Component Status
- 📧 Send Status Report

### ✅ Automatic Features:
- Color coding already applied
- Formulas calculating percentages
- Timestamp columns formatted
- Headers frozen for scrolling

## 📱 Quick Mobile Setup

### On Your Phone:
1. Download **Google Sheets** app
2. Open the app and sign in
3. Find "IoT Stack Progress Master"
4. Tap the **⭐ star** to add to favorites
5. Enable notifications in app settings

## 🔗 Get Your Sheet ID

Your sheet URL will look like:
```
https://docs.google.com/spreadsheets/d/ABC123XYZ/edit
                                      ^^^^^^^^^ 
                                    This is your Sheet ID
```

Save this ID for the automation scripts!

## 🎉 That's It! You're Done!

Your Industrial IoT Stack Progress Tracker is now live and ready to use. The whole process should have taken less than 5 minutes.

### Next Steps:
1. **Bookmark** your sheet for easy access
2. **Share** with team members (Share button → Add emails)
3. **Test** the custom menu functions
4. **Set up** automation scripts with your Sheet ID

### Need Help?
- If the script fails, try running it again
- Check for any error messages in the Apps Script editor
- Make sure you're using a Google account with Sheets access

---

**Congratulations! 🎊 You now have a professional IoT monitoring dashboard!**