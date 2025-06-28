#!/usr/bin/env python3
"""
CT-086 Agent 4: Authentication & Access Control Manager
Enterprise-grade authentication and access control for Parachute Drop system

This agent provides multi-factor authentication, role-based access control,
and security hardening for remote access to industrial networks.
"""

import os
import json
import sqlite3
import hashlib
import secrets
import time
import logging
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import jwt
import pyotp
import qrcode
from cryptography.fernet import Fernet
import bcrypt


class UserRole(Enum):
    """User roles for access control"""
    ADMIN = "admin"
    ENGINEER = "engineer"
    TECHNICIAN = "technician"
    OPERATOR = "operator"
    VIEWER = "viewer"
    GUEST = "guest"


class AccessLevel(Enum):
    """Network access levels"""
    FULL = "full"
    MANAGEMENT = "management"
    INDUSTRIAL = "industrial"
    MONITORING = "monitoring"
    READONLY = "readonly"
    RESTRICTED = "restricted"


class SessionState(Enum):
    """User session states"""
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    LOCKED = "locked"


@dataclass
class User:
    """User account information"""
    username: str
    email: str
    role: UserRole
    access_level: AccessLevel
    password_hash: str
    mfa_secret: str
    mfa_enabled: bool
    created_at: datetime
    last_login: Optional[datetime]
    failed_attempts: int
    account_locked: bool
    allowed_networks: List[str]
    ssh_public_key: Optional[str]
    is_active: bool = True


@dataclass
class UserSession:
    """Active user session"""
    session_id: str
    username: str
    role: UserRole
    access_level: AccessLevel
    created_at: datetime
    last_activity: datetime
    ip_address: str
    user_agent: str
    vpn_client_id: Optional[str]
    state: SessionState
    allowed_actions: List[str]


@dataclass
class AccessAttempt:
    """Authentication attempt logging"""
    timestamp: datetime
    username: str
    ip_address: str
    user_agent: str
    attempt_type: str  # 'login', 'mfa', 'ssh', 'vpn'
    success: bool
    failure_reason: Optional[str]
    session_id: Optional[str]


class SecurityHardening:
    """Security hardening configuration"""
    
    def __init__(self):
        self.password_policy = {
            "min_length": 12,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special": True,
            "max_age_days": 90,
            "history_count": 5
        }
        
        self.session_policy = {
            "max_idle_minutes": 30,
            "max_session_hours": 8,
            "require_mfa": True,
            "max_failed_attempts": 3,
            "lockout_duration_minutes": 15
        }
        
        self.network_policy = {
            "allowed_ssh_networks": ["192.168.10.0/24"],
            "allowed_vpn_networks": ["10.0.0.0/24"],
            "require_vpn_for_remote": True,
            "max_concurrent_sessions": 3
        }


