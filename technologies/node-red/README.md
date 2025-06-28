# Node-RED Technology Stack Documentation
*Quick reference for Claude instances working on Node-RED flows and integrations*

## 🎯 Quick Start for New Claude Instances

**Working on Node-RED?** Start here:
1. **Architecture**: `reference/technical-reference.md` - Core Node-RED patterns
2. **Setup**: `setup-guides/` - Installation and configuration guides
3. **Flows**: `flows/` - Working flow examples (JSON files)
4. **Integrations**: `integrations/` - Connect Node-RED to other stack components
5. **Real Implementations**: `implementations/` - Production flows from Steel Bonnet & projects

## 📂 File Organization

### Setup Guides
- **Basic Node-RED Setup** - Installation and initial configuration
- **MQTT Integration** - Connect Node-RED to MQTT brokers
- **OPC UA Integration** - Bridge Node-RED to Ignition via OPC UA
- **Dashboard Setup** - Creating operational dashboards

### Flows (JSON Files)
- **MQTT Processing Flows** - Message routing and transformation
- **Equipment Monitoring** - Real-time equipment status flows
- **Alert Systems** - Trigger notifications based on conditions
- **Integration Bridges** - Connect different protocols

### Implementations
- **Steel Bonnet Brewery** - Complete brewery automation flows
- **Parachute Drop CT-084** - Edge device management flows
- **Monitoring Dashboards** - Production dashboard examples

### Integrations
- **MQTT ↔ Node-RED** - Bidirectional MQTT communication
- **Ignition ↔ Node-RED** - OPC UA data exchange
- **n8n ↔ Node-RED** - Workflow automation triggers
- **WhatsApp/Discord** - Notification integrations

## 🔗 Related Technologies

- **MQTT**: `../mqtt/` - Message broker integration
- **Ignition**: `../ignition/` - SCADA/HMI integration via OPC UA
- **n8n**: `../n8n/` - Advanced workflow automation
- **Docker**: `../docker/` - Containerized Node-RED deployment

## 📊 Current Projects Using Node-RED

- **CT-084**: Parachute Drop - Phidget sensor integration flows
- **CT-085**: Network Discovery - Protocol scanning visualization
- **Steel Bonnet**: Brewery automation - Complete production flows
- **Monitoring System**: Real-time equipment dashboards

## 🎯 Common Node-RED Patterns in This Stack

1. **MQTT Bridge**: MQTT In → Transform → MQTT Out to different topics
2. **Protocol Translation**: Modbus/OPC UA → MQTT for unified messaging
3. **Alert Workflows**: Equipment data → Threshold check → Notifications
4. **Dashboard Creation**: Real-time data → UI elements → Web interface
5. **Edge Processing**: Local computation before cloud transmission

## 💡 Node-RED Best Practices

- **Flow Organization**: Group by function, use link nodes for clarity
- **Error Handling**: Always include catch nodes for production flows
- **Documentation**: Use comment nodes to explain complex logic
- **Version Control**: Export flows as JSON for Git tracking
- **Performance**: Limit debug nodes in production

---
*Last Updated: 2025-06-28 | Files: Being organized | Status: Active Development*