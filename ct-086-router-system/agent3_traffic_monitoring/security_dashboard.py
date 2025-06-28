#!/usr/bin/env python3
"""
CT-086 Agent 3: Security Monitoring Dashboard
Real-time security dashboard for network traffic monitoring

This module provides a web-based security dashboard for monitoring
network traffic, security events, and industrial protocol analysis.
"""

import os
import json
import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from flask import Flask, render_template, jsonify, request, Response
import plotly.graph_objs as go
import plotly.utils
import threading
import time


class SecurityDashboard:
    """
    Web-based security monitoring dashboard
    """
    
    def __init__(self, database_path: str, port: int = 8086):
        self.database_path = database_path
        self.port = port
        self.logger = logging.getLogger(__name__)
        
        # Create Flask app
        self.app = Flask(__name__, 
                        template_folder='templates',
                        static_folder='static')
        
        # Dashboard state
        self.dashboard_active = False
        self.dashboard_thread = None
        
        # Setup routes
        self._setup_routes()
        
        # Create templates directory and files
        self._create_dashboard_templates()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page"""
            return render_template('dashboard.html')
        
        @self.app.route('/api/status')
        def api_status():
            """API endpoint for dashboard status"""
            return jsonify({
                "status": "active",
                "timestamp": datetime.now().isoformat(),
                "database_connected": os.path.exists(self.database_path)
            })
        
        @self.app.route('/api/traffic_summary')
        def api_traffic_summary():
            """API endpoint for traffic summary"""
            return jsonify(self._get_traffic_summary())
        
        @self.app.route('/api/security_alerts')
        def api_security_alerts():
            """API endpoint for security alerts"""
            hours = request.args.get('hours', default=24, type=int)
            return jsonify(self._get_security_alerts(hours))
        
        @self.app.route('/api/protocol_stats')
        def api_protocol_stats():
            """API endpoint for protocol statistics"""
            return jsonify(self._get_protocol_statistics())
        
        @self.app.route('/api/bandwidth_history')
        def api_bandwidth_history():
            """API endpoint for bandwidth history"""
            hours = request.args.get('hours', default=24, type=int)
            return jsonify(self._get_bandwidth_history(hours))
        
        @self.app.route('/api/top_talkers')
        def api_top_talkers():
            """API endpoint for top talking hosts"""
            return jsonify(self._get_top_talkers())
        
        @self.app.route('/api/industrial_protocols')
        def api_industrial_protocols():
            """API endpoint for industrial protocol analysis"""
            return jsonify(self._get_industrial_protocol_analysis())
        
        @self.app.route('/api/network_map')
        def api_network_map():
            """API endpoint for network topology map"""
            return jsonify(self._get_network_map())
    
    def _create_dashboard_templates(self):
        """Create HTML templates for the dashboard"""
        templates_dir = "/home/server/industrial-iot-stack/ct-086-router-system/agent3_traffic_monitoring/templates"
        static_dir = "/home/server/industrial-iot-stack/ct-086-router-system/agent3_traffic_monitoring/static"
        
        os.makedirs(templates_dir, exist_ok=True)
        os.makedirs(static_dir, exist_ok=True)
        
        # Main dashboard template
        dashboard_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parachute Drop - Network Security Monitor</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .status-bar {
            background-color: #28a745;
            color: white;
            padding: 10px;
            text-align: center;
            font-weight: bold;
        }
        .dashboard-container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-left: 4px solid #007bff;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #007bff;
            margin-bottom: 5px;
        }
        .metric-label {
            color: #666;
            font-size: 14px;
        }
        .chart-container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .chart-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
        }
        .alert-container {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .alert-item {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 4px;
            border-left: 4px solid;
        }
        .alert-critical { border-left-color: #dc3545; background-color: #f8d7da; }
        .alert-high { border-left-color: #fd7e14; background-color: #ffeaa7; }
        .alert-medium { border-left-color: #ffc107; background-color: #fff3cd; }
        .alert-low { border-left-color: #28a745; background-color: #d4edda; }
        .protocol-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        .protocol-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 6px;
            border-left: 4px solid #17a2b8;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Parachute Drop Network Security Monitor</h1>
        <p>Real-time industrial network traffic analysis and security monitoring</p>
    </div>
    
    <div class="status-bar" id="statusBar">
        ⚡ System Active - Monitoring Network Traffic
    </div>
    
    <div class="dashboard-container">
        <!-- Metrics Overview -->
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value" id="activeFlows">--</div>
                <div class="metric-label">Active Network Flows</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="totalBandwidth">--</div>
                <div class="metric-label">Total Bandwidth (Mbps)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="securityAlerts">--</div>
                <div class="metric-label">Security Alerts (24h)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" id="protocolCount">--</div>
                <div class="metric-label">Protocols Detected</div>
            </div>
        </div>
        
        <!-- Bandwidth Chart -->
        <div class="chart-container">
            <div class="chart-title">📊 Network Bandwidth Usage</div>
            <div id="bandwidthChart" style="height: 400px;"></div>
        </div>
        
        <!-- Protocol Analysis -->
        <div class="chart-container">
            <div class="chart-title">🔧 Industrial Protocol Distribution</div>
            <div id="protocolChart" style="height: 400px;"></div>
        </div>
        
        <!-- Security Alerts -->
        <div class="alert-container">
            <div class="chart-title">🚨 Recent Security Alerts</div>
            <div id="alertsList">
                <div class="loading">Loading security alerts...</div>
            </div>
        </div>
        
        <!-- Industrial Protocols -->
        <div class="chart-container">
            <div class="chart-title">🏭 Industrial Protocol Analysis</div>
            <div id="industrialProtocols" class="protocol-list">
                <div class="loading">Loading protocol analysis...</div>
            </div>
        </div>
    </div>
    
    <script>
        // Dashboard refresh interval
        const REFRESH_INTERVAL = 30000; // 30 seconds
        
        // Initialize dashboard
        $(document).ready(function() {
            updateDashboard();
            setInterval(updateDashboard, REFRESH_INTERVAL);
        });
        
        function updateDashboard() {
            updateMetrics();
            updateBandwidthChart();
            updateProtocolChart();
            updateSecurityAlerts();
            updateIndustrialProtocols();
        }
        
        function updateMetrics() {
            $.get('/api/traffic_summary')
                .done(function(data) {
                    $('#activeFlows').text(data.active_flows || 0);
                    $('#totalBandwidth').text((data.current_bandwidth?.total || 0).toFixed(1));
                    $('#protocolCount').text(data.total_protocols || 0);
                })
                .fail(function() {
                    console.error('Failed to fetch traffic summary');
                });
            
            $.get('/api/security_alerts?hours=24')
                .done(function(data) {
                    $('#securityAlerts').text(data.alerts?.length || 0);
                })
                .fail(function() {
                    console.error('Failed to fetch security alerts');
                });
        }
        
        function updateBandwidthChart() {
            $.get('/api/bandwidth_history?hours=6')
                .done(function(data) {
                    if (data.history && data.history.length > 0) {
                        const timestamps = data.history.map(h => h.timestamp);
                        const rxData = data.history.map(h => h.rx_mbps);
                        const txData = data.history.map(h => h.tx_mbps);
                        
                        const traces = [
                            {
                                x: timestamps,
                                y: rxData,
                                name: 'RX (Mbps)',
                                type: 'scatter',
                                mode: 'lines',
                                line: { color: '#007bff' }
                            },
                            {
                                x: timestamps,
                                y: txData,
                                name: 'TX (Mbps)',
                                type: 'scatter',
                                mode: 'lines',
                                line: { color: '#28a745' }
                            }
                        ];
                        
                        const layout = {
                            margin: { t: 20, r: 20, b: 40, l: 60 },
                            xaxis: { title: 'Time' },
                            yaxis: { title: 'Bandwidth (Mbps)' },
                            showlegend: true
                        };
                        
                        Plotly.newPlot('bandwidthChart', traces, layout, {responsive: true});
                    }
                })
                .fail(function() {
                    console.error('Failed to fetch bandwidth history');
                });
        }
        
        function updateProtocolChart() {
            $.get('/api/protocol_stats')
                .done(function(data) {
                    if (data.protocols && data.protocols.length > 0) {
                        const protocols = data.protocols.map(p => p.protocol_name);
                        const flowCounts = data.protocols.map(p => p.flow_count);
                        
                        const trace = {
                            labels: protocols,
                            values: flowCounts,
                            type: 'pie',
                            hole: 0.3,
                            textinfo: 'label+percent'
                        };
                        
                        const layout = {
                            margin: { t: 20, r: 20, b: 20, l: 20 },
                            showlegend: true
                        };
                        
                        Plotly.newPlot('protocolChart', [trace], layout, {responsive: true});
                    }
                })
                .fail(function() {
                    console.error('Failed to fetch protocol stats');
                });
        }
        
        function updateSecurityAlerts() {
            $.get('/api/security_alerts?hours=24')
                .done(function(data) {
                    const alertsContainer = $('#alertsList');
                    
                    if (data.alerts && data.alerts.length > 0) {
                        const alertsHtml = data.alerts.slice(0, 10).map(alert => {
                            const alertClass = `alert-${alert.severity}`;
                            const timestamp = new Date(alert.timestamp).toLocaleString();
                            
                            return `
                                <div class="alert-item ${alertClass}">
                                    <strong>${alert.alert_type}</strong> - ${alert.severity.toUpperCase()}
                                    <br>
                                    <small>${timestamp} | ${alert.source_ip} | ${alert.description}</small>
                                </div>
                            `;
                        }).join('');
                        
                        alertsContainer.html(alertsHtml);
                    } else {
                        alertsContainer.html('<div class="loading">No recent security alerts</div>');
                    }
                })
                .fail(function() {
                    $('#alertsList').html('<div class="loading">Failed to load security alerts</div>');
                });
        }
        
        function updateIndustrialProtocols() {
            $.get('/api/industrial_protocols')
                .done(function(data) {
                    const protocolsContainer = $('#industrialProtocols');
                    
                    if (data.protocols && data.protocols.length > 0) {
                        const protocolsHtml = data.protocols.map(protocol => `
                            <div class="protocol-item">
                                <strong>${protocol.name}</strong>
                                <br>
                                <small>Connections: ${protocol.connections}</small>
                                <br>
                                <small>Bandwidth: ${protocol.bandwidth_mbps.toFixed(2)} Mbps</small>
                            </div>
                        `).join('');
                        
                        protocolsContainer.html(protocolsHtml);
                    } else {
                        protocolsContainer.html('<div class="loading">No industrial protocols detected</div>');
                    }
                })
                .fail(function() {
                    $('#industrialProtocols').html('<div class="loading">Failed to load protocol analysis</div>');
                });
        }
    </script>
</body>
</html>
        '''
        
        with open(f"{templates_dir}/dashboard.html", 'w') as f:
            f.write(dashboard_html)
    
    def _get_traffic_summary(self) -> Dict[str, Any]:
        """Get traffic summary from database"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                # Get active flows count
                cursor = conn.execute('''
                    SELECT COUNT(*) FROM network_flows 
                    WHERE flow_state = 'active'
                ''')
                active_flows = cursor.fetchone()[0]
                
                # Get latest bandwidth
                cursor = conn.execute('''
                    SELECT rx_mbps, tx_mbps, utilization_percent 
                    FROM bandwidth_metrics 
                    ORDER BY timestamp DESC LIMIT 1
                ''')
                bandwidth_row = cursor.fetchone()
                
                current_bandwidth = {"rx_mbps": 0.0, "tx_mbps": 0.0, "total": 0.0}
                if bandwidth_row:
                    current_bandwidth = {
                        "rx_mbps": bandwidth_row[0],
                        "tx_mbps": bandwidth_row[1],
                        "total": bandwidth_row[0] + bandwidth_row[1]
                    }
                
                # Get protocol count
                cursor = conn.execute('''
                    SELECT COUNT(DISTINCT protocol_name) 
                    FROM protocol_statistics 
                    WHERE timestamp > datetime('now', '-1 hour')
                ''')
                protocol_count = cursor.fetchone()[0]
                
                return {
                    "active_flows": active_flows,
                    "current_bandwidth": current_bandwidth,
                    "total_protocols": protocol_count,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get traffic summary: {e}")
            return {"error": str(e)}
    
    def _get_security_alerts(self, hours: int = 24) -> Dict[str, Any]:
        """Get security alerts from database"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute('''
                    SELECT timestamp, alert_type, severity, source_ip, target_ip, 
                           protocol, description, raw_data
                    FROM security_alerts 
                    WHERE timestamp > datetime('now', '-{} hours')
                    ORDER BY timestamp DESC
                '''.format(hours))
                
                alerts = []
                for row in cursor.fetchall():
                    alerts.append({
                        "timestamp": row[0],
                        "alert_type": row[1],
                        "severity": row[2],
                        "source_ip": row[3],
                        "target_ip": row[4],
                        "protocol": row[5],
                        "description": row[6],
                        "raw_data": json.loads(row[7]) if row[7] else {}
                    })
                
                return {"alerts": alerts}
                
        except Exception as e:
            self.logger.error(f"Failed to get security alerts: {e}")
            return {"error": str(e)}
    
    def _get_protocol_statistics(self) -> Dict[str, Any]:
        """Get protocol statistics from database"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute('''
                    SELECT protocol_name, SUM(total_bytes) as total_bytes,
                           SUM(total_packets) as total_packets,
                           AVG(flow_count) as avg_flow_count,
                           AVG(bandwidth_mbps) as avg_bandwidth
                    FROM protocol_statistics 
                    WHERE timestamp > datetime('now', '-1 hour')
                    GROUP BY protocol_name
                    ORDER BY total_bytes DESC
                ''')
                
                protocols = []
                for row in cursor.fetchall():
                    protocols.append({
                        "protocol_name": row[0],
                        "total_bytes": row[1],
                        "total_packets": row[2],
                        "flow_count": int(row[3]) if row[3] else 0,
                        "bandwidth_mbps": row[4] if row[4] else 0.0
                    })
                
                return {"protocols": protocols}
                
        except Exception as e:
            self.logger.error(f"Failed to get protocol statistics: {e}")
            return {"error": str(e)}
    
    def _get_bandwidth_history(self, hours: int = 24) -> Dict[str, Any]:
        """Get bandwidth history from database"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute('''
                    SELECT timestamp, rx_mbps, tx_mbps, utilization_percent
                    FROM bandwidth_metrics 
                    WHERE timestamp > datetime('now', '-{} hours')
                    ORDER BY timestamp ASC
                '''.format(hours))
                
                history = []
                for row in cursor.fetchall():
                    history.append({
                        "timestamp": row[0],
                        "rx_mbps": row[1],
                        "tx_mbps": row[2],
                        "utilization_percent": row[3]
                    })
                
                return {"history": history}
                
        except Exception as e:
            self.logger.error(f"Failed to get bandwidth history: {e}")
            return {"error": str(e)}
    
    def _get_top_talkers(self) -> Dict[str, Any]:
        """Get top talking hosts"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute('''
                    SELECT src_ip, SUM(bytes_sent + bytes_received) as total_bytes
                    FROM network_flows 
                    WHERE start_time > datetime('now', '-1 hour')
                    GROUP BY src_ip
                    ORDER BY total_bytes DESC
                    LIMIT 10
                ''')
                
                top_talkers = []
                for row in cursor.fetchall():
                    top_talkers.append({
                        "ip_address": row[0],
                        "total_bytes": row[1]
                    })
                
                return {"top_talkers": top_talkers}
                
        except Exception as e:
            self.logger.error(f"Failed to get top talkers: {e}")
            return {"error": str(e)}
    
    def _get_industrial_protocol_analysis(self) -> Dict[str, Any]:
        """Get industrial protocol analysis"""
        try:
            industrial_protocols = [
                'Modbus TCP', 'OPC-UA', 'EtherNet/IP', 'MQTT', 
                'BACnet/IP', 'DNP3', 'Modbus RTU'
            ]
            
            with sqlite3.connect(self.database_path) as conn:
                protocols = []
                
                for protocol in industrial_protocols:
                    cursor = conn.execute('''
                        SELECT COUNT(*) as connections, 
                               AVG(bandwidth_mbps) as avg_bandwidth
                        FROM protocol_statistics 
                        WHERE protocol_name LIKE ? 
                        AND timestamp > datetime('now', '-1 hour')
                    ''', (f'%{protocol}%',))
                    
                    row = cursor.fetchone()
                    if row and row[0] > 0:
                        protocols.append({
                            "name": protocol,
                            "connections": row[0],
                            "bandwidth_mbps": row[1] if row[1] else 0.0
                        })
                
                return {"protocols": protocols}
                
        except Exception as e:
            self.logger.error(f"Failed to get industrial protocol analysis: {e}")
            return {"error": str(e)}
    
    def _get_network_map(self) -> Dict[str, Any]:
        """Get network topology map data"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute('''
                    SELECT DISTINCT src_ip, dst_ip, protocol
                    FROM network_flows 
                    WHERE flow_state = 'active'
                    AND src_ip != dst_ip
                ''')
                
                nodes = set()
                edges = []
                
                for row in cursor.fetchall():
                    src_ip, dst_ip, protocol = row
                    nodes.add(src_ip)
                    nodes.add(dst_ip)
                    edges.append({
                        "source": src_ip,
                        "target": dst_ip,
                        "protocol": protocol
                    })
                
                return {
                    "nodes": [{"id": node, "label": node} for node in nodes],
                    "edges": edges
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get network map: {e}")
            return {"error": str(e)}
    
    def start_dashboard(self):
        """Start the web dashboard"""
        if self.dashboard_active:
            self.logger.warning("Dashboard already running")
            return
        
        self.dashboard_active = True
        self.dashboard_thread = threading.Thread(
            target=self._run_dashboard,
            daemon=True
        )
        self.dashboard_thread.start()
        
        self.logger.info(f"Security dashboard started on port {self.port}")
    
    def stop_dashboard(self):
        """Stop the web dashboard"""
        self.dashboard_active = False
        if self.dashboard_thread:
            self.dashboard_thread.join(timeout=10)
        
        self.logger.info("Security dashboard stopped")
    
    def _run_dashboard(self):
        """Run the Flask dashboard"""
        try:
            self.app.run(
                host='0.0.0.0',
                port=self.port,
                debug=False,
                use_reloader=False
            )
        except Exception as e:
            self.logger.error(f"Dashboard error: {e}")
    
    def deploy_parachute_drop_dashboard(self) -> Dict[str, Any]:
        """Deploy dashboard for Parachute Drop system"""
        try:
            self.logger.info("Deploying Parachute Drop security dashboard...")
            
            # Start the dashboard
            self.start_dashboard()
            
            # Wait a moment for startup
            time.sleep(2)
            
            deployment_info = {
                "dashboard_url": f"http://localhost:{self.port}",
                "api_endpoints": [
                    f"http://localhost:{self.port}/api/status",
                    f"http://localhost:{self.port}/api/traffic_summary",
                    f"http://localhost:{self.port}/api/security_alerts",
                    f"http://localhost:{self.port}/api/protocol_stats",
                    f"http://localhost:{self.port}/api/bandwidth_history"
                ],
                "deployment_time": datetime.now().isoformat(),
                "features": [
                    "Real-time traffic monitoring",
                    "Security alert dashboard",
                    "Industrial protocol analysis",
                    "Bandwidth utilization charts",
                    "Network topology visualization"
                ]
            }
            
            # Save deployment info
            config_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent3_traffic_monitoring/dashboard_deployment.json"
            with open(config_path, 'w') as f:
                json.dump(deployment_info, f, indent=2)
            
            self.logger.info(f"Security dashboard deployed: {deployment_info['dashboard_url']}")
            return deployment_info
            
        except Exception as e:
            self.logger.error(f"Failed to deploy security dashboard: {e}")
            raise


def main():
    """Test security dashboard"""
    logging.basicConfig(level=logging.INFO)
    
    database_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent3_traffic_monitoring/traffic_analysis.db"
    dashboard = SecurityDashboard(database_path, port=8086)
    
    print("🖥️ Security Dashboard for Parachute Drop System")
    print("=" * 55)
    
    try:
        deployment_info = dashboard.deploy_parachute_drop_dashboard()
        print("✅ Security dashboard deployed successfully!")
        print(f"🌐 Dashboard URL: {deployment_info['dashboard_url']}")
        print(f"📊 Features: {len(deployment_info['features'])}")
        
        # Keep running for demonstration
        print("\n📡 Dashboard running... Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping dashboard...")
            dashboard.stop_dashboard()
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()