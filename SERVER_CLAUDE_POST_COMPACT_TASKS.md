# Server Claude Post-Compact Task Assignment

## 🎯 Mission: Discord Bot + @Claude Response System
**Primary Goal**: Enable real-time @claude mentions in Discord with instant responses  
**Timeline**: ~1 hour to working prototype  
**Impact**: Turn Discord into live Claude interface  

## 📊 Current System Status (Pre-Compact)

### ✅ **What's Already Working:**
- **Discord webhooks**: Fully operational, tested, sending notifications
- **n8n API**: 75% endpoint success, fully accessible
- **MQTT broker (EMQX)**: Running and tested
- **Google Sheets API**: Operational, all tracking sheets current
- **GitHub Actions**: Infrastructure prepared, org key being tested
- **System integration**: 90%+ complete

### 🔄 **What's In Progress:**
- **CT-008**: Integration Test (90% complete, Mac Claude finishing)
- **GitHub Actions Claude**: Organization key testing
- **n8n workflows**: Mac Claude handling Google Sheets integration

### 📋 **Key Stats:**
- **Claude Tasks**: 23/37 completed (62.2% success rate)
- **Human Tasks**: HT-001 completed, HT-003 assigned to Mac Claude
- **System Status**: Production-ready, final integrations pending

## 🎯 **Your Primary Mission: Discord Bot Development**

### **Phase 1: Discord Bot Setup (20 min)**

#### **1. Create Discord Application & Bot**
- Go to https://discord.gg/developers/applications
- Create new application: "Industrial IoT Claude Bot"
- Bot section → Create Bot
- Copy bot token (save securely)
- Bot permissions: Send Messages, Read Message History, Use Slash Commands

#### **2. Install Bot to Server**
- OAuth2 → URL Generator
- Scopes: bot, applications.commands
- Bot permissions: Send Messages, Read Message History, Embed Links
- Install to Industrial IoT Discord server

#### **3. Test Bot Access**
- Verify bot appears in server
- Test basic connectivity
- Confirm permissions working

### **Phase 2: Bot Development (30 min)**

#### **Create Discord Bot Script**
```python
# Location: scripts/discord_claude_bot.py
# Purpose: Monitor @claude mentions, trigger responses
# Integration: Use existing webhook for responses
```

#### **Key Features:**
- **@claude mention detection**: Monitor all channels
- **Message parsing**: Extract user question/request
- **Response generation**: Connect to Claude API or session
- **Response delivery**: Use existing Discord webhook
- **Context awareness**: Industrial IoT Stack knowledge

#### **Integration Points:**
- **Existing webhook**: `https://discord.com/api/webhooks/1380061953883373660/...`
- **Claude API**: Use organization key or session key approach
- **System context**: Reference EMQX, n8n, Node-RED status

### **Phase 3: Testing & Deployment (10 min)**

#### **Test Scenarios:**
1. `@claude hello` → Basic response test
2. `@claude what's the MQTT broker status?` → System query
3. `@claude help with n8n workflow` → Technical assistance
4. `@claude check equipment alerts` → Integration query

#### **Validation:**
- Bot responds to mentions ✅
- Responses are contextually relevant ✅
- Integration with existing systems ✅
- No conflicts with webhooks ✅

## 🔧 **Technical Resources Available**

### **Critical Configuration:**
- **Discord Webhook**: Already working, tested
- **n8n API**: `http://172.28.214.170:5678/api/v1/`
- **n8n API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (in session state)
- **Google Sheets ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **EMQX MQTT**: `172.17.0.4:1883` (host.docker.internal from containers)

### **Existing Integration Scripts:**
- `scripts/discord_webhook_integration.py` - Working webhook system
- `scripts/claude_max_oauth_setup.py` - Authentication guidance
- `scripts/github_actions_claude_runner.py` - Claude API examples
- `discord_webhook_config.json` - Webhook configuration

### **Documentation:**
- `STACK_CONFIG.md` - Complete system configuration
- `CLAUDE_MAX_SESSION_KEY_GUIDE.md` - OAuth setup instructions
- `GITHUB_ACTIONS_CLAUDE_INTEGRATION.md` - API integration examples
- `SERVER_CLAUDE_SESSION_STATE.md` - Complete session context

