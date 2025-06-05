#!/bin/bash
# Test MQTT to Google Sheets flow

echo "🧪 Testing MQTT → n8n → Google Sheets Flow"
echo "==========================================="
echo ""

echo "📋 Prerequisites Check:"
echo "- n8n workflow imported and activated"
echo "- Google Sheets credentials configured in n8n"
echo "- MQTT host set to 'host.docker.internal'"
echo "- Equipment Alerts and All Equipment Events sheets created"
echo ""

echo "🔄 Starting test sequence..."
echo ""

echo "Test 1: Info Level Alert (Sheets only)"
mosquitto_pub -h localhost -p 1883 -t "equipment/status" -m '{"equipmentId":"TEST-001","type":"test_sensor","location":"Test Lab","value":"normal","description":"Test info message"}'
echo "✅ Sent info alert"
sleep 2

echo ""
echo "Test 2: Warning Alert (Sheets + WhatsApp)"
mosquitto_pub -h localhost -p 1883 -t "equipment/alerts" -m '{"equipmentId":"PUMP-001","type":"centrifugal_pump","location":"Building A","value":78,"threshold":75,"description":"Vibration levels elevated"}'
echo "✅ Sent warning alert"
sleep 2

echo ""
echo "Test 3: Critical Alert (Sheets + WhatsApp)"
mosquitto_pub -h localhost -p 1883 -t "sensors/critical" -m '{"equipmentId":"TEMP-001","type":"temperature_sensor","location":"Reactor Room","value":95,"threshold":85,"description":"Critical temperature exceeded"}'
echo "✅ Sent critical alert"
sleep 2

echo ""
echo "Test 4: Fault Alert (Sheets + WhatsApp)"
mosquitto_pub -h localhost -p 1883 -t "actuators/fault" -m '{"equipmentId":"VALVE-003","type":"control_valve","location":"Process Line 2","value":"stuck_closed","description":"Valve failed to open"}'
echo "✅ Sent fault alert"

echo ""
echo "🔍 Check Results:"
echo "================="
echo "1. n8n Execution History: http://localhost:5678/executions"
echo "2. Google Sheets: https://docs.google.com/spreadsheets/d/1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do"
echo "   - Equipment Alerts sheet (warning/critical only)"
echo "   - All Equipment Events sheet (all messages)"
echo "3. WhatsApp/Webhook (if configured)"
echo ""

echo "📊 Expected Results:"
echo "- 4 entries in 'All Equipment Events' sheet"
echo "- 3 entries in 'Equipment Alerts' sheet (warning/critical/fault)"
echo "- 3 WhatsApp alerts sent (if configured)"
echo ""

echo "🎯 Test complete! Check the results in n8n and Google Sheets."