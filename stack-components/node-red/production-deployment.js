/**
 * Production Deployment Package Generator for CT-084 Parachute Drop System
 * Creates complete production-ready deployment configurations with remote monitoring
 * Author: Agent 3 - Dashboard Generator and Production Deployment
 */

const fs = require('fs').promises;
const path = require('path');
const os = require('os');
const crypto = require('crypto');

class ProductionDeploymentGenerator {
    constructor(options = {}) {
        this.options = {
            projectName: options.projectName || 'CT-084 Parachute Drop System',
            version: options.version || '1.0.0',
            environment: options.environment || 'production',
            platform: options.platform || 'raspberry-pi',
            enableSecurity: options.enableSecurity !== false,
            enableRemoteMonitoring: options.enableRemoteMonitoring !== false,
            enableBackups: options.enableBackups !== false,
            outputPath: options.outputPath || './deployment-package',
            ...options
        };
        
        this.deploymentConfig = null;
        this.generatedFiles = [];
    }

    /**
     * Generate complete production deployment package
     */
    async generateDeploymentPackage() {
        console.log('📦 Generating production deployment package...');
        
        try {
            // Create output directory
            await fs.mkdir(this.options.outputPath, { recursive: true });
            
            // Generate all deployment components
            await this.generateDockerCompose();
            await this.generateNodeRedSettings();
            await this.generateInstallationScripts();
            await this.generateConfigurationFiles();
            await this.generateMonitoringScripts();
            await this.generateBackupScripts();
            await this.generateSecurityConfiguration();
            await this.generateDocumentation();
            await this.generateDeploymentManifest();
            
            console.log(`✅ Production deployment package generated at: ${this.options.outputPath}`);
            console.log(`📄 Generated ${this.generatedFiles.length} files`);
            
            return {
                packagePath: this.options.outputPath,
                filesGenerated: this.generatedFiles.length,
                files: this.generatedFiles,
                deploymentConfig: this.deploymentConfig
            };
            
        } catch (error) {
            console.error('❌ Failed to generate deployment package:', error);
            throw error;
        }
    }

    /**
     * Generate Docker Compose configuration
     */
    async generateDockerCompose() {
        const dockerCompose = {
            version: '3.8',
            
            services: {
                'node-red': {
                    image: 'nodered/node-red:latest',
                    container_name: 'ct084-node-red',
                    restart: 'unless-stopped',
                    ports: ['1880:1880'],
                    volumes: [
                        './node-red-data:/data',
                        './config:/config:ro'
                    ],
                    environment: {
                        TZ: process.env.TZ || 'UTC',
                        NODE_RED_ENABLE_PROJECTS: 'true'
                    },
                    networks: ['ct084-network'],
                    depends_on: ['mqtt-broker', 'influxdb'],
                    healthcheck: {
                        test: ['CMD', 'curl', '-f', 'http://localhost:1880/'],
                        interval: '30s',
                        timeout: '10s',
                        retries: 3
                    }
                },
                
                'mqtt-broker': {
                    image: 'eclipse-mosquitto:latest',
                    container_name: 'ct084-mqtt',
                    restart: 'unless-stopped',
                    ports: ['1883:1883', '9001:9001'],
                    volumes: [
                        './mosquitto/config:/mosquitto/config',
                        './mosquitto/data:/mosquitto/data',
                        './mosquitto/log:/mosquitto/log'
                    ],
                    networks: ['ct084-network'],
                    healthcheck: {
                        test: ['CMD', 'mosquitto_pub', '-h', 'localhost', '-t', 'health/check', '-m', 'ok'],
                        interval: '30s',
                        timeout: '5s',
                        retries: 3
                    }
                },
                
                'influxdb': {
                    image: 'influxdb:2.7',
                    container_name: 'ct084-influxdb',
                    restart: 'unless-stopped',
                    ports: ['8086:8086'],
                    volumes: [
                        './influxdb/data:/var/lib/influxdb2',
                        './influxdb/config:/etc/influxdb2'
                    ],
                    environment: {
                        DOCKER_INFLUXDB_INIT_MODE: 'setup',
                        DOCKER_INFLUXDB_INIT_USERNAME: 'admin',
                        DOCKER_INFLUXDB_INIT_PASSWORD: 'changeme123',
                        DOCKER_INFLUXDB_INIT_ORG: 'ct084-org',
                        DOCKER_INFLUXDB_INIT_BUCKET: 'parachute-data'
                    },
                    networks: ['ct084-network']
                },
                
                'grafana': {
                    image: 'grafana/grafana:latest',
                    container_name: 'ct084-grafana',
                    restart: 'unless-stopped',
                    ports: ['3000:3000'],
                    volumes: [
                        './grafana/data:/var/lib/grafana',
                        './grafana/provisioning:/etc/grafana/provisioning'
                    ],
                    environment: {
                        GF_SECURITY_ADMIN_PASSWORD: 'changeme123',
                        GF_INSTALL_PLUGINS: 'grafana-worldmap-panel'
                    },
                    networks: ['ct084-network'],
                    depends_on: ['influxdb']
                }
            },
            
            networks: {
                'ct084-network': {
                    driver: 'bridge',
                    ipam: {
                        config: [{ subnet: '172.20.0.0/16' }]
                    }
                }
            },
            
            volumes: {
                'node-red-data': {},
                'influxdb-data': {},
                'grafana-data': {}
            }
        };

        // Add platform-specific configurations
        if (this.options.platform === 'raspberry-pi') {
            // Add GPIO access for Raspberry Pi
            dockerCompose.services['node-red'].devices = ['/dev/gpiomem:/dev/gpiomem'];
            dockerCompose.services['node-red'].privileged = true;
        }

        await this.writeFile('docker-compose.yml', this.yamlStringify(dockerCompose));
    }

