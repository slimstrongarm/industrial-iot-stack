# Node-RED Testing Roadmap - Steel Bonnet

## Current State
- **Total Flows**: 18 application flows
- **Debugged Flows**: 4 (monitoring_dashboard, mqtt_protocol, modbus_protocol, event_processing)
- **Deployment System**: ✅ One-button deployment working
- **Dashboard**: ✅ UI operational with layout fixes applied

## Testing Sequence

### Phase 1: Core Foundation (Morning)
**Goal**: Establish working core infrastructure

1. **protocol_core_flow.json** [30 min]
   - Dependencies: None
   - Test: Data normalization, protocol registration
   - Success Criteria: Can register protocols, normalize data formats

2. **equipment_registration_flow.json** [45 min]
   - Dependencies: protocol_core
   - Test: Equipment CRUD operations, registry management
   - Success Criteria: Can add/edit/delete equipment entries

3. **equipment_registration_forms_flow.json** [30 min]
   - Dependencies: equipment_registration
   - Test: UI forms, validation, data submission
   - Success Criteria: Forms display correctly, validation works

### Phase 2: Protocol Integration (Late Morning)
**Goal**: Verify protocol handlers work with core

4. **opcua_client_bridge_flow.json** [45 min]
   - Dependencies: protocol_core
   - Test: OPC UA connection, data reading
   - Success Criteria: Can simulate OPC data (no server required)

5. **opcua_data_sync_flow.json** [30 min]
   - Dependencies: opcua_client_bridge
   - Test: Data synchronization, buffering
   - Success Criteria: Data flows from OPC to system

### Phase 3: Data Flow Testing (Early Afternoon)
**Goal**: Verify data simulation and processing

6. **data_simulation_flow.json** [30 min]
   - Dependencies: equipment_registration
   - Test: 4-20mA signal generation, equipment simulation
   - Success Criteria: Generates realistic sensor data

7. **manual_event_entry_flow.json** [30 min]
   - Dependencies: event_processing_core
   - Test: Manual event creation UI
   - Success Criteria: Can create and submit events

8. **event_dashboard_flow.json** [30 min]
   - Dependencies: event_processing_core
   - Test: Event display, filtering, acknowledgment
   - Success Criteria: Shows events in real-time

### Phase 4: Device-Specific Flows (Mid Afternoon)
**Goal**: Test specialized device integrations

9. **phidget_discovery_flow.json** [30 min]
   - Dependencies: protocol_core
   - Test: Device discovery simulation
   - Success Criteria: Discovers simulated Phidget devices

10. **phidget_registration_flow.json** [30 min]
    - Dependencies: phidget_discovery, equipment_registration
    - Test: Device registration process
    - Success Criteria: Can register discovered devices

11. **phidget_data_flow.json** [30 min]
    - Dependencies: phidget_registration
    - Test: Data collection from Phidget devices
    - Success Criteria: Processes Phidget sensor data

### Phase 5: Analysis & Discovery (Late Afternoon)
**Goal**: Test analysis and discovery features

12. **mqtt_discovery_flow.json** [30 min]
    - Dependencies: mqtt_protocol_module
    - Test: MQTT topic discovery, device detection
    - Success Criteria: Discovers MQTT topics/devices

13. **mqtt_analysis_flow.json** [30 min]
    - Dependencies: mqtt_discovery
    - Test: MQTT traffic analysis, pattern detection
    - Success Criteria: Analyzes MQTT data patterns

14. **valve_control_discovery_flow.json** [30 min]
    - Dependencies: modbus_protocol_module
    - Test: Valve discovery via Modbus
    - Success Criteria: Discovers valve controllers

## Testing Approach

### For Each Flow:
1. **Initial Check** (5 min)
   - Deploy using Ctrl+Shift+D
   - Check for errors in debug panel
   - Verify flow appears in Node-RED

2. **Standalone Test** (10-15 min)
   - Enable simulation mode
   - Trigger test data generation
   - Verify outputs in debug panel

3. **Integration Test** (10-15 min)
   - Connect to dependent flows
   - Verify data flow between components
   - Check global context sharing

4. **UI Test** (if applicable) (5-10 min)
   - Navigate to dashboard tab
   - Verify UI elements render
   - Test user interactions

## Quick Fixes for Common Issues

### Missing Global Debug Config
```javascript
// Add to a function node in any flow:
global.set('debugSettings', {
    enabled: true,
    mode: 'testing',
    simulationEnabled: true,
    opcEnabled: false
});
```

### Debug Errors (simulateEvents, etc.)
- These occur when debug config isn't initialized
- Run the fix above in an inject node
- Errors should clear after initialization

### Flow Not Appearing in UI
- Check dashboard tab/group configuration
- Ensure ui_base node exists
- Verify tab has a label and order

## Success Metrics
- [ ] All 14 remaining flows deployed without critical errors
- [ ] Core infrastructure flows working together
- [ ] At least one flow from each category tested
- [ ] Data flowing through protocol → core → dashboard
- [ ] No blocking errors preventing basic operation

## Notes
- Focus on **functional testing** not performance
- Use **simulation mode** to avoid external dependencies
- Document any flows that need debug infrastructure added
- Prioritize getting data flowing end-to-end over perfect individual flows