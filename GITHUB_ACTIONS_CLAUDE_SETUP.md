# GitHub Actions with Claude Code Setup Guide

## Overview
Automate your Industrial IoT stack management using Claude Code in GitHub Actions. This setup enables automatic deployments, health checks, testing, and documentation updates.

## Features
- **Automated Health Checks**: Daily system validation
- **Smart Deployments**: Claude-powered deployment validation
- **Intelligent Testing**: Comprehensive test automation
- **Auto Documentation**: Keep docs updated automatically
- **Google Sheets Integration**: Log all activities to your tracking sheets
- **Discord/WhatsApp Notifications**: Real-time status updates

## Quick Setup (10 minutes)

### 1. Enable GitHub Actions
The workflow file is already created at `.github/workflows/claude-automation.yml`

### 2. Configure Repository Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

**Required Secrets:**
```
ANTHROPIC_API_KEY=your-claude-api-key
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account",...}
GOOGLE_SHEETS_ID=1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do
```

**Optional Secrets (for notifications):**
```
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
DISCORD_BOT_TOKEN=your-discord-bot-token
DISCORD_WEBHOOK_URL=your-discord-webhook-url
```

### 3. Google Sheets API Setup for GitHub Actions

#### Create Service Account for GitHub Actions:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project (or create new one)
3. Enable Google Sheets API
4. Create credentials → Service Account
5. Name it: "github-actions-claude"
6. Download JSON key file
7. Copy entire JSON content to `GOOGLE_SHEETS_CREDENTIALS` secret

#### Share Sheet with Service Account:
1. Open your Google Sheet
2. Click Share
3. Add the service account email (from JSON file)
4. Give "Editor" permissions

## Available Automation Tasks

### 1. Health Check (Default)
**Trigger**: Daily at 6 AM UTC, manual dispatch
**What it does**:
- Validates all configuration files
- Tests Google Sheets connectivity
- Checks GitHub workflow status
- Updates Claude Tasks with any issues

### 2. Deploy Staging
**Trigger**: Manual dispatch
**What it does**:
- Validates configurations
- Runs pre-deployment tests
- Deploys Docker containers
- Tests MQTT and WhatsApp integration
- Updates deployment status

### 3. Run Tests
**Trigger**: On push/PR to main
**What it does**:
- Tests Node-RED flows
- Validates MQTT processing
- Tests Discord bot
- Checks WhatsApp integration
- Generates test reports

### 4. Update Documentation
**Trigger**: Manual dispatch
**What it does**:
- Scans for new files
- Updates README files
- Generates API docs
- Updates integration guides
- Commits changes

### 5. Backup Configurations
**Trigger**: Manual dispatch
**What it does**:
- Exports Node-RED flows
- Backs up Docker configs
- Archives Ignition projects
- Updates backup status

## Manual Triggers

### Run Specific Task
1. Go to your GitHub repository
2. Click "Actions" tab
3. Select "Claude Code Automation for Industrial IoT"
4. Click "Run workflow"
5. Choose task type from dropdown
6. Click "Run workflow"

### Available Task Types
- `health-check` - System validation
- `deploy-staging` - Deploy to staging
- `run-tests` - Run test suite
- `update-docs` - Update documentation
- `backup-configs` - Backup configurations

## Integration with Your Current Setup

### Google Sheets Updates
The automation will:
- Add entries to "Agent Activities" tab
- Log automation results
- Track deployment status
- Update task completion

### Discord Integration
If configured, sends notifications to your Discord server:
- Automation start/completion
- Success/failure status
- Links to workflow runs
- Error summaries

### WhatsApp Alerts (Future)
Can be extended to send critical alerts via WhatsApp:
- Deployment failures
- System health issues
- Security alerts

## Example Workflow Runs

### Daily Health Check
```
🤖 6:00 AM UTC - Health check started
✅ Configuration files validated
✅ Google Sheets connectivity confirmed
✅ All services healthy
📊 Updated tracking sheets
💬 Sent Discord notification
```

### Deployment to Staging
```
🚀 Manual trigger - Deploy staging
✅ Pre-deployment tests passed
🐳 Docker containers deployed
📡 MQTT connectivity confirmed
📱 WhatsApp integration tested
📊 Deployment status logged
```

### Test Suite Execution
```
🧪 PR #23 triggered test suite
✅ Node-RED flows validated
✅ MQTT message processing tested
✅ Discord bot responded correctly
✅ Steel Bonnet integration working
📈 Test coverage: 95%
```

## Monitoring and Logs

### GitHub Actions Logs
- Go to Actions tab to see all runs
- Click on specific run for detailed logs
- Download artifacts for reports

### Google Sheets Tracking
- All automation activities logged to "Agent Activities"
- Deployment status tracked
- Error summaries included

### Discord Notifications
- Real-time status updates
- Links to workflow runs
- Color-coded success/failure

## Troubleshooting

### Common Issues

#### 1. Claude API Key Issues
```
Error: Invalid API key
Solution: Verify ANTHROPIC_API_KEY in repository secrets
```

#### 2. Google Sheets Access Denied
```
Error: 403 Forbidden
Solution: 
- Check service account has Editor access to sheet
- Verify GOOGLE_SHEETS_CREDENTIALS is valid JSON
```

#### 3. Workflow Timeout
```
Error: Timeout after 10 minutes
Solution: Complex tasks may need longer timeout
```

### Debug Steps
1. Check repository secrets are set correctly
2. Verify Google Sheets sharing permissions
3. Test Claude API key manually
4. Check workflow logs for specific errors

## Security Considerations

### Secrets Management
- Never commit API keys to repository
- Use GitHub secrets for all sensitive data
- Rotate keys regularly
- Limit service account permissions

### Access Control
- Service account has minimal required permissions
- GitHub Actions only runs on main branch
- Manual approval for sensitive operations

## Advanced Configuration

### Custom Claude Prompts
Modify the `claude_prompts` in the workflow to customize automation behavior:

```python
'custom-task': """
    Your custom Claude automation prompt here.
    Be specific about what you want Claude to do.
"""
```

### Extended Notifications
Add Slack, Teams, or email notifications by modifying the notification job.

### Environment-Specific Deployments
Create separate workflows for dev/staging/production environments.

## Cost Estimation

### GitHub Actions
- 2,000 free minutes per month
- Additional minutes: $0.008/minute
- Typical run: 5-10 minutes
- Monthly cost: ~$0-5

### Claude API Usage
- Health checks: ~1,000 tokens
- Deployments: ~5,000 tokens
- Daily usage: ~2,000 tokens
- Monthly cost: ~$2-10

## Next Steps

1. **Set up secrets** in your GitHub repository
2. **Test health check** by running workflow manually
3. **Configure Discord webhook** for notifications
4. **Schedule regular deployments** as needed
5. **Customize prompts** for your specific needs

## Benefits for Your IoT Stack

### Automation
- Hands-off daily health monitoring
- Intelligent deployment validation
- Automated testing and documentation

### Reliability
- Catch issues before they affect production
- Consistent deployment processes
- Automated backup procedures

### Visibility
- Real-time status in Discord
- Comprehensive logging in Google Sheets
- GitHub Actions history

### Scalability
- Easy to add new automation tasks
- Scales with your IoT infrastructure
- Integrates with existing tools

---

**Ready to automate your Industrial IoT stack with Claude Code!** 🤖🏭