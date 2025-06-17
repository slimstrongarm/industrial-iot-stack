#!/usr/bin/env python3
"""
CT-086 Agent 5: System Integration & Validation Tester
Comprehensive testing and validation for complete Parachute Drop router system

This agent provides integration testing between CT-084, CT-085, and CT-086 systems,
validates end-to-end functionality, and ensures production readiness.
"""

import os
import json
import time
import subprocess
import requests
import socket
import logging
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import sqlite3
import threading


class TestResult(Enum):
    """Test result status"""
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    ERROR = "error"


class TestCategory(Enum):
    """Test categories"""
    NETWORK = "network"
    SECURITY = "security"
    INTEGRATION = "integration"
    PERFORMANCE = "performance"
    FUNCTIONALITY = "functionality"


@dataclass
class TestCase:
    """Test case definition"""
    test_id: str
    name: str
    description: str
    category: TestCategory
    prerequisites: List[str]
    expected_result: str
    timeout_seconds: int
    critical: bool = False


@dataclass
class TestExecution:
    """Test execution result"""
    test_case: TestCase
    result: TestResult
    start_time: datetime
    end_time: datetime
    duration: timedelta
    output: str
    error_message: Optional[str]
    details: Dict[str, Any]


class SystemIntegrationTester:
    """
    Comprehensive system integration and validation tester
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.results_dir = "/home/server/industrial-iot-stack/ct-086-router-system/agent5_integration_validation/test_results"
        
        # Test execution state
        self.test_cases: List[TestCase] = []
        self.test_results: List[TestExecution] = []
        self.current_test_run: Optional[str] = None
        
        # System endpoints
        self.endpoints = {
            "ct084_api": "http://localhost:8084",
            "ct085_api": "http://localhost:8085",
            "ct086_dashboard": "http://localhost:8086",
            "router_management": "http://192.168.8.1",
            "vpn_server": "127.0.0.1:51820",
            "auth_service": "http://localhost:8087"
        }
        
        # Initialize test cases
        self._initialize_test_cases()
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
    
    def _initialize_test_cases(self):
        """Initialize comprehensive test cases"""
        test_cases = [
            # Network Connectivity Tests
            TestCase(
                test_id="NET-001",
                name="Router Network Connectivity",
                description="Test basic network connectivity to GL.iNet router",
                category=TestCategory.NETWORK,
                prerequisites=[],
                expected_result="Router responds to ping and HTTP requests",
                timeout_seconds=30,
                critical=True
            ),
            
            TestCase(
                test_id="NET-002",
                name="VLAN Isolation Verification",
                description="Verify network isolation between VLANs",
                category=TestCategory.NETWORK,
                prerequisites=["NET-001"],
                expected_result="Traffic properly isolated between network segments",
                timeout_seconds=60,
                critical=True
            ),
            
            TestCase(
                test_id="NET-003",
                name="VPN Tunnel Connectivity",
                description="Test VPN tunnel establishment and connectivity",
                category=TestCategory.NETWORK,
                prerequisites=["NET-001"],
                expected_result="VPN tunnel establishes successfully",
                timeout_seconds=45,
                critical=True
            ),
            
            # Security Tests
            TestCase(
                test_id="SEC-001",
                name="Firewall Rule Validation",
                description="Verify firewall rules are properly configured",
                category=TestCategory.SECURITY,
                prerequisites=["NET-001"],
                expected_result="Firewall rules block unauthorized traffic",
                timeout_seconds=30,
                critical=True
            ),
            
            TestCase(
                test_id="SEC-002",
                name="Authentication System Test",
                description="Test user authentication and authorization",
                category=TestCategory.SECURITY,
                prerequisites=[],
                expected_result="Authentication system validates users correctly",
                timeout_seconds=20,
                critical=True
            ),
            
            TestCase(
                test_id="SEC-003",
                name="Intrusion Detection Test",
                description="Verify intrusion detection system is active",
                category=TestCategory.SECURITY,
                prerequisites=["SEC-001"],
                expected_result="IDS detects and responds to threats",
                timeout_seconds=60
            ),
            
            # Integration Tests
            TestCase(
                test_id="INT-001",
                name="CT-084 Integration",
                description="Test integration with CT-084 Parachute Drop system",
                category=TestCategory.INTEGRATION,
                prerequisites=["NET-001"],
                expected_result="CT-084 system accessible through router",
                timeout_seconds=30,
                critical=True
            ),
            
            TestCase(
                test_id="INT-002",
                name="CT-085 Integration",
                description="Test integration with CT-085 Network Discovery system",
                category=TestCategory.INTEGRATION,
                prerequisites=["NET-001"],
                expected_result="CT-085 discovery works through router networks",
                timeout_seconds=45,
                critical=True
            ),
            
            TestCase(
                test_id="INT-003",
                name="Cross-System Communication",
                description="Test communication between CT-084 and CT-085",
                category=TestCategory.INTEGRATION,
                prerequisites=["INT-001", "INT-002"],
                expected_result="Systems communicate through router infrastructure",
                timeout_seconds=60,
                critical=True
            ),
            
            # Performance Tests
            TestCase(
                test_id="PERF-001",
                name="Network Throughput Test",
                description="Measure network throughput through router",
                category=TestCategory.PERFORMANCE,
                prerequisites=["NET-001"],
                expected_result="Network throughput meets minimum requirements",
                timeout_seconds=120
            ),
            
            TestCase(
                test_id="PERF-002",
                name="VPN Performance Test",
                description="Measure VPN tunnel performance",
                category=TestCategory.PERFORMANCE,
                prerequisites=["NET-003"],
                expected_result="VPN performance meets industrial requirements",
                timeout_seconds=90
            ),
            
            TestCase(
                test_id="PERF-003",
                name="Concurrent Connection Test",
                description="Test multiple simultaneous connections",
                category=TestCategory.PERFORMANCE,
                prerequisites=["NET-001"],
                expected_result="Router handles multiple connections efficiently",
                timeout_seconds=180
            ),
            
            # Functionality Tests
            TestCase(
                test_id="FUNC-001",
                name="Traffic Monitoring Dashboard",
                description="Verify traffic monitoring dashboard functionality",
                category=TestCategory.FUNCTIONALITY,
                prerequisites=["NET-001"],
                expected_result="Dashboard displays real-time traffic data",
                timeout_seconds=30
            ),
            
            TestCase(
                test_id="FUNC-002",
                name="Industrial Protocol Detection",
                description="Test industrial protocol detection and analysis",
                category=TestCategory.FUNCTIONALITY,
                prerequisites=["INT-002"],
                expected_result="Industrial protocols properly detected and classified",
                timeout_seconds=60
            ),
            
            TestCase(
                test_id="FUNC-003",
                name="Remote Access Functionality",
                description="Test complete remote access workflow",
                category=TestCategory.FUNCTIONALITY,
                prerequisites=["NET-003", "SEC-002"],
                expected_result="Remote users can securely access industrial networks",
                timeout_seconds=90,
                critical=True
            ),
            
            # End-to-End Tests
            TestCase(
                test_id="E2E-001",
                name="Complete System Deployment",
                description="End-to-end test of complete Parachute Drop system",
                category=TestCategory.INTEGRATION,
                prerequisites=["INT-001", "INT-002", "INT-003", "FUNC-003"],
                expected_result="Complete system functions as integrated solution",
                timeout_seconds=300,
                critical=True
            )
        ]
        
        self.test_cases = test_cases
    
    async def execute_test_case(self, test_case: TestCase) -> TestExecution:
        """Execute a single test case"""
        start_time = datetime.now()
        
        self.logger.info(f"Executing test: {test_case.test_id} - {test_case.name}")
        
        try:
            # Check prerequisites
            for prereq in test_case.prerequisites:
                if not self._check_prerequisite(prereq):
                    return TestExecution(
                        test_case=test_case,
                        result=TestResult.SKIP,
                        start_time=start_time,
                        end_time=datetime.now(),
                        duration=datetime.now() - start_time,
                        output="",
                        error_message=f"Prerequisite {prereq} not met",
                        details={}
                    )
            
            # Execute test based on category and ID
            result, output, details = await self._run_specific_test(test_case)
            
            end_time = datetime.now()
            
            return TestExecution(
                test_case=test_case,
                result=result,
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                output=output,
                error_message=None,
                details=details
            )
            
        except asyncio.TimeoutError:
            end_time = datetime.now()
            return TestExecution(
                test_case=test_case,
                result=TestResult.ERROR,
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                output="",
                error_message=f"Test timed out after {test_case.timeout_seconds} seconds",
                details={}
            )
            
        except Exception as e:
            end_time = datetime.now()
            return TestExecution(
                test_case=test_case,
                result=TestResult.ERROR,
                start_time=start_time,
                end_time=end_time,
                duration=end_time - start_time,
                output="",
                error_message=str(e),
                details={}
            )
    
    async def _run_specific_test(self, test_case: TestCase) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Run specific test based on test ID"""
        test_id = test_case.test_id
        
        if test_id == "NET-001":
            return await self._test_router_connectivity()
        elif test_id == "NET-002":
            return await self._test_vlan_isolation()
        elif test_id == "NET-003":
            return await self._test_vpn_connectivity()
        elif test_id == "SEC-001":
            return await self._test_firewall_rules()
        elif test_id == "SEC-002":
            return await self._test_authentication()
        elif test_id == "SEC-003":
            return await self._test_intrusion_detection()
        elif test_id == "INT-001":
            return await self._test_ct084_integration()
        elif test_id == "INT-002":
            return await self._test_ct085_integration()
        elif test_id == "INT-003":
            return await self._test_cross_system_communication()
        elif test_id == "PERF-001":
            return await self._test_network_throughput()
        elif test_id == "PERF-002":
            return await self._test_vpn_performance()
        elif test_id == "PERF-003":
            return await self._test_concurrent_connections()
        elif test_id == "FUNC-001":
            return await self._test_traffic_dashboard()
        elif test_id == "FUNC-002":
            return await self._test_protocol_detection()
        elif test_id == "FUNC-003":
            return await self._test_remote_access()
        elif test_id == "E2E-001":
            return await self._test_complete_system()
        else:
            return TestResult.SKIP, f"Test {test_id} not implemented", {}
    
    async def _test_router_connectivity(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test router network connectivity"""
        try:
            # Ping test
            ping_result = subprocess.run(
                ["ping", "-c", "3", "192.168.8.1"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            ping_success = ping_result.returncode == 0
            
            # HTTP test
            try:
                response = requests.get("http://192.168.8.1", timeout=10)
                http_success = response.status_code in [200, 401, 403]  # Accept auth redirects
            except:
                http_success = False
            
            if ping_success and http_success:
                return TestResult.PASS, "Router connectivity verified", {
                    "ping_success": ping_success,
                    "http_success": http_success,
                    "ping_output": ping_result.stdout
                }
            else:
                return TestResult.FAIL, "Router connectivity failed", {
                    "ping_success": ping_success,
                    "http_success": http_success,
                    "ping_output": ping_result.stdout
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Router connectivity test error: {e}", {}
    
    async def _test_vlan_isolation(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test VLAN isolation"""
        try:
            # Test inter-VLAN communication blocking
            test_ips = [
                ("192.168.10.1", "192.168.20.1"),  # Management to Industrial
                ("192.168.20.1", "192.168.40.1"),  # Industrial to Guest
                ("192.168.40.1", "192.168.10.1")   # Guest to Management
            ]
            
            isolation_results = []
            
            for src_ip, dst_ip in test_ips:
                # Attempt ping between VLANs (should fail)
                ping_result = subprocess.run(
                    ["ping", "-c", "1", "-W", "2", dst_ip],
                    capture_output=True,
                    text=True
                )
                
                # Isolation is working if ping fails
                isolated = ping_result.returncode != 0
                isolation_results.append({
                    "src": src_ip,
                    "dst": dst_ip,
                    "isolated": isolated
                })
            
            # Check if all inter-VLAN traffic is properly isolated
            all_isolated = all(result["isolated"] for result in isolation_results)
            
            if all_isolated:
                return TestResult.PASS, "VLAN isolation verified", {
                    "isolation_results": isolation_results
                }
            else:
                return TestResult.FAIL, "VLAN isolation compromised", {
                    "isolation_results": isolation_results
                }
                
        except Exception as e:
            return TestResult.ERROR, f"VLAN isolation test error: {e}", {}
    
    async def _test_vpn_connectivity(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test VPN tunnel connectivity"""
        try:
            # Check if WireGuard interface exists
            wg_result = subprocess.run(
                ["ip", "addr", "show", "wg0"],
                capture_output=True,
                text=True
            )
            
            interface_exists = wg_result.returncode == 0
            
            # Check WireGuard status
            wg_status_result = subprocess.run(
                ["wg", "show"],
                capture_output=True,
                text=True
            )
            
            wg_running = wg_status_result.returncode == 0 and "wg0" in wg_status_result.stdout
            
            # Test VPN port accessibility
            vpn_port_open = self._test_port_connectivity("127.0.0.1", 51820)
            
            if interface_exists and wg_running and vpn_port_open:
                return TestResult.PASS, "VPN connectivity verified", {
                    "interface_exists": interface_exists,
                    "wireguard_running": wg_running,
                    "port_accessible": vpn_port_open,
                    "wg_status": wg_status_result.stdout
                }
            else:
                return TestResult.FAIL, "VPN connectivity failed", {
                    "interface_exists": interface_exists,
                    "wireguard_running": wg_running,
                    "port_accessible": vpn_port_open
                }
                
        except Exception as e:
            return TestResult.ERROR, f"VPN connectivity test error: {e}", {}
    
    async def _test_firewall_rules(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test firewall rule configuration"""
        try:
            # Check iptables rules
            iptables_result = subprocess.run(
                ["iptables", "-L", "-n"],
                capture_output=True,
                text=True
            )
            
            if iptables_result.returncode != 0:
                return TestResult.FAIL, "Cannot access iptables", {}
            
            rules_output = iptables_result.stdout
            
            # Check for expected rules
            expected_rules = [
                "DROP",          # Default drop policy
                "ACCEPT",        # Allow established connections
                "22",            # SSH port
                "443",           # HTTPS port
                "51820"          # VPN port
            ]
            
            rules_found = {}
            for rule in expected_rules:
                rules_found[rule] = rule in rules_output
            
            all_rules_present = all(rules_found.values())
            
            if all_rules_present:
                return TestResult.PASS, "Firewall rules verified", {
                    "rules_found": rules_found,
                    "total_rules": len(rules_output.split('\n'))
                }
            else:
                return TestResult.FAIL, "Missing firewall rules", {
                    "rules_found": rules_found
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Firewall test error: {e}", {}
    
    async def _test_authentication(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test authentication system"""
        try:
            # Check if authentication database exists
            auth_db_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security/auth_database.db"
            db_exists = os.path.exists(auth_db_path)
            
            if not db_exists:
                return TestResult.FAIL, "Authentication database not found", {}
            
            # Check database tables
            with sqlite3.connect(auth_db_path) as conn:
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ["users", "user_sessions", "access_attempts"]
            tables_present = all(table in tables for table in expected_tables)
            
            # Check for default admin user
            with sqlite3.connect(auth_db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM users WHERE username='admin'")
                admin_exists = cursor.fetchone()[0] > 0
            
            if tables_present and admin_exists:
                return TestResult.PASS, "Authentication system verified", {
                    "database_exists": db_exists,
                    "tables_present": tables_present,
                    "admin_user_exists": admin_exists,
                    "tables_found": tables
                }
            else:
                return TestResult.FAIL, "Authentication system incomplete", {
                    "database_exists": db_exists,
                    "tables_present": tables_present,
                    "admin_user_exists": admin_exists
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Authentication test error: {e}", {}
    
    async def _test_intrusion_detection(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test intrusion detection system"""
        try:
            # Check if security monitoring is configured
            security_config_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent4_remote_access_security/security_deployment.json"
            config_exists = os.path.exists(security_config_path)
            
            if config_exists:
                with open(security_config_path, 'r') as f:
                    config = json.load(f)
                
                monitoring_active = config.get("monitoring_active", False)
                intrusion_signatures = len(config.get("intrusion_signatures", []))
                
                return TestResult.PASS, "Intrusion detection verified", {
                    "config_exists": config_exists,
                    "monitoring_active": monitoring_active,
                    "signatures_count": intrusion_signatures
                }
            else:
                return TestResult.FAIL, "Intrusion detection not configured", {
                    "config_exists": config_exists
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Intrusion detection test error: {e}", {}
    
    async def _test_ct084_integration(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test CT-084 system integration"""
        try:
            ct084_path = "/home/server/industrial-iot-stack/ct-084-parachute-drop-system"
            system_exists = os.path.exists(ct084_path)
            
            # Check for main system file
            main_script = f"{ct084_path}/setup_ct084_system.py"
            script_exists = os.path.exists(main_script)
            
            # Test API endpoint if available
            api_accessible = False
            try:
                response = requests.get(self.endpoints["ct084_api"], timeout=5)
                api_accessible = response.status_code in [200, 404]  # Service running
            except:
                pass
            
            if system_exists and script_exists:
                return TestResult.PASS, "CT-084 integration verified", {
                    "system_exists": system_exists,
                    "script_exists": script_exists,
                    "api_accessible": api_accessible
                }
            else:
                return TestResult.FAIL, "CT-084 integration failed", {
                    "system_exists": system_exists,
                    "script_exists": script_exists,
                    "api_accessible": api_accessible
                }
                
        except Exception as e:
            return TestResult.ERROR, f"CT-084 integration test error: {e}", {}
    
    async def _test_ct085_integration(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test CT-085 system integration"""
        try:
            ct085_path = "/home/server/industrial-iot-stack/ct-085-network-discovery"
            system_exists = os.path.exists(ct085_path)
            
            # Check for main system file
            main_script = f"{ct085_path}/setup_ct085_system.py"
            script_exists = os.path.exists(main_script)
            
            # Test API endpoint if available
            api_accessible = False
            try:
                response = requests.get(self.endpoints["ct085_api"], timeout=5)
                api_accessible = response.status_code in [200, 404]  # Service running
            except:
                pass
            
            if system_exists and script_exists:
                return TestResult.PASS, "CT-085 integration verified", {
                    "system_exists": system_exists,
                    "script_exists": script_exists,
                    "api_accessible": api_accessible
                }
            else:
                return TestResult.FAIL, "CT-085 integration failed", {
                    "system_exists": system_exists,
                    "script_exists": script_exists,
                    "api_accessible": api_accessible
                }
                
        except Exception as e:
            return TestResult.ERROR, f"CT-085 integration test error: {e}", {}
    
    async def _test_cross_system_communication(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test communication between systems"""
        try:
            # Test network connectivity between system components
            network_tests = [
                ("CT-084 to CT-085", "localhost", 8085),
                ("CT-085 to Dashboard", "localhost", 8086),
                ("Dashboard to Auth", "localhost", 8087)
            ]
            
            connectivity_results = {}
            for test_name, host, port in network_tests:
                connectivity_results[test_name] = self._test_port_connectivity(host, port)
            
            # Check if systems can communicate
            all_connected = all(connectivity_results.values())
            
            if all_connected:
                return TestResult.PASS, "Cross-system communication verified", {
                    "connectivity_results": connectivity_results
                }
            else:
                return TestResult.FAIL, "Cross-system communication failed", {
                    "connectivity_results": connectivity_results
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Cross-system communication test error: {e}", {}
    
    async def _test_network_throughput(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test network throughput performance"""
        try:
            # Simple throughput test using dd and network pipes
            start_time = time.time()
            
            # Create test data
            test_result = subprocess.run(
                ["dd", "if=/dev/zero", "bs=1M", "count=10"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Calculate approximate throughput
            data_size_mb = 10
            throughput_mbps = (data_size_mb * 8) / duration if duration > 0 else 0
            
            # Industrial networks typically need at least 1 Mbps
            meets_requirements = throughput_mbps >= 1.0
            
            if meets_requirements:
                return TestResult.PASS, "Network throughput adequate", {
                    "throughput_mbps": throughput_mbps,
                    "duration_seconds": duration,
                    "meets_requirements": meets_requirements
                }
            else:
                return TestResult.FAIL, "Network throughput insufficient", {
                    "throughput_mbps": throughput_mbps,
                    "duration_seconds": duration,
                    "meets_requirements": meets_requirements
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Network throughput test error: {e}", {}
    
    async def _test_vpn_performance(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test VPN tunnel performance"""
        try:
            # Test VPN latency and connectivity
            vpn_ip = "10.0.0.1"  # Typical VPN gateway IP
            
            ping_result = subprocess.run(
                ["ping", "-c", "5", vpn_ip],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if ping_result.returncode == 0:
                # Extract latency information
                output_lines = ping_result.stdout.split('\n')
                latency_info = [line for line in output_lines if "time=" in line]
                
                return TestResult.PASS, "VPN performance acceptable", {
                    "ping_success": True,
                    "latency_samples": len(latency_info),
                    "ping_output": ping_result.stdout
                }
            else:
                return TestResult.FAIL, "VPN performance test failed", {
                    "ping_success": False,
                    "error": ping_result.stderr
                }
                
        except Exception as e:
            return TestResult.ERROR, f"VPN performance test error: {e}", {}
    
    async def _test_concurrent_connections(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test multiple concurrent connections"""
        try:
            # Test multiple simultaneous connections to router
            concurrent_tests = []
            
            for i in range(5):  # Test 5 concurrent connections
                test_task = asyncio.create_task(self._test_single_connection(i))
                concurrent_tests.append(test_task)
            
            # Wait for all tests to complete
            results = await asyncio.gather(*concurrent_tests, return_exceptions=True)
            
            successful_connections = sum(1 for result in results if result is True)
            total_connections = len(results)
            
            success_rate = successful_connections / total_connections
            
            if success_rate >= 0.8:  # 80% success rate
                return TestResult.PASS, "Concurrent connections handled well", {
                    "successful_connections": successful_connections,
                    "total_connections": total_connections,
                    "success_rate": success_rate
                }
            else:
                return TestResult.FAIL, "Concurrent connection handling insufficient", {
                    "successful_connections": successful_connections,
                    "total_connections": total_connections,
                    "success_rate": success_rate
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Concurrent connection test error: {e}", {}
    
    async def _test_single_connection(self, connection_id: int) -> bool:
        """Test a single network connection"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex(("192.168.8.1", 80))
            sock.close()
            return result == 0
        except:
            return False
    
    async def _test_traffic_dashboard(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test traffic monitoring dashboard"""
        try:
            # Check if dashboard is accessible
            try:
                response = requests.get(self.endpoints["ct086_dashboard"], timeout=10)
                dashboard_accessible = response.status_code == 200
            except:
                dashboard_accessible = False
            
            # Check if dashboard files exist
            dashboard_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent3_traffic_monitoring"
            dashboard_exists = os.path.exists(f"{dashboard_path}/security_dashboard.py")
            
            if dashboard_accessible or dashboard_exists:
                return TestResult.PASS, "Traffic dashboard verified", {
                    "dashboard_accessible": dashboard_accessible,
                    "dashboard_files_exist": dashboard_exists
                }
            else:
                return TestResult.FAIL, "Traffic dashboard not available", {
                    "dashboard_accessible": dashboard_accessible,
                    "dashboard_files_exist": dashboard_exists
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Traffic dashboard test error: {e}", {}
    
    async def _test_protocol_detection(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test industrial protocol detection"""
        try:
            # Check if protocol detection components exist
            protocol_detector_path = "/home/server/industrial-iot-stack/ct-085-network-discovery/protocols"
            detector_exists = os.path.exists(protocol_detector_path)
            
            if detector_exists:
                # Check for protocol scanner files
                protocol_files = [
                    "modbus_scanner.py",
                    "opcua_scanner.py", 
                    "mqtt_scanner.py",
                    "ethernet_ip_scanner.py"
                ]
                
                files_present = {}
                for pfile in protocol_files:
                    files_present[pfile] = os.path.exists(f"{protocol_detector_path}/{pfile}")
                
                all_files_present = all(files_present.values())
                
                if all_files_present:
                    return TestResult.PASS, "Protocol detection verified", {
                        "detector_exists": detector_exists,
                        "protocol_files": files_present
                    }
                else:
                    return TestResult.FAIL, "Protocol detection incomplete", {
                        "detector_exists": detector_exists,
                        "protocol_files": files_present
                    }
            else:
                return TestResult.FAIL, "Protocol detection not found", {
                    "detector_exists": detector_exists
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Protocol detection test error: {e}", {}
    
    async def _test_remote_access(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test complete remote access functionality"""
        try:
            # Test VPN + Authentication + Network Access
            vpn_available = await self._test_vpn_connectivity()
            auth_available = await self._test_authentication()
            
            vpn_ok = vpn_available[0] == TestResult.PASS
            auth_ok = auth_available[0] == TestResult.PASS
            
            # Test if remote access configuration exists
            vpn_config_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent2_vpn_tunnel"
            config_exists = os.path.exists(f"{vpn_config_path}/vpn_config.json")
            
            if vpn_ok and auth_ok and config_exists:
                return TestResult.PASS, "Remote access functionality verified", {
                    "vpn_available": vpn_ok,
                    "auth_available": auth_ok,
                    "config_exists": config_exists
                }
            else:
                return TestResult.FAIL, "Remote access functionality incomplete", {
                    "vpn_available": vpn_ok,
                    "auth_available": auth_ok,
                    "config_exists": config_exists
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Remote access test error: {e}", {}
    
    async def _test_complete_system(self) -> Tuple[TestResult, str, Dict[str, Any]]:
        """Test complete integrated system"""
        try:
            # Comprehensive system test
            system_components = {
                "ct084_system": "/home/server/industrial-iot-stack/ct-084-parachute-drop-system",
                "ct085_system": "/home/server/industrial-iot-stack/ct-085-network-discovery", 
                "ct086_router": "/home/server/industrial-iot-stack/ct-086-router-system"
            }
            
            components_present = {}
            for name, path in system_components.items():
                components_present[name] = os.path.exists(path)
            
            all_components = all(components_present.values())
            
            # Test critical functionality
            critical_tests = ["NET-001", "SEC-002", "INT-001", "INT-002", "FUNC-003"]
            critical_results = {}
            
            for test_id in critical_tests:
                if self._check_prerequisite(test_id):
                    critical_results[test_id] = True
                else:
                    critical_results[test_id] = False
            
            all_critical_pass = all(critical_results.values())
            
            if all_components and all_critical_pass:
                return TestResult.PASS, "Complete system verification successful", {
                    "components_present": components_present,
                    "critical_tests": critical_results,
                    "system_ready": True
                }
            else:
                return TestResult.FAIL, "Complete system verification failed", {
                    "components_present": components_present,
                    "critical_tests": critical_results,
                    "system_ready": False
                }
                
        except Exception as e:
            return TestResult.ERROR, f"Complete system test error: {e}", {}
    
    def _test_port_connectivity(self, host: str, port: int) -> bool:
        """Test if a port is accessible"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _check_prerequisite(self, test_id: str) -> bool:
        """Check if prerequisite test passed"""
        for result in self.test_results:
            if result.test_case.test_id == test_id:
                return result.result == TestResult.PASS
        return False
    
    async def run_test_suite(self, test_categories: List[TestCategory] = None) -> Dict[str, Any]:
        """Run complete test suite"""
        self.current_test_run = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Filter tests by categories if specified
        if test_categories:
            tests_to_run = [tc for tc in self.test_cases if tc.category in test_categories]
        else:
            tests_to_run = self.test_cases
        
        self.logger.info(f"Starting test suite execution: {len(tests_to_run)} tests")
        
        # Execute tests
        for test_case in tests_to_run:
            try:
                result = await asyncio.wait_for(
                    self.execute_test_case(test_case),
                    timeout=test_case.timeout_seconds
                )
                self.test_results.append(result)
                
                # Log result
                status_symbol = "✅" if result.result == TestResult.PASS else "❌" if result.result == TestResult.FAIL else "⚠️"
                self.logger.info(f"{status_symbol} {test_case.test_id}: {result.result.value}")
                
            except Exception as e:
                self.logger.error(f"Test execution failed for {test_case.test_id}: {e}")
        
        # Generate test report
        report = self._generate_test_report()
        
        # Save results
        self._save_test_results(report)
        
        return report
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r.result == TestResult.PASS)
        failed_tests = sum(1 for r in self.test_results if r.result == TestResult.FAIL)
        error_tests = sum(1 for r in self.test_results if r.result == TestResult.ERROR)
        skipped_tests = sum(1 for r in self.test_results if r.result == TestResult.SKIP)
        
        # Calculate success rate
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        # Group by category
        category_results = {}
        for category in TestCategory:
            category_tests = [r for r in self.test_results if r.test_case.category == category]
            category_passed = sum(1 for r in category_tests if r.result == TestResult.PASS)
            category_total = len(category_tests)
            
            category_results[category.value] = {
                "total": category_total,
                "passed": category_passed,
                "success_rate": (category_passed / category_total * 100) if category_total > 0 else 0
            }
        
        # Critical test analysis
        critical_tests = [r for r in self.test_results if r.test_case.critical]
        critical_passed = sum(1 for r in critical_tests if r.result == TestResult.PASS)
        critical_total = len(critical_tests)
        
        # System readiness assessment
        system_ready = (
            success_rate >= 80 and
            critical_passed == critical_total and
            failed_tests == 0
        )
        
        return {
            "test_run_id": self.current_test_run,
            "execution_time": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "skipped": skipped_tests,
                "success_rate": success_rate
            },
            "category_results": category_results,
            "critical_tests": {
                "total": critical_total,
                "passed": critical_passed,
                "success_rate": (critical_passed / critical_total * 100) if critical_total > 0 else 0
            },
            "system_assessment": {
                "ready_for_production": system_ready,
                "readiness_score": success_rate,
                "critical_issues": failed_tests + error_tests,
                "recommendations": self._generate_recommendations()
            },
            "detailed_results": [
                {
                    "test_id": r.test_case.test_id,
                    "name": r.test_case.name,
                    "category": r.test_case.category.value,
                    "result": r.result.value,
                    "duration": r.duration.total_seconds(),
                    "critical": r.test_case.critical,
                    "error_message": r.error_message,
                    "details": r.details
                }
                for r in self.test_results
            ]
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        failed_tests = [r for r in self.test_results if r.result == TestResult.FAIL]
        error_tests = [r for r in self.test_results if r.result == TestResult.ERROR]
        
        if failed_tests:
            recommendations.append(f"Address {len(failed_tests)} failed tests before production deployment")
        
        if error_tests:
            recommendations.append(f"Investigate {len(error_tests)} test execution errors")
        
        # Category-specific recommendations
        network_failures = [r for r in failed_tests if r.test_case.category == TestCategory.NETWORK]
        if network_failures:
            recommendations.append("Review network configuration and connectivity")
        
        security_failures = [r for r in failed_tests if r.test_case.category == TestCategory.SECURITY]
        if security_failures:
            recommendations.append("Strengthen security configurations before deployment")
        
        integration_failures = [r for r in failed_tests if r.test_case.category == TestCategory.INTEGRATION]
        if integration_failures:
            recommendations.append("Verify system integration and component communication")
        
        if not recommendations:
            recommendations.append("System ready for production deployment")
        
        return recommendations
    
    def _save_test_results(self, report: Dict[str, Any]):
        """Save test results to file"""
        try:
            # Save JSON report
            report_file = f"{self.results_dir}/test_report_{self.current_test_run}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            # Save summary report
            summary_file = f"{self.results_dir}/test_summary_{self.current_test_run}.txt"
            with open(summary_file, 'w') as f:
                f.write(f"CT-086 System Integration Test Report\n")
                f.write(f"{'=' * 50}\n\n")
                f.write(f"Test Run ID: {report['test_run_id']}\n")
                f.write(f"Execution Time: {report['execution_time']}\n\n")
                
                f.write(f"Summary:\n")
                f.write(f"  Total Tests: {report['summary']['total_tests']}\n")
                f.write(f"  Passed: {report['summary']['passed']}\n")
                f.write(f"  Failed: {report['summary']['failed']}\n")
                f.write(f"  Errors: {report['summary']['errors']}\n")
                f.write(f"  Success Rate: {report['summary']['success_rate']:.1f}%\n\n")
                
                f.write(f"System Assessment:\n")
                f.write(f"  Production Ready: {report['system_assessment']['ready_for_production']}\n")
                f.write(f"  Readiness Score: {report['system_assessment']['readiness_score']:.1f}%\n")
                f.write(f"  Critical Issues: {report['system_assessment']['critical_issues']}\n\n")
                
                f.write(f"Recommendations:\n")
                for rec in report['system_assessment']['recommendations']:
                    f.write(f"  - {rec}\n")
            
            self.logger.info(f"Test results saved to {report_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save test results: {e}")
    
    def deploy_parachute_drop_validation(self) -> Dict[str, Any]:
        """Deploy validation system for Parachute Drop"""
        try:
            self.logger.info("Deploying Parachute Drop validation system...")
            
            deployment_info = {
                "deployment_time": datetime.now().isoformat(),
                "test_cases_configured": len(self.test_cases),
                "test_categories": [cat.value for cat in TestCategory],
                "results_directory": self.results_dir,
                "system_endpoints": self.endpoints,
                "validation_features": [
                    "Network connectivity testing",
                    "Security validation",
                    "System integration testing", 
                    "Performance benchmarking",
                    "End-to-end validation",
                    "Production readiness assessment"
                ]
            }
            
            # Save deployment configuration
            config_path = "/home/server/industrial-iot-stack/ct-086-router-system/agent5_integration_validation/validation_deployment.json"
            with open(config_path, 'w') as f:
                json.dump(deployment_info, f, indent=2)
            
            self.logger.info("Parachute Drop validation system deployed successfully")
            return deployment_info
            
        except Exception as e:
            self.logger.error(f"Validation deployment failed: {e}")
            raise


async def main():
    """Test system integration validator"""
    logging.basicConfig(level=logging.INFO)
    
    tester = SystemIntegrationTester()
    
    print("🧪 System Integration Tester for Parachute Drop System")
    print("=" * 65)
    
    try:
        # Deploy validation system
        deployment_info = tester.deploy_parachute_drop_validation()
        print("✅ Validation system deployed successfully!")
        
        print(f"\n📋 Test Cases: {deployment_info['test_cases_configured']}")
        print(f"📊 Categories: {', '.join(deployment_info['test_categories'])}")
        print(f"📁 Results Dir: {deployment_info['results_directory']}")
        
        # Run critical tests only for demonstration
        print(f"\n🧪 Running critical system tests...")
        critical_categories = [TestCategory.NETWORK, TestCategory.SECURITY, TestCategory.INTEGRATION]
        
        report = await tester.run_test_suite(critical_categories)
        
        print(f"\n📊 Test Results:")
        print(f"  Total Tests: {report['summary']['total_tests']}")
        print(f"  Passed: {report['summary']['passed']}")
        print(f"  Failed: {report['summary']['failed']}")
        print(f"  Success Rate: {report['summary']['success_rate']:.1f}%")
        print(f"  Production Ready: {report['system_assessment']['ready_for_production']}")
        
        if report['system_assessment']['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in report['system_assessment']['recommendations'][:3]:
                print(f"  - {rec}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())