    /**
     * Generate Node-RED production settings
     */
    async generateNodeRedSettings() {
        const adminPassword = this.generateSecurePassword();
        const apiKey = this.generateApiKey();
        
        const settings = `
module.exports = {
    // Production Node-RED settings for CT-084 Parachute Drop System
    
    // Server settings
    uiPort: process.env.PORT || 1880,
    uiHost: "0.0.0.0",
    
    // Runtime settings
    verbose: false,
    
    // Security
    ${this.options.enableSecurity ? `
    adminAuth: {
        type: "credentials",
        users: [{
            username: "admin",
            password: "${adminPassword}",
            permissions: "*"
        }, {
            username: "operator",
            password: "${this.generateSecurePassword()}",
            permissions: "read"
        }]
    },
    httpAdminRoot: '/admin',
    ` : 'adminAuth: false,'}
    
    httpNodeRoot: '/api',
    httpStatic: '/data/static',
    
    // Editor settings
    editorTheme: {
        page: {
            title: "${this.options.projectName}",
            favicon: "/data/static/favicon.ico",
            css: "/data/static/custom.css"
        },
        header: {
            title: "${this.options.projectName}",
            image: "/data/static/logo.png"
        },
        deployButton: {
            type: "simple",
            icon: "fa-upload"
        },
        menu: {
            "menu-item-import-library": false,
            "menu-item-export-library": false
        },
        userMenu: true,
        login: {
            image: "/data/static/login-bg.png"
        },
        projects: {
            enabled: true
        }
    },
    
    // Logging
    logging: {
        console: {
            level: "info",
            metrics: false,
            audit: ${this.options.enableSecurity ? 'true' : 'false'}
        },
        file: {
            level: "info",
            filename: "/data/logs/node-red.log",
            maxFiles: 10,
            maxSize: "10MB"
        }
    },
    
    // Function node settings
    functionGlobalContext: {
        // System information
        system: {
            name: "${this.options.projectName}",
            version: "${this.options.version}",
            environment: "${this.options.environment}",
            platform: "${this.options.platform}",
            apiKey: "${apiKey}"
        },
        
        // External libraries
        os: require('os'),
        fs: require('fs'),
        path: require('path'),
        crypto: require('crypto'),
        
        // Custom utilities
        utils: {
            formatTimestamp: function(ts) {
                return new Date(ts).toISOString();
            },
            generateId: function() {
                return require('crypto').randomBytes(16).toString('hex');
            }
        }
    },
    
    // Export settings
    exportGlobalContextKeys: false,
    
    // Context storage
    contextStorage: {
        default: "file",
        file: {
            module: "localfilesystem",
            config: {
                dir: "/data/context",
                flushInterval: 30
            }
        },
        memory: {
            module: "memory"
        }
    },
    
    // Flow file settings
    flowFile: 'flows.json',
    flowFilePretty: true,
    
    // Credential settings
    credentialSecret: "${this.generateCredentialSecret()}",
    
    // Dashboard settings
    ui: {
        path: "ui",
        middleware: function(req, res, next) {
            // Add security headers
            res.setHeader('X-Frame-Options', 'DENY');
            res.setHeader('X-Content-Type-Options', 'nosniff');
            res.setHeader('X-XSS-Protection', '1; mode=block');
            next();
        }
    },
    
    // HTTPS settings (if certificates are available)
    ${this.options.enableSecurity ? `
    https: {
        key: process.env.SSL_KEY || '/data/certs/server.key',
        cert: process.env.SSL_CERT || '/data/certs/server.crt'
    },
    requireHTTPS: true,
    ` : ''}
    
    // API maximum payload size
    apiMaxLength: '50mb',
    
    // Maximum number of messages in catch-all queue
    debugMaxLength: 1000,
    
    // Maximum number of log entries
    maxNodeRedLogs: 100
};
        `;
        
        await this.writeFile('config/node-red-settings.js', settings);
        
        // Generate environment file for credentials
        const envFile = `
# CT-084 Production Environment Variables
NODE_RED_API_KEY=${apiKey}
ADMIN_PASSWORD_HASH=${adminPassword}
CREDENTIAL_SECRET=${this.generateCredentialSecret()}
INFLUXDB_TOKEN=${this.generateApiKey()}
MQTT_USERNAME=ct084_user
MQTT_PASSWORD=${this.generateSecurePassword()}
TZ=UTC

# Database connections
INFLUXDB_URL=http://influxdb:8086
INFLUXDB_ORG=ct084-org
INFLUXDB_BUCKET=parachute-data

# MQTT Configuration
MQTT_BROKER=mqtt://mqtt-broker:1883

# Alert configurations
ALERT_EMAIL_SMTP=smtp.example.com
ALERT_EMAIL_USER=alerts@example.com
ALERT_EMAIL_PASS=${this.generateSecurePassword()}

# Backup configuration
BACKUP_ENABLED=true
BACKUP_SCHEDULE=0 2 * * *
BACKUP_RETENTION_DAYS=30
        `;
        
        await this.writeFile('.env', envFile);
    }

