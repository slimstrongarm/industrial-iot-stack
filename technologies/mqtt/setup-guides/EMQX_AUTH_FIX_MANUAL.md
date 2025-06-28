# EMQX Authentication Fix - Manual Method

## Problem Identified ✅
EMQX is configured for MySQL authentication, but MySQL database is not running. This causes all MQTT connections to fail.

## Solution: Enable Anonymous Access via EMQX Dashboard

### Step 1: Access EMQX Dashboard
1. Open browser: http://localhost:18083
2. Login with:
   - Username: `admin`
   - Password: `public`

### Step 2: Disable MySQL Authentication
1. Go to **Access Control** → **Authentication**
2. Find the **MySQL** authentication provider
3. **Disable** or **Delete** the MySQL authentication provider

### Step 3: Enable Anonymous Access
1. In **Access Control** → **Authentication**
2. Look for **Allow Anonymous** setting
3. **Enable** anonymous access
4. Click **Save** or **Apply**

### Step 4: Alternative - Add Built-in Authentication
If you prefer not to use anonymous access:
1. Go to **Access Control** → **Authentication**
2. Click **Add Authentication**
3. Choose **Built-in Database**
4. Configure as follows:
   ```
   Backend: Built-in Database
   Mechanism: Password-based
   Password Hash: Plain
   ```
5. **Save** the configuration

### Step 5: Create MQTT User (if using built-in auth)
1. Go to **Access Control** → **Users**
2. Click **Add User**
3. Create user:
   ```
   Username: mqttuser
   Password: mqttpass
   ```
4. **Save**

## Test n8n Connection

After making changes, try these configurations in n8n:

### Option 1: Anonymous Access
```
Protocol: mqtt://
Host: 172.17.0.4
Port: 1883
Username: (leave empty)
Password: (leave empty)
Client ID: n8n-mqtt-client
SSL: OFF
```

### Option 2: Built-in User
```
Protocol: mqtt://
Host: 172.17.0.4
Port: 1883
Username: mqttuser
Password: mqttpass
Client ID: n8n-mqtt-client
SSL: OFF
```

## Verify Fix via Dashboard

1. In EMQX Dashboard, go to **Monitoring** → **Clients**
2. Try connecting from n8n
3. You should see the n8n client appear in the clients list

## Quick Test from Browser

You can also test MQTT from the EMQX dashboard:
1. Go to **Diagnose** → **WebSocket Client**
2. Connect to: `ws://172.17.0.4:8083/mqtt`
3. Try publishing a test message

---

**The key issue**: EMQX is trying to authenticate against a MySQL database that doesn't exist. Either enable anonymous access or switch to built-in authentication.