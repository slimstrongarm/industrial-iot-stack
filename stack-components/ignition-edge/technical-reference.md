# Ignition Edge Technical Reference

## Core Features and Capabilities

### Edge Computing Platform
- **Local HMI Runtime**: Run Vision or Perspective clients locally without internet connectivity
- **Edge Compute**: Process data at the source, reducing bandwidth and latency
- **Limited Tag Count**: 500 tags (Standard Edge), unlimited with Edge Enterprise
- **No Database Connections**: Edge editions cannot directly connect to databases
- **Local Historian**: Store up to 1 week of data locally (configurable)
- **Edge Gateway Network**: Connect to central Ignition Gateway for data synchronization

### Key Differences from Full Ignition
- No direct database connections (use MQTT/Gateway Network for data storage)
- Limited designer connections (2 concurrent)
- No redundancy support
- Limited alarm notification options
- No reporting module support

## Jython 2.7 Scripting Guidelines

### Best Practices
```python
# Always use explicit imports
from java.util import Date
from java.lang import Thread

# Handle exceptions properly
def read_tag_safely(tagPath):
    try:
        value = system.tag.read(tagPath).value
        return value if value is not None else 0
    except Exception as e:
        system.util.getLogger("EdgeScripts").error("Tag read failed: %s" % str(e))
        return 0

# Use system.util.invokeAsynchronous for long-running tasks
def process_data_async():
    def long_task():
        # Heavy processing here
        pass
    system.util.invokeAsynchronous(long_task)
```

### Common Pitfalls
- **String Formatting**: Use `%` formatting, not f-strings (Python 2.7)
- **Print Statements**: Use `print "text"` not `print("text")`
- **Division**: Integer division by default, use `float()` for decimals
- **Unicode**: Explicitly handle with `u"string"` prefix

### Memory Management
```python
# Clear large objects after use
data = system.dataset.toDataSet(headers, rows)
# Process data...
data = None  # Help garbage collection

# Use generators for large datasets
def process_large_dataset(dataset):
    for row in xrange(dataset.getRowCount()):
        yield dataset.getValueAt(row, "value")
```

## OPC-UA Server Configuration

### Server Setup
1. **Enable OPC-UA Module**: Modules → OPC-UA → Settings
2. **Configure Endpoints**:
   ```
   Endpoint URL: opc.tcp://[hostname]:62541/discovery
   Security Policies: Basic256Sha256, None (for testing only)
   ```

3. **Expose Tags**:
   ```python
   # Script to expose tags to OPC-UA
   tags = ["Edge/Production/Line1/*", "Edge/Quality/*"]
   for pattern in tags:
       system.opcua.addServerNode(pattern)
   ```

### Security Configuration
- **Anonymous Access**: Disable in production
- **User Source**: Configure OPC-UA specific user source
- **Certificates**: Generate and install proper certificates
- **Allowed Clients**: Whitelist client certificates

## UDT (User Defined Types) Management

### UDT Best Practices
```json
{
  "name": "Motor",
  "typeId": "Motor_Type",
  "tags": [
    {
      "name": "Status",
      "dataType": "Int4",
      "opcItemPath": "{InstanceName}/Status"
    },
    {
      "name": "Speed",
      "dataType": "Float4",
      "opcItemPath": "{InstanceName}/Speed",
      "engUnit": "RPM"
    },
    {
      "name": "RunHours",
      "dataType": "Float8",
      "opcItemPath": "{InstanceName}/RunHours"
    }
  ],
  "parameters": {
    "MotorID": {
      "dataType": "String",
      "value": ""
    },
    "MaxSpeed": {
      "dataType": "Int4",
      "value": 3600
    }
  }
}
```

### UDT Inheritance
```python
# Create base UDT
baseMotor = {
    "name": "BaseMotor",
    "tags": ["Status", "Speed", "Current"]
}

# Extend for specific motor types
vfdMotor = {
    "name": "VFDMotor",
    "parentType": "BaseMotor",
    "tags": ["Frequency", "Torque"]
}
```

## Tag Structure and UNS Naming Conventions

### Unified Namespace (UNS) Structure
```
Enterprise/
├── Site/
│   ├── Area/
│   │   ├── Line/
│   │   │   ├── Cell/
│   │   │   │   ├── Equipment/
│   │   │   │   │   ├── Status
│   │   │   │   │   ├── Production
│   │   │   │   │   └── Quality
```

### Naming Conventions
- **Use PascalCase**: `ProductionCount`, not `production_count`
- **Avoid Abbreviations**: `Temperature`, not `Temp`
- **Include Units**: `Speed_RPM`, `Pressure_PSI`
- **Timestamp Format**: `LastUpdate_UTC`

