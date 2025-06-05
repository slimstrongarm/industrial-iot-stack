# How to Create n8n API Key

## Step-by-Step Instructions

### 1. Access n8n Web Interface
- Open your browser and go to: **http://localhost:5678**
- Login with:
  - Username: **admin**
  - Password: **admin**

### 2. Navigate to Settings
- Once logged in, look for your user menu (usually top-right corner)
- Click on **Settings**

### 3. Find API Settings
- In the Settings menu, look for **API** or **API Settings**
- Click on it to open the API configuration page

### 4. Generate API Key
- Click on **"Create API Key"** or **"Generate New API Key"** button
- Give your API key a descriptive name like "Industrial IoT Integration"
- Click **Create** or **Generate**

### 5. Copy the API Key
- **IMPORTANT**: Copy the API key immediately!
- The key will look something like: `n8n_api_1234567890abcdef...`
- Store it securely - you won't be able to see it again

### 6. Save the API Key
Add the API key to your configuration file:

```bash
# Add to STACK_CONFIG.md or create a .env file
N8N_API_KEY=your_api_key_here
```

### 7. Test the API Key
Test that your API key works:

```bash
# Test with curl
curl -H "X-N8N-API-KEY: your_api_key_here" http://localhost:5678/api/v1/workflows

# Should return a list of workflows (or empty array if none exist)
```

## Using the API Key

### In Python:
```python
import requests

headers = {
    'X-N8N-API-KEY': 'your_api_key_here',
    'Content-Type': 'application/json'
}

# Get all workflows
response = requests.get('http://localhost:5678/api/v1/workflows', headers=headers)
print(response.json())
```

### In Bash:
```bash
# Set API key as environment variable
export N8N_API_KEY="your_api_key_here"

# Use in curl commands
curl -H "X-N8N-API-KEY: $N8N_API_KEY" http://localhost:5678/api/v1/workflows
```

## What to Share with Mac-Claude

Once you have the API key, share these details:
- **API Endpoint**: http://localhost:5678/api/v1
- **API Key**: (the key you generated)
- **Header Name**: X-N8N-API-KEY

## Troubleshooting

If you can't find the API settings:
1. Make sure you're using a recent version of n8n
2. Check under "User Management" or "Personal Settings"
3. The API feature might be under "Developer" settings

If the API key doesn't work:
1. Make sure you copied it correctly (no extra spaces)
2. Check that you're using the correct header name: `X-N8N-API-KEY`
3. Verify n8n is running: `docker ps | grep n8n`