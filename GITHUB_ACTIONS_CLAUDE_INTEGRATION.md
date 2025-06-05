# GitHub Actions Claude Integration Guide

## 🚀 Overview
This guide helps integrate the GitHub Actions Claude instance with our Industrial IoT Stack.

## 📋 Setup Checklist

### 1. Repository Secrets
Configure these secrets in your GitHub repository:

```
GOOGLE_SHEETS_ID=YOUR_SHEET_ID
GOOGLE_CREDENTIALS=<service-account-json-content>
DISCORD_WEBHOOK=https://discord.com/api/webhooks/...
N8N_API_KEY=<your-n8n-api-key>
N8N_API_URL=http://172.28.214.170:5678/api/v1
```

### 2. Workflow Triggers
The Claude automation workflow can be triggered by:
- **Push to main/development** - Automatic health checks
- **Pull requests** - Validation and testing
- **Manual dispatch** - On-demand Claude tasks

### 3. Available Claude Tasks
- `system_health_check` - Comprehensive system validation
- `deploy_updates` - Deploy configuration changes
- `run_integration_tests` - Execute end-to-end tests
- `update_documentation` - Sync documentation

### 4. Integration Points

#### Discord Notifications
- Health check results sent to Discord
- Deployment status updates
- Error alerts and warnings

#### Google Sheets Updates
- Execution logs and status
- Performance metrics
- Task completion tracking

#### n8n API Integration
- Workflow health monitoring
- Execution status checks
- Configuration validation

## 🔧 File Structure
```
.github/
  workflows/
    claude-automation.yml    # Main workflow
scripts/
  github_actions_claude_runner.py     # Execution engine
  update_github_actions_status.py     # Status tracking
requirements-github-actions.txt       # Dependencies
```

## 🎯 Usage Examples

### Manual Workflow Dispatch
```bash
# Trigger health check
gh workflow run claude-automation.yml \
  -f claude_task=system_health_check \
  -f environment=production

# Run integration tests
gh workflow run claude-automation.yml \
  -f claude_task=run_integration_tests \
  -f environment=staging
```

### API Integration
```python
# Monitor workflow status
import requests

def check_github_actions_status():
    url = "https://api.github.com/repos/OWNER/REPO/actions/runs"
    headers = {"Authorization": "token YOUR_TOKEN"}
    response = requests.get(url, headers=headers)
    return response.json()
```

## 🔄 Coordination with Other Claude Instances

### Server Claude
- Provides system state and configuration
- Manages Docker services and MQTT
- Handles Discord integration

### Mac Claude  
- Repository management and development
- Code reviews and architecture
- Local testing and validation

### GitHub Actions Claude
- CI/CD automation and deployment
- Health monitoring and alerting
- Cross-environment coordination

## 📊 Monitoring and Alerting

### Discord Integration
All GitHub Actions Claude activities will be posted to Discord with:
- Execution status and timing
- Health check results
- Error details and stack traces
- Performance metrics

### Google Sheets Tracking
Execution data flows to Google Sheets for:
- Historical trend analysis
- Performance monitoring
- Task completion tracking

## 🚀 Next Steps

1. **Configure secrets** in GitHub repository
2. **Test workflow** with manual dispatch
3. **Verify Discord** notifications working
4. **Enable automatic** triggers on main branch
5. **Monitor execution** logs and performance

Created: 2025-06-05 07:08:20
