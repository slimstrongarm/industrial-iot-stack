-- Industrial Network Discovery Database Schema
-- SQLite schema for device discovery and classification

CREATE TABLE IF NOT EXISTS discovered_devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip_address TEXT NOT NULL,
    mac_address TEXT,
    hostname TEXT,
    device_type TEXT,
    manufacturer TEXT,
    model TEXT,
    firmware_version TEXT,
    protocols TEXT, -- JSON array of supported protocols
    ports TEXT, -- JSON array of open ports
    services TEXT, -- JSON array of discovered services
    confidence_score REAL DEFAULT 0.0,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'active', -- active, inactive, unreachable
    security_zone TEXT,
    tags TEXT, -- JSON array of device tags
    raw_discovery_data TEXT, -- JSON blob of raw scan data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS protocol_endpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    protocol TEXT NOT NULL,
    port INTEGER NOT NULL,
    endpoint_url TEXT,
    authentication_required BOOLEAN DEFAULT FALSE,
    ssl_enabled BOOLEAN DEFAULT FALSE,
    response_time_ms INTEGER,
    last_response TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES discovered_devices(id)
);

CREATE TABLE IF NOT EXISTS scan_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    scan_type TEXT NOT NULL, -- full, targeted, scheduled
    network_ranges TEXT, -- JSON array of scanned ranges
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    devices_found INTEGER DEFAULT 0,
    total_hosts_scanned INTEGER DEFAULT 0,
    status TEXT DEFAULT 'running', -- running, completed, failed, stopped
    error_log TEXT,
    config_snapshot TEXT, -- JSON snapshot of scan configuration
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS device_classifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    classification_type TEXT NOT NULL, -- manufacturer, device_type, model
    classification_value TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    classification_method TEXT, -- ai_fingerprint, port_scan, protocol_response
    evidence TEXT, -- JSON blob of classification evidence
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (device_id) REFERENCES discovered_devices(id)
);

CREATE TABLE IF NOT EXISTS network_topology (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_device_id INTEGER NOT NULL,
    target_device_id INTEGER NOT NULL,
    connection_type TEXT, -- switch_port, gateway, peer
    hop_count INTEGER DEFAULT 1,
    latency_ms REAL,
    bandwidth_mbps REAL,
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_device_id) REFERENCES discovered_devices(id),
    FOREIGN KEY (target_device_id) REFERENCES discovered_devices(id)
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    target_ip TEXT,
    target_port INTEGER,
    protocol TEXT,
    user_agent TEXT DEFAULT 'industrial-discovery-engine',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    session_id TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_devices_ip ON discovered_devices(ip_address);
CREATE INDEX IF NOT EXISTS idx_devices_mac ON discovered_devices(mac_address);
CREATE INDEX IF NOT EXISTS idx_devices_type ON discovered_devices(device_type);
CREATE INDEX IF NOT EXISTS idx_devices_manufacturer ON discovered_devices(manufacturer);
CREATE INDEX IF NOT EXISTS idx_devices_status ON discovered_devices(status);
CREATE INDEX IF NOT EXISTS idx_devices_last_seen ON discovered_devices(last_seen);

CREATE INDEX IF NOT EXISTS idx_endpoints_device ON protocol_endpoints(device_id);
CREATE INDEX IF NOT EXISTS idx_endpoints_protocol ON protocol_endpoints(protocol);
CREATE INDEX IF NOT EXISTS idx_endpoints_port ON protocol_endpoints(port);

CREATE INDEX IF NOT EXISTS idx_sessions_status ON scan_sessions(status);
CREATE INDEX IF NOT EXISTS idx_sessions_start_time ON scan_sessions(start_time);

CREATE INDEX IF NOT EXISTS idx_classifications_device ON device_classifications(device_id);
CREATE INDEX IF NOT EXISTS idx_classifications_type ON device_classifications(classification_type);

CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_target_ip ON audit_log(target_ip);

-- Views for common queries
CREATE VIEW IF NOT EXISTS active_devices AS
SELECT 
    d.*,
    COUNT(pe.id) as endpoint_count,
    GROUP_CONCAT(DISTINCT pe.protocol) as protocols_list
FROM discovered_devices d
LEFT JOIN protocol_endpoints pe ON d.id = pe.device_id
WHERE d.status = 'active'
GROUP BY d.id;

CREATE VIEW IF NOT EXISTS device_summary AS
SELECT 
    manufacturer,
    device_type,
    COUNT(*) as device_count,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_count,
    AVG(confidence_score) as avg_confidence
FROM discovered_devices
GROUP BY manufacturer, device_type;

-- Triggers for automatic timestamp updates
CREATE TRIGGER IF NOT EXISTS update_device_timestamp
    AFTER UPDATE ON discovered_devices
BEGIN
    UPDATE discovered_devices 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_endpoint_timestamp
    AFTER UPDATE ON protocol_endpoints
BEGIN
    UPDATE protocol_endpoints 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;