#!/usr/bin/env python3
"""
Discord Bot Health Monitor
Monitors Discord bot and task worker health, restarts if needed
"""

import time
import subprocess
import requests
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/opt/claude/logs/health_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('HealthMonitor')

class HealthMonitor:
    def __init__(self):
        self.check_interval = 60  # Check every minute
        self.failure_threshold = 3  # Restart after 3 consecutive failures
        self.failures = {
            'discord-bot': 0,
            'task-worker': 0
        }
        
    def check_docker_container(self, container_name):
        """Check if Docker container is healthy"""
        try:
            result = subprocess.run(
                ['docker', 'inspect', '--format', '{{.State.Health.Status}}', container_name],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() == 'healthy'
        except Exception as e:
            logger.error(f"Error checking container {container_name}: {e}")
            return False
    
    def check_systemd_service(self, service_name):
        """Check if systemd service is active"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', service_name],
                capture_output=True, text=True, timeout=10
            )
            return result.stdout.strip() == 'active'
        except Exception as e:
            logger.error(f"Error checking service {service_name}: {e}")
            return False
    
    def restart_docker_container(self, container_name):
        """Restart Docker container"""
        try:
            subprocess.run(['docker', 'restart', container_name], timeout=30)
            logger.info(f"Restarted Docker container: {container_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to restart container {container_name}: {e}")
            return False
    
    def restart_systemd_service(self, service_name):
        """Restart systemd service"""
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', service_name], timeout=30)
            logger.info(f"Restarted systemd service: {service_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to restart service {service_name}: {e}")
            return False
    
    def send_alert(self, message):
        """Send alert notification (Discord webhook or other)"""
        # This could be enhanced to send Discord webhook notifications
        logger.critical(f"ALERT: {message}")
        
    def monitor_loop(self):
        """Main monitoring loop"""
        logger.info("Health monitor started")
        
        while True:
            try:
                # Check if we're running in Docker or systemd mode
                docker_mode = subprocess.run(['docker', 'ps'], capture_output=True).returncode == 0
                
                if docker_mode:
                    self.monitor_docker_services()
                else:
                    self.monitor_systemd_services()
                    
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                logger.info("Health monitor stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in monitor loop: {e}")
                time.sleep(self.check_interval)
    
    def monitor_docker_services(self):
        """Monitor Docker-based services"""
        services = {
            'discord-claude-bot': 'discord-bot',
            'mac-claude-worker': 'task-worker'
        }
        
        for container_name, service_key in services.items():
            healthy = self.check_docker_container(container_name)
            
            if healthy:
                self.failures[service_key] = 0
                logger.debug(f"{container_name} is healthy")
            else:
                self.failures[service_key] += 1
                logger.warning(f"{container_name} health check failed ({self.failures[service_key]}/{self.failure_threshold})")
                
                if self.failures[service_key] >= self.failure_threshold:
                    logger.error(f"Restarting {container_name} due to repeated failures")
                    if self.restart_docker_container(container_name):
                        self.failures[service_key] = 0
                        self.send_alert(f"Restarted unhealthy container: {container_name}")
                    else:
                        self.send_alert(f"Failed to restart container: {container_name}")
    
    def monitor_systemd_services(self):
        """Monitor systemd-based services"""
        services = {
            'claude-discord': 'discord-bot',
            'claude-worker': 'task-worker'
        }
        
        for service_name, service_key in services.items():
            active = self.check_systemd_service(service_name)
            
            if active:
                self.failures[service_key] = 0
                logger.debug(f"{service_name} is active")
            else:
                self.failures[service_key] += 1
                logger.warning(f"{service_name} is not active ({self.failures[service_key]}/{self.failure_threshold})")
                
                if self.failures[service_key] >= self.failure_threshold:
                    logger.error(f"Restarting {service_name} due to repeated failures")
                    if self.restart_systemd_service(service_name):
                        self.failures[service_key] = 0
                        self.send_alert(f"Restarted inactive service: {service_name}")
                    else:
                        self.send_alert(f"Failed to restart service: {service_name}")

if __name__ == "__main__":
    monitor = HealthMonitor()
    monitor.monitor_loop()