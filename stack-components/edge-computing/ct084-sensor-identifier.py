#!/usr/bin/env python3
"""
CT-084 Intelligent Sensor Identification and Auto-Configuration System
Advanced AI-Powered Sensor Classification and Setup

Author: Claude Agent 1 - Edge Computing Specialist
Version: 1.0.0
Project: CT-084 Parachute Drop System
"""

import json
import time
import asyncio
import logging
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import math

# Scientific computing for signal analysis
import numpy as np
import pandas as pd
from scipy import signal, stats
from scipy.fft import fft, fftfreq

# Phidget libraries for sensor testing
try:
    from Phidget22.Phidget import *
    from Phidget22.Devices.HumiditySensor import *
    from Phidget22.Devices.TemperatureSensor import *
    from Phidget22.Devices.VoltageRatioInput import *
    from Phidget22.Devices.VoltageInput import *
    from Phidget22.Devices.CurrentInput import *
    PHIDGETS_AVAILABLE = True
except ImportError:
    PHIDGETS_AVAILABLE = False
    logging.warning("Phidget22 library not available")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/ct084/sensor-identifier.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('CT084-SensorIdentifier')

class SensorType(Enum):
    """Detailed sensor type classification"""
    TEMPERATURE_THERMOCOUPLE = "temperature_thermocouple"
    TEMPERATURE_RTD = "temperature_rtd"
    TEMPERATURE_THERMISTOR = "temperature_thermistor"
    TEMPERATURE_SEMICONDUCTOR = "temperature_semiconductor"
    HUMIDITY_CAPACITIVE = "humidity_capacitive"
    HUMIDITY_RESISTIVE = "humidity_resistive"
    PRESSURE_ABSOLUTE = "pressure_absolute"
    PRESSURE_GAUGE = "pressure_gauge"
    PRESSURE_DIFFERENTIAL = "pressure_differential"
    FLOW_TURBINE = "flow_turbine"
    FLOW_ULTRASONIC = "flow_ultrasonic"
    FLOW_ELECTROMAGNETIC = "flow_electromagnetic"
    LEVEL_ULTRASONIC = "level_ultrasonic"
    LEVEL_PRESSURE = "level_pressure"
    LEVEL_CAPACITIVE = "level_capacitive"
    VIBRATION_ACCELEROMETER = "vibration_accelerometer"
    VIBRATION_VELOCITY = "vibration_velocity"
    CURRENT_DC = "current_dc"
    CURRENT_AC_RMS = "current_ac_rms"
    VOLTAGE_DC = "voltage_dc"
    VOLTAGE_AC_RMS = "voltage_ac_rms"
    ANALOG_4_20MA = "analog_4_20ma"
    ANALOG_0_10V = "analog_0_10v"
    DIGITAL_DISCRETE = "digital_discrete"
    UNKNOWN = "unknown"

class IndustrialApplication(Enum):
    """Industrial application context"""
    FERMENTATION_TEMPERATURE = "fermentation_temperature"
    FERMENTATION_PRESSURE = "fermentation_pressure"
    AMBIENT_MONITORING = "ambient_monitoring"
    GLYCOL_SYSTEM = "glycol_system"
    UTILITIES_MONITORING = "utilities_monitoring"
    SAFETY_SYSTEMS = "safety_systems"
    PROCESS_CONTROL = "process_control"
    ENERGY_MONITORING = "energy_monitoring"
    ASSET_CONDITION = "asset_condition"
    QUALITY_CONTROL = "quality_control"
    UNKNOWN = "unknown"

@dataclass
class SensorCharacteristics:
    """Sensor electrical and measurement characteristics"""
    measurement_range: Tuple[float, float]
    electrical_range: Tuple[float, float]
    response_time: float  # seconds
    accuracy: float  # percentage
    resolution: float
    linearity: float  # percentage
    update_rate: float  # Hz
    signal_type: str  # voltage, current, digital, frequency
    noise_level: float
    drift_rate: float  # per hour
    temperature_coefficient: float

@dataclass
class SensorSignature:
    """AI-generated sensor signature for identification"""
    signal_statistics: Dict[str, float]
    frequency_characteristics: Dict[str, float]
    response_characteristics: Dict[str, float]
    noise_characteristics: Dict[str, float]
    stability_metrics: Dict[str, float]
    pattern_features: List[str]
    confidence_score: float

@dataclass
class IdentifiedSensor:
    """Fully identified and characterized sensor"""
    sensor_id: str
    sensor_type: SensorType
    application: IndustrialApplication
    characteristics: SensorCharacteristics
    signature: SensorSignature
    configuration: Dict[str, Any]
    calibration_data: Dict[str, Any]
    metadata: Dict[str, Any]
    identification_timestamp: datetime
    confidence: float

