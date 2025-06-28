# GitHub Actions with Claude Max Setup Guide

## Overview
Leverage your existing Claude Max subscription for automated Industrial IoT stack management. This approach uses GitHub Actions to prepare context and create tasks, then you complete them using Claude Max - no additional API costs!

## Key Benefits
- ✅ **Use your existing Claude Max subscription** (no API charges)
- 🤖 **Automated context preparation** via GitHub Actions  
- 📋 **Structured task workflows** with clear instructions
- 📊 **Google Sheets integration** for tracking
- 💬 **Discord notifications** when tasks are ready
- 📁 **Downloadable context files** for each session

## How It Works

### 1. GitHub Actions Prepares Everything
- Analyzes repository state and recent changes
- Generates task-specific context and recommendations
- Creates downloadable artifacts with all needed information
- Updates Google Sheets with task status
- Creates GitHub issue with session instructions

### 2. You Execute with Claude Max
- Download context files from GitHub Actions artifacts
- Use Claude Max to review context and execute tasks
- Update Google Sheets when complete
- Close the GitHub issue

### 3. No API Costs
- Uses your existing Claude Max subscription
- GitHub Actions only does preparation work
- All AI analysis happens in your Claude Max session

## Quick Setup (5 minutes)

### 1. Repository Secrets
Go to GitHub repository → Settings → Secrets and variables → Actions

**Required:**
```
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}
GOOGLE_SHEETS_ID=1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do
```

**Optional (for notifications):**
```
DISCORD_WEBHOOK_URL=your-discord-webhook-url
```

### 2. Test the Workflow
1. Go to Actions tab in your repository
2. Select "Claude Max Automation for Industrial IoT"
3. Click "Run workflow"
4. Choose a task type (start with "health-check")
5. Click "Run workflow"

## Available Automation Tasks

### 🔍 Health Check
**What GitHub Actions prepares:**
- Repository analysis and recent changes
- System component status validation
- Configuration file checks
- Integration point verification

**What you do in Claude Max:**
- Review system health context
- Identify any issues or improvements
- Update recommendations in Google Sheets

### 🚀 Deploy Staging
**What GitHub Actions prepares:**
- Docker configuration analysis
- Deployment readiness checklist
- Environment variable validation
- Integration test preparation

**What you do in Claude Max:**
- Validate deployment configurations
- Review Steel Bonnet MQTT setup
- Test Discord bot deployment readiness
- Update deployment status

### 🧪 Run Tests
**What GitHub Actions prepares:**
- Test file inventory and analysis
- Integration testing checklist
- Known issues and test history
- Performance baseline data

**What you do in Claude Max:**
- Design comprehensive test scenarios
- Validate WhatsApp integration flow
- Test Discord bot functionality
- Update test results and recommendations

### 📝 Update Documentation
**What GitHub Actions prepares:**
- Documentation inventory and gaps
- Recent code changes requiring docs
- Integration guide status
- API documentation needs

**What you do in Claude Max:**
- Review and update documentation
- Ensure guides are current
- Add missing documentation
- Commit documentation updates

### 💾 Backup Configurations
**What GitHub Actions prepares:**
- Configuration file inventory
- Backup status and history
- Critical files identification
- Archive preparation checklist

**What you do in Claude Max:**
- Review backup completeness
- Identify missing configurations
- Update backup procedures
- Validate recovery processes

## Workflow Example

### 1. Trigger Automation
```
You: Run "health-check" via GitHub Actions
↓
GitHub Actions: Prepares context, creates issue, notifies Discord
```

### 2. Claude Max Session
```
GitHub Issue Created: "🤖 Claude Max Session Ready: health-check"
↓
You: Download context files from GitHub Actions artifacts
↓
Claude Max: Review context, execute health check analysis
↓ 
You: Update Google Sheets with findings
```

### 3. Completion
```
Google Sheets: Updated with results
GitHub Issue: Closed
Discord: Notified of completion
```

## Context Files Generated

### `claude_max_context.json`
```json
{
  "metadata": {
    "task_type": "health-check",
    "github_run_id": "123456",
    "generated_at": "2025-06-04T10:30:00Z"
  },
  "repository_analysis": {
    "branch": "main",
    "recent_commits": [...],
    "file_counts": {...}
  },
  "system_health": {
    "File: docker-compose.yml": "✅ Present",
    "Directory: Steel_Bonnet": "✅ Present"
  },
  "task_context": {
    "focus": "System health validation",
    "key_files": [...],
    "actions_needed": [...]
  }
}
```

### `claude_max_summary.md`
Human-readable summary with:
- Task-specific guidance
- Key files to review
- Actions needed
- Current repository status
- Health check results

