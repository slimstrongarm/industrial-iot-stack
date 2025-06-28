# Node-RED Steel Bonnet Brewery Automation - Updated Installation Guide

## Overview
This guide provides step-by-step instructions for installing the Steel Bonnet brewery automation system in Node-RED using the actual flow files in this repository. The system provides comprehensive equipment management, multi-protocol integration, manual data entry, and testing capabilities.

## Available Flow Files

### Core System Flows (node-red-flows/)
- `protocol_core_flow.json` - Central protocol management hub
- `equipment_registration_flow.json` - Equipment registration and management
- `equipment_registration_forms_flow.json` - Advanced registration forms
- `monitoring_dashboard_flow.json` - Real-time monitoring
- `data_simulation_flow.json` - Testing and simulation

### Protocol Modules (node-red-flows/)
- `mqtt_protocol_module_flow.json` - MQTT integration
- `mqtt_discovery_flow.json` - MQTT device discovery
- `mqtt_analysis_flow.json` - MQTT traffic analysis
- `modbus_protocol_module_flow.json` - Modbus integration
- `phidget_discovery_flow.json` - Phidget device discovery
- `phidget_registration_flow.json` - Phidget registration
- `phidget_data_flow.json` - Phidget data processing
- `opcua_client_bridge_flow.json` - OPC UA client
- `opcua_data_sync_flow.json` - OPC UA data synchronization

### Event Processing (node-red-flows/)
- `event_processing_core_flow.json` - Event handling system
- `manual_event_entry_flow.json` - Manual event entry
- `event_dashboard_flow.json` - Event monitoring

### User Interfaces (views/)
- `operator_data_entry_flow.json` - Operator data entry forms
- `mobile_dashboard_flow.json` - Mobile-optimized interface
- `compliance_reporting_flow.json` - Regulatory compliance

### Multi-Instance Architecture (views/)
- `main_coordinator_instance_flow.json` - Central coordinator
- `satellite_phidget_instance_flow.json` - Phidget satellite
- `satellite_remote_instance_flow.json` - Remote location satellite
- `inter_instance_communication_flow.json` - Instance communication
- `failover_redundancy_flow.json` - High availability

### Testing Tools
- `equipment_simulator_flow.json` (views/) - Equipment simulation
- `opc_validation_tools_flow.json` - OPC validation
- `performance_monitoring_flow.json` - Performance monitoring

## Prerequisites

### System Requirements
- Node-RED 3.0+ installed
- Node.js 16+ 
- Minimum 4GB RAM (8GB recommended)
- Network connectivity to brewery equipment
- Access to Ignition SCADA system (if using OPC UA)

### Required Node-RED Nodes
```bash
# Core protocol nodes
npm install node-red-contrib-opcua
npm install node-red-contrib-modbus
npm install node-red-contrib-mqtt-broker
npm install node-red-contrib-phidget22

# UI and dashboard nodes  
npm install node-red-dashboard
npm install node-red-contrib-ui-led

# Database and storage
npm install node-red-node-mysql
npm install node-red-node-sqlite

# Utility nodes
npm install node-red-node-email
```

## Installation Order

### Phase 1: Core Infrastructure (Required)

1. **Protocol Core System** (`protocol_core_flow.json`)
   ```
   Menu → Import → Select file → node-red-flows/protocol_core_flow.json → Import
   ```
   - Central hub for all protocols
   - Must be installed FIRST
   - Configure MQTT broker connection in MQTT nodes

2. **Equipment Registration** (`equipment_registration_flow.json`)
   ```
   Menu → Import → Select file → node-red-flows/equipment_registration_flow.json → Import
   ```
   - Basic equipment registration
   - Depends on Protocol Core
   - Access dashboard at `/ui`

3. **Monitoring Dashboard** (`monitoring_dashboard_flow.json`)
   ```
   Menu → Import → Select file → node-red-flows/monitoring_dashboard_flow.json → Import
   ```
   - Real-time data visualization
   - Depends on Protocol Core

### Phase 2: Protocol Integration (Choose as needed)

4. **MQTT Integration**
   ```bash
   # Import in this order:
   node-red-flows/mqtt_protocol_module_flow.json
   node-red-flows/mqtt_discovery_flow.json
   node-red-flows/mqtt_analysis_flow.json
   ```
   - Configure MQTT broker settings
   - Test with: `mosquitto_pub -t "test/topic" -m "test"`

