#!/usr/bin/env python3
"""
Create Ignition API scripts for Server Claude (CT-016)
"""

from pathlib import Path
import json

def create_ignition_scripts():
    """Create Ignition scripts that call n8n API"""
    
    # Create directory
    ignition_dir = Path.home() / 'Desktop/industrial-iot-stack/ignition-scripts'
    ignition_dir.mkdir(exist_ok=True)
    
    # N8N API caller script for Ignition
    n8n_api_script = '''# Ignition Gateway Script: N8N API Caller
# Place this in Ignition Gateway > Scripts > Project Library

import system
import java.net.URL as URL
import java.net.HttpURLConnection as HttpURLConnection
import java.io.OutputStreamWriter as OutputStreamWriter
import java.io.BufferedReader as BufferedReader
import java.io.InputStreamReader as InputStreamReader

def callN8nWorkflow(webhookUrl, alertData):
    """
    Call n8n webhook with alert data
    
    Args:
        webhookUrl (str): N8n webhook URL 
        alertData (dict): Alert information
    
    Returns:
        bool: True if successful
    """
    try:
        # Create JSON payload
        payload = system.util.jsonEncode(alertData)
        
        # Setup HTTP connection
        url = URL(webhookUrl)
        connection = url.openConnection()
        connection.setRequestMethod("POST")
        connection.setRequestProperty("Content-Type", "application/json")
        connection.setDoOutput(True)
        
        # Send data
        writer = OutputStreamWriter(connection.getOutputStream())
        writer.write(payload)
        writer.flush()
        writer.close()
        
        # Get response
        responseCode = connection.getResponseCode()
        
        if responseCode == 200:
            # Read response
            reader = BufferedReader(InputStreamReader(connection.getInputStream()))
            response = reader.readLine()
            reader.close()
            
            print("N8N webhook successful: %s" % response)
            return True
        else:
            print("N8N webhook failed with code: %d" % responseCode)
            return False
            
    except Exception as e:
        print("Error calling N8N API: %s" % str(e))
        return False

def triggerEquipmentAlert(equipmentName, alertType, severity, description):
    """
    Trigger equipment alert via N8N
    
    Args:
        equipmentName (str): Name of equipment
        alertType (str): Type of alert (temperature, pressure, etc.)
        severity (str): high, medium, low
        description (str): Alert description
    """
    
    # N8N webhook URL - update with actual URL
    webhookUrl = "http://localhost:5678/webhook/equipment-alert"
    
    # Create alert data
    alertData = {
        "timestamp": system.date.now(),
        "equipment": equipmentName,
        "alertType": alertType,
        "severity": severity,
        "description": description,
        "location": "Brewery Floor 1",  # Customize as needed
        "source": "Ignition Gateway"
    }
    
    # Call N8N
    success = callN8nWorkflow(webhookUrl, alertData)
    
    if success:
        print("Alert sent successfully for %s" % equipmentName)
    else:
        print("Failed to send alert for %s" % equipmentName)
    
    return success

# Example usage in Ignition alarm script:
def onAlarmStateChange(alarmEvent):
    """
    Call this from Ignition alarm pipeline
    """
    if alarmEvent.getState().getActiveState():
        # Alarm became active
        equipmentName = str(alarmEvent.getSource().getSource())
        alertType = "alarm_active"
        severity = "high" if "Critical" in alarmEvent.getDisplayName() else "medium"
        description = str(alarmEvent.getDisplayName())
        
        triggerEquipmentAlert(equipmentName, alertType, severity, description)

# Temperature monitoring function
def checkTemperatureAlerts():
    """
    Check temperature tags and trigger alerts
    Call this from scheduled script every 30 seconds
    """
    
    # Read temperature tags
    tempTags = [
        "[default]Brewery/Tank1/Temperature",
        "[default]Brewery/Tank2/Temperature", 
        "[default]Brewery/Boiler/Temperature"
    ]
    
    for tagPath in tempTags:
        try:
            tempValue = system.tag.readBlocking([tagPath])[0].value
            
            # Check thresholds
            if tempValue > 80:  # High temperature
                equipmentName = tagPath.split("/")[-2]  # Extract equipment name
                triggerEquipmentAlert(
                    equipmentName,
                    "high_temperature",
                    "high",
                    "Temperature exceeded 80°F: %.1f°F" % tempValue
                )
                
        except Exception as e:
            print("Error reading temperature tag %s: %s" % (tagPath, str(e)))
'''

    # Save Ignition script
    with open(ignition_dir / 'n8n_api_caller.py', 'w') as f:
        f.write(n8n_api_script)
    
    # Create setup instructions
    setup_instructions = '''# Ignition N8N API Integration Setup

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
'''

    with open(ignition_dir / 'SETUP_INSTRUCTIONS.md', 'w') as f:
        f.write(setup_instructions)
    
    print(f"✅ Created Ignition API scripts in: {ignition_dir}")
    return ignition_dir

if __name__ == "__main__":
    create_ignition_scripts()