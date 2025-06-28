# Ignition Equipment Alert Script
# Sends equipment alerts to n8n API for processing
# Usage: Call from tag change scripts, expression tags, or scheduled scripts

import system
import json

# Configuration
N8N_API_URL = "http://172.28.214.170:5678/api/v1"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4"

def sendEquipmentAlert(equipmentId, equipmentType, location, alertType, value=None, threshold=None, description=""):
    """
    Send equipment alert to n8n API
    
    Args:
        equipmentId: Unique equipment identifier (e.g., "PUMP-001")
        equipmentType: Type of equipment (e.g., "Centrifugal Pump")
        location: Physical location (e.g., "Building A, Floor 2")
        alertType: Type of alert ("critical", "warning", "info", "fault")
        value: Current reading/value (optional)
        threshold: Alert threshold (optional)
        description: Alert description
    
    Returns:
        True if successful, False otherwise
    """
    
    try:
        # Prepare alert data
        alertData = {
            "equipmentId": equipmentId,
            "type": equipmentType,
            "location": location,
            "alertType": alertType,
            "value": value,
            "threshold": threshold,
            "description": description,
            "timestamp": system.date.now(),
            "source": "ignition"
        }
        
        # Determine MQTT topic based on alert type
        if alertType == "critical":
            topic = "sensors/critical"
        elif alertType == "fault":
            topic = "actuators/fault"
        else:
            topic = "equipment/alerts"
        
        # Prepare webhook trigger data
        webhookData = {
            "topic": topic,
            "payload": alertData
        }
        
        # Send to n8n webhook endpoint (if webhook trigger exists)
        headers = {
            "Content-Type": "application/json",
            "X-N8N-API-KEY": N8N_API_KEY
        }
        
        # Method 1: Direct webhook trigger (preferred)
        webhookUrl = "http://172.28.214.170:5678/webhook/ignition-alerts"
        
        try:
            response = system.net.httpPost(
                url=webhookUrl,
                postData=system.util.jsonEncode(webhookData),
                headerValues=headers,
                timeout=5000
            )
            
            if response.good:
                system.util.getLogger("EquipmentAlerts").info("Alert sent successfully: " + equipmentId)
                return True
            else:
                system.util.getLogger("EquipmentAlerts").warn("Webhook failed, trying API method")
        except:
            system.util.getLogger("EquipmentAlerts").warn("Webhook unavailable, using API method")
        
        # Method 2: Trigger workflow via API (fallback)
        workflowId = "PptMUA3BfrivzhG9"  # MQTT→WhatsApp workflow ID
        
        triggerUrl = N8N_API_URL + "/workflows/" + workflowId + "/execute"
        
        response = system.net.httpPost(
            url=triggerUrl,
            postData=system.util.jsonEncode({"data": webhookData}),
            headerValues=headers,
            timeout=10000
        )
        
        if response.good:
            system.util.getLogger("EquipmentAlerts").info("Alert triggered via API: " + equipmentId)
            return True
        else:
            system.util.getLogger("EquipmentAlerts").error("Failed to send alert: " + str(response.error))
            return False
            
    except Exception as e:
        system.util.getLogger("EquipmentAlerts").error("Exception in sendEquipmentAlert: " + str(e))
        return False

def sendCriticalAlert(equipmentId, equipmentType, location, value, threshold, description):
    """Send critical equipment alert"""
    return sendEquipmentAlert(equipmentId, equipmentType, location, "critical", value, threshold, description)

def sendWarningAlert(equipmentId, equipmentType, location, value, threshold, description):
    """Send warning equipment alert"""
    return sendEquipmentAlert(equipmentId, equipmentType, location, "warning", value, threshold, description)

def sendFaultAlert(equipmentId, equipmentType, location, description):
    """Send equipment fault alert"""
    return sendEquipmentAlert(equipmentId, equipmentType, location, "fault", None, None, description)

# Example usage functions that can be called from Ignition tags/expressions
def checkTemperatureSensor(tagPath, equipmentId, location, criticalThreshold=85, warningThreshold=75):
    """
    Check temperature sensor and send alerts if thresholds exceeded
    Call this from a tag change script on temperature tags
    """
    try:
        currentTemp = system.tag.readBlocking([tagPath])[0].value
        
        if currentTemp >= criticalThreshold:
            sendCriticalAlert(
                equipmentId=equipmentId,
                equipmentType="Temperature Sensor",
                location=location,
                value=currentTemp,
                threshold=criticalThreshold,
                description="Critical temperature exceeded - immediate action required"
            )
        elif currentTemp >= warningThreshold:
            sendWarningAlert(
                equipmentId=equipmentId,
                equipmentType="Temperature Sensor", 
                location=location,
                value=currentTemp,
                threshold=warningThreshold,
                description="Temperature warning - monitor closely"
            )
    except Exception as e:
        system.util.getLogger("EquipmentAlerts").error("Temperature check failed: " + str(e))

def checkPumpStatus(tagPath, equipmentId, location):
    """
    Check pump status and send fault alert if stopped unexpectedly
    Call this from a tag change script on pump status tags
    """
    try:
        pumpRunning = system.tag.readBlocking([tagPath])[0].value
        
        if not pumpRunning:
            sendFaultAlert(
                equipmentId=equipmentId,
                equipmentType="Centrifugal Pump",
                location=location,
                description="Pump stopped - check for mechanical issues"
            )
    except Exception as e:
        system.util.getLogger("EquipmentAlerts").error("Pump status check failed: " + str(e))

def checkVibrationLevels(tagPath, equipmentId, location, criticalThreshold=10.0, warningThreshold=7.5):
    """
    Check vibration levels and send alerts
    Call this from a tag change script on vibration sensor tags
    """
    try:
        vibration = system.tag.readBlocking([tagPath])[0].value
        
        if vibration >= criticalThreshold:
            sendCriticalAlert(
                equipmentId=equipmentId,
                equipmentType="Vibration Sensor",
                location=location,
                value=vibration,
                threshold=criticalThreshold,
                description="Critical vibration levels - stop equipment immediately"
            )
        elif vibration >= warningThreshold:
            sendWarningAlert(
                equipmentId=equipmentId,
                equipmentType="Vibration Sensor",
                location=location, 
                value=vibration,
                threshold=warningThreshold,
                description="Elevated vibration - schedule maintenance"
            )
    except Exception as e:
        system.util.getLogger("EquipmentAlerts").error("Vibration check failed: " + str(e))

# Scheduled function to send system health status
def sendSystemHealthStatus():
    """
    Send periodic system health status to n8n
    Configure this to run every 15 minutes via scheduled script
    """
    try:
        # Get system stats
        tagCount = len(system.tag.browse())
        
        # Send health status
        sendEquipmentAlert(
            equipmentId="IGNITION-GATEWAY",
            equipmentType="Ignition Gateway",
            location="Server Room",
            alertType="info",
            value=tagCount,
            description="System health check - " + str(tagCount) + " tags active"
        )
        
        system.util.getLogger("SystemHealth").info("Health status sent to n8n")
        
    except Exception as e:
        system.util.getLogger("SystemHealth").error("Health status failed: " + str(e))