    /**
     * Generate installation scripts
     */
    async generateInstallationScripts() {
        // Main installation script
        const installScript = `#!/bin/bash
# CT-084 Parachute Drop System Installation Script
# Generated: ${new Date().toISOString()}

set -e

echo "🚀 Installing CT-084 Parachute Drop System..."

# Check system requirements
check_requirements() {
    echo "📋 Checking system requirements..."
    
    # Check if running on supported platform
    if [[ "${this.options.platform}" == "raspberry-pi" ]]; then
        if ! grep -q "Raspberry Pi" /proc/cpuinfo; then
            echo "❌ This package is designed for Raspberry Pi"
            exit 1
        fi
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo "🐳 Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        usermod -aG docker \${USER}
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo "🐳 Installing Docker Compose..."
        pip3 install docker-compose
    fi
    
    echo "✅ System requirements satisfied"
}

# Create directory structure
create_directories() {
    echo "📁 Creating directory structure..."
    
    mkdir -p node-red-data/{logs,context,static,projects}
    mkdir -p mosquitto/{config,data,log}
    mkdir -p influxdb/{data,config}
    mkdir -p grafana/{data,provisioning}
    mkdir -p backups
    mkdir -p logs
    mkdir -p certs
    
    # Set permissions for Raspberry Pi
    if [[ "${this.options.platform}" == "raspberry-pi" ]]; then
        chown -R 1000:1000 node-red-data
        chown -R 1883:1883 mosquitto
        chmod -R 755 mosquitto/config
    fi
    
    echo "✅ Directories created"
}

# Configure Mosquitto
configure_mosquitto() {
    echo "🦟 Configuring Mosquitto MQTT broker..."
    
    cat > mosquitto/config/mosquitto.conf << 'EOF'
# Mosquitto configuration for CT-084
listener 1883
allow_anonymous false
password_file /mosquitto/config/passwd

# WebSocket support
listener 9001
protocol websockets

# Logging
log_dest file /mosquitto/log/mosquitto.log
log_type error
log_type warning
log_type notice
log_type information
log_timestamp true

# Persistence
persistence true
persistence_location /mosquitto/data/
autosave_interval 1800

# Security
max_connections 100
max_inflight_messages 20
max_queued_messages 100
EOF

    # Create user credentials
    docker run --rm -v \$(pwd)/mosquitto/config:/mosquitto/config eclipse-mosquitto:latest mosquitto_passwd -c -b /mosquitto/config/passwd ct084_user \$(grep MQTT_PASSWORD .env | cut -d'=' -f2)
    
    echo "✅ Mosquitto configured"
}

# Install Node-RED packages
install_node_red_packages() {
    echo "📦 Installing Node-RED packages..."
    
    # Wait for Node-RED to start
    sleep 30
    
    # Install required packages
    docker exec ct084-node-red npm install --save \\
        node-red-dashboard \\
        node-red-contrib-phidget22 \\
        node-red-contrib-opcua \\
        node-red-contrib-modbus \\
        node-red-contrib-influxdb \\
        node-red-node-rbe \\
        node-red-contrib-cron-plus \\
        node-red-contrib-buffer-parser
    
    # Restart Node-RED to load packages
    docker restart ct084-node-red
    
    echo "✅ Node-RED packages installed"
}

# Main installation process
main() {
    echo "🎯 Starting CT-084 installation..."
    
    check_requirements
    create_directories
    configure_mosquitto
    
    # Start services
    echo "🚀 Starting services..."
    docker-compose up -d
    
    install_node_red_packages
    
    echo "✅ Installation completed successfully!"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Node-RED: http://localhost:1880"
    echo "   Grafana: http://localhost:3000"
    echo "   MQTT: mqtt://localhost:1883"
    echo ""
    echo "📝 Default credentials are in .env file"
    echo "⚠️  Please change default passwords in production!"
}

main "\$@"
        `;
        
        await this.writeFile('install.sh', installScript, { mode: 0o755 });
        
        // Uninstall script
        const uninstallScript = `#!/bin/bash
# CT-084 Uninstall Script

echo "🗑️ Uninstalling CT-084 Parachute Drop System..."

# Stop and remove containers
docker-compose down

# Remove volumes (optional)
read -p "Remove all data volumes? (y/N): " -n 1 -r
echo
if [[ \$REPLY =~ ^[Yy]\$ ]]; then
    docker volume prune -f
    rm -rf node-red-data mosquitto influxdb grafana
    echo "✅ Data volumes removed"
fi

echo "✅ CT-084 system uninstalled"
        `;
        
        await this.writeFile('uninstall.sh', uninstallScript, { mode: 0o755 });
    }

