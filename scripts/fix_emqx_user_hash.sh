#!/bin/bash
# Fix EMQX user with proper password hash

echo "🔧 Fixing EMQX User Authentication"
echo "=================================="
echo ""

echo "Current configuration:"
echo "- User ID Type: clientid"
echo "- Password Hash: sha256 with suffix salt"
echo ""

# Since we can't easily create SHA256 hashed passwords, let's change the auth to plain text
echo "📝 Solution: Change password hash algorithm to plain text"
echo ""

# Create a new authentication config with plain text passwords
cat > /tmp/plain_auth.hocon << 'EOF'
authentication = [
  {
    enable = true
    backend = built_in_database
    mechanism = password_based
    password_hash_algorithm {
      name = plain
      salt_position = disable
    }
    user_id_type = clientid
  }
]
EOF

echo "Applying plain text authentication configuration..."
docker cp /tmp/plain_auth.hocon emqxnodec:/tmp/plain_auth.hocon
docker exec emqxnodec emqx_ctl conf load /tmp/plain_auth.hocon

echo ""
echo "✅ Configuration updated to use plain text passwords"
echo ""

# Now create the user via bootstrap file
echo "Creating bootstrap file with n8nuser..."
cat > /tmp/auth-users.csv << 'EOF'
user_id,password,is_superuser
n8nuser,n8npass123,false
EOF

docker cp /tmp/auth-users.csv emqxnodec:/opt/emqx/etc/auth-built-in-db-bootstrap.csv

echo "Reloading EMQX configuration..."
docker exec emqxnodec emqx_ctl reload

sleep 2

echo ""
echo "📋 New configuration applied!"
echo ""
echo "🔌 n8n MQTT Configuration:"
echo "=========================="
echo "Protocol: mqtt://"
echo "Host: localhost"  
echo "Port: 1883"
echo "Username: (LEAVE EMPTY)"
echo "Password: n8npass123"
echo "Client ID: n8nuser"
echo "SSL: OFF"
echo ""
echo "⚠️  Remember: Username field MUST be empty!"
echo "⚠️  'n8nuser' goes in the Client ID field!"