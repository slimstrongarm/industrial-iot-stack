# Node-RED Technical Reference

## Table of Contents
1. [Flow-Based Programming Concepts](#flow-based-programming-concepts)
2. [Core Nodes and Their Usage](#core-nodes-and-their-usage)
3. [Context Storage](#context-storage)
4. [Custom Node Development](#custom-node-development)
5. [MQTT Integration Patterns](#mqtt-integration-patterns)
6. [OPC-UA Client Configuration](#opc-ua-client-configuration)
7. [Error Handling and Debugging](#error-handling-and-debugging)
8. [Performance Optimization for Industrial Use](#performance-optimization-for-industrial-use)

## Flow-Based Programming Concepts

### Core Principles
- **Visual Programming**: Flows are created by connecting nodes through wires
- **Event-Driven**: Data flows are triggered by events (messages)
- **Asynchronous**: Non-blocking message passing between nodes
- **Modular**: Each node performs a specific function

### Message Structure
```javascript
{
    payload: any,      // Primary data
    topic: string,     // Message topic/identifier
    _msgid: string,    // Unique message ID
    // Custom properties as needed
}
```

### Flow Execution Model
1. Messages flow from left to right
2. Each node processes messages independently
3. Nodes can emit 0, 1, or multiple messages
4. Parallel branches execute concurrently

## Core Nodes and Their Usage

### Input Nodes
#### Inject Node
- Triggers flows manually or on schedule
- Supports cron expressions for complex schedules
- Can inject various data types (string, number, boolean, JSON, buffer)

```javascript
// Example: Inject every 5 minutes
{
    repeat: "300",
    crontab: "",
    once: false,
    onceDelay: 0.1
}
```

#### HTTP In Node
- Creates HTTP endpoints (GET, POST, PUT, DELETE)
- Supports URL parameters and query strings
- Integrates with response node for RESTful APIs

#### MQTT In Node
- Subscribes to MQTT topics
- Supports wildcards (+, #)
- QoS levels 0, 1, 2

### Function Nodes
#### Function Node
- Execute custom JavaScript code
- Access to Node.js globals and npm modules (when configured)
- Multiple outputs for conditional routing

```javascript
// Example: Data transformation
if (msg.payload.temperature > 75) {
    return [msg, null];  // Output 1
} else {
    return [null, msg];  // Output 2
}
```

#### Switch Node
- Route messages based on property values
- Supports multiple conditions and outputs
- Comparison operators: ==, !=, <, >, <=, >=, contains, regex

#### Change Node
- Set, change, delete, or move message properties
- Support for JSONata expressions
- Can work with flow/global context

### Output Nodes
#### Debug Node
- Display messages in debug sidebar
- Can output complete message or specific properties
- Configurable output to console or status

#### HTTP Response Node
- Send responses to HTTP requests
- Set status codes and headers
- Return JSON, HTML, or other content types

#### File Node
- Write data to files
- Append or overwrite modes
- Automatic directory creation

## Context Storage

### Context Levels
1. **Node Context**: Data specific to a single node instance
2. **Flow Context**: Shared across all nodes in a flow
3. **Global Context**: Shared across all flows

### Usage in Function Nodes
```javascript
// Node context
context.set('counter', 0);
let count = context.get('counter') || 0;

// Flow context
flow.set('deviceStatus', 'online');
let status = flow.get('deviceStatus');

// Global context
global.set('config', {
    mqttBroker: 'tcp://localhost:1883',
    opcEndpoint: 'opc.tcp://localhost:4840'
});
let config = global.get('config');

// Async operations with callbacks
context.get('data', 'memory', function(err, value) {
    if (!err) {
        // Use value
    }
});
```

### Persistent Storage
Configure in settings.js:
```javascript
contextStorage: {
    default: {
        module: "memory"
    },
    file: {
        module: "localfilesystem",
        config: {
            dir: "/data/node-red/context",
            flushInterval: 30
        }
    }
}
```

## Custom Node Development

### Node Structure
```javascript
module.exports = function(RED) {
    function CustomNode(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        
        // Node initialization
        node.name = config.name;
        
        // Handle incoming messages
        node.on('input', function(msg, send, done) {
            // Process message
            msg.payload = processData(msg.payload);
            
            // Send message (Node-RED 1.0+)
            send = send || function() { node.send.apply(node,arguments) }
            send(msg);
            
            // Signal completion
            if (done) {
                done();
            }
        });
        
        // Cleanup on deploy/restart
        node.on('close', function(done) {
            // Cleanup operations
            done();
        });
    }
    
    RED.nodes.registerType("custom-node", CustomNode);
}
```

### Package Structure
```
custom-node/
├── package.json
├── custom-node.js
├── custom-node.html
└── icons/
    └── custom-node.png
```

### HTML Definition
```html
<script type="text/javascript">
    RED.nodes.registerType('custom-node', {
        category: 'function',
        color: '#a6bbcf',
        defaults: {
            name: {value: ""},
            property: {value: "", required: true}
        },
        inputs: 1,
        outputs: 1,
        icon: "custom-node.png",
        label: function() {
            return this.name || "custom-node";
        }
    });
</script>

<script type="text/html" data-template-name="custom-node">
    <div class="form-row">
        <label for="node-input-name"><i class="fa fa-tag"></i> Name</label>
        <input type="text" id="node-input-name" placeholder="Name">
    </div>
</script>
```

## MQTT Integration Patterns

### Connection Configuration
```javascript
// MQTT Broker Config Node
{
    broker: "localhost",
    port: 1883,
    clientid: "node-red-" + Date.now(),
    usetls: false,
    protocolVersion: 4,
    keepalive: 60,
    cleansession: true
}
```

### Publishing Patterns
```javascript
// Structured topic hierarchy
msg.topic = `plant/area/line/machine/sensor`;
msg.payload = {
    timestamp: Date.now(),
    value: sensorValue,
    unit: "°C",
    quality: "good"
};
msg.qos = 1;
msg.retain = true;
return msg;
```

### Subscription Patterns
```javascript
// Multi-level wildcards
"plant/+/line1/+/temperature"  // All temperature sensors on line1
"plant/area1/#"                 // Everything in area1

// Dynamic subscriptions
msg.action = "subscribe";
msg.topic = "plant/area2/+/status";
return msg;
```

### MQTT Best Practices
1. Use QoS 1 for critical data
2. Implement Last Will and Testament (LWT)
3. Use retained messages for configuration
4. Implement reconnection logic
5. Monitor connection status

## OPC-UA Client Configuration

### Basic Connection
```javascript
// OPC-UA Client Config
{
    endpoint: "opc.tcp://localhost:4840",
    securityPolicy: "None",
    securityMode: "None",
    certificateFile: "",
    privateKeyFile: "",
    defaultSecureTokenLifetime: 60000
}
```

### Reading Data
```javascript
// Browse for available nodes
msg.action = "browse";
msg.nodeid = "ns=2;s=Device1";

// Read single value
msg.action = "read";
msg.nodeid = "ns=2;s=Device1.Temperature";

// Read multiple values
msg.action = "readmultiple";
msg.nodesToRead = [
    {nodeId: "ns=2;s=Device1.Temperature"},
    {nodeId: "ns=2;s=Device1.Pressure"},
    {nodeId: "ns=2;s=Device1.Status"}
];
```

### Writing Data
```javascript
// Write single value
msg.action = "write";
msg.nodeid = "ns=2;s=Device1.SetPoint";
msg.payload = {
    value: 75.5,
    dataType: "Double"
};

// Write with specific data type
msg.payload = {
    value: true,
    dataType: "Boolean",
    arrayType: "Scalar"
};
```

### Subscriptions
```javascript
// Subscribe to value changes
msg.action = "subscribe";
msg.interval = 1000;  // Sampling interval in ms
msg.nodeid = "ns=2;s=Device1.Temperature";

// Monitor multiple items
msg.action = "monitor";
msg.monitoredItems = [
    {nodeId: "ns=2;s=Device1.Temperature", interval: 1000},
    {nodeId: "ns=2;s=Device1.Pressure", interval: 5000}
];
```

## Error Handling and Debugging

### Try-Catch in Function Nodes
```javascript
try {
    // Risky operation
    let data = JSON.parse(msg.payload);
    msg.payload = processData(data);
    return msg;
} catch (error) {
    node.error("Failed to process data: " + error.message, msg);
    // Optionally send to error output
    return [null, {payload: error.message, _error: error}];
}
```

### Catch Node Usage
```javascript
// Catch all errors in flow
{
    scope: ["flowId"],
    uncaught: false
}

// Catch uncaught errors only
{
    scope: null,  // All flows
    uncaught: true
}
```

### Status Node Monitoring
```javascript
// Monitor node status changes
msg.status = {
    fill: "red",
    shape: "ring",
    text: "disconnected"
};

// In function node
node.status({
    fill: "green",
    shape: "dot",
    text: "connected"
});
```

### Debugging Techniques
1. **Strategic Debug Nodes**: Place at key points in flow
2. **Node Status**: Use status to show current state
3. **Context Inspection**: Use context viewer in sidebar
4. **Console Logging**: For detailed debugging
5. **Flow Testing**: Use inject nodes with test data

### Performance Metrics
```javascript
// Measure processing time
let startTime = Date.now();

// Process data
let result = heavyComputation(msg.payload);

let duration = Date.now() - startTime;
node.metric("processing_time", duration);

// Log if threshold exceeded
if (duration > 1000) {
    node.warn(`Processing took ${duration}ms`);
}
```

## Performance Optimization for Industrial Use

### Message Queue Management
```javascript
// Implement rate limiting
let queue = context.get('queue') || [];
queue.push(msg);

if (queue.length >= 100) {
    // Process batch
    let batch = queue.splice(0, 100);
    processBatch(batch);
}

context.set('queue', queue);
```

### Memory Management
1. **Clear References**: Remove large objects when done
2. **Stream Processing**: Use streams for large files
3. **Context Cleanup**: Periodically clean context storage
4. **Message Cloning**: Avoid unnecessary cloning

```javascript
// Efficient message passing
msg.payload = largeData;
send(msg);
msg.payload = null;  // Clear reference
```

### CPU Optimization
```javascript
// Use setImmediate for long operations
function processLargeDataset(data, callback) {
    let index = 0;
    
    function processNext() {
        let chunk = data.slice(index, index + 1000);
        // Process chunk
        
        index += 1000;
        if (index < data.length) {
            setImmediate(processNext);
        } else {
            callback();
        }
    }
    
    processNext();
}
```

### Flow Design Patterns
1. **Parallel Processing**: Split large tasks across multiple paths
2. **Caching**: Use context storage for frequently accessed data
3. **Debouncing**: Reduce message frequency for chatty sensors
4. **Aggregation**: Combine multiple messages before processing

### Industrial-Specific Optimizations
```javascript
// Store-and-forward for network outages
let buffer = flow.get('buffer') || [];

if (isNetworkAvailable()) {
    // Send buffered data
    buffer.forEach(data => sendData(data));
    flow.set('buffer', []);
    
    // Send current data
    sendData(msg.payload);
} else {
    // Buffer data
    buffer.push({
        timestamp: Date.now(),
        payload: msg.payload
    });
    
    // Limit buffer size
    if (buffer.length > 10000) {
        buffer = buffer.slice(-10000);
    }
    
    flow.set('buffer', buffer);
}
```

### Resource Monitoring
```javascript
// Monitor Node-RED process
const os = require('os');

global.set('systemMetrics', {
    cpuUsage: process.cpuUsage(),
    memoryUsage: process.memoryUsage(),
    uptime: process.uptime(),
    loadAverage: os.loadavg(),
    freeMemory: os.freemem(),
    totalMemory: os.totalmem()
});

// Alert on high memory usage
if (process.memoryUsage().heapUsed > 500 * 1024 * 1024) {
    node.error("High memory usage detected");
}
```

### Best Practices Summary
1. **Minimize Message Size**: Only pass necessary data
2. **Avoid Blocking Operations**: Use async patterns
3. **Implement Circuit Breakers**: Prevent cascade failures
4. **Use Connection Pooling**: For database and protocol connections
5. **Regular Maintenance**: Clean logs, restart periodically
6. **Monitor Performance**: Track metrics and set alerts
7. **Test at Scale**: Simulate production loads
8. **Document Flows**: Maintain clear documentation