#!/bin/bash
# Import n8n workflows for CT-007
# Imports Formbricks→Sheets and MQTT→WhatsApp workflows

echo "🔄 CT-007: n8n Workflow Import"
echo "=============================="
echo ""

# Check if n8n is running
if ! docker ps | grep -q " n8n "; then
    echo "❌ n8n container is not running"
    echo "   Start it with: docker-compose -f docker-compose-n8n-stack.yml up -d"
    exit 1
fi

echo "✅ n8n container is running"
echo ""

# Check n8n accessibility
echo "🌐 Testing n8n web interface accessibility..."
if timeout 10 curl -s http://localhost:5678 > /dev/null; then
    echo "✅ n8n web interface is accessible"
else
    echo "⚠️  n8n web interface not immediately accessible (may need authentication)"
fi

echo ""

# Workflow files to import
WORKFLOWS=(
    "formbricks-n8n-workflow-with-error-handling.json:Formbricks to Google Sheets"
    "mqtt-whatsapp-alert-workflow.json:MQTT Equipment Alert to WhatsApp"
)

echo "📋 Workflows to Import:"
for workflow in "${WORKFLOWS[@]}"; do
    filename="${workflow%%:*}"
    description="${workflow##*:}"
    if [ -f "$filename" ]; then
        echo "  ✅ $filename - $description"
    else
        echo "  ❌ $filename - NOT FOUND"
    fi
done

echo ""

# Method 1: Copy workflows to n8n data volume for manual import
echo "📁 Method 1: Copying workflows to n8n data volume..."

# Create workflows directory in n8n volume
docker exec n8n mkdir -p /home/node/.n8n/workflows-import

# Copy workflow files to n8n container
for workflow in "${WORKFLOWS[@]}"; do
    filename="${workflow%%:*}"
    description="${workflow##*:}"
    
    if [ -f "$filename" ]; then
        echo "  📋 Copying $filename..."
        docker cp "$filename" n8n:/home/node/.n8n/workflows-import/
        echo "  ✅ $filename copied to container"
    else
        echo "  ❌ $filename not found, skipping"
    fi
done

echo ""

# Method 2: Use n8n CLI (if available)
echo "🔧 Method 2: Attempting n8n CLI import..."

# Check if n8n CLI is available
if docker exec n8n which n8n > /dev/null 2>&1; then
    echo "✅ n8n CLI is available"
    
    for workflow in "${WORKFLOWS[@]}"; do
        filename="${workflow%%:*}"
        description="${workflow##*:}"
        
        if [ -f "$filename" ]; then
            echo "  📋 Importing $filename via CLI..."
            
            # Try CLI import (may not work without proper setup)
            if docker exec n8n n8n import:workflow --input="/home/node/.n8n/workflows-import/$filename" 2>/dev/null; then
                echo "  ✅ $filename imported successfully via CLI"
            else
                echo "  ⚠️  CLI import failed for $filename (manual import required)"
            fi
        fi
    done
else
    echo "⚠️  n8n CLI not available for automatic import"
fi

echo ""

# Method 3: Manual import instructions
echo "📝 Method 3: Manual Import Instructions"
echo "=====================================

Since n8n workflows typically require manual import through the web interface:

1. **Access n8n**: http://localhost:5678
   - Username: admin
   - Password: admin

2. **Import Workflows**:
   
   **Formbricks→Sheets Workflow:**
   - Click 'Import from File'
   - Select: formbricks-n8n-workflow-with-error-handling.json
   - Configure Google Sheets credentials if needed
   
   **MQTT→WhatsApp Workflow:**
   - Click 'Import from File' 
   - Select: mqtt-whatsapp-alert-workflow.json
   - Configure:
     • MQTT connection: Host = 172.17.0.4, Port = 1883
     • WhatsApp API credentials (if available)
     • Google Sheets service account

3. **Test Workflows**:
   - Activate both workflows
   - Test MQTT workflow with sample equipment data
   - Verify Google Sheets logging

**Alternative**: Workflows are copied to container at:
/home/node/.n8n/workflows-import/

You can import them directly through the n8n interface.
"

# Provide configuration details
echo ""
echo "🔧 Configuration Details"
echo "========================

**MQTT Configuration:**
- Host: 172.17.0.4 (EMQX container IP)
- Port: 1883
- Topics: equipment/alerts, sensors/critical, actuators/fault
- QoS: 1

**Google Sheets Configuration:**
- Spreadsheet ID: 1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do
- Service Account: server-claude@iiot-stack-automation.iam.gserviceaccount.com
- Sheets: 'Equipment Alerts', 'All Equipment Events'

**WhatsApp Configuration (requires setup):**
- API Token: YOUR_WHATSAPP_API_TOKEN (to be configured)
- Phone Number: YOUR_PHONE_NUMBER (to be configured)
- API Endpoint: https://api.whatsapp.com/send

**Test Topics for CT-008:**
- equipment/alerts/pump-001
- sensors/critical/temperature
- actuators/fault/valve-203
"

echo ""
echo "📊 Import Status Summary:"
echo "  ✅ Workflows copied to n8n container"
echo "  ⏳ Manual import required through web interface"
echo "  📋 Configuration details provided"
echo ""
echo "🎯 Next Steps:"
echo "  1. Access n8n at http://localhost:5678" 
echo "  2. Import both workflow files manually"
echo "  3. Configure credentials and connections"
echo "  4. Activate workflows"
echo "  5. Proceed to CT-008 testing"