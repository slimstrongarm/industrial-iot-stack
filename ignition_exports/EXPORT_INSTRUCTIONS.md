# Ignition Project Export Instructions

## Projects to Export (9 total):
1. test_run_01
2. brewery_control
3. steel_bonnet_hmi
4. equipment_registry
5. mqtt_integration
6. reporting_dashboards
7. alarm_management
8. user_management
9. data_historian

## Manual Export Steps:

1. **Open Ignition Designer Launcher**
   - URL: http://localhost:8088
   - Username: admin
   - Password: password

2. **For each project above:**
   - Open project in Designer
   - Go to File → Export
   - Save as: `{project_name}_export.zip`
   - Save to: `/Users/joshpayneair/Desktop/industrial-iot-stack/ignition_exports`

3. **After exporting all projects:**
   - Run the verification script: `python3 verify_exports.py`
   - Check export_manifest.json for summary

## Automated Alternative:
If you have curl installed:
```bash
# Run the automated export script
./automated_export.sh
```

Generated: 2025-06-01 10:11:39
