#!/usr/bin/env python3
"""
Help extract Claude Max session information for OAuth setup
"""

import os
import json
import glob
from pathlib import Path

def find_claude_session():
    """Try to find Claude session information"""
    
    print("🔍 Looking for Claude Max session information...")
    print("=" * 50)
    
    # Common locations for Claude session data
    search_paths = [
        "~/.claude*",
        "~/Library/Application Support/Claude*",
        "~/Library/Preferences/Claude*",
        "~/.config/claude*",
        "~/AppData/Local/Claude*",  # Windows
        "~/AppData/Roaming/Claude*"  # Windows
    ]
    
    session_info = {}
    
    # Check environment variables
    print("\n🌍 Checking Environment Variables:")
    claude_env_vars = [var for var in os.environ if 'claude' in var.lower()]
    if claude_env_vars:
        for var in claude_env_vars:
            print(f"   {var}: {os.environ[var][:20]}..." if len(os.environ[var]) > 20 else f"   {var}: {os.environ[var]}")
            session_info[f"env_{var}"] = os.environ[var]
    else:
        print("   No Claude environment variables found")
    
    # Check file system
    print("\n📁 Checking File System:")
    found_files = []
    
    for pattern in search_paths:
        expanded_pattern = os.path.expanduser(pattern)
        matches = glob.glob(expanded_pattern)
        found_files.extend(matches)
    
    if found_files:
        print("   Found Claude-related files:")
        for file_path in found_files[:10]:  # Limit to first 10
            print(f"   📄 {file_path}")
            
            # Try to read JSON files
            if file_path.endswith('.json') and os.path.isfile(file_path):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        if 'session' in str(data).lower() or 'token' in str(data).lower():
                            session_info[f"file_{os.path.basename(file_path)}"] = data
                except:
                    pass
    else:
        print("   No Claude configuration files found")
    
    # Check browser storage locations (Chrome/Safari)
    print("\n🌐 Browser Storage Locations:")
    browser_paths = [
        "~/Library/Application Support/Google/Chrome/Default/Local Storage",
        "~/Library/Application Support/Google/Chrome/Default/Session Storage",
        "~/Library/Safari/LocalStorage",
        "~/AppData/Local/Google/Chrome/User Data/Default/Local Storage"
    ]
    
    for path in browser_paths:
        expanded_path = os.path.expanduser(path)
        if os.path.exists(expanded_path):
            print(f"   ✅ Found: {expanded_path}")
            # Look for Claude-related storage
            try:
                for file in os.listdir(expanded_path):
                    if 'claude' in file.lower():
                        print(f"      🎯 Claude storage: {file}")
            except:
                pass
        else:
            print(f"   ❌ Not found: {expanded_path}")
    
    print("\n" + "=" * 50)
    
    if session_info:
        print("🎉 Found potential session information!")
        print("\n💾 Saving to claude_session_info.json...")
        
        with open('claude_session_info.json', 'w') as f:
            json.dump(session_info, f, indent=2, default=str)
        
        print("✅ Session info saved to claude_session_info.json")
        return True
    else:
        print("❌ No session information found automatically")
        return False

def manual_instructions():
    """Provide manual instructions for getting session key"""
    
    print("\n📋 Manual Method - Browser Developer Tools:")
    print("=" * 50)
    print("1. 🌐 Open Claude.ai in your browser")
    print("2. 🔐 Make sure you're logged into Claude Max")
    print("3. 🛠️  Open Developer Tools (F12 or Cmd+Option+I)")
    print("4. 📱 Go to 'Application' or 'Storage' tab")
    print("5. 🔍 Look under 'Local Storage' for claude.ai")
    print("6. 🎯 Find keys containing 'session', 'token', or 'auth'")
    print("7. 📋 Copy the session token value")
    print()
    print("🔗 Alternative: Check Network tab for API calls to see auth headers")
    print()
    print("💡 The session key typically starts with 'sess-' or similar")

def github_secret_instructions():
    """Instructions for adding to GitHub secrets"""
    
    print("\n🔑 Adding to GitHub Secrets:")
    print("=" * 50)
    print("1. Go to: https://github.com/slimstrongarm/industrial-iot-stack/settings/secrets/actions")
    print("2. Click 'New repository secret'")
    print("3. Name: CLAUDE_MAX_SESSION_KEY")
    print("4. Value: [paste your session token]")
    print("5. Click 'Add secret'")
    print()
    print("🔄 Then update .github/workflows/claude.yml to use:")
    print("   session-key: ${{ secrets.CLAUDE_MAX_SESSION_KEY }}")
    print("   (instead of anthropic-api-key)")

def main():
    """Main function"""
    print("🚀 Claude Max Session Key Finder")
    print("Helping you set up OAuth authentication for GitHub Actions")
    print()
    
    found_session = find_claude_session()
    
    if not found_session:
        manual_instructions()
    
    github_secret_instructions()
    
    print("\n🎯 Goal: Use your Claude Max subscription with GitHub Actions!")
    print("💰 Benefit: No additional API costs!")

if __name__ == "__main__":
    main()