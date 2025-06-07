# Industrial IoT Stack - Complete Navigation Index

## 🚀 Quick Start
- **[START HERE](START_HERE.md)** - Essential onboarding for new users
- **[Quick Tour](QUICK-TOUR.md)** - 5-minute overview of the entire stack
- **[Setup Guide](docs/setup/QUICK_SETUP.md)** - Step-by-step installation

## 📚 Core Documentation

### System Overview
- **[Stack Overview](STACK-OVERVIEW.md)** - Complete system architecture
- **[Session Summary](SESSION_SUMMARY.md)** - Current project status
- **[Integration Guide](INTEGRATION-GUIDE.md)** - How components connect

### Setup & Configuration
- **[Docker Migration Strategy](DOCKER_MIGRATION_STRATEGY.md)** - Containerization approach
- **[Server Setup Guide](SERVER_SETUP_GUIDE.md)** - Production deployment
- **[Scalability Analysis](SCALABILITY_ANALYSIS.md)** - Performance planning

## 🔧 Component Documentation

### Communication Systems
- **[WhatsApp Integration](WHATSAPP_API_INTEGRATION_GUIDE.md)** - Complete WhatsApp API guide
- **[Discord Integration](DISCORD_INTEGRATION_VISION.md)** - Team coordination setup
- **[Formbricks Integration](FORMBRICKS_HYBRID_INTEGRATION_GUIDE.md)** - Form management system

### Workflow Automation
- **[n8n Setup](N8N_API_CAPABILITIES.md)** - Workflow automation
- **[n8n Troubleshooting](N8N_MQTT_TROUBLESHOOTING_GUIDE.md)** - Common issues
- **[Node-RED Flows](node-red-flows/)** - Visual flow programming

### Data Management
- **[Google Sheets Integration](GOOGLE_SHEETS_FEATURES.md)** - Complete setup guide
- **[MQTT Architecture](MQTT_BROKER_ARCHITECTURE.md)** - Message broker design
- **[Topic Alignment](TOPIC-ALIGNMENT.md)** - Data flow mapping

### Ignition & Industrial Systems
- **[Ignition Integration](IGNITION_INTEGRATION_SETUP.md)** - HMI/SCADA setup
- **[Flint Integration](FLINT_IGNITION_INTEGRATION.md)** - Development tools
- **[Ignition Module Setup](IGNITION_MODULE_SETUP.md)** - Custom modules

## 🏭 Steel Bonnet Brewery

### Implementation
- **[Steel Bonnet Overview](Steel_Bonnet/README.md)** - Brewery-specific setup
- **[Equipment Registration](Steel_Bonnet/EQUIPMENT_REGISTRATION_FIXES.md)** - Asset management
- **[MQTT Topic Map](Steel_Bonnet/docs/MQTT_topic_map.md)** - Data structure

### Resources
- **[Scripts](Steel_Bonnet/scripts/)** - Automation and utilities
- **[UDTs](Steel_Bonnet/udts/)** - User Defined Types
- **[Views](Steel_Bonnet/views/)** - HMI screens
- **[Node-RED Flows](Steel_Bonnet/node-red-flows/)** - Brewery workflows

## 🛠️ Development Tools

### Scripts & Utilities
- **[Setup Scripts](scripts/setup/)** - Installation automation
- **[Testing Scripts](scripts/testing/)** - Validation tools
- **[Monitoring Scripts](scripts/monitoring/)** - System health
- **[Utility Scripts](scripts/utilities/)** - General purpose tools

### Automation
- **[GitHub Actions](GITHUB_ACTIONS_CLAUDE_MAX_SETUP.md)** - CI/CD setup
- **[Agent Management](agents/)** - Automated assistants
- **[Backup Systems](backups/)** - Data protection

## 📱 Integration Points

### APIs & Webhooks
- **[WhatsApp API Client](scripts/whatsapp_api_client.py)** - Complete implementation
- **[Discord Webhook](scripts/discord_notification_client.py)** - Team notifications
- **[Formbricks API](scripts/formbricks_api_client.py)** - Form processing
- **[Unified Monitoring](scripts/unified_monitoring_system.py)** - System oversight

