# Ignition n8n Integration Scripts

## Overview
Complete set of Python scripts for integrating Ignition with n8n workflows.

## Scripts Generated
1. **ignition_equipment_alerts.py** - Send equipment alerts to n8n MQTT workflow
2. **ignition_data_logger.py** - Log equipment data to Google Sheets via n8n  
3. **ignition_webhook_receiver.py** - Receive and execute commands from n8n

## Quick Start
1. Copy scripts to Ignition Designer Project Library
2. Configure n8n webhook endpoints
3. Update equipment tag mappings in scripts
4. Test integration with sample alerts

## API Configuration
- n8n API URL: http://172.28.214.170:5678/api/v1
- Webhook Base: http://172.28.214.170:5678/webhook/
- Authentication: API Key included in scripts

## Support
See installation_guide.json for detailed setup instructions.

Generated: 2025-06-04 06:42:10
