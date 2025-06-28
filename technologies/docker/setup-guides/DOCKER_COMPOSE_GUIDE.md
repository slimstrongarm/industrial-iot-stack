# Docker Compose Guide - Industrial IoT Stack

## Overview
This guide covers the comprehensive Docker Compose setup for the Industrial IoT stack, including migration from individual containers to a unified compose environment.

## Important: Docker Wrapper Integration
⚠️ **This setup uses system-wide Docker wrappers** to resolve conflicts between Docker Desktop's WSL integration and Claude Code. Ensure the wrappers are installed before proceeding.

### Docker Wrapper Status
- ✅ System-wide `docker` command available
- ✅ System-wide `docker-compose` command available  
- ✅ Compatible with automation scripts and CI/CD
- ✅ No WSL integration conflicts with Claude Code

## Current Architecture

### Core Services
1. **EMQX MQTT Broker** (`emqxnodec`)
   - Ports: 1883 (MQTT), 8883 (MQTT/SSL), 18083 (Dashboard)
   - Custom image: `emqxnodei`
   - Status: ✅ Running and verified

2. **TimescaleDB** (`timescaledb`)
   - Port: 5432
   - Image: `timescale/timescaledb:latest-pg17`
   - Purpose: Time-series data storage

3. **Node-RED** (`nodered`)
   - Port: 1880
   - Image: `nodered/node-red:latest`
   - Status: Healthy

4. **Ignition Gateway** (Reference)
   - Port: 8088
   - Purpose: Flint detection/integration

### Optional Services (Profiles)
- **PgAdmin**: Database administration (port 5050)
- **Grafana**: Monitoring and visualization (port 3000)

## File Structure
```
├── docker-compose.yml                    # Current (Ignition reference only)
├── docker-compose-comprehensive.yml      # New comprehensive setup
└── scripts/
    └── migrate-to-comprehensive-compose.sh # Migration script
```

## Migration Options

### Option 1: Test Migration (Recommended First)
Test the comprehensive setup alongside existing services:
```bash
./scripts/migrate-to-comprehensive-compose.sh
# Choose option 1: Test migration
```

This creates temporary services on alternate ports:
- EMQX Dashboard: http://localhost:18084
- Node-RED: http://localhost:1881
- TimescaleDB: localhost:5433

### Option 2: Full Migration
Replace current setup with comprehensive compose:
```bash
./scripts/migrate-to-comprehensive-compose.sh
# Choose option 2: Full migration
```

**Note**: This preserves all data through Docker volumes.

## Manual Commands

### Start All Core Services
```bash
docker-compose -f docker-compose-comprehensive.yml up -d
```

### Include Admin Tools
```bash
docker-compose -f docker-compose-comprehensive.yml --profile admin-tools up -d
```

### Include Monitoring
```bash
docker-compose -f docker-compose-comprehensive.yml --profile monitoring up -d
```

### Start Everything
```bash
docker-compose -f docker-compose-comprehensive.yml --profile admin-tools --profile monitoring up -d
```

## Service Access Points

### Production Services
- **EMQX Dashboard**: http://localhost:18083
- **Node-RED**: http://localhost:1880
- **Ignition Gateway**: http://localhost:8088
- **TimescaleDB**: localhost:5432

### Admin Tools (Optional)
- **PgAdmin**: http://localhost:5050
  - Email: admin@iot.local
  - Password: admin

### Monitoring (Optional)
- **Grafana**: http://localhost:3000
  - Username: admin
  - Password: admin

## Data Persistence
All services use named Docker volumes for data persistence:
- `emqx-data`, `emqx-etc`, `emqx-log`: EMQX configuration and logs
- `timescale-data`: Database storage
- `nodered-data`: Node-RED flows and configuration
- `ignition-data`: Ignition gateway data
- `pgadmin-data`: PgAdmin settings
- `grafana-data`: Grafana dashboards and settings

## Network Configuration
- **Network**: `iiot-network` (172.20.0.0/16)
- **Driver**: Bridge
- **Inter-service communication**: Enabled via service names

## Troubleshooting

### Docker Command Issues
If Docker commands fail, verify wrapper installation:
```bash
which docker
docker --version
which docker-compose
```

### Service Connectivity
Check if services can communicate:
```bash
docker-compose exec nodered ping emqx
docker-compose exec nodered ping timescaledb
```

### View Logs
```bash
docker-compose logs -f [service-name]
```

### Check Service Status
```bash
docker-compose ps
```

## Backup and Recovery
The migration script automatically creates backups in `backups/migration-YYYYMMDD_HHMMSS/` including:
- Original docker-compose.yml
- Container configurations
- Current state documentation

## Implementation Status
- **CT-001**: ✅ Docker audit complete
- **CT-002**: ✅ EMQX configuration verified
- **CT-003**: ✅ Comprehensive docker-compose.yml created
- **CT-004**: ⏳ MQTT integration testing pending

## Created By
- **Date**: June 3, 2025
- **Author**: server-claude via Claude Code
- **Dependencies**: System-wide Docker wrappers