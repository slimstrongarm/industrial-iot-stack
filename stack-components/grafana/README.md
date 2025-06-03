# Grafana - Industrial IoT Visualization Platform

## Overview
Grafana is an open-source analytics and interactive visualization platform. In our Industrial IoT stack, Grafana provides real-time dashboards, historical trending, and alerting for all operational data.

## Why Grafana for Industrial IoT?

### Perfect Fit Because:
- **Real-time Dashboards**: Live production metrics
- **Time-series Visualization**: Ideal for sensor data
- **Multi-source Support**: Combine data from Ignition, MQTT, databases
- **Alerting**: Visual and notification-based alerts
- **Mobile Responsive**: Operators can view on tablets/phones
- **Custom Plugins**: Extend for industrial-specific needs

## Role in IIoT Stack
```
[Ignition] ──┐
[Node-RED] ──┼──► [Time Series DB] ──► [Grafana] ──► [Operators]
[MQTT]     ──┘                                        [Managers]
[n8n]      ──────► [PostgreSQL]    ──┘                [Maintenance]
```

## Key Features for Industrial Use

### 1. Production Dashboards
- **OEE Monitoring**: Availability, Performance, Quality
- **Production Counts**: Real-time vs targets
- **Downtime Tracking**: Reason codes and duration
- **Shift Performance**: Comparative analysis

### 2. Equipment Monitoring
- **Asset Health**: Temperature, vibration, pressure
- **Predictive Maintenance**: Trend analysis
- **Alarm History**: Frequency and patterns
- **Energy Consumption**: Real-time and historical

### 3. Quality Metrics
- **SPC Charts**: Control limits and violations
- **Batch Tracking**: Product genealogy
- **Defect Analysis**: Pareto charts
- **Compliance Reporting**: Regulatory requirements

### 4. Utility Monitoring
- **Power Usage**: Peak demand tracking
- **Water/Gas/Air**: Consumption patterns
- **Environmental**: Temperature, humidity
- **Cost Analysis**: Resource optimization

## Data Sources Configuration

### 1. InfluxDB (Time Series)
Primary source for real-time sensor data
```yaml
- type: influxdb
  access: proxy
  url: http://influxdb:8086
  database: industrial_iot
```

### 2. PostgreSQL (Ignition)
Historical data and batch records
```yaml
- type: postgres
  access: proxy
  url: postgres:5432
  database: ignition
```

### 3. MQTT (Live Data)
Real-time streaming via MQTT plugin
```yaml
- type: mqtt-datasource
  mqttServer: tcp://mqtt-broker:1883
  topics:
    - iiot/+/+/+
```

### 4. Prometheus (Metrics)
System and application metrics
```yaml
- type: prometheus
  access: proxy
  url: http://prometheus:9090
```

## Docker Deployment

```yaml
# Grafana service configuration
grafana:
  image: grafana/grafana:10.3.1
  container_name: iiot-grafana
  ports:
    - "3000:3000"
  environment:
    - GF_SECURITY_ADMIN_USER=${GRAFANA_USER:-admin}
    - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    - GF_INSTALL_PLUGINS=grafana-mqtt-datasource,grafana-worldmap-panel,grafana-clock-panel,grafana-piechart-panel
    - GF_SERVER_ROOT_URL=https://grafana.${DOMAIN}
    - GF_SMTP_ENABLED=true
    - GF_SMTP_HOST=${SMTP_HOST}:${SMTP_PORT}
    - GF_SMTP_USER=${SMTP_USER}
    - GF_SMTP_PASSWORD=${SMTP_PASSWORD}
  volumes:
    - grafana_data:/var/lib/grafana
    - ./grafana/provisioning:/etc/grafana/provisioning
    - ./grafana/dashboards:/var/lib/grafana/dashboards
  depends_on:
    - influxdb
    - postgres
  networks:
    - iiot-network
  restart: unless-stopped

# InfluxDB for time-series data
influxdb:
  image: influxdb:2.7-alpine
  container_name: iiot-influxdb
  ports:
    - "8086:8086"
  environment:
    - DOCKER_INFLUXDB_INIT_MODE=setup
    - DOCKER_INFLUXDB_INIT_USERNAME=${INFLUXDB_USER:-admin}
    - DOCKER_INFLUXDB_INIT_PASSWORD=${INFLUXDB_PASSWORD}
    - DOCKER_INFLUXDB_INIT_ORG=industrial-iot
    - DOCKER_INFLUXDB_INIT_BUCKET=sensors
    - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=${INFLUXDB_TOKEN}
  volumes:
    - influxdb_data:/var/lib/influxdb2
    - influxdb_config:/etc/influxdb2
  networks:
    - iiot-network
  restart: unless-stopped

volumes:
  grafana_data:
  influxdb_data:
  influxdb_config:
```

## Industrial Dashboard Templates

### 1. Production Overview
- Current production rate
- Shift targets vs actuals
- Quality metrics
- Downtime events

### 2. Equipment Status
- Real-time equipment states
- Alarm status grid
- Maintenance schedules
- Performance trends

### 3. Energy Management
- Real-time consumption
- Cost tracking
- Peak demand alerts
- Efficiency metrics

### 4. Quality Control
- SPC charts
- Defect tracking
- Batch genealogy
- Compliance status

## Integration Examples

### From Node-RED to InfluxDB
```javascript
// Node-RED function to send to InfluxDB
msg.payload = [{
    measurement: "temperature",
    tags: {
        equipment: "TANK-01",
        area: "Brewing"
    },
    fields: {
        value: msg.payload.temperature,
        setpoint: msg.payload.setpoint
    },
    timestamp: new Date()
}];
return msg;
```

### From MQTT to Grafana
```javascript
// MQTT topic structure
iiot/brewery/fermentation/TANK-01/temperature
// Grafana query
SELECT mean("value") FROM "temperature" WHERE "equipment" = 'TANK-01'
```

## Security Considerations
- HTTPS enforcement
- LDAP/AD integration available
- Role-based access control
- API key management
- Audit logging

## Performance Optimization
- Data retention policies
- Query caching
- Dashboard refresh rates
- Aggregation strategies
- Index optimization

## Next Steps
1. Deploy Grafana container
2. Configure data sources
3. Import industrial dashboards
4. Set up alerting rules
5. Create custom visualizations
6. Train operators on usage