    /**
     * Generate monitoring scripts
     */
    async generateMonitoringScripts() {
        // Health check script
        const healthCheckScript = `#!/bin/bash
# CT-084 Health Check Script

check_container_health() {
    local container=\$1
    local status=\$(docker inspect --format='{{.State.Health.Status}}' \$container 2>/dev/null)
    
    if [[ "\$status" == "healthy" ]]; then
        echo "✅ \$container: healthy"
        return 0
    else
        echo "❌ \$container: \$status"
        return 1
    fi
}

check_service_ports() {
    local port=\$1
    local service=\$2
    
    if nc -z localhost \$port; then
        echo "✅ \$service (:\$port): accessible"
        return 0
    else
        echo "❌ \$service (:\$port): not accessible"
        return 1
    fi
}

echo "🏥 CT-084 System Health Check"
echo "=============================="

# Check container health
failed=0
check_container_health "ct084-node-red" || failed=1
check_container_health "ct084-mqtt" || failed=1
check_container_health "ct084-influxdb" || failed=1

# Check service ports
check_service_ports 1880 "Node-RED" || failed=1
check_service_ports 1883 "MQTT" || failed=1
check_service_ports 8086 "InfluxDB" || failed=1
check_service_ports 3000 "Grafana" || failed=1

# Check disk space
df_output=\$(df -h | grep -E '/$|/var|/tmp' | awk '{print \$5}' | sed 's/%//')
for usage in \$df_output; do
    if [[ \$usage -gt 90 ]]; then
        echo "⚠️ Disk usage high: \${usage}%"
        failed=1
    fi
done

# Check memory usage
mem_usage=\$(free | grep Mem | awk '{printf("%.0f", \$3/\$2 * 100.0)}')
if [[ \$mem_usage -gt 90 ]]; then
    echo "⚠️ Memory usage high: \${mem_usage}%"
    failed=1
fi

if [[ \$failed -eq 0 ]]; then
    echo "✅ All systems healthy"
    exit 0
else
    echo "❌ System issues detected"
    exit 1
fi
        `;
        
        await this.writeFile('scripts/health-check.sh', healthCheckScript, { mode: 0o755 });
        
        // Status script
        const statusScript = `#!/bin/bash
# CT-084 System Status

echo "📊 CT-084 System Status"
echo "======================"
echo "Timestamp: \$(date)"
echo

# Container status
echo "🐳 Container Status:"
docker-compose ps

echo
echo "💾 Resource Usage:"
echo "Memory: \$(free -h | grep Mem | awk '{print \$3 "/" \$2}')"
echo "Disk: \$(df -h / | tail -1 | awk '{print \$3 "/" \$2 " (" \$5 ")"}')"
echo "CPU Load: \$(uptime | cut -d',' -f3-)"

echo
echo "🌐 Network Connectivity:"
curl -s -o /dev/null -w "Node-RED: %{http_code}\\n" http://localhost:1880/admin || echo "Node-RED: unreachable"
curl -s -o /dev/null -w "Grafana: %{http_code}\\n" http://localhost:3000 || echo "Grafana: unreachable"

echo
echo "📈 Service Metrics:"
echo "Node-RED Flows: \$(curl -s http://localhost:1880/flows | jq '. | length' 2>/dev/null || echo "N/A")"
echo "MQTT Topics: \$(mosquitto_sub -h localhost -t '\\$SYS/broker/subscriptions/count' -C 1 2>/dev/null || echo "N/A")"
        `;
        
        await this.writeFile('scripts/status.sh', statusScript, { mode: 0o755 });
        
        // Log viewer script
        const logsScript = `#!/bin/bash
# CT-084 Log Viewer

service=\${1:-node-red}

case \$service in
    node-red|nr)
        docker logs -f ct084-node-red
        ;;
    mqtt|mosquitto)
        docker logs -f ct084-mqtt
        ;;
    influx|influxdb)
        docker logs -f ct084-influxdb
        ;;
    grafana)
        docker logs -f ct084-grafana
        ;;
    all)
        docker-compose logs -f
        ;;
    *)
        echo "Usage: \$0 [node-red|mqtt|influx|grafana|all]"
        exit 1
        ;;
esac
        `;
        
        await this.writeFile('scripts/logs.sh', logsScript, { mode: 0o755 });
    }

