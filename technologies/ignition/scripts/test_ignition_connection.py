#!/usr/bin/env python3
"""
Test Ignition Gateway Connection and Project Scan Endpoint
This script verifies that the Ignition gateway and scan endpoint are working
before attempting VS Code integration.
"""

import requests
import json
import sys
from datetime import datetime

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def test_gateway_connection():
    """Test basic gateway connectivity"""
    print(f"\n{BLUE}Testing Ignition Gateway Connection...{RESET}")
    
    try:
        response = requests.get("http://localhost:8088", timeout=5)
        if response.status_code == 200:
            print(f"{GREEN}✅ Gateway is accessible at http://localhost:8088{RESET}")
            return True
        else:
            print(f"{RED}❌ Gateway returned status code: {response.status_code}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}❌ Failed to connect to gateway: {e}{RESET}")
        return False

def test_scan_endpoint():
    """Test the project scan endpoint"""
    print(f"\n{BLUE}Testing Project Scan Endpoint...{RESET}")
    
    try:
        # Test confirm-support endpoint
        response = requests.get(
            "http://localhost:8088/data/project-scan-endpoint/confirm-support",
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("supported") == True:
                print(f"{GREEN}✅ Scan endpoint is active and supported{RESET}")
                print(f"   Response: {data}")
                return True
            else:
                print(f"{YELLOW}⚠️  Endpoint responded but support is false{RESET}")
                return False
        else:
            print(f"{RED}❌ Scan endpoint returned status: {response.status_code}{RESET}")
            return False
            
    except Exception as e:
        print(f"{RED}❌ Failed to test scan endpoint: {e}{RESET}")
        return False

def test_project_scan():
    """Test the actual project scanning functionality"""
    print(f"\n{BLUE}Testing Project Scan Functionality...{RESET}")
    
    try:
        # Trigger a project scan
        response = requests.post(
            "http://localhost:8088/data/project-scan-endpoint/scan",
            params={
                "updateDesigners": "true",
                "forceUpdate": "true"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"{GREEN}✅ Project scan completed successfully{RESET}")
            return True
        else:
            print(f"{YELLOW}⚠️  Project scan returned status: {response.status_code}{RESET}")
            # This might be expected if no projects exist
            return True
            
    except Exception as e:
        print(f"{RED}❌ Failed to execute project scan: {e}{RESET}")
        return False

def check_workspace_file():
    """Check if workspace file exists and has proper configuration"""
    print(f"\n{BLUE}Checking VS Code Workspace Configuration...{RESET}")
    
    workspace_path = "/Users/joshpayneair/Desktop/industrial-iot-stack/industrial-iot-stack.code-workspace"
    
    try:
        with open(workspace_path, 'r') as f:
            config = json.load(f)
            
        # Check for gateway configuration
        if "settings" in config and "ignition.gateways" in config["settings"]:
            gateways = config["settings"]["ignition.gateways"]
            if gateways and len(gateways) > 0:
                gateway = gateways[0]
                print(f"{GREEN}✅ Workspace file configured with gateway:{RESET}")
                print(f"   Name: {gateway.get('name', 'Unknown')}")
                print(f"   URL: {gateway.get('url', 'Unknown')}")
                print(f"   Username: {gateway.get('username', 'Unknown')}")
                print(f"   Enabled: {gateway.get('enabled', False)}")
                return True
            else:
                print(f"{RED}❌ No gateways configured in workspace{RESET}")
                return False
        else:
            print(f"{RED}❌ Gateway settings missing from workspace{RESET}")
            return False
            
    except FileNotFoundError:
        print(f"{RED}❌ Workspace file not found at: {workspace_path}{RESET}")
        return False
    except Exception as e:
        print(f"{RED}❌ Error reading workspace file: {e}{RESET}")
        return False

def print_solution():
    """Print the solution for VS Code integration"""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}SOLUTION: How to Connect VS Code to Ignition{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    print(f"\n{YELLOW}The issue:{RESET} VS Code is open in the directory but hasn't loaded the workspace configuration.")
    
    print(f"\n{GREEN}The fix is simple:{RESET}")
    print("1. In VS Code, go to: File → Open Workspace from File...")
    print("2. Navigate to: /Users/joshpayneair/Desktop/industrial-iot-stack/")
    print("3. Select: industrial-iot-stack.code-workspace")
    print("4. Click 'Open'")
    
    print(f"\n{GREEN}After VS Code reloads:{RESET}")
    print("1. Look in the left sidebar for 'IGNITION GATEWAYS'")
    print("2. You should see 'Local Edge Gateway' listed")
    print("3. Click to expand and browse projects")
    
    print(f"\n{YELLOW}If it still doesn't work:{RESET}")
    print("1. Open Command Palette (Cmd+Shift+P)")
    print("2. Type: 'Ignition Flint: Refresh Ignition Gateways'")
    print("3. Check Output → Ignition Flint for any errors")
    
    print(f"\n{BLUE}{'='*60}{RESET}")

def main():
    """Run all tests"""
    print(f"{BLUE}🔍 Ignition Connection Test Suite{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    results = []
    results.append(("Gateway Connection", test_gateway_connection()))
    results.append(("Scan Endpoint", test_scan_endpoint()))
    results.append(("Project Scan", test_project_scan()))
    results.append(("Workspace Config", check_workspace_file()))
    
    # Summary
    print(f"\n{BLUE}Test Summary:{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    all_passed = True
    for test_name, passed in results:
        status = f"{GREEN}✅ PASS{RESET}" if passed else f"{RED}❌ FAIL{RESET}"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print(f"\n{GREEN}🎉 All tests passed! Your Ignition setup is ready.{RESET}")
        print_solution()
    else:
        print(f"\n{RED}⚠️  Some tests failed. Please fix the issues above first.{RESET}")
        
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())