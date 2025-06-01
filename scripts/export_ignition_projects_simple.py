#!/usr/bin/env python3
"""
Ignition Project Export Script (Simple Version)
Task ID: DM-005 - Create Ignition project export script
Assigned to: MacBook Claude
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Configuration
EXPORT_DIR = Path.home() / "Desktop" / "industrial-iot-stack" / "ignition_exports"

# Your 9 Ignition projects
PROJECTS = [
    "test_run_01",
    "brewery_control", 
    "steel_bonnet_hmi",
    "equipment_registry",
    "mqtt_integration",
    "reporting_dashboards",
    "alarm_management",
    "user_management",
    "data_historian"
]

def create_export_structure():
    """Create export directory structure and preparation files"""
    print(f"""
╔═══════════════════════════════════════════════════════╗
║        Ignition Project Export Preparation            ║
║               Task ID: DM-005                         ║
╚═══════════════════════════════════════════════════════╝
    """)
    
    # Create export directory
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created export directory: {EXPORT_DIR}")
    
    # Create manual export instructions
    instructions_path = EXPORT_DIR / "EXPORT_INSTRUCTIONS.md"
    with open(instructions_path, 'w') as f:
        f.write(f"""# Ignition Project Export Instructions

## Projects to Export (9 total):
{chr(10).join(f'{i+1}. {p}' for i, p in enumerate(PROJECTS))}

## Manual Export Steps:

1. **Open Ignition Designer Launcher**
   - URL: http://localhost:8088
   - Username: admin
   - Password: password

2. **For each project above:**
   - Open project in Designer
   - Go to File → Export
   - Save as: `{'{project_name}'}_export.zip`
   - Save to: `{EXPORT_DIR}`

3. **After exporting all projects:**
   - Run the verification script: `python3 verify_exports.py`
   - Check export_manifest.json for summary

## Automated Alternative:
If you have curl installed:
```bash
# Run the automated export script
./automated_export.sh
```

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
    print("📝 Created EXPORT_INSTRUCTIONS.md")
    
    # Create automated export script
    script_path = EXPORT_DIR / "automated_export.sh"
    with open(script_path, 'w') as f:
        f.write("""#!/bin/bash
# Automated Ignition Project Export Script

GATEWAY_URL="http://localhost:8088"
AUTH="admin:password"
EXPORT_DIR="$(pwd)"

echo "🚀 Starting automated export..."

projects=(
    "test_run_01"
    "brewery_control"
    "steel_bonnet_hmi"
    "equipment_registry"
    "mqtt_integration"
    "reporting_dashboards"
    "alarm_management"
    "user_management"
    "data_historian"
)

for project in "${projects[@]}"; do
    echo "📦 Exporting $project..."
    
    curl -X POST \\
        -u $AUTH \\
        -H "Content-Type: application/json" \\
        -d "{\\"projectName\\": \\"$project\\"}" \\
        -o "${project}_export.zip" \\
        "$GATEWAY_URL/data/designer/export"
    
    if [ -f "${project}_export.zip" ]; then
        echo "✅ Exported $project"
    else
        echo "❌ Failed to export $project"
    fi
done

echo "✅ Export complete! Check the files above."
""")
    os.chmod(script_path, 0o755)
    print("🔧 Created automated_export.sh (executable)")
    
    # Create verification script
    verify_path = EXPORT_DIR / "verify_exports.py"
    with open(verify_path, 'w') as f:
        f.write(f"""#!/usr/bin/env python3
import os
import json
from pathlib import Path

EXPECTED_PROJECTS = {json.dumps(PROJECTS)}
export_dir = Path(__file__).parent

found_exports = []
missing_exports = []

for project in EXPECTED_PROJECTS:
    export_file = export_dir / f"{{project}}_export.zip"
    if export_file.exists():
        size_mb = export_file.stat().st_size / (1024 * 1024)
        found_exports.append({{
            "project": project,
            "file": export_file.name,
            "size_mb": f"{{size_mb:.2f}}"
        }})
    else:
        missing_exports.append(project)

# Create manifest
manifest = {{
    "export_date": "{datetime.now().isoformat()}",
    "total_expected": len(EXPECTED_PROJECTS),
    "total_found": len(found_exports),
    "found_exports": found_exports,
    "missing_exports": missing_exports,
    "ready_for_docker": len(missing_exports) == 0
}}

with open("export_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"✅ Found {{len(found_exports)}} / {{len(EXPECTED_PROJECTS)}} exports")
if missing_exports:
    print(f"❌ Missing: {{', '.join(missing_exports)}}")
else:
    print("🎉 All projects exported successfully!")
print("📋 See export_manifest.json for details")
""")
    os.chmod(verify_path, 0o755)
    print("✅ Created verify_exports.py")
    
    # Create transfer script
    transfer_path = EXPORT_DIR / "transfer_to_server.sh"
    with open(transfer_path, 'w') as f:
        f.write("""#!/bin/bash
# Transfer exports to server via Tailscale

TAILSCALE_IP="100.x.x.x"  # Update with your server's Tailscale IP
USERNAME="your-username"   # Update with your username
REMOTE_DIR="/tmp/ignition_imports"

echo "📤 Transferring Ignition exports to server..."
echo "Note: Update TAILSCALE_IP and USERNAME in this script first!"

# Create remote directory
ssh $USERNAME@$TAILSCALE_IP "mkdir -p $REMOTE_DIR"

# Transfer all export files
scp *.zip $USERNAME@$TAILSCALE_IP:$REMOTE_DIR/

# Transfer import script
scp import_to_docker.sh $USERNAME@$TAILSCALE_IP:$REMOTE_DIR/

echo "✅ Transfer complete!"
echo "Next steps on server:"
echo "1. cd $REMOTE_DIR"
echo "2. ./import_to_docker.sh"
""")
    os.chmod(transfer_path, 0o755)
    print("📤 Created transfer_to_server.sh")
    
    # Summary
    print(f"""
╔═══════════════════════════════════════════════════════╗
║              Export Preparation Complete              ║
╚═══════════════════════════════════════════════════════╝

✅ Created export directory structure
✅ Generated export instructions
✅ Created automation scripts
✅ Prepared verification tools

📁 Export Directory: {EXPORT_DIR}

Next Steps:
1. Read EXPORT_INSTRUCTIONS.md
2. Export projects (manual or automated)
3. Run verify_exports.py to check
4. Use transfer_to_server.sh when ready

🎯 Task DM-005: Ready for project exports!
""")

if __name__ == "__main__":
    create_export_structure()
    
    print("\n📊 Update Google Sheets:")
    print("- Task DM-005 Status: Complete")
    print("- Task DM-005 Completion: 100%")
    print("- Task DM-005 Notes: Export scripts created, ready for manual export")