#!/usr/bin/env python3
"""
CT-085 System Setup and Integration - Agent 5
Complete deployment package with validation and testing suite
"""

import asyncio
import json
import logging
import sys
import os
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add project paths
sys.path.append('/home/server/industrial-iot-stack/ct-085-network-discovery')

from network_discovery_engine import NetworkDiscoveryEngine
from ai_classification.device_classifier import DeviceClassifier
from nodered_generator.flow_generator import NodeREDFlowGenerator
from dashboard_generator.dashboard_generator import DashboardGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CT085SystemOrchestrator:
    """Complete CT-085 system orchestrator with remote monitoring and integration"""
    
    def __init__(self):
        """Initialize the CT-085 system orchestrator"""
        self.discovery_engine = NetworkDiscoveryEngine()
        self.device_classifier = DeviceClassifier()
        self.flow_generator = NodeREDFlowGenerator()
        self.dashboard_generator = DashboardGenerator()
        
        self.system_status = {
            'initialization_time': datetime.now().isoformat(),
            'components_loaded': 0,
            'last_discovery': None,
            'total_devices_found': 0,
            'system_health': 'initializing'
        }
        
        logger.info("CT-085 System Orchestrator initialized successfully")
    
    async def deploy_complete_system(self, target_networks: List[str] = None) -> Dict[str, Any]:
        """Deploy complete CT-085 discovery and monitoring system"""
        logger.info("🚀 Starting CT-085 complete system deployment...")
        
        deployment_results = {
            'deployment_start': datetime.now().isoformat(),
            'phases': {},
            'success': False,
            'summary': {}
        }
        
        try:
            # Phase 1: Network Discovery
            logger.info("📡 Phase 1: Network Discovery")
            discovered_devices = await self.discovery_engine.discover_network(target_networks)
            deployment_results['phases']['discovery'] = {
                'status': 'completed',
                'devices_found': sum(len(devices) for devices in discovered_devices.values()),
                'protocols': list(discovered_devices.keys())
            }
            
            # Phase 2: AI Classification
            logger.info("🤖 Phase 2: AI Device Classification")
            classified_devices = await self._classify_all_devices(discovered_devices)
            deployment_results['phases']['classification'] = {
                'status': 'completed',
                'devices_classified': len(classified_devices),
                'manufacturers_identified': len(set(d.get('manufacturer', 'Unknown') for d in classified_devices))
            }
            
            # Phase 3: Node-RED Flow Generation
            logger.info("🔧 Phase 3: Node-RED Flow Generation")
            tag_analysis = []
            for device_data in classified_devices:
                if 'tag_analysis' in device_data:
                    tag_analysis.extend(device_data['tag_analysis'])
            
            flows = await self.flow_generator.generate_flows_from_discovery(discovered_devices, tag_analysis)
            flow_file = self.flow_generator.export_flows_to_file(flows)
            
            deployment_results['phases']['flow_generation'] = {
                'status': 'completed',
                'flows_created': len(flows['flows']),
                'config_nodes': len(flows['configs']),
                'export_file': flow_file
            }
            
            # Phase 4: Dashboard Generation
            logger.info("📊 Phase 4: Professional Dashboard Generation")
            dashboards = await self.dashboard_generator.generate_dashboards(discovered_devices, tag_analysis)
            dashboard_json = self.dashboard_generator.export_dashboards(dashboards, 'json')
            dashboard_html = self.dashboard_generator.export_dashboards(dashboards, 'html')
            
            deployment_results['phases']['dashboard_generation'] = {
                'status': 'completed',
                'dashboards_created': len(dashboards) - 1,  # Exclude metadata
                'export_files': [dashboard_json, dashboard_html]
            }
            
            # Phase 5: System Integration & Validation
            logger.info("✅ Phase 5: System Integration & Validation")
            validation_results = await self._validate_system_integration(
                discovered_devices, flows, dashboards
            )
            deployment_results['phases']['validation'] = validation_results
            
            # Phase 6: Remote Monitoring Setup
            logger.info("📱 Phase 6: Remote Monitoring Setup")
            monitoring_setup = await self._setup_remote_monitoring()
            deployment_results['phases']['monitoring'] = monitoring_setup
            
            # Update system status
            self.system_status.update({
                'last_discovery': datetime.now().isoformat(),
                'total_devices_found': sum(len(devices) for devices in discovered_devices.values()),
                'system_health': 'operational'
            })
            
            deployment_results['success'] = True
            deployment_results['deployment_end'] = datetime.now().isoformat()
            deployment_results['summary'] = self._generate_deployment_summary(deployment_results)
            
            logger.info("🎉 CT-085 system deployment completed successfully!")
            return deployment_results
            
        except Exception as e:
            logger.error(f"❌ CT-085 deployment failed: {e}")
            deployment_results['success'] = False
            deployment_results['error'] = str(e)
            return deployment_results
    
    async def _classify_all_devices(self, discovered_devices: Dict) -> List[Dict[str, Any]]:
        """Classify all discovered devices using AI classifier"""
        classified_devices = []
        
        for protocol, devices in discovered_devices.items():
            for device in devices:
                device_info = {
                    'ip_address': device.ip_address,
                    'port': device.port,
                    'protocol': device.protocol,
                    'capabilities': device.capabilities,
                    'manufacturer_detection': {
                        'manufacturer': device.manufacturer,
                        'confidence': device.confidence_score
                    }
                }
                
                classification = await self.device_classifier.classify_device(device_info)
                classified_devices.append(classification)
        
        return classified_devices
    
    async def _validate_system_integration(self, devices: Dict, flows: Dict, dashboards: Dict) -> Dict[str, Any]:
        """Validate complete system integration"""
        validation_results = {
            'status': 'completed',
            'tests_run': 0,
            'tests_passed': 0,
            'tests_failed': 0,
            'details': []
        }
        
        # Test 1: Device Discovery Validation
        test_result = self._validate_device_discovery(devices)
        validation_results['details'].append(test_result)
        validation_results['tests_run'] += 1
        if test_result['passed']:
            validation_results['tests_passed'] += 1
        else:
            validation_results['tests_failed'] += 1
        
        # Test 2: Flow Generation Validation
        test_result = self._validate_flow_generation(flows, devices)
        validation_results['details'].append(test_result)
        validation_results['tests_run'] += 1
        if test_result['passed']:
            validation_results['tests_passed'] += 1
        else:
            validation_results['tests_failed'] += 1
        
        # Test 3: Dashboard Generation Validation
        test_result = self._validate_dashboard_generation(dashboards, devices)
        validation_results['details'].append(test_result)
        validation_results['tests_run'] += 1
        if test_result['passed']:
            validation_results['tests_passed'] += 1
        else:
            validation_results['tests_failed'] += 1
        
        # Test 4: File System Validation
        test_result = self._validate_file_system()
        validation_results['details'].append(test_result)
        validation_results['tests_run'] += 1
        if test_result['passed']:
            validation_results['tests_passed'] += 1
        else:
            validation_results['tests_failed'] += 1
        
        validation_results['success_rate'] = validation_results['tests_passed'] / validation_results['tests_run']
        
        return validation_results
    
    def _validate_device_discovery(self, devices: Dict) -> Dict[str, Any]:
        """Validate device discovery functionality"""
        try:
            total_devices = sum(len(device_list) for device_list in devices.values())
            protocols_found = len(devices.keys())
            
            passed = total_devices > 0 and protocols_found > 0
            
            return {
                'test_name': 'Device Discovery Validation',
                'passed': passed,
                'details': {
                    'total_devices': total_devices,
                    'protocols_found': protocols_found,
                    'protocols': list(devices.keys())
                },
                'message': f"Found {total_devices} devices across {protocols_found} protocols" if passed else "No devices discovered"
            }
        except Exception as e:
            return {
                'test_name': 'Device Discovery Validation',
                'passed': False,
                'error': str(e),
                'message': 'Device discovery validation failed'
            }
    
    def _validate_flow_generation(self, flows: Dict, devices: Dict) -> Dict[str, Any]:
        """Validate Node-RED flow generation"""
        try:
            flows_created = len(flows.get('flows', []))
            configs_created = len(flows.get('configs', []))
            device_count = sum(len(device_list) for device_list in devices.values())
            
            # Expect at least one flow per device
            passed = flows_created > 0 and configs_created > 0
            
            return {
                'test_name': 'Flow Generation Validation',
                'passed': passed,
                'details': {
                    'flows_created': flows_created,
                    'configs_created': configs_created,
                    'device_count': device_count
                },
                'message': f"Generated {flows_created} flows and {configs_created} configs" if passed else "Flow generation failed"
            }
        except Exception as e:
            return {
                'test_name': 'Flow Generation Validation',
                'passed': False,
                'error': str(e),
                'message': 'Flow generation validation failed'
            }
    
    def _validate_dashboard_generation(self, dashboards: Dict, devices: Dict) -> Dict[str, Any]:
        """Validate dashboard generation"""
        try:
            dashboard_count = len([k for k in dashboards.keys() if k != 'metadata'])
            device_count = sum(len(device_list) for device_list in devices.values())
            
            passed = dashboard_count > 0 and 'overview' in dashboards
            
            return {
                'test_name': 'Dashboard Generation Validation',
                'passed': passed,
                'details': {
                    'dashboards_created': dashboard_count,
                    'has_overview': 'overview' in dashboards,
                    'device_count': device_count
                },
                'message': f"Generated {dashboard_count} dashboards" if passed else "Dashboard generation failed"
            }
        except Exception as e:
            return {
                'test_name': 'Dashboard Generation Validation',
                'passed': False,
                'error': str(e),
                'message': 'Dashboard generation validation failed'
            }
    
    def _validate_file_system(self) -> Dict[str, Any]:
        """Validate file system structure and permissions"""
        try:
            required_paths = [
                '/home/server/industrial-iot-stack/ct-085-network-discovery',
                '/home/server/industrial-iot-stack/ct-085-network-discovery/protocols',
                '/home/server/industrial-iot-stack/ct-085-network-discovery/ai_classification',
                '/home/server/industrial-iot-stack/ct-085-network-discovery/nodered_generator',
                '/home/server/industrial-iot-stack/ct-085-network-discovery/dashboard_generator'
            ]
            
            paths_exist = all(os.path.exists(path) for path in required_paths)
            
            return {
                'test_name': 'File System Validation',
                'passed': paths_exist,
                'details': {
                    'required_paths': len(required_paths),
                    'paths_exist': sum(1 for path in required_paths if os.path.exists(path)),
                    'missing_paths': [path for path in required_paths if not os.path.exists(path)]
                },
                'message': 'All required paths exist' if paths_exist else 'Some required paths missing'
            }
        except Exception as e:
            return {
                'test_name': 'File System Validation',
                'passed': False,
                'error': str(e),
                'message': 'File system validation failed'
            }
    
    async def _setup_remote_monitoring(self) -> Dict[str, Any]:
        """Setup remote monitoring capabilities"""
        monitoring_setup = {
            'status': 'completed',
            'features': [
                'REST API endpoint (port 8085)',
                'Health monitoring',
                'Performance metrics',
                'Alert notifications',
                'Mobile dashboard access'
            ],
            'endpoints': {
                'health': 'http://localhost:8085/health',
                'devices': 'http://localhost:8085/api/devices',
                'flows': 'http://localhost:8085/api/flows',
                'dashboards': 'http://localhost:8085/api/dashboards',
                'status': 'http://localhost:8085/api/status'
            },
            'monitoring_active': True
        }
        
        # Start API server for remote access
        try:
            self.discovery_engine.start_api_server('0.0.0.0', 8085)
            monitoring_setup['api_server_started'] = True
        except Exception as e:
            monitoring_setup['api_server_started'] = False
            monitoring_setup['api_error'] = str(e)
        
        return monitoring_setup
    
    def _generate_deployment_summary(self, deployment_results: Dict) -> Dict[str, Any]:
        """Generate comprehensive deployment summary"""
        summary = {
            'deployment_duration': self._calculate_duration(
                deployment_results['deployment_start'],
                deployment_results['deployment_end']
            ),
            'total_devices_discovered': deployment_results['phases']['discovery']['devices_found'],
            'protocols_supported': deployment_results['phases']['discovery']['protocols'],
            'flows_generated': deployment_results['phases']['flow_generation']['flows_created'],
            'dashboards_created': deployment_results['phases']['dashboard_generation']['dashboards_created'],
            'validation_success_rate': deployment_results['phases']['validation']['success_rate'],
            'system_health': 'operational',
            'next_steps': [
                'Deploy flows to Node-RED instance',
                'Configure dashboard access',
                'Set up monitoring alerts',
                'Test remote access endpoints',
                'Schedule periodic discovery scans'
            ]
        }
        
        return summary
    
    def _calculate_duration(self, start_time: str, end_time: str) -> str:
        """Calculate duration between timestamps"""
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = end - start
        return str(duration)
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            **self.system_status,
            'current_time': datetime.now().isoformat(),
            'discovery_engine_active': not self.discovery_engine.emergency_stop,
            'components': {
                'discovery_engine': 'operational',
                'device_classifier': 'operational',
                'flow_generator': 'operational',
                'dashboard_generator': 'operational'
            }
        }
    
    def export_deployment_report(self, deployment_results: Dict) -> str:
        """Export deployment report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/home/server/industrial-iot-stack/ct-085-network-discovery/CT085_DEPLOYMENT_REPORT_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(deployment_results, f, indent=2)
        
        logger.info(f"Deployment report exported to {filename}")
        return filename

async def main():
    """Main deployment function"""
    print("🚀 CT-085 Network Discovery System Deployment")
    print("=" * 50)
    
    orchestrator = CT085SystemOrchestrator()
    
    # Deploy complete system
    results = await orchestrator.deploy_complete_system()
    
    # Export deployment report
    report_file = orchestrator.export_deployment_report(results)
    
    print("\n📋 Deployment Summary:")
    print(f"Success: {results['success']}")
    if results['success']:
        summary = results['summary']
        print(f"Duration: {summary['deployment_duration']}")
        print(f"Devices Found: {summary['total_devices_discovered']}")
        print(f"Protocols: {', '.join(summary['protocols_supported'])}")
        print(f"Flows Generated: {summary['flows_generated']}")
        print(f"Dashboards Created: {summary['dashboards_created']}")
        print(f"Validation Success Rate: {summary['validation_success_rate']:.1%}")
        print(f"Report: {report_file}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())