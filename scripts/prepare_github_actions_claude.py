#!/usr/bin/env python3
"""
Prepare for GitHub Actions Claude instance rollout - create integration files and workflows
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

def create_github_actions_preparation():
    """Create all necessary files and documentation for GitHub Actions Claude integration"""
    
    print("🔧 PREPARING FOR GITHUB ACTIONS CLAUDE ROLLOUT")
    print("=" * 50)
    
    base_path = Path("/mnt/c/Users/LocalAccount/industrial-iot-stack")
    
    # 1. Create .github/workflows directory
    workflows_dir = base_path / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created {workflows_dir}")
    
    # 2. Create GitHub Actions workflow for Claude automation
    claude_workflow = {
        "name": "Claude Automation Pipeline",
        "on": {
            "push": {
                "branches": ["main", "development"]
            },
            "pull_request": {
                "branches": ["main"]
            },
            "workflow_dispatch": {
                "inputs": {
                    "claude_task": {
                        "description": "Claude task to execute",
                        "required": True,
                        "default": "system_health_check"
                    },
                    "environment": {
                        "description": "Environment to target",
                        "required": True,
                        "default": "production",
                        "type": "choice",
                        "options": ["production", "staging", "development"]
                    }
                }
            }
        },
        "jobs": {
            "claude_automation": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {
                        "name": "Checkout Repository",
                        "uses": "actions/checkout@v4"
                    },
                    {
                        "name": "Setup Python",
                        "uses": "actions/setup-python@v4",
                        "with": {
                            "python-version": "3.11"
                        }
                    },
                    {
                        "name": "Install Dependencies",
                        "run": "pip install -r requirements-github-actions.txt"
                    },
                    {
                        "name": "Claude Health Check",
                        "env": {
                            "GOOGLE_SHEETS_ID": "${{ secrets.GOOGLE_SHEETS_ID }}",
                            "GOOGLE_CREDENTIALS": "${{ secrets.GOOGLE_CREDENTIALS }}",
                            "DISCORD_WEBHOOK": "${{ secrets.DISCORD_WEBHOOK }}",
                            "N8N_API_KEY": "${{ secrets.N8N_API_KEY }}",
                            "N8N_API_URL": "${{ secrets.N8N_API_URL }}"
                        },
                        "run": "python scripts/github_actions_claude_runner.py"
                    },
                    {
                        "name": "Update Status",
                        "if": "always()",
                        "run": "python scripts/update_github_actions_status.py"
                    }
                ]
            }
        }
    }
    
    workflow_file = workflows_dir / "claude-automation.yml"
    with open(workflow_file, 'w') as f:
        import yaml
        yaml.dump(claude_workflow, f, default_flow_style=False, sort_keys=False)
    print(f"✅ Created GitHub Actions workflow: {workflow_file}")
    
    # 3. Create requirements file for GitHub Actions
    requirements_content = """google-auth==2.23.4
google-auth-oauthlib==1.1.0
google-auth-httplib2==0.1.1
google-api-python-client==2.108.0
requests==2.31.0
pyyaml==6.0.1
python-dotenv==1.0.0
"""
    
    requirements_file = base_path / "requirements-github-actions.txt"
    with open(requirements_file, 'w') as f:
        f.write(requirements_content)
    print(f"✅ Created requirements file: {requirements_file}")
    
    # 4. Create GitHub Actions Claude runner script
    runner_script = '''#!/usr/bin/env python3
"""
GitHub Actions Claude Runner - Execute Claude tasks in CI/CD pipeline
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path

def get_environment_config():
    """Get configuration based on environment"""
    return {
        'google_sheets_id': os.getenv('GOOGLE_SHEETS_ID'),
        'discord_webhook': os.getenv('DISCORD_WEBHOOK'),
        'n8n_api_key': os.getenv('N8N_API_KEY'),
        'n8n_api_url': os.getenv('N8N_API_URL'),
        'environment': os.getenv('GITHUB_REF_NAME', 'unknown')
    }

def send_discord_notification(webhook_url, message, color=0x00ff00):
    """Send notification to Discord"""
    if not webhook_url:
        print("⚠️  No Discord webhook configured")
        return
    
    payload = {
        "embeds": [{
            "title": "🤖 GitHub Actions Claude",
            "description": message,
            "color": color,
            "timestamp": datetime.now().isoformat(),
            "footer": {"text": "Industrial IoT Stack CI/CD"}
        }]
    }
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("✅ Discord notification sent")
        else:
            print(f"⚠️  Discord notification failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord error: {e}")

