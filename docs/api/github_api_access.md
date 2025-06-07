# GitHub API Access Documentation
**Date**: 2025-06-06  
**Purpose**: Access customer repositories for integration analysis

## 🔑 Authentication
```bash
# Using Personal Access Token (Required for private repos)
curl -H "Authorization: Bearer YOUR-TOKEN" \
  https://api.github.com/repos/OWNER/REPO/contents/

# Public repos (no auth needed)
curl -L -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/OWNER/REPO/contents/
```

## 📂 Repository Contents API

### List Directory Contents
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/contents/PATH
```

### Get File Contents (Base64 Encoded)
```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/contents/path/to/file.json
```

### Get Raw File Content (Direct)
```bash
curl -H 'Accept: application/vnd.github.v3.raw' \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  https://api.github.com/repos/OWNER/REPO/contents/path/to/file.json
```

## 🍺 Brewery Repository Examples

### Access dcramb/zymnist-sbbc-scmc Repository
```bash
# List root contents
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR-TOKEN" \
  https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents/

# List ZymLib/node-red-contrib directory
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR-TOKEN" \
  https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents/ZymLib/node-red-contrib

# List ZymBots/lt-controller directory  
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR-TOKEN" \
  https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents/ZymBots/lt-controller

# Get a specific Node-RED flow file
curl -H 'Accept: application/vnd.github.v3.raw' \
  -H "Authorization: Bearer YOUR-TOKEN" \
  https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents/ZymLib/node-red-contrib/flows.json
```

## 🔍 What to Look For

### MQTT Configuration Files
- Node-RED flow exports (*.json)
- MQTT broker configurations
- Topic mapping files
- Equipment definitions

### Expected File Types
- `flows.json` - Node-RED flow export
- `package.json` - Node dependencies
- `*.config.js` - Configuration files
- `README.md` - Documentation
- `mqtt-config.json` - MQTT settings

## 📊 Response Format

### Directory Listing Response
```json
[
  {
    "name": "flows.json",
    "path": "ZymLib/node-red-contrib/flows.json",
    "sha": "abc123...",
    "size": 2048,
    "url": "https://api.github.com/repos/dcramb/zymnist-sbbc-scmc/contents/ZymLib/node-red-contrib/flows.json",
    "html_url": "https://github.com/dcramb/zymnist-sbbc-scmc/blob/main/ZymLib/node-red-contrib/flows.json",
    "download_url": "https://raw.githubusercontent.com/dcramb/zymnist-sbbc-scmc/main/ZymLib/node-red-contrib/flows.json",
    "type": "file"
  }
]
```

### File Content Response
```json
{
  "name": "flows.json",
  "content": "ewogICJpZCI6ICJmbG93MSIsCiAgIm5hbWUi...", 
  "encoding": "base64",
  "size": 2048,
  "type": "file"
}
```

## 🛠️ Integration Scripts

### Python Example
```python
import requests
import base64
import json

def get_github_file(owner, repo, path, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get('encoding') == 'base64':
            content = base64.b64decode(data['content']).decode('utf-8')
            return json.loads(content) if path.endswith('.json') else content
    return None

# Usage
token = "your-github-token"
flows = get_github_file("dcramb", "zymnist-sbbc-scmc", "ZymLib/node-red-contrib/flows.json", token)
```

### Bash Script Example
```bash
#!/bin/bash
TOKEN="your-github-token"
REPO="dcramb/zymnist-sbbc-scmc"

# Function to get directory contents
get_directory() {
    local path=$1
    curl -s -L \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer $TOKEN" \
      "https://api.github.com/repos/$REPO/contents/$path"
}

# Function to get raw file content
get_file() {
    local path=$1
    curl -s -H 'Accept: application/vnd.github.v3.raw' \
      -H "Authorization: Bearer $TOKEN" \
      "https://api.github.com/repos/$REPO/contents/$path"
}

# Get Node-RED flows
get_file "ZymLib/node-red-contrib/flows.json" > brewery_flows.json
```

## 🚨 Important Limitations

- **File Size**: API supports files up to 1MB. For larger files, use raw media type
- **Directory Size**: Max 1,000 files per directory. Use Git Trees API for larger directories  
- **Rate Limits**: 60 requests/hour for unauthenticated, 5,000/hour for authenticated
- **Private Repos**: Require authentication with appropriate permissions

## 🎯 Use Cases for Brewery Integration

1. **MQTT Topic Discovery**: Parse Node-RED flows to extract topic structures
2. **Configuration Analysis**: Review broker settings and connection parameters
3. **Equipment Mapping**: Find equipment definitions and naming conventions
4. **Payload Analysis**: Extract message formats and data structures
5. **Integration Planning**: Understand their current automation setup