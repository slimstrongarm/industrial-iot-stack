# Node-RED Setup Guide for Steel Bonnet

This guide walks you through setting up Node-RED to work with the Steel Bonnet OPC UA architecture in Ignition.

## Prerequisites

✅ Ignition with OPC UA structure created (you've done this!)
✅ Node-RED installed
✅ OPC UA client nodes for Node-RED

## Step 1: Install Required Node-RED Nodes

Open Node-RED and install these nodes via Palette Manager:

```bash
# Via command line:
npm install node-red-contrib-opcua
npm install node-red-dashboard
npm install node-red-contrib-ui-level

# Or search in Palette Manager:
- node-red-contrib-opcua
- node-red-dashboard
- node-red-contrib-ui-level
```

## Step 2: Configure OPC UA Connection

### Ignition OPC UA Server Settings

1. In Ignition Gateway, go to **Config > OPC UA > Server Settings**
2. Note your endpoint URL (typically `opc.tcp://localhost:62541/discovery`)
3. Create a user for Node-RED if needed

### Node-RED OPC UA Client Configuration

1. In Node-RED, add an **OpcUa-Client** node
2. Double-click to configure:
   - **Endpoint**: `opc.tcp://[YOUR_IGNITION_IP]:62541/discovery`
   - **Security Policy**: None (for testing)
   - **Security Mode**: None (for testing)
   - **User**: Your Ignition username
   - **Password**: Your Ignition password

## Step 3: Tag Paths in Ignition OPC UA

Your Ignition tags are exposed via OPC UA with this format:

```
ns=2;s=[default]TagPath

Examples:
ns=2;s=[default]OPCUA/Data/TestCorp/Plant01/Production/TestPump_01/payload
ns=2;s=[default]OPCUA/Data/TestCorp/Plant01/Production/TestPump_01/_trigger
ns=2;s=[default]Enterprise/TestCorp/Plant01/Production/TestPump_01/flow_rate
```

## Step 4: Import Node-RED Flows

Import these flows for different use cases:

### A. Equipment Registration Flow
- Form-based equipment registration
- Writes to `[default]OPCUA/Registration/Pending/`
- Waits for Ignition response

### B. Data Simulation Flow
- Simulates 4-20mA sensor data
- Writes to `[default]OPCUA/Data/` structure
- Triggers Ignition processing

### C. Dashboard Monitoring
- Real-time equipment monitoring
- Reads from `[default]Enterprise/` structure
- Shows scaled engineering values

### D. Alarm Management
- Monitors equipment alarms
- Sends notifications
- Logs alarm history

## Step 5: Test the Connection

1. Deploy a simple test flow:
   - **Inject** node → **OpcUa-Client** node → **Debug** node
   
2. Configure OpcUa-Client to read:
   ```
   NodeId: ns=2;s=[default]OPCUA/Config/equipment_type_mappings
   ```

3. Deploy and test - you should see the JSON configuration

## Step 6: Equipment Registration Workflow

1. User fills form in Node-RED dashboard
2. Node-RED writes to:
   - `[default]OPCUA/Registration/Pending/[timestamp]/enterprise`
   - `[default]OPCUA/Registration/Pending/[timestamp]/site`
   - `[default]OPCUA/Registration/Pending/[timestamp]/area`
   - `[default]OPCUA/Registration/Pending/[timestamp]/equipment_name`
   - `[default]OPCUA/Registration/Pending/[timestamp]/equipment_type`
   - `[default]OPCUA/Registration/Pending/[timestamp]/trigger` = true

3. Ignition processes and creates equipment in UNS

4. Node-RED checks response at:
   - `[default]OPCUA/Responses/Registration/[timestamp]/success`
   - `[default]OPCUA/Responses/Registration/[timestamp]/message`

## Step 7: Data Flow Workflow

1. Node-RED collects sensor data (4-20mA signals)
2. Writes JSON payload to:
   ```
   [default]OPCUA/Data/[Enterprise]/[Site]/[Area]/[Equipment]/payload
   ```

3. Sets trigger:
   ```
   [default]OPCUA/Data/[Enterprise]/[Site]/[Area]/[Equipment]/_trigger = true
   ```

4. Ignition processes:
   - Scales 4-20mA to engineering units
   - Updates equipment tags
   - Publishes to MQTT if configured

5. Node-RED can monitor results at:
   ```
   [default]Enterprise/[Enterprise]/[Site]/[Area]/[Equipment]/[tag_name]
   ```

## Troubleshooting

### Connection Issues
- Verify Ignition OPC UA is enabled
- Check firewall allows port 62541
- Test with UaExpert first
- Enable anonymous access for testing

### Tag Not Found
- Tags must exist in Ignition first
- Check exact spelling and case
- Use browse function to verify paths
- Ensure proper namespace (ns=2)

### Write Failures
- Check tag permissions
- Verify data types match
- Some tags may be read-only
- Check Ignition logs

### Performance
- Batch writes when possible
- Use subscription for monitoring
- Limit poll rates
- Consider Edge deployment

## Security Best Practices

1. **Production Setup**:
   - Enable OPC UA security
   - Use certificates
   - Implement user authentication
   - Restrict tag access

2. **Network Security**:
   - Use VPN or private network
   - Implement firewall rules
   - Monitor access logs
   - Regular security updates

## Next Steps

1. Import the provided Node-RED flows
2. Customize for your equipment types
3. Build dashboards for operators
4. Set up alarm notifications
5. Configure data historians
6. Implement redundancy

## Example OPC UA Operations

### Read Tag Value
```javascript
msg.topic = "ns=2;s=[default]Enterprise/TestCorp/Plant01/Production/TestPump_01/flow_rate";
msg.datatype = "Float";
msg.attributeId = 13; // Value
```

### Write Tag Value
```javascript
msg.topic = "ns=2;s=[default]OPCUA/Data/TestCorp/Plant01/Production/TestPump_01/flow_rate";
msg.payload = 15.2; // 4-20mA value
msg.datatype = "Float";
```

### Browse Tags
```javascript
msg.topic = "ns=2;s=[default]OPCUA";
msg.browseName = "";
```

## Support Resources

- Ignition OPC UA Documentation
- Node-RED OPC UA Node Documentation
- Steel Bonnet GitHub Repository
- Community Forums