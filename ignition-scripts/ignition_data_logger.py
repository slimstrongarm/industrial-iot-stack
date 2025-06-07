# Ignition Data Logger Script
# Logs equipment data to n8n for processing and storage in Google Sheets
# Usage: Call from scheduled scripts or tag change events

import system
import json

# Configuration
N8N_WEBHOOK_URL = "http://172.28.214.170:5678/webhook/ignition-data"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4"

def logEquipmentData(equipmentId, equipmentType, location, measurements, notes=""):
    """
    Log equipment data to Google Sheets via n8n
    
    Args:
        equipmentId: Equipment identifier
        equipmentType: Type of equipment
        location: Physical location
        measurements: Dictionary of measurement names and values
        notes: Optional notes
    
    Returns:
        True if successful, False otherwise
    """
    
    try:
        # Prepare data payload
        dataPayload = {
            "equipmentId": equipmentId,
            "equipmentType": equipmentType,
            "location": location,
            "measurements": measurements,
            "notes": notes,
            "timestamp": system.date.now(),
            "source": "ignition_logger"
        }
        
        # Send to n8n
        headers = {
            "Content-Type": "application/json",
            "X-N8N-API-KEY": N8N_API_KEY
        }
        
        response = system.net.httpPost(
            url=N8N_WEBHOOK_URL,
            postData=system.util.jsonEncode(dataPayload),
            headerValues=headers,
            timeout=5000
        )
        
        if response.good:
            system.util.getLogger("DataLogger").info("Data logged for: " + equipmentId)
            return True
        else:
            system.util.getLogger("DataLogger").error("Data logging failed: " + str(response.error))
            return False
            
    except Exception as e:
        system.util.getLogger("DataLogger").error("Exception in logEquipmentData: " + str(e))
        return False

def logHourlyData():
    """
    Log hourly equipment data for all monitored equipment
    Configure this to run every hour via scheduled script
    """
    
    equipment_list = [
        {
            "id": "PUMP-001",
            "type": "Centrifugal Pump",
            "location": "Building A",
            "tags": {
                "flow_rate": "[default]Equipment/Pump001/FlowRate",
                "pressure": "[default]Equipment/Pump001/Pressure",
                "temperature": "[default]Equipment/Pump001/Temperature",
                "vibration": "[default]Equipment/Pump001/Vibration",
                "status": "[default]Equipment/Pump001/Running"
            }
        },
        {
            "id": "TEMP-001", 
            "type": "Temperature Sensor",
            "location": "Reactor Room",
            "tags": {
                "temperature": "[default]Sensors/Temperature/Reactor001",
                "humidity": "[default]Sensors/Humidity/Reactor001"
            }
        }
        # Add more equipment as needed
    ]
    
    for equipment in equipment_list:
        try:
            # Read all tags for this equipment
            tag_paths = equipment["tags"].values()
            tag_values = system.tag.readBlocking(tag_paths)
            
            # Create measurements dictionary
            measurements = {}
            for i, (measurement_name, tag_path) in enumerate(equipment["tags"].items()):
                if i < len(tag_values) and tag_values[i].quality.isGood():
                    measurements[measurement_name] = tag_values[i].value
                else:
                    measurements[measurement_name] = None
            
            # Log the data
            logEquipmentData(
                equipmentId=equipment["id"],
                equipmentType=equipment["type"],
                location=equipment["location"],
                measurements=measurements,
                notes="Hourly data collection"
            )
            
        except Exception as e:
            system.util.getLogger("DataLogger").error("Failed to log data for " + equipment["id"] + ": " + str(e))

def logManualReading(equipmentId, measurementType, value, operator="Auto", notes=""):
    """
    Log manual equipment reading
    Can be called from Vision screens or scripts
    """
    
    measurements = {
        measurementType: value,
        "reading_type": "manual",
        "operator": operator
    }
    
    return logEquipmentData(
        equipmentId=equipmentId,
        equipmentType="Manual Reading",
        location="Field",
        measurements=measurements,
        notes=notes
    )