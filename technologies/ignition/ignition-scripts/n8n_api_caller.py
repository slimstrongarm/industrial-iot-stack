# Ignition Gateway Script: N8N API Caller
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
