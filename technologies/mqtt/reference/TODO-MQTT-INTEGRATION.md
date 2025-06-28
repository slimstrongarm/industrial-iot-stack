# TODO: MQTT → Node-RED → Ignition Integration

## Current Status
- ✅ Mosquitto MQTT Broker installed (default port 1883)
- ✅ Ignition Edge Gateway running (trial)
- ✅ Node-RED flows exist in Steel_Bonnet repo
- ⏳ Integration testing needed

## Phase 1: Validate Basic Connectivity

### 1.1 Test MQTT Broker
- [ ] Verify Mosquitto is running: `sudo systemctl status mosquitto`
- [ ] Test local publish/subscribe:
  ```bash
  # Terminal 1: Subscribe
  mosquitto_sub -h localhost -t "test/#" -v
  
  # Terminal 2: Publish
  mosquitto_pub -h localhost -t "test/hello" -m "MQTT is working"
  ```
- [ ] Document MQTT broker IP for Node-RED config

### 1.2 Configure Node-RED MQTT Connection
- [ ] Open Node-RED (http://localhost:1880)
- [ ] Check MQTT broker configuration nodes
- [ ] Verify connection status (should show "connected")
- [ ] Test with debug node on simple topic

### 1.3 Configure Ignition OPC-UA Server
- [ ] Enable OPC-UA server in Ignition Gateway
- [ ] Note the endpoint URL (typically `opc.tcp://localhost:62541/discovery`)
- [ ] Set up test folder structure in Ignition tags
- [ ] Create `SteelBonnet/Test` folder for testing

## Phase 2: Equipment Registration Flow

### 2.1 Standard Registration Payload
- [ ] Define registration message format:
  ```json
  {
    "action": "register",
    "timestamp": "ISO-8601",
    "equipment": {
      "id": "unique_id",
      "name": "Human Readable Name",
      "type": "equipment_type",
      "area": "location",
      "capabilities": {
        "sensors": ["temperature", "pressure"],
        "controls": ["pump_speed", "valve_position"],
        "alarms": ["high_temp", "low_pressure"]
      }
    }
  }
  ```

### 2.2 Node-RED Registration Handler
- [ ] Create/update registration flow
- [ ] Parse equipment type and capabilities
- [ ] Map to appropriate Ignition UDT
- [ ] Create tag structure dynamically
- [ ] Send confirmation back via MQTT

### 2.3 Heartbeat/Watchdog Pattern
- [ ] Define heartbeat interval (30 seconds?)
- [ ] Create status tags in Ignition
- [ ] Implement "last seen" timestamp
- [ ] Create alarm for missing heartbeat
- [ ] Test equipment going offline/online

## Phase 3: Data Flow Testing

### 3.1 Test Equipment Types
- [ ] Pump test payload and UDT creation
- [ ] Tank test payload and UDT creation
- [ ] Valve test payload and UDT creation
- [ ] Environmental sensor payload

### 3.2 Data Quality Handling
- [ ] Good quality data flow
- [ ] Bad quality data handling
- [ ] Stale data detection
- [ ] Error state propagation

### 3.3 Performance Testing
- [ ] Single equipment updates
- [ ] Bulk updates (10+ tags)
- [ ] Rapid update testing (1-second intervals)
- [ ] Memory/CPU monitoring

## Success Criteria
- [ ] Equipment can self-register via MQTT
- [ ] Tags appear in Ignition within 2 seconds
- [ ] Heartbeat shows equipment online/offline status
- [ ] Data quality is preserved through the pipeline
- [ ] No memory leaks after 24-hour test

## Notes for Controls Engineer Partner
- Tag naming follows UNS structure
- All equipment gets standard status/control folders
- Alarm configuration in UDTs
- Screen templates can bind to UDT instances

## Integration Points
- MQTT Topics: `SteelBonnet/+/+/+/register` for registration
- Data Topics: `SteelBonnet/+/+/+/data`
- Command Topics: `SteelBonnet/+/+/+/cmd`