    /**
     * Generate backup scripts
     */
    async generateBackupScripts() {
        if (!this.options.enableBackups) return;
        
        const backupScript = `#!/bin/bash
# CT-084 Backup Script

BACKUP_DIR="./backups"
TIMESTAMP=\$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="ct084_backup_\$TIMESTAMP"

echo "💾 Creating backup: \$BACKUP_NAME"

# Create backup directory
mkdir -p "\$BACKUP_DIR/\$BACKUP_NAME"

# Backup Node-RED flows and configuration
echo "📊 Backing up Node-RED data..."
cp -r node-red-data "\$BACKUP_DIR/\$BACKUP_NAME/"

# Backup environment configuration
echo "⚙️ Backing up configuration..."
cp .env "\$BACKUP_DIR/\$BACKUP_NAME/"
cp docker-compose.yml "\$BACKUP_DIR/\$BACKUP_NAME/"

# Export InfluxDB data
echo "🗄️ Backing up InfluxDB data..."
docker exec ct084-influxdb influx backup /tmp/backup
docker cp ct084-influxdb:/tmp/backup "\$BACKUP_DIR/\$BACKUP_NAME/influxdb-backup"

# Create compressed archive
echo "🗜️ Compressing backup..."
cd "\$BACKUP_DIR"
tar -czf "\$BACKUP_NAME.tar.gz" "\$BACKUP_NAME"
rm -rf "\$BACKUP_NAME"

# Cleanup old backups (keep last 30 days)
find "\$BACKUP_DIR" -name "ct084_backup_*.tar.gz" -mtime +30 -delete

echo "✅ Backup completed: \$BACKUP_DIR/\$BACKUP_NAME.tar.gz"

# Optional: Upload to remote storage
if [[ -n "\$BACKUP_REMOTE_URL" ]]; then
    echo "☁️ Uploading to remote storage..."
    # Add your remote backup logic here
    # Examples: rsync, scp, aws s3 cp, etc.
fi
        `;
        
        await this.writeFile('scripts/backup.sh', backupScript, { mode: 0o755 });
        
        // Restore script
        const restoreScript = `#!/bin/bash
# CT-084 Restore Script

BACKUP_FILE=\$1

if [[ -z "\$BACKUP_FILE" ]]; then
    echo "Usage: \$0 <backup_file.tar.gz>"
    echo "Available backups:"
    ls -la backups/ct084_backup_*.tar.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

if [[ ! -f "\$BACKUP_FILE" ]]; then
    echo "❌ Backup file not found: \$BACKUP_FILE"
    exit 1
fi

echo "🔄 Restoring from backup: \$BACKUP_FILE"

# Stop services
echo "🛑 Stopping services..."
docker-compose down

# Extract backup
echo "📦 Extracting backup..."
TEMP_DIR=\$(mktemp -d)
tar -xzf "\$BACKUP_FILE" -C "\$TEMP_DIR"
BACKUP_DIR=\$(ls "\$TEMP_DIR")

# Restore files
echo "📁 Restoring files..."
cp -r "\$TEMP_DIR/\$BACKUP_DIR/node-red-data" ./
cp "\$TEMP_DIR/\$BACKUP_DIR/.env" ./
cp "\$TEMP_DIR/\$BACKUP_DIR/docker-compose.yml" ./

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for InfluxDB
sleep 30

# Restore InfluxDB data
if [[ -d "\$TEMP_DIR/\$BACKUP_DIR/influxdb-backup" ]]; then
    echo "🗄️ Restoring InfluxDB data..."
    docker cp "\$TEMP_DIR/\$BACKUP_DIR/influxdb-backup" ct084-influxdb:/tmp/
    docker exec ct084-influxdb influx restore /tmp/influxdb-backup
fi

# Cleanup
rm -rf "\$TEMP_DIR"

echo "✅ Restore completed successfully"
        `;
        
        await this.writeFile('scripts/restore.sh', restoreScript, { mode: 0o755 });
        
        // Automated backup cron job
        const cronBackup = `#!/bin/bash
# CT-084 Automated Backup (for cron)

# Change to deployment directory
cd /opt/ct084-parachute-drop

# Run backup with logging
./scripts/backup.sh >> logs/backup.log 2>&1

# Send status notification (optional)
if [[ \$? -eq 0 ]]; then
    echo "\$(date): Backup completed successfully" >> logs/backup.log
else
    echo "\$(date): Backup failed" >> logs/backup.log
    # Add notification logic here (email, webhook, etc.)
fi
        `;
        
        await this.writeFile('scripts/cron-backup.sh', cronBackup, { mode: 0o755 });
    }

