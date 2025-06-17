#!/bin/bash
# CT-084 Quick Validation Script
# Fast validation checks for CT-084 Parachute Drop System components
# Author: Claude Agent 1 - Edge Computing Specialist
# Version: 1.0.0

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Validation results
PASSED=0
FAILED=0
TOTAL=0

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        "PASS")  echo -e "${GREEN}[PASS]${NC}  $message" ;;
        "FAIL")  echo -e "${RED}[FAIL]${NC}  $message" ;;
        "WARN")  echo -e "${YELLOW}[WARN]${NC}  $message" ;;
        "INFO")  echo -e "${BLUE}[INFO]${NC}  $message" ;;
    esac
}

# Test function
test_check() {
    local test_name="$1"
    local test_command="$2"
    
    ((TOTAL++))
    
    if eval "$test_command" &>/dev/null; then
        log "PASS" "$test_name"
        ((PASSED++))
        return 0
    else
        log "FAIL" "$test_name"
        ((FAILED++))
        return 1
    fi
}

# Validation functions
validate_file_structure() {
    log "INFO" "Validating CT-084 file structure..."
    
    local files=(
        "$SCRIPT_DIR/ct084-pi-image-builder.sh"
        "$SCRIPT_DIR/ct084-discovery-agent.py"
        "$SCRIPT_DIR/ct084-device-detector.py"
        "$SCRIPT_DIR/ct084-sensor-identifier.py"
        "$SCRIPT_DIR/ct084-system-tester.py"
        "$SCRIPT_DIR/ct084-config.json"
    )
    
    for file in "${files[@]}"; do
        test_check "File exists: $(basename "$file")" "[ -f '$file' ]"
    done
}

validate_script_syntax() {
    log "INFO" "Validating script syntax..."
    
    # Check shell scripts
    test_check "Image builder syntax" "bash -n '$SCRIPT_DIR/ct084-pi-image-builder.sh'"
    test_check "Quick validate syntax" "bash -n '$SCRIPT_DIR/ct084-quick-validate.sh'"
    
    # Check Python scripts (basic syntax)
    local python_scripts=(
        "ct084-discovery-agent.py"
        "ct084-device-detector.py" 
        "ct084-sensor-identifier.py"
        "ct084-system-tester.py"
    )
    
    for script in "${python_scripts[@]}"; do
        test_check "Python syntax: $script" "python3 -m py_compile '$SCRIPT_DIR/$script'"
    done
}

validate_json_config() {
    log "INFO" "Validating JSON configuration..."
    
    test_check "JSON syntax: ct084-config.json" "python3 -m json.tool '$SCRIPT_DIR/ct084-config.json' > /dev/null"
    
    # Check required configuration sections
    local config_file="$SCRIPT_DIR/ct084-config.json"
    
    test_check "Config has device_info" "jq -e '.device_info' '$config_file' > /dev/null"
    test_check "Config has discovery" "jq -e '.discovery' '$config_file' > /dev/null"
    test_check "Config has network" "jq -e '.network' '$config_file' > /dev/null"
    test_check "Config has sensors" "jq -e '.sensors' '$config_file' > /dev/null"
    test_check "Config has monitoring" "jq -e '.monitoring' '$config_file' > /dev/null"
}

validate_dependencies() {
    log "INFO" "Validating system dependencies..."
    
    # System utilities
    local system_deps=(
        "curl"
        "wget"
        "python3"
        "systemctl"
        "jq"
    )
    
    for dep in "${system_deps[@]}"; do
        test_check "Command available: $dep" "command -v $dep"
    done
    
    # Python modules (basic check)
    local python_modules=(
        "json"
        "asyncio"
        "logging"
        "pathlib"
        "datetime"
    )
    
    for module in "${python_modules[@]}"; do
        test_check "Python module: $module" "python3 -c 'import $module'"
    done
}

validate_permissions() {
    log "INFO" "Validating file permissions..."
    
    # Executable scripts
    test_check "Image builder executable" "[ -x '$SCRIPT_DIR/ct084-pi-image-builder.sh' ]"
    test_check "Quick validate executable" "[ -x '$SCRIPT_DIR/ct084-quick-validate.sh' ]"
    
    # Readable Python scripts
    local python_scripts=(
        "ct084-discovery-agent.py"
        "ct084-device-detector.py"
        "ct084-sensor-identifier.py" 
        "ct084-system-tester.py"
    )
    
    for script in "${python_scripts[@]}"; do
        test_check "Readable: $script" "[ -r '$SCRIPT_DIR/$script' ]"
    done
    
    # Config file
    test_check "Config file readable" "[ -r '$SCRIPT_DIR/ct084-config.json' ]"
}

validate_content_quality() {
    log "INFO" "Validating content quality..."
    
    # Check for required functions in image builder
    local image_builder="$SCRIPT_DIR/ct084-pi-image-builder.sh"
    
    test_check "Image builder has main function" "grep -q 'main()' '$image_builder'"
    test_check "Image builder has dependency check" "grep -q 'check_dependencies' '$image_builder'"
    test_check "Image builder has setup function" "grep -q 'setup_build_env' '$image_builder'"
    test_check "Image builder has config function" "grep -q 'configure_pi_system' '$image_builder'"
    
    # Check for required classes in discovery agent
    local discovery_agent="$SCRIPT_DIR/ct084-discovery-agent.py"
    
    test_check "Discovery agent has main class" "grep -q 'class CT084DiscoveryAgent' '$discovery_agent'"
    test_check "Discovery agent has tag builder" "grep -q 'class IntelligentTagBuilder' '$discovery_agent'"
    test_check "Discovery agent has phidget engine" "grep -q 'class PhidgetDiscoveryEngine' '$discovery_agent'"
    
    # Check configuration completeness
    local config_file="$SCRIPT_DIR/ct084-config.json"
    
    test_check "Config has device ID" "jq -e '.device_info.device_id' '$config_file' > /dev/null"
    test_check "Config has version" "jq -e '.device_info.version' '$config_file' > /dev/null"
    test_check "Config has discovery settings" "jq -e '.discovery.enabled' '$config_file' > /dev/null"
}