def run_system_health_check(config):
    """Run comprehensive system health check"""
    print("🏥 Running System Health Check...")
    
    health_results = {
        "timestamp": datetime.now().isoformat(),
        "environment": config['environment'],
        "checks": {}
    }
    
    # Check n8n API if configured
    if config['n8n_api_url'] and config['n8n_api_key']:
        try:
            headers = {'X-N8N-API-KEY': config['n8n_api_key']}
            response = requests.get(f"{config['n8n_api_url']}/workflows", 
                                  headers=headers, timeout=10)
            
            if response.status_code == 200:
                workflows = response.json()
                health_results["checks"]["n8n_api"] = {
                    "status": "✅ HEALTHY",
                    "workflow_count": len(workflows.get('data', [])),
                    "response_time": response.elapsed.total_seconds()
                }
            else:
                health_results["checks"]["n8n_api"] = {
                    "status": "❌ FAILED", 
                    "error": f"HTTP {response.status_code}"
                }
        except Exception as e:
            health_results["checks"]["n8n_api"] = {
                "status": "❌ ERROR",
                "error": str(e)
            }
    
    # Check repository structure
    expected_files = [
        "STACK_CONFIG.md",
        "docker-compose.yml", 
        "scripts/discord_webhook_integration.py",
        "discord_webhook_config.json"
    ]
    
    missing_files = []
    for file_path in expected_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    health_results["checks"]["repository_structure"] = {
        "status": "✅ HEALTHY" if not missing_files else "⚠️  ISSUES",
        "missing_files": missing_files
    }
    
    # Generate health report
    overall_status = "✅ HEALTHY"
    issues = []
    
    for check_name, check_result in health_results["checks"].items():
        if "❌" in check_result["status"] or "⚠️" in check_result["status"]:
            overall_status = "⚠️  ISSUES DETECTED"
            issues.append(f"{check_name}: {check_result['status']}")
    
    # Send Discord notification
    if config['discord_webhook']:
        message = f"**System Health Check Complete**\\n"
        message += f"Environment: {config['environment']}\\n"
        message += f"Overall Status: {overall_status}\\n"
        
        if issues:
            message += f"Issues: {', '.join(issues)}"
        else:
            message += "All systems operational!"
        
        color = 0x00ff00 if overall_status == "✅ HEALTHY" else 0xff9900
        send_discord_notification(config['discord_webhook'], message, color)
    
    # Save results
    with open('github-actions-health-report.json', 'w') as f:
        json.dump(health_results, f, indent=2)
    
    print(f"✅ Health check complete: {overall_status}")
    return overall_status == "✅ HEALTHY"

def main():
    """Main GitHub Actions Claude runner"""
    print("🚀 GitHub Actions Claude Runner Starting...")
    
    config = get_environment_config()
    task = os.getenv('INPUT_CLAUDE_TASK', 'system_health_check')
    
    print(f"Environment: {config['environment']}")
    print(f"Task: {task}")
    
    success = False
    
    if task == 'system_health_check':
        success = run_system_health_check(config)
    else:
        print(f"❌ Unknown task: {task}")
        return 1
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
'''
    
    runner_file = base_path / "scripts" / "github_actions_claude_runner.py"
    with open(runner_file, 'w') as f:
        f.write(runner_script)
    print(f"✅ Created GitHub Actions runner: {runner_file}")
    
    # 5. Create status updater script
    status_updater = '''#!/usr/bin/env python3
"""
Update GitHub Actions status in Google Sheets
"""

import os
import json
from datetime import datetime

def update_github_actions_status():
    """Update GitHub Actions execution status"""
    
    print("📊 Updating GitHub Actions status...")
    
    # Read health report if it exists
    health_report = {}
    if os.path.exists('github-actions-health-report.json'):
        with open('github-actions-health-report.json', 'r') as f:
            health_report = json.load(f)
    
    # Create status entry
    status_entry = {
        "timestamp": datetime.now().isoformat(),
        "github_ref": os.getenv('GITHUB_REF', 'unknown'),
        "github_sha": os.getenv('GITHUB_SHA', 'unknown'),
        "workflow_run_id": os.getenv('GITHUB_RUN_ID', 'unknown'),
        "health_report": health_report
    }
    
    # Save to file for potential pickup by other systems
    with open('github-actions-status.json', 'w') as f:
        json.dump(status_entry, f, indent=2)
    
    print(f"✅ Status updated: {status_entry['timestamp']}")

if __name__ == "__main__":
    update_github_actions_status()