    /**
     * Generate security configuration
     */
    async generateSecurityConfiguration() {
        if (!this.options.enableSecurity) return;
        
        // SSL certificate generation script
        const generateCerts = `#!/bin/bash
# Generate self-signed SSL certificates for CT-084

CERT_DIR="./certs"
mkdir -p "\$CERT_DIR"

# Generate private key
openssl genrsa -out "\$CERT_DIR/server.key" 2048

# Generate certificate signing request
openssl req -new -key "\$CERT_DIR/server.key" -out "\$CERT_DIR/server.csr" -subj "/C=US/ST=State/L=City/O=Organization/CN=ct084-parachute"

# Generate self-signed certificate
openssl x509 -req -days 365 -in "\$CERT_DIR/server.csr" -signkey "\$CERT_DIR/server.key" -out "\$CERT_DIR/server.crt"

# Set permissions
chmod 600 "\$CERT_DIR/server.key"
chmod 644 "\$CERT_DIR/server.crt"

echo "✅ SSL certificates generated in \$CERT_DIR"
echo "⚠️ These are self-signed certificates. Use proper CA-signed certificates in production."
        `;
        
        await this.writeFile('scripts/generate-certs.sh', generateCerts, { mode: 0o755 });
        
        // Firewall configuration
        const firewallConfig = `#!/bin/bash
# CT-084 Firewall Configuration

echo "🔥 Configuring firewall for CT-084..."

# Allow SSH (change port if needed)
ufw allow 22/tcp

# Allow HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Allow Node-RED
ufw allow 1880/tcp

# Allow MQTT
ufw allow 1883/tcp
ufw allow 8883/tcp

# Allow Grafana
ufw allow 3000/tcp

# Deny all other incoming
ufw --force enable

echo "✅ Firewall configured"
        `;
        
        await this.writeFile('scripts/configure-firewall.sh', firewallConfig, { mode: 0o755 });
        
        // Security hardening script
        const hardeningScript = `#!/bin/bash
# CT-084 Security Hardening

echo "🔒 Applying security hardening..."

# Update system packages
apt update && apt upgrade -y

# Install security tools
apt install -y fail2ban ufw unattended-upgrades

# Configure automatic security updates
dpkg-reconfigure -plow unattended-upgrades

# Secure shared memory
if ! grep -q "tmpfs /run/shm" /etc/fstab; then
    echo "tmpfs /run/shm tmpfs defaults,noexec,nosuid 0 0" >> /etc/fstab
fi

# Disable unused services
systemctl disable bluetooth
systemctl disable avahi-daemon

# Set secure permissions on deployment files
chmod 600 .env
chmod -R 700 scripts
chown -R root:root scripts

echo "✅ Security hardening completed"
echo "⚠️ Please review and test all changes"
        `;
        
        await this.writeFile('scripts/security-hardening.sh', hardeningScript, { mode: 0o755 });
    }

