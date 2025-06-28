# 🐳 Docker Containerization - Industrial IoT Stack

**Docker provides containerization** for consistent deployment and scaling of our industrial IoT stack components across development and production environments.

## 🚀 Quick Start for Claude Instances

**New to Docker integration?** Start here:
1. `setup-guides/DOCKER_INSTALLATION_COMMANDS.md` - Installation guide
2. `setup-guides/DOCKER_COMPOSE_GUIDE.md` - Docker Compose workflows
3. `configurations/` - Ready-to-use compose files
4. `docker-configs/` - Service-specific configurations

## 🎯 What Docker Does in Our Stack

### Core Capabilities
- **Consistent Environments**: Identical containers across dev/staging/prod
- **Service Orchestration**: Multi-container application management
- **Resource Management**: CPU and memory allocation control
- **Network Isolation**: Secure inter-service communication

### Key Containerized Services
- **Node-RED**: Flow-based programming environment
- **n8n**: Workflow automation platform
- **MQTT Broker**: Message routing infrastructure
- **Discord Bot**: 24/7 automated task management
- **Database Services**: PostgreSQL, InfluxDB for data storage

## 🏭 Production Features

- **Docker Compose**: Multi-service orchestration
- **Health Checks**: Automatic service monitoring
- **Auto-restart**: Failed container recovery
- **Volume Management**: Persistent data storage
- **Network Security**: Isolated service communication

## 📂 Directory Structure

```
technologies/docker/
├── README.md                    # You are here
├── setup-guides/                # Installation and configuration
├── configurations/              # Docker Compose files
└── docker-configs/              # Service-specific configs
```

## 🔧 Essential Commands

```bash
# Start all services
docker-compose up -d

# View running containers
docker ps

# View logs
docker-compose logs -f [service-name]

# Stop all services
docker-compose down
```

## 🔗 Related Technologies

- **Node-RED**: `../node-red/` - Containerized flow environment
- **n8n**: `../n8n/` - Containerized workflow platform
- **Discord**: `../discord/` - Containerized bot deployment
- **MQTT**: `../mqtt/` - Containerized broker services

---
*Files Organized: 8+ | Technology Status: ✅ Production Ready*