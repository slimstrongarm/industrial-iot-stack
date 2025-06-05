# Scripts Directory

This directory contains all automation scripts for the Industrial IoT Stack, organized by function.

## 📁 Directory Structure

### `/setup/`
- **Purpose**: Installation and configuration automation
- **Contents**: Environment setup, dependency installation, initial configuration
- **Examples**: `install_dependencies.py`, `configure_environment.sh`, `setup_credentials.py`

### `/testing/`
- **Purpose**: Testing and validation automation
- **Contents**: Integration tests, API validation, system health checks
- **Examples**: `test_integrations.py`, `validate_configurations.py`, `health_check.py`

### `/monitoring/`
- **Purpose**: System monitoring and analytics
- **Contents**: Performance monitoring, alert processing, data collection
- **Examples**: `unified_monitoring_system.py`, `monitor_sheets_progress.py`, `system_health.py`

### `/utilities/`
- **Purpose**: General-purpose utility scripts
- **Contents**: Data processing, file management, helper functions
- **Examples**: `backup_configs.py`, `clean_logs.py`, `export_data.py`

## 🔧 Current Scripts (To Be Reorganized)

### Google Sheets Integration
- `google_sheets_setup.gs` → `/setup/`
- `sheets_monitor_live.py` → `/monitoring/`
- `test_sheets_access.py` → `/testing/`
- `comprehensive_sheets_update.py` → `/utilities/`

### API Clients
- `whatsapp_api_client.py` → `/utilities/`
- `formbricks_api_client.py` → `/utilities/`
- `discord_notification_client.py` → `/utilities/`

### Monitoring Systems
- `unified_monitoring_system.py` → `/monitoring/`
- `monitor_claude_tasks.py` → `/monitoring/`
- `morning_status_update.py` → `/monitoring/`

### Setup & Configuration
- `setup_claude_server_instance.sh` → `/setup/`
- `setup_form_submissions_sheet.py` → `/setup/`
- `automated_server_setup.expect` → `/setup/`

### Testing & Validation
- `test_sheets_connection.py` → `/testing/`
- `test_n8n_mqtt_connection.py` → `/testing/`
- `test_github_actions_access.py` → `/testing/`

## 📜 Script Naming Conventions

- **Python scripts**: `lowercase_with_underscores.py`
- **Shell scripts**: `lowercase_with_underscores.sh`
- **Google Apps Scripts**: `camelCase.gs`
- **Configuration files**: `UPPERCASE_UNDERSCORES.json/yml`

## 🚀 Usage Guidelines

### Running Scripts
```bash
# From repository root
python3 scripts/monitoring/unified_monitoring_system.py
bash scripts/setup/configure_environment.sh
```

### Adding New Scripts
1. **Choose appropriate directory** based on function
2. **Follow naming conventions**
3. **Add docstring** with purpose and usage
4. **Update this README** with new script reference

### Dependencies
- **Python 3.9+** for all Python scripts
- **Required packages**: Listed in each script's docstring
- **Environment variables**: Documented in `/docs/setup/`

## 🔗 Integration Points

### Google Sheets
- **Credentials**: `../credentials/iot-stack-credentials.json`
- **Sheet ID**: Environment variable `GOOGLE_SHEETS_ID`
- **API Scope**: Read/write access to spreadsheets

### Discord
- **Webhook URL**: `../credentials/discord_webhook.txt`
- **Notification types**: Equipment alerts, task updates, system status

### WhatsApp
- **Twilio API**: Environment variables for account SID and auth token
- **Phone numbers**: Configured in environment

### n8n
- **API Endpoint**: http://100.94.84.126:5678
- **Authentication**: Basic auth with environment variables

## 📊 Monitoring & Logging

All scripts should:
- **Log to console** with appropriate verbosity
- **Update Google Sheets** for tracking (when applicable)
- **Send Discord notifications** for important events
- **Handle errors gracefully** with proper exception handling

---

**Maintained by**: Industrial IoT Stack Team  
**Last Updated**: 2025-06-04 23:40:00 UTC