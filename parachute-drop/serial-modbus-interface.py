#!/usr/bin/env python3
"""
🪂 Parachute Drop - Serial/Modbus Interface
Legacy protocol support for older industrial equipment
"""

import serial
import time
import json
import struct
import threading
from pymodbus.client.sync import ModbusSerialClient
from pymodbus.client.sync import ModbusTcpClient
import minimalmodbus
import paho.mqtt.client as mqtt

class SerialModbusInterface:
    def __init__(self, mqtt_client=None):
        self.serial_ports = []
        self.modbus_devices = {}
        self.mqtt_client = mqtt_client
        self.scanning = False
        
    def scan_serial_ports(self):
        """Scan for available serial ports"""
        import serial.tools.list_ports
        
        ports = serial.tools.list_ports.comports()
        available_ports = []
        
        for port in ports:
            port_info = {
                "device": port.device,
                "description": port.description,
                "hwid": port.hwid,
                "manufacturer": getattr(port, 'manufacturer', 'Unknown')
            }
            available_ports.append(port_info)
            print(f"📡 Found serial port: {port.device} - {port.description}")
            
        self.serial_ports = available_ports
        return available_ports
    
    def scan_modbus_rtu(self, port="/dev/ttyUSB0", baudrates=[9600, 19200, 38400]):
        """Scan for Modbus RTU devices across different baud rates"""
        discovered_devices = []
        
        for baud in baudrates:
            print(f"🔍 Scanning Modbus RTU at {port}, {baud} baud...")
            
            try:
                # Scan slave addresses 1-247
                for slave_id in range(1, 248):
                    try:
                        instrument = minimalmodbus.Instrument(port, slave_id)
                        instrument.serial.baudrate = baud
                        instrument.serial.timeout = 0.5
                        instrument.mode = minimalmodbus.MODE_RTU
                        
                        # Try to read a holding register
                        value = instrument.read_register(1, 0)
                        
                        device = {
                            "slave_id": slave_id,
                            "port": port,
                            "baud": baud,
                            "protocol": "Modbus RTU",
                            "test_register": {"address": 1, "value": value},
                            "discovered_registers": self.scan_device_registers(instrument)
                        }
                        
                        discovered_devices.append(device)
                        print(f"✅ Found Modbus device: Slave {slave_id} at {baud} baud")
                        
                        # Publish to MQTT
                        if self.mqtt_client:
                            topic = f"parachute/modbus/device_{slave_id}/status"
                            self.mqtt_client.publish(topic, "online")
                            
                    except Exception as e:
                        # Device not found at this address/baud
                        continue
                        
            except Exception as e:
                print(f"❌ Error scanning {port} at {baud}: {e}")
                
        self.modbus_devices[port] = discovered_devices
        return discovered_devices
    
    def scan_device_registers(self, instrument, max_registers=50):
        """Scan a Modbus device for readable registers"""
        registers = []
        
        # Common register types to scan
        register_types = [
            {"name": "Holding Registers", "function": "read_register", "start": 1},
            {"name": "Input Registers", "function": "read_register", "start": 30001},
            {"name": "Coils", "function": "read_bit", "start": 1},
            {"name": "Discrete Inputs", "function": "read_bit", "start": 10001}
        ]
        
        for reg_type in register_types:
            for addr in range(reg_type["start"], reg_type["start"] + max_registers):
                try:
                    if reg_type["function"] == "read_register":
                        value = instrument.read_register(addr, 0)
                        purpose = self.guess_register_purpose(addr, value)
                    else:
                        value = instrument.read_bit(addr)
                        purpose = self.guess_bit_purpose(addr, value)
                    
                    register = {
                        "address": addr,
                        "type": reg_type["name"],
                        "value": value,
                        "purpose": purpose,
                        "readable": True
                    }
                    registers.append(register)
                    
                except Exception:
                    # Register not readable
                    continue
                    
        return registers[:20]  # Limit to first 20 found registers
    
    def guess_register_purpose(self, address, value):
        """Guess register purpose based on address and value patterns"""
        
        # Common Modbus register purposes by address range
        if 1 <= address <= 100:
            if 0 <= value <= 100:
                return "Process Variable (%)"
            elif 0 <= value <= 1000:
                return "Temperature or Pressure"
            elif value in [0, 1]:
                return "Status Flag"
        
        elif 101 <= address <= 200:
            return "Setpoint or Configuration"
            
        elif 201 <= address <= 300:
            return "Control Output"
            
        # Value-based guessing
        if 20 <= value <= 80:
            return "Temperature (°C)"
        elif 68 <= value <= 176:
            return "Temperature (°F)"
        elif 0 <= value <= 300:
            return "Pressure (PSI)"
        elif value in [0, 1]:
            return "Digital Status"
            
        return "Unknown Process Variable"
    
    def guess_bit_purpose(self, address, value):
        """Guess bit purpose based on address"""
        if 1 <= address <= 100:
            return "Control Bit"
        elif 101 <= address <= 200:
            return "Status Bit"
        elif address > 10000:
            return "Input Status"
        else:
            return "Digital I/O"
    
    def start_continuous_monitoring(self, port, slave_id, baud=9600, interval=5):
        """Start continuous monitoring of a Modbus device"""
        def monitor_loop():
            try:
                instrument = minimalmodbus.Instrument(port, slave_id)
                instrument.serial.baudrate = baud
                instrument.serial.timeout = 1.0
                instrument.mode = minimalmodbus.MODE_RTU
                
                while self.scanning:
                    try:
                        # Read key registers
                        for reg_addr in range(1, 21):  # Monitor first 20 registers
                            try:
                                value = instrument.read_register(reg_addr, 0)
                                
                                # Publish to MQTT
                                if self.mqtt_client:
                                    topic = f"parachute/modbus/slave_{slave_id}/reg_{reg_addr}"
                                    payload = {
                                        "value": value,
                                        "timestamp": time.time(),
                                        "address": reg_addr,
                                        "slave_id": slave_id
                                    }
                                    self.mqtt_client.publish(topic, json.dumps(payload))
                                    
                            except Exception:
                                continue
                                
                        time.sleep(interval)
                        
                    except Exception as e:
                        print(f"❌ Monitoring error for slave {slave_id}: {e}")
                        time.sleep(interval * 2)  # Longer delay on error
                        
            except Exception as e:
                print(f"❌ Failed to start monitoring for slave {slave_id}: {e}")
        
        self.scanning = True
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
        print(f"📊 Started monitoring Modbus slave {slave_id}")
    
    def scan_common_protocols(self, port="/dev/ttyUSB0"):
        """Scan for common serial protocols beyond Modbus"""
        protocols = {
            "Modbus RTU": [9600, 19200, 38400],
            "BACnet MS/TP": [9600, 19200, 38400, 76800],
            "Profibus": [9600, 19200, 45450, 93750],
            "DF1": [9600, 19200, 38400]  # Allen-Bradley
        }
        
        discovered = {}
        
        for protocol, bauds in protocols.items():
            print(f"🔍 Scanning for {protocol}...")
            
            for baud in bauds:
                try:
                    ser = serial.Serial(port, baud, timeout=1)
                    
                    # Send protocol-specific test command
                    if protocol == "Modbus RTU":
                        # Already handled by scan_modbus_rtu
                        continue
                    elif protocol == "BACnet MS/TP":
                        # BACnet test frame
                        test_frame = b'\\x55\\xFF\\x05\\x0C\\x00\\x01\\x00\\x02\\x00\\x00'
                        ser.write(test_frame)
                    elif protocol == "DF1":
                        # DF1 test command
                        test_frame = b'\\x10\\x02\\x07\\x00\\x00\\x00\\x00\\x00\\x00\\x10\\x03'
                        ser.write(test_frame)
                    
                    response = ser.read(100)
                    if len(response) > 0:
                        discovered[protocol] = {
                            "baud": baud,
                            "response_length": len(response),
                            "response_hex": response.hex()
                        }
                        print(f"✅ {protocol} response at {baud} baud")
                    
                    ser.close()
                    
                except Exception:
                    continue
        
        return discovered
    
    def generate_node_red_flows(self, discovered_devices):
        """Generate Node-RED flows for discovered Modbus devices"""
        flows = []
        
        for port, devices in self.modbus_devices.items():
            for device in devices:
                slave_id = device["slave_id"]
                
                # Create Modbus read node
                modbus_node = {
                    "id": f"modbus_read_{slave_id}",
                    "type": "modbus-read",
                    "name": f"Modbus Slave {slave_id}",
                    "topic": "",
                    "showStatusActivities": True,
                    "logIOActivities": False,
                    "unitid": slave_id,
                    "dataType": "HoldingRegister",
                    "adr": "1",
                    "quantity": "10",
                    "rate": "5",
                    "rateUnit": "s",
                    "server": "modbus_server",
                    "x": 200,
                    "y": 100 + (slave_id * 100),
                    "wires": [[f"mqtt_out_{slave_id}"]]
                }
                
                # Create MQTT output node
                mqtt_node = {
                    "id": f"mqtt_out_{slave_id}",
                    "type": "mqtt out",
                    "name": f"Publish Slave {slave_id}",
                    "topic": f"parachute/modbus/slave_{slave_id}/data",
                    "qos": "1",
                    "retain": "false",
                    "broker": "mqtt_broker",
                    "x": 500,
                    "y": 100 + (slave_id * 100),
                    "wires": []
                }
                
                flows.extend([modbus_node, mqtt_node])
        
        return flows

