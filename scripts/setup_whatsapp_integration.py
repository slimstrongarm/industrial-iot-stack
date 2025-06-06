#!/usr/bin/env python3
"""
WhatsApp Integration Setup - Create a simple MQTT to WhatsApp alert system
This will work without needing complex n8n workflow imports
"""

import json
import paho.mqtt.client as mqtt
import requests
import time
from datetime import datetime
import threading

class WhatsAppAlertSystem:
    def __init__(self):
        self.mqtt_host = "localhost"  # Use localhost for host-based scripts
        self.mqtt_port = 1883
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        # Discord webhook for alerts (already working)
        with open('discord_webhook_config.json', 'r') as f:
            self.discord_config = json.load(f)
        
        self.alert_webhook = self.discord_config['discord']['alerts_webhook']
        
    def on_connect(self, client, userdata, flags, rc):
        """Callback for MQTT connection"""
        if rc == 0:
            print("✅ Connected to MQTT broker")
            # Subscribe to alert topics
            topics = [
                "equipment/alerts",
                "sensors/critical", 
                "actuators/fault"
            ]
            for topic in topics:
                client.subscribe(topic)
                print(f"📡 Subscribed to: {topic}")
        else:
            print(f"❌ Failed to connect to MQTT broker: {rc}")
    
    def on_message(self, client, userdata, msg):
        """Process incoming MQTT alerts"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            
            print(f"\n🚨 Alert received on {topic}")
            print(f"📋 Payload: {json.dumps(payload, indent=2)}")
            
            # Process the alert
            self.process_alert(topic, payload)
            
        except Exception as e:
            print(f"❌ Error processing message: {e}")
    
    def process_alert(self, topic, payload):
        """Process and route alerts"""
        # Extract alert data
        equipment_id = payload.get('equipmentId', 'unknown')
        equipment_type = payload.get('type', 'equipment')
        location = payload.get('location', 'unknown location')
        value = payload.get('value', 'N/A')
        threshold = payload.get('threshold', 'N/A')
        description = payload.get('description', 'Equipment alert')
        
        # Determine severity
        severity = 'critical' if any(word in topic for word in ['critical', 'fault', 'emergency']) else 'warning'
        
        # Create alert message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # For now, send to Discord (WhatsApp integration would go here)
        self.send_discord_alert(equipment_id, equipment_type, location, value, threshold, description, severity, timestamp)
        
        # Log to Google Sheets (if available)
        self.log_to_sheets(topic, payload, severity, timestamp)
        
        # Simulate WhatsApp alert (placeholder for actual WhatsApp API)
        self.simulate_whatsapp_alert(equipment_id, equipment_type, location, description, severity, timestamp)
    
    def send_discord_alert(self, equipment_id, equipment_type, location, value, threshold, description, severity, timestamp):
        """Send alert to Discord"""
        severity_emoji = "🚨" if severity == 'critical' else "⚠️"
        severity_color = 0xff0000 if severity == 'critical' else 0xff9900
        
        embed = {
            "title": f"{severity_emoji} Industrial IoT Equipment Alert",
            "description": f"**{severity.upper()} Alert Detected**",
            "color": severity_color,
            "fields": [
                {"name": "🏭 Equipment", "value": f"{equipment_type} ({equipment_id})", "inline": True},
                {"name": "📍 Location", "value": location, "inline": True},
                {"name": "📊 Current Value", "value": str(value), "inline": True},
                {"name": "🎯 Threshold", "value": str(threshold), "inline": True},
                {"name": "⏰ Time", "value": timestamp, "inline": True},
                {"name": "🔧 Description", "value": description, "inline": False}
            ],
            "footer": {"text": "Industrial IoT Monitoring - MQTT to Discord"},
            "timestamp": datetime.now().isoformat()
        }
        
        message = {"embeds": [embed]}
        
        try:
            response = requests.post(self.alert_webhook, json=message)
            if response.status_code == 204:
                print("✅ Discord alert sent successfully")
            else:
                print(f"⚠️ Discord alert failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Discord alert error: {e}")
    
    def simulate_whatsapp_alert(self, equipment_id, equipment_type, location, description, severity, timestamp):
        """Simulate WhatsApp alert (placeholder for actual integration)"""
        whatsapp_message = f"""🚨 *IoT Equipment Alert*

🏭 *Equipment:* {equipment_type} ({equipment_id})
📍 *Location:* {location}
⏰ *Time:* {timestamp}
🎯 *Severity:* {severity.upper()}

📋 *Description:* {description}

_Industrial IoT Monitoring System_"""
        
        print("\n📱 WhatsApp Alert (Simulated):")
        print("=" * 40)
        print(whatsapp_message)
        print("=" * 40)
        
        # TODO: Replace with actual WhatsApp API call
        # This would typically use WhatsApp Business API:
        # - Meta's WhatsApp Business API
        # - Twilio WhatsApp API
        # - Or other WhatsApp service provider
    
    def log_to_sheets(self, topic, payload, severity, timestamp):
        """Log alert to Google Sheets (placeholder)"""
        print(f"📊 Logging to Google Sheets: {topic} - {severity} - {timestamp}")
        # This would use the existing Google Sheets integration
    
    def start_monitoring(self):
        """Start the MQTT monitoring"""
        print("🚀 Starting WhatsApp Alert Integration")
        print("=" * 50)
        
        try:
            self.client.connect(self.mqtt_host, self.mqtt_port, 60)
            print(f"🔌 Connecting to MQTT broker at {self.mqtt_host}:{self.mqtt_port}")
            
            # Start the MQTT loop in a separate thread
            self.client.loop_start()
            
            print("✅ WhatsApp Alert System is running!")
            print("📡 Monitoring MQTT topics for equipment alerts...")
            print("📱 Alerts will be sent to Discord and simulated for WhatsApp")
            print("\nPress Ctrl+C to stop\n")
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n👋 Stopping WhatsApp Alert System...")
            self.client.loop_stop()
            self.client.disconnect()
        except Exception as e:
            print(f"❌ Error: {e}")

def test_system():
    """Send test alerts to verify the system"""
    print("🧪 Sending test alerts...")
    
    test_alerts = [
        {
            "topic": "equipment/alerts",
            "payload": {
                "equipmentId": "PUMP-001",
                "type": "Centrifugal Pump",
                "location": "Building A - Floor 2",
                "value": 95.5,
                "threshold": 80,
                "description": "Pump temperature exceeding critical threshold",
                "timestamp": datetime.now().isoformat()
            }
        },
        {
            "topic": "sensors/critical",
            "payload": {
                "equipmentId": "TEMP-SENSOR-42",
                "type": "Temperature Sensor",
                "location": "Reactor Room 3",
                "value": 150,
                "threshold": 120,
                "description": "Reactor temperature critical - immediate action required",
                "timestamp": datetime.now().isoformat()
            }
        }
    ]
    
    import paho.mqtt.publish as publish
    
    for alert in test_alerts:
        try:
            publish.single(
                alert["topic"],
                json.dumps(alert["payload"]),
                hostname="localhost",
                port=1883
            )
            print(f"✅ Test alert sent to {alert['topic']}")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Failed to send test alert: {e}")

def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_system()
    else:
        # Start the monitoring system
        alert_system = WhatsAppAlertSystem()
        alert_system.start_monitoring()

if __name__ == "__main__":
    main()