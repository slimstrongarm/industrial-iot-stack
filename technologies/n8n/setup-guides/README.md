# n8n - Workflow Automation Platform

## Overview
n8n is an extendable workflow automation tool that enables you to connect anything to everything. In our Industrial IoT stack, n8n serves as the advanced workflow orchestration layer, complementing Node-RED for complex integrations and business logic.

## Role in IIoT Stack
- **Advanced Workflow Automation**: Complex multi-step processes
- **Data Integration Hub**: Connect disparate systems
- **Business Logic Layer**: Implement sophisticated rules
- **API Orchestration**: Manage external service integrations

## Key Capabilities
- 350+ native integrations
- Visual workflow builder
- Code flexibility when needed
- Self-hostable with full data control
- Webhook support for real-time triggers
- Error handling and retry logic
- Version control for workflows

## Current Implementation Status
- ✅ Architecture designed
- ✅ Docker configuration prepared
- 🔄 Formbricks integration POC
- 📋 Pending deployment to server

## Why n8n + Node-RED?
While Node-RED excels at:
- Real-time data processing
- Hardware integration
- MQTT/OPC-UA protocols
- Edge computing logic

n8n complements with:
- Complex business workflows
- Database operations
- API integrations
- Scheduled jobs
- Human-in-the-loop processes

## Architecture Position
```
[Field Devices] → [Node-RED] → [MQTT] → [n8n] → [Business Systems]
                                    ↓
                               [Ignition]
```

## Use Cases in Industrial Settings
1. **Quality Control Workflows**
   - Form submission → Data validation → Database storage → Alert generation

2. **Maintenance Scheduling**
   - Equipment data → Threshold checks → Work order creation → Technician notification

3. **Production Reporting**
   - Shift data collection → Aggregation → Report generation → Email distribution

4. **Compliance Documentation**
   - Sensor readings → Compliance checks → Document generation → Regulatory submission

5. **Customer Integration**
   - Order systems → Production scheduling → Status updates → Customer portals

## Docker Deployment
```yaml
n8n:
  image: n8nio/n8n:latest
  container_name: iiot-n8n
  ports:
    - "5678:5678"
  environment:
    - N8N_BASIC_AUTH_ACTIVE=true
    - N8N_BASIC_AUTH_USER=admin
    - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
    - N8N_HOST=n8n.${DOMAIN}
    - N8N_PORT=5678
    - N8N_PROTOCOL=https
    - NODE_ENV=production
    - WEBHOOK_URL=https://n8n.${DOMAIN}/
    - GENERIC_TIMEZONE=America/Chicago
  volumes:
    - n8n_data:/home/node/.n8n
  networks:
    - iiot-network
  restart: unless-stopped
```

## Integration Points
- **Ignition**: Via REST API and database
- **Node-RED**: Via webhooks and MQTT
- **Google Sheets**: Native integration
- **Databases**: PostgreSQL, MySQL, MongoDB
- **Cloud Services**: AWS, Azure, Google Cloud
- **Communication**: Email, Slack, Teams

## Security Considerations
- Basic auth for UI access
- Encrypted credentials storage
- Webhook authentication
- API key management
- Network isolation options

## Next Steps
1. Deploy n8n container
2. Configure authentication
3. Import workflow templates
4. Test Formbricks integration
5. Create IIoT-specific workflows
6. Document best practices