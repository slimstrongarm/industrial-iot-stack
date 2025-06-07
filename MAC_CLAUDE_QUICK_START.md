# Mac Claude Quick Start Guide 🚀

## 🎯 Current Situation (June 4, 2025)
- **Industrial IoT Stack project** is running on Windows/WSL2 with Docker
- **Server Claude** has been working autonomously and completed major tasks
- **Mac Claude** is joining fresh to help with remaining integration work
- **Github Actions path didn't work** - we're going back to direct collaboration

## 📊 Project Status Summary

### ✅ What's ALREADY WORKING:
- **Docker Stack**: EMQX MQTT, Node-RED, n8n all running
- **n8n API**: Fully configured and tested (75% endpoint success rate)
- **MQTT Integration**: Fixed Docker network isolation with `host.docker.internal`
- **Workflows**: Both Formbricks→Sheets and MQTT→WhatsApp imported to n8n
- **Google Sheets**: Live progress tracking system operational

### 🔄 What's IN PROGRESS:
- **CT-008**: Integration Test (70% complete, waiting on human tasks)
- **CT-022**: Discord Integration (scripts ready, need webhook URLs)

### ⏳ What NEEDS MAC CLAUDE:
- **HT-002**: Create Discord webhooks (5 min)
- **HT-003**: Configure n8n Google Sheets credentials (5 min) 
- **HT-006**: Get Formbricks API key (10 min)

## 🔗 Repository Access Test

### First Priority: Verify Repository Access
```bash
# 1. Check if you can access the repo
cd /path/to/your/workspace
git clone https://github.com/[USER]/industrial-iot-stack.git
cd industrial-iot-stack

# 2. Test read access to key files
ls -la
cat STACK_CONFIG.md
cat N8N_INTEGRATION_COMPLETE.md
```

## 🚀 Critical Connection Details

### n8n API Access (READY TO USE)
```bash
# Test n8n API connectivity from Mac
curl -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4" \
     http://172.28.214.170:5678/api/v1/workflows
```

### Google Sheets Integration
- **Spreadsheet ID**: `1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do`
- **Credentials**: Available on Windows machine
- **Live tracking**: Claude Tasks, Human Tasks, System Components

### Docker Network Discovery
- **EMQX MQTT**: `172.17.0.4:1883` (use `host.docker.internal` from n8n)
- **Node-RED**: `172.28.214.170:1880`
- **n8n**: `172.28.214.170:5678`

## 🎯 Immediate Next Steps for Mac Claude

### Step 1: Repository Verification (2 min)
```bash
# Clone and verify access
git clone [REPO_URL]
cd industrial-iot-stack
ls scripts/ docs/ 
```

### Step 2: Test n8n API (2 min)
```bash
# Verify n8n API works from Mac
curl -H "X-N8N-API-KEY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4" \
     http://172.28.214.170:5678/api/v1/workflows
```

### Step 3: Quick Human Task Wins (15 min total)
1. **HT-002**: Create Discord webhooks (5 min)
2. **HT-003**: Configure Google Sheets in n8n (5 min)
3. **HT-006**: Get Formbricks API key (5 min)

## 📋 Key Files to Review

### Critical Documents:
- `STACK_CONFIG.md` - All system IPs, ports, credentials
- `N8N_INTEGRATION_COMPLETE.md` - Complete n8n setup guide
- `CT-008_PROGRESS_REPORT.json` - Current integration test status
- `scripts/discord_webhook_integration.py` - Ready Discord integration

### Current Workflows in n8n:
- **Formbricks→Sheets**: ID `n3UFERK5ilPYrLP3`
- **MQTT→WhatsApp**: ID `PptMUA3BfrivzhG9`

## 🚨 Known Issues & Solutions

### Docker Network (SOLVED)
- **Issue**: n8n couldn't reach EMQX across Docker networks
- **Solution**: Use `host.docker.internal` instead of container IPs
- **Status**: ✅ Fixed and documented

### MQTT Authentication (SOLVED)
- **Issue**: Various MQTT auth failures
- **Solution**: Network isolation, not auth - fixed with network discovery
- **Status**: ✅ Working

## 🤝 Coordination Protocol

### When Mac Claude Completes Tasks:
1. **Update Google Sheets** immediately
2. **Commit changes** to repository  
3. **Report status** to human user
4. **Coordinate with Server Claude** on next steps

### Communication Format:
```
✅ COMPLETED: [Task ID] - [Brief description]
📊 IMPACT: [What this enables]
🎯 NEXT: [Recommended next step]
```

## 📞 Emergency Contacts & Fallbacks

### If Repository Access Fails:
- Try via HTTPS vs SSH
- Check network connectivity to GitHub
- Alternative: work locally and share via other means

### If n8n API Fails:
- Check Windows machine Docker status
- Verify IP address hasn't changed
- Test with simple ping first

### If Stuck:
- Focus on the 3 immediate human tasks (HT-002, HT-003, HT-006)
- These can be done independently of complex integrations
- Each takes 5-10 minutes max

## 🎯 Success Criteria

### Immediate (Next 30 min):
- ✅ Repository access confirmed
- ✅ n8n API connectivity verified
- ✅ At least 1 human task completed

### Short-term (Next 2 hours):
- ✅ All 3 human tasks completed
- ✅ CT-008 integration test advanced to 90%+
- ✅ End-to-end MQTT→Discord flow working

---

## 🚀 LET'S GO!

**Priority 1**: Test repository access
**Priority 2**: Test n8n API 
**Priority 3**: Complete HT-002 (Discord webhooks)

The infrastructure is ready - we just need to connect the final pieces! 🔗