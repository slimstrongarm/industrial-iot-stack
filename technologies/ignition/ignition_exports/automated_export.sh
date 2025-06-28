#!/bin/bash
# Automated Ignition Project Export Script

GATEWAY_URL="http://localhost:8088"
AUTH="admin:password"
EXPORT_DIR="$(pwd)"

echo "🚀 Starting automated export..."

projects=(
    "test_run_01"
    "brewery_control"
    "steel_bonnet_hmi"
    "equipment_registry"
    "mqtt_integration"
    "reporting_dashboards"
    "alarm_management"
    "user_management"
    "data_historian"
)

for project in "${projects[@]}"; do
    echo "📦 Exporting $project..."
    
    curl -X POST \
        -u $AUTH \
        -H "Content-Type: application/json" \
        -d "{\"projectName\": \"$project\"}" \
        -o "${project}_export.zip" \
        "$GATEWAY_URL/data/designer/export"
    
    if [ -f "${project}_export.zip" ]; then
        echo "✅ Exported $project"
    else
        echo "❌ Failed to export $project"
    fi
done

echo "✅ Export complete! Check the files above."
