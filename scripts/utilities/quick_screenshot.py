#!/usr/bin/env python3
"""
Quick Screenshot Tool - No hotkeys needed
Just run this script to take a screenshot
"""

import os
import datetime
import subprocess
import sys

def take_quick_screenshot():
    """Take a screenshot using Windows Snipping Tool or Print Screen"""
    
    # Create screenshots directory
    screenshot_dir = "/mnt/c/Users/LocalAccount/industrial-iot-stack/screenshots"
    os.makedirs(screenshot_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    filepath = os.path.join(screenshot_dir, filename)
    
    print("📸 Taking screenshot...")
    print("Options:")
    print("1. Use Windows Snipping Tool (recommended)")
    print("2. Use Print Screen + Paint")
    print("3. Quick capture (if available)")
    
    choice = input("Choose option (1-3) or press Enter for option 1: ").strip()
    
    if choice == "2":
        print("📋 Instructions:")
        print("1. Press Alt+Tab to switch to your desired window")
        print("2. Press Print Screen key")
        print("3. Open Paint (Win+R, type 'mspaint', press Enter)")
        print("4. Press Ctrl+V to paste")
        print(f"5. Save as: {filename}")
        
    elif choice == "3":
        # Try using Windows built-in screenshot
        try:
            subprocess.run(["cmd", "/c", "start", "ms-screenclip:"], check=True)
            print("📱 Windows screenshot tool opened")
        except:
            print("❌ Quick capture not available, using Snipping Tool...")
            subprocess.run(["cmd", "/c", "start", "snippingtool"], check=True)
    else:
        # Default: Snipping Tool
        try:
            subprocess.run(["cmd", "/c", "start", "snippingtool"], check=True)
            print("✂️ Snipping Tool opened")
        except:
            print("❌ Snipping Tool not found")
    
    print(f"💾 Save your screenshot as: {filename}")
    print(f"📁 In directory: {screenshot_dir}")
    print("\nTo share with Claude:")
    print(f"1. Save the screenshot as '{filename}'")
    print("2. Tell Claude the filename")
    print("3. Claude can read the screenshot file")

if __name__ == "__main__":
    take_quick_screenshot()