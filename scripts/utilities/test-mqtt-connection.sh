#!/bin/bash
# Quick MQTT connection test script

echo "=== Testing MQTT Connection ==="

# Test if mosquitto is running
if systemctl is-active --quiet mosquitto; then
    echo "✅ Mosquitto service is running"
else
    echo "❌ Mosquitto service is not running"
    echo "Start with: sudo systemctl start mosquitto"
    exit 1
fi

# Test local connection
echo -e "\n📡 Testing MQTT publish/subscribe..."
echo "Starting subscriber in background..."

# Subscribe in background and save PID
mosquitto_sub -h localhost -t "SteelBonnet/Test/#" -v > mqtt_test.log 2>&1 &
SUB_PID=$!

# Give subscriber time to connect
sleep 2

# Publish test messages
echo "Publishing test messages..."
mosquitto_pub -h localhost -t "SteelBonnet/Test/Gateway/Status" -m "online"
mosquitto_pub -h localhost -t "SteelBonnet/Test/Equipment/Temperature" -m "72.5"
mosquitto_pub -h localhost -t "SteelBonnet/Test/Equipment/register" -m '{"id":"TEST001","type":"pump","area":"Test"}'

# Wait for messages to be received
sleep 2

# Kill subscriber
kill $SUB_PID 2>/dev/null

# Check results
echo -e "\n📋 Messages received:"
cat mqtt_test.log

# Cleanup
rm -f mqtt_test.log

echo -e "\n✅ MQTT test complete!"
echo "Ready to proceed with Node-RED integration"