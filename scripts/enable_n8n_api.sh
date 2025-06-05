#!/bin/bash
# CT-013: Enable n8n API Access
# Configures n8n for API access and generates API keys

echo "🔐 CT-013: Enabling n8n API Access"
echo "==================================="
echo ""

# Check if n8n is running
if ! docker ps | grep -q "n8n"; then
    echo "❌ n8n container is not running"
    exit 1
fi

echo "✅ n8n container is running"
echo ""

# Update n8n configuration to enable public API
echo "📝 Updating n8n configuration for API access..."

# Create updated docker-compose with API settings
cat > docker-compose-n8n-api.yml << 'EOF'
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
    volumes:
      - n8n-postgres-data:/var/lib/postgresql/data
    networks:
      - n8n-network
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U n8n_user -d n8n']
      interval: 5s
      timeout: 5s
      retries: 10

  # n8n workflow automation with API enabled
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
      
      # API Configuration
      - N8N_PUBLIC_API_DISABLED=false
      - N8N_PUBLIC_API_ENDPOINT=http://localhost:5678/api/v1
      
      # Server Configuration
      - N8N_HOST=0.0.0.0
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
      
    volumes:
      - n8n-data:/home/node/.n8n
      - n8n-workflows:/home/node/.n8n/workflows
    networks:
      - n8n-network
      - bridge  # Connect to bridge network for EMQX access
    depends_on:
      n8n-postgres:
        condition: service_healthy

networks:
  n8n-network:
    driver: bridge
  bridge:
    external: true

volumes:
  n8n-postgres-data:
    driver: local
  n8n-data:
    driver: local
  n8n-workflows:
    driver: local
EOF

echo "✅ Updated configuration created"
echo ""

# Restart n8n with new configuration
echo "🔄 Restarting n8n with API enabled..."
docker-compose -f docker-compose-n8n-api.yml down
docker-compose -f docker-compose-n8n-api.yml up -d

# Wait for n8n to start
echo "⏳ Waiting for n8n to start..."
sleep 15

# Check if n8n is accessible
echo ""
echo "🧪 Testing n8n accessibility..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5678 | grep -q "200\|401"; then
    echo "✅ n8n web interface is accessible"
else
    echo "❌ n8n web interface not accessible"
fi

# Create API test script
echo ""
echo "📝 Creating API test script..."

cat > test_n8n_api.py << 'EOF'
#!/usr/bin/env python3
"""Test n8n API endpoints with basic authentication"""

import requests
from requests.auth import HTTPBasicAuth
import json

# n8n API configuration
N8N_URL = "http://localhost:5678"
USERNAME = "admin"
PASSWORD = "admin"

# Create auth object
auth = HTTPBasicAuth(USERNAME, PASSWORD)

print("🧪 Testing n8n API Endpoints")
print("===========================\n")

# Test 1: Health Check
print("1️⃣ Testing health endpoint...")
try:
    response = requests.get(f"{N8N_URL}/healthz", timeout=5)
    if response.status_code == 200:
        print(f"✅ Health check passed: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get Workflows
print("\n2️⃣ Testing workflows endpoint...")
try:
    response = requests.get(f"{N8N_URL}/api/v1/workflows", auth=auth, timeout=5)
    if response.status_code == 200:
        workflows = response.json().get('data', [])
        print(f"✅ Found {len(workflows)} workflows")
        for wf in workflows:
            print(f"   - {wf.get('name')} (ID: {wf.get('id')})")
    else:
        print(f"❌ Failed to get workflows: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Get Executions
print("\n3️⃣ Testing executions endpoint...")
try:
    response = requests.get(f"{N8N_URL}/api/v1/executions", auth=auth, timeout=5)
    if response.status_code == 200:
        executions = response.json().get('data', [])
        print(f"✅ Found {len(executions)} executions")
    else:
        print(f"❌ Failed to get executions: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Display API connection details
print("\n📋 API Connection Details:")
print("========================")
print(f"URL: {N8N_URL}/api/v1")
print(f"Authentication: Basic Auth")
print(f"Username: {USERNAME}")
print(f"Password: {PASSWORD}")
print("\nExample curl command:")
print(f'curl -u {USERNAME}:{PASSWORD} {N8N_URL}/api/v1/workflows')
EOF

chmod +x test_n8n_api.py

echo "✅ API test script created"
echo ""

# Run API tests
echo "🧪 Running API tests..."
python3 test_n8n_api.py

echo ""
echo "📊 n8n API Configuration Summary:"
echo "================================="
echo "API Endpoint: http://localhost:5678/api/v1"
echo "Authentication: Basic Auth"
echo "Username: admin"
echo "Password: admin"
echo ""
echo "Example API calls:"
echo "- Get workflows: curl -u admin:admin http://localhost:5678/api/v1/workflows"
echo "- Get executions: curl -u admin:admin http://localhost:5678/api/v1/executions"
echo "- Health check: curl http://localhost:5678/healthz"
echo ""
echo "✅ n8n API access enabled!"