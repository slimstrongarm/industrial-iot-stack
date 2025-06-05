#!/bin/bash
# Migration script to comprehensive docker-compose setup
# This preserves existing data while reorganizing services

echo "🔄 Industrial IoT Stack Migration Script"
echo "========================================"
echo ""
echo "This script will migrate to a comprehensive docker-compose setup"
echo "while preserving all existing data and configurations."
echo ""

# Check if Docker is working
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Ensure system-wide Docker wrappers are installed."
    exit 1
fi

echo "✅ Docker found: $(docker --version)"
echo ""

# Backup current state
echo "📦 Creating backup of current state..."
BACKUP_DIR="backups/migration-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup current docker-compose.yml
cp docker-compose.yml "$BACKUP_DIR/docker-compose-original.yml"
echo "✅ Backed up original docker-compose.yml"

# Export current container configurations
echo "📋 Documenting current container state..."
docker ps > "$BACKUP_DIR/running-containers.txt"
docker images > "$BACKUP_DIR/docker-images.txt"
docker volume ls > "$BACKUP_DIR/docker-volumes.txt"
docker network ls > "$BACKUP_DIR/docker-networks.txt"

# Create container inspection backups
for container in $(docker ps --format "{{.Names}}"); do
    echo "  📊 Backing up $container configuration..."
    docker inspect "$container" > "$BACKUP_DIR/${container}-config.json"
done

echo "✅ Current state documented in $BACKUP_DIR"
echo ""

# Validate comprehensive compose file
echo "🔍 Validating comprehensive docker-compose.yml..."
if docker-compose -f docker-compose-comprehensive.yml config > /dev/null 2>&1; then
    echo "✅ Comprehensive compose file is valid"
else
    echo "❌ Comprehensive compose file has errors"
    docker-compose -f docker-compose-comprehensive.yml config
    exit 1
fi

echo ""
echo "🔄 Migration Options:"
echo "1. Test migration (bring up services alongside existing)"
echo "2. Full migration (replace current setup)"
echo "3. Cancel migration"
echo ""

read -p "Choose option (1-3): " choice

case $choice in
    1)
        echo "🧪 Testing comprehensive setup alongside existing services..."
        echo "This will use different ports to avoid conflicts."
        
        # Create test version with different ports
        cp docker-compose-comprehensive.yml docker-compose-test.yml
        sed -i 's/1883:1883/1884:1883/g' docker-compose-test.yml
        sed -i 's/5432:5432/5433:5432/g' docker-compose-test.yml
        sed -i 's/1880:1880/1881:1880/g' docker-compose-test.yml
        sed -i 's/18083:18083/18084:18083/g' docker-compose-test.yml
        
        docker-compose -f docker-compose-test.yml up -d
        echo "✅ Test environment started on alternate ports"
        echo "   EMQX Dashboard: http://localhost:18084"
        echo "   Node-RED: http://localhost:1881"
        echo "   TimescaleDB: localhost:5433"
        ;;
        
    2)
        echo "⚠️  FULL MIGRATION SELECTED"
        echo "This will stop current containers and start comprehensive setup."
        echo "All data will be preserved through Docker volumes."
        echo ""
        read -p "Are you sure? (yes/no): " confirm
        
        if [ "$confirm" = "yes" ]; then
            echo "🛑 Stopping current containers gracefully..."
            docker stop emqxnodec timescaledb nodered || true
            
            echo "🔄 Backing up current docker-compose.yml..."
            mv docker-compose.yml docker-compose-original.yml
            
            echo "🔄 Installing comprehensive docker-compose.yml..."
            cp docker-compose-comprehensive.yml docker-compose.yml
            
            echo "🚀 Starting comprehensive IoT stack..."
            docker-compose up -d
            
            echo "✅ Migration complete!"
            echo ""
            echo "📊 Service Status:"
            docker-compose ps
            
        else
            echo "❌ Migration cancelled"
        fi
        ;;
        
    3)
        echo "❌ Migration cancelled"
        exit 0
        ;;
        
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "📋 Migration Summary:"
echo "  • Backup location: $BACKUP_DIR"
echo "  • Comprehensive compose: docker-compose-comprehensive.yml"
echo "  • Current compose: docker-compose.yml"
echo ""
echo "🔧 Useful commands:"
echo "  • View logs: docker-compose logs -f"
echo "  • Restart services: docker-compose restart"
echo "  • Stop services: docker-compose down"
echo "  • View status: docker-compose ps"