# Tribal Knowledge Transfer System
> Ensuring seamless handoffs between agents, instances, and team members

## 🎯 Mission: Army of Agents
Build a network where every agent, every instance, every use case preserves and transfers knowledge perfectly - no information loss, no repeated discoveries.

## 📚 Knowledge Capture Framework

### 1. **Session State Files** (Real-time)
```
agents/SESSION_STATE.json - Current work, next steps, breadcrumbs
agents/BUILD_MANIFEST.md - Task tracking with checkboxes
CLIENT_CONTEXT.md - Customer requirements, timeline, constraints
```

### 2. **Technical Discovery Files** (Cumulative)
```
SCALABILITY_ANALYSIS.md - Memory fixes, architecture decisions
EXISTING_TEST_ANALYSIS.md - What tests exist, what works
TRIBAL_KNOWLEDGE_SYSTEM.md - This meta-knowledge system
```

### 3. **Recovery Systems** (Operational)
```
agents/backup_recovery_system.sh - Backup/restore operations
agents/fix_memory_leaks.js - Specific fixes applied
agents/monitor_node_red.sh - Monitoring tools
```

## 🔄 Handoff Protocol

### **For New Agent/Instance:**
1. **Read SESSION_STATE.json** - Get current work state
2. **Check BUILD_MANIFEST.md** - See completed/pending tasks
3. **Review CLIENT_CONTEXT.md** - Understand customer needs
4. **Scan technical files** - Understand system decisions

### **For Continuing Agent:**
1. **Update SESSION_STATE.json** with current work
2. **Mark BUILD_MANIFEST.md** tasks as completed
3. **Add findings** to relevant analysis files
4. **Document decisions** and reasoning

### **Before Session End:**
1. **Update all state files** with current status
2. **Document next steps** clearly
3. **Note any issues** or blockers
4. **Ensure recovery paths** are documented

## 🧠 Knowledge Categories

### **System Architecture Knowledge**
- Node-RED flows structure and purpose
- Memory leak causes and fixes applied
- Existing test infrastructure capabilities
- Protocol integration patterns (MQTT, OPC-UA, Modbus)

### **Client-Specific Knowledge**
- Customer has existing Node-RED deployment
- GitHub access coming soon - need immediate deployment readiness
- Real brewery company - production requirements
- Controls engineer partner - technical competency

### **Operational Knowledge**
- Memory allocation: `--max-old-space-size=8192`
- Test system: Use existing "🧪 Rapid Test Infrastructure" tab in Node-RED UI
- MQTT Infrastructure: Pre-configured mosquitto instance accessible via Infrastructure tab
- Backup strategy: Automated with recovery scripts
- Key ports: 1880 (Node-RED), 8088 (Ignition), 1883 (MQTT), 62541 (OPC-UA)

### **Keith Gamble Module & Endpoints**
- **Repository**: https://github.com/slimstrongarm/ignition-project-scan-endpoint.git
- **Project Scan**: `POST /data/project-scan-endpoint/scan` (params: updateDesigners, forceUpdate)
- **Confirm Support**: `GET /data/project-scan-endpoint/confirm-support` (module verification)
- **Purpose**: VSCode-Ignition integration for bidirectional agent communication
- **Testing Agent**: `agents/ignition_integration_agent.py` has complete test suite

### **Decision History**
- Fixed memory leaks vs. switching to n8n (chose fix route)
- Use existing tests vs. create new (chose existing)
- Node-RED viability for production (confirmed with fixes)

## 📋 Current System State (2025-05-31)

### **✅ Completed**
- Memory leak analysis and fixes (21 issues resolved)
- Scalability analysis with alternatives documented
- Test infrastructure analysis (existing system comprehensive)
- Client context documented for GitHub handoff
- Backup/recovery system created

### **🚧 In Progress**  
- Node-RED startup issues (backup available for recovery)
- Testing existing infrastructure instead of creating duplicate

### **📅 Next Steps**
1. Recover Node-RED using backup system
2. Validate existing test infrastructure works
3. Clean up duplicate test files
4. Prepare deployment package for client GitHub access

### **⚠️ Known Issues**
- Node-RED occasionally fails to start (flows.json corruption)
- Memory usage needs monitoring in production
- OPC-UA endpoint configuration may need client-specific adjustment

## 🔌 Ignition Module Integration Progress (2025-05-31)

