# Flint VS Code Extension Deep Troubleshooting

## Current Situation (2025-05-31 @ 3:30 PM)
- User has already tried opening the workspace file
- Flint still shows "No Ignition gateways configured"
- Need deeper troubleshooting approach

## What We Know Works ✅
1. **Ignition Gateway**: Running at http://localhost:8088
2. **Scan Endpoint Module**: v1.0.0 installed and verified
3. **Endpoints Active**:
   - GET /data/project-scan-endpoint/confirm-support → {"supported":true}
   - POST /data/project-scan-endpoint/scan → Works
4. **Workspace File**: Contains correct gateway configuration
5. **Flint Extension**: Activated in VS Code

## Deeper Troubleshooting Steps

### 1. Run Diagnostic Test
```bash
cd /Users/joshpayneair/Desktop/industrial-iot-stack
python test_ignition_connection.py
```
This will verify all components are working before debugging VS Code.

### 2. Check Flint Extension Logs
1. Open VS Code Output panel (View → Output)
2. Select "Ignition Flint" from dropdown
3. Look for error messages about:
   - Authentication failures
   - Connection timeouts
   - Invalid gateway configuration
   - Module compatibility issues

### 3. Verify Flint Extension Settings
1. Open VS Code Settings (Cmd+,)
2. Search for "ignition"
3. Check these settings:
   - `ignition.gateway.scanProjects`: Should be true
   - `ignition.gateway.autoRefresh`: Should be true
   - `ignition.gateways`: Should show array with gateway

### 4. Manual Gateway Refresh
1. Open Command Palette (Cmd+Shift+P)
2. Run: "Ignition Flint: Refresh Ignition Gateways"
3. Watch Output panel for errors

### 5. Alternative Connection Methods

#### Method A: Direct Settings Configuration
1. Open VS Code Settings (Cmd+,)
2. Click "Open Settings (JSON)" icon (top right)
3. Add/verify this configuration:
```json
{
  "ignition.gateways": [
    {
      "name": "Local Edge Gateway",
      "url": "http://localhost:8088",
      "username": "admin",
      "password": "password",
      "enabled": true
    }
  ]
}
```

#### Method B: Check Extension Version
1. Go to Extensions sidebar
2. Find "Ignition" by Keith Gamble
3. Check version - might need update or downgrade
4. Try v0.1.6 if on newer version (known stable)

#### Method C: Authentication Test
```bash
# Test with credentials
curl -u admin:password http://localhost:8088/data/project-scan-endpoint/confirm-support
```

### 6. Nuclear Options

#### Option 1: Full Extension Reset
1. Uninstall Flint extension
2. Quit VS Code completely
3. Delete VS Code cache:
   ```bash
   rm -rf ~/Library/Application\ Support/Code/Cache
   rm -rf ~/Library/Application\ Support/Code/CachedData
   ```
4. Reinstall Flint extension
5. Open workspace file

#### Option 2: Direct API Testing
If Flint won't connect, we can still use the API directly:
```python
# Direct project scan via API
import requests

# Trigger scan
response = requests.post(
    "http://localhost:8088/data/project-scan-endpoint/scan",
    params={"updateDesigners": True},
    auth=("admin", "password")
)
print(response.status_code)
```

## Common Issues We've Seen

### Issue 1: Workspace vs Folder
- **Symptom**: Extension doesn't load gateway settings
- **Cause**: VS Code opened as folder, not workspace
- **Fix**: Must use "Open Workspace from File" specifically

### Issue 2: Authentication Mismatch
- **Symptom**: Gateway configured but won't connect
- **Cause**: Credentials in workspace don't match gateway
- **Fix**: Verify admin/password are correct

### Issue 3: Port Conflicts
- **Symptom**: Connection timeouts
- **Cause**: Another service on port 8088
- **Fix**: Check with `lsof -i :8088`

### Issue 4: Module Version Incompatibility
- **Symptom**: Endpoints work but Flint can't use them
- **Cause**: Flint expects different API version
- **Fix**: Check Flint extension logs for version requirements

## Next Actions
1. Run the diagnostic test script
2. Check Flint output logs for specific errors
3. Try manual refresh command
4. Report back with any error messages

## Alternative Approach
If VS Code integration continues to fail, we have these options:
1. Use Ignition Designer directly (already working)
2. Create Python scripts for project management
3. Use the REST API directly for automation
4. Consider alternative VS Code extensions

---
**Remember**: The gateway and module are working correctly. This is specifically a VS Code/Flint configuration issue.