class AuthenticationManager:
    """
    Comprehensive authentication and access control system
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.database_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security/auth_database.db"
        self.encryption_key = self._load_or_create_encryption_key()
        self.cipher = Fernet(self.encryption_key)
        
        # Security policies
        self.security_hardening = SecurityHardening()
        
        # Active sessions
        self.active_sessions: Dict[str, UserSession] = {}
        self.access_attempts: List[AccessAttempt] = []
        
        # JWT settings
        self.jwt_secret = secrets.token_urlsafe(32)
        self.jwt_algorithm = "HS256"
        self.jwt_expiration_hours = 1
        
        # Initialize database
        self._initialize_database()
        
        # Create default admin user if none exists
        self._create_default_admin()
        
        # Start session cleanup thread
        self._start_session_cleanup()
    
    def _load_or_create_encryption_key(self) -> bytes:
        """Load or create encryption key for sensitive data"""
        key_file = "/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security/encryption.key"
        
        try:
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                key = Fernet.generate_key()
                os.makedirs(os.path.dirname(key_file), exist_ok=True)
                with open(key_file, 'wb') as f:
                    f.write(key)
                os.chmod(key_file, 0o600)  # Restrict access
                return key
        except Exception as e:
            self.logger.error(f"Failed to load/create encryption key: {e}")
            return Fernet.generate_key()
    
    def _initialize_database(self):
        """Initialize authentication database"""
        os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
        
        with sqlite3.connect(self.database_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    email TEXT UNIQUE,
                    role TEXT,
                    access_level TEXT,
                    password_hash TEXT,
                    mfa_secret TEXT,
                    mfa_enabled BOOLEAN,
                    created_at TEXT,
                    last_login TEXT,
                    failed_attempts INTEGER DEFAULT 0,
                    account_locked BOOLEAN DEFAULT 0,
                    allowed_networks TEXT,
                    ssh_public_key TEXT,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    session_id TEXT PRIMARY KEY,
                    username TEXT,
                    role TEXT,
                    access_level TEXT,
                    created_at TEXT,
                    last_activity TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    vpn_client_id TEXT,
                    state TEXT,
                    allowed_actions TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS access_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    username TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    attempt_type TEXT,
                    success BOOLEAN,
                    failure_reason TEXT,
                    session_id TEXT
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS password_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password_hash TEXT,
                    created_at TEXT
                )
            ''')
    
    def _create_default_admin(self):
        """Create default admin user if none exists"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute('SELECT COUNT(*) FROM users WHERE role = ?', (UserRole.ADMIN.value,))
                admin_count = cursor.fetchone()[0]
                
                if admin_count == 0:
                    admin_password = secrets.token_urlsafe(16)
                    mfa_secret = pyotp.random_base32()
                    
                    admin_user = User(
                        username="admin",
                        email="admin@parachutedrops.local",
                        role=UserRole.ADMIN,
                        access_level=AccessLevel.FULL,
                        password_hash=self._hash_password(admin_password),
                        mfa_secret=mfa_secret,
                        mfa_enabled=True,
                        created_at=datetime.now(),
                        last_login=None,
                        failed_attempts=0,
                        account_locked=False,
                        allowed_networks=["0.0.0.0/0"],
                        ssh_public_key=None
                    )
                    
                    self._store_user(admin_user)
                    
                    # Save admin credentials to secure file
                    admin_info = {
                        "username": "admin",
                        "password": admin_password,
                        "mfa_secret": mfa_secret,
                        "created_at": admin_user.created_at.isoformat()
                    }
                    
                    admin_file = "/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security/admin_credentials.json"
                    with open(admin_file, 'w') as f:
                        json.dump(admin_info, f, indent=2)
                    os.chmod(admin_file, 0o600)
                    
                    self.logger.info(f"Created default admin user - credentials saved to {admin_file}")
                    
        except Exception as e:
            self.logger.error(f"Failed to create default admin: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception:
            return False
    
    def _generate_mfa_secret(self) -> str:
        """Generate MFA secret for TOTP"""
        return pyotp.random_base32()
    
    def _verify_mfa_token(self, secret: str, token: str) -> bool:
        """Verify MFA TOTP token"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(token, valid_window=1)
        except Exception:
            return False
    
    def create_user(self, username: str, email: str, password: str, 
                   role: UserRole, access_level: AccessLevel,
                   allowed_networks: List[str] = None) -> bool:
        """Create a new user account"""
        try:
            # Validate password policy
            if not self._validate_password_policy(password):
                raise ValueError("Password does not meet security requirements")
            
            # Check if user exists
            if self._get_user(username):
                raise ValueError(f"User {username} already exists")
            
            if allowed_networks is None:
                allowed_networks = ["192.168.0.0/16"]
            
            # Create user
            user = User(
                username=username,
                email=email,
                role=role,
                access_level=access_level,
                password_hash=self._hash_password(password),
                mfa_secret=self._generate_mfa_secret(),
                mfa_enabled=True,
                created_at=datetime.now(),
                last_login=None,
                failed_attempts=0,
                account_locked=False,
                allowed_networks=allowed_networks,
                ssh_public_key=None
            )
            
            self._store_user(user)
            self._store_password_history(username, user.password_hash)
            
            self.logger.info(f"Created user: {username} with role {role.value}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create user {username}: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str, 
                         mfa_token: str = None, ip_address: str = "",
                         user_agent: str = "") -> Optional[str]:
        """Authenticate user and return session token"""
        attempt = AccessAttempt(
            timestamp=datetime.now(),
            username=username,
            ip_address=ip_address,
            user_agent=user_agent,
            attempt_type="login",
            success=False,
            failure_reason=None,
            session_id=None
        )
        
        try:
            # Get user
            user = self._get_user(username)
            if not user:
                attempt.failure_reason = "User not found"
                self._log_access_attempt(attempt)
                return None
            
            # Check if account is locked
            if user.account_locked:
                attempt.failure_reason = "Account locked"
                self._log_access_attempt(attempt)
                return None
            
            # Check if account is active
            if not user.is_active:
                attempt.failure_reason = "Account disabled"
                self._log_access_attempt(attempt)
                return None
            
            # Verify password
            if not self._verify_password(password, user.password_hash):
                user.failed_attempts += 1
                
                # Lock account if too many failed attempts
                if user.failed_attempts >= self.security_hardening.session_policy["max_failed_attempts"]:
                    user.account_locked = True
                    self.logger.warning(f"Account {username} locked due to failed attempts")
                
                self._store_user(user)
                attempt.failure_reason = "Invalid password"
                self._log_access_attempt(attempt)
                return None
            
            # Verify MFA if enabled
            if user.mfa_enabled:
                if not mfa_token or not self._verify_mfa_token(user.mfa_secret, mfa_token):
                    attempt.failure_reason = "Invalid MFA token"
                    self._log_access_attempt(attempt)
                    return None
            
            # Reset failed attempts on successful login
            user.failed_attempts = 0
            user.last_login = datetime.now()
            user.account_locked = False
            self._store_user(user)
            
            # Create session
            session_id = self._create_session(user, ip_address, user_agent)
            
            attempt.success = True
            attempt.session_id = session_id
            self._log_access_attempt(attempt)
            
            self.logger.info(f"User {username} authenticated successfully")
            return session_id
            
        except Exception as e:
            attempt.failure_reason = f"Authentication error: {str(e)}"
            self._log_access_attempt(attempt)
            self.logger.error(f"Authentication error for {username}: {e}")
            return None
    
    def _create_session(self, user: User, ip_address: str, user_agent: str) -> str:
        """Create user session"""
        session_id = secrets.token_urlsafe(32)
        
        # Define allowed actions based on role and access level
        allowed_actions = self._get_allowed_actions(user.role, user.access_level)
        
        session = UserSession(
            session_id=session_id,
            username=user.username,
            role=user.role,
            access_level=user.access_level,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            ip_address=ip_address,
            user_agent=user_agent,
            vpn_client_id=None,
            state=SessionState.ACTIVE,
            allowed_actions=allowed_actions
        )
        
        self.active_sessions[session_id] = session
        self._store_session(session)
        
        return session_id
    
    def _get_allowed_actions(self, role: UserRole, access_level: AccessLevel) -> List[str]:
        """Get allowed actions for role and access level"""
        actions = []
        
        # Base actions for all authenticated users
        actions.extend(["view_dashboard", "change_password"])
        
        # Role-based actions
        if role == UserRole.ADMIN:
            actions.extend([
                "manage_users", "view_logs", "modify_settings", 
                "access_all_networks", "manage_vpn", "system_administration"
            ])
        elif role == UserRole.ENGINEER:
            actions.extend([
                "configure_devices", "access_industrial_networks",
                "view_technical_data", "modify_configurations"
            ])
        elif role == UserRole.TECHNICIAN:
            actions.extend([
                "access_maintenance_tools", "view_diagnostics",
                "limited_device_access"
            ])
        elif role == UserRole.OPERATOR:
            actions.extend([
                "monitor_systems", "view_operational_data",
                "basic_control_actions"
            ])
        elif role == UserRole.VIEWER:
            actions.extend(["view_monitoring_data", "generate_reports"])
        
        # Access level restrictions
        if access_level == AccessLevel.READONLY:
            actions = [action for action in actions if action.startswith("view_") or action.startswith("monitor_")]
        elif access_level == AccessLevel.RESTRICTED:
            actions = [action for action in actions if not action.startswith("manage_")]
        
        return actions
    
    def validate_session(self, session_id: str, ip_address: str = "") -> Optional[UserSession]:
        """Validate and update session"""
        if session_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_id]
        current_time = datetime.now()
        
        # Check session expiry
        max_idle = timedelta(minutes=self.security_hardening.session_policy["max_idle_minutes"])
        max_session = timedelta(hours=self.security_hardening.session_policy["max_session_hours"])
        
        if (current_time - session.last_activity > max_idle or
            current_time - session.created_at > max_session):
            session.state = SessionState.EXPIRED
            self._store_session(session)
            del self.active_sessions[session_id]
            return None
        
        # Update activity
        session.last_activity = current_time
        if ip_address and ip_address != session.ip_address:
            # IP address changed - potential session hijacking
            self.logger.warning(f"Session {session_id} IP changed: {session.ip_address} -> {ip_address}")
            session.state = SessionState.TERMINATED
            self._store_session(session)
            del self.active_sessions[session_id]
            return None
        
        self._store_session(session)
        return session
    
    def terminate_session(self, session_id: str):
        """Terminate user session"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session.state = SessionState.TERMINATED
            self._store_session(session)
            del self.active_sessions[session_id]
            self.logger.info(f"Session terminated: {session_id}")
    
    def generate_mfa_qr_code(self, username: str) -> Optional[str]:
        """Generate QR code for MFA setup"""
        try:
            user = self._get_user(username)
            if not user:
                return None
            
            # Create TOTP URI
            totp = pyotp.TOTP(user.mfa_secret)
            provisioning_uri = totp.provisioning_uri(
                name=user.email,
                issuer_name="Parachute Drop System"
            )
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(provisioning_uri)
            qr.make(fit=True)
            
            qr_path = f"/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security/mfa_qr/{username}_mfa.png"
            os.makedirs(os.path.dirname(qr_path), exist_ok=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(qr_path)
            
            return qr_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate MFA QR code for {username}: {e}")
            return None
    
    def _validate_password_policy(self, password: str) -> bool:
        """Validate password against security policy"""
        policy = self.security_hardening.password_policy
        
        if len(password) < policy["min_length"]:
            return False
        
        if policy["require_uppercase"] and not any(c.isupper() for c in password):
            return False
        
        if policy["require_lowercase"] and not any(c.islower() for c in password):
            return False
        
        if policy["require_numbers"] and not any(c.isdigit() for c in password):
            return False
        
        if policy["require_special"] and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False
        
        return True
    
    def _get_user(self, username: str) -> Optional[User]:
        """Get user from database"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                cursor = conn.execute('''
                    SELECT username, email, role, access_level, password_hash, mfa_secret,
                           mfa_enabled, created_at, last_login, failed_attempts, account_locked,
                           allowed_networks, ssh_public_key, is_active
                    FROM users WHERE username = ?
                ''', (username,))
                
                row = cursor.fetchone()
                if row:
                    return User(
                        username=row[0],
                        email=row[1],
                        role=UserRole(row[2]),
                        access_level=AccessLevel(row[3]),
                        password_hash=row[4],
                        mfa_secret=row[5],
                        mfa_enabled=bool(row[6]),
                        created_at=datetime.fromisoformat(row[7]),
                        last_login=datetime.fromisoformat(row[8]) if row[8] else None,
                        failed_attempts=row[9],
                        account_locked=bool(row[10]),
                        allowed_networks=json.loads(row[11]) if row[11] else [],
                        ssh_public_key=row[12],
                        is_active=bool(row[13])
                    )
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to get user {username}: {e}")
            return None
    
    def _store_user(self, user: User):
        """Store user to database"""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO users 
                (username, email, role, access_level, password_hash, mfa_secret, mfa_enabled,
                 created_at, last_login, failed_attempts, account_locked, allowed_networks,
                 ssh_public_key, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user.username, user.email, user.role.value, user.access_level.value,
                user.password_hash, user.mfa_secret, user.mfa_enabled,
                user.created_at.isoformat(),
                user.last_login.isoformat() if user.last_login else None,
                user.failed_attempts, user.account_locked,
                json.dumps(user.allowed_networks), user.ssh_public_key, user.is_active
            ))
    
    def _store_session(self, session: UserSession):
        """Store session to database"""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO user_sessions 
                (session_id, username, role, access_level, created_at, last_activity,
                 ip_address, user_agent, vpn_client_id, state, allowed_actions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session.session_id, session.username, session.role.value,
                session.access_level.value, session.created_at.isoformat(),
                session.last_activity.isoformat(), session.ip_address,
                session.user_agent, session.vpn_client_id, session.state.value,
                json.dumps(session.allowed_actions)
            ))
    
    def _log_access_attempt(self, attempt: AccessAttempt):
        """Log access attempt to database"""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute('''
                INSERT INTO access_attempts 
                (timestamp, username, ip_address, user_agent, attempt_type,
                 success, failure_reason, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                attempt.timestamp.isoformat(), attempt.username, attempt.ip_address,
                attempt.user_agent, attempt.attempt_type, attempt.success,
                attempt.failure_reason, attempt.session_id
            ))
    
    def _store_password_history(self, username: str, password_hash: str):
        """Store password history"""
        with sqlite3.connect(self.database_path) as conn:
            conn.execute('''
                INSERT INTO password_history (username, password_hash, created_at)
                VALUES (?, ?, ?)
            ''', (username, password_hash, datetime.now().isoformat()))
    
    def _start_session_cleanup(self):
        """Start background thread for session cleanup"""
        def cleanup_loop():
            while True:
                try:
                    current_time = datetime.now()
                    expired_sessions = []
                    
                    for session_id, session in self.active_sessions.items():
                        max_idle = timedelta(minutes=self.security_hardening.session_policy["max_idle_minutes"])
                        if current_time - session.last_activity > max_idle:
                            expired_sessions.append(session_id)
                    
                    for session_id in expired_sessions:
                        self.terminate_session(session_id)
                    
                    time.sleep(300)  # Check every 5 minutes
                    
                except Exception as e:
                    self.logger.error(f"Session cleanup error: {e}")
                    time.sleep(300)
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()
    
    def get_security_status(self) -> Dict[str, Any]:
        """Get authentication system security status"""
        try:
            with sqlite3.connect(self.database_path) as conn:
                # Count users by role
                cursor = conn.execute('SELECT role, COUNT(*) FROM users GROUP BY role')
                user_counts = dict(cursor.fetchall())
                
                # Count active sessions
                active_session_count = len(self.active_sessions)
                
                # Recent failed attempts (last hour)
                cursor = conn.execute('''
                    SELECT COUNT(*) FROM access_attempts 
                    WHERE success = 0 AND timestamp > datetime('now', '-1 hour')
                ''')
                recent_failures = cursor.fetchone()[0]
                
                # Locked accounts
                cursor = conn.execute('SELECT COUNT(*) FROM users WHERE account_locked = 1')
                locked_accounts = cursor.fetchone()[0]
                
                return {
                    "users_by_role": user_counts,
                    "active_sessions": active_session_count,
                    "recent_failed_attempts": recent_failures,
                    "locked_accounts": locked_accounts,
                    "mfa_enabled": True,
                    "password_policy_enforced": True,
                    "session_timeout_enabled": True,
                    "timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.logger.error(f"Failed to get security status: {e}")
            return {"error": str(e)}
    
    def deploy_parachute_drop_authentication(self) -> Dict[str, Any]:
        """Deploy authentication system for Parachute Drop"""
        try:
            self.logger.info("Deploying Parachute Drop authentication system...")
            
            # Create default users for different roles
            default_users = [
                ("engineer", "engineer@parachutedrops.local", UserRole.ENGINEER, AccessLevel.INDUSTRIAL),
                ("technician", "technician@parachutedrops.local", UserRole.TECHNICIAN, AccessLevel.MONITORING),
                ("operator", "operator@parachutedrops.local", UserRole.OPERATOR, AccessLevel.READONLY)
            ]
            
            created_users = []
            for username, email, role, access_level in default_users:
                temp_password = secrets.token_urlsafe(12)
                if self.create_user(username, email, temp_password, role, access_level):
                    created_users.append({
                        "username": username,
                        "password": temp_password,
                        "role": role.value,
                        "access_level": access_level.value
                    })
            
            deployment_info = {
                "deployment_time": datetime.now().isoformat(),
                "authentication_enabled": True,
                "mfa_enabled": True,
                "users_created": len(created_users),
                "default_users": created_users,
                "security_policies": {
                    "password_policy": self.security_hardening.password_policy,
                    "session_policy": self.security_hardening.session_policy,
                    "network_policy": self.security_hardening.network_policy
                },
                "admin_credentials_file": "/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security/admin_credentials.json"
            }
            
            # Save deployment info
            config_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security/auth_deployment.json"
            with open(config_path, 'w') as f:
                json.dump(deployment_info, f, indent=2)
            
            self.logger.info("Parachute Drop authentication system deployed successfully")
            return deployment_info
            
        except Exception as e:
            self.logger.error(f"Authentication deployment failed: {e}")
            raise


def main():
    """Test authentication manager"""
    logging.basicConfig(level=logging.INFO)
    
    auth_manager = AuthenticationManager()
    
    print("🔐 Authentication Manager for Parachute Drop System")
    print("=" * 60)
    
    try:
        # Deploy authentication system
        deployment_info = auth_manager.deploy_parachute_drop_authentication()
        print("✅ Authentication system deployed successfully!")
        
        print(f"\n👥 Users Created: {deployment_info['users_created']}")
        print(f"🔒 MFA Enabled: {deployment_info['mfa_enabled']}")
        print(f"📋 Security Policies: {len(deployment_info['security_policies'])}")
        
        # Get security status
        status = auth_manager.get_security_status()
        print(f"\n📊 Security Status:")
        print(f"  Active Sessions: {status['active_sessions']}")
        print(f"  Recent Failed Attempts: {status['recent_failed_attempts']}")
        print(f"  Locked Accounts: {status['locked_accounts']}")
        
        # Test authentication
        print(f"\n🧪 Testing Authentication...")
        
        # This would require actual password input in production
        print("(Authentication testing requires actual credentials)")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()