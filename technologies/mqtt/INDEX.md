# MQTT Technology Stack - Complete File Index
*Every MQTT-related file in the industrial IoT stack*

## 🚀 Quick Access for Claude Instances

**New to this codebase?** Start with:
1. `reference/MQTT_BROKER_ARCHITECTURE.md` - Core architecture
2. `setup-guides/EMQX_BROKER_STATUS.md` - Current broker status  
3. `implementations/` - Working examples from real projects

## 📂 Complete File Listing

### 🏗️ Reference & Architecture
```
reference/
├── MQTT_BROKER_ARCHITECTURE.md          # Core MQTT design patterns  
└── TODO-MQTT-INTEGRATION.md             # Integration roadmap
```

### ⚙️ Setup Guides (13 files)
```
setup-guides/
├── EMQX_AUTH_FIX_MANUAL.md              # EMQX authentication setup
├── EMQX_BROKER_STATUS.md                # Current broker configuration  
├── EMQX_CLIENT_CREATED.md               # Client creation process
├── EMQX_CLIENTID_AUTH.md                # Client ID authentication
├── EMQX_DASHBOARD_ACCESS.md             # EMQX web dashboard setup
├── EMQX_DISABLE_AUTH_GUIDE.md           # Disable auth for testing
├── EMQX_FIXED_STATUS.md                 # Fixed configuration status
├── EMQX_MQTT_CREDENTIALS.md             # Credential management
├── N8N_MQTT_COMPLETE_GUIDE.md           # Complete n8n-MQTT integration
├── N8N_MQTT_CREDENTIAL_SETUP.md         # n8n MQTT credentials
├── N8N_MQTT_NETWORK_FIX.md              # n8n network configuration
├── N8N_MQTT_WORKING_CONFIG.md           # Working n8n configuration
└── NODE_RED_MQTT_SETUP.md               # Node-RED MQTT setup
```

### 🔧 Troubleshooting (4 files)
```
troubleshooting/
├── EMQX_NETWORK_TROUBLESHOOTING.md      # EMQX network issues
├── MQTT_AUTH_DEBUG.md                   # Authentication debugging
├── MQTT_INTEGRATION_TEST.md             # Integration testing
└── MQTT_WORKFLOW_FIX.md                 # Workflow troubleshooting
```

### 🏭 Real Implementations (7 files)
```
implementations/
├── brewery_actual_mqtt_analysis.md       # Live brewery MQTT analysis
├── brewery_mqtt_analysis.md              # Brewery MQTT design analysis  
├── BREWERY_MQTT_INTEGRATION_GUIDE.md     # Complete brewery integration
├── mqtt-whatsapp-integration.md          # MQTT → WhatsApp alerts
├── steel-bonnet-edge-testing.md          # Edge device MQTT testing
├── steel-bonnet-protocol-module.md       # Steel Bonnet MQTT protocol
└── steel-bonnet-topic-map.md             # Steel Bonnet topic mapping
```

## 🎯 MQTT Usage Patterns

### Authentication & Security
- **EMQX Setup**: `setup-guides/EMQX_AUTH_FIX_MANUAL.md`
- **Client Management**: `setup-guides/EMQX_CLIENT_CREATED.md`  
- **Debug Auth Issues**: `troubleshooting/MQTT_AUTH_DEBUG.md`

### Integration Patterns
- **Node-RED Integration**: `setup-guides/NODE_RED_MQTT_SETUP.md`
- **n8n Workflows**: `setup-guides/N8N_MQTT_COMPLETE_GUIDE.md`
- **Cross-System**: `reference/MQTT_BROKER_ARCHITECTURE.md`

### Production Examples
- **Steel Bonnet Brewery**: `implementations/steel-bonnet-*`
- **WhatsApp Alerts**: `implementations/mqtt-whatsapp-integration.md`
- **Live Analysis**: `implementations/brewery_actual_mqtt_analysis.md`

## 🔗 Related Technologies

- **Node-RED**: `../node-red/` - MQTT message processing flows
- **n8n**: `../n8n/` - MQTT workflow automation
- **Ignition**: `../ignition/` - MQTT ↔ OPC UA bridging
- **Docker**: `../docker/` - MQTT broker containerization

## 📊 Project Cross-References

- **CT-084 Parachute Drop**: Edge device MQTT telemetry
- **CT-085 Network Discovery**: MQTT device scanning
- **Steel Bonnet Project**: Production brewery MQTT implementation  
- **WhatsApp Integration**: MQTT-triggered notifications

## 🎯 Common Commands

```bash
# Test MQTT connection
mosquitto_pub -h localhost -t test/topic -m "test message"

# Monitor MQTT traffic  
mosquitto_sub -h localhost -t '#' -v

# Check EMQX status
docker logs emqx

# Access EMQX dashboard
http://localhost:18083 (admin/public)
```

---
*Files Organized: 24 | Last Updated: 2025-06-28 | Status: ✅ Ready for Claude*