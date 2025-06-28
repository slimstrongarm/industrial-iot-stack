#!/usr/bin/env python3
"""
Unified Industrial IoT Monitoring System
Combines Docker monitoring with existing platform monitoring
"""

import docker
import requests
import subprocess
import psutil
import json
import time
from datetime import datetime
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class UnifiedIndustrialMonitor:
    def __init__(self):
        """Initialize all monitoring connections"""
        self.docker_client = self._init_docker()
        self.sheet_client = self._init_sheets()
        self.n8n_auth = self._init_n8n_auth()
        self.monitored_containers = [
            'discord-claude-bot',
            'mac-claude-worker', 
            'iiot-emqx',
            'iiot-node-red',
            'iiot-n8n',
            'iiot-ignition',
            'iiot-timescaledb'
        ]
        
    def _init_docker(self):
        """Initialize Docker client"""
        try:
            return docker.from_env()
        except Exception as e:
            print(f"❌ Docker connection failed: {e}")
            return None
    
    def _init_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            creds_file = 'credentials/iot-stack-credentials.json'
            creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
            client = gspread.authorize(creds)
            return client.open_by_key('1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do')
        except Exception as e:
            print(f"❌ Sheets connection error: {e}")
            return None
    
    def _init_n8n_auth(self):
        """Initialize n8n API authentication"""
        try:
            import base64
            auth_string = "iiot-admin:StrongPassword123!"
            auth_bytes = base64.b64encode(auth_string.encode()).decode()
            return {"Authorization": f"Basic {auth_bytes}"}
        except Exception as e:
            print(f"❌ n8n auth error: {e}")
            return None
    
    def monitor_docker_containers(self):
        """Monitor all Docker containers in the stack"""
        if not self.docker_client:
            return {"error": "Docker not available"}
        
        container_status = {}
        
        try:
            # Get all containers (running and stopped)
            all_containers = self.docker_client.containers.list(all=True)
            
            for container in all_containers:
                name = container.name
                if any(monitored in name for monitored in self.monitored_containers):
                    try:
                        # Get detailed container info
                        container.reload()
                        stats = container.stats(stream=False) if container.status == 'running' else None
                        
                        container_status[name] = {
                            'status': container.status,
                            'image': container.image.tags[0] if container.image.tags else 'unknown',
                            'created': container.attrs['Created'],
                            'ports': container.ports,
                            'health': self._get_container_health(container),
                            'cpu_usage': self._calculate_cpu_usage(stats) if stats else 0,
                            'memory_usage': self._calculate_memory_usage(stats) if stats else 0
                        }
                    except Exception as e:
                        container_status[name] = {'error': str(e)}
            
            return container_status
            
        except Exception as e:
            return {"error": f"Docker monitoring failed: {e}"}
    
    def _get_container_health(self, container):
        """Get container health status"""
        try:
            health = container.attrs.get('State', {}).get('Health', {})
            if health:
                return health.get('Status', 'unknown')
            else:
                # If no health check defined, use container status
                return 'healthy' if container.status == 'running' else 'unhealthy'
        except:
            return 'unknown'
    
    def _calculate_cpu_usage(self, stats):
        """Calculate CPU usage percentage from container stats"""
        try:
            cpu_stats = stats['cpu_stats']
            precpu_stats = stats['precpu_stats']
            
            cpu_delta = cpu_stats['cpu_usage']['total_usage'] - precpu_stats['cpu_usage']['total_usage']
            system_delta = cpu_stats['system_cpu_usage'] - precpu_stats['system_cpu_usage']
            
            if system_delta > 0:
                return round((cpu_delta / system_delta) * 100, 2)
            return 0
        except:
            return 0
    
    def _calculate_memory_usage(self, stats):
        """Calculate memory usage in MB"""
        try:
            memory_usage = stats['memory_stats']['usage']
            return round(memory_usage / (1024 * 1024), 2)  # Convert to MB
        except:
            return 0
    
    def monitor_mqtt_brokers(self):
        """Monitor MQTT broker health"""
        brokers = {
            'mosquitto_local': {'host': 'localhost', 'port': 1883},
            'emqx_server': {'host': 'localhost', 'port': 1883}
        }
        
        broker_status = {}
        
        for name, config in brokers.items():
            try:
                import paho.mqtt.client as mqtt
                
                def on_connect(client, userdata, flags, rc):
                    userdata['connected'] = rc == 0
                
                client_data = {'connected': False}
                client = mqtt.Client(userdata=client_data)
                client.on_connect = on_connect
                
                # Try to connect with timeout
                client.connect(config['host'], config['port'], 60)
                client.loop_start()
                time.sleep(2)  # Give it time to connect
                client.loop_stop()
                client.disconnect()
                
                broker_status[name] = {
                    'status': 'healthy' if client_data['connected'] else 'unhealthy',
                    'host': config['host'],
                    'port': config['port'],
                    'timestamp': datetime.now().isoformat()
                }
                
            except Exception as e:
                broker_status[name] = {
                    'status': 'error',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                }
        
        return broker_status
    
    def monitor_node_red_flows(self):
        """Monitor Node-RED flows and health"""
        try:
            # Check Node-RED admin API
            response = requests.get('http://localhost:1880/flows', timeout=10)
            if response.status_code == 200:
                flows = response.json()
                
                # Count flow types
                flow_stats = {
                    'total_flows': len([f for f in flows if f.get('type') == 'tab']),
                    'total_nodes': len([f for f in flows if f.get('type') != 'tab']),
                    'debug_nodes': len([f for f in flows if f.get('type') == 'debug']),
                    'mqtt_nodes': len([f for f in flows if f.get('type') in ['mqtt in', 'mqtt out']]),
                    'http_nodes': len([f for f in flows if f.get('type') in ['http in', 'http request']]),
                    'function_nodes': len([f for f in flows if f.get('type') == 'function'])
                }
                
                return {
                    'status': 'healthy',
                    'stats': flow_stats,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {'status': 'unhealthy', 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def monitor_ignition_gateway(self):
        """Monitor Ignition Gateway health"""
        try:
            # Check Ignition web interface
            response = requests.get('http://localhost:8088/main/system/gateway/status', 
                                  timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                return {
                    'status': 'healthy',
                    'response_code': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'unhealthy', 
                    'response_code': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }
                
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_system_metrics(self):
        """Get overall system health metrics"""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'load_average': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None,
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def update_unified_dashboard(self, monitoring_data):
        """Update Google Sheets with unified monitoring data"""
        if not self.sheet_client:
            return False
        
        try:
            # Update monitoring dashboard sheet
            dashboard = self.sheet_client.worksheet('Monitoring Dashboard')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Container status summary
            containers = monitoring_data.get('docker_containers', {})
            healthy_containers = len([c for c in containers.values() if c.get('status') == 'running'])
            total_containers = len(containers)
            
            # System health summary
            system = monitoring_data.get('system_metrics', {})
            
            # Update key metrics (adjust row numbers as needed)
            updates = [
                ('B2', f"{healthy_containers}/{total_containers} containers running"),  # Docker Status
                ('B3', monitoring_data.get('mqtt_brokers', {}).get('emqx_server', {}).get('status', 'unknown')),  # MQTT Status
                ('B4', monitoring_data.get('node_red', {}).get('status', 'unknown')),  # Node-RED Status
                ('B5', monitoring_data.get('ignition', {}).get('status', 'unknown')),  # Ignition Status
                ('B6', f"{system.get('cpu_percent', 0):.1f}%"),  # CPU Usage
                ('B7', f"{system.get('memory_percent', 0):.1f}%"),  # Memory Usage
                ('B8', timestamp)  # Last Updated
            ]
            
            for cell, value in updates:
                dashboard.update(cell, value)
            
            return True
            
        except Exception as e:
            print(f"❌ Dashboard update error: {e}")
            return False
    
    def run_unified_monitoring(self):
        """Run complete unified monitoring cycle"""
        print("🏭 Unified Industrial IoT Monitoring System")
        print("=" * 60)
        
        monitoring_data = {}
        
        # Monitor Docker containers
        print("\n🐳 Docker Container Health:")
        containers = self.monitor_docker_containers()
        monitoring_data['docker_containers'] = containers
        
        if 'error' not in containers:
            for name, status in containers.items():
                if 'error' not in status:
                    health_icon = "🟢" if status['status'] == 'running' else "🔴"
                    cpu = status.get('cpu_usage', 0)
                    memory = status.get('memory_usage', 0)
                    print(f"  {health_icon} {name}: {status['status']} (CPU: {cpu}%, RAM: {memory}MB)")
                else:
                    print(f"  ❌ {name}: {status['error']}")
        else:
            print(f"  ❌ Docker monitoring failed: {containers['error']}")
        
        # Monitor MQTT Brokers
        print("\n📡 MQTT Broker Health:")
        mqtt_status = self.monitor_mqtt_brokers()
        monitoring_data['mqtt_brokers'] = mqtt_status
        
        for name, status in mqtt_status.items():
            health_icon = "🟢" if status['status'] == 'healthy' else "🔴"
            print(f"  {health_icon} {name}: {status['status']}")
        
        # Monitor Node-RED
        print("\n🔄 Node-RED Flow Health:")
        node_red_status = self.monitor_node_red_flows()
        monitoring_data['node_red'] = node_red_status
        
        if node_red_status['status'] == 'healthy':
            stats = node_red_status['stats']
            print(f"  🟢 Node-RED: {stats['total_flows']} flows, {stats['total_nodes']} nodes")
            print(f"    MQTT nodes: {stats['mqtt_nodes']}, Functions: {stats['function_nodes']}")
        else:
            print(f"  🔴 Node-RED: {node_red_status.get('error', 'unhealthy')}")
        
        # Monitor Ignition Gateway
        print("\n🏭 Ignition Gateway Health:")
        ignition_status = self.monitor_ignition_gateway()
        monitoring_data['ignition'] = ignition_status
        
        health_icon = "🟢" if ignition_status['status'] == 'healthy' else "🔴"
        print(f"  {health_icon} Ignition Gateway: {ignition_status['status']}")
        
        # Get System Metrics
        print("\n💻 System Health:")
        system_metrics = self.get_system_metrics()
        monitoring_data['system_metrics'] = system_metrics
        
        if 'error' not in system_metrics:
            print(f"  CPU: {system_metrics['cpu_percent']:.1f}%")
            print(f"  Memory: {system_metrics['memory_percent']:.1f}%") 
            print(f"  Disk: {system_metrics['disk_percent']:.1f}%")
        else:
            print(f"  ❌ System metrics error: {system_metrics['error']}")
        
        # Update Dashboard
        print(f"\n📊 Updating Unified Dashboard...")
        dashboard_updated = self.update_unified_dashboard(monitoring_data)
        print(f"Dashboard Updated: {'✅' if dashboard_updated else '❌'}")
        
        # Save monitoring data
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"/tmp/unified_industrial_monitoring_{timestamp}.json"
        
        try:
            with open(output_file, 'w') as f:
                json.dump(monitoring_data, f, indent=2, default=str)
            print(f"💾 Monitoring data saved: {output_file}")
        except Exception as e:
            print(f"❌ Save error: {e}")
        
        # Update CT-058 Monitoring Dashboard
        print(f"\n📊 Updating CT-058 Monitoring Dashboard...")
        dashboard_updated = self.update_monitoring_dashboard_ct058(monitoring_data)
        print(f"CT-058 Dashboard Updated: {'✅' if dashboard_updated else '❌'}")
        
        print("=" * 60)
        print("🎯 Unified industrial monitoring complete!")
        
        return monitoring_data
    
    def update_monitoring_dashboard_ct058(self, monitoring_data):
        """Update the CT-058 Monitoring Dashboard with current data"""
        if not self.sheet_client:
            return False
        
        try:
            # Update Monitoring Dashboard tab
            dashboard = self.sheet_client.worksheet('Monitoring Dashboard')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # Update overall status and timestamp
            dashboard.update('E3', timestamp)
            
            # Update container health section
            if 'docker_containers' in monitoring_data and monitoring_data['docker_containers']:
                containers = monitoring_data['docker_containers']
                healthy_containers = len([c for c in containers.values() if c.get('status') == 'running'])
                total_containers = len(containers)
                
                # Update container summary
                dashboard.update('B3', f"{healthy_containers}/{total_containers} containers healthy")
                
                # Update individual container rows (starting at row 10)
                container_row = 10
                for name, status in containers.items():
                    if 'error' not in status:
                        container_data = [
                            name,
                            status.get('status', 'UNKNOWN').upper(),
                            f"{status.get('cpu_usage', 0)}%",
                            f"{status.get('memory_usage', 0)}MB",
                            'Running',  # Would calculate actual uptime from container.attrs
                            status.get('health', 'UNKNOWN').upper()
                        ]
                        
                        # Update row
                        range_name = f'A{container_row}:F{container_row}'
                        dashboard.update(range_name, [container_data])
                        container_row += 1
            
            # Update industrial systems section
            system_row = 21
            if 'mqtt_brokers' in monitoring_data:
                mqtt_status = monitoring_data['mqtt_brokers'].get('emqx_server', {}).get('status', 'UNKNOWN')
                dashboard.update(f'B{system_row}', mqtt_status.upper())
                dashboard.update(f'D{system_row}', timestamp.split()[1])  # Just time part
            
            system_row += 1
            if 'node_red' in monitoring_data:
                node_red_status = monitoring_data['node_red'].get('status', 'UNKNOWN')
                dashboard.update(f'B{system_row}', node_red_status.upper())
                dashboard.update(f'D{system_row}', timestamp.split()[1])
            
            system_row += 1  
            if 'ignition' in monitoring_data:
                ignition_status = monitoring_data['ignition'].get('status', 'UNKNOWN')
                dashboard.update(f'B{system_row}', ignition_status.upper())
                dashboard.update(f'D{system_row}', timestamp.split()[1])
            
            # Update system resources section
            if 'system_metrics' in monitoring_data:
                metrics = monitoring_data['system_metrics']
                
                # CPU Usage (row 38)
                cpu_percent = metrics.get('cpu_percent', 0)
                dashboard.update('B38', f"{cpu_percent:.1f}%")
                cpu_status = 'NORMAL' if cpu_percent < 80 else 'WARNING' if cpu_percent < 95 else 'CRITICAL'
                dashboard.update('D38', cpu_status)
                
                # Memory Usage (row 39)
                memory_percent = metrics.get('memory_percent', 0)
                dashboard.update('B39', f"{memory_percent:.1f}%")
                memory_status = 'NORMAL' if memory_percent < 85 else 'WARNING' if memory_percent < 95 else 'CRITICAL'
                dashboard.update('D39', memory_status)
                
                # Disk Usage (row 40)
                disk_percent = metrics.get('disk_percent', 0)
                dashboard.update('B40', f"{disk_percent:.1f}%")
                disk_status = 'NORMAL' if disk_percent < 90 else 'WARNING' if disk_percent < 98 else 'CRITICAL'
                dashboard.update('D40', disk_status)
            
            # Add activity log entry
            activity_time = datetime.now().strftime('%H:%M')
            activity_data = [
                activity_time,
                'INFO',
                'Unified monitoring system updated dashboard',
                'COMPLETE'
            ]
            
            # Find next available row in activity section (starting around row 46)
            try:
                # Add to recent activity (you'd want to implement a rolling log)
                dashboard.update('A46:D46', [activity_data])
            except:
                pass  # Ignore if activity section doesn't exist yet
            
            return True
            
        except Exception as e:
            print(f"❌ CT-058 Dashboard update error: {e}")
            return False

def main():
    """Main monitoring function"""
    monitor = UnifiedIndustrialMonitor()
    return monitor.run_unified_monitoring()

if __name__ == "__main__":
    main()