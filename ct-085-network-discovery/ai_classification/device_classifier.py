#!/usr/bin/env python3
"""
CT-085 AI Device Classifier - Agent 2
AI-powered device classification and tag analysis system for industrial networks

This module provides intelligent device identification and tag purpose detection
using machine learning models and semantic analysis techniques.
"""

import asyncio
import json
import logging
import re
import pickle
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
import numpy as np
from collections import defaultdict
import sqlite3

logger = logging.getLogger(__name__)

@dataclass
class TagAnalysis:
    """Data class for analyzed industrial tag information"""
    tag_name: str
    tag_type: str
    purpose: str
    data_type: str
    units: str
    description: str
    category: str
    criticality: str
    update_frequency: str
    confidence_score: float

@dataclass
class DeviceClassification:
    """Data class for device classification results"""
    device_type: str
    manufacturer: str
    model: str
    confidence_score: float
    capabilities: List[str]
    tag_analysis: List[TagAnalysis]
    semantic_fingerprint: Dict[str, Any]

class DeviceClassifier:
    """
    AI-powered device classifier with semantic tag analysis
    Uses machine learning models and pattern recognition for industrial device identification
    """
    
    # Industrial device type patterns
    DEVICE_TYPE_PATTERNS = {
        'PLC': [
            r'program.*logic.*control', r'plc', r'cpu', r'controller',
            r'automation.*controller', r'programmable.*controller'
        ],
        'HMI': [
            r'human.*machine.*interface', r'hmi', r'operator.*panel',
            r'touch.*panel', r'display.*unit'
        ],
        'Drive': [
            r'variable.*frequency.*drive', r'vfd', r'inverter', r'drive',
            r'motor.*controller', r'speed.*controller'
        ],
        'I/O Module': [
            r'input.*output', r'i/o.*module', r'remote.*i/o', r'field.*i/o',
            r'digital.*input', r'analog.*input', r'digital.*output', r'analog.*output'
        ],
        'Sensor': [
            r'sensor', r'transmitter', r'transducer', r'detector',
            r'temperature.*sensor', r'pressure.*sensor', r'flow.*sensor'
        ],
        'Gateway': [
            r'gateway', r'bridge', r'converter', r'protocol.*gateway',
            r'communication.*gateway', r'fieldbus.*gateway'
        ],
        'Safety System': [
            r'safety.*plc', r'emergency.*stop', r'safety.*relay',
            r'safety.*controller', r'sis', r'safety.*instrumented'
        ]
    }
    
    # Tag purpose classification patterns
    TAG_PURPOSE_PATTERNS = {
        'Process Variable': [
            r'pv', r'process.*value', r'measured.*value', r'actual.*value',
            r'temperature', r'pressure', r'flow', r'level', r'ph', r'conductivity'
        ],
        'Setpoint': [
            r'sp', r'setpoint', r'set.*point', r'target.*value', r'desired.*value',
            r'reference.*value', r'command.*value'
        ],
        'Control Output': [
            r'cv', r'control.*value', r'output.*value', r'manipulated.*variable',
            r'control.*signal', r'actuator.*position'
        ],
        'Alarm': [
            r'alarm', r'alert', r'warning', r'fault', r'error',
            r'high.*alarm', r'low.*alarm', r'critical.*alarm'
        ],
        'Status': [
            r'status', r'state', r'condition', r'mode', r'running',
            r'stopped', r'manual', r'automatic', r'enabled', r'disabled'
        ],
        'Counter': [
            r'count', r'counter', r'total', r'accumulator', r'batch.*count',
            r'cycle.*count', r'production.*count'
        ],
        'Configuration': [
            r'config', r'parameter', r'setting', r'gain', r'offset',
            r'scale', r'calibration', r'tuning'
        ]
    }
    
    # Manufacturer identification patterns
    MANUFACTURER_SIGNATURES = {
        'Allen-Bradley': {
            'protocols': ['ethernet_ip', 'modbus'],
            'tag_patterns': [r'PLC_', r'HMI_', r'AB_', r'LOCAL:', r'PROGRAM:'],
            'model_patterns': [r'1756', r'1769', r'CompactLogix', r'ControlLogix', r'MicroLogix'],
            'characteristic_tags': ['GSV', 'SSV', 'MSG', 'COP', 'MOV']
        },
        'Schneider Electric': {
            'protocols': ['modbus', 'ethernet_ip'],
            'tag_patterns': [r'MW', r'%M', r'%I', r'%Q', r'SCHNEIDER_'],
            'model_patterns': [r'M340', r'M580', r'Modicon', r'Unity', r'EcoStruxure'],
            'characteristic_tags': ['BOOL', 'INT', 'DINT', 'REAL', 'STRING']
        },
        'Siemens': {
            'protocols': ['opcua', 'modbus'],
            'tag_patterns': [r'DB', r'M', r'I', r'Q', r'SIMATIC_'],
            'model_patterns': [r'S7-300', r'S7-400', r'S7-1200', r'S7-1500', r'SIMATIC'],
            'characteristic_tags': ['DB', 'FC', 'FB', 'OB', 'UDT']
        },
        'Omron': {
            'protocols': ['ethernet_ip', 'modbus'],
            'tag_patterns': [r'D', r'W', r'H', r'CIO', r'OMRON_'],
            'model_patterns': [r'CJ', r'CP', r'NX', r'NJ', r'Sysmac'],
            'characteristic_tags': ['CIO', 'WR', 'HR', 'AR', 'DM']
        }
    }
    
    def __init__(self):
        """Initialize the AI device classifier"""
        self.classification_cache = {}
        self.tag_database = {}
        self.learning_data = defaultdict(list)
        self.confidence_threshold = 0.7
        
        # Load pre-trained models (in a real implementation, these would be actual ML models)
        self.device_embeddings = self._load_device_embeddings()
        self.tag_embeddings = self._load_tag_embeddings()
        
        logger.info("AI Device Classifier initialized successfully")
    
    def _load_device_embeddings(self) -> Dict[str, np.ndarray]:
        """Load pre-trained device embeddings for classification"""
        # In a real implementation, this would load actual embeddings
        # For now, we'll create synthetic embeddings based on common patterns
        
        embeddings = {}
        for device_type in self.DEVICE_TYPE_PATTERNS.keys():
            # Create synthetic embedding (in reality, this would be from training data)
            embedding = np.random.random(128)  # 128-dimensional embedding
            embeddings[device_type] = embedding
            
        return embeddings
    
    def _load_tag_embeddings(self) -> Dict[str, np.ndarray]:
        """Load pre-trained tag embeddings for purpose classification"""
        embeddings = {}
        for purpose in self.TAG_PURPOSE_PATTERNS.keys():
            # Create synthetic embedding
            embedding = np.random.random(64)  # 64-dimensional embedding
            embeddings[purpose] = embedding
            
        return embeddings
    
    async def classify_device(self, device_info: Dict) -> Dict[str, Any]:
        """
        Classify device using AI models and pattern analysis
        
        Args:
            device_info: Device information from network discovery
            
        Returns:
            Classification results with confidence scores
        """
        try:
            # Extract features for classification
            features = await self._extract_device_features(device_info)
            
            # Perform device type classification
            device_type, type_confidence = await self._classify_device_type(features)
            
            # Perform manufacturer identification
            manufacturer, manufacturer_confidence = await self._identify_manufacturer(features)
            
            # Perform model identification
            model, model_confidence = await self._identify_model(features, manufacturer)
            
            # Analyze tags if available
            tag_analysis = await self._analyze_device_tags(features)
            
            # Calculate overall confidence
            overall_confidence = (type_confidence + manufacturer_confidence + model_confidence) / 3
            
            # Generate semantic fingerprint
            semantic_fingerprint = await self._generate_semantic_fingerprint(features, tag_analysis)
            
            # Create classification result
            classification = DeviceClassification(
                device_type=device_type,
                manufacturer=manufacturer,
                model=model,
                confidence_score=overall_confidence,
                capabilities=features.get('capabilities', []),
                tag_analysis=tag_analysis,
                semantic_fingerprint=semantic_fingerprint
            )
            
            # Cache result for future use
            cache_key = f"{device_info.get('ip_address')}:{device_info.get('port')}"
            self.classification_cache[cache_key] = classification
            
            # Learn from this classification for future improvements
            await self._update_learning_data(features, classification)
            
            logger.info(f"Device classified: {manufacturer} {model} ({device_type}) with {overall_confidence:.2f} confidence")
            
            return {
                'device_type': device_type,
                'manufacturer': manufacturer,
                'model': model,
                'confidence_score': overall_confidence,
                'capabilities': features.get('capabilities', []),
                'tag_count': len(tag_analysis),
                'semantic_fingerprint': semantic_fingerprint
            }
            
        except Exception as e:
            logger.error(f"Device classification failed: {e}")
            return {
                'device_type': 'Unknown',
                'manufacturer': 'Unknown',
                'model': 'Unknown',
                'confidence_score': 0.0,
                'capabilities': [],
                'tag_count': 0,
                'semantic_fingerprint': {}
            }
    
    async def _extract_device_features(self, device_info: Dict) -> Dict[str, Any]:
        """Extract relevant features from device information"""
        features = {
            'protocol': device_info.get('protocol', ''),
            'port': device_info.get('port', 0),
            'capabilities': device_info.get('capabilities', []),
            'ip_address': device_info.get('ip_address', ''),
            'device_signature': device_info.get('device_signature', ''),
            'manufacturer_detection': device_info.get('manufacturer_detection', {}),
            'registers_found': device_info.get('registers_found', []),
            'ascii_data': [],
            'numeric_patterns': [],
            'string_patterns': []
        }
        
        # Extract ASCII data from registers
        for register_info in features['registers_found']:
            ascii_text = register_info.get('ascii', '')
            if ascii_text:
                features['ascii_data'].append(ascii_text)
        
        # Extract patterns from capability data
        if 'opcua' in features['protocol']:
            features['opcua_endpoints'] = device_info.get('endpoints', [])
            features['security_policies'] = device_info.get('security_policies', [])
        
        # Analyze protocol-specific data
        if 'modbus' in features['protocol']:
            features['unit_id'] = device_info.get('unit_id', 1)
            features['function_codes'] = self._extract_function_codes(features['capabilities'])
        
        return features
    
    def _extract_function_codes(self, capabilities: List[str]) -> List[int]:
        """Extract Modbus function codes from capabilities"""
        function_code_map = {
            'coils': 1,
            'discrete_inputs': 2,
            'holding_registers': 3,
            'input_registers': 4
        }
        
        return [function_code_map[cap] for cap in capabilities if cap in function_code_map]
    
    async def _classify_device_type(self, features: Dict[str, Any]) -> Tuple[str, float]:
        """Classify device type using pattern matching and ML"""
        scores = {}
        
        # Pattern-based classification
        ascii_text = ' '.join(features['ascii_data']).lower()
        
        for device_type, patterns in self.DEVICE_TYPE_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, ascii_text, re.IGNORECASE):
                    score += 1
            
            if score > 0:
                scores[device_type] = score / len(patterns)
        
        # Protocol-based hints
        protocol = features['protocol']
        if protocol == 'modbus':
            scores['PLC'] = scores.get('PLC', 0) + 0.3
            scores['I/O Module'] = scores.get('I/O Module', 0) + 0.2
        elif protocol == 'opcua':
            scores['HMI'] = scores.get('HMI', 0) + 0.3
            scores['Gateway'] = scores.get('Gateway', 0) + 0.2
        elif protocol == 'ethernet_ip':
            scores['PLC'] = scores.get('PLC', 0) + 0.4
            scores['Drive'] = scores.get('Drive', 0) + 0.2
        
        # Port-based hints
        port = features['port']
        if port == 502:  # Modbus
            scores['PLC'] = scores.get('PLC', 0) + 0.2
        elif port == 4840:  # OPC-UA
            scores['HMI'] = scores.get('HMI', 0) + 0.2
        elif port == 44818:  # EtherNet/IP
            scores['PLC'] = scores.get('PLC', 0) + 0.3
        
        # Determine best match
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = scores[best_type]
            return best_type, min(confidence, 1.0)
        else:
            return 'Unknown Device', 0.1
    
    async def _identify_manufacturer(self, features: Dict[str, Any]) -> Tuple[str, float]:
        """Identify device manufacturer using signature matching"""
        scores = {}
        
        # Check existing manufacturer detection from protocol scanners
        manufacturer_detection = features.get('manufacturer_detection', {})
        if manufacturer_detection and 'manufacturer' in manufacturer_detection:
            detected_manufacturer = manufacturer_detection['manufacturer']
            confidence = manufacturer_detection.get('confidence', 0.5)
            return detected_manufacturer, confidence
        
        # ASCII pattern matching
        ascii_text = ' '.join(features['ascii_data']).upper()
        
        for manufacturer, signature in self.MANUFACTURER_SIGNATURES.items():
            score = 0
            
            # Check tag patterns
            for pattern in signature['tag_patterns']:
                if re.search(pattern, ascii_text, re.IGNORECASE):
                    score += 2
            
            # Check model patterns
            for pattern in signature['model_patterns']:
                if re.search(pattern, ascii_text, re.IGNORECASE):
                    score += 3
            
            # Check protocol compatibility
            protocol = features['protocol']
            if protocol in signature['protocols']:
                score += 1
            
            if score > 0:
                scores[manufacturer] = score / 6  # Normalize score
        
        # Determine best match
        if scores:
            best_manufacturer = max(scores, key=scores.get)
            confidence = scores[best_manufacturer]
            return best_manufacturer, min(confidence, 1.0)
        else:
            return 'Unknown', 0.1
    
    async def _identify_model(self, features: Dict[str, Any], manufacturer: str) -> Tuple[str, float]:
        """Identify specific device model"""
        if manufacturer == 'Unknown':
            return 'Unknown', 0.1
        
        ascii_text = ' '.join(features['ascii_data']).upper()
        
        if manufacturer in self.MANUFACTURER_SIGNATURES:
            signature = self.MANUFACTURER_SIGNATURES[manufacturer]
            
            for model_pattern in signature['model_patterns']:
                match = re.search(model_pattern, ascii_text, re.IGNORECASE)
                if match:
                    return match.group(0), 0.8
        
        # Generic model identification based on protocol and capabilities
        protocol = features['protocol']
        capabilities = features['capabilities']
        
        if manufacturer == 'Allen-Bradley':
            if 'ethernet_ip' in protocol:
                return 'ControlLogix/CompactLogix', 0.6
            elif 'modbus' in protocol:
                return 'MicroLogix', 0.6
        elif manufacturer == 'Schneider Electric':
            if len(capabilities) > 3:
                return 'Modicon M580', 0.6
            else:
                return 'Modicon M340', 0.6
        elif manufacturer == 'Siemens':
            if 'opcua' in protocol:
                return 'S7-1500', 0.6
            else:
                return 'S7-300/400', 0.6
        
        return 'Unknown Model', 0.2
    
    async def _analyze_device_tags(self, features: Dict[str, Any]) -> List[TagAnalysis]:
        """Analyze device tags for purpose and semantic meaning"""
        tag_analyses = []
        
        # Extract tag information from various sources
        tags = []
        
        # From ASCII data (look for tag-like patterns)
        for ascii_data in features['ascii_data']:
            # Look for tag patterns like "TAG_NAME", "PV_01", etc.
            tag_matches = re.findall(r'[A-Z][A-Z0-9_]{2,}', ascii_data)
            tags.extend(tag_matches)
        
        # From capabilities (convert to tag-like names)
        for capability in features['capabilities']:
            tag_name = f"CAPABILITY_{capability.upper()}"
            tags.append(tag_name)
        
        # Analyze each tag
        for tag_name in tags[:20]:  # Limit to first 20 tags for performance
            analysis = await self._analyze_single_tag(tag_name)
            if analysis:
                tag_analyses.append(analysis)
        
        return tag_analyses
    
    async def _analyze_single_tag(self, tag_name: str) -> Optional[TagAnalysis]:
        """Analyze a single tag for purpose and meaning"""
        try:
            # Determine tag purpose
            purpose, purpose_confidence = self._classify_tag_purpose(tag_name)
            
            # Determine data type
            data_type = self._infer_data_type(tag_name)
            
            # Determine units
            units = self._infer_units(tag_name)
            
            # Generate description
            description = self._generate_tag_description(tag_name, purpose)
            
            # Determine category
            category = self._determine_tag_category(tag_name, purpose)
            
            # Assess criticality
            criticality = self._assess_tag_criticality(tag_name, purpose)
            
            # Estimate update frequency
            update_frequency = self._estimate_update_frequency(tag_name, purpose)
            
            return TagAnalysis(
                tag_name=tag_name,
                tag_type='Process' if purpose != 'Configuration' else 'Configuration',
                purpose=purpose,
                data_type=data_type,
                units=units,
                description=description,
                category=category,
                criticality=criticality,
                update_frequency=update_frequency,
                confidence_score=purpose_confidence
            )
            
        except Exception as e:
            logger.debug(f"Tag analysis failed for {tag_name}: {e}")
            return None
    
    def _classify_tag_purpose(self, tag_name: str) -> Tuple[str, float]:
        """Classify the purpose of a tag"""
        scores = {}
        
        tag_lower = tag_name.lower()
        
        for purpose, patterns in self.TAG_PURPOSE_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, tag_lower):
                    score += 1
            
            if score > 0:
                scores[purpose] = score / len(patterns)
        
        if scores:
            best_purpose = max(scores, key=scores.get)
            confidence = scores[best_purpose]
            return best_purpose, confidence
        else:
            return 'Unknown', 0.1
    
    def _infer_data_type(self, tag_name: str) -> str:
        """Infer data type from tag name"""
        tag_lower = tag_name.lower()
        
        if re.search(r'temp|pressure|flow|level|speed|rate', tag_lower):
            return 'REAL'
        elif re.search(r'count|total|batch|cycle', tag_lower):
            return 'INT'
        elif re.search(r'running|stopped|alarm|fault|enable', tag_lower):
            return 'BOOL'
        elif re.search(r'name|description|message|text', tag_lower):
            return 'STRING'
        else:
            return 'UNKNOWN'
    
    def _infer_units(self, tag_name: str) -> str:
        """Infer engineering units from tag name"""
        tag_lower = tag_name.lower()
        
        unit_patterns = {
            'degC': [r'temp', r'temperature'],
            'bar': [r'pressure', r'press'],
            'L/min': [r'flow'],
            'mm': [r'level', r'position'],
            'rpm': [r'speed', r'motor'],
            '%': [r'percent', r'pct', r'valve'],
            'count': [r'count', r'total', r'batch'],
            'seconds': [r'time', r'timer']
        }
        
        for unit, patterns in unit_patterns.items():
            for pattern in patterns:
                if re.search(pattern, tag_lower):
                    return unit
        
        return 'dimensionless'
    
    def _generate_tag_description(self, tag_name: str, purpose: str) -> str:
        """Generate human-readable description for tag"""
        # Simple description generation based on tag name and purpose
        base_description = tag_name.replace('_', ' ').title()
        return f"{purpose}: {base_description}"
    
    def _determine_tag_category(self, tag_name: str, purpose: str) -> str:
        """Determine functional category of tag"""
        tag_lower = tag_name.lower()
        
        if purpose in ['Process Variable', 'Setpoint', 'Control Output']:
            if re.search(r'temp|temperature', tag_lower):
                return 'Temperature Control'
            elif re.search(r'pressure|press', tag_lower):
                return 'Pressure Control'
            elif re.search(r'flow', tag_lower):
                return 'Flow Control'
            elif re.search(r'level', tag_lower):
                return 'Level Control'
            else:
                return 'Process Control'
        elif purpose in ['Alarm', 'Status']:
            return 'Monitoring'
        elif purpose == 'Counter':
            return 'Production Tracking'
        elif purpose == 'Configuration':
            return 'System Configuration'
        else:
            return 'General'
    
    def _assess_tag_criticality(self, tag_name: str, purpose: str) -> str:
        """Assess criticality level of tag"""
        tag_lower = tag_name.lower()
        
        # High criticality indicators
        if re.search(r'safety|emergency|critical|shutdown|trip', tag_lower):
            return 'Critical'
        elif re.search(r'alarm|fault|error|warning', tag_lower):
            return 'High'
        elif purpose in ['Process Variable', 'Control Output']:
            return 'Medium'
        else:
            return 'Low'
    
    def _estimate_update_frequency(self, tag_name: str, purpose: str) -> str:
        """Estimate how frequently tag value updates"""
        tag_lower = tag_name.lower()
        
        if purpose == 'Process Variable':
            if re.search(r'temp|temperature|pressure', tag_lower):
                return 'Slow (1-10 sec)'
            elif re.search(r'flow|speed|current', tag_lower):
                return 'Fast (100ms-1sec)'
            else:
                return 'Medium (1-5 sec)'
        elif purpose in ['Alarm', 'Status']:
            return 'Event-driven'
        elif purpose == 'Counter':
            return 'On-change'
        elif purpose == 'Configuration':
            return 'Static'
        else:
            return 'Unknown'
    
    async def _generate_semantic_fingerprint(self, features: Dict[str, Any], tag_analysis: List[TagAnalysis]) -> Dict[str, Any]:
        """Generate semantic fingerprint for device"""
        fingerprint = {
            'protocol_signature': features['protocol'],
            'capability_vector': len(features['capabilities']),
            'tag_purposes': {},
            'data_type_distribution': {},
            'criticality_profile': {},
            'functional_categories': {}
        }
        
        # Analyze tag purposes
        for tag in tag_analysis:
            purpose = tag.purpose
            fingerprint['tag_purposes'][purpose] = fingerprint['tag_purposes'].get(purpose, 0) + 1
        
        # Analyze data types
        for tag in tag_analysis:
            data_type = tag.data_type
            fingerprint['data_type_distribution'][data_type] = fingerprint['data_type_distribution'].get(data_type, 0) + 1
        
        # Analyze criticality
        for tag in tag_analysis:
            criticality = tag.criticality
            fingerprint['criticality_profile'][criticality] = fingerprint['criticality_profile'].get(criticality, 0) + 1
        
        # Analyze categories
        for tag in tag_analysis:
            category = tag.category
            fingerprint['functional_categories'][category] = fingerprint['functional_categories'].get(category, 0) + 1
        
        return fingerprint
    
    async def _update_learning_data(self, features: Dict[str, Any], classification: DeviceClassification):
        """Update learning data for continuous improvement"""
        learning_entry = {
            'timestamp': datetime.now().isoformat(),
            'features': features,
            'classification': classification,
            'confidence': classification.confidence_score
        }
        
        device_type = classification.device_type
        self.learning_data[device_type].append(learning_entry)
        
        # Keep only recent learning data (last 1000 entries per type)
        if len(self.learning_data[device_type]) > 1000:
            self.learning_data[device_type] = self.learning_data[device_type][-1000:]
    
    def get_classification_statistics(self) -> Dict[str, Any]:
        """Get statistics about classification performance"""
        stats = {
            'total_classifications': len(self.classification_cache),
            'device_types': {},
            'manufacturers': {},
            'average_confidence': 0.0,
            'learning_data_size': sum(len(data) for data in self.learning_data.values())
        }
        
        confidences = []
        for classification in self.classification_cache.values():
            device_type = classification.device_type
            manufacturer = classification.manufacturer
            confidence = classification.confidence_score
            
            stats['device_types'][device_type] = stats['device_types'].get(device_type, 0) + 1
            stats['manufacturers'][manufacturer] = stats['manufacturers'].get(manufacturer, 0) + 1
            confidences.append(confidence)
        
        if confidences:
            stats['average_confidence'] = sum(confidences) / len(confidences)
        
        return stats

# Test functionality
if __name__ == "__main__":
    async def test_device_classifier():
        classifier = DeviceClassifier()
        
        # Mock device info for testing
        test_device = {
            'ip_address': '192.168.1.100',
            'port': 502,
            'protocol': 'modbus',
            'capabilities': ['holding_registers', 'input_registers'],
            'registers_found': [
                {'address': 0x0000, 'values': [0x414C, 0x4C45], 'ascii': 'ALLE'},  # "ALLE" (Allen-Bradley)
                {'address': 0x0001, 'values': [0x4E2D, 0x4252], 'ascii': 'N-BR'},  # "N-BR"
            ],
            'manufacturer_detection': {
                'manufacturer': 'Allen-Bradley',
                'confidence': 0.85
            }
        }
        
        # Test classification
        result = await classifier.classify_device(test_device)
        
        print("Device Classification Result:")
        print(json.dumps(result, indent=2))
        
        # Get statistics
        stats = classifier.get_classification_statistics()
        print("\nClassification Statistics:")
        print(json.dumps(stats, indent=2))
    
    import json
    asyncio.run(test_device_classifier())