class SignalAnalyzer:
    """Advanced signal analysis for sensor identification"""
    
    def __init__(self):
        self.sample_rate = 10.0  # Hz
        self.analysis_duration = 30.0  # seconds
        
    async def analyze_sensor_signal(self, sensor_data: List[float], 
                                  timestamps: List[float]) -> SensorSignature:
        """Analyze sensor signal and generate signature"""
        try:
            # Convert to numpy arrays
            data = np.array(sensor_data)
            times = np.array(timestamps)
            
            # Calculate signal statistics
            signal_stats = self._calculate_signal_statistics(data)
            
            # Frequency domain analysis
            freq_chars = self._analyze_frequency_domain(data, times)
            
            # Response characteristics
            response_chars = self._analyze_response_characteristics(data, times)
            
            # Noise analysis
            noise_chars = self._analyze_noise_characteristics(data)
            
            # Stability metrics
            stability_metrics = self._calculate_stability_metrics(data, times)
            
            # Pattern feature extraction
            pattern_features = self._extract_pattern_features(data)
            
            # Calculate overall confidence
            confidence = self._calculate_confidence_score(
                signal_stats, freq_chars, response_chars, noise_chars
            )
            
            return SensorSignature(
                signal_statistics=signal_stats,
                frequency_characteristics=freq_chars,
                response_characteristics=response_chars,
                noise_characteristics=noise_chars,
                stability_metrics=stability_metrics,
                pattern_features=pattern_features,
                confidence_score=confidence
            )
            
        except Exception as e:
            logger.error(f"Signal analysis failed: {e}")
            return SensorSignature({}, {}, {}, {}, {}, [], 0.0)
    
    def _calculate_signal_statistics(self, data: np.ndarray) -> Dict[str, float]:
        """Calculate comprehensive signal statistics"""
        if len(data) == 0:
            return {}
        
        return {
            "mean": float(np.mean(data)),
            "std": float(np.std(data)),
            "var": float(np.var(data)),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "range": float(np.max(data) - np.min(data)),
            "rms": float(np.sqrt(np.mean(data**2))),
            "skewness": float(stats.skew(data)),
            "kurtosis": float(stats.kurtosis(data)),
            "median": float(np.median(data)),
            "q25": float(np.percentile(data, 25)),
            "q75": float(np.percentile(data, 75)),
            "iqr": float(np.percentile(data, 75) - np.percentile(data, 25))
        }
    
    def _analyze_frequency_domain(self, data: np.ndarray, 
                                times: np.ndarray) -> Dict[str, float]:
        """Analyze frequency domain characteristics"""
        try:
            if len(data) < 10:
                return {}
            
            # Calculate sampling rate
            dt = np.mean(np.diff(times)) if len(times) > 1 else 1.0
            fs = 1.0 / dt if dt > 0 else 1.0
            
            # FFT analysis
            fft_data = fft(data - np.mean(data))
            freqs = fftfreq(len(data), dt)
            
            # Power spectral density
            psd = np.abs(fft_data)**2
            
            # Frequency characteristics
            positive_freqs = freqs[freqs > 0]
            positive_psd = psd[freqs > 0]
            
            if len(positive_psd) == 0:
                return {}
            
            # Find dominant frequency
            dominant_freq_idx = np.argmax(positive_psd)
            dominant_freq = positive_freqs[dominant_freq_idx]
            
            # Calculate spectral centroid
            spectral_centroid = np.sum(positive_freqs * positive_psd) / np.sum(positive_psd)
            
            # Calculate spectral bandwidth
            spectral_bandwidth = np.sqrt(
                np.sum(((positive_freqs - spectral_centroid)**2) * positive_psd) / 
                np.sum(positive_psd)
            )
            
            return {
                "dominant_frequency": float(dominant_freq),
                "spectral_centroid": float(spectral_centroid),
                "spectral_bandwidth": float(spectral_bandwidth),
                "total_power": float(np.sum(psd)),
                "high_freq_power": float(np.sum(psd[freqs > fs/4])),
                "low_freq_power": float(np.sum(psd[freqs < fs/10])),
                "snr_estimate": float(np.max(psd) / np.mean(psd[1:]))
            }
            
        except Exception as e:
            logger.warning(f"Frequency analysis failed: {e}")
            return {}
    
    def _analyze_response_characteristics(self, data: np.ndarray, 
                                        times: np.ndarray) -> Dict[str, float]:
        """Analyze sensor response characteristics"""
        try:
            if len(data) < 5:
                return {}
            
            # Calculate first and second derivatives
            dt = np.mean(np.diff(times)) if len(times) > 1 else 1.0
            first_derivative = np.gradient(data, dt)
            second_derivative = np.gradient(first_derivative, dt)
            
            # Response time estimation (time to reach 63% of step change)
            response_time = self._estimate_response_time(data, times)
            
            # Settling time (time to reach steady state)
            settling_time = self._estimate_settling_time(data, times)
            
            # Overshoot calculation
            overshoot = self._calculate_overshoot(data)
            
            return {
                "response_time": response_time,
                "settling_time": settling_time,
                "overshoot": overshoot,
                "max_rate_of_change": float(np.max(np.abs(first_derivative))),
                "avg_rate_of_change": float(np.mean(np.abs(first_derivative))),
                "acceleration_max": float(np.max(np.abs(second_derivative))),
                "smoothness": float(1.0 / (1.0 + np.std(first_derivative)))
            }
            
        except Exception as e:
            logger.warning(f"Response analysis failed: {e}")
            return {}
    
    def _analyze_noise_characteristics(self, data: np.ndarray) -> Dict[str, float]:
        """Analyze noise characteristics of sensor signal"""
        try:
            if len(data) < 10:
                return {}
            
            # High-pass filter to isolate noise
            filtered_data = signal.detrend(data)
            
            # Noise level estimation
            noise_level = np.std(filtered_data)
            
            # Signal-to-noise ratio
            signal_power = np.var(data - filtered_data)
            noise_power = np.var(filtered_data)
            snr = signal_power / noise_power if noise_power > 0 else float('inf')
            
            # Noise distribution analysis
            noise_skewness = stats.skew(filtered_data)
            noise_kurtosis = stats.kurtosis(filtered_data)
            
            # Autocorrelation for noise pattern
            autocorr = np.correlate(filtered_data, filtered_data, mode='full')
            autocorr = autocorr[autocorr.size // 2:]
            autocorr = autocorr / autocorr[0]  # Normalize
            
            # Find first zero crossing or significant drop
            noise_correlation = 0.0
            for i in range(1, min(len(autocorr), 10)):
                if autocorr[i] < 0.1:
                    noise_correlation = i
                    break
            
            return {
                "noise_level": float(noise_level),
                "snr": float(snr),
                "noise_skewness": float(noise_skewness),
                "noise_kurtosis": float(noise_kurtosis),
                "noise_correlation_length": float(noise_correlation),
                "effective_bits": float(np.log2(snr)) if snr > 1 else 0.0
            }
            
        except Exception as e:
            logger.warning(f"Noise analysis failed: {e}")
            return {}
    
    def _calculate_stability_metrics(self, data: np.ndarray, 
                                   times: np.ndarray) -> Dict[str, float]:
        """Calculate signal stability metrics"""
        try:
            if len(data) < 10:
                return {}
            
            # Drift calculation (linear trend)
            if len(times) == len(data):
                slope, intercept, r_value, p_value, std_err = stats.linregress(times, data)
                drift_rate = slope * 3600  # Convert to per hour
            else:
                drift_rate = 0.0
                r_value = 0.0
            
            # Allan variance (sensor stability measure)
            allan_var = self._calculate_allan_variance(data)
            
            # Range stability
            window_size = max(5, len(data) // 10)
            windowed_ranges = []
            for i in range(0, len(data) - window_size, window_size):
                window_data = data[i:i + window_size]
                windowed_ranges.append(np.max(window_data) - np.min(window_data))
            
            range_stability = np.std(windowed_ranges) / np.mean(windowed_ranges) if windowed_ranges else 0.0
            
            # Temperature coefficient estimation (if temperature data available)
            temp_coefficient = 0.0  # Placeholder for future implementation
            
            return {
                "drift_rate": float(drift_rate),
                "drift_correlation": float(r_value**2),
                "allan_variance": float(allan_var),
                "range_stability": float(range_stability),
                "temperature_coefficient": float(temp_coefficient),
                "long_term_stability": float(1.0 / (1.0 + abs(drift_rate)))
            }
            
        except Exception as e:
            logger.warning(f"Stability analysis failed: {e}")
            return {}
    
    def _extract_pattern_features(self, data: np.ndarray) -> List[str]:
        """Extract characteristic pattern features"""
        features = []
        
        try:
            if len(data) < 5:
                return features
            
            # Monotonic behavior
            if np.all(np.diff(data) >= 0):
                features.append("monotonic_increasing")
            elif np.all(np.diff(data) <= 0):
                features.append("monotonic_decreasing")
            
            # Periodic behavior
            autocorr = np.correlate(data, data, mode='full')
            autocorr = autocorr[autocorr.size // 2:]
            if len(autocorr) > 10:
                peaks, _ = signal.find_peaks(autocorr[1:10], height=0.5*np.max(autocorr))
                if len(peaks) > 0:
                    features.append("periodic")
            
            # Step changes
            diff_data = np.abs(np.diff(data))
            threshold = 3 * np.std(diff_data)
            step_changes = np.sum(diff_data > threshold)
            if step_changes > 0:
                features.append("step_changes")
            
            # Noise characteristics
            if np.std(data) / np.mean(np.abs(data)) > 0.1:
                features.append("noisy")
            else:
                features.append("clean")
            
            # Value range characteristics
            data_range = np.max(data) - np.min(data)
            if data_range < 0.1 * np.mean(np.abs(data)):
                features.append("stable")
            
            # Digital-like behavior
            unique_values = len(np.unique(np.round(data, 1)))
            if unique_values < 10 and len(data) > 20:
                features.append("digital_like")
            
        except Exception as e:
            logger.warning(f"Pattern extraction failed: {e}")
        
        return features
    
    def _estimate_response_time(self, data: np.ndarray, times: np.ndarray) -> float:
        """Estimate sensor response time"""
        try:
            # Look for step changes and measure response
            diff_data = np.abs(np.diff(data))
            if len(diff_data) == 0:
                return 0.0
            
            threshold = 3 * np.std(diff_data)
            step_indices = np.where(diff_data > threshold)[0]
            
            if len(step_indices) == 0:
                return 0.0
            
            # Use first significant step change
            step_idx = step_indices[0]
            if step_idx >= len(data) - 5:
                return 0.0
            
            # Calculate 63% response time
            initial_value = data[step_idx]
            final_value = np.mean(data[step_idx + 5:min(step_idx + 15, len(data))])
            target_value = initial_value + 0.63 * (final_value - initial_value)
            
            # Find when target is reached
            post_step_data = data[step_idx:]
            target_idx = np.argmax(np.abs(post_step_data - target_value) < 0.1 * abs(final_value - initial_value))
            
            if target_idx > 0 and len(times) > step_idx + target_idx:
                dt = times[step_idx + target_idx] - times[step_idx]
                return max(0.0, dt)
            
        except Exception as e:
            logger.debug(f"Response time estimation failed: {e}")
        
        return 0.0
    
    def _estimate_settling_time(self, data: np.ndarray, times: np.ndarray) -> float:
        """Estimate settling time to steady state"""
        # Similar to response time but for 95% settling
        # Implementation similar to _estimate_response_time but with 95% threshold
        return 0.0  # Placeholder
    
    def _calculate_overshoot(self, data: np.ndarray) -> float:
        """Calculate percentage overshoot"""
        # Find step responses and calculate overshoot
        return 0.0  # Placeholder
    
    def _calculate_allan_variance(self, data: np.ndarray) -> float:
        """Calculate Allan variance for stability measurement"""
        try:
            if len(data) < 10:
                return 0.0
            
            # Simple Allan variance calculation
            n = len(data)
            tau_max = n // 4
            
            if tau_max < 2:
                return np.var(data)
            
            allan_vars = []
            for tau in range(1, min(tau_max, 10)):
                if 2 * tau >= n:
                    break
                
                # Calculate Allan variance for this tau
                y_k = []
                for i in range(0, n - 2*tau, tau):
                    avg1 = np.mean(data[i:i+tau])
                    avg2 = np.mean(data[i+tau:i+2*tau])
                    y_k.append(avg2 - avg1)
                
                if len(y_k) > 1:
                    allan_var = np.var(y_k) / 2.0
                    allan_vars.append(allan_var)
            
            return float(np.mean(allan_vars)) if allan_vars else float(np.var(data))
            
        except Exception as e:
            logger.debug(f"Allan variance calculation failed: {e}")
            return float(np.var(data))
    
    def _calculate_confidence_score(self, signal_stats: Dict[str, float],
                                  freq_chars: Dict[str, float],
                                  response_chars: Dict[str, float],
                                  noise_chars: Dict[str, float]) -> float:
        """Calculate overall confidence score for signal analysis"""
        confidence_factors = []
        
        # Signal quality factors
        if signal_stats.get("std", 0) > 0:
            confidence_factors.append(0.8)  # Good signal variation
        
        if noise_chars.get("snr", 0) > 10:
            confidence_factors.append(0.9)  # Good SNR
        elif noise_chars.get("snr", 0) > 3:
            confidence_factors.append(0.7)  # Acceptable SNR
        else:
            confidence_factors.append(0.3)  # Poor SNR
        
        # Data completeness
        total_metrics = len(signal_stats) + len(freq_chars) + len(response_chars) + len(noise_chars)
        if total_metrics > 15:
            confidence_factors.append(0.9)
        elif total_metrics > 10:
            confidence_factors.append(0.7)
        else:
            confidence_factors.append(0.5)
        
        return np.mean(confidence_factors) if confidence_factors else 0.5

class SensorClassifier:
    """AI-powered sensor classification system"""
    
    def __init__(self):
        self.classification_rules = self._load_classification_rules()
        self.application_rules = self._load_application_rules()
    
    def _load_classification_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load sensor classification rules"""
        return {
            "temperature_thermocouple": {
                "signal_range": (-200, 1800),  # Celsius
                "electrical_type": "voltage",
                "typical_noise": "low",
                "response_time": (0.1, 10.0),  # seconds
                "patterns": ["monotonic_response", "temperature_profile"],
                "confidence_threshold": 0.7
            },
            "temperature_rtd": {
                "signal_range": (-200, 850),
                "electrical_type": "resistance",
                "typical_noise": "very_low",
                "response_time": (1.0, 30.0),
                "patterns": ["stable", "clean"],
                "confidence_threshold": 0.8
            },
            "humidity_capacitive": {
                "signal_range": (0, 100),  # %RH
                "electrical_type": "voltage",
                "typical_noise": "low",
                "response_time": (5.0, 60.0),
                "patterns": ["environmental_correlation"],
                "confidence_threshold": 0.7
            },
            "pressure_absolute": {
                "signal_range": (0, 1000),  # kPa
                "electrical_type": "voltage_current",
                "typical_noise": "medium",
                "response_time": (0.01, 1.0),
                "patterns": ["process_pressure"],
                "confidence_threshold": 0.75
            },
            "analog_4_20ma": {
                "signal_range": (4, 20),  # mA
                "electrical_type": "current",
                "typical_noise": "low",
                "response_time": (0.1, 5.0),
                "patterns": ["industrial_analog"],
                "confidence_threshold": 0.8
            },
            "analog_0_10v": {
                "signal_range": (0, 10),  # V
                "electrical_type": "voltage",
                "typical_noise": "medium",
                "response_time": (0.1, 5.0),
                "patterns": ["industrial_analog"],
                "confidence_threshold": 0.8
            }
        }
    
    def _load_application_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load industrial application classification rules"""
        return {
            "fermentation_temperature": {
                "temperature_range": (10, 30),  # Celsius
                "stability_required": "high",
                "update_rate": (0.1, 1.0),  # Hz
                "location_keywords": ["ferment", "tank", "vessel", "fv"],
                "confidence_threshold": 0.8
            },
            "glycol_system": {
                "temperature_range": (-10, 40),
                "stability_required": "medium",
                "update_rate": (0.1, 2.0),
                "location_keywords": ["glycol", "cooling", "chiller"],
                "confidence_threshold": 0.7
            },
            "ambient_monitoring": {
                "sensor_types": ["temperature", "humidity"],
                "stability_required": "medium",
                "update_rate": (0.01, 0.1),
                "location_keywords": ["ambient", "room", "area"],
                "confidence_threshold": 0.6
            },
            "utilities_monitoring": {
                "sensor_types": ["current", "voltage", "power"],
                "stability_required": "medium",
                "update_rate": (1.0, 10.0),
                "location_keywords": ["utility", "power", "electrical"],
                "confidence_threshold": 0.7
            }
        }
    
    def classify_sensor(self, signature: SensorSignature, 
                       device_context: Dict[str, Any]) -> Tuple[SensorType, float]:
        """Classify sensor type based on signature and context"""
        best_match = SensorType.UNKNOWN
        best_confidence = 0.0
        
        # Evaluate each classification rule
        for sensor_type_name, rules in self.classification_rules.items():
            confidence = self._evaluate_classification_rules(signature, rules, device_context)
            
            if confidence > best_confidence and confidence > rules["confidence_threshold"]:
                best_confidence = confidence
                try:
                    best_match = SensorType(sensor_type_name)
                except ValueError:
                    best_match = SensorType.UNKNOWN
        
        return best_match, best_confidence
    
    def classify_application(self, sensor_type: SensorType, signature: SensorSignature,
                           device_context: Dict[str, Any]) -> Tuple[IndustrialApplication, float]:
        """Classify industrial application based on sensor and context"""
        best_match = IndustrialApplication.UNKNOWN
        best_confidence = 0.0
        
        # Evaluate application rules
        for app_name, rules in self.application_rules.items():
            confidence = self._evaluate_application_rules(sensor_type, signature, rules, device_context)
            
            if confidence > best_confidence and confidence > rules["confidence_threshold"]:
                best_confidence = confidence
                try:
                    best_match = IndustrialApplication(app_name)
                except ValueError:
                    best_match = IndustrialApplication.UNKNOWN
        
        return best_match, best_confidence
    
    def _evaluate_classification_rules(self, signature: SensorSignature,
                                     rules: Dict[str, Any],
                                     context: Dict[str, Any]) -> float:
        """Evaluate classification rules and return confidence score"""
        confidence_factors = []
        
        # Signal range check
        if "signal_range" in rules and signature.signal_statistics:
            signal_min = signature.signal_statistics.get("min", 0)
            signal_max = signature.signal_statistics.get("max", 0)
            rule_min, rule_max = rules["signal_range"]
            
            if rule_min <= signal_min <= signal_max <= rule_max:
                confidence_factors.append(0.9)
            elif rule_min <= signal_max <= rule_max or rule_min <= signal_min <= rule_max:
                confidence_factors.append(0.6)
            else:
                confidence_factors.append(0.2)
        
        # Noise characteristics
        if "typical_noise" in rules and signature.noise_characteristics:
            snr = signature.noise_characteristics.get("snr", 1)
            noise_level = rules["typical_noise"]
            
            if noise_level == "very_low" and snr > 100:
                confidence_factors.append(0.9)
            elif noise_level == "low" and snr > 20:
                confidence_factors.append(0.8)
            elif noise_level == "medium" and snr > 5:
                confidence_factors.append(0.7)
            else:
                confidence_factors.append(0.4)
        
        # Response time check
        if "response_time" in rules and signature.response_characteristics:
            response_time = signature.response_characteristics.get("response_time", 0)
            min_time, max_time = rules["response_time"]
            
            if min_time <= response_time <= max_time:
                confidence_factors.append(0.8)
            else:
                confidence_factors.append(0.3)
        
        # Pattern matching
        if "patterns" in rules and signature.pattern_features:
            pattern_matches = 0
            for pattern in rules["patterns"]:
                if any(pattern in feature for feature in signature.pattern_features):
                    pattern_matches += 1
            
            if pattern_matches > 0:
                confidence_factors.append(min(0.9, 0.3 + 0.6 * pattern_matches / len(rules["patterns"])))
            else:
                confidence_factors.append(0.2)
        
        # Use signature confidence as base
        base_confidence = signature.confidence_score
        rule_confidence = np.mean(confidence_factors) if confidence_factors else 0.5
        
        return (base_confidence + rule_confidence) / 2.0
    
    def _evaluate_application_rules(self, sensor_type: SensorType, signature: SensorSignature,
                                  rules: Dict[str, Any], context: Dict[str, Any]) -> float:
        """Evaluate application classification rules"""
        confidence_factors = []
        
        # Sensor type compatibility
        if "sensor_types" in rules:
            type_match = any(st in sensor_type.value for st in rules["sensor_types"])
            confidence_factors.append(0.8 if type_match else 0.2)
        
        # Location keyword matching
        if "location_keywords" in rules:
            location = context.get("location", "").lower()
            name = context.get("name", "").lower()
            combined_text = f"{location} {name}"
            
            keyword_matches = sum(1 for keyword in rules["location_keywords"] 
                                if keyword in combined_text)
            
            if keyword_matches > 0:
                confidence_factors.append(min(0.9, 0.5 + 0.4 * keyword_matches / len(rules["location_keywords"])))
            else:
                confidence_factors.append(0.3)
        
        # Temperature range for temperature sensors
        if "temperature_range" in rules and "temperature" in sensor_type.value:
            if signature.signal_statistics:
                mean_temp = signature.signal_statistics.get("mean", 0)
                min_temp, max_temp = rules["temperature_range"]
                
                if min_temp <= mean_temp <= max_temp:
                    confidence_factors.append(0.9)
                else:
                    confidence_factors.append(0.4)
        
        # Update rate requirements
        if "update_rate" in rules and signature.response_characteristics:
            # This would need actual update rate measurement
            confidence_factors.append(0.6)  # Placeholder
        
        return np.mean(confidence_factors) if confidence_factors else 0.5

class CT084SensorIdentifier:
    """Main CT-084 sensor identification system"""
    
    def __init__(self, config_file: str = "/etc/ct084/ct084-config.json"):
        self.config_file = Path(config_file)
        self.config = {}
        self.load_config()
        
        # Initialize components
        self.signal_analyzer = SignalAnalyzer()
        self.classifier = SensorClassifier()
        
        # Results storage
        self.identified_sensors = {}
    
    def load_config(self):
        """Load configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {"sensor_identification": {"enabled": True}}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            self.config = {"sensor_identification": {"enabled": True}}
    
    async def identify_sensor(self, device_info: Dict[str, Any], 
                            sensor_data: List[float], 
                            timestamps: List[float]) -> Optional[IdentifiedSensor]:
        """Identify and characterize a sensor"""
        try:
            logger.info(f"Identifying sensor: {device_info.get('name', 'Unknown')}")
            
            # Analyze sensor signal
            signature = await self.signal_analyzer.analyze_sensor_signal(sensor_data, timestamps)
            
            # Classify sensor type
            sensor_type, type_confidence = self.classifier.classify_sensor(signature, device_info)
            
            # Classify application
            application, app_confidence = self.classifier.classify_application(
                sensor_type, signature, device_info
            )
            
            # Generate sensor characteristics
            characteristics = self._generate_characteristics(sensor_type, signature)
            
            # Create configuration
            configuration = self._generate_configuration(sensor_type, application, characteristics)
            
            # Generate calibration data
            calibration_data = self._generate_calibration_data(sensor_type, signature)
            
            # Build metadata
            metadata = {
                "identification_method": "ai_signal_analysis",
                "signal_analysis_duration": len(timestamps),
                "type_confidence": type_confidence,
                "application_confidence": app_confidence,
                "device_info": device_info,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            # Calculate overall confidence
            overall_confidence = (signature.confidence_score + type_confidence + app_confidence) / 3.0
            
            # Generate sensor ID
            sensor_id = f"sensor_{device_info.get('device_id', 'unknown')}_{int(time.time())}"
            
            identified_sensor = IdentifiedSensor(
                sensor_id=sensor_id,
                sensor_type=sensor_type,
                application=application,
                characteristics=characteristics,
                signature=signature,
                configuration=configuration,
                calibration_data=calibration_data,
                metadata=metadata,
                identification_timestamp=datetime.now(),
                confidence=overall_confidence
            )
            
            self.identified_sensors[sensor_id] = identified_sensor
            
            logger.info(f"Sensor identified: {sensor_type.value} for {application.value} "
                       f"(confidence: {overall_confidence:.2f})")
            
            return identified_sensor
            
        except Exception as e:
            logger.error(f"Sensor identification failed: {e}")
            return None
    
    def _generate_characteristics(self, sensor_type: SensorType, 
                                signature: SensorSignature) -> SensorCharacteristics:
        """Generate sensor characteristics based on type and signature"""
        # Default characteristics based on sensor type
        defaults = {
            SensorType.TEMPERATURE_THERMOCOUPLE: {
                "measurement_range": (-200.0, 1800.0),
                "electrical_range": (-10.0, 70.0),  # mV
                "response_time": 1.0,
                "accuracy": 0.5,
                "resolution": 0.1,
                "signal_type": "voltage"
            },
            SensorType.HUMIDITY_CAPACITIVE: {
                "measurement_range": (0.0, 100.0),
                "electrical_range": (0.0, 5.0),  # V
                "response_time": 15.0,
                "accuracy": 2.0,
                "resolution": 0.1,
                "signal_type": "voltage"
            },
            SensorType.ANALOG_4_20MA: {
                "measurement_range": (0.0, 100.0),  # Scaled
                "electrical_range": (4.0, 20.0),  # mA
                "response_time": 1.0,
                "accuracy": 0.25,
                "resolution": 0.01,
                "signal_type": "current"
            }
        }
        
        # Get defaults for this sensor type
        default_chars = defaults.get(sensor_type, {
            "measurement_range": (0.0, 100.0),
            "electrical_range": (0.0, 10.0),
            "response_time": 1.0,
            "accuracy": 1.0,
            "resolution": 0.1,
            "signal_type": "voltage"
        })
        
        # Override with signature-based values where available
        if signature.signal_statistics:
            signal_range = (
                signature.signal_statistics.get("min", default_chars["electrical_range"][0]),
                signature.signal_statistics.get("max", default_chars["electrical_range"][1])
            )
        else:
            signal_range = default_chars["electrical_range"]
        
        response_time = signature.response_characteristics.get("response_time", default_chars["response_time"])
        noise_level = signature.noise_characteristics.get("noise_level", 0.1)
        
        return SensorCharacteristics(
            measurement_range=default_chars["measurement_range"],
            electrical_range=signal_range,
            response_time=response_time,
            accuracy=default_chars["accuracy"],
            resolution=default_chars["resolution"],
            linearity=99.0,  # Assume good linearity
            update_rate=1.0,  # Default 1 Hz
            signal_type=default_chars["signal_type"],
            noise_level=noise_level,
            drift_rate=0.0,  # Assume minimal drift
            temperature_coefficient=0.0  # Assume minimal temp coefficient
        )
    
    def _generate_configuration(self, sensor_type: SensorType, 
                              application: IndustrialApplication,
                              characteristics: SensorCharacteristics) -> Dict[str, Any]:
        """Generate optimal sensor configuration"""
        config = {
            "update_rate": 1.0,  # Hz
            "averaging_samples": 1,
            "filtering": {
                "enabled": True,
                "type": "low_pass",
                "cutoff_frequency": 0.1
            },
            "scaling": {
                "enabled": True,
                "input_min": characteristics.electrical_range[0],
                "input_max": characteristics.electrical_range[1],
                "output_min": characteristics.measurement_range[0],
                "output_max": characteristics.measurement_range[1]
            },
            "alarms": {
                "enabled": True,
                "high_limit": characteristics.measurement_range[1] * 0.9,
                "low_limit": characteristics.measurement_range[0] * 1.1,
                "deadband": 2.0
            },
            "units": self._get_units_for_sensor_type(sensor_type),
            "precision": 2
        }
        
        # Application-specific adjustments
        if application == IndustrialApplication.FERMENTATION_TEMPERATURE:
            config["update_rate"] = 0.1  # Slower for fermentation
            config["alarms"]["high_limit"] = 30.0  # °C
            config["alarms"]["low_limit"] = 10.0   # °C
        elif application == IndustrialApplication.UTILITIES_MONITORING:
            config["update_rate"] = 2.0  # Faster for utilities
        
        return config
    
    def _generate_calibration_data(self, sensor_type: SensorType, 
                                 signature: SensorSignature) -> Dict[str, Any]:
        """Generate calibration data for the sensor"""
        return {
            "calibration_date": datetime.now().isoformat(),
            "calibration_method": "auto_identification",
            "offset": 0.0,
            "gain": 1.0,
            "linearity_correction": [],
            "temperature_compensation": {
                "enabled": False,
                "coefficient": 0.0
            },
            "next_calibration_due": (datetime.now() + timedelta(days=365)).isoformat(),
            "calibration_confidence": signature.confidence_score
        }
    
    def _get_units_for_sensor_type(self, sensor_type: SensorType) -> str:
        """Get appropriate units for sensor type"""
        units_map = {
            SensorType.TEMPERATURE_THERMOCOUPLE: "°C",
            SensorType.TEMPERATURE_RTD: "°C",
            SensorType.TEMPERATURE_THERMISTOR: "°C",
            SensorType.TEMPERATURE_SEMICONDUCTOR: "°C",
            SensorType.HUMIDITY_CAPACITIVE: "%RH",
            SensorType.HUMIDITY_RESISTIVE: "%RH",
            SensorType.PRESSURE_ABSOLUTE: "kPa",
            SensorType.PRESSURE_GAUGE: "PSI",
            SensorType.PRESSURE_DIFFERENTIAL: "Pa",
            SensorType.CURRENT_DC: "A",
            SensorType.CURRENT_AC_RMS: "A",
            SensorType.VOLTAGE_DC: "V",
            SensorType.VOLTAGE_AC_RMS: "V",
            SensorType.ANALOG_4_20MA: "mA",
            SensorType.ANALOG_0_10V: "V",
        }
        return units_map.get(sensor_type, "units")
    
    async def save_identification_results(self):
        """Save identification results to file"""
        try:
            results = {
                "identification_timestamp": datetime.now().isoformat(),
                "identifier_version": "1.0.0",
                "total_sensors": len(self.identified_sensors),
                "sensors": {
                    sensor_id: asdict(sensor)
                    for sensor_id, sensor in self.identified_sensors.items()
                }
            }
            
            results_file = Path("/var/log/ct084/sensor-identification-results.json")
            results_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            logger.info(f"Identification results saved to {results_file}")
            
        except Exception as e:
            logger.error(f"Failed to save identification results: {e}")

async def main():
    """Main entry point for sensor identifier"""
    identifier = CT084SensorIdentifier()
    
    # Example usage with test data
    device_info = {
        "device_id": "test_sensor_001",
        "name": "Fermentation Tank 1 Temperature",
        "location": "CT084/Brewery/Fermentation/Tank1"
    }
    
    # Generate test temperature data
    timestamps = [i * 0.1 for i in range(300)]  # 30 seconds at 10 Hz
    sensor_data = [20.0 + 0.1 * np.sin(0.1 * t) + 0.02 * np.random.randn() for t in timestamps]
    
    try:
        identified_sensor = await identifier.identify_sensor(device_info, sensor_data, timestamps)
        
        if identified_sensor:
            print(f"\nSensor Identification Results:")
            print(f"==============================")
            print(f"Sensor ID: {identified_sensor.sensor_id}")
            print(f"Type: {identified_sensor.sensor_type.value}")
            print(f"Application: {identified_sensor.application.value}")
            print(f"Confidence: {identified_sensor.confidence:.2f}")
            print(f"Response Time: {identified_sensor.characteristics.response_time:.2f}s")
            print(f"Measurement Range: {identified_sensor.characteristics.measurement_range}")
            print(f"Units: {identified_sensor.configuration['units']}")
        
        await identifier.save_identification_results()
        
    except Exception as e:
        logger.error(f"Identification failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())