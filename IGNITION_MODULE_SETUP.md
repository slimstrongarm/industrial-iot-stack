# Ignition Project Scan Endpoint Module Setup

## Status
- ✅ VS Code Flint configuration created
- ❌ Project scan endpoint module not installed
- ✅ Ignition Gateway running on localhost:8088

## Required Module: ignition-project-scan-endpoint

**Purpose**: Enables VS Code Flint extension to scan and interact with Ignition projects

**Repository**: https://github.com/slimstrongarm/ignition-project-scan-endpoint

## Installation Steps

### Option 1: Download Pre-built Module
If available, download the `.modl` file directly from the releases page.

### Option 2: Build from Source
```bash
# Clone the repository
git clone https://github.com/slimstrongarm/ignition-project-scan-endpoint.git
cd ignition-project-scan-endpoint

# Build with Gradle
./gradlew build

# The .modl file will be in build/libs/
```

### Option 3: Install via Ignition Gateway (Manual)
1. Open http://localhost:8088
2. Go to Configure → Modules
3. Install new module → Upload .modl file
4. Restart gateway if prompted

## Alternative: VS Code Direct Connection

If the module isn't available, Flint extension might work with:
- Direct OPC-UA connection
- Web interface scraping
- Alternative project scanning methods

## Current VS Code Configuration

Created `.vscode/settings.json` with:
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

## Next Steps
1. Try restarting VS Code to pick up new configuration
2. Check if Flint extension detects the gateway
3. Install scan endpoint module if needed for full functionality
4. Test project visibility in VS Code

## Testing
- Gateway accessible: ✅ http://localhost:8088 (redirects to /Start)
- Module endpoint: ❌ http://localhost:8088/data/project-scan-endpoint/confirm-support (404)
- VS Code config: ✅ Created
