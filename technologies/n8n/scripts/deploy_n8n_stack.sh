#!/bin/bash
<<<<<<< HEAD
# Deploy complete n8n stack with PostgreSQL backend
# CT-006: n8n Deployment Script

echo "🚀 Deploying n8n Stack with PostgreSQL Backend"
echo "==============================================="
echo ""

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Ensure system-wide Docker wrappers are installed."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Ensure system-wide Docker wrappers are installed."
    exit 1
fi

echo "✅ Docker and Docker Compose available"
echo ""

# Create n8n-specific docker-compose file
echo "📝 Creating n8n PostgreSQL stack configuration..."

cat > docker-compose-n8n-stack.yml << 'EOF'
version: '3.8'

services:
  # PostgreSQL database for n8n
  n8n-postgres:
    image: postgres:15
    container_name: n8n-postgres
    restart: unless-stopped
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n_user
      - POSTGRES_PASSWORD=n8n_password
      - POSTGRES_NON_ROOT_USER=n8n_user
      - POSTGRES_NON_ROOT_PASSWORD=n8n_password
    volumes:
      - n8n-postgres-data:/var/lib/postgresql/data
    networks:
      - n8n-network
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U n8n_user -d n8n']
      interval: 5s
      timeout: 5s
      retries: 10

  # n8n workflow automation with PostgreSQL backend
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      # Database Configuration
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=n8n-postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n_user
      - DB_POSTGRESDB_PASSWORD=n8n_password
      
      # Basic Auth
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin
      
      # Server Configuration
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
      
      # Timezone and Misc
      - GENERIC_TIMEZONE=America/New_York
      - N8N_METRICS=true
      - N8N_LOG_LEVEL=info
      
      # Workflow Configuration
      - WORKFLOWS_DEFAULT_NAME=IoT Workflow
      - N8N_DEFAULT_BINARY_DATA_MODE=filesystem
      
      # External Services Integration
      - N8N_AVAILABLE_BINARY_DATA_MODES=default,s3
      
    volumes:
      - n8n-data:/home/node/.n8n
      - n8n-workflows:/home/node/.n8n/workflows
    networks:
      - n8n-network
      - iiot-network  # Connect to main IoT network for MQTT access
    depends_on:
      n8n-postgres:
        condition: service_healthy

networks:
  n8n-network:
    driver: bridge
  iiot-network:
    external: true
    name: industrial-iot-stack_iiot-network

volumes:
  n8n-postgres-data:
    driver: local
  n8n-data:
    driver: local
  n8n-workflows:
    driver: local
EOF

echo "✅ n8n stack configuration created"
echo ""

# Check if IoT network exists, create if needed
echo "🔗 Checking IoT network connectivity..."
if ! docker network ls | grep -q "industrial-iot-stack_iiot-network"; then
    echo "⚠️  IoT network not found, creating basic network..."
    docker network create iiot-network
    NETWORK_NAME="iiot-network"
else
    NETWORK_NAME="industrial-iot-stack_iiot-network"
    echo "✅ IoT network found: $NETWORK_NAME"
fi

# Update the compose file with correct network name
sed -i "s/industrial-iot-stack_iiot-network/$NETWORK_NAME/g" docker-compose-n8n-stack.yml

echo ""

# Start the n8n stack
echo "🚀 Starting n8n PostgreSQL stack..."
docker-compose -f docker-compose-n8n-stack.yml up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check service status
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose-n8n-stack.yml ps

# Test connectivity
echo ""
echo "🧪 Testing Service Connectivity..."

# Test PostgreSQL
if docker exec n8n-postgres pg_isready -U n8n_user -d n8n > /dev/null 2>&1; then
    echo "✅ PostgreSQL database ready"
else
    echo "❌ PostgreSQL database not ready"
fi

# Test n8n
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5678 | grep -q "200\|401"; then
    echo "✅ n8n web interface accessible"
else
    echo "⚠️  n8n web interface not ready yet (may need more time)"