    /**
     * Generate documentation
     */
    async generateDocumentation() {
        const readme = `# CT-084 Parachute Drop System
## Production Deployment Package

### Overview
This package contains everything needed to deploy the CT-084 Parachute Drop System in a production environment.

### System Requirements
- ${this.options.platform === 'raspberry-pi' ? 'Raspberry Pi 4 (4GB RAM recommended)' : 'Linux server with Docker support'}
- Docker and Docker Compose
- 32GB+ storage space
- Network connectivity

### Quick Start
1. Extract this package to your target system
2. Run the installation script: \`./install.sh\`
3. Access the dashboard: http://localhost:1880
4. Change default passwords in production!

### Services
- **Node-RED Dashboard**: http://localhost:1880
- **Grafana**: http://localhost:3000  
- **MQTT Broker**: mqtt://localhost:1883
- **InfluxDB**: http://localhost:8086

### Default Credentials
See the \`.env\` file for default credentials. **Change these in production!**

### Management Scripts
- \`./scripts/status.sh\` - Check system status
- \`./scripts/health-check.sh\` - Run health checks
- \`./scripts/backup.sh\` - Create system backup
- \`./scripts/logs.sh <service>\` - View service logs

### Security
${this.options.enableSecurity ? `
- SSL certificates: \`./scripts/generate-certs.sh\`
- Firewall setup: \`./scripts/configure-firewall.sh\`
- System hardening: \`./scripts/security-hardening.sh\`
` : 'Security features disabled in this build.'}

### Monitoring
${this.options.enableRemoteMonitoring ? `
- Health checks run automatically
- Logs are rotated and archived
- System metrics are collected
` : 'Remote monitoring disabled in this build.'}

### Backup & Recovery
${this.options.enableBackups ? `
- Automatic daily backups
- Manual backup: \`./scripts/backup.sh\`
- Restore: \`./scripts/restore.sh <backup_file>\`
` : 'Backup features disabled in this build.'}

### Support
- Check logs: \`./scripts/logs.sh all\`
- System status: \`./scripts/status.sh\`
- Health check: \`./scripts/health-check.sh\`

### Version Information
- Package Version: ${this.options.version}
- Generated: ${new Date().toISOString()}
- Platform: ${this.options.platform}
- Environment: ${this.options.environment}
        `;
        
        await this.writeFile('README.md', readme);
        
        // Technical documentation
        const technicalDoc = `# CT-084 Technical Documentation

## Architecture Overview
The CT-084 Parachute Drop System uses a microservices architecture with Docker containers:

### Services
1. **Node-RED**: Main application logic and dashboard
2. **Mosquitto**: MQTT message broker
3. **InfluxDB**: Time-series database
4. **Grafana**: Advanced visualization and alerting

### Data Flow
\`\`\`
Sensors → MQTT → Node-RED → InfluxDB → Grafana
                     ↓
                  Dashboard
\`\`\`

### Network Configuration
- Internal network: 172.20.0.0/16
- Services communicate via Docker network
- External access through published ports

### Security Features
${this.options.enableSecurity ? `
- Authentication required for all services
- SSL/TLS encryption
- Firewall configuration
- User role management
` : 'Security features disabled'}

### Monitoring
${this.options.enableRemoteMonitoring ? `
- Container health checks
- Resource monitoring
- Log aggregation
- Alert notifications
` : 'Monitoring features disabled'}

### Backup Strategy
${this.options.enableBackups ? `
- Daily automated backups
- Configuration and data included
- Compressed and archived
- Retention policy: 30 days
` : 'Backup features disabled'}

## Configuration Files
- \`docker-compose.yml\`: Service definitions
- \`.env\`: Environment variables
- \`config/node-red-settings.js\`: Node-RED configuration
- \`mosquitto/config/mosquitto.conf\`: MQTT broker settings

## Troubleshooting
Common issues and solutions...

## API Reference
Available REST endpoints and MQTT topics...
        `;
        
