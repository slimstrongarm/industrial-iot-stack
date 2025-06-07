#!/usr/bin/env python3
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
