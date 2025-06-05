# EMQX Client ID Authentication Setup

## Issue Identified ✅
- MySQL authentication is OFF (that's why username/password fails)
- Built-in database user created but not working
- EMQX can authenticate by Client ID instead

## Solution: Client ID Authentication

### Option 1: Enable Built-in Database Authentication
Since you created `n8nuser` / `n8npass123`, we need to:

1. **In EMQX Dashboard** → **Access Control** → **Authentication**
2. **ENABLE** the Built-in Database authentication (toggle it ON)
3. **Make sure MySQL authentication stays OFF**

### Option 2: Client ID Based Authentication
Set up authentication based on Client ID rather than username/password:

1. **In EMQX Dashboard** → **Access Control** → **Authentication**
2. **Edit** the Built-in Database authentication
3. **Change** "User ID Type" from "Username" to "Client ID"
4. **Create Client ID** instead of username:
   - Client ID: `n8n-mqtt-client`
   - Password: `n8npass123`

### Option 3: Anonymous with Client ACL
Enable anonymous access but control via Client ID:

1. **Access Control** → **Authentication** → **Allow Anonymous** = ON
2. **Access Control** → **Authorization** → **Add Client ID rules**

## n8n Configuration

### For Built-in Database (Option 1):
```
Protocol: mqtt://
Host: localhost
Port: 1883
Username: n8nuser
Password: n8npass123
Client ID: n8n-mqtt-client
SSL: OFF
```

### For Client ID Auth (Option 2):
```
Protocol: mqtt://
Host: localhost
Port: 1883
Username: (leave empty)
Password: n8npass123
Client ID: n8n-mqtt-client
SSL: OFF
```

### For Anonymous (Option 3):
```
Protocol: mqtt://
Host: localhost
Port: 1883
Username: (leave empty)
Password: (leave empty)
Client ID: n8n-mqtt-client
SSL: OFF
```

## Recommended Steps

1. **First**: Make sure Built-in Database authentication is **ENABLED** in dashboard
2. **Test**: n8nuser / n8npass123 in n8n
3. **If fails**: Try Client ID authentication approach
4. **If still fails**: Enable anonymous access as fallback

## Check Current Status

In EMQX Dashboard:
- **Access Control** → **Authentication** → Should show "Built-in Database" as ENABLED
- **Access Control** → **Users** → Should show n8nuser listed

The key is making sure the authentication method you created is actually **ACTIVE/ENABLED** in EMQX!