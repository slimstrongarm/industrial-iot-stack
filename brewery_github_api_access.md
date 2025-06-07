# Brewery GitHub API Access Documentation
**Date**: 2025-06-06  
**Repository**: dcramb/zymnist-sbbc-scmc  
**Status**: Need to implement proper API access

## API Endpoints for Repository Access

### List Repository Contents
```bash
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents
```

### Get Specific Directory Contents
```bash
# ZymLib/node-red-contrib directory
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents/ZymLib/node-red-contrib

# ZymBots/lt-controller directory  
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents/ZymBots/lt-controller
```

### Get File Contents
```bash
# Get a specific file's content
curl -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents/path/to/file.json
```

## What We Need to Find
1. **Node-RED flow files** (.json) showing MQTT configurations
2. **Configuration files** showing topic structure
3. **Documentation** about their MQTT implementation
4. **Equipment definitions** and naming conventions

## Current Status
- Repository is PUBLIC
- We have accepted invitation
- Need to properly access via API or browser to see actual MQTT topic structure