#!/usr/bin/env python3
"""
🪂 TOUCHSCREEN DASHBOARD ENHANCER
Enhances the existing CT-084 auto-sensor-configurator for 7" touchscreen
Works with auto-sensor-configurator.py output
"""

import json
from pathlib import Path
from datetime import datetime

class TouchscreenDashboardEnhancer:
    def __init__(self):
        self.base_config = None
        self.enhanced_flows = []
        
    def load_base_configuration(self):
        """Load configuration from CT-084 auto-sensor-configurator"""
        config_path = Path("/home/pi/parachute_drop/sensor_configuration.json")
        
        if not config_path.exists():
            print("⚠️ Base configuration not found. Running auto-sensor-configurator first...")
            # Import and run the existing configurator
            from auto_sensor_configurator import AutoSensorConfigurator
            configurator = AutoSensorConfigurator()
            self.base_config = configurator.generate_complete_configuration()
            configurator.save_configuration(self.base_config)
        else:
            with open(config_path, 'r') as f:
                self.base_config = json.load(f)
        
        print(f"✅ Loaded base configuration with {self.base_config['parachute_drop_config']['sensors_detected']} sensors")
        
    def enhance_for_touchscreen(self):
        """Enhance the existing flows for 7" touchscreen display"""
        
        # Get base flows
        base_flows = self.base_config["parachute_drop_config"]["node_red_flows"]
        
        # Create enhanced UI base configuration
        ui_base = {
            "id": "ui_base_touchscreen",
            "type": "ui_base",
            "theme": {
                "name": "theme-brewery-touchscreen",
                "lightTheme": {
                    "default": "#2C5282",
                    "baseColor": "#1A365D",
                    "baseFont": "-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif",
                    "edited": True
                }
            },
            "site": {
                "name": "🪂 Brewery Parachute Drop",
                "hideToolbar": "false",
                "allowSwipe": "true", 
                "lockMenu": "false",
                "dateFormat": "MM/DD/YYYY",
                "sizes": {
                    "sx": 48,  # Larger for touch
                    "sy": 48,
                    "gx": 6,
                    "gy": 6,
                    "cx": 6,
                    "cy": 6,
                    "px": 0,
                    "py": 0
                }
            }
        }
        
        # Find and enhance the tab
        for flow in base_flows:
            if flow.get("type") == "ui_tab":
                flow["name"] = "🪂 Brewery Monitor"
                flow["icon"] = "dashboard"
                break
        
        # Add status header group
        status_group = {
            "id": "status_header_group",
            "type": "ui_group",
            "name": "System Status",
            "tab": "parachute_tab",
            "order": 0,
            "disp": True,
            "width": "12",
            "collapse": False
        }
        
        # Enhance sensor widgets for touchscreen
        sensor_details = self.base_config["parachute_drop_config"]["sensor_details"]
        enhanced_widgets = []
        
        for port, sensor in sensor_details.items():
            
            # Find existing widget and enhance it
            widget_id = f"dashboard_{port}"
            for flow in base_flows:
                if flow.get("id") == widget_id:
                    # Make it bigger and more touch-friendly
                    if flow.get("type") == "ui_gauge":
                        flow["width"] = "6"
                        flow["height"] = "5"
                        flow["gtype"] = "gage"
                        flow["format"] = "{{value | number:1}}"
                        # Add larger color segments for visibility
                        flow["colors"] = ["#3182CE", "#48BB78", "#ED8936"]
                        
                    elif flow.get("type") == "ui_led":
                        flow["width"] = "4"
                        flow["height"] = "2"
                        # Bigger LED for touch screen
                        
            # Add text display under each gauge
            text_display = {
                "id": f"text_display_{port}",
                "type": "ui_text",
                "group": "sensors_group",
                "order": (int(port) + 1) * 10 + 5,
                "width": "6", 
                "height": "2",
                "name": f"{sensor['name']} Display",
                "label": "",
                "format": f"<div style='text-align:center; font-size:32px; font-weight:bold;'>{{{{msg.payload}}}} {sensor['unit']}</div>",
                "layout": "col-center",
                "x": 500,
                "y": 100 + int(port) * 100 + 50,
                "wires": []
            }
            enhanced_widgets.append(text_display)
            
            # Connect sensor processing to text display
            for flow in base_flows:
                if flow.get("id") == f"sensor_process_{port}":
                    # Add text display to outputs
                    if f"text_display_{port}" not in flow.get("wires", [[]])[0]:
                        flow["wires"][0].append(f"text_display_{port}")
        
        # Add system status display
        status_display = {
            "id": "system_status_display",
            "type": "ui_text",
            "group": "status_header_group",
            "order": 1,
            "width": "12",
            "height": "3",
            "name": "System Status",
            "label": "",
            "format": """
            <div style='text-align:center; padding:15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; border-radius:10px;'>
                <div style='font-size:28px; font-weight:bold; margin-bottom:10px;'>
                    🪂 PARACHUTE DROP ACTIVE
                </div>
                <div style='font-size:18px;'>
                    {{sensors_detected}} Sensors Online | Status: {{status}} | {{timestamp}}
                </div>
            </div>
            """,
            "layout": "col-center",
            "x": 100,
            "y": 50,
            "wires": []
        }
        
        # Add status update function
        status_function = {
            "id": "update_status_display",
            "type": "function",
            "name": "Update Status",
            "func": f"""
            // Update system status display
            const sensorsDetected = {len(sensor_details)};
            const timestamp = new Date().toLocaleTimeString();
            let status = "🟢 NORMAL";
            
            // Determine overall status based on sensor data
            if (msg.temp_data && (msg.temp_data.status === 'high' || msg.temp_data.status === 'low')) {{
                status = "🟡 WARNING";
            }}
            if (msg.current_data && msg.current_data.status === 'overload') {{
                status = "🔴 ALARM";
            }}
            
            msg.payload = {{
                sensors_detected: sensorsDetected,
                status: status,
                timestamp: timestamp
            }};
            
            return msg;
            """,
            "outputs": 1,
            "x": 300,
            "y": 50,
            "wires": [["system_status_display"]]
        }
        
        # Connect all sensor processors to status function
        for flow in base_flows:
            if flow.get("type") == "function" and "sensor_process_" in flow.get("id", ""):
                flow["wires"][0].append("update_status_display")
        
        # Combine all enhanced flows
        self.enhanced_flows = [ui_base, status_group, status_display, status_function] + base_flows + enhanced_widgets
        
        return self.enhanced_flows
    
    def add_trending_charts(self):
        """Add trending charts for sensor data"""
        
        # Create trends group
        trends_group = {
            "id": "trends_group",
            "type": "ui_group",
            "name": "Live Trends",
            "tab": "parachute_tab", 
            "order": 99,
            "disp": True,
            "width": "12",
            "collapse": False
        }
        
        # Get sensor details
        sensor_details = self.base_config["parachute_drop_config"]["sensor_details"]
        
        chart_flows = [trends_group]
        
        # Add chart for each numeric sensor
        chart_position = 600
        for port, sensor in sensor_details.items():
            if sensor['type'] in ['temperature', 'current', 'pressure']:
                
                # Chart widget
                chart = {
                    "id": f"chart_{port}",
                    "type": "ui_chart",
                    "name": f"{sensor['name']} Trend",
                    "group": "trends_group",
                    "order": int(port) + 1,
                    "width": "6",
                    "height": "4",
                    "label": f"{sensor['name']} ({sensor['unit']})",
                    "chartType": "line",
                    "legend": "false",
                    "xformat": "HH:mm:ss",
                    "interpolate": "bezier",
                    "nodata": "Collecting data...",
                    "dot": False,
                    "ymin": "",
                    "ymax": "",
                    "removeOlder": "10",
                    "removeOlderPoints": "50",
                    "removeOlderUnit": "60",
                    "cutout": 0,
                    "useOneColor": True,
                    "colors": ["#2C5282"],
                    "x": 600,
                    "y": chart_position,
                    "wires": [[]]
                }
                
                # Connect sensor processing to chart
                for flow in self.enhanced_flows:
                    if flow.get("id") == f"sensor_process_{port}":
                        flow["wires"][0].append(f"chart_{port}")
                
                chart_flows.append(chart)
                chart_position += 100
        
        self.enhanced_flows.extend(chart_flows)
        
    def create_demo_data_generator(self):
        """Create demo data generator for testing without sensors"""
        
        demo_flows = []
        
        # Demo data injection
        demo_injector = {
            "id": "demo_data_injector",
            "type": "inject",
            "name": "Demo Data",
            "props": [{"p": "payload"}],
            "repeat": "5",
            "crontab": "",
            "once": True,
            "onceDelay": 3,
            "topic": "",
            "payload": "",
            "payloadType": "date",
            "x": 100,
            "y": 800,
            "wires": [["generate_demo_data"]]
        }
        
        # Demo data generator
        demo_generator = {
            "id": "generate_demo_data",
            "type": "function",
            "name": "Generate Demo Data",
            "func": """
            // Generate realistic brewery demo data
            const sensors = {
                0: {type: 'temperature', base: 22, variation: 3, name: 'HLT_Temperature'},
                1: {type: 'current', base: 12, variation: 5, name: 'Pump_1_Current'},
                2: {type: 'digital', base: 1, variation: 0, name: 'Motor_Contactor'},
                3: {type: 'temperature', base: 18, variation: 2, name: 'Ambient_Temp'}
            };
            
            Object.keys(sensors).forEach(port => {
                const sensor = sensors[port];
                let value;
                
                if (sensor.type === 'digital') {
                    value = Math.random() > 0.8 ? 0 : 1;  // Occasional state changes
                } else {
                    value = sensor.base + (Math.random() - 0.5) * sensor.variation;
                }
                
                setTimeout(() => {
                    node.send({
                        payload: value,
                        topic: `demo/${sensor.name}`,
                        _msgid: `demo_${port}_${Date.now()}`
                    });
                }, port * 200);  // Stagger the outputs
            });
            
            return null;
            """,
            "outputs": 1,
            "x": 300,
            "y": 800,
            "wires": [["distribute_demo_data"]]
        }
        
        # Demo data distributor
        demo_distributor = {
            "id": "distribute_demo_data", 
            "type": "function",
            "name": "Distribute Demo Data",
            "func": """
            // Route demo data to appropriate sensor processors
            const topic = msg.topic;
            
            if (topic.includes('HLT_Temperature')) {
                node.send([msg, null, null, null]);
            } else if (topic.includes('Pump_1_Current')) {
                node.send([null, msg, null, null]);
            } else if (topic.includes('Motor_Contactor')) {
                node.send([null, null, msg, null]);
            } else if (topic.includes('Ambient_Temp')) {
                node.send([null, null, null, msg]);
            }
            
            return null;
            """,
            "outputs": 4,
            "x": 500,
            "y": 800,
            "wires": [
                ["sensor_process_0"],
                ["sensor_process_1"], 
                ["sensor_process_2"],
                ["sensor_process_3"]
            ]
        }
        
        demo_flows = [demo_injector, demo_generator, demo_distributor]
        self.enhanced_flows.extend(demo_flows)
        
    def save_enhanced_configuration(self):
        """Save the enhanced configuration"""
        output_dir = Path("/home/pi/parachute_drop")
        output_dir.mkdir(exist_ok=True)
        
        # Create enhanced configuration
        enhanced_config = {
            "touchscreen_dashboard_config": {
                "timestamp": datetime.now().isoformat(),
                "base_config": self.base_config,
                "enhanced_flows": self.enhanced_flows,
                "display_specs": {
                    "screen_size": "7_inch",
                    "resolution": "800x480",
                    "orientation": "landscape",
                    "touch_optimized": True
                },
                "features": [
                    "auto_sensor_detection",
                    "touch_friendly_widgets",
                    "live_trending",
                    "system_status_display",
                    "demo_data_generator",
                    "brewery_theme"
                ]
            }
        }
        
        # Save enhanced flows for Node-RED import
        with open(output_dir / "touchscreen_dashboard_flows.json", "w") as f:
            json.dump(self.enhanced_flows, f, indent=2)
        
        # Save complete enhanced config
        with open(output_dir / "touchscreen_configuration.json", "w") as f:
            json.dump(enhanced_config, f, indent=2)
        
        print(f"💾 Enhanced configuration saved to {output_dir}")
        return output_dir