5. **Phidget Integration**
   ```bash
   # Import in this order:
   node-red-flows/phidget_discovery_flow.json
   node-red-flows/phidget_registration_flow.json
   node-red-flows/phidget_data_flow.json
   ```
   - Requires Phidget drivers installed
   - Configure Phidget Network Server

6. **Modbus Integration**
   ```
   node-red-flows/modbus_protocol_module_flow.json
   ```
   - Configure device IP addresses
   - Set polling intervals

7. **OPC UA Integration**
   ```bash
   # Import both:
   node-red-flows/opcua_client_bridge_flow.json
   node-red-flows/opcua_data_sync_flow.json
   ```
   - Configure OPC UA server endpoint
   - Set security credentials

### Phase 3: Event Processing

8. **Event System**
   ```bash
   # Import in this order:
   node-red-flows/event_processing_core_flow.json
   node-red-flows/manual_event_entry_flow.json
   node-red-flows/event_dashboard_flow.json
   ```

### Phase 4: Advanced Features

#### Option A: Single Instance (< 50 devices)
Continue with Phase 5 directly

#### Option B: Multi-Instance Architecture (50+ devices)

9. **Main Coordinator**
   ```
   views/main_coordinator_instance_flow.json
   ```

10. **Satellite Instances** (as needed)
    ```
    views/satellite_phidget_instance_flow.json
    views/satellite_remote_instance_flow.json
    ```

11. **Inter-Instance Communication**
    ```
    views/inter_instance_communication_flow.json
    views/failover_redundancy_flow.json
    ```

### Phase 5: User Interfaces

12. **Operator Interfaces**
    ```bash
    # Import all:
    views/operator_data_entry_flow.json
    views/mobile_dashboard_flow.json
    views/compliance_reporting_flow.json
    ```

### Phase 6: Testing Tools (Recommended)

13. **Testing and Validation**
    ```bash
    # Import:
    views/equipment_simulator_flow.json
    opc_validation_tools_flow.json
    performance_monitoring_flow.json
    ```

## Configuration Steps

### 1. MQTT Configuration
After importing protocol_core_flow.json:
- Double-click any MQTT node
- Set broker to your MQTT server (default: localhost:1883)
- Configure topics: `brewery/#`

### 2. Equipment Registration
- Access dashboard: `http://localhost:1880/ui`
- Navigate to "Equipment Registration"
- Register your equipment with ISA-95 hierarchy

### 3. Protocol Module Setup
For each protocol you're using:
- Configure connection settings
- Map to registered equipment
- Test with simulation data

## Testing Your Installation

### Test 1: Core System
```javascript
// In a function node, inject:
msg.payload = {
    id: "TEST001",
    source: { protocol: "test" },
    equipment: { name: "Test Sensor" },
    data: { value: 42 }
};
return msg;
```

### Test 2: MQTT
```bash
mosquitto_pub -t "brewery/test/sensor" -m '{"value": 68.5, "unit": "F"}'
```

### Test 3: Equipment Simulator
- Import `equipment_simulator_flow.json`
- Open simulator dashboard
- Create test equipment
- Verify data flow

## Troubleshooting

### Common Issues

**Flows not connecting:**
- Ensure protocol_core_flow.json is deployed first
- Check link nodes are properly configured
- Verify MQTT broker is running

**Dashboard not accessible:**
- Install node-red-dashboard: `npm install node-red-dashboard`
- Restart Node-RED
- Access at `http://localhost:1880/ui`

**Equipment not registering:**
- Check equipment registry is initialized
- Verify MQTT topics match expected patterns
- Review debug output in Node-RED

## Architecture Overview

```
Protocol Core (Hub)
    ├── Equipment Registration
    ├── Protocol Modules
    │   ├── MQTT Module
    │   ├── Phidget Module
    │   ├── Modbus Module
    │   └── OPC UA Module
    ├── Event Processing
    ├── Monitoring Dashboard
    └── Data Routing to Ignition
```

## Next Steps

1. Start with Phase 1 (Core Infrastructure)
2. Add protocol modules based on your equipment
3. Configure equipment registration
4. Test with simulator before connecting real devices
5. Deploy user interfaces as needed
6. Enable performance monitoring

## Support

- Check debug panel in Node-RED for errors
- Review flow descriptions for configuration details
- Test with equipment simulator first
- Monitor performance dashboard for bottlenecks

---

**Updated**: January 2025  
**Version**: 2.0  
**Note**: This guide reflects the actual flow files in the repository