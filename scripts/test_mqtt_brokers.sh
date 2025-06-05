#!/bin/bash
# Test MQTT communication between Server EMQX and Mac Broker

echo "🔧 Testing MQTT Broker Communication"
echo "===================================="
echo ""

# Check EMQX status first
echo "📋 Step 1: Check Server EMQX Status"
echo "--------------------------------"
if docker ps | grep -q emqx; then
    echo "✅ EMQX container is running"
    EMQX_IP=$(docker inspect emqxnodec | grep '"IPAddress"' | head -1 | cut -d'"' -f4)
    echo "   IP: $EMQX_IP"
    echo "   Port: 1883"
else
    echo "❌ EMQX container not running"
    exit 1
fi

echo ""
echo "📋 Step 2: Server EMQX Listener Status"
echo "-----------------------------------"
docker exec emqxnodec emqx_ctl listeners | grep -A 3 tcp:default

echo ""
echo "📋 Step 3: Test Server EMQX Accessibility"
echo "--------------------------------------"

# Test different connection methods to EMQX
echo "Testing connection methods to EMQX:"

echo "1. Testing localhost:1883..."
if timeout 3 bash -c "</dev/tcp/localhost/1883" 2>/dev/null; then
    echo "   ✅ localhost:1883 accessible"
    EMQX_HOST="localhost"
else
    echo "   ❌ localhost:1883 not accessible"
fi

echo "2. Testing $EMQX_IP:1883..."
if timeout 3 bash -c "</dev/tcp/$EMQX_IP/1883" 2>/dev/null; then
    echo "   ✅ $EMQX_IP:1883 accessible"
    EMQX_HOST="$EMQX_IP"
else
    echo "   ❌ $EMQX_IP:1883 not accessible"
fi

if [ -z "$EMQX_HOST" ]; then
    echo "❌ Cannot connect to EMQX - check container networking"
    exit 1
fi

echo ""
echo "📋 Step 4: Install MQTT Client Tools"
echo "--------------------------------"
# Check if mosquitto clients are installed
if ! command -v mosquitto_pub &> /dev/null; then
    echo "📦 Installing mosquitto clients..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y mosquitto-clients
    elif command -v yum &> /dev/null; then
        sudo yum install -y mosquitto-clients
    else
        echo "⚠️  Please install mosquitto-clients manually"
        echo "   Ubuntu/Debian: sudo apt-get install mosquitto-clients"
        echo "   RHEL/CentOS: sudo yum install mosquitto-clients"
        exit 1
    fi
else
    echo "✅ mosquitto clients available"
fi

echo ""
echo "📋 Step 5: Test Server EMQX Pub/Sub"
echo "--------------------------------"

# Test topic for server broker testing
TEST_TOPIC="test/server-broker"
TEST_MESSAGE="Hello from server EMQX - $(date)"

echo "Testing server EMQX broker internally..."

# Test 1: Anonymous connection (if enabled)
echo "1. Testing anonymous connection..."
if timeout 5 mosquitto_pub -h $EMQX_HOST -p 1883 -t "$TEST_TOPIC" -m "$TEST_MESSAGE" 2>/dev/null; then
    echo "   ✅ Anonymous publish successful"
    AUTH_METHOD="anonymous"
else
    echo "   ❌ Anonymous publish failed"
    AUTH_METHOD="needs_auth"
fi

# Test 2: With admin credentials (if anonymous failed)
if [ "$AUTH_METHOD" = "needs_auth" ]; then
    echo "2. Testing with admin credentials..."
    if timeout 5 mosquitto_pub -h $EMQX_HOST -p 1883 -u admin -P adminpass123 -t "$TEST_TOPIC" -m "$TEST_MESSAGE" 2>/dev/null; then
        echo "   ✅ Admin credentials publish successful"
        AUTH_METHOD="admin_auth"
    else
        echo "   ❌ Admin credentials publish failed"
        AUTH_METHOD="failed"
    fi
fi

echo ""
echo "📋 Step 6: Instructions for Mac Broker Test"
echo "=========================================="
echo ""
echo "Now test from Mac to connect to this server:"
echo ""
echo "Mac → Server EMQX Test:"
echo "======================"
echo "1. On Mac, install mosquitto clients:"
echo "   brew install mosquitto"
echo ""
echo "2. Get server's external IP:"
echo "   - Find your server's IP address that Mac can reach"
echo "   - Or use localhost if testing on same machine"
echo ""
echo "3. Test publish from Mac to server EMQX:"

if [ "$AUTH_METHOD" = "anonymous" ]; then
    echo "   mosquitto_pub -h YOUR_SERVER_IP -p 1883 -t 'test/mac-to-server' -m 'Hello from Mac'"
elif [ "$AUTH_METHOD" = "admin_auth" ]; then
    echo "   mosquitto_pub -h YOUR_SERVER_IP -p 1883 -u admin -P adminpass123 -t 'test/mac-to-server' -m 'Hello from Mac'"
else
    echo "   ⚠️  Authentication issue - fix EMQX auth first"
fi

echo ""
echo "4. Test subscribe from Mac to server EMQX:"

if [ "$AUTH_METHOD" = "anonymous" ]; then
    echo "   mosquitto_sub -h YOUR_SERVER_IP -p 1883 -t 'test/#'"
elif [ "$AUTH_METHOD" = "admin_auth" ]; then
    echo "   mosquitto_sub -h YOUR_SERVER_IP -p 1883 -u admin -P adminpass123 -t 'test/#'"
fi

echo ""
echo "Server → Mac Broker Test:"
echo "========================"
echo "5. On Mac, start mosquitto broker (if not running):"
echo "   brew services start mosquitto"
echo "   # Default Mac broker runs on localhost:1883"
echo ""
echo "6. From server, test publish to Mac broker:"
echo "   mosquitto_pub -h MAC_IP_ADDRESS -p 1883 -t 'test/server-to-mac' -m 'Hello from Server'"
echo ""
echo "7. On Mac, subscribe to see server messages:"
echo "   mosquitto_sub -h localhost -p 1883 -t 'test/#'"

echo ""
echo "📋 Step 7: Expected Results"
echo "========================="
echo ""
echo "✅ Success indicators:"
echo "   - Mac can publish to server EMQX"
echo "   - Mac can subscribe to server EMQX"
echo "   - Server can publish to Mac broker"
echo "   - Messages appear in subscribers"
echo ""
echo "❌ If MQTT brokers work but n8n doesn't:"
echo "   - Issue is specifically with n8n MQTT integration"
echo "   - Focus on n8n credential configuration"
echo "   - Check n8n container networking"
echo ""
echo "❌ If MQTT brokers don't work:"
echo "   - Fix basic MQTT connectivity first"
echo "   - Check firewall/network settings"
echo "   - Verify broker authentication"

echo ""
echo "📊 Current Server EMQX Status:"
echo "=============================="
echo "Host: $EMQX_HOST"
echo "Port: 1883"
echo "Authentication: $AUTH_METHOD"
echo ""
echo "🎯 Next: Test Mac ↔ Server MQTT communication"
echo "   Then come back to n8n integration if MQTT works"