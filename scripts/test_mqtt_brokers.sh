#!/bin/bash

# MQTT Broker Cross-Testing Script
# Tests pub/sub between Mosquitto (Mac) and EMQX (Server)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MAC_BROKER="localhost"
SERVER_BROKER="100.94.84.126"  # Update with actual server IP
MAC_PORT="1883"
SERVER_PORT="1883"

echo -e "${BLUE}🔧 MQTT Broker Cross-Testing${NC}"
echo "======================================"

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

# Test 1: Local Mosquitto
echo -e "\n${BLUE}Test 1: Mac Mosquitto Broker${NC}"
echo "Testing: $MAC_BROKER:$MAC_PORT"

# Test local publish/subscribe with proper timing
TEST_MESSAGE="Test from Mac Mosquitto - $(date)"

# Start subscriber in background, then publish
mosquitto_sub -h $MAC_BROKER -p $MAC_PORT -t "test/mac-local" -C 1 > /tmp/mqtt_test.txt 2>/dev/null &
SUB_PID=$!
sleep 1
mosquitto_pub -h $MAC_BROKER -p $MAC_PORT -t "test/mac-local" -m "$TEST_MESSAGE"
wait $SUB_PID
RECEIVED=$(cat /tmp/mqtt_test.txt 2>/dev/null || echo "")

if [[ "$RECEIVED" == "$TEST_MESSAGE" ]]; then
    print_status "Mac Mosquitto pub/sub working"
else
    print_error "Mac Mosquitto pub/sub failed"
    echo "Expected: $TEST_MESSAGE"
    echo "Received: $RECEIVED"
fi

# Test 2: Server EMQX (if accessible)
echo -e "\n${BLUE}Test 2: Server EMQX Broker${NC}"
echo "Testing: $SERVER_BROKER:$SERVER_PORT"

# Try to connect to server broker
if mosquitto_pub -h $SERVER_BROKER -p $SERVER_PORT -t "test/server-connection" -m "Connection test from Mac" 2>/dev/null; then
    print_status "Can connect to Server EMQX"
    
    # Test publish to server, subscribe from Mac
    echo -e "\n${YELLOW}Cross-broker test: Mac → Server → Mac${NC}"
    
    # Publish to server
    SERVER_MESSAGE="Cross-broker test from Mac to Server - $(date)"
    mosquitto_pub -h $SERVER_BROKER -p $SERVER_PORT -t "iiot/test/cross-broker" -m "$SERVER_MESSAGE"
    print_status "Published to Server EMQX"
    
    # Try to subscribe from server (if possible)
    echo "To complete the test, run this on the server:"
    echo "mosquitto_sub -h localhost -p 1883 -t \"iiot/test/cross-broker\" -C 1"
    
else
    print_warning "Cannot connect to Server EMQX at $SERVER_BROKER:$SERVER_PORT"
    echo "This could be due to:"
    echo "  - Firewall blocking port 1883"
    echo "  - EMQX not configured for external connections"
    echo "  - Network connectivity issues"
fi

# Test 3: Topic structure validation
echo -e "\n${BLUE}Test 3: Topic Structure Validation${NC}"

# Test various topic patterns used in the stack
TOPICS=(
    "brewery/data/ignition_opc/Boiler_1"
    "iiot/alerts/critical"
    "iiot/commands/Pumps_Pump_1/Start"
    "steel_bonnet/equipment/status"
)

for topic in "${TOPICS[@]}"; do
    mosquitto_pub -h $MAC_BROKER -p $MAC_PORT -t "$topic" -m "Test message for $topic"
    print_status "Published to topic: $topic"
done

# Test 4: QoS levels
echo -e "\n${BLUE}Test 4: QoS Level Testing${NC}"

for qos in 0 1 2; do
    mosquitto_pub -h $MAC_BROKER -p $MAC_PORT -t "test/qos-$qos" -m "QoS $qos test" -q $qos
    print_status "QoS $qos publish successful"
done

# Test 5: Retained messages
echo -e "\n${BLUE}Test 5: Retained Message Testing${NC}"

mosquitto_pub -h $MAC_BROKER -p $MAC_PORT -t "test/retained" -m "This is a retained message" -r
print_status "Retained message published"

# Wait a moment then subscribe to retained message
sleep 1
RETAINED_MSG=$(mosquitto_sub -h $MAC_BROKER -p $MAC_PORT -t "test/retained" -C 1 2>/dev/null || echo "")
if [[ -n "$RETAINED_MSG" ]]; then
    print_status "Retained message received: $RETAINED_MSG"
else
    print_warning "Retained message not received"
fi

# Test 6: Wildcard subscriptions
echo -e "\n${BLUE}Test 6: Wildcard Subscription Testing${NC}"

# Publish to multiple topics
mosquitto_pub -h $MAC_BROKER -p $MAC_PORT -t "test/wildcard/topic1" -m "Message 1"
mosquitto_pub -h $MAC_BROKER -p $MAC_PORT -t "test/wildcard/topic2" -m "Message 2"
mosquitto_pub -h $MAC_BROKER -p $MAC_PORT -t "test/wildcard/deep/topic3" -m "Message 3"

print_status "Published test messages for wildcard testing"
echo "To test wildcards, run:"
echo "  Single level: mosquitto_sub -h $MAC_BROKER -t 'test/wildcard/+'"
echo "  Multi level:  mosquitto_sub -h $MAC_BROKER -t 'test/wildcard/#'"

# Configuration summary
echo -e "\n${BLUE}Configuration Summary${NC}"
echo "======================================"
echo "Mac Mosquitto:"
echo "  Host: $MAC_BROKER"
echo "  Port: $MAC_PORT"
echo "  Config: /opt/homebrew/etc/mosquitto/mosquitto.conf"
echo ""
echo "Server EMQX:"
echo "  Host: $SERVER_BROKER"
echo "  Port: $SERVER_PORT"
echo "  Dashboard: http://$SERVER_BROKER:18083 (if configured)"
echo ""
echo "For n8n MQTT node configuration:"
echo "  Use Server EMQX: $SERVER_BROKER:$SERVER_PORT"
echo "  Topics to monitor: iiot/alerts/critical, brewery/data/+/+"

# Troubleshooting section
echo -e "\n${YELLOW}Troubleshooting Tips${NC}"
echo "======================================"
echo "If n8n can't connect to EMQX:"
echo "1. Check EMQX is running: docker ps | grep emqx"
echo "2. Check EMQX config allows external connections"
echo "3. Test from server: mosquitto_sub -h localhost -t 'test'"
echo "4. Check firewall: telnet $SERVER_BROKER 1883"
echo "5. Use EMQX dashboard to verify listeners"
echo ""
echo "If cross-broker communication fails:"
echo "1. Verify network connectivity between Mac and Server"
echo "2. Check both brokers are on same topic namespace"
echo "3. Consider MQTT bridge configuration"

echo -e "\n${GREEN}🎉 MQTT Testing Complete!${NC}"
