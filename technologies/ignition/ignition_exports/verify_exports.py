#!/usr/bin/env python3
import os
import json
from pathlib import Path

EXPECTED_PROJECTS = ["test_run_01", "brewery_control", "steel_bonnet_hmi", "equipment_registry", "mqtt_integration", "reporting_dashboards", "alarm_management", "user_management", "data_historian"]
export_dir = Path(__file__).parent

found_exports = []
missing_exports = []

for project in EXPECTED_PROJECTS:
    export_file = export_dir / f"{project}_export.zip"
    if export_file.exists():
        size_mb = export_file.stat().st_size / (1024 * 1024)
        found_exports.append({
            "project": project,
            "file": export_file.name,
            "size_mb": f"{size_mb:.2f}"
        })
    else:
        missing_exports.append(project)

# Create manifest
manifest = {
    "export_date": "2025-06-01T10:11:39.867160",
    "total_expected": len(EXPECTED_PROJECTS),
    "total_found": len(found_exports),
    "found_exports": found_exports,
    "missing_exports": missing_exports,
    "ready_for_docker": len(missing_exports) == 0
}

with open("export_manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)

print(f"✅ Found {len(found_exports)} / {len(EXPECTED_PROJECTS)} exports")
if missing_exports:
    print(f"❌ Missing: {', '.join(missing_exports)}")
else:
    print("🎉 All projects exported successfully!")
print("📋 See export_manifest.json for details")