### Data Flow
- **[MQTT → WhatsApp](whatsapp-integration/)** - Equipment alerts
- **[Formbricks → Sheets](n8n-workflows/)** - Form submissions
- **[Discord → Team](discord-bot/)** - Coordination hub

## 🔒 Security & Credentials
- **[Credentials Management](credentials/)** - API keys and certificates
- **[Security Checklist](docs/security/SECURITY_CHECKLIST.md)** - Best practices
- **[Environment Variables](docs/setup/ENVIRONMENT_SETUP.md)** - Configuration

## 📊 Monitoring & Analytics
- **[System Status](STATUS.md)** - Current health overview
- **[Performance Monitoring](scripts/monitoring/)** - Automated checks
- **[Tribal Knowledge](TRIBAL_KNOWLEDGE_SYSTEM.md)** - Accumulated insights

## 🚀 Deployment

### Local Development
- **[Local Setup](docs/setup/LOCAL_DEVELOPMENT.md)** - Development environment
- **[Testing Guide](docs/testing/TESTING_GUIDE.md)** - Validation procedures
- **[Troubleshooting](docs/troubleshooting/COMMON_ISSUES.md)** - Problem resolution

### Production Deployment
- **[Server Deployment](SERVER_CLAUDE_DEPLOYMENT_PACKAGE.md)** - Production setup
- **[Docker Configuration](docker-configs/)** - Container management
- **[Cloud Setup](docs/deployment/CLOUD_DEPLOYMENT.md)** - Scalable hosting

## 🔄 Workflow Automation

### n8n Workflows
- **[MQTT → WhatsApp](n8n-workflows/mqtt-to-whatsapp-alerts.json)** - Equipment alerts
- **[Formbricks → Sheets](n8n-workflows/formbricks-to-sheets-final.json)** - Form processing

### Node-RED Flows
- **[Equipment Monitoring](node-red-flows/mqtt-to-alerts-bridge.json)** - Real-time alerts
- **[System Integration](node-red-flows/n8n-to-ignition-commands.json)** - Cross-platform

## 📖 Reference Documentation

### Technical Specifications
- **[MQTT Protocol](docs/protocols/MQTT_SPECIFICATION.md)** - Message standards
- **[API Reference](docs/api/API_REFERENCE.md)** - Endpoint documentation
- **[Data Models](docs/models/DATA_MODELS.md)** - Structure definitions

### Operational Procedures
- **[Daily Operations](docs/operations/DAILY_PROCEDURES.md)** - Routine tasks
- **[Maintenance Schedule](docs/maintenance/SCHEDULE.md)** - Upkeep planning
- **[Emergency Procedures](docs/emergency/EMERGENCY_RESPONSE.md)** - Crisis management

## 🎯 For Different Users

### **New Team Members**
1. Start with [START_HERE.md](START_HERE.md)
2. Review [QUICK-TOUR.md](QUICK-TOUR.md)
3. Follow [Quick Setup](docs/setup/QUICK_SETUP.md)

### **Developers**
1. Check [Local Development](docs/setup/LOCAL_DEVELOPMENT.md)
2. Review [Testing Guide](docs/testing/TESTING_GUIDE.md)
3. Explore [Scripts Organization](scripts/)

### **Operators**
1. Review [Steel Bonnet Setup](Steel_Bonnet/README.md)
2. Check [WhatsApp Integration](WHATSAPP_API_INTEGRATION_GUIDE.md)
3. Monitor via [Discord Integration](DISCORD_INTEGRATION_VISION.md)

### **System Administrators**
1. Follow [Server Setup](SERVER_SETUP_GUIDE.md)
2. Review [Docker Configuration](docker-configs/)
3. Check [Monitoring Tools](scripts/monitoring/)

---

## 📧 Support & Coordination

- **Discord Channel**: Team coordination and real-time alerts
- **WhatsApp Integration**: Equipment monitoring and maintenance alerts
- **Google Sheets**: Progress tracking and analytics
- **GitHub Issues**: Bug reports and feature requests

**Last Updated**: 2025-06-04 23:30:00 UTC  
**Repository Organization**: 5/5 ⭐  
**Ready for Production**: ✅