def main():
    """Main execution"""
    print("🪂 TOUCHSCREEN DASHBOARD ENHANCER")
    print("====================================")
    print("Enhancing CT-084 auto-sensor-configurator for 7\" touchscreen")
    
    enhancer = TouchscreenDashboardEnhancer()
    
    # Load base configuration from CT-084
    enhancer.load_base_configuration()
    
    # Enhance for touchscreen
    enhancer.enhance_for_touchscreen()
    
    # Add trending charts
    enhancer.add_trending_charts()
    
    # Add demo data generator
    enhancer.create_demo_data_generator()
    
    # Save enhanced configuration
    output_dir = enhancer.save_enhanced_configuration()
    
    print(f"\n✅ TOUCHSCREEN ENHANCEMENT COMPLETE!")
    print(f"📊 Enhanced Features:")
    print(f"   • Touch-optimized widgets (larger, easier to tap)")
    print(f"   • System status header with parachute drop branding")
    print(f"   • Live trending charts for all sensors")
    print(f"   • Demo data generator for testing")
    print(f"   • 7\" screen optimized layout (800x480)")
    print(f"   • Professional brewery theme")
    print(f"\n🎯 Next Steps:")
    print(f"   1. Import: {output_dir}/touchscreen_dashboard_flows.json")
    print(f"   2. Access: http://localhost:1880/ui")
    print(f"   3. Connect your Pi 7\" touchscreen")
    print(f"   4. Watch your Phidget sensors come alive!")
    
    return enhancer

if __name__ == "__main__":
    main()