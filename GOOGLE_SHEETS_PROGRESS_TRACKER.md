# Google Sheets Progress Tracker Integration

## 📊 Overview
Centralized progress tracking system using Google Sheets for real-time visibility of all Industrial IoT Stack tasks, deployments, and agent activities.

## 🎯 Google Sheets Structure

### Master Progress Sheet
**Sheet Name**: `IoT_Stack_Progress_Master`
**URL**: `https://docs.google.com/spreadsheets/d/[YOUR_SHEET_ID]/`

### Sheet Tabs:

#### 1. **Docker Migration Tasks**
| Task ID | Task Description | Status | Priority | Assigned To | Start Date | Due Date | Completion % | Notes | Dependencies |
|---------|-----------------|---------|----------|-------------|------------|----------|--------------|-------|--------------|
| DM-001 | Create Docker Compose for Ignition | In Progress | High | Server Claude | 2025-06-01 | 2025-06-03 | 25% | Base config done | - |
| DM-002 | Research Flint Docker integration | Pending | High | MacBook Claude | - | 2025-06-02 | 0% | - | DM-001 |
| DM-003 | Design modular stack architecture | Pending | High | MacBook Claude | - | 2025-06-04 | 0% | - | - |

#### 2. **System Components Status**
| Component | Docker Status | Health Check | Version | Last Updated | Uptime | CPU Usage | Memory Usage | Alerts |
|-----------|--------------|--------------|---------|--------------|---------|-----------|--------------|--------|
| Ignition Gateway | Running | ✅ Healthy | 8.1.43 | 2025-06-01 14:30 | 2d 4h | 12% | 2.1GB | None |
| Node-RED | Running | ✅ Healthy | 3.1.9 | 2025-06-01 14:30 | 2d 4h | 8% | 512MB | None |
| MQTT Broker | Running | ✅ Healthy | 2.0.18 | 2025-06-01 14:30 | 2d 4h | 2% | 128MB | None |

#### 3. **Project Migration Tracker**
| Project Name | Local Status | Export Status | Transfer Status | Import Status | Validation | VS Code Access | Notes |
|--------------|--------------|---------------|-----------------|---------------|------------|----------------|-------|
| test_run_01 | ✅ Ready | ⏳ Pending | - | - | - | - | Main test project |
| brewery_control | ✅ Ready | ⏳ Pending | - | - | - | - | Production templates |
| steel_bonnet_hmi | ✅ Ready | ⏳ Pending | - | - | - | - | HMI screens |

#### 4. **Agent Activities**
| Timestamp | Agent Type | Task | Status | Duration | Output | Next Action |
|-----------|------------|------|---------|----------|---------|-------------|
| 2025-06-01 14:45 | MacBook Claude | Docker strategy planning | Complete | 45 min | DOCKER_MIGRATION_STRATEGY.md | Server deployment |
| 2025-06-01 15:30 | Server Claude | Docker setup | Pending | - | - | Execute compose files |

#### 5. **Integration Checklist**
| Integration Point | Status | Test Result | Documentation | Production Ready |
|-------------------|---------|-------------|---------------|------------------|
| Ignition ↔ Flint | 🔄 In Progress | - | ✅ Complete | ❌ No |
| Node-RED ↔ MQTT | ✅ Complete | ✅ Pass | ✅ Complete | ✅ Yes |
| MQTT ↔ Ignition | 🔄 In Progress | ⚠️ Partial | 📝 In Progress | ❌ No |

## 🔄 Automation Scripts

### Python Script for Google Sheets Updates
```python
#!/usr/bin/env python3
# File: scripts/update_google_sheets.py

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime
import subprocess

# Google Sheets configuration
SHEET_ID = 'your-sheet-id-here'
CREDS_FILE = 'path/to/google-credentials.json'

class ProgressTracker:
    def __init__(self):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(SHEET_ID)
    
    def update_docker_status(self):
        """Update Docker container status"""
        worksheet = self.sheet.worksheet('System Components Status')
        
        # Get Docker status
        docker_ps = subprocess.run(
            ['docker', 'ps', '--format', 'json'],
            capture_output=True,
            text=True
        )
        
        containers = json.loads(docker_ps.stdout)
        for i, container in enumerate(containers, start=2):  # Start at row 2
            worksheet.update(f'A{i}', container['Names'])
            worksheet.update(f'B{i}', container['Status'])
            worksheet.update(f'C{i}', '✅ Healthy' if 'healthy' in container['Status'] else '⚠️ Check')
            worksheet.update(f'E{i}', datetime.now().strftime('%Y-%m-%d %H:%M'))
    
    def add_task(self, task_data):
        """Add new task to Docker Migration Tasks"""
        worksheet = self.sheet.worksheet('Docker Migration Tasks')
        worksheet.append_row([
            task_data['id'],
            task_data['description'],
            task_data['status'],
            task_data['priority'],
            task_data['assigned_to'],
            task_data['start_date'],
            task_data['due_date'],
            task_data['completion'],
            task_data['notes'],
            task_data['dependencies']
        ])
    
    def log_agent_activity(self, activity):
        """Log agent activity"""
        worksheet = self.sheet.worksheet('Agent Activities')
        worksheet.append_row([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            activity['agent_type'],
            activity['task'],
            activity['status'],
            activity['duration'],
            activity['output'],
            activity['next_action']
        ])

# Usage example
if __name__ == "__main__":
    tracker = ProgressTracker()
    
    # Update Docker status
    tracker.update_docker_status()
    
    # Add new task
    tracker.add_task({
        'id': 'DM-004',
        'description': 'Configure Google Sheets integration',
        'status': 'Complete',
        'priority': 'High',
        'assigned_to': 'MacBook Claude',
        'start_date': '2025-06-01',
        'due_date': '2025-06-01',
        'completion': '100%',
        'notes': 'Integration scripts created',
        'dependencies': 'None'
    })
```

