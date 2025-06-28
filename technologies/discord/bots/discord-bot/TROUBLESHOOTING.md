# Discord Bot Troubleshooting Guide

## Issue: Bot Not Creating Tasks in Google Sheets

### Possible Causes:

1. **Bot Mention Format**
   - Discord bot name: "Mac Claude Bot"
   - Bot might be looking for "@claude" but actual mention is "@Mac Claude Bot"
   - Solution: Update bot to recognize its actual Discord name

2. **Command Processing Order**
   - Bot was processing commands before natural language
   - Fixed by reordering message processing

3. **Google Sheets Integration**
   - ✅ Verified working - test script created CT-047
   - Service account has proper permissions

### How Discord Mentions Work:

When you type `@Mac Claude Bot add task Fix sensor`, Discord converts it to:
- `<@1380419945975779378> add task Fix sensor` (using bot ID)

The bot needs to:
1. Detect it was mentioned (using bot ID)
2. Strip out the mention
3. Process remaining text

### Testing Steps:

1. **Run Test Bot**
   ```bash
   discord-bot/manage_bot.sh test
   ```
   This runs a simplified bot that logs every message

2. **In Discord, try:**
   - `@Mac Claude Bot status` - Simple test
   - `@Mac Claude Bot add task Test Google Sheets` - Task creation

3. **Check Console Output**
   The test bot will show exactly what it receives

### Fix Applied:

The enhanced bot now:
- ✅ Properly detects mentions using bot ID
- ✅ Has full Google Sheets integration
- ✅ Creates sequential task IDs (CT-XXX)
- ✅ Includes debug logging

### Manual Task Creation Test:

If Discord mention detection fails, the Google Sheets integration itself works:
```bash
python3 discord-bot/test_sheets_integration.py
```
This created CT-047 successfully.