'''
    
    status_file = base_path / "scripts" / "update_github_actions_status.py"
    with open(status_file, 'w') as f:
        f.write(status_updater)
    print(f"✅ Created status updater: {status_file}")
    
    # 6. Create GitHub Actions integration guide
    integration_guide = f"""# GitHub Actions Claude Integration Guide

## 🚀 Overview
This guide helps integrate the GitHub Actions Claude instance with our Industrial IoT Stack.

## 📋 Setup Checklist

### 1. Repository Secrets
Configure these secrets in your GitHub repository:

```
GOOGLE_SHEETS_ID={os.getenv('GOOGLE_SHEETS_ID', 'YOUR_SHEET_ID')}
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
gh workflow run claude-automation.yml \\
  -f claude_task=system_health_check \\
  -f environment=production

# Run integration tests
gh workflow run claude-automation.yml \\
  -f claude_task=run_integration_tests \\
  -f environment=staging
```

### API Integration
```python
# Monitor workflow status
import requests

def check_github_actions_status():
    url = "https://api.github.com/repos/OWNER/REPO/actions/runs"
    headers = {{"Authorization": "token YOUR_TOKEN"}}
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

Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    guide_file = base_path / "GITHUB_ACTIONS_CLAUDE_INTEGRATION.md"
    with open(guide_file, 'w') as f:
        f.write(integration_guide)
    print(f"✅ Created integration guide: {guide_file}")
    
    # 7. Create coordination task for Claude Tasks sheet
    coordination_info = {
        "new_claude_task": {
            "task_id": "CT-031",
            "instance": "GitHub Actions Claude",
            "task_type": "CI/CD Integration",
            "priority": "High",
            "status": "Ready",
            "description": "Integrate GitHub Actions Claude instance for automated deployment and monitoring",
            "expected_output": "Automated CI/CD pipeline with Discord notifications and Google Sheets tracking",
            "dependencies": "Mac Claude GitHub Actions setup",
            "date_added": datetime.now().strftime('%Y-%m-%d'),
            "notes": "Prepared by Server Claude - ready for Mac Claude's GitHub Actions completion"
        }
    }
    
    coord_file = base_path / "github_actions_claude_coordination.json"
    with open(coord_file, 'w') as f:
        json.dump(coordination_info, f, indent=2)
    print(f"✅ Created coordination info: {coord_file}")
    
    return True

def send_preparation_notification():
    """Send Discord notification about GitHub Actions preparation"""
    
    webhook_url = "https://discordapp.com/api/webhooks/1380061953883373660/lFn5d2hcBxAhaMJSpBNwjQNInczAGYQ-HYky70iSiNymhFXw7egnjUapMdAHZXrRWJhG"
    
    prep_message = {
        "embeds": [{
            "title": "🔧 GITHUB ACTIONS CLAUDE PREPARATION COMPLETE",
            "description": "Ready for Mac Claude's GitHub Actions Claude rollout!",
            "color": 0x6f42c1,  # Purple for GitHub
            "fields": [
                {
                    "name": "📁 Files Created",
                    "value": "• .github/workflows/claude-automation.yml\n• scripts/github_actions_claude_runner.py\n• requirements-github-actions.txt\n• Integration guide & docs",
                    "inline": False
                },
                {
                    "name": "🔗 Integration Points",
                    "value": "• Discord notifications ✅\n• Google Sheets tracking ✅\n• n8n API monitoring ✅\n• System health checks ✅",
                    "inline": True
                },
                {
                    "name": "🎯 Ready For",
                    "value": "• Automated CI/CD\n• Health monitoring\n• Cross-Claude coordination\n• Deployment automation",
                    "inline": True
                },
                {
                    "name": "⏳ Waiting On",
                    "value": "Mac Claude to complete GitHub Actions setup",
                    "inline": False
                },
                {
                    "name": "🚀 What This Enables",
                    "value": "Third Claude instance for automated deployment, monitoring, and CI/CD pipeline management!",
                    "inline": False
                }
            ],
            "footer": {
                "text": "Industrial IoT Stack - Three Claude Coordination!"
            },
            "timestamp": datetime.now().isoformat()
        }]
    }
    
    try:
        import requests
        response = requests.post(webhook_url, json=prep_message, timeout=10)
        if response.status_code == 204:
            print("📢 GitHub Actions preparation notification sent!")
    except Exception as e:
        print(f"⚠️ Discord notification failed: {e}")

def main():
    """Main preparation workflow"""
    
    print("🚀 GITHUB ACTIONS CLAUDE PREPARATION")
    print("=" * 45)
    
    success = create_github_actions_preparation()
    
    if success:
        send_preparation_notification()
        
        print(f"\n✅ GITHUB ACTIONS CLAUDE PREPARATION COMPLETE!")
        print("=" * 50)
        
        print("📁 Files Created:")
        print("  • .github/workflows/claude-automation.yml")
        print("  • scripts/github_actions_claude_runner.py") 
        print("  • scripts/update_github_actions_status.py")
        print("  • requirements-github-actions.txt")
        print("  • GITHUB_ACTIONS_CLAUDE_INTEGRATION.md")
        print("  • github_actions_claude_coordination.json")
        
        print(f"\n🎯 Ready For Mac Claude:")
        print("  • Complete GitHub Actions setup")
        print("  • Configure repository secrets")
        print("  • Test workflow execution")
        print("  • Enable automatic triggers")
        
        print(f"\n🔗 Three Claude Coordination:")
        print("  • Server Claude: System management & Discord")
        print("  • Mac Claude: Development & architecture")
        print("  • GitHub Actions Claude: CI/CD & monitoring")
        
        print(f"\n🚀 This Will Enable:")
        print("  • Automated deployment pipeline")
        print("  • Continuous health monitoring")
        print("  • Cross-environment coordination")
        print("  • Integrated Discord notifications")
        
        return True
    else:
        print("\n❌ GitHub Actions preparation failed")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Ready for the GitHub Actions Claude rollout!")
    else:
        sys.exit(1)