### Node-RED Flow for Real-time Updates
```json
{
  "id": "google-sheets-updater",
  "type": "tab",
  "label": "Google Sheets Progress Tracker",
  "flows": [
    {
      "id": "1",
      "type": "inject",
      "name": "Every 5 minutes",
      "props": [{"p": "payload"}],
      "repeat": "300",
      "crontab": "",
      "once": true
    },
    {
      "id": "2",
      "type": "exec",
      "command": "docker ps --format json",
      "name": "Get Docker Status"
    },
    {
      "id": "3",
      "type": "function",
      "name": "Format for Sheets",
      "func": "// Parse Docker output and format for Google Sheets\nconst containers = JSON.parse(msg.payload);\nmsg.payload = containers.map(c => ({\n    name: c.Names,\n    status: c.Status,\n    health: c.Status.includes('healthy') ? '✅' : '⚠️',\n    updated: new Date().toISOString()\n}));\nreturn msg;"
    },
    {
      "id": "4",
      "type": "google-sheets",
      "name": "Update Sheet",
      "sheet": "IoT_Stack_Progress_Master",
      "tab": "System Components Status"
    }
  ]
}
```

## 📱 Mobile Dashboard View

### Google Sheets Mobile App Configuration
1. **Install Google Sheets app** on mobile devices
2. **Star the IoT_Stack_Progress_Master** sheet for quick access
3. **Enable notifications** for status changes

### Key Mobile Views:
- **Summary Dashboard**: Pivot table showing overall progress
- **Alerts View**: Filtered view of components with issues
- **Today's Tasks**: Filtered by due date = TODAY()
- **Agent Activity Log**: Last 24 hours of activities

## 🔔 Automated Alerts

### Google Apps Script for Alerts
```javascript
// In Google Sheets: Extensions > Apps Script
function checkSystemHealth() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet();
  const statusSheet = sheet.getSheetByName('System Components Status');
  const data = statusSheet.getDataRange().getValues();
  
  const alerts = [];
  
  // Check for unhealthy components
  for (let i = 1; i < data.length; i++) {
    if (data[i][2] && data[i][2].includes('⚠️')) {
      alerts.push(`${data[i][0]} is unhealthy: ${data[i][1]}`);
    }
  }
  
  // Send email if alerts exist
  if (alerts.length > 0) {
    MailApp.sendEmail({
      to: 'your-email@example.com',
      subject: 'IoT Stack Alert',
      body: alerts.join('\n')
    });
  }
}

// Set trigger to run every 15 minutes
function setupTriggers() {
  ScriptApp.newTrigger('checkSystemHealth')
    .timeBased()
    .everyMinutes(15)
    .create();
}
```

## 🔗 Integration with Industrial IoT Stack

### Environment Variables
```bash
# Add to .env file
GOOGLE_SHEETS_ID=your-sheet-id-here
GOOGLE_CREDS_PATH=/path/to/credentials.json
PROGRESS_UPDATE_INTERVAL=300  # 5 minutes
```

### Docker Service for Updates
```yaml
# Add to docker-compose.yml
progress-tracker:
  build: ./progress-tracker
  container_name: progress-tracker
  environment:
    - GOOGLE_SHEETS_ID=${GOOGLE_SHEETS_ID}
    - GOOGLE_CREDS_PATH=/creds/google-credentials.json
  volumes:
    - ./google-credentials.json:/creds/google-credentials.json:ro
    - /var/run/docker.sock:/var/run/docker.sock:ro
  restart: unless-stopped
  networks:
    - iot-stack
```

## 📊 Quick Access Links

### Sheet Templates
1. **[Copy Master Template](https://docs.google.com/spreadsheets/d/[TEMPLATE_ID]/copy)**
2. **[View Sample Dashboard](https://docs.google.com/spreadsheets/d/[SAMPLE_ID]/)**

### Setup Checklist
- [ ] Create Google Sheets from template
- [ ] Set up service account credentials
- [ ] Configure automation scripts
- [ ] Test data population
- [ ] Set up mobile access
- [ ] Configure alerts
- [ ] Share with team members

## 🚀 Benefits

1. **Single Source of Truth**: All progress visible in one place
2. **Real-time Updates**: Automated sync every 5 minutes
3. **Mobile Access**: Monitor from anywhere
4. **Team Collaboration**: Multiple users can view/update
5. **Historical Tracking**: Complete audit trail
6. **Automated Alerts**: Proactive issue notification

---

**Next Steps**: 
1. Create Google Sheets from template
2. Set up service account for API access
3. Deploy progress tracker container
4. Test automated updates