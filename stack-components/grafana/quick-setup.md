# Grafana Quick Setup Guide

## 🚀 5-Minute Setup

### Step 1: Create Environment File
Create `.env` file in the grafana directory:
```bash
# Grafana Admin
GRAFANA_USER=admin
GRAFANA_PASSWORD=your_secure_password

# InfluxDB
INFLUXDB_USER=admin
INFLUXDB_PASSWORD=your_secure_password
INFLUXDB_TOKEN=your-super-secret-auth-token

# PostgreSQL (use existing Ignition DB)
POSTGRES_USER=ignition
POSTGRES_PASSWORD=your_postgres_password

# MQTT
MQTT_USER=iiot
MQTT_PASSWORD=your_mqtt_password

# Domain
DOMAIN=your-domain.com

# SMTP (optional)
SMTP_ENABLED=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Step 2: Deploy Stack
```bash
# Create network if not exists
docker network create iiot-network

# Deploy Grafana stack
docker-compose up -d

# Check status
docker-compose ps
```

### Step 3: Access Grafana
1. Open browser to http://localhost:3000
2. Login with admin credentials
3. You'll see pre-configured data sources

### Step 4: Import Industrial Dashboard
1. Click "+" → "Import"
2. Upload `industrial-dashboards/production-overview.json`
3. Select InfluxDB as data source
4. Click Import

## 📊 Pre-Built Industrial Dashboards

### 1. Production Overview
- Real-time production rates
- OEE calculations
- Downtime tracking
- Quality metrics

### 2. Equipment Monitoring
- Asset health status
- Vibration/temperature trends
- Maintenance schedules
- Alarm history

### 3. Energy Management
- Power consumption
- Peak demand tracking
- Cost analysis
- Efficiency metrics

### 4. Quality Control
- SPC charts
- Defect tracking
- Batch genealogy
- Compliance status

## 🔌 Connecting Your Data

### From Node-RED
Add InfluxDB node and configure:
```javascript
Server: influxdb
Port: 8086
Token: your-influxdb-token
Organization: industrial-iot
Bucket: sensors
```

### From MQTT
Already configured! Topics matching `iiot/+/+/+` are automatically ingested.

### From Ignition
1. Use Ignition's database
2. Or send via MQTT using Cirrus Link modules
3. Or use Ignition's Web Dev module for REST API

## 📱 Mobile Access
1. Grafana is mobile-responsive
2. Pin important dashboards
3. Set up public dashboards for read-only access
4. Use Grafana app for iOS/Android

## 🚨 Setting Up Alerts

### Example: High Temperature Alert
1. Edit panel → Alert tab
2. Create alert condition:
   ```
   WHEN avg() OF query(A, 5m, now) IS ABOVE 80
   ```
3. Configure notification channel (email/slack)
4. Set alert frequency

## 🎯 Industrial Use Cases

### 1. Shift Handover Dashboard
- Previous shift summary
- Active alarms
- Production totals
- Quality issues

### 2. Maintenance Dashboard
- Upcoming maintenance
- Asset runtime hours
- Failure predictions
- Work order status

### 3. Management Overview
- KPI summary
- Cost tracking
- Efficiency trends
- Compliance status

## 🔧 Customization Tips

### Custom Panel for OEE
```sql
SELECT 
  (availability * performance * quality) as oee,
  availability,
  performance,
  quality
FROM oee_metrics
WHERE equipment = '$equipment'
  AND $__timeFilter(time)
```

### Production Counter
```sql
SELECT 
  difference(last(counter)) as production
FROM production_counts
WHERE $__timeFilter(time)
GROUP BY time(1h), equipment
```

## 📈 Performance Optimization

### Data Retention
Configure in InfluxDB:
```bash
# 7 days for raw data
influx bucket update \
  --id YOUR_BUCKET_ID \
  --retention 168h

# Create downsampled bucket for long-term
influx bucket create \
  --name sensors_monthly \
  --retention 8760h
```

### Dashboard Tips
- Use variables for equipment selection
- Limit time ranges for better performance
- Cache dashboard results
- Use table panels sparingly

## 🔐 Security

### Read-Only User
```sql
CREATE USER 'operator' WITH PASSWORD 'password';
GRANT SELECT ON *.* TO 'operator';
```

### Public Dashboards
1. Dashboard settings → Public dashboard
2. Generate public URL
3. No login required for viewing

## 🆘 Troubleshooting

### No Data Showing
1. Check data source connection
2. Verify time range
3. Check InfluxDB is receiving data:
   ```bash
   docker exec -it iiot-influxdb influx query \
     'from(bucket:"sensors") |> range(start: -1h)'
   ```

### Performance Issues
1. Reduce query frequency
2. Add data aggregation
3. Increase Grafana memory:
   ```yaml
   environment:
     - GF_SERVER_ROUTER_LOGGING=true
     - GF_DATABASE_WAL=true
   ```

Ready to visualize your industrial data! 🏭📊