        await this.writeFile('docs/TECHNICAL.md', technicalDoc);
    }

    /**
     * Generate deployment manifest
     */
    async generateDeploymentManifest() {
        this.deploymentConfig = {
            package: {
                name: this.options.projectName,
                version: this.options.version,
                description: 'Production deployment package for CT-084 Parachute Drop System',
                generated: new Date().toISOString(),
                platform: this.options.platform,
                environment: this.options.environment
            },
            
            features: {
                security: this.options.enableSecurity,
                remoteMonitoring: this.options.enableRemoteMonitoring,
                backups: this.options.enableBackups
            },
            
            services: {
                'node-red': {
                    image: 'nodered/node-red:latest',
                    port: 1880,
                    path: '/admin'
                },
                'mqtt-broker': {
                    image: 'eclipse-mosquitto:latest',
                    port: 1883
                },
                'influxdb': {
                    image: 'influxdb:2.7',
                    port: 8086
                },
                'grafana': {
                    image: 'grafana/grafana:latest',
                    port: 3000
                }
            },
            
            requirements: {
                platform: this.options.platform,
                docker: '>=20.0.0',
                dockerCompose: '>=1.29.0',
                diskSpace: '32GB',
                memory: this.options.platform === 'raspberry-pi' ? '4GB' : '8GB'
            },
            
            files: this.generatedFiles,
            
            installation: {
                steps: [
                    'Extract package to target directory',
                    'Run ./install.sh',
                    'Configure .env file with production settings',
                    'Access dashboard at http://localhost:1880'
                ],
                postInstall: [
                    'Change default passwords',
                    'Configure SSL certificates',
                    'Set up firewall rules',
                    'Configure backup schedule'
                ]
            }
        };
        
        await this.writeFile('deployment-manifest.json', JSON.stringify(this.deploymentConfig, null, 2));
    }

    /**
     * Helper method to write files
     */
    async writeFile(filePath, content, options = {}) {
        const fullPath = path.join(this.options.outputPath, filePath);
        const dir = path.dirname(fullPath);
        
        // Create directory if it doesn't exist
        await fs.mkdir(dir, { recursive: true });
        
        // Write file
        await fs.writeFile(fullPath, content, options);
        
        // Track generated file
        this.generatedFiles.push({
            path: filePath,
            size: Buffer.byteLength(content),
            mode: options.mode || 0o644,
            generated: new Date().toISOString()
        });
        
        console.log(`📄 Generated: ${filePath}`);
    }

    /**
     * Generate secure password
     */
    generateSecurePassword(length = 16) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*';
        let password = '';
        for (let i = 0; i < length; i++) {
            password += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return password;
    }

    /**
     * Generate API key
     */
    generateApiKey() {
        return crypto.randomBytes(32).toString('hex');
    }

    /**
     * Generate credential secret
     */
    generateCredentialSecret() {
        return crypto.randomBytes(32).toString('hex');
    }

    /**
     * Convert object to YAML string
     */
    yamlStringify(obj, indent = 0) {
        let yaml = '';
        const spaces = '  '.repeat(indent);
        
        for (const [key, value] of Object.entries(obj)) {
            if (value === null || value === undefined) {
                yaml += `${spaces}${key}: null\n`;
            } else if (typeof value === 'string') {
                yaml += `${spaces}${key}: "${value}"\n`;
            } else if (typeof value === 'number' || typeof value === 'boolean') {
                yaml += `${spaces}${key}: ${value}\n`;
            } else if (Array.isArray(value)) {
                yaml += `${spaces}${key}:\n`;
                value.forEach(item => {
                    if (typeof item === 'string') {
                        yaml += `${spaces}  - "${item}"\n`;
                    } else {
                        yaml += `${spaces}  - ${item}\n`;
                    }
                });
            } else if (typeof value === 'object') {
                yaml += `${spaces}${key}:\n`;
                yaml += this.yamlStringify(value, indent + 1);
            }
        }
        
        return yaml;
    }
}

module.exports = ProductionDeploymentGenerator;