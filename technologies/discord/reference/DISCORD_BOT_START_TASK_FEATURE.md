# Discord Bot - Start Existing Task Feature

## 🎯 Feature Overview
Mobile-first task coordination allowing any Claude instance to pick up and start working on existing tasks via Discord commands.

## 📱 Usage Examples
```
@Mac Claude Bot start task CT-094
@Server Claude Bot start task CT-095
```

## ⚙️ Implementation Details

### Command Detection
```python
# In process_natural_language() method
elif 'start task' in content and 'ct-' in content:
    logger.info("Detected start existing task request")
    await self.handle_start_existing_task(message, content)
```

### Task ID Extraction
```python
import re
task_match = re.search(r'ct-(\d+)', content.lower())
task_id = f"CT-{task_match.group(1).zfill(3)}"
```

### Google Sheets Updates
1. **Assigned To** (Column 2) → Instance name (Mac Claude/Server Claude)
2. **Status** (Column 5) → "In Progress"  
3. **Notes** (Column 6) → "Started by [Instance] via Discord"

### Response Format
```python
embed = discord.Embed(
    title=f"🚀 Starting Task {task_id}",
    description=f"**{instance_name}** is now working on this task",
    color=0x0099ff
)
# Shows: Task title, Status update, Assigned to, Google Sheets link
```

## 🔄 Workflow Integration

### Current Task Management
1. **Create**: `@Mac Claude add task Build dashboard`
2. **Assign**: `@Server Claude start task CT-096`
3. **Result**: Server Claude takes ownership and updates status

### Mobile Coordination
- User on phone can assign tasks to any instance
- Real-time status updates in Google Sheets
- Discord confirmation with task details
- Cross-instance work coordination

## 🛠️ Error Handling
- **Missing Task**: "Task CT-XXX not found in Google Sheets"
- **Invalid Format**: "Please specify a task ID like: @Server Claude start task CT-094"
- **Sheets Unavailable**: "Google Sheets integration not available"
- **General Errors**: Full error logging with user notification

## 📊 Current Status
- ✅ **Code**: Complete and deployed
- ✅ **Discord**: Responding to commands
- ❌ **Google Sheets**: Connection issue ("Connection reset by peer")
- ⏳ **Testing**: Pending Sheets connection fix

## 🔧 Troubleshooting
Current issue: Google Sheets authentication failure
- Symptoms: "Connection aborted", "Connection reset by peer"
- Likely cause: Auth token refresh needed
- Impact: Bot responds but can't update Sheets

## 🎯 Next Steps
1. Fix Google Sheets connection (credentials/auth refresh)
2. Test complete workflow: Create → Assign → Update
3. Deploy identical feature to Server Claude
4. Validate mobile phone Discord app compatibility

---
*Feature ready for production use once Sheets connection is restored*