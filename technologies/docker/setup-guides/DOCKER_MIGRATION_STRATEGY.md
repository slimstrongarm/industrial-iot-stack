# Docker Migration Strategy - Industrial IoT Stack

## 🎯 Strategic Overview
Migrating from local Ignition setup to Docker-based deployment on dedicated server infrastructure. This approach enables modular, scalable architecture suitable for multi-enterprise deployment.

## 🏗️ Modular Technology Stack Architecture

```
industrial-iot-stack/
├── docker-stacks/
│   ├── ignition-flint/           # Ignition + Flint module
│   │   ├── docker-compose.yml
│   │   ├── .env
│   │   └── volumes/
│   │       ├── projects/
│   │       ├── modules/
│   │       └── data/
│   ├── node-red-flows/           # Node-RED automation
│   │   ├── docker-compose.yml
│   │   └── volumes/
│   ├── mqtt-infrastructure/      # MQTT broker stack
│   │   ├── docker-compose.yml
│   │   └── volumes/
│   ├── databases/                # Time-series DBs
│   │   ├── docker-compose.yml
│   │   └── volumes/
│   └── monitoring/               # System visibility
│       ├── docker-compose.yml
│       └── volumes/
```

## 📦 Phase 1: Docker Compose Configuration

### Ignition + Flint Stack (`docker-stacks/ignition-flint/docker-compose.yml`)

```yaml
version: '3.8'

services:
  ignition:
    image: inductiveautomation/ignition:8.1.43
    container_name: ignition-gateway
    ports:
      - "8088:8088"      # Gateway web interface
      - "8043:8043"      # Gateway SSL
      - "8060:8060"      # Vision Client
      - "62541:62541"    # OPC-UA
    volumes:
      - ./volumes/data:/usr/local/bin/ignition/data
      - ./volumes/modules:/usr/local/bin/ignition/user-lib/modules
      - ./volumes/projects:/usr/local/bin/ignition/data/projects
      - ./volumes/backups:/backups
    environment:
      - ACCEPT_IGNITION_EULA=Y
      - GATEWAY_ADMIN_USERNAME=${GATEWAY_ADMIN_USERNAME:-admin}
      - GATEWAY_ADMIN_PASSWORD=${GATEWAY_ADMIN_PASSWORD:-password}
      - IGNITION_EDITION=edge
      - TZ=${TIMEZONE:-America/New_York}
    restart: unless-stopped
    networks:
      - iot-stack
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8088/StatusPing"]
      interval: 30s
      timeout: 10s
      retries: 5
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ignition.rule=Host(`ignition.${DOMAIN}`)"
      - "com.centurylinklabs.watchtower.enable=false"

  # Flint module will be installed via volume mount
  # Keith Gamble's module: ignition-project-scan-endpoint.modl

networks:
  iot-stack:
    external: true
```

### Environment Configuration (`.env`)
```bash
# Gateway Configuration
GATEWAY_ADMIN_USERNAME=admin
GATEWAY_ADMIN_PASSWORD=SecurePassword123!
DOMAIN=iot.company.com
TIMEZONE=America/New_York

# Tailscale Integration
TAILSCALE_IP=100.x.x.x
TAILSCALE_HOSTNAME=iot-server

# Module Versions
FLINT_MODULE_VERSION=1.0.0
MQTT_ENGINE_VERSION=4.0.20
```

## 🚀 Phase 2: Server Setup Commands

### SSH + TMUX Session Management
```bash
#!/bin/bash
# File: scripts/server-setup.sh

# Connect via Tailscale
echo "Connecting to IoT Server via Tailscale..."
ssh username@${TAILSCALE_IP}

# Create persistent TMUX session
tmux new-session -s iot-stack -d

# Create window layout for monitoring
tmux rename-window 'IoT Stack'
tmux split-window -h -p 50
tmux split-window -v -p 30
tmux select-pane -t 0
tmux split-window -v -p 30

# Assign panes
# Pane 0: Docker logs for Ignition
# Pane 1: System monitoring
# Pane 2: Docker compose status
# Pane 3: Interactive shell

# Attach to session
tmux attach-session -t iot-stack
```

### TMUX Pane Commands
```bash
# Pane 0: Monitor Ignition logs
docker logs -f ignition-gateway --tail 100

# Pane 1: System monitoring
htop || top

# Pane 2: Docker status
watch -n 5 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'

# Pane 3: Interactive shell for management
```

## 📊 Phase 3: System Visibility Dashboard

### Docker-based Monitoring Stack
```yaml
# docker-stacks/monitoring/docker-compose.yml
version: '3.8'

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped
    networks:
      - iot-stack

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana
      - ./dashboards:/etc/grafana/provisioning/dashboards
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    restart: unless-stopped
    networks:
      - iot-stack

volumes:
  portainer_data:
  grafana_data:

networks:
  iot-stack:
    external: true
```

