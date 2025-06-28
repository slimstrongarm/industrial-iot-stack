#!/usr/bin/env python3
"""
🧪 Discord Bot Setup & Testing Script
Validates Industrial IoT Claude Bot installation and configuration

Following .claude standards for testing and validation
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

def check_requirements():
    """Check if all required dependencies are installed"""
    print("🔍 Checking Python dependencies...")
    
    required_packages = [
        'discord.py',
        'aiohttp', 
        'gspread',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2'
    ]
    
    missing_packages = []
    
    import_map = {
        'discord.py': 'discord',
        'aiohttp': 'aiohttp', 
        'gspread': 'gspread',
        'google-auth': 'google.auth',
        'google-auth-oauthlib': 'google_auth_oauthlib',
        'google-auth-httplib2': 'google.auth.transport.requests'
    }
    
    for package in required_packages:
        try:
            import_name = import_map.get(package, package.replace('-', '_'))
            __import__(import_name)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_discord_token():
    """Check if Discord bot token is configured"""
    print("\n🔑 Checking Discord bot token...")
    
    token = os.environ.get('DISCORD_BOT_TOKEN')
    if token:
        print(f"  ✅ DISCORD_BOT_TOKEN found (length: {len(token)})")
        return True
    else:
        print("  ❌ DISCORD_BOT_TOKEN not set")
        print("  Set your Discord bot token:")
        print("  export DISCORD_BOT_TOKEN='your_token_here'")
        return False

def check_google_sheets_credentials():
    """Check Google Sheets credentials"""
    print("\n📊 Checking Google Sheets credentials...")
    
    creds_path = '/Users/joshpayneair/Desktop/industrial-iot-stack/credentials/iot-stack-credentials.json'
    
    if os.path.exists(creds_path):
        try:
            with open(creds_path) as f:
                creds = json.load(f)
            
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            if all(field in creds for field in required_fields):
                print(f"  ✅ Google Sheets credentials valid")
                print(f"  📧 Service account: {creds['client_email']}")
                return True
            else:
                print(f"  ❌ Invalid credentials format")
                return False
                
        except json.JSONDecodeError:
            print(f"  ❌ Invalid JSON in credentials file")
            return False
    else:
        print(f"  ❌ Credentials file not found: {creds_path}")
        return False

def check_system_endpoints():
    """Check Industrial IoT system endpoints"""
    print("\n🌐 Checking system endpoints...")
    
    endpoints = [
        ('Node-RED', 'http://localhost:1880'),
        ('n8n', 'http://localhost:5678'),
        ('Ignition', 'http://localhost:8088')
    ]
    
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"  ✅ {name}: {url}")
            else:
                print(f"  ⚠️ {name}: {url} (HTTP {response.status_code})")
        except requests.exceptions.RequestException:
            print(f"  ❌ {name}: {url} (not accessible)")

def check_docker_containers():
    """Check Docker containers for Industrial IoT stack"""
    print("\n🐳 Checking Docker containers...")
    
    try:
        result = subprocess.run(['docker', 'ps', '--format', 'json'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            containers = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    container = json.loads(line)
                    containers.append(container)
            
            if containers:
                print(f"  ✅ Found {len(containers)} running containers:")
                for container in containers:
                    status = "🟢" if "Up" in container.get('Status', '') else "🔴"
                    print(f"    {status} {container.get('Names', 'Unknown')}")
            else:
                print("  ⚠️ No running containers found")
                
        else:
            print("  ❌ Docker not accessible")
            
    except subprocess.TimeoutExpired:
        print("  ❌ Docker command timed out")
    except FileNotFoundError:
        print("  ❌ Docker not installed")

def test_bot_syntax():
    """Test bot script syntax"""
    print("\n🧪 Testing bot script syntax...")
    
    bot_script = '/Users/joshpayneair/Desktop/industrial-iot-stack/discord-bot/industrial_iot_claude_bot.py'
    
    try:
        result = subprocess.run([sys.executable, '-m', 'py_compile', bot_script],
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Bot script syntax is valid")
            return True
        else:
            print("  ❌ Bot script syntax errors:")
            print(f"    {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Failed to test syntax: {e}")
        return False

def run_setup_validation():
    """Run complete setup validation"""
    print("🤖 Industrial IoT Claude Discord Bot - Setup Validation")
    print("=" * 60)
    
    checks = [
        check_requirements(),
        check_discord_token(), 
        check_google_sheets_credentials(),
        test_bot_syntax()
    ]
    
    # System checks (informational)
    check_system_endpoints()
    check_docker_containers()
    
    print("\n📋 VALIDATION SUMMARY")
    print("=" * 60)
    
    if all(checks):
        print("✅ ALL REQUIRED CHECKS PASSED")
        print("\n🚀 Ready to start Discord bot:")
        print("python3 discord-bot/industrial_iot_claude_bot.py")
        print("\n💬 Test in Discord:")
        print("@claude help")
        print("@claude status")
        return True
    else:
        print("❌ SOME CHECKS FAILED")
        print("Fix the issues above before running the bot")
        return False

if __name__ == "__main__":
    success = run_setup_validation()
    sys.exit(0 if success else 1)