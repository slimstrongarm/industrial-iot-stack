# Backup Manifest
**Created**: Sat May 31 10:10:04 PDT 2025
**Purpose**: Full system backup before recovery operations

## Contents
- flows.json - Node-RED flows (original: 615848 bytes)
- flows_cred.json - Node-RED credentials (if exists)
- CLIENT_CONTEXT.md - Customer requirements and context
- SCALABILITY_ANALYSIS.md - Memory fixes and architecture analysis
- BUILD_MANIFEST.md - Build progress tracking
- SESSION_STATE.json - Current session state
- agents/ - All build and test agents

## Recovery Instructions
1. Stop Node-RED: `pkill -f node-red`
2. Restore flows: `cp flows.json /Users/joshpayneair/Desktop/industrial-iot-stack/Steel_Bonnet/node-red-flows/`
3. Start Node-RED: `cd /Users/joshpayneair/Desktop/industrial-iot-stack/Steel_Bonnet/node-red-flows && node-red --max-old-space-size=8192`

## Backup Status
672K total backup size
