# 🤖 Discord Bot & Claude Workers: Terminal → Production Migration (Ultra-Think)

## 🚨 Current Problem: Terminal Fragility

**Current Reality:**
- Discord Bot: `nohup python3 discord-bot/industrial_iot_claude_bot.py &`
- Mac Claude Worker: Terminal-based polling loop 
- **CRITICAL FLAW**: Both die when laptop closes, terminals end, SSH drops

**What Works Perfectly:**
- Discord → Google Sheets → Claude automation pipeline ✅
- Real-time task creation from iPhone ✅ 
- Automatic task processing ✅
- System monitoring (Docker, MQTT, Node-RED) ✅

## 🎯 Migration Strategy: Three-Tier Approach

### Option A: 🐳 **Docker Production Stack** (RECOMMENDED for Server)

```
┌─────────────────────────────────────────────────────────────┐
│                Production Docker Stack                      │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐ │
│ │  Discord Bot    │  │ Mac Claude      │  │ Server Claude │ │
│ │  Container      │  │ Task Worker     │  │ Task Worker   │ │
│ │                 │  │ Container       │  │ Container     │ │
│ │ • Always-on     │  │                 │  │               │ │
│ │ • Auto-restart  │  │ • Google Sheets │  │ • Google      │ │
│ │ • Health checks │  │ • Auto process  │  │   Sheets      │ │
│ │ • Real-time     │  │ • Never stops   │  │ • Always up   │ │
│ └─────────────────┘  └─────────────────┘  └───────────────┘ │
│                                                             │
│ ┌─────────────────┐  ┌─────────────────┐  ┌───────────────┐ │
│ │ Process Monitor │  │  Log Collector  │  │  Prometheus   │ │
│ │ (Supervisor)    │  │  (Fluentd)      │  │  Metrics      │ │
│ └─────────────────┘  └─────────────────┘  └───────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Option B: 🔧 **PM2 Process Manager** (QUICK WIN)

```bash
# Transform terminal processes into production services
pm2 start discord-bot/industrial_iot_claude_bot.py --name "discord-bot" --interpreter python3
pm2 start scripts/mac_claude_task_worker.py --name "mac-claude-worker" --interpreter python3

# Auto-restart on crash, auto-start on boot
pm2 startup  # Creates systemd service
pm2 save     # Saves current process list
```

### Option C: 🖥️ **Systemd Services** (Linux Production)

```bash
# Create native Linux services
sudo systemctl enable discord-claude-bot.service
sudo systemctl enable mac-claude-worker.service

# Services auto-start on boot, restart on failure
systemctl status discord-claude-bot
```

## 🚀 **IMMEDIATE ACTION PLAN** (24-48 Hours)

### Phase 1: Quick PM2 Migration (2 hours)

**1. Install PM2 on Mac**
```bash
# Install PM2 globally
npm install -g pm2

# Create PM2 ecosystem file
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'discord-claude-bot',
    script: 'discord-bot/industrial_iot_claude_bot.py',
    interpreter: 'python3',
    cwd: '/Users/joshpayneair/Desktop/industrial-iot-stack',
    env: {
      DISCORD_BOT_TOKEN: process.env.DISCORD_BOT_TOKEN,
      PYTHONPATH: '/Users/joshpayneair/Desktop/industrial-iot-stack'
    },
    max_restarts: 10,
    min_uptime: '10s',
    restart_delay: 1000
  }, {
    name: 'mac-claude-worker',
    script: 'scripts/mac_claude_task_worker.py', 
    interpreter: 'python3',
    cwd: '/Users/joshpayneair/Desktop/industrial-iot-stack',
    max_restarts: 10,
    min_uptime: '10s',
    restart_delay: 5000
  }]
};
EOF

# Start services
pm2 start ecosystem.config.js

# Setup auto-start on Mac login
pm2 startup launchd
pm2 save
```

**2. Add Health Monitoring**
```python
# Add to both scripts - simple health endpoint
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        health_data = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": time.time() - start_time
        }
        self.wfile.write(json.dumps(health_data).encode())

def start_health_server(port):
    server = HTTPServer(('localhost', port), HealthHandler)
    health_thread = threading.Thread(target=server.serve_forever, daemon=True)
    health_thread.start()
    return server

