# Industrial IoT Stack Configuration Reference

## Service Endpoints

### EMQX MQTT Broker
- **Container IP**: 172.17.0.4 (Bridge network)
- **MQTT Port**: 1883 (Authentication DISABLED)
- **WebSocket Port**: 8083
- **Dashboard**: http://localhost:18083
- **Dashboard Username**: admin
- **Dashboard Password**: adminpass123
- **MQTT Connection**: Anonymous (no credentials required)
- **n8n Connection Host**: `host.docker.internal` (due to network isolation)

### n8n Workflow Automation
- **Web Interface**: http://localhost:5678
- **Username**: admin
- **Password**: admin
- **Database**: PostgreSQL (n8n-postgres container)
- **API Endpoints**:
  - REST API: http://localhost:5678/rest/* (Basic Auth)
  - API v1: http://localhost:5678/api/v1/* (API Key required)
- **API Key**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZjkyYWY0Ni01YmQ1LTQ0MTgtODdmZi1iMzBlZWU4NDI1YzYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzQ4OTgwMDg0fQ.SzBoM46h15zLzepNuFgWV2cqCAgQSHVROvsgaFPzTC4`

### Node-RED
- **Web Interface**: http://localhost:1880
- **Container Name**: nodered

### TimescaleDB
- **Port**: 5432
- **Database**: iotstack
- **Username**: postgres
- **Password**: postgres

### Ignition Edge
- **Gateway**: http://localhost:8088
- **Designer Port**: 8043

## Google Sheets Integration
- **Service Account Email**: server-claude@iiot-stack-automation.iam.gserviceaccount.com
- **Credentials File**: `/home/server/google-sheets-credentials.json`
- **Master Spreadsheet ID**: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do

## Docker Networks
- **Bridge Network**: Default Docker bridge (172.17.0.0/16) - EMQX runs here
- **IoT Network**: industrial-iot-stack_iiot-network - n8n, PostgreSQL run here
- **⚠️ Cross-Network Communication**: Use `host.docker.internal` for container→host→container communication

## n8n Workflow Files (Imported)
1. **Formbricks→Sheets**: Workflow ID `n3UFERK5ilPYrLP3`
2. **MQTT→WhatsApp**: Workflow ID `PptMUA3BfrivzhG9` (Fixed with proper MQTT trigger)

## MQTT Topics for Testing
- `equipment/alerts` - Critical equipment alerts
- `sensors/critical` - Critical sensor readings
- `actuators/fault` - Actuator fault notifications

## Quick Commands
```bash
# Check all services
docker ps

# View n8n logs
docker logs -f n8n

# Test MQTT connection (from host)
mosquitto_pub -h localhost -p 1883 -t "test/topic" -m "test message"

# Test MQTT from external (Mac/other machine)
mosquitto_pub -h <WINDOWS_IP> -p 1883 -t "test/topic" -m "test message"

# Access n8n PostgreSQL
docker exec -it n8n-postgres psql -U n8n_user -d n8n
```

## Last Updated
June 3, 2025