## 🔄 Phase 4: Project Migration Workflow

### Export Projects from Local Ignition
```python
#!/usr/bin/env python3
# File: scripts/export_projects.py

import requests
import json
import os
from datetime import datetime

GATEWAY_URL = "http://localhost:8088"
AUTH = ("admin", "password")
EXPORT_DIR = "./project_exports"

def export_all_projects():
    """Export all projects from local Ignition"""
    os.makedirs(EXPORT_DIR, exist_ok=True)
    
    # Get project list
    response = requests.get(
        f"{GATEWAY_URL}/data/project-management/projects",
        auth=AUTH
    )
    projects = response.json()
    
    for project in projects:
        project_name = project['name']
        print(f"Exporting {project_name}...")
        
        # Export project
        export_response = requests.post(
            f"{GATEWAY_URL}/data/project-management/export",
            json={"projectName": project_name},
            auth=AUTH
        )
        
        # Save export
        filename = f"{EXPORT_DIR}/{project_name}_{datetime.now().strftime('%Y%m%d')}.zip"
        with open(filename, 'wb') as f:
            f.write(export_response.content)
        
        print(f"✓ Exported to {filename}")

if __name__ == "__main__":
    export_all_projects()
```

### Import Projects to Docker Ignition
```bash
#!/bin/bash
# File: scripts/import_to_docker.sh

# Copy exports to server
scp -r ./project_exports username@${TAILSCALE_IP}:/tmp/

# SSH and import
ssh username@${TAILSCALE_IP} << 'EOF'
# Copy to Docker volume
docker cp /tmp/project_exports ignition-gateway:/imports/

# Import each project via API
docker exec ignition-gateway python3 << 'PYTHON'
import requests
import os

for file in os.listdir('/imports'):
    if file.endswith('.zip'):
        print(f"Importing {file}")
        # Import logic here
PYTHON
EOF
```

## 🧩 Modular Integration Points

### Inter-Stack Communication
```yaml
# docker-stacks/docker-compose.override.yml
# Defines shared networks and volumes

networks:
  iot-stack:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  shared-data:
    driver: local
  mqtt-data:
    driver: local
```

### Service Discovery
Each stack can discover others via Docker DNS:
- `ignition-gateway.iot-stack`
- `node-red.iot-stack`
- `mqtt-broker.iot-stack`

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Verify Docker and Docker Compose installed on server
- [ ] Confirm Tailscale connection working
- [ ] Export all 8-9 projects from local Ignition
- [ ] Download Flint module (.modl file)
- [ ] Create directory structure on server

### Deployment Steps
- [ ] Create Docker network: `docker network create iot-stack`
- [ ] Deploy Ignition stack
- [ ] Install Flint module via volume mount
- [ ] Import projects
- [ ] Configure MQTT Engine module
- [ ] Test VS Code Flint connection
- [ ] Deploy monitoring stack
- [ ] Verify all services healthy

### Post-Deployment
- [ ] Document access procedures
- [ ] Create backup strategy
- [ ] Set up automated health checks
- [ ] Configure alerts for service failures
- [ ] Test project deployment workflow

## 🔐 Security Considerations

### Network Security
- All services behind Tailscale VPN
- No direct internet exposure
- Service-to-service communication on internal network

### Access Control
- Unique passwords per service
- API keys for service communication
- Role-based access in Ignition

### Data Protection
- Regular automated backups
- Encrypted volumes for sensitive data
- Audit logging enabled

## 📚 Agent Documentation

### For MacBook Claude (Strategic Coordinator)
- Review Docker Compose files
- Plan network architecture
- Design backup strategies
- Coordinate troubleshooting

### For Server Claude Code (Implementation)
- Execute Docker commands
- Monitor service health
- Troubleshoot connectivity
- Optimize performance

### SSH/TMUX Quick Reference
```bash
# Connect to server
ssh user@tailscale-ip

# List TMUX sessions
tmux ls

# Attach to IoT session
tmux attach -t iot-stack

# Detach from session
Ctrl+b, d

# Switch panes
Ctrl+b, arrow keys

# Create new window
Ctrl+b, c

# Switch windows
Ctrl+b, n (next)
Ctrl+b, p (previous)
```

## 🎯 Success Metrics

### Technical Success
- All containers running with health checks passing
- Flint extension connects and shows tag tree
- Projects accessible and editable via VS Code
- MQTT data flowing between services

### Business Success
- Modular architecture supports multi-tenant deployment
- Easy to replicate for new customers
- Clear documentation for team onboarding
- Scalable to enterprise requirements

---

**Next Step**: Begin with creating the Docker Compose configuration and testing on your server via Tailscale SSH connection.