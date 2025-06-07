#!/usr/bin/env python3
"""
Quick script to refresh the file tree visualization when needed
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Run the file tree visualization update"""
    
    print("🔄 Refreshing File Tree Visualization...")
    
    script_path = Path(__file__).parent / "create_file_tree_visualization.py"
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ File tree updated successfully!")
            print(result.stdout)
        else:
            print("❌ Update failed:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error updating file tree: {e}")

if __name__ == "__main__":
    main()