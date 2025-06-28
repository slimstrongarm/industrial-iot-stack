# Node-RED Scalability Analysis

## Memory Leak Root Causes (Found & Fixed)

### 1. **Undefined Variable Access**
- Function nodes accessing properties on undefined objects
- Causing repeated TypeError exceptions (5-10 per second)
- Each error creates stack trace objects → memory accumulation

### 2. **MQTT Broker Reconnection Loop**
- Broker disconnecting/reconnecting every 5-6 seconds
- Creating new connection objects without cleanup
- Fixed with longer keepalive and reconnect delays

### 3. **Unthrottled Error Logging**
- Errors logged without rate limiting
- Unknown protocol warnings firing continuously
- Fixed with rate-limited error handling

## Production Scalability Assessment

### ✅ Viable for Production With Fixes
- Memory leaks are fixable (not architectural)
- 8GB memory sufficient for brewery operations
- Node-RED proven in industrial environments

### ⚠️ Considerations for Scale
1. **Message Volume**: ~1000 msgs/sec sustainable
2. **Tag Count**: 10,000+ tags manageable
3. **Flow Complexity**: Current 19 flows OK, monitor at 50+

### 🔄 Alternative Architectures

#### Option 1: Pure Node-RED (Current)
- **Pros**: Customer familiar, quick deployment
- **Cons**: Single point of failure, JavaScript limitations
- **Best for**: Single site, <50k tags

#### Option 2: Hybrid (Node-RED + n8n)
- **Node-RED**: Edge data collection, protocol conversion
- **n8n**: Business logic, integrations, workflows
- **Pros**: Separation of concerns, better scaling
- **Best for**: Multi-site, complex workflows

#### Option 3: Ignition-Centric
- **Ignition**: Primary SCADA + scripting
- **Node-RED**: Protocol adapters only
- **Pros**: Industrial-grade, better performance
- **Best for**: Mission-critical, high-volume

## Recommendations

### Immediate (POC Phase)
1. Deploy fixed Node-RED flows
2. Monitor memory usage closely
3. Implement health checks

### Short-term (Production)
1. Add Redis for state management
2. Implement flow-level error boundaries
3. Create automated recovery scripts

### Long-term (Scale)
1. Evaluate n8n for workflow orchestration
2. Consider Kubernetes deployment
3. Plan for horizontal scaling

## Client-Specific Notes
- Owner has existing Node-RED → compatibility important
- Start with fixes, migrate gradually if needed
- Document everything for handoff

---
*Memory fixes implemented: 2025-05-31*