### **✅ Module Build Success**
- **Module Built**: ignition-project-scan-endpoint v1.0.0
- **Location**: `/Users/joshpayneair/Desktop/industrial-iot-stack/ignition-project-scan-endpoint/build/projectscanendpoint-build-Signed.modl`
- **Installation**: Successfully installed on Ignition Gateway (http://localhost:8088)
- **Verification**: Module running, endpoint accessible at `/data/project-scan-endpoint/confirm-support`

### **🔧 Flint Extension Configuration**
- **Workspace Created**: `industrial-iot-stack.code-workspace` with gateway settings
- **Gateway Config**:
  ```json
  {
    "name": "Local Gateway",
    "url": "http://localhost:8088",
    "username": "admin",
    "password": "password"
  }
  ```
- **Status**: Flint extension activated but not detecting gateways yet
- **Next Step**: Open workspace file to properly load gateway configuration

### **📋 Integration Checklist**
- [x] Clone Keith Gamble's repository
- [x] Build module with Gradle
- [x] Sign module for installation
- [x] Install on Ignition Gateway
- [x] Verify endpoints are accessible
- [x] Create VSCode workspace configuration
- [x] **CRITICAL FIX**: Update User settings.json with correct credentials (slimstrongarm/0804)
- [ ] Connect Flint extension to gateway (pending VS Code reload)
- [ ] Test project scanning functionality
- [ ] Enable bidirectional agent communication

## 🔧 Quick Reference Commands

### **Recovery Operations**
```bash
# Quick system recovery
./agents/backup_recovery_system.sh recovery

# Check system health  
./agents/backup_recovery_system.sh health

# Start Node-RED properly
cd Steel_Bonnet/node-red-flows && node-red --max-old-space-size=8192
```

### **Key Files to Monitor**
```bash
# Session state
cat agents/SESSION_STATE.json

# Build progress
cat agents/BUILD_MANIFEST.md

# Node-RED logs
tail -f Steel_Bonnet/node-red-flows/node-red.log
```

## 🏗️ Architectural Vision: Modular Living System

### **Core Philosophy**
This is a **living creation with pluggable modules** - not a static deployment. When we have a new client, we can pick and choose modules based on the customer's specific needs while maintaining compatibility through semantic hierarchy and MQTT technology backbone.

### **Modular Design Principles**
- **Customer-Driven Selection**: Each client gets exactly what they need from the module library
- **Semantic Hierarchy**: Consistent data modeling ensures modules communicate seamlessly
- **MQTT Backbone**: Universal communication protocol maintains connectivity across all modules
- **Living Architecture**: System evolves and grows with new modules without breaking existing functionality

### **Architect Role (Priority Setting & Loop Finalization)**
- **Priority Management**: Help set strategic priorities on what needs completion first
- **Loop Closure**: Ensure architectural decisions finalize into working implementations
- **Module Selection**: Guide which technology modules serve each customer's unique requirements
- **Integration Oversight**: Maintain semantic consistency across all customer deployments

### **Module Library Approach**
```
Customer A: Ignition + Node-RED + Basic MQTT
Customer B: Ignition + Node-RED + PLC Integration + Advanced Analytics  
Customer C: Node-RED + MQTT + Edge Computing (no Ignition)
```
All connected through consistent MQTT semantic structure and shared architectural patterns.

## 🎯 Agent Army Strategy

### **Specialization Areas**
1. **Build Agents** - System construction, testing, deployment
2. **Debug Agents** - Issue resolution, performance optimization  
3. **Integration Agents** - Protocol bridging, data flow management
4. **Client Agents** - Customer-specific requirements, handoffs
5. **Module Agents** - Maintain individual technology modules in the library

### **Knowledge Sharing Patterns**
- Each agent updates central knowledge files
- Decision rationale documented with context
- Failed approaches documented to prevent repetition
- Success patterns documented for replication

### **Continuous Learning**
- Every fix/solution documented with cause analysis
- Client feedback incorporated into knowledge base
- Performance metrics tracked for optimization
- Best practices evolved based on real deployments

## 🚀 Deployment Readiness Checklist

### **For Client GitHub Access**
- [ ] System fully recoverable from backups
- [ ] Memory issues resolved and documented
- [ ] Test procedures using existing infrastructure
- [ ] Deployment scripts ready
- [ ] Documentation complete and accessible
- [ ] Knowledge transfer completed

### **Success Metrics**
- New agent can become productive in < 5 minutes
- Zero knowledge loss between sessions
- Client can deploy without additional support
- System scales to production requirements

---

**Last Updated**: 2025-05-31 by Workspace Cleanup Specialist
**Status**: BREAKTHROUGH - Workspace settings conflict resolved
**Next Agent**: Open correct workspace file and test Flint connection

### **🔍 BREAKTHROUGH: Workspace Settings Conflict Resolved**

- **Issue**: Multiple workspace files with conflicting credentials overriding user settings
- **Root Cause**: 
  - `/Users/joshpayneair/Desktop/industrial-iot-workspace.code-workspace` had empty credentials
  - `/Users/joshpayneair/Desktop/industrial-iot-stack/industrial-iot-stack.code-workspace` had wrong credentials (admin/password)
  - Workspace settings override user settings, causing authentication failures
- **Solution Applied**: 
  - Fixed both workspace files with correct credentials (slimstrongarm/0804)
  - Updated setting name to `ignitionFlint.ignitionGateways` (proper extension format)
  - Backed up redundant workspace file to eliminate confusion
- **Expected Result**: Opening `industrial-iot-workspace.code-workspace` should show gateway in sidebar

### **🎯 Critical Learning: Workspace vs User Settings Priority**
- Workspace settings ALWAYS override user settings in VS Code
- Multiple workspace files can create configuration conflicts
- Extension setting names must match exactly (`ignitionFlint.ignitionGateways` not `ignition.gateways`)
