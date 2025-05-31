# TODO: Node-RED Flow Cleanup & Standardization

## Current Status
- ✅ Multiple flows exist in Steel_Bonnet/node-red-flows/
- ⏳ Need consolidation and cleanup
- ⏳ Self-aware equipment pattern to implement
- ⏳ Standard error handling needed

## Phase 1: Flow Assessment & Cleanup

### 1.1 Inventory Existing Flows
- [ ] Document each flow's purpose:
  - [ ] flows.json - Main flow file
  - [ ] ignition_opc_config_flow.json - OPC config
  - [ ] opc_connection_manager.json - Connection management
  - [ ] equipment_simulator_flow.json - Testing
- [ ] Identify duplicate functionality
- [ ] Mark flows for consolidation
- [ ] Backup all flows before changes

### 1.2 Create Standard Flow Structure
- [ ] Main Equipment Registration Flow
- [ ] Data Processing Flow
- [ ] Alarm Management Flow
- [ ] Diagnostics/Health Flow
- [ ] Test/Simulation Flow

### 1.3 Implement Flow Standards
- [ ] Consistent error handling
- [ ] Standard logging format
- [ ] Flow documentation headers
- [ ] Subflow for common patterns
- [ ] Environment variable usage

## Phase 2: Self-Aware Equipment Pattern

### 2.1 Registration Flow
```javascript
// Equipment announces itself
// Input: MQTT topic: SteelBonnet/+/+/+/announce
// Process: Validate → Create UDT → Confirm
```
- [ ] Create registration subflow
- [ ] Validate equipment against schema
- [ ] Check for duplicate registrations
- [ ] Create Ignition tags via OPC-UA
- [ ] Store equipment registry
- [ ] Send acknowledgment

### 2.2 Heartbeat Management
- [ ] Create heartbeat receiver
- [ ] Update last-seen timestamps
- [ ] Detect missing heartbeats
- [ ] Generate offline alarms
- [ ] Auto-recovery on reconnect

### 2.3 Dynamic Topic Subscription
- [ ] Subscribe to equipment-specific topics after registration
- [ ] Handle topic wildcards efficiently
- [ ] Manage subscription lifecycle
- [ ] Clean up on equipment removal

## Phase 3: Data Flow Optimization

### 3.1 MQTT to OPC-UA Bridge
- [ ] Batch tag updates (reduce OPC calls)
- [ ] Implement change-only updates
- [ ] Add data validation rules
- [ ] Handle timestamp synchronization
- [ ] Quality code mapping

### 3.2 Standard Data Transformations
- [ ] Engineering unit conversions
- [ ] Data type standardization
- [ ] Null/undefined handling
- [ ] Array/object flattening
- [ ] Metadata enrichment

### 3.3 Performance Optimization
- [ ] Rate limiting for high-frequency data
- [ ] Message queuing for bursts
- [ ] Connection pooling for OPC-UA
- [ ] Memory usage monitoring
- [ ] CPU usage optimization

## Phase 4: Production Features

### 4.1 Security
- [ ] MQTT authentication
- [ ] Topic ACLs
- [ ] OPC-UA certificates
- [ ] Encrypted credentials
- [ ] Audit logging

### 4.2 Monitoring & Diagnostics
- [ ] Flow performance metrics
- [ ] Message counters
- [ ] Error rate tracking
- [ ] Latency measurement
- [ ] Dashboard creation

### 4.3 Deployment & Backup
- [ ] Git integration for flows
- [ ] Automated backup schedule
- [ ] Flow versioning
- [ ] Rollback procedures
- [ ] Change documentation

## Success Criteria
- [ ] Single flow handles all equipment types
- [ ] Auto-discovery of new equipment
- [ ] < 100ms latency MQTT to OPC
- [ ] Zero message loss
- [ ] Self-documenting flows

## Code Patterns to Implement

### Registration Handler
```javascript
// Standardized registration handler
const equipment = msg.payload.equipment;
const udtType = mapEquipmentToUDT(equipment.type);
const tagPath = buildUNSPath(equipment);

// Create in Ignition
createIgnitionTags(tagPath, udtType);

// Store in context
flow.set(`equipment.${equipment.id}`, equipment);

// Send confirmation
msg.payload = {
    action: "registered",
    id: equipment.id,
    tagPath: tagPath,
    timestamp: new Date().toISOString()
};
return msg;
```

### For Your Controls Engineer
- All equipment follows same registration pattern
- Standard tag structure for HMI binding
- Predictable alarm paths
- Consistent status indicators