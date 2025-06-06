# Ignition N8N API Integration Setup

## Installation Steps

### 1. Copy Script to Ignition
1. Open Ignition Designer
2. Go to Project > Scripts > Project Library
3. Create new script: "N8nApiCaller"
4. Copy contents of `n8n_api_caller.py`

### 2. Configure N8N Webhook URL
Update the webhook URL in the script:
```python
webhookUrl = "http://YOUR_SERVER:5678/webhook/equipment-alert"
```

### 3. Setup Alarm Integration
- Add `onAlarmStateChange()` to alarm pipelines
- Configure alarm priorities to trigger appropriate severity levels

### 4. Schedule Temperature Monitoring
- Create Gateway Timer script
- Call `checkTemperatureAlerts()` every 30 seconds
- Customize temperature thresholds as needed

### 5. Test Integration
```python
# Test call from Ignition Script Console
import N8nApiCaller
N8nApiCaller.triggerEquipmentAlert("TestEquipment", "test", "low", "Test alert from Ignition")
```

## Customization

### Equipment Names
Update equipment names to match your tag structure:
- Tank1, Tank2, Boiler (examples)
- Modify `checkTemperatureAlerts()` for your specific tags

### Alert Types
- temperature_high/low
- pressure_high/low  
- equipment_offline
- maintenance_due
- alarm_active

### Severity Levels
- high: Immediate attention required
- medium: Monitor closely
- low: Informational

## N8N Workflow Requirements

The N8N workflow should expect this JSON structure:
```json
{
    "timestamp": "2025-06-04T10:30:00Z",
    "equipment": "Tank1", 
    "alertType": "high_temperature",
    "severity": "high",
    "description": "Temperature exceeded 80°F: 85.2°F",
    "location": "Brewery Floor 1",
    "source": "Ignition Gateway"
}
```

Server Claude: Deploy this after n8n is running and test the integration.