## Step-by-Step Usage

### 1. Running an Automation Task

**From GitHub:**
1. Go to your repository → Actions tab
2. Select "Claude Max Automation for Industrial IoT"  
3. Click "Run workflow"
4. Choose task type from dropdown
5. Click "Run workflow"

**From Schedule:**
- Health checks run automatically daily at 6 AM UTC
- Creates context and GitHub issue automatically

### 2. Accessing Your Claude Max Session

**Check Discord:**
- Get notification that session is ready
- Link to GitHub issue with instructions

**GitHub Issue:**
- Auto-created with title like "🤖 Claude Max Session Ready: health-check"
- Contains download links and instructions
- Assigned to you automatically

**Download Context:**
1. Click workflow run link from issue
2. Scroll to "Artifacts" section  
3. Download "claude-max-context-{task-type}"
4. Extract files locally

### 3. Claude Max Session

**Open Claude Max and:**
1. Upload `claude_max_summary.md` for quick context
2. Reference `claude_max_context.json` for detailed data
3. Execute the task as outlined in the summary
4. Take notes on findings and recommendations

### 4. Update Tracking

**Google Sheets:**
1. Go to "Agent Activities" tab
2. Update the automation task row:
   - Status: "Complete"
   - Duration: Time spent
   - Output: Your findings/recommendations
   - Next Action: Any follow-up needed

**GitHub Issue:**
- Add comment with summary of work done
- Close the issue

## Integration with Your Current Setup

### Google Sheets Updates
The automation will:
- Create "In Progress" entry when started
- You update to "Complete" when done
- Tracks all automation activities
- Links to GitHub workflow runs

### Discord Notifications
- Session ready notifications
- Links to GitHub issues
- Status updates when you complete tasks

### GitHub Issues
- Automatic issue creation for each session
- Contains all needed context and links
- Assigned to repository owner
- Auto-labeled for organization

## Cost Comparison

### Claude Max Approach (This Setup)
- ✅ **Claude Max subscription**: Already paid
- ✅ **GitHub Actions**: 2,000 free minutes/month
- ✅ **Total additional cost**: $0

### API Approach (Previous Setup)  
- 💰 **Claude API**: ~$2-10/month for automation
- ✅ **GitHub Actions**: 2,000 free minutes/month
- 💰 **Total additional cost**: $2-10/month

## Advantages of Claude Max Approach

### 🧠 Better Context Understanding
- Upload multiple files to Claude Max
- Longer context windows
- More sophisticated analysis

### 🎛️ Interactive Control
- Ask follow-up questions
- Iterate on solutions
- Real-time problem solving

### 💰 Cost Efficiency
- No additional API charges
- Leverage existing subscription
- Unlimited automation sessions

### 🔄 Flexible Execution
- Run when convenient for you
- No time pressure from API costs
- Can spend more time on complex issues

## Example Session Workflow

### Morning Health Check
```
6:00 AM UTC: GitHub Actions runs health check
6:05 AM: Discord notification sent
8:00 AM: You check Discord, see automation ready
8:05 AM: Download context files
8:10 AM: Claude Max session - review IoT stack health
8:30 AM: Update Google Sheets with findings
8:35 AM: Close GitHub issue
```

### Manual Deployment
```
2:00 PM: You trigger "deploy-staging" workflow
2:05 PM: GitHub issue created with deployment context
2:10 PM: Download deployment checklist and configs
2:15 PM: Claude Max session - validate deployment
2:45 PM: Update deployment status in Google Sheets
2:50 PM: Deploy with confidence
```

## Troubleshooting

### Context Files Not Generated
- Check GitHub Actions logs
- Verify repository permissions
- Ensure secrets are configured

### Google Sheets Not Updating
- Verify service account permissions
- Check credentials secret format
- Test sheet access manually

### Discord Notifications Missing
- Verify webhook URL secret
- Check Discord channel permissions
- Test webhook manually

## Security Notes

### No API Keys Required
- No Claude API key needed
- Reduces secret management burden
- Uses existing authentication methods

### Secure Context Handling
- Context files stored as GitHub artifacts
- Automatic cleanup after 30 days
- No sensitive data in artifacts

## Next Steps

1. **Set up repository secrets** (Google Sheets + Discord)
2. **Test health check automation** 
3. **Run your first Claude Max session**
4. **Configure daily automation schedule**
5. **Customize task types** for your specific needs

---

**Ready to automate your Industrial IoT stack with Claude Max!** 🤖🏭

*No additional costs, maximum flexibility, leveraging your existing subscription.*