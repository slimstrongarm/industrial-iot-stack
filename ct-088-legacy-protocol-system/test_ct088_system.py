#!/usr/bin/env python3
"""
CT-088 Legacy Protocol System - Integration Testing and Validation
Comprehensive validation of the 3-agent legacy protocol system
"""

import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime

def validate_system_outputs():
    """Validate all system output files and data"""
    validation_results = {
        'timestamp': datetime.now().isoformat(),
        'validation_status': 'passed',
        'validations': []
    }
    
    required_files = [
        '/tmp/ct-088-legacy-protocol-scan.json',
        '/tmp/ct-088-discovery-mapping.json', 
        '/tmp/ct-088-register-map.db',
        '/tmp/ct-088-nodered-flows.json',
        '/tmp/ct-088-dashboards.json',
        '/tmp/ct-088-monitoring-config.json',
        '/tmp/ct-088-system-summary.json'
    ]
    
    # File existence validation
    for file_path in required_files:
        if os.path.exists(file_path):
            validation_results['validations'].append({
                'test': f'File exists: {file_path}',
                'status': 'passed'
            })
        else:
            validation_results['validations'].append({
                'test': f'File exists: {file_path}',
                'status': 'failed'
            })
            validation_results['validation_status'] = 'failed'
    
    # Database validation
    try:
        conn = sqlite3.connect('/tmp/ct-088-register-map.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM device_profiles')
        device_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM device_registers')
        register_count = cursor.fetchone()[0]
        
        validation_results['validations'].append({
            'test': 'Database schema validation',
            'status': 'passed',
            'details': f'{device_count} devices, {register_count} registers'
        })
        
        conn.close()
        
    except Exception as e:
        validation_results['validations'].append({
            'test': 'Database validation',
            'status': 'failed',
            'error': str(e)
        })
        validation_results['validation_status'] = 'failed'
    
    # JSON structure validation
    json_files = [
        '/tmp/ct-088-system-summary.json',
        '/tmp/ct-088-dashboards.json',
        '/tmp/ct-088-monitoring-config.json'
    ]
    
    for json_file in json_files:
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                validation_results['validations'].append({
                    'test': f'JSON validation: {json_file}',
                    'status': 'passed',
                    'size': len(str(data))
                })
        except Exception as e:
            validation_results['validations'].append({
                'test': f'JSON validation: {json_file}',
                'status': 'failed',
                'error': str(e)
            })
            validation_results['validation_status'] = 'failed'
    
    return validation_results

def validate_agent_completion():
    """Validate all agents completed successfully"""
    agent_validation = {
        'agents_validated': [],
        'all_agents_completed': True
    }
    
    expected_agents = [
        'agent1_legacy_protocol_engine',
        'agent2_auto_discovery_mapping', 
        'agent3_parachute_integration'
    ]
    
    base_path = Path('/home/server/industrial-iot-stack/ct-088-legacy-protocol-system')
    
    for agent_id in expected_agents:
        completion_file = base_path / f"{agent_id}_completion.json"
        
        if completion_file.exists():
            try:
                with open(completion_file, 'r') as f:
                    completion_data = json.load(f)
                    
                agent_validation['agents_validated'].append({
                    'agent_id': agent_id,
                    'status': completion_data.get('status', 'unknown'),
                    'completion_time': completion_data.get('completion_time', 'unknown')
                })
                
                if completion_data.get('status') != 'completed':
                    agent_validation['all_agents_completed'] = False
                    
            except Exception as e:
                agent_validation['agents_validated'].append({
                    'agent_id': agent_id,
                    'status': 'validation_failed',
                    'error': str(e)
                })
                agent_validation['all_agents_completed'] = False
        else:
            agent_validation['agents_validated'].append({
                'agent_id': agent_id,
                'status': 'completion_file_missing'
            })
            agent_validation['all_agents_completed'] = False
    
    return agent_validation

