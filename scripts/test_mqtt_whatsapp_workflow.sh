#!/bin/bash
# CT-008: Test MQTT→WhatsApp Alert Workflow
# Tests the n8n MQTT to WhatsApp integration

echo "🧪 CT-008: MQTT→WhatsApp Workflow Testing"
echo "=========================================="
echo ""

# Load configuration
EMQX_HOST="172.17.0.4"
EMQX_PORT="1883"

echo "📋 Test Configuration:"
echo "  • EMQX Host: $EMQX_HOST"
echo "  • EMQX Port: $EMQX_PORT"
echo "  • n8n Interface: http://localhost:5678"
echo ""

# Check if mosquitto_pub is available
if ! command -v mosquitto_pub &> /dev/null; then
    echo "⚠️  mosquitto_pub not found. Installing mosquitto-clients..."
    sudo apt-get update && sudo apt-get install -y mosquitto-clients
fi

echo "🔍 Pre-flight Checks:"
echo "====================="

# Check EMQX
if nc -zv $EMQX_HOST $EMQX_PORT 2>&1 | grep -q succeeded; then
    echo "✅ EMQX broker is reachable"
else
    echo "❌ EMQX broker not reachable at $EMQX_HOST:$EMQX_PORT"
    exit 1
fi

# Check n8n
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5678 | grep -q "200\|401"; then
    echo "✅ n8n is running"
else
    echo "❌ n8n not accessible"
    exit 1
fi

echo ""
echo "⚠️  IMPORTANT: Before running tests, ensure:"
echo "  1. Both workflows are imported in n8n"
echo "  2. MQTT→WhatsApp workflow is ACTIVATED"
echo "  3. Google Sheets credentials are configured"
echo "  4. MQTT connection is configured (Host: $EMQX_HOST)"
echo ""
read -p "Press Enter to continue with tests..."

echo ""
echo "📊 Test Scenarios:"
echo "=================="

# Test 1: Critical Equipment Alert
echo ""
echo "1️⃣ Test 1: Critical Equipment Failure"
echo "   Topic: equipment/alerts"
echo "   Severity: Critical"

PAYLOAD_1='{
  "equipmentId": "PUMP-001",
  "type": "Centrifugal Pump",
  "location": "Building A - Floor 2",
  "value": 95.5,
  "threshold": 80,
  "description": "Pump temperature exceeding critical threshold",
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'

echo "   Sending: $PAYLOAD_1"
mosquitto_pub -h $EMQX_HOST -p $EMQX_PORT -t "equipment/alerts" -m "$PAYLOAD_1"
echo "   ✅ Critical alert sent"
sleep 3

# Test 2: Sensor Warning
echo ""
echo "2️⃣ Test 2: Critical Sensor Reading"
echo "   Topic: sensors/critical"
echo "   Severity: Critical"

PAYLOAD_2='{
  "equipmentId": "TEMP-SENSOR-42",
  "type": "Temperature Sensor",
  "location": "Reactor Room 3",
  "value": 150,
  "threshold": 120,
  "description": "Reactor temperature critical - immediate action required",
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'

echo "   Sending sensor critical alert..."
mosquitto_pub -h $EMQX_HOST -p $EMQX_PORT -t "sensors/critical" -m "$PAYLOAD_2"
echo "   ✅ Sensor alert sent"
sleep 3

# Test 3: Actuator Fault
echo ""
echo "3️⃣ Test 3: Actuator Fault Detection"
echo "   Topic: actuators/fault"
echo "   Severity: Critical"

PAYLOAD_3='{
  "equipmentId": "VALVE-203",
  "type": "Control Valve",
  "location": "Pipeline Section B",
  "value": "FAULT",
  "threshold": "NORMAL",
  "description": "Valve actuator not responding to control signals",
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'

echo "   Sending actuator fault..."
mosquitto_pub -h $EMQX_HOST -p $EMQX_PORT -t "actuators/fault" -m "$PAYLOAD_3"
echo "   ✅ Actuator fault sent"
sleep 3

# Test 4: Info Level Event (Should not trigger WhatsApp)
echo ""
echo "4️⃣ Test 4: Normal Operation Event"
echo "   Topic: equipment/status"
echo "   Severity: Info (no WhatsApp alert expected)"

PAYLOAD_4='{
  "equipmentId": "MOTOR-005",
  "type": "Electric Motor",
  "location": "Production Line 1",
  "value": 45,
  "threshold": 80,
  "description": "Motor operating within normal parameters",
  "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"
}'

echo "   Sending normal status update..."
mosquitto_pub -h $EMQX_HOST -p $EMQX_PORT -t "equipment/status" -m "$PAYLOAD_4"
echo "   ✅ Status update sent"

echo ""
echo "📊 Test Results Expected:"
echo "========================"
echo ""
echo "✅ Expected in Google Sheets 'Equipment Alerts':"
echo "   - 3 rows (only critical/warning alerts)"
echo "   - Pump, Sensor, and Valve alerts"
echo ""
echo "✅ Expected in Google Sheets 'All Equipment Events':"
echo "   - 4 rows (all events including info)"
echo "   - All test messages logged"
echo ""
echo "✅ Expected WhatsApp Messages:"
echo "   - 3 messages for critical alerts"
echo "   - No message for info-level event"
echo ""
echo "🔍 Verification Steps:"
echo "1. Check n8n Executions: http://localhost:5678/executions"
echo "2. Check Google Sheets for new entries"
echo "3. Verify WhatsApp messages (if configured)"
echo ""
echo "📋 Troubleshooting:"
echo "- If no executions appear, check if workflow is activated"
echo "- If executions fail, check MQTT connection settings"
echo "- For Google Sheets errors, verify service account permissions"
echo ""
echo "✅ Test execution complete!"