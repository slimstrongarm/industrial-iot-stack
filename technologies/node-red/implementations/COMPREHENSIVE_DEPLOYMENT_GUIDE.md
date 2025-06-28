# Comprehensive Deployment Guide - Steel Bonnet Node-RED System

## Overview
This guide provides a complete deployment strategy for the Steel Bonnet Node-RED flows, incorporating the standardized debug infrastructure pattern across all modules. The system is designed to support three deployment modes: Testing, Development, and Production.

## Debug Infrastructure Pattern

### Core Components
Every flow now includes:
1. **Debug Configuration Node** - Initializes debug settings from global config
2. **Toggle-able Debug Nodes** - Strategic placement for troubleshooting
3. **Simulation Capabilities** - Test without external dependencies
4. **Debug Control Panel** - UI for real-time control
5. **Statistics Tracking** - Performance and error monitoring

### Global Debug Configuration
```javascript
{
    enabled: true,              // Master debug switch
    mode: 'testing',           // testing, development, production
    showDataFormats: true,     // Display data type information
    validateData: false,       // Enable data validation
    opcEnabled: false,         // OPC server availability
    simulationEnabled: true    // Use simulated data
}
```

## Deployment Modes

### 1. Testing Mode (Default)
- **Purpose**: Initial deployment and functional testing
- **Characteristics**:
  - All debug features enabled
  - Simulation data active
  - No external dependencies required
  - Verbose logging
  - Shorter intervals for faster feedback

### 2. Development Mode
- **Purpose**: Integration testing with real systems
- **Characteristics**:
  - Debug features available but selective
  - Can toggle between simulation and real data
  - Enhanced error reporting
  - Data validation enabled
  - Normal operational intervals

### 3. Production Mode
- **Purpose**: Live operational deployment
- **Characteristics**:
  - Minimal logging
  - No simulation data
  - Optimized performance
  - Error logging only
  - Production intervals and thresholds

## Deployment Steps

### Step 1: Initial Setup
1. Import all flows into Node-RED
2. Verify node dependencies are installed:
   - node-red-dashboard
   - node-red-contrib-modbus
   - node-red-contrib-opcua (if using OPC)

### Step 2: Configure Global Settings
1. Open any flow and locate the Debug Configuration node
2. Set the appropriate mode in the initialization:
```javascript
const globalDebug = global.get('debugConfig') || {
    enabled: true,
    mode: 'testing',  // Change to 'development' or 'production'
    // ... other settings
};
```

### Step 3: Flow-by-Flow Deployment

#### Equipment Registration Flow
1. **Testing**: Uses simulated form submissions
2. **Development**: Connect to real database/storage
3. **Production**: Disable debug UI elements

#### Monitoring Dashboard Flow
1. **Testing**: Shows demo equipment with simulated data
2. **Development**: Connects to registered equipment
3. **Production**: Full equipment monitoring

#### MQTT Protocol Module
1. **Testing**: Simulated MQTT broker with test topics
2. **Development**: Configure real MQTT broker settings
3. **Production**: Secure broker with authentication

#### Modbus Protocol Module
1. **Testing**: Simulated PLCs and devices
2. **Development**: Configure real Modbus devices
3. **Production**: Full device polling

#### Event Processing Core
1. **Testing**: High event generation rate
2. **Development**: Normal thresholds and intervals
3. **Production**: Optimized buffer sizes

### Step 4: Debug Control Usage

#### Enable/Disable Debug Features
1. Access the dashboard for each flow
2. Use Debug Control Panel to:
   - Toggle debug mode on/off
   - Enable/disable simulation
   - View real-time statistics
   - Configure debug options

#### Monitor Flow Performance
1. Check statistics regularly:
   - Message counts
   - Error rates
   - Processing times
   - Buffer utilization

#### Troubleshooting
1. Enable specific debug nodes:
   - Right-click debug node → Enable
   - View output in debug sidebar
   - Disable when issue resolved

### Step 5: Production Deployment

#### Pre-Production Checklist
- [ ] Set all flows to 'production' mode
- [ ] Disable unnecessary debug nodes
- [ ] Configure real external connections
- [ ] Set production thresholds and intervals
- [ ] Test failover scenarios
- [ ] Document configuration settings

#### Production Configuration
1. Update global debug config:
```javascript
{
    enabled: false,
    mode: 'production',
    showDataFormats: false,
    validateData: true,
    opcEnabled: true,
    simulationEnabled: false
}
```

2. Configure external systems:
   - MQTT broker credentials
   - Modbus device IPs
   - OPC server endpoints
   - Database connections

3. Set production intervals:
   - MQTT discovery: 60 seconds
   - Modbus polling: 10 seconds
   - Event buffer flush: 5 seconds
   - Pattern analysis: 5 minutes

## Best Practices

### 1. Mode Transitions
- Always test in 'testing' mode first
- Gradually transition through 'development'
- Thoroughly validate before 'production'

### 2. Debug Management
- Keep debug infrastructure in production
- Disable output but maintain capability
- Can re-enable for troubleshooting

### 3. Performance Optimization
- Monitor buffer sizes in production
- Adjust intervals based on load
- Use event suppression wisely

### 4. Error Handling
- Check error statistics regularly
- Set up alerts for critical errors
- Maintain error logs for analysis

## Common Issues and Solutions

### Issue: No data appearing in dashboards
1. Check simulation is enabled in testing mode
2. Verify flow connections (link nodes)
3. Enable relevant debug nodes
4. Check browser console for errors

### Issue: High memory usage
1. Reduce buffer sizes
2. Increase flush intervals
3. Enable event suppression
4. Check for memory leaks in function nodes

### Issue: External connections failing
1. Verify network connectivity
2. Check credentials and endpoints
3. Enable connection debug logging
4. Test with simulation first

### Issue: Events not correlating
1. Check correlation window settings
2. Verify event timestamps
3. Enable correlation debug output
4. Review correlation rules

## Maintenance Guidelines

### Regular Tasks
1. **Daily**: Check error logs and statistics
2. **Weekly**: Review performance metrics
3. **Monthly**: Analyze event patterns
4. **Quarterly**: Update thresholds and rules

### Updates and Changes
1. Test all changes in testing mode
2. Use version control for flows
3. Document configuration changes
4. Plan maintenance windows

## Security Considerations

### Production Security
1. Disable debug UI in production
2. Secure MQTT with TLS
3. Use authentication for all protocols
4. Limit dashboard access
5. Regular security audits

### Data Protection
1. No sensitive data in debug logs
2. Sanitize error messages
3. Secure credential storage
4. Encrypted communications

## Conclusion
This standardized debug infrastructure provides a robust framework for deploying and maintaining the Steel Bonnet Node-RED system. The pattern ensures consistent behavior across all flows while supporting the full development lifecycle from initial testing to production deployment.

For additional support or questions, refer to the individual flow guides:
- MONITORING_DASHBOARD_V3_GUIDE.md
- MQTT_PROTOCOL_MODULE_GUIDE.md
- (Additional guides for other flows)