## 🤝 **Coordination with Mac Claude**

### **While You Build Discord Bot:**
**Mac Claude is handling:**
- HT-003: Configure Google Sheets in n8n
- HT-005: Test MQTT→Google Sheets flow  
- CT-008: Complete integration test (90% → 100%)
- CT-010/011: Import and test Node-RED flows

### **Communication:**
- **Google Sheets**: Live status updates in tracking tabs
- **Discord**: Progress notifications via existing webhook
- **Documentation**: Update session summaries

### **Timeline Sync:**
- **Your work**: ~1 hour (Discord bot)
- **Mac Claude work**: ~1.5 hours (workflow completion)
- **Coordination**: Regular status updates via Discord

## 🎯 **Success Criteria**

### **Primary Goal Achievement:**
```
User types: "@claude what's the reactor temperature?"
Bot responds: "Reactor 3 temperature is 78°C, within normal range. 
Last alert was 2 hours ago. MQTT broker healthy, 
n8n workflows processing normally."
```

### **Technical Validation:**
- ✅ Bot responds to @claude mentions
- ✅ Responses include Industrial IoT context
- ✅ Integration with existing webhook system
- ✅ No conflicts with current notifications
- ✅ Real-time conversation capability

### **Integration Success:**
- ✅ Discord becomes live Claude interface
- ✅ Industrial IoT monitoring enhanced
- ✅ Real-time system interaction
- ✅ User's dream feature implemented

## 📊 **Expected Outcomes**

### **Immediate Benefits:**
- **Live Discord ↔ Claude chat**: Your original dream feature!
- **Enhanced monitoring**: Ask questions about system status
- **Real-time troubleshooting**: Instant assistance with alerts
- **Team collaboration**: Share Claude interactions in Discord

### **System Integration:**
- **Discord bot** + **existing webhook system** = full two-way communication
- **Industrial IoT awareness** in all responses
- **Context-aware assistance** for MQTT, n8n, Node-RED
- **Seamless integration** with current infrastructure

## 🚀 **Quick Start Checklist**

### **Immediate Actions (First 10 min):**
1. ✅ Read `SERVER_CLAUDE_SESSION_STATE.md` for full context
2. ✅ Review `STACK_CONFIG.md` for system details
3. ✅ Check Google Sheets "Server Claude Session Summary" tab
4. ✅ Test existing Discord webhook (send test message)
5. ✅ Verify n8n API access with provided credentials

### **Development Phase (Next 50 min):**
1. 🔧 Create Discord application and bot
2. 🔧 Install bot to server with permissions
3. 🔧 Develop `discord_claude_bot.py`
4. 🔧 Integrate with existing webhook system
5. 🔧 Test @claude mention responses
6. 🔧 Deploy and validate functionality

## 💡 **Pro Tips**

### **Leverage Existing Work:**
- **Don't reinvent**: Use existing webhook configuration
- **Build on success**: Extend current Discord integration
- **Reuse patterns**: Follow established API patterns
- **Document progress**: Update session summaries

### **Development Approach:**
- **Start simple**: Basic @claude mention detection first
- **Iterate quickly**: Test early, refine responses
- **Use context**: Reference Industrial IoT Stack components
- **Stay secure**: Follow established authentication patterns

## 🎉 **The Vision Realized**

### **End State:**
```
Discord Channel:
🚨 [MQTT Alert] Equipment temperature high: 85°C

User: "@claude what caused this spike?"

Claude Bot: "Analyzing MQTT data... The temperature spike at 14:23 
corresponds with cooling pump flow drop detected in n8n workflow. 
Node-RED bridge shows valve V-301 may need attention. Recommend 
checking pump status and valve position."

User: "@claude can you restart the cooling system?"

Claude Bot: "I can guide you through the restart process. First, 
check the EMQX broker for any error messages, then use the n8n 
workflow to send restart command to equipment/control topic."
```

**This is the breakthrough feature that turns Discord into your 
live Industrial IoT command center!** 🚀

---

**Created**: Pre-auto compact preparation  
**Priority**: High - User's dream feature implementation  
**Dependencies**: Existing Discord webhook system (working)  
**Timeline**: ~1 hour to working prototype  
**Impact**: Revolutionary Discord ↔ Claude interaction capability