### Example Tag Structure
```
Plant1/
├── Packaging/
│   ├── Line1/
│   │   ├── Filler/
│   │   │   ├── Status (Int: 0=Off, 1=Running, 2=Fault)
│   │   │   ├── BottleCount (Int)
│   │   │   ├── Speed_BPM (Float)
│   │   │   └── Efficiency_Percent (Float)
│   │   └── Capper/
│   │       ├── Status
│   │       ├── TorqueSetpoint_NM
│   │       └── RejectCount
```

## Store and Forward Configuration

### System Setup
```python
# Enable Store and Forward
system.tag.write("[System]Gateway/StoreAndForward/Enabled", True)

# Configure memory buffer
system.tag.write("[System]Gateway/StoreAndForward/MemoryBufferSize", 10000)  # records

# Set disk cache
system.tag.write("[System]Gateway/StoreAndForward/DiskCacheEnabled", True)
system.tag.write("[System]Gateway/StoreAndForward/DiskCacheSize", 100)  # MB
```

### History Configuration
```python
# Configure tag history with store and forward
tagConfig = {
    "name": "ProductionCount",
    "historyEnabled": True,
    "historyProvider": "EdgeHistorian",
    "historicalDeadband": 1.0,
    "historicalDeadbandMode": "Absolute",
    "sampleMode": "OnChange",
    "storageProvider": "StoreAndForward"
}
```

### Monitoring Store and Forward
```python
def check_store_forward_status():
    """Monitor store and forward health"""
    quarantined = system.tag.read("[System]Gateway/StoreAndForward/QuarantinedCount").value
    pending = system.tag.read("[System]Gateway/StoreAndForward/PendingCount").value
    
    if quarantined > 0:
        system.util.getLogger("S&F").warn("Quarantined records: %d" % quarantined)
    
    return {
        "pending": pending,
        "quarantined": quarantined,
        "status": "Healthy" if quarantined == 0 else "Issues"
    }
```

## Common Gotchas and Limitations

### Memory Management
- **Tag Limit**: Monitor tag count, especially with UDT instances
- **Client Sessions**: Limited to 2 designer/5 runtime sessions
- **History Storage**: Default 1 week, plan accordingly
- **Script Memory**: Long-running scripts can cause memory issues

### Scripting Limitations
```python
# WRONG - Will fail in Edge
data = system.db.runQuery("SELECT * FROM production")  # No DB access!

# RIGHT - Use tags or MQTT
data = system.tag.readBlocking(["Production/Count", "Production/Rate"])
```

### Gateway Network Quirks
- **Certificate Issues**: Always verify certificates match
- **Firewall Rules**: Port 8060 (default) must be open bidirectionally
- **Connection Limits**: Edge can only connect to one upstream gateway

### Tag Provider Issues
```python
# Check tag provider status
providers = system.tag.getProviders()
for provider in providers:
    config = system.tag.getConfiguration(provider)
    if not config.isEnabled():
        system.util.getLogger("Tags").error("Provider %s is disabled!" % provider)
```

### Performance Considerations
1. **Tag Subscriptions**: Limit to necessary tags only
2. **History Resolution**: Balance between data granularity and storage
3. **Script Frequency**: Avoid timer scripts < 1000ms
4. **Expression Tags**: Can impact performance with complex expressions

### Troubleshooting Tips
```python
# Enable debug logging
logger = system.util.getLogger("EdgeDebug")
logger.setLevel("DEBUG")

# Monitor system performance
def log_system_stats():
    cpu = system.util.getSystemFlags()["cpu.usage"]
    memory = system.util.getSystemFlags()["memory.usage"]
    logger.info("CPU: %.1f%%, Memory: %.1f%%" % (cpu, memory))
    
# Schedule to run every 5 minutes
system.util.invokeScheduled(log_system_stats, 300000)
```

### Edge-Specific Workarounds
1. **Database Operations**: Use MQTT to publish to central system
2. **Reporting**: Generate data locally, process centrally
3. **Alarming**: Limited to local notification, use MQTT for remote
4. **User Management**: Sync from central gateway via Gateway Network

## Best Practices Summary
1. Always plan for offline operation
2. Implement proper error handling in all scripts
3. Use UDTs for consistent data structures
4. Follow UNS naming from the start
5. Monitor Store & Forward queue sizes
6. Test failover scenarios regularly
7. Document all custom scripts thoroughly
8. Keep Edge configuration lightweight