def validate_protocol_support():
    """Validate protocol implementations"""
    protocol_validation = {
        'protocols_tested': [],
        'all_protocols_supported': True
    }
    
    try:
        with open('/tmp/ct-088-system-summary.json', 'r') as f:
            system_data = json.load(f)
            
        expected_protocols = [
            'Modbus RTU protocol support',
            'BACnet MS/TP protocol support', 
            'DF1 protocol support'
        ]
        
        capabilities = system_data.get('system_capabilities', [])
        
        for protocol in expected_protocols:
            if protocol in capabilities:
                protocol_validation['protocols_tested'].append({
                    'protocol': protocol,
                    'status': 'supported'
                })
            else:
                protocol_validation['protocols_tested'].append({
                    'protocol': protocol,
                    'status': 'not_found'
                })
                protocol_validation['all_protocols_supported'] = False
                
    except Exception as e:
        protocol_validation['validation_error'] = str(e)
        protocol_validation['all_protocols_supported'] = False
    
    return protocol_validation

def validate_integration_features():
    """Validate parachute drop integration features"""
    integration_validation = {
        'features_validated': [],
        'integration_complete': True
    }
    
    expected_features = [
        ('dashboards', '/tmp/ct-088-dashboards.json'),
        ('nodered_flows', '/tmp/ct-088-nodered-flows.json'), 
        ('monitoring_config', '/tmp/ct-088-monitoring-config.json')
    ]
    
    for feature_name, file_path in expected_features:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    
                integration_validation['features_validated'].append({
                    'feature': feature_name,
                    'status': 'validated',
                    'file_size': os.path.getsize(file_path),
                    'data_elements': len(data) if isinstance(data, (list, dict)) else 1
                })
                
            except Exception as e:
                integration_validation['features_validated'].append({
                    'feature': feature_name,
                    'status': 'validation_failed',
                    'error': str(e)
                })
                integration_validation['integration_complete'] = False
        else:
            integration_validation['features_validated'].append({
                'feature': feature_name,
                'status': 'file_missing'
            })
            integration_validation['integration_complete'] = False
    
    return integration_validation

def run_comprehensive_validation():
    """Run complete system validation"""
    print("🧪 CT-088 Legacy Protocol System - Validation Testing")
    print("=" * 60)
    
    validation_report = {
        'system': 'CT-088 Legacy Protocol System',
        'validation_timestamp': datetime.now().isoformat(),
        'overall_status': 'passed',
        'test_results': {}
    }
    
    # System outputs validation
    print("\n📁 Validating system outputs...")
    outputs_validation = validate_system_outputs()
    validation_report['test_results']['system_outputs'] = outputs_validation
    
    if outputs_validation['validation_status'] != 'passed':
        validation_report['overall_status'] = 'failed'
    
    # Agent completion validation
    print("\n🤖 Validating agent completion...")
    agent_validation = validate_agent_completion()
    validation_report['test_results']['agent_completion'] = agent_validation
    
    if not agent_validation['all_agents_completed']:
        validation_report['overall_status'] = 'failed'
    
    # Protocol support validation
    print("\n🔌 Validating protocol support...")
    protocol_validation = validate_protocol_support()
    validation_report['test_results']['protocol_support'] = protocol_validation
    
    if not protocol_validation['all_protocols_supported']:
        validation_report['overall_status'] = 'failed'
    
    # Integration features validation
    print("\n🔗 Validating integration features...")
    integration_validation = validate_integration_features()
    validation_report['test_results']['integration_features'] = integration_validation
    
    if not integration_validation['integration_complete']:
        validation_report['overall_status'] = 'failed'
    
    # Generate validation summary
    print(f"\n✅ Validation Summary:")
    print(f"   Overall Status: {validation_report['overall_status'].upper()}")
    print(f"   System Outputs: {'✅' if outputs_validation['validation_status'] == 'passed' else '❌'}")
    print(f"   Agent Completion: {'✅' if agent_validation['all_agents_completed'] else '❌'}")
    print(f"   Protocol Support: {'✅' if protocol_validation['all_protocols_supported'] else '❌'}")
    print(f"   Integration Features: {'✅' if integration_validation['integration_complete'] else '❌'}")
    
    # Save validation report
    with open('/tmp/ct-088-validation-report.json', 'w') as f:
        json.dump(validation_report, f, indent=2)
    
    print(f"\n📄 Validation report saved: /tmp/ct-088-validation-report.json")
    
    return validation_report['overall_status'] == 'passed'

if __name__ == "__main__":
    success = run_comprehensive_validation()
    exit(0 if success else 1)