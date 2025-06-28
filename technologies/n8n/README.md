# 🔄 n8n Workflow Automation - Industrial IoT Stack

**n8n is a powerful workflow automation platform** that connects various systems in our industrial IoT stack through visual programming and API integrations.

## 🚀 Quick Start for Claude Instances

**New to n8n integration?** Start here:
1. `setup-guides/N8N_INITIAL_SETUP.md` - Complete n8n installation
2. `setup-guides/N8N_API_KEY_SETUP.md` - API access configuration
3. `docker-configs/docker-compose-n8n.yml` - Production deployment
4. `workflows/` - Ready-to-import workflow examples

## 🎯 What n8n Does in Our Stack

### Core Capabilities
- **Visual Workflow Builder**: Drag-and-drop interface for complex automations
- **400+ Integrations**: Built-in nodes for APIs, databases, cloud services
- **Event-Driven**: Responds to webhooks, schedules, and data changes
- **Real-time Processing**: Instant data transformation and routing

### Key Integrations
- **Google Sheets**: Automated task management and data synchronization
- **MQTT**: Industrial equipment monitoring and alert processing
- **WhatsApp**: Automated notifications and status updates
- **Discord**: Task creation and team communication
- **Formbricks**: Survey data processing and analysis

## 🏭 Production Features

- **Self-hosted**: Full control over workflows and data
- **API Access**: Programmatic workflow management
- **Webhook Support**: Real-time external system integration
- **Error Handling**: Built-in retry and error management
- **Scalable**: Handles high-volume industrial data processing

## 📂 Directory Structure

```
technologies/n8n/
├── README.md              # You are here
├── INDEX.md               # Complete file listing
├── setup-guides/          # Installation and configuration
├── workflows/             # Ready-to-import workflows
├── integrations/          # Technology-specific integrations
├── scripts/               # Automation and management scripts
├── docker-configs/        # Production deployment configs
└── troubleshooting/       # Common issues and solutions
```

## 🔧 Essential Endpoints

- **n8n UI**: http://localhost:5678
- **API**: http://localhost:5678/api/v1
- **Webhooks**: http://localhost:5678/webhook/[workflow-id]
- **Health Check**: http://localhost:5678/healthz

## 🔗 Related Technologies

- **MQTT**: `../mqtt/` - Equipment data ingestion
- **Google Sheets**: `../google-sheets/` - Task tracking integration
- **Discord**: `../discord/` - Notification workflows
- **WhatsApp**: `../whatsapp/` - Alert messaging

## 💡 Common Workflows

1. **MQTT to WhatsApp Alerts**: Equipment alarms → WhatsApp notifications
2. **Formbricks to Sheets**: Survey responses → Google Sheets tracking
3. **Discord to Sheets**: Task creation → Automated processing
4. **Equipment Monitoring**: Continuous data → Multi-channel alerts

---
*Files Organized: 45+ | Technology Status: ✅ Production Ready*