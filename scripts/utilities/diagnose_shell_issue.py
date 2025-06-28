#!/usr/bin/env python3
"""
Diagnose Claude Code Shell Environment Issue
The error: zsh:source:1: no such file or directory: /var/folders/_b/byfnb129181d7gv9d2l7vjwh0000gn/T/claude-shell-snapshot-40f3
"""

import os
import subprocess
import tempfile
from pathlib import Path

def diagnose_shell_issue():
    print("🔍 Diagnosing Claude Code Shell Environment Issue")
    print("=" * 60)
    
    # Check the problematic path
    problem_path = "/var/folders/_b/byfnb129181d7gv9d2l7vjwh0000gn/T/claude-shell-snapshot-40f3"
    print(f"❌ Problem file: {problem_path}")
    print(f"   Exists: {os.path.exists(problem_path)}")
    
    # Check temp directory structure
    temp_base = "/var/folders/_b/byfnb129181d7gv9d2l7vjwh0000gn/T"
    print(f"\n📁 Temp directory: {temp_base}")
    print(f"   Exists: {os.path.exists(temp_base)}")
    
    if os.path.exists(temp_base):
        try:
            files = os.listdir(temp_base)
            claude_files = [f for f in files if 'claude' in f.lower()]
            print(f"   Total files: {len(files)}")
            print(f"   Claude-related files: {len(claude_files)}")
            if claude_files:
                print("   Claude files found:")
                for f in claude_files[:5]:  # Show first 5
                    print(f"     - {f}")
        except PermissionError:
            print("   Permission denied to list files")
    
    # Check current working directory
    print(f"\n📂 Current working directory: {os.getcwd()}")
    
    # Check environment variables
    print(f"\n🌍 Environment variables:")
    shell_vars = ['SHELL', 'HOME', 'USER', 'TMPDIR', 'PWD']
    for var in shell_vars:
        value = os.environ.get(var, 'Not set')
        print(f"   {var}: {value}")
    
    # Check if we can create temp files normally
    print(f"\n🔧 Temp file creation test:")
    try:
        with tempfile.NamedTemporaryFile(delete=False, prefix='claude-test-') as tmp:
            tmp.write(b"test content")
            tmp_path = tmp.name
        
        print(f"   ✅ Created: {tmp_path}")
        print(f"   ✅ Exists: {os.path.exists(tmp_path)}")
        
        # Clean up
        os.unlink(tmp_path)
        print(f"   ✅ Cleaned up successfully")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test basic shell execution
    print(f"\n⚡ Shell execution test:")
    try:
        result = subprocess.run(['echo', 'Hello from shell'], 
                              capture_output=True, text=True, timeout=5)
        print(f"   ✅ Echo test: {result.stdout.strip()}")
        print(f"   Return code: {result.returncode}")
    except Exception as e:
        print(f"   ❌ Shell test failed: {e}")
    
    # Check if the specific snapshot file pattern exists
    print(f"\n🔍 Looking for similar snapshot files:")
    try:
        import glob
        pattern = "/var/folders/_b/byfnb129181d7gv9d2l7vjwh0000gn/T/claude-shell-snapshot-*"
        matches = glob.glob(pattern)
        print(f"   Found {len(matches)} snapshot files")
        for match in matches[:3]:
            print(f"     - {match}")
    except Exception as e:
        print(f"   ❌ Error searching: {e}")
    
    print(f"\n💡 Recommendations:")
    print("1. This appears to be a Claude Code environment issue")
    print("2. The shell snapshot file doesn't exist or is corrupted")
    print("3. Try restarting Claude Code completely")
    print("4. Check if there are permission issues with temp directory")
    print("5. Consider using file operations instead of bash commands temporarily")
    
    return True

if __name__ == "__main__":
    diagnose_shell_issue()