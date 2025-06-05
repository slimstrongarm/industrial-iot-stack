#!/bin/bash
# Set up built-in database authentication in EMQX

echo "🔧 Setting Up EMQX Built-in Database Authentication"
echo "=================================================="
echo ""

echo "📋 Step 1: Enable built-in database authentication"
cat > /tmp/builtin_auth.hocon << 'EOF'
authentication = [
  {
    enable = true
    backend = built_in_database
    mechanism = password_based
    password_hash_algorithm {
      name = plain
      salt_position = disable
    }
    user_id_type = username
  }
]
EOF

echo "Loading built-in authentication config..."
docker cp /tmp/builtin_auth.hocon emqxnodec:/tmp/builtin_auth.hocon
docker exec emqxnodec emqx_ctl conf load /tmp/builtin_auth.hocon

echo ""
echo "📋 Step 2: Create test user via EMQX CLI"
echo "Creating user: testuser / testpass123"

# Try different CLI methods to create user
echo "Method 1: Direct user creation..."
docker exec emqxnodec emqx_ctl users add testuser testpass123 2>&1 || echo "Method 1 failed"

echo "Method 2: Authentication user creation..."
docker exec emqxnodec emqx_ctl auth add username testuser password testpass123 2>&1 || echo "Method 2 failed"

echo ""
echo "📋 Step 3: Alternative - Create via config file"
cat > /tmp/user_config.hocon << 'EOF'
authentication = [
  {
    enable = true
    backend = built_in_database
    mechanism = password_based
    password_hash_algorithm {
      name = plain
      salt_position = disable
    }
    user_id_type = username
    bootstrap_file = "/tmp/users.json"
  }
]
EOF

# Create users file
cat > /tmp/users.json << 'EOF'
[
  {
    "user_id": "n8nuser",
    "password": "n8npass123"
  },
  {
    "user_id": "testuser", 
    "password": "testpass123"
  }
]
EOF

echo "Loading user config..."
docker cp /tmp/user_config.hocon emqxnodec:/tmp/user_config.hocon
docker cp /tmp/users.json emqxnodec:/tmp/users.json
docker exec emqxnodec emqx_ctl conf load /tmp/user_config.hocon

echo ""
echo "📋 Step 4: Check configuration"
docker exec emqxnodec emqx_ctl conf show authentication | head -10

echo ""
echo "📋 Step 5: Test credentials in n8n"
echo "=================================="
echo ""
echo "Try these credentials in n8n MQTT:"
echo ""
echo "Option 1:"
echo "  Username: n8nuser"
echo "  Password: n8npass123"
echo ""
echo "Option 2:"
echo "  Username: testuser"
echo "  Password: testpass123"
echo ""
echo "All other settings:"
echo "  Protocol: mqtt://"
echo "  Host: localhost"
echo "  Port: 1883"
echo "  Client ID: n8n-mqtt-client"
echo "  SSL: OFF"

echo ""
echo "🧪 If that doesn't work, let's check the EMQX dashboard:"
echo "1. Go to: http://localhost:18083"
echo "2. Login: admin / adminpass123"
echo "3. Access Control → Authentication"
echo "4. Add Built-in Database authentication"
echo "5. Access Control → Users → Add User"

echo ""
echo "✅ Built-in authentication setup complete!"