fi

# Test EMQX connectivity from n8n
if docker ps | grep -q emqxnodec; then
    if docker exec n8n ping -c 1 emqxnodec > /dev/null 2>&1; then
        echo "✅ n8n can reach EMQX broker"
    else
        echo "⚠️  n8n cannot reach EMQX broker (network issue)"
    fi
else
    echo "⚠️  EMQX broker not running"
fi

echo ""
echo "🎉 n8n PostgreSQL Stack Deployment Complete!"
echo "============================================"
echo ""
echo "📊 Access Points:"
echo "  • n8n Interface: http://localhost:5678"
echo "  • Username: admin"
echo "  • Password: admin"
echo "  • Database: PostgreSQL (n8n database)"
echo ""
echo "🔧 Stack Components:"
echo "  • n8n: Workflow automation platform"
echo "  • PostgreSQL: Persistent workflow and execution data"
echo "  • Networks: Connected to IoT network for MQTT integration"
echo ""
echo "📋 Next Steps:"
echo "  1. Access n8n at http://localhost:5678"
echo "  2. Import workflows (CT-007)"
echo "  3. Test MQTT→WhatsApp integration (CT-008)"
echo ""
echo "🔍 Useful Commands:"
echo "  • View logs: docker-compose -f docker-compose-n8n-stack.yml logs -f"
echo "  • Restart: docker-compose -f docker-compose-n8n-stack.yml restart"
echo "  • Stop: docker-compose -f docker-compose-n8n-stack.yml down"
=======

# n8n Deployment Script for Industrial IoT Stack
# This script deploys n8n as part of the Docker stack

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCKER_CONFIG_DIR="$PROJECT_ROOT/docker-configs"
CREDENTIALS_DIR="$PROJECT_ROOT/credentials"

echo -e "${BLUE}🚀 Industrial IoT Stack - n8n Deployment${NC}"
echo "=================================================="

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
echo -e "\n${BLUE}Checking prerequisites...${NC}"

# Check Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed or not in PATH"
    exit 1
fi
print_status "Docker is available"

# Check Docker Compose
if ! docker compose version &> /dev/null; then
    print_error "Docker Compose is not available"
    exit 1
fi
print_status "Docker Compose is available"

# Check if we're in the right directory
if [[ ! -f "$PROJECT_ROOT/STACK-OVERVIEW.md" ]]; then
    print_error "Script must be run from the industrial-iot-stack project"
    exit 1
fi
print_status "Project directory confirmed"

# Check credentials
if [[ ! -f "$CREDENTIALS_DIR/iot-stack-credentials.json" ]]; then
    print_warning "Google Sheets credentials not found at $CREDENTIALS_DIR/iot-stack-credentials.json"
    echo "  You'll need to configure Google Sheets integration manually"
else
    print_status "Google Sheets credentials found"
fi

# Create environment file if it doesn't exist
ENV_FILE="$DOCKER_CONFIG_DIR/.env"
if [[ ! -f "$ENV_FILE" ]]; then
    echo -e "\n${BLUE}Creating environment file...${NC}"
    cat > "$ENV_FILE" << EOF
# n8n Configuration
N8N_PASSWORD=StrongPassword123!

# PostgreSQL Database Configuration
POSTGRES_PASSWORD=n8n_secure_$(openssl rand -hex 8)

# WhatsApp Business API Configuration (for MQTT alerts)
# WHATSAPP_ACCESS_TOKEN=your_permanent_access_token
# WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
# DEFAULT_ALERT_PHONE=+1234567890

# Email Configuration (optional)
# SMTP_USER=your-email@domain.com
# SMTP_PASS=your-app-password

# Domain Configuration (for production)
# DOMAIN=yourdomain.com
EOF
    print_status "Environment file created at $ENV_FILE"
    print_warning "Please review and update the environment variables in $ENV_FILE"
    print_warning "Don't forget to configure WhatsApp credentials for MQTT alerts!"
else
    print_status "Environment file already exists"
fi

# Create workflows directory if it doesn't exist
WORKFLOWS_DIR="$PROJECT_ROOT/n8n-workflows"
if [[ ! -d "$WORKFLOWS_DIR" ]]; then
    mkdir -p "$WORKFLOWS_DIR"
    print_status "Created n8n-workflows directory"
fi

# Deploy n8n stack
echo -e "\n${BLUE}Deploying n8n stack (n8n + PostgreSQL)...${NC}"
cd "$DOCKER_CONFIG_DIR"

# Pull the latest images
docker pull n8nio/n8n:latest
docker pull postgres:15-alpine
print_status "Container images updated"

# Start the stack
if docker compose -f docker-compose-n8n.yml up -d; then
    print_status "n8n stack deployed successfully (n8n + PostgreSQL)"
else
    print_error "Failed to deploy n8n stack"
    exit 1
fi

# Wait for n8n to be ready
echo -e "\n${BLUE}Waiting for n8n to start...${NC}"
for i in {1..30}; do
    if curl -s http://localhost:5678/healthz > /dev/null 2>&1; then
        print_status "n8n is ready!"
        break
    fi
    echo -n "."
    sleep 2
done

if ! curl -s http://localhost:5678/healthz > /dev/null 2>&1; then
    print_warning "n8n may not be fully ready yet. Check logs with: docker logs iiot-n8n"
fi

# Display connection info
echo -e "\n${GREEN}🎉 n8n Deployment Complete!${NC}"
echo "=============================================="
echo -e "📍 Access URL: ${BLUE}http://localhost:5678${NC}"
echo -e "👤 Username:   ${BLUE}iiot-admin${NC}"
echo -e "🔑 Password:   ${BLUE}StrongPassword123!${NC} (or from .env file)"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Open http://localhost:5678 in your browser"
echo "2. Log in with the credentials above"
echo "3. Go to Settings → Credentials to configure Google Sheets"
echo "4. Import workflows from $WORKFLOWS_DIR"
echo "5. Configure MQTT connection to EMQX broker"
echo ""
echo -e "${BLUE}Available workflows:${NC}"
if ls "$WORKFLOWS_DIR"/*.json &>/dev/null; then
    for workflow in "$WORKFLOWS_DIR"/*.json; do
        basename=$(basename "$workflow" .json)
        case $basename in
            "formbricks-to-sheets-final")
                echo "  📋 $basename - Form data collection to Google Sheets"
                ;;
            "mqtt-to-whatsapp-alerts")
                echo "  📱 $basename - MQTT alerts to WhatsApp messages"
                ;;
            *)
                echo "  ⚙️  $basename"
                ;;
        esac
    done
else
    echo "  - No workflows found yet"
fi
echo ""
echo -e "${BLUE}Database:${NC}"
echo "  📊 PostgreSQL database for production use"
echo "  🔗 Connection: n8n-postgres:5432"
echo ""
echo -e "${BLUE}Management commands:${NC}"
echo "  Start:      docker compose -f docker-compose-n8n.yml up -d"
echo "  Stop:       docker compose -f docker-compose-n8n.yml down"
echo "  Logs (n8n): docker logs iiot-n8n -f"
echo "  Logs (DB):  docker logs iiot-n8n-db -f"
echo "  Status:     docker ps | grep -E '(n8n|postgres)'"
echo ""
echo -e "${YELLOW}⚠️  Next Steps for WhatsApp Alerts:${NC}"
echo "  1. Set up WhatsApp Business API account"
echo "  2. Configure credentials in n8n"
echo "  3. Import mqtt-to-whatsapp-alerts.json workflow"
echo "  4. Test MQTT → WhatsApp flow"
echo "  See: n8n-workflows/MQTT_WHATSAPP_SETUP.md"
echo ""
echo -e "${GREEN}Ready for industrial workflow automation! 🏭⚡📱${NC}"
>>>>>>> 7858b458385cf576eab884e5c3fd1b8815eb6ddb
