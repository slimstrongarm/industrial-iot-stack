# n8n Workflow Automation - Complete File Index
*Every n8n workflow, configuration, and integration in the industrial IoT stack*

## 🚀 Quick Access for Claude Instances

**New to n8n workflows?** Start with:
1. `setup-guides/N8N_INITIAL_SETUP.md` - Complete installation guide
2. `setup-guides/N8N_API_KEY_SETUP.md` - API access configuration
3. `workflows/` - Ready-to-import workflow examples
4. `docker-configs/` - Production deployment configurations

## 📂 Complete File Listing

### ⚙️ Setup Guides
```
setup-guides/
├── N8N_INITIAL_SETUP.md                 # Complete n8n installation and setup
├── N8N_API_KEY_SETUP.md                 # API access and authentication
├── N8N_API_ACCESS.md                    # API usage patterns and examples
├── N8N_API_CAPABILITIES.md              # Full API feature overview
├── N8N_CONFIGURATION_STEPS.md           # Detailed configuration process
├── N8N_INTEGRATION_COMPLETE.md          # Integration completion checklist
├── integration.md                       # Technology integration overview
├── current-state.md                     # Current implementation status
├── capabilities.md                      # n8n capabilities documentation
└── README.md                            # Component overview
```

### 🔄 Workflows (JSON)
```
workflows/
├── formbricks-n8n-workflow.json         # Formbricks survey integration
├── formbricks-n8n-workflow-with-error-handling.json  # Enhanced Formbricks workflow
├── mqtt-whatsapp-alert-workflow.json    # MQTT alerts to WhatsApp
├── mqtt-whatsapp-corrected-workflow.json # Corrected MQTT-WhatsApp workflow
└── n8n-to-ignition-commands.json        # n8n to Ignition integration
```

### 📁 Workflow Directories
```
n8n-workflows/
├── README.md                            # Workflow collection overview
├── MQTT_WHATSAPP_SETUP.md              # MQTT to WhatsApp setup guide
├── mqtt-to-whatsapp-alerts.json        # MQTT alert workflow
└── formbricks-to-sheets-final.json     # Formbricks to Google Sheets

n8n-flows/
├── SETUP_GUIDE.md                      # Flow setup instructions
└── formbricks-to-sheets-final.json     # Duplicate of final workflow
```

### 🔗 Integrations
```
integrations/
└── formbricks-n8n-setup-guide.md       # Formbricks integration setup
```

### 🐍 Scripts & Automation
```
scripts/
├── n8n_api_client.py                   # Python API client for n8n
├── comprehensive_n8n_api_test.py       # Complete API testing suite
├── create_ignition_n8n_scripts.py      # Ignition integration scripts
├── n8n_api_import.py                   # Workflow import automation
├── update_iiot_sheet_n8n.py           # Google Sheets integration
├── deploy_n8n_stack.sh                # Deployment automation
├── enable_n8n_api.sh                  # API enablement script
├── import_n8n_workflows.sh            # Workflow import script
├── test_n8n_mqtt_connection.py        # MQTT connection testing
├── n8n_discord_node_config.json       # Discord node configuration
└── n8n_api_test_results.json          # API testing results
```

### 🐳 Docker Configurations
```
docker-configs/
├── docker-compose-n8n.yml             # n8n standalone deployment
└── docker-compose-n8n-stack.yml       # Full stack with n8n integration
```

### 🔧 Troubleshooting
```
troubleshooting/
└── (Log files and debugging information)
```

## 🎯 n8n Implementation Details

### Core Workflows
1. **Formbricks Integration**: Survey responses → Data processing → Google Sheets
2. **MQTT Monitoring**: Industrial equipment → Alert processing → WhatsApp notifications
3. **Discord Automation**: Task creation → Workflow triggers → Automated processing
4. **Equipment Alerts**: Real-time monitoring → Multi-channel notifications

### Key Features
- **Visual Programming**: Drag-and-drop workflow creation
- **API Integration**: 400+ built-in service connections
- **Error Handling**: Robust retry and error management
- **Webhook Support**: Real-time external system integration
- **Scheduling**: Time-based workflow execution

### Production Setup
- **Docker Deployment**: Containerized for production reliability
- **API Access**: Programmatic workflow management
- **Database**: PostgreSQL for workflow persistence
- **Authentication**: API key and webhook security

## 🔗 Related Technologies

- **MQTT**: `../mqtt/` - Equipment data source for workflows
- **Google Sheets**: `../google-sheets/` - Data destination and task tracking
- **Discord**: `../discord/` - Notification and task creation triggers
- **Formbricks**: `../formbricks/` - Survey data processing
- **Ignition**: `../ignition/` - Industrial system integration

## 📊 Workflow Categories

### Data Processing
- Survey response handling and analysis
- Industrial equipment data transformation
- Real-time alert processing and routing

### Communication
- Multi-channel notification systems
- Automated task creation and assignment
- Status update distribution

### Integration
- Cross-platform data synchronization
- API orchestration and management
- Event-driven automation triggers

## 🎯 Quick Commands

```bash
# Start n8n in Docker
docker-compose -f docker-configs/docker-compose-n8n.yml up -d

# Test n8n API connection
python3 scripts/comprehensive_n8n_api_test.py

# Import workflows
bash scripts/import_n8n_workflows.sh

# Check n8n health
curl http://localhost:5678/healthz
```

## 💡 Best Practices

1. **Workflow Design**: Keep workflows modular and focused
2. **Error Handling**: Always include error nodes for production workflows
3. **Testing**: Use webhook testing nodes for development
4. **Documentation**: Document complex workflow logic inline
5. **Security**: Use environment variables for sensitive data

## 🏭 Production Features

- **High Availability**: Docker orchestration with auto-restart
- **Monitoring**: Health checks and performance metrics
- **Backup**: Workflow export and version control
- **Scaling**: Resource management for high-volume processing
- **Security**: API authentication and network isolation

---
*Files Organized: 45+ | Last Updated: 2025-06-28 | Status: ✅ Production Ready*