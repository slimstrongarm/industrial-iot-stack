#!/usr/bin/env python3
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
        message = f"**System Health Check Complete**\n"
        message += f"Environment: {config['environment']}\n"
        message += f"Overall Status: {overall_status}\n"
        
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
