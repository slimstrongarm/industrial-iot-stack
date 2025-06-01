#!/bin/bash
# Backup and Recovery System for Industrial IoT Stack
# Ensures no data loss and quick recovery for client deployments

STACK_DIR="/Users/joshpayneair/Desktop/industrial-iot-stack"
BACKUP_DIR="$STACK_DIR/backups"
FLOWS_DIR="$STACK_DIR/Steel_Bonnet/node-red-flows"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Industrial IoT Stack Backup & Recovery System${NC}"
echo "================================================"

# Create backup directory
mkdir -p "$BACKUP_DIR"

backup_system() {
    echo -e "${YELLOW}📦 Creating system backup...${NC}"
    
    # Create timestamped backup
    BACKUP_NAME="iiot_stack_backup_$TIMESTAMP"
    BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
    mkdir -p "$BACKUP_PATH"
    
    # Backup Node-RED flows
    if [ -f "$FLOWS_DIR/flows.json" ]; then
        cp "$FLOWS_DIR/flows.json" "$BACKUP_PATH/flows.json"
        echo "✓ Node-RED flows backed up"
    fi
    
    # Backup credentials if they exist
    if [ -f "$FLOWS_DIR/flows_cred.json" ]; then
        cp "$FLOWS_DIR/flows_cred.json" "$BACKUP_PATH/flows_cred.json"
        echo "✓ Node-RED credentials backed up"
    fi
    
    # Backup key configuration files
    cp "$STACK_DIR/CLIENT_CONTEXT.md" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  CLIENT_CONTEXT.md not found"
    cp "$STACK_DIR/SCALABILITY_ANALYSIS.md" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  SCALABILITY_ANALYSIS.md not found"
    cp "$STACK_DIR/agents/BUILD_MANIFEST.md" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  BUILD_MANIFEST.md not found"
    cp "$STACK_DIR/agents/SESSION_STATE.json" "$BACKUP_PATH/" 2>/dev/null || echo "⚠️  SESSION_STATE.json not found"
    
    # Backup all agent scripts
    if [ -d "$STACK_DIR/agents" ]; then
        cp -r "$STACK_DIR/agents" "$BACKUP_PATH/"
        echo "✓ Agent scripts backed up"
    fi
    
    # Create backup manifest
    cat > "$BACKUP_PATH/BACKUP_MANIFEST.md" << EOF
# Backup Manifest
**Created**: $(date)
**Purpose**: Full system backup before recovery operations

## Contents
- flows.json - Node-RED flows (original: $(ls -l "$FLOWS_DIR/flows.json" 2>/dev/null | awk '{print $5}') bytes)
- flows_cred.json - Node-RED credentials (if exists)
- CLIENT_CONTEXT.md - Customer requirements and context
- SCALABILITY_ANALYSIS.md - Memory fixes and architecture analysis
- BUILD_MANIFEST.md - Build progress tracking
- SESSION_STATE.json - Current session state
- agents/ - All build and test agents

## Recovery Instructions
1. Stop Node-RED: \`pkill -f node-red\`
2. Restore flows: \`cp flows.json $FLOWS_DIR/\`
3. Start Node-RED: \`cd $FLOWS_DIR && node-red --max-old-space-size=8192\`

## Backup Status
$(du -sh "$BACKUP_PATH" | awk '{print $1}') total backup size
EOF
    
    echo -e "${GREEN}✅ Backup completed: $BACKUP_NAME${NC}"
    echo -e "   Location: $BACKUP_PATH"
    echo -e "   Size: $(du -sh "$BACKUP_PATH" | awk '{print $1}')"
}

list_backups() {
    echo -e "${BLUE}📋 Available Backups:${NC}"
    if [ -d "$BACKUP_DIR" ]; then
        ls -la "$BACKUP_DIR" | grep "iiot_stack_backup" | awk '{print "   " $9 " (" $5 " bytes, " $6 " " $7 " " $8 ")"}'
        
        # Also check for flows.json backups
        echo -e "\n${BLUE}Node-RED Flow Backups:${NC}"
        ls -la "$FLOWS_DIR"/*.backup* 2>/dev/null | awk '{print "   " $9 " (" $5 " bytes, " $6 " " $7 " " $8 ")"}' || echo "   No flow backups found"
    else
        echo "   No backups found"
    fi
}

restore_flows() {
    echo -e "${YELLOW}🔄 Restoring Node-RED flows...${NC}"
    
    # Check for available backups
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/iiot_stack_backup_*/flows.json 2>/dev/null | head -1)
    FLOWS_BACKUP=$(ls -t "$FLOWS_DIR"/flows.json.backup* 2>/dev/null | head -1)
    
    if [ -f "$LATEST_BACKUP" ]; then
        echo "Using latest system backup: $(basename $(dirname "$LATEST_BACKUP"))"
        cp "$LATEST_BACKUP" "$FLOWS_DIR/flows.json"
        echo -e "${GREEN}✅ Flows restored from system backup${NC}"
    elif [ -f "$FLOWS_BACKUP" ]; then
        echo "Using flows backup: $(basename "$FLOWS_BACKUP")"
        cp "$FLOWS_BACKUP" "$FLOWS_DIR/flows.json"
        echo -e "${GREEN}✅ Flows restored from flows backup${NC}"
    else
        echo -e "${RED}❌ No backup files found!${NC}"
        return 1
    fi
}

start_node_red() {
    echo -e "${YELLOW}🚀 Starting Node-RED...${NC}"
    
    # Kill any existing processes
    pkill -f node-red 2>/dev/null || true
    sleep 2
    
    cd "$FLOWS_DIR"
    
    # Start Node-RED in background
    nohup node-red --max-old-space-size=8192 > node-red.log 2>&1 &
    NODE_RED_PID=$!
    
    echo "Node-RED starting with PID: $NODE_RED_PID"
    
    # Wait for startup
    for i in {1..30}; do
        if curl -s http://localhost:1880 > /dev/null 2>&1; then
            echo -e "${GREEN}✅ Node-RED is running at http://localhost:1880${NC}"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    
    echo -e "\n${RED}❌ Node-RED failed to start${NC}"
    return 1
}

quick_recovery() {
    echo -e "${BLUE}🚨 Quick Recovery Mode${NC}"
    backup_system
    restore_flows
    start_node_red
}

health_check() {
    echo -e "${BLUE}🏥 System Health Check${NC}"
    
    # Check Node-RED process
    if pgrep -f node-red > /dev/null; then
        echo -e "${GREEN}✅ Node-RED process running${NC}"
    else
        echo -e "${RED}❌ Node-RED not running${NC}"
    fi
    
    # Check HTTP accessibility
    if curl -s http://localhost:1880 > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Node-RED web interface accessible${NC}"
    else
        echo -e "${RED}❌ Node-RED web interface not accessible${NC}"
    fi
    
    # Check flows file
    if [ -f "$FLOWS_DIR/flows.json" ]; then
        FLOW_SIZE=$(ls -l "$FLOWS_DIR/flows.json" | awk '{print $5}')
        echo -e "${GREEN}✅ flows.json exists (${FLOW_SIZE} bytes)${NC}"
        
        # Validate JSON
        if node -e "JSON.parse(require('fs').readFileSync('$FLOWS_DIR/flows.json', 'utf8'))" 2>/dev/null; then
            echo -e "${GREEN}✅ flows.json is valid JSON${NC}"
        else
            echo -e "${RED}❌ flows.json is corrupted${NC}"
        fi
    else
        echo -e "${RED}❌ flows.json missing${NC}"
    fi
    
    # Check log for errors
    if [ -f "$FLOWS_DIR/node-red.log" ]; then
        ERROR_COUNT=$(grep -c "ERROR\|FATAL" "$FLOWS_DIR/node-red.log" 2>/dev/null || echo "0")
        if [ "$ERROR_COUNT" -gt 0 ]; then
            echo -e "${YELLOW}⚠️  $ERROR_COUNT errors found in log${NC}"
        else
            echo -e "${GREEN}✅ No critical errors in log${NC}"
        fi
    fi
}

# Main menu
case "${1:-menu}" in
    "backup")
        backup_system
        ;;
    "list")
        list_backups
        ;;
    "restore")
        restore_flows
        ;;
    "start")
        start_node_red
        ;;
    "recovery")
        quick_recovery
        ;;
    "health")
        health_check
        ;;
    "menu"|*)
        echo "Usage: $0 {backup|list|restore|start|recovery|health}"
        echo ""
        echo "Commands:"
        echo "  backup   - Create full system backup"
        echo "  list     - List available backups"
        echo "  restore  - Restore flows from latest backup"
        echo "  start    - Start Node-RED with proper memory settings"
        echo "  recovery - Full recovery: backup + restore + start"
        echo "  health   - Check system health status"
        ;;
esac