validate_logging_setup() {
    log "INFO" "Validating logging configuration..."
    
    # Check if log directories would be created
    test_check "Python scripts configure logging" "grep -q 'logging.basicConfig' '$SCRIPT_DIR/ct084-discovery-agent.py'"
    test_check "System tester configures logging" "grep -q 'logging.basicConfig' '$SCRIPT_DIR/ct084-system-tester.py'"
    
    # Check log file paths are consistent
    test_check "Discovery agent log path" "grep -q '/var/log/ct084/' '$SCRIPT_DIR/ct084-discovery-agent.py'"
    test_check "Device detector log path" "grep -q '/var/log/ct084/' '$SCRIPT_DIR/ct084-device-detector.py'"
}

validate_error_handling() {
    log "INFO" "Validating error handling..."
    
    # Check for error handling patterns
    test_check "Image builder has error handling" "grep -q 'error_exit' '$SCRIPT_DIR/ct084-pi-image-builder.sh'"
    test_check "Discovery agent has try-catch" "grep -q 'except Exception' '$SCRIPT_DIR/ct084-discovery-agent.py'"
    test_check "Device detector has error handling" "grep -q 'except Exception' '$SCRIPT_DIR/ct084-device-detector.py'"
    test_check "System tester has error handling" "grep -q 'except Exception' '$SCRIPT_DIR/ct084-system-tester.py'"
}

# Performance validation
validate_performance_considerations() {
    log "INFO" "Validating performance considerations..."
    
    # Check for async patterns
    test_check "Discovery agent uses async" "grep -q 'async def' '$SCRIPT_DIR/ct084-discovery-agent.py'"
    test_check "Device detector uses async" "grep -q 'async def' '$SCRIPT_DIR/ct084-device-detector.py'"
    test_check "System tester uses async" "grep -q 'async def' '$SCRIPT_DIR/ct084-system-tester.py'"
    
    # Check for proper imports
    test_check "Scripts import asyncio" "grep -q 'import asyncio' '$SCRIPT_DIR/ct084-discovery-agent.py'"
}

# Security validation
validate_security_practices() {
    log "INFO" "Validating security practices..."
    
    # Check for secure practices
    test_check "Image builder uses set -euo pipefail" "grep -q 'set -euo pipefail' '$SCRIPT_DIR/ct084-pi-image-builder.sh'"
    test_check "No hardcoded passwords" "! grep -i 'password.*=' '$SCRIPT_DIR/ct084-config.json'"
    test_check "Uses proper file permissions" "grep -q 'chmod' '$SCRIPT_DIR/ct084-pi-image-builder.sh'"
}

# Integration validation
validate_integration_points() {
    log "INFO" "Validating integration points..."
    
    # Check for OPC-UA integration
    test_check "Discovery agent has OPC-UA" "grep -q 'opcua' '$SCRIPT_DIR/ct084-discovery-agent.py'"
    test_check "Config has OPC-UA endpoint" "jq -e '.network.opcua_endpoint' '$SCRIPT_DIR/ct084-config.json' > /dev/null"
    
    # Check for MQTT integration
    test_check "Discovery agent has MQTT" "grep -q 'mqtt' '$SCRIPT_DIR/ct084-discovery-agent.py'"
    test_check "Config has MQTT broker" "jq -e '.network.mqtt_broker' '$SCRIPT_DIR/ct084-config.json' > /dev/null"
    
    # Check for Phidget integration
    test_check "Discovery agent has Phidget support" "grep -q 'Phidget' '$SCRIPT_DIR/ct084-discovery-agent.py'"
    test_check "Device detector has Phidget support" "grep -q 'Phidget' '$SCRIPT_DIR/ct084-device-detector.py'"
}

# Main validation function
main() {
    echo "CT-084 Parachute Drop System - Quick Validation"
    echo "==============================================="
    echo ""
    
    # Run all validation checks
    validate_file_structure
    echo ""
    
    validate_script_syntax
    echo ""
    
    validate_json_config
    echo ""
    
    validate_dependencies
    echo ""
    
    validate_permissions
    echo ""
    
    validate_content_quality
    echo ""
    
    validate_logging_setup
    echo ""
    
    validate_error_handling
    echo ""
    
    validate_performance_considerations
    echo ""
    
    validate_security_practices
    echo ""
    
    validate_integration_points
    echo ""
    
    # Final summary
    echo "Validation Summary"
    echo "=================="
    echo "Total Tests: $TOTAL"
    echo "Passed: $PASSED"
    echo "Failed: $FAILED"
    
    if [ $FAILED -eq 0 ]; then
        log "PASS" "All validation checks passed!"
        echo ""
        echo "✓ CT-084 system is ready for deployment"
        exit 0
    else
        log "FAIL" "$FAILED validation checks failed"
        echo ""
        echo "✗ CT-084 system requires attention before deployment"
        exit 1
    fi
}

# Run main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi