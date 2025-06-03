#!/bin/bash

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