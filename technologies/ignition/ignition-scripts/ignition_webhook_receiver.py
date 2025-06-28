# Ignition Webhook Receiver Script
# Receives commands from n8n and executes them in Ignition
# Usage: Set up as Gateway Event Script for Message Handler

import system
import json

def handleN8nCommand(message):
    """
    Handle incoming command from n8n
    Configure this in Gateway Events → Message Handler
    """
    
    try:
        # Parse the incoming message
        if hasattr(message, 'payload'):
            command_data = system.util.jsonDecode(message.payload)
        else:
            command_data = message
        
        command_type = command_data.get("command", "")
        equipment_id = command_data.get("equipmentId", "")
        
        system.util.getLogger("N8nCommands").info("Received command: " + command_type + " for " + equipment_id)
        
        # Execute command based on type
        if command_type == "start_equipment":
            startEquipment(equipment_id, command_data)
        elif command_type == "stop_equipment":
            stopEquipment(equipment_id, command_data)
        elif command_type == "set_setpoint":
            setSetpoint(equipment_id, command_data)
        elif command_type == "acknowledge_alarm":
            acknowledgeAlarm(equipment_id, command_data)
        elif command_type == "request_status":
            sendStatusUpdate(equipment_id, command_data)
        else:
            system.util.getLogger("N8nCommands").warn("Unknown command type: " + command_type)
            
    except Exception as e:
        system.util.getLogger("N8nCommands").error("Error handling n8n command: " + str(e))

def startEquipment(equipment_id, command_data):
    """Start equipment based on equipment ID"""
    
    # Map equipment IDs to control tags
    equipment_controls = {
        "PUMP-001": "[default]Equipment/Pump001/StartCommand",
        "VALVE-001": "[default]Equipment/Valve001/OpenCommand",
        "MOTOR-001": "[default]Equipment/Motor001/StartCommand"
    }
    
    if equipment_id in equipment_controls:
        tag_path = equipment_controls[equipment_id]
        system.tag.writeBlocking([tag_path], [True])
        
        system.util.getLogger("N8nCommands").info("Started equipment: " + equipment_id)
        
        # Send confirmation back to n8n
        sendCommandConfirmation(equipment_id, "start_equipment", "success")
    else:
        system.util.getLogger("N8nCommands").error("Unknown equipment ID: " + equipment_id)
        sendCommandConfirmation(equipment_id, "start_equipment", "failed - unknown equipment")

def stopEquipment(equipment_id, command_data):
    """Stop equipment based on equipment ID"""
    
    equipment_controls = {
        "PUMP-001": "[default]Equipment/Pump001/StopCommand",
        "VALVE-001": "[default]Equipment/Valve001/CloseCommand", 
        "MOTOR-001": "[default]Equipment/Motor001/StopCommand"
    }
    
    if equipment_id in equipment_controls:
        tag_path = equipment_controls[equipment_id]
        system.tag.writeBlocking([tag_path], [True])
        
        system.util.getLogger("N8nCommands").info("Stopped equipment: " + equipment_id)
        sendCommandConfirmation(equipment_id, "stop_equipment", "success")
    else:
        system.util.getLogger("N8nCommands").error("Unknown equipment ID: " + equipment_id)
        sendCommandConfirmation(equipment_id, "stop_equipment", "failed - unknown equipment")

def setSetpoint(equipment_id, command_data):
    """Set equipment setpoint"""
    
    setpoint_value = command_data.get("setpoint", 0)
    
    equipment_setpoints = {
        "TEMP-CTRL-001": "[default]Controllers/Temperature001/Setpoint",
        "PRESSURE-CTRL-001": "[default]Controllers/Pressure001/Setpoint",
        "FLOW-CTRL-001": "[default]Controllers/Flow001/Setpoint"
    }
    
    if equipment_id in equipment_setpoints:
        tag_path = equipment_setpoints[equipment_id]
        system.tag.writeBlocking([tag_path], [setpoint_value])
        
        system.util.getLogger("N8nCommands").info("Set setpoint for " + equipment_id + " to " + str(setpoint_value))
        sendCommandConfirmation(equipment_id, "set_setpoint", "success - setpoint: " + str(setpoint_value))
    else:
        system.util.getLogger("N8nCommands").error("Unknown controller ID: " + equipment_id)
        sendCommandConfirmation(equipment_id, "set_setpoint", "failed - unknown controller")

def sendCommandConfirmation(equipment_id, command, status):
    """Send command confirmation back to n8n"""
    
    confirmation = {
        "equipmentId": equipment_id,
        "command": command,
        "status": status,
        "timestamp": system.date.now(),
        "source": "ignition_gateway"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = system.net.httpPost(
            url="http://172.28.214.170:5678/webhook/ignition-confirmations",
            postData=system.util.jsonEncode(confirmation),
            headerValues=headers,
            timeout=5000
        )
        
        if response.good:
            system.util.getLogger("N8nCommands").info("Confirmation sent for: " + equipment_id)
        else:
            system.util.getLogger("N8nCommands").warn("Failed to send confirmation: " + str(response.error))
            
    except Exception as e:
        system.util.getLogger("N8nCommands").error("Exception sending confirmation: " + str(e))