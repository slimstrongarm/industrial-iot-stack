# Mac Claude Post-Compact Task Assignment

## 🎯 Coordination Plan
**Server Claude Focus**: Discord bot for @claude responses  
**Mac Claude Focus**: n8n workflows + Node-RED flows testing  
**Timeline**: Post-auto compact parallel work  

## 📋 Mac Claude Priority Tasks

### 🔥 **High Priority: n8n Workflow Completion**

#### **1. n8n Google Sheets Integration (HT-003)**
- **Status**: Ready - API working, credentials needed
- **Task**: Configure Google Sheets service account in n8n
- **Location**: n8n instance at `http://172.28.214.170:5678`
- **Credentials**: Service account JSON (same as used for automation)
- **Expected Time**: 5-10 minutes
- **Impact**: Unlocks MQTT → Google Sheets logging

#### **2. Test MQTT→Google Sheets Flow (HT-005)**
- **Status**: Ready after HT-003 completion
- **Task**: Activate and test n8n MQTT workflow
- **Test Data**: Use equipment alerts topic
- **Validation**: Verify data appears in "Equipment Alerts" sheet
- **Expected Time**: 10 minutes

#### **3. Complete CT-008 Integration Test**
- **Current Status**: 90% complete
- **Remaining**: End-to-end MQTT → n8n → Google Sheets → Discord flow
- **Test Scenario**: Publish MQTT alert, verify all endpoints receive data
- **Success Criteria**: 100% integration test completion

### ⚡ **Medium Priority: Node-RED Flow Testing**

#### **4. Import Node-RED MQTT Alert Bridge (CT-010)**
- **Status**: Ready for import
- **Location**: Node-RED at `http://172.28.214.170:1880`
- **Task**: Import MQTT alert bridge flow
- **Purpose**: Alternative MQTT routing path
- **Dependencies**: CT-008 completion recommended

#### **5. Import Node-RED n8n Command Bridge (CT-011)**
- **Status**: Ready for import
- **Location**: Same Node-RED instance
- **Task**: Import n8n command bridge flow
- **Purpose**: Node-RED ↔ n8n coordination
- **Dependencies**: CT-010 completion

#### **6. Node-RED Flow Validation**
- **Test**: Both imported flows functional
- **Validate**: MQTT routing working correctly
- **Verify**: No conflicts with existing n8n workflows
- **Document**: Flow performance and reliability

## 🔧 **Technical Details**

### **n8n Instance Access:**
- **URL**: `http://172.28.214.170:5678`
- **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4`
- **Existing Workflows**: 
  - Formbricks→Sheets (ID: n3UFERK5ilPYrLP3)
  - MQTT→WhatsApp (ID: PptMUA3BfrivzhG9)

### **Node-RED Instance Access:**
- **URL**: `http://172.28.214.170:1880`
- **Admin Interface**: Available for flow import
- **MQTT Config**: Should connect to EMQX at `host.docker.internal:1883`

### **MQTT Broker Details:**
- **EMQX**: `172.17.0.4:1883` (from outside Docker)
- **From n8n/Node-RED**: Use `host.docker.internal:1883`
- **Topics**: `equipment/alerts`, `system/status`, `equipment/data`

### **Google Sheets Integration:**
- **Sheet ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **Target Sheets**: "Equipment Alerts", "All Equipment Events"
- **Service Account**: Same JSON used for automation scripts

## 🎯 **Success Criteria**

### **Completion Targets:**
1. **HT-003**: Complete (Google Sheets working in n8n)
2. **HT-005**: Complete (MQTT→Sheets flow tested)
3. **CT-008**: 100% Complete (full integration working)
4. **CT-010**: Complete (Node-RED MQTT bridge active)
5. **CT-011**: Complete (Node-RED n8n bridge active)

### **Validation Tests:**
- ✅ MQTT message → n8n → Google Sheets
- ✅ MQTT message → Node-RED → processing
- ✅ n8n ↔ Node-RED coordination
- ✅ No conflicts between workflows
- ✅ Discord notifications working end-to-end

## 📊 **Expected Outcomes**

### **System Integration:**
- **n8n**: 100% operational with Google Sheets
- **Node-RED**: Active with imported flows
- **MQTT**: Full routing through both systems
- **End-to-End**: Complete Industrial IoT Stack workflow

### **Task Completion:**
- **5 tasks completed** (HT-003, HT-005, CT-008, CT-010, CT-011)
- **Integration testing**: 100% validated
- **System reliability**: Proven stable operation

## 🤝 **Coordination Notes**

### **While Mac Claude Works on n8n/Node-RED:**
**Server Claude will handle:**
- Discord bot development for @claude responses
- GitHub Actions organization key testing
- Discord ↔ Claude integration
- Real-time conversation setup

### **Communication:**
- **Google Sheets**: Live status updates
- **Discord**: Progress notifications via webhook
- **Session summaries**: Document completion status

### **Timeline Estimate:**
- **n8n tasks**: 30-45 minutes
- **Node-RED tasks**: 20-30 minutes
- **Testing & validation**: 15-20 minutes
- **Total**: ~1.5 hours for complete workflow validation

## 🚀 **Post-Completion Benefits**

### **Fully Operational Industrial IoT Stack:**
- MQTT → n8n → Google Sheets → Discord (complete pipeline)
- Node-RED alternative routing (redundancy)
- Real-time monitoring and alerting
- Cross-system coordination

### **Ready for Production:**
- All integration paths validated
- Multiple workflow options
- Comprehensive testing completed
- Documentation current

---

**Created**: Pre-auto compact coordination  
**Priority**: High - these tasks unlock the final 10% of system integration  
**Dependencies**: Server Claude completing Discord bot in parallel  
**Success**: 100% Industrial IoT Stack operational capability