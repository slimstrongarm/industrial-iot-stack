#!/bin/bash
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