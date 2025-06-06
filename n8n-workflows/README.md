# n8n Workflows for Industrial IoT Stack

## Quick Setup Instructions

### 1. Deploy n8n Container
```bash
# From the docker-configs directory
cd /path/to/industrial-iot-stack/docker-configs
docker-compose -f docker-compose-n8n.yml up -d
```

### 2. Access n8n Interface
- URL: http://localhost:5678
- Username: `iiot-admin`
- Password: `StrongPassword123!` (or set N8N_PASSWORD environment variable)

### 3. Initial Configuration

#### Google Sheets Integration
1. Go to Settings → Credentials → Add Credential
2. Select "Google Sheets API"
3. Choose "Service Account" method
4. Upload: `/opt/credentials/iot-stack-credentials.json`
5. Test connection

#### MQTT Integration  
1. Add MQTT credential
2. Host: `host.docker.internal` (for local EMQX) or server IP
3. Port: `1883`
4. Configure authentication if needed

### 4. Import Industrial Workflows

Available workflows in this directory:
- `formbricks-to-sheets-final.json` - Form data collection
- `mqtt-to-sheets-logger.json` - MQTT data logging
- `equipment-maintenance-scheduler.json` - Maintenance workflows
- `quality-control-processor.json` - Quality data processing

To import:
1. Go to Workflows → Import from File
2. Select the JSON file
3. Configure credentials in each node
4. Activate the workflow

## Environment Variables

Create a `.env` file in the docker-configs directory:
```bash
# n8n Configuration
N8N_PASSWORD=YourSecurePassword123!

# Database (if using PostgreSQL)
POSTGRES_PASSWORD=your_postgres_password

# Email notifications (optional)
SMTP_USER=your-email@domain.com
SMTP_PASS=your-app-password
```

## Production Considerations

### 1. Database Upgrade
For production, uncomment PostgreSQL service in docker-compose-n8n.yml:
```yaml
# Change in n8n service environment:
- DB_TYPE=postgresdb
- DB_POSTGRESDB_HOST=n8n-postgres
- DB_POSTGRESDB_DATABASE=n8n
- DB_POSTGRESDB_USER=n8n
- DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
```

### 2. SSL/HTTPS Setup
Add reverse proxy (Traefik/Nginx) for HTTPS:
```yaml
# Add to n8n service
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.n8n.rule=Host(`n8n.yourdomain.com`)"
  - "traefik.http.routers.n8n.tls.certresolver=letsencrypt"
```

### 3. Backup Strategy
```bash
# Backup workflows and credentials
docker exec iiot-n8n n8n export:workflow --all --output=/home/node/.n8n/backups/
docker exec iiot-n8n n8n export:credentials --all --output=/home/node/.n8n/backups/

# Backup database
docker exec iiot-n8n-db pg_dump -U n8n n8n > n8n_backup_$(date +%Y%m%d).sql
```

## Integration with Existing Stack

### Node-RED Integration
- Use HTTP Request nodes to call Node-RED flows
- Share MQTT topics between Node-RED and n8n
- Webhook communication for triggering flows

### Ignition Integration
- REST API calls to Ignition Gateway
- Database queries to Ignition SQL tags
- OPC-UA client nodes for direct communication

### EMQX Integration
- MQTT Subscribe/Publish nodes
- Real-time data processing from brewery equipment
- Alert generation based on sensor thresholds

## Monitoring & Maintenance

### Health Checks
```bash
# Check n8n status
docker exec iiot-n8n wget -q --spider http://localhost:5678/healthz

# View logs
docker logs iiot-n8n --tail 100 -f
```

### Performance Monitoring
- Access n8n logs at: Settings → Log files
- Monitor execution history: Executions → View all
- Check resource usage: `docker stats iiot-n8n`

## Troubleshooting

### Common Issues
1. **Credential errors**: Verify Google Sheets service account permissions
2. **Webhook timeouts**: Check firewall and network connectivity  
3. **Memory issues**: Increase container memory limits
4. **Database locks**: Restart container if SQLite issues occur

### Log Analysis
```bash
# Container logs
docker logs iiot-n8n

# n8n internal logs
docker exec iiot-n8n ls -la /home/node/.n8n/logs/
```

Ready for industrial workflow automation! 🏭⚡