# Add to main() in both scripts
start_health_server(8080)  # Discord bot
start_health_server(8081)  # Mac Claude worker
```

**3. Enhanced Logging**
```python
# Replace basic logging with structured logging
import logging
import sys
from datetime import datetime

def setup_logging(service_name):
    logging.basicConfig(
        level=logging.INFO,
        format=f'[{service_name}] %(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'/Users/joshpayneair/Desktop/industrial-iot-stack/logs/{service_name}.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(service_name)

# Usage in each script
logger = setup_logging('discord-claude-bot')  # or 'mac-claude-worker'
```

### Phase 2: Server Migration (1-2 days)

**1. Server Setup with Docker**
```bash
# SSH to server
ssh user@server

# Create project directory
mkdir -p /opt/industrial-iot-stack
cd /opt/industrial-iot-stack

# Copy essential files
scp -r discord-bot/ scripts/ credentials/ user@server:/opt/industrial-iot-stack/
```

**2. Production Docker Compose**
```yaml
# File: docker-compose.production.yml
version: '3.8'

services:
  discord-bot:
    build: 
      context: ./discord-bot
      dockerfile: Dockerfile.production
    environment:
      - DISCORD_BOT_TOKEN=${DISCORD_BOT_TOKEN}
    volumes:
      - ./credentials:/app/credentials:ro
      - ./logs:/app/logs
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - iot-stack

  mac-claude-worker:
    build:
      context: ./scripts
      dockerfile: Dockerfile.worker
    environment:
      - WORKER_NAME=Mac Claude
    volumes:
      - ./credentials:/app/credentials:ro
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - iot-stack

  server-claude-worker:
    build:
      context: ./scripts
      dockerfile: Dockerfile.worker
    environment:
      - WORKER_NAME=Server Claude
    volumes:
      - ./credentials:/app/credentials:ro
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8082/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - iot-stack

  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=3600
    restart: unless-stopped

volumes:
  logs:

networks:
  iot-stack:
    driver: bridge
```

**3. Production Dockerfiles**
```dockerfile
# File: discord-bot/Dockerfile.production
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py ./
COPY credentials/ ./credentials/

# Create logs directory
RUN mkdir -p logs

# Health check endpoint
EXPOSE 8080

# Run application
CMD ["python3", "industrial_iot_claude_bot.py"]
```

```dockerfile
# File: scripts/Dockerfile.worker
FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *claude_task_worker.py ./
COPY credentials/ ./credentials/

RUN mkdir -p logs

# Health check endpoints
EXPOSE 8081 8082

CMD ["python3", "mac_claude_task_worker.py"]
```

### Phase 3: Advanced Monitoring (2-3 days)

**1. Monitoring Stack**
```yaml
# File: monitoring/docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    networks:
      - iot-stack

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/datasources:/etc/grafana/provisioning/datasources
    networks:
      - iot-stack

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
    networks:
      - iot-stack

volumes:
  prometheus_data:
  grafana_data:

networks:
  iot-stack:
    external: true
```

**2. Prometheus Configuration**
```yaml
# File: monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'discord-bot'
    static_configs:
      - targets: ['discord-bot:8080']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'claude-workers'
    static_configs:
      - targets: ['mac-claude-worker:8081', 'server-claude-worker:8082']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

## 🎛️ **Deployment Commands**

### Immediate PM2 Deployment (TODAY)
```bash
# Stop current terminal processes
killall python3  # Or more selective process killing

# Install and start PM2 services
npm install -g pm2
cd /Users/joshpayneair/Desktop/industrial-iot-stack
pm2 start ecosystem.config.js

# Verify services running
pm2 status
pm2 logs

# Setup auto-start
pm2 startup
pm2 save

# Test health endpoints
curl http://localhost:8080/health  # Discord bot
curl http://localhost:8081/health  # Mac Claude worker
```

### Server Production Deployment (WITHIN WEEK)
```bash
# Deploy to server
scp -r * user@server:/opt/industrial-iot-stack/
ssh user@server

# Create network and deploy
docker network create iot-stack
cd /opt/industrial-iot-stack
export DISCORD_BOT_TOKEN="your_token"
export GRAFANA_PASSWORD="secure_password"

# Start production stack
docker-compose -f docker-compose.production.yml up -d

# Monitor deployment
docker-compose -f docker-compose.production.yml logs -f
docker-compose -f docker-compose.production.yml ps

# Start monitoring
cd monitoring
docker-compose up -d
```

## 📊 **Success Metrics & Monitoring**

### Health Check Dashboard
```bash
# Quick status check script
#!/bin/bash
echo "=== Discord Bot & Claude Workers Status ==="
echo "Discord Bot Health: $(curl -s http://localhost:8080/health | jq -r .status)"
echo "Mac Claude Worker Health: $(curl -s http://localhost:8081/health | jq -r .status)"
echo "Tasks Processed Today: $(curl -s http://localhost:8081/metrics | grep tasks_processed)"
echo "PM2 Status:"
pm2 status --no-color
```

### Grafana Dashboard Panels
- **Service Uptime**: 99.9% target
- **Task Processing Rate**: Real-time task completion
- **Error Rate**: < 1% failed tasks
- **Response Time**: Health check latency
- **Resource Usage**: CPU/Memory per service

### Alerting Rules
```yaml
# File: monitoring/alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'

route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'discord-webhook'

receivers:
- name: 'discord-webhook'
  webhook_configs:
  - url: 'DISCORD_WEBHOOK_URL'
    send_resolved: true
```

## 🔒 **Security & Best Practices**

### Environment Variables
```bash
# File: .env.production
DISCORD_BOT_TOKEN=your_actual_token
GRAFANA_PASSWORD=secure_random_password
GOOGLE_SHEETS_CREDS_PATH=/app/credentials/iot-stack-credentials.json

# Docker secrets (more secure)
echo "your_discord_token" | docker secret create discord_token -
```

### Backup Strategy
```bash
#!/bin/bash
# File: scripts/backup_claude_services.sh

# Backup logs
tar -czf "/backups/claude_logs_$(date +%Y%m%d).tar.gz" logs/

# Backup Google Sheets data (via API)
python3 scripts/backup_sheets_data.py

# Backup Docker volumes
docker run --rm -v iot-stack_logs:/data -v $(pwd)/backups:/backup alpine tar czf /backup/docker_logs_$(date +%Y%m%d).tar.gz /data
```

## 🎯 **Migration Timeline**

### ✅ TODAY (2 hours)
- [ ] Install PM2 and migrate from terminal processes
- [ ] Add health check endpoints  
- [ ] Setup logging and monitoring
- [ ] Test task creation → processing pipeline

### 📅 THIS WEEK (3 days)
- [ ] Create production Dockerfiles
- [ ] Deploy to server with Docker Compose
- [ ] Setup monitoring stack (Prometheus + Grafana)
- [ ] Configure alerting for service failures

### 🚀 NEXT WEEK (2 days) 
- [ ] Performance optimization and resource tuning
- [ ] Backup and disaster recovery procedures
- [ ] Documentation for team handoff
- [ ] Load testing and scalability analysis

## 💎 **Business Impact**

### Reliability Benefits
- **99.9% Uptime**: Services run continuously regardless of laptop state
- **Automatic Recovery**: Failed services restart within 30 seconds
- **Zero Manual Intervention**: No more checking if bot is running

### Productivity Benefits  
- **Mobile Task Creation**: Create tasks from iPhone anytime via Discord
- **Guaranteed Processing**: Tasks are never missed due to service downtime
- **Real-time Monitoring**: Know immediately if something goes wrong

### Scalability Benefits
- **Multi-Worker Support**: Can scale to multiple Claude workers
- **Load Distribution**: Distribute tasks across multiple instances
- **Resource Optimization**: Right-size containers for workload

## 🏁 **DECISION POINT**

**Recommendation**: Start with **PM2 migration TODAY** (2-hour effort) for immediate reliability, then move to **Docker production deployment THIS WEEK** for maximum robustness.

This gives you:
1. **Immediate relief** from terminal fragility 
2. **Production-grade infrastructure** within days
3. **Monitoring and alerting** for operational excellence
4. **Scalable foundation** for future growth

**Next Action**: Run the PM2 setup commands above to eliminate terminal dependency in the next 2 hours.