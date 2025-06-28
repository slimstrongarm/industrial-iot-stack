#!/usr/bin/env python3
"""
Screenshot Helper - Global hotkey for screenshots
Requires: pip install pillow pynput pyautogui
"""

import os
import datetime
from pynput import keyboard
import pyautogui
import threading
import time

# Screenshot directory
SCREENSHOT_DIR = "/mnt/c/Users/LocalAccount/industrial-iot-stack/screenshots"

def ensure_screenshot_dir():
    """Create screenshots directory if it doesn't exist"""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def take_screenshot():
    """Take a screenshot and save it"""
    try:
        ensure_screenshot_dir()
        
        # Generate filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(SCREENSHOT_DIR, filename)
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        
        print(f"📸 Screenshot saved: {filepath}")
        print(f"To share with Claude: {filename}")
        
        # Copy path to clipboard (Windows)
        os.system(f'echo {filepath} | clip')
        print("📋 File path copied to clipboard!")
        
        return filepath
    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        return None

def on_hotkey():
    """Hotkey handler"""
    print("🔥 Hotkey triggered! Taking screenshot...")
    take_screenshot()

def main():
    """Main function to set up global hotkey"""
    print("🎯 Screenshot Helper Started")
    print("📸 Hotkey: Ctrl+Shift+S")
    print("📁 Screenshots will be saved to: screenshots/")
    print("Press Ctrl+C to exit")
    
    # Set up global hotkey: Ctrl+Shift+S
    with keyboard.GlobalHotKeys({
        '<ctrl>+<shift>+s': on_hotkey
    }):
        try:
            # Keep the program running
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Screenshot helper stopped")

if __name__ == "__main__":
    main()