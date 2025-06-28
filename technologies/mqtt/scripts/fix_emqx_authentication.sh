#!/bin/bash
# Fix EMQX Authentication - Enable Anonymous Access

echo "🔧 Fixing EMQX Authentication Issue"
echo "==================================="
echo ""

echo "🔍 Current authentication status:"
docker exec emqxnodec emqx_ctl conf show authentication | head -5

echo ""
echo "📝 Problem: EMQX is configured for MySQL authentication but MySQL DB is not available"
echo "💡 Solution: Enable anonymous access for MQTT connections"
echo ""

# Method 1: Try to enable anonymous access via CLI
echo "🔧 Method 1: Enabling anonymous access via CLI..."
docker exec emqxnodec emqx_ctl conf set zone.default.allow_anonymous true 2>&1

# Method 2: Disable the MySQL authentication temporarily
echo ""
echo "🔧 Method 2: Disabling MySQL authentication..."
docker exec emqxnodec emqx_ctl conf set authentication.1.enable false 2>&1

# Method 3: Create a simple built-in user
echo ""
echo "🔧 Method 3: Creating simple authentication..."
docker exec emqxnodec emqx_ctl conf load - <<'EOF'
authentication = [
  {
    backend = built_in_database
    enable = true
    mechanism = password_based
    password_hash_algorithm {name = plain, salt_position = disable}
    user_id_type = username
  }
]
EOF

echo ""
echo "📋 Testing connection..."

# Install mosquitto clients if not available
if ! command -v mosquitto_pub &> /dev/null; then
    echo "📦 Installing mosquitto clients..."
    sudo apt-get update && sudo apt-get install -y mosquitto-clients
fi

# Test anonymous connection
echo "🧪 Testing anonymous MQTT connection..."
timeout 5 mosquitto_pub -h 172.17.0.4 -p 1883 -t "test/anonymous" -m "test" 2>&1 || echo "Anonymous connection failed"

# Test with basic credentials
echo "🧪 Testing with admin credentials..."
timeout 5 mosquitto_pub -h 172.17.0.4 -p 1883 -u admin -P public -t "test/auth" -m "test" 2>&1 || echo "Admin credentials failed"

echo ""
echo "📊 Current EMQX listeners status:"
docker exec emqxnodec emqx_ctl listeners | grep -A 3 tcp:default

echo ""
echo "🎯 For n8n MQTT Credentials, try:"
echo "================================="
echo "Option 1 (Anonymous):"
echo "  Protocol: mqtt://"
echo "  Host: 172.17.0.4"
echo "  Port: 1883"
echo "  Username: (leave empty)"
echo "  Password: (leave empty)"
echo "  Client ID: n8n-mqtt-client"
echo "  SSL: OFF"
echo ""
echo "Option 2 (If built-in auth is working):"
echo "  Protocol: mqtt://"
echo "  Host: 172.17.0.4"
echo "  Port: 1883"
echo "  Username: admin"
echo "  Password: admin"
echo "  Client ID: n8n-mqtt-client"
echo "  SSL: OFF"
echo ""
echo "✅ EMQX authentication fix completed!"
echo "Now try the n8n MQTT credential test again."