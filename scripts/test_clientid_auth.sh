#!/bin/bash
# Test MQTT connection using Client ID authentication

echo "🔍 EMQX Authentication Configuration Found!"
echo "=========================================="
echo ""
echo "✅ Built-in Database: ENABLED"
echo "❌ User ID Type: clientid (NOT username!)"
echo "❌ Password Hash: sha256 with suffix salt"
echo ""
echo "This means:"
echo "- Put 'n8nuser' in the Client ID field"
echo "- Username field should be empty"
echo "- Password might need to be hashed"
echo ""
echo "🧪 Testing with mosquitto client using Client ID:"
echo ""

# Test 1: Client ID with plain password
echo "Test 1: Using Client ID with plain password..."
mosquitto_pub -h localhost -p 1883 \
  -i "n8nuser" \
  -P "n8npass123" \
  -t "test/topic" \
  -m "Test from client ID" 2>&1

echo ""
echo "📝 n8n Configuration to try:"
echo "============================"
echo "Protocol: mqtt://"
echo "Host: localhost"
echo "Port: 1883"
echo "Username: (LEAVE EMPTY)"
echo "Password: n8npass123"
echo "Client ID: n8nuser"
echo "SSL: OFF"
echo ""
echo "⚠️  IMPORTANT: The username field must be EMPTY!"
echo "⚠️  Put 'n8nuser' in the Client ID field instead!"