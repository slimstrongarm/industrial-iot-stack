# ⚡ Ignition SCADA Platform - Industrial IoT Stack

**Inductive Automation's Ignition** is our primary SCADA/HMI platform providing industrial-grade visualization, data collection, and control capabilities for the Steel Bonnet brewery implementation.

## 🚀 Quick Start for Claude Instances

**New to Ignition integration?** Start here:
1. `setup-guides/IGNITION_INTEGRATION_SETUP.md` - Complete platform setup
2. `setup-guides/IGNITION_MODULE_SETUP.md` - Custom module installation
3. `modules/ignition-project-scan-endpoint/` - Custom Java module project
4. `ignition-scripts/` - Python scripting and automation

## 🎯 What Ignition Does in Our Stack

### Core Capabilities
- **SCADA Operations**: Real-time process monitoring and control
- **HMI Development**: Touch-screen interfaces and dashboards
- **Data Historian**: Time-series data collection and trending
- **OPC UA Server/Client**: Industrial protocol communication
- **Python Scripting**: Custom automation and integration logic

### Key Integrations
- **Steel Bonnet Brewery**: Complete brewery automation and monitoring
- **Node-RED**: OPC UA data bridge to MQTT broker
- **MQTT**: Equipment data publication for IoT integration
- **Google Sheets**: Task tracking and operational reporting
- **n8n**: Workflow automation and alert processing

## 🏭 Production Implementation

### Steel Bonnet Integration
- **Equipment Monitoring**: Real-time brewery equipment status
- **Process Control**: Automated brewing sequence management  
- **Data Collection**: Temperature, pressure, flow rate logging
- **Operator Interface**: Touch-screen HMI for brewery operators

### Custom Module Development
- **Project Scan Endpoint**: Java-based Ignition module for project management
- **Gateway Integration**: Server-side functionality and web routes
- **Designer Integration**: Client-side tools and project browser

## 📂 Directory Structure

```
technologies/ignition/
├── README.md                    # You are here
├── INDEX.md                     # Complete file listing
├── setup-guides/                # Installation and configuration
├── modules/                     # Custom Ignition modules
│   └── ignition-project-scan-endpoint/  # Java module project
├── ignition-scripts/            # Python scripts and automation
├── ignition_exports/            # Project export management
├── scripts/                     # Integration and utility scripts
├── integrations/               # Cross-platform integrations
├── documentation/              # Technical reference
└── troubleshooting/            # FLINT system troubleshooting
```

## 🔧 Essential Endpoints

- **Ignition Gateway**: http://localhost:8088
- **Gateway Admin**: http://localhost:8088/main/web/config
- **Designer Launcher**: http://localhost:8088/main/system/launch/designer
- **OPC UA Server**: opc.tcp://localhost:62541
- **Gateway API**: http://localhost:8088/main/system/gateway

## 🔗 Related Technologies

- **Node-RED**: `../node-red/` - OPC UA to MQTT bridge
- **MQTT**: `../mqtt/` - Equipment data distribution  
- **Steel Bonnet**: `../../projects/steel-bonnet/` - Brewery implementation
- **n8n**: `../n8n/` - Workflow automation integration
- **Docker**: `../docker/` - Containerized deployment

## 💡 Key Features

### SCADA Operations
- Real-time equipment monitoring and control
- Alarm management and notification systems
- Historical data trending and analysis
- Process visualization and dashboards

### Industrial Connectivity
- OPC UA server for standardized communication
- Multiple protocol support (Modbus, EtherNet/IP, etc.)
- Database connectivity for enterprise integration
- Web-based remote access capabilities

### Development Platform
- Python scripting environment
- Custom module development (Java)
- Vision and Perspective HMI platforms
- Expression language for dynamic content

## 🎯 Common Use Cases

1. **Brewery Monitoring**: Real-time process visualization
2. **Equipment Control**: Automated brewing sequences
3. **Data Logging**: Historical trend analysis
4. **Alert Management**: Multi-channel notification system
5. **Reporting**: Automated production reports

---
*Files Organized: 30+ | Technology Status: ✅ Production Ready | SCADA Platform: Ignition 8.1+*