def main():
    print("🪂 PARACHUTE DROP - Serial/Modbus Interface Starting...")
    
    # Initialize MQTT client
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
    
    interface = SerialModbusInterface(mqtt_client)
    
    # Scan for serial ports
    ports = interface.scan_serial_ports()
    
    # Scan for Modbus devices on each port
    for port_info in ports:
        port = port_info["device"]
        if "/dev/ttyUSB" in port or "/dev/ttyS" in port:
            devices = interface.scan_modbus_rtu(port)
            
            # Start monitoring found devices
            for device in devices:
                interface.start_continuous_monitoring(
                    port, 
                    device["slave_id"], 
                    device["baud"]
                )
    
    # Generate Node-RED flows
    flows = interface.generate_node_red_flows(interface.modbus_devices)
    
    # Save results
    results = {
        "serial_ports": interface.serial_ports,
        "modbus_devices": interface.modbus_devices,
        "node_red_flows": flows,
        "timestamp": time.time()
    }
    
    with open('/home/pi/parachute_drop/serial_scan_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("✅ Serial/Modbus scan complete!")
    print(f"📊 Found {len(interface.serial_ports)} serial ports")
    print(f"📡 Discovered {sum(len(devices) for devices in interface.modbus_devices.values())} Modbus devices")
    
    return results

if __name__ == "__main__":
    main()