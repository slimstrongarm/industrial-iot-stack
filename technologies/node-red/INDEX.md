# Node-RED Technology Stack - Complete File Index
*Every Node-RED flow, integration, and guide in the industrial IoT stack*

## 🚀 Quick Access for Claude Instances

**New to Node-RED in this codebase?** Start with:
1. `reference/technical-reference.md` - Core Node-RED architecture patterns
2. `setup-guides/NODE_RED_SETUP_GUIDE.md` - Complete setup instructions
3. `flows/` - Working JSON flow examples
4. `implementations/` - Production flows from Steel Bonnet brewery

## 📂 Complete File Listing

### 🏗️ Reference & Architecture
```
reference/
├── technical-reference.md               # Core Node-RED patterns and best practices
└── TODO-NODERED-CLEANUP.md             # Node-RED cleanup and optimization tasks
```

### ⚙️ Setup Guides
```
setup-guides/
└── NODE_RED_SETUP_GUIDE.md             # Complete Node-RED installation and setup
```

### 🔄 Working Flows (JSON Files)
```
flows/
├── brewery_mqtt_translation_flow.json   # MQTT message translation for brewery
├── opc_validation_tools_flow.json       # OPC UA connection validation tools
├── performance_monitoring_flow.json     # System performance monitoring
├── pi-touchscreen-flow.json            # Raspberry Pi touchscreen interface
└── steel-bonnet-whatsapp-flow.json     # WhatsApp alert integration
```

### 🏭 Real Implementations (Steel Bonnet Production)
```
implementations/
├── COMPREHENSIVE_DEPLOYMENT_GUIDE.md    # Complete deployment strategy
├── MONITORING_DASHBOARD_V3_GUIDE.md     # Production monitoring dashboard
├── MQTT_PROTOCOL_MODULE_GUIDE.md        # MQTT protocol handling module
├── NODERED_INSTALLATION_GUIDE_UPDATED.md # Updated installation process
└── TESTING_ROADMAP.md                   # Testing strategy and roadmap
```

## 🎯 Node-RED Usage Patterns

### Flow Development
- **Basic Setup**: `setup-guides/NODE_RED_SETUP_GUIDE.md`
- **Production Deployment**: `implementations/COMPREHENSIVE_DEPLOYMENT_GUIDE.md`
- **Testing Strategy**: `implementations/TESTING_ROADMAP.md`

### Integration Patterns
- **MQTT Integration**: `flows/brewery_mqtt_translation_flow.json`
- **OPC UA Bridge**: `flows/opc_validation_tools_flow.json`
- **WhatsApp Alerts**: `flows/steel-bonnet-whatsapp-flow.json`
- **Monitoring**: `flows/performance_monitoring_flow.json`

### UI/Dashboard
- **Production Dashboard**: `implementations/MONITORING_DASHBOARD_V3_GUIDE.md`
- **Touchscreen Interface**: `flows/pi-touchscreen-flow.json`

## 🔗 Related Technologies

- **MQTT**: `../mqtt/` - Message broker integration (see MQTT_PROTOCOL_MODULE_GUIDE.md)
- **Ignition**: `../ignition/` - OPC UA integration for SCADA
- **n8n**: `../n8n/` - Advanced workflow automation
- **WhatsApp**: `../whatsapp/` - Alert notification system

## 📊 Project Cross-References

- **Steel Bonnet Brewery**: Complete production implementation
- **CT-084 Parachute Drop**: Edge device flows with touchscreen
- **Monitoring System**: Real-time dashboards and alerts
- **WhatsApp Integration**: Equipment alerts via messaging

## 🎯 Common Node-RED Commands

```bash
# Start Node-RED
node-red

# Start with specific settings
node-red -s settings.js

# Install Node-RED node
npm install node-red-contrib-[node-name]

# Access Node-RED UI
http://localhost:1880

# Access Node-RED Dashboard
http://localhost:1880/ui
```

## 💡 Flow Import Instructions

To import any of the JSON flows:
1. Open Node-RED UI (http://localhost:1880)
2. Click menu → Import → Clipboard
3. Paste the JSON content from `flows/` directory
4. Click Import
5. Deploy the flow

## 🏭 Steel Bonnet Implementation Highlights

The Steel Bonnet brewery implementation includes:
- **MQTT Protocol Module**: Advanced MQTT message handling
- **Monitoring Dashboard V3**: Real-time equipment monitoring
- **Comprehensive Deployment**: Production-ready deployment guide
- **Testing Roadmap**: Complete testing strategy

## 📱 Mobile & HMI Integration

- **Pi Touchscreen Flow**: 7" touchscreen interface for field operators
- **WhatsApp Integration**: Mobile alerts for critical events
- **Dashboard Access**: Mobile-responsive web dashboards

---
*Files Organized: 13 | Last Updated: 2025-06-28 | Status: ✅ Ready for Claude*