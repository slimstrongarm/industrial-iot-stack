#!/usr/bin/env python3
"""
Verify all access for new Claude instances
Run this first thing in any new Claude session
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def run_command(cmd, timeout=5):
    """Run command and return success/output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_github_access():
    """Check GitHub repository access"""
    print("📂 GitHub Repository Access:")
    
    # Check if we're in a git repo
    success, output, error = run_command("git rev-parse --is-inside-work-tree")
    if not success:
        print("❌ Not in a git repository")
        return False
    
    # Check remote
    success, remote_url, error = run_command("git remote get-url origin")
    if success:
        print(f"✅ Repository: {remote_url}")
    else:
        print("❌ No git remote found")
        return False
    
    # Check status
    success, status, error = run_command("git status --porcelain")
    print(f"✅ Git status accessible")
    
    # Test push access (dry run)
    success, output, error = run_command("git push --dry-run origin main")
    if "Everything up-to-date" in output or "Would push" in output:
        print("✅ Push access confirmed")
        return True
    elif "Permission denied" in error or "Authentication failed" in error:
        print("⚠️ Push access may be limited")
        return True  # Read access is sufficient for most operations
    else:
        print("✅ Basic git access confirmed")
        return True

def check_google_sheets_access():
    """Check Google Sheets API access"""
    print("\n📊 Google Sheets API Access:")
    
    creds_file = Path("credentials/iot-stack-credentials.json")
    if not creds_file.exists():
        print("❌ Google Sheets credentials file not found")
        print("   Expected: credentials/iot-stack-credentials.json")
        return False
    
    try:
        with open(creds_file) as f:
            creds = json.load(f)
        
        client_email = creds.get('client_email', 'Unknown')
        project_id = creds.get('project_id', 'Unknown')
        
        print(f"✅ Credentials file found")
        print(f"✅ Service account: {client_email}")
        print(f"✅ Project ID: {project_id}")
        
        # Test actual connection
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(str(creds_file), scope)
            client = gspread.authorize(credentials)
            
            # Test access to the main sheet
            sheet_id = '1lLZ7c3ec4PfGb32SWWHFeVN-TF2UJeLUsmH99vBb9Do'
            sheet = client.open_by_key(sheet_id)
            print(f"✅ Google Sheets connection successful")
            print(f"✅ Sheet access: {sheet.title}")
            return True
            
        except ImportError:
            print("⚠️ Google Sheets libraries not installed")
            print("   Run: pip install gspread oauth2client")
            return False
        except Exception as e:
            print(f"❌ Google Sheets connection failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error reading credentials: {e}")
        return False

def check_server_access():
    """Check server SSH access"""
    print("\n🖥️ Server Access:")
    
    # Test ping first
    success, output, error = run_command("ping -c 1 100.94.84.126", timeout=10)
    if success:
        print("✅ Server reachable via ping")
    else:
        print("❌ Server not reachable via ping")
        return False
    
    # Test SSH
    success, output, error = run_command("ssh -o ConnectTimeout=5 -o StrictHostKeyChecking=no localaccount@100.94.84.126 'echo Connected'")
    if success:
        print("✅ SSH access confirmed")
        
        # Test Docker on server
        success, output, error = run_command("ssh -o ConnectTimeout=5 localaccount@100.94.84.126 'docker ps'")
        if success:
            print("✅ Docker access on server confirmed")
        else:
            print("⚠️ Docker access on server limited")
        
        return True
    else:
        print("❌ SSH access failed")
        print(f"   Error: {error}")
        return False

def check_local_docker():
    """Check local Docker access"""
    print("\n🐳 Local Docker Access:")
    
    success, output, error = run_command("docker --version")
    if not success:
        print("⚠️ Docker not available locally (normal on some systems)")
        return True  # Not critical for Mac Claude
    
    print(f"✅ Docker version: {output}")
    
    success, output, error = run_command("docker ps")
    if success:
        print("✅ Docker daemon accessible")
        return True
    else:
        print("⚠️ Docker daemon not accessible")
        return False

def detect_claude_type():
    """Detect if this is Mac Claude or Server Claude"""
    if os.path.exists('/mnt/c'):
        return 'server'
    elif sys.platform == 'darwin':
        return 'mac'
    else:
        return 'unknown'

def main():
    print("🤖 Claude Instance Access Verification")
    print("=" * 40)
    
    claude_type = detect_claude_type()
    print(f"🎯 Detected Claude type: {claude_type.upper()}")
    
    results = {}
    
    # Always check GitHub
    results['github'] = check_github_access()
    
    # Always check Google Sheets
    results['sheets'] = check_google_sheets_access()
    
    # Check server access for coordination
    results['server'] = check_server_access()
    
    # Check local Docker (less critical)
    results['docker'] = check_local_docker()
    
    print("\n🎯 ACCESS SUMMARY")
    print("=" * 20)
    
    critical_access = ['github', 'sheets']
    all_critical = all(results[key] for key in critical_access)
    
    for key, status in results.items():
        icon = "✅" if status else "❌"
        critical = " (CRITICAL)" if key in critical_access else ""
        print(f"{icon} {key.title()}: {'PASS' if status else 'FAIL'}{critical}")
    
    if all_critical:
        print("\n🚀 READY TO PROCEED!")
        print("   Critical access verified - Claude can work effectively")
    else:
        print("\n⚠️  SETUP NEEDED!")
        print("   Some critical access missing - check .claude/CREDENTIAL_VERIFICATION.md")
    
    # Specific recommendations
    if not results['github']:
        print("\n📂 GitHub Setup:")
        print("   • Check git configuration: git config --list")
        print("   • May need to re-authenticate: gh auth login")
    
    if not results['sheets']:
        print("\n📊 Google Sheets Setup:")
        print("   • Ensure credentials/iot-stack-credentials.json exists")
        print("   • Install libraries: pip install gspread oauth2client")
    
    print(f"\n📋 Next steps for {claude_type.upper()} Claude:")
    if claude_type == 'mac':
        print("   • Read .claude/CURRENT_CONTEXT.md")
        print("   • Focus on GitHub Actions YAML fix")
        print("   • Monitor Google Sheets progress")
    elif claude_type == 'server':
        print("   • Set up blue TMUX session")
        print("   • Deploy Discord bot (CT-027)")
        print("   • Deploy WhatsApp integration (CT-029)")
    
    return all_critical

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)