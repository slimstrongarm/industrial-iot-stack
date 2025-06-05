# EMQX - Complete Authentication & Authorization Disable Guide

## What You've Done ✅
- Disabled MySQL Authentication

## What to Do Next 🔧

### Step 1: Check Authorization Too
1. In the EMQX Dashboard left menu, look for:
   - **Access Control** → **Authorization**
2. You'll likely see a **MySQL Authorization** provider there too
3. **Disable** or **Delete** the MySQL authorization provider

### Step 2: Look for Anonymous Settings
After disabling MySQL auth/authz, look for:
- A global **"Allow Anonymous"** toggle/checkbox
- Sometimes it's under **Settings** → **MQTT** 
- Or in **Access Control** → **Settings**
- Or as a general setting at the top of the Authentication page

### Step 3: Alternative - Add Simple Authentication
If you can't find "Allow Anonymous", create a simple built-in authentication:

1. **Access Control** → **Authentication**
2. Click **+ Add** or **Create**
3. Choose **Built-in Database**
4. Configure:
   ```
   Backend: Built-in Database
   Mechanism: Password-based
   Password Hash: Plain
   ```
5. **Save/Apply**

### Step 4: Create Test User (if using built-in)
1. **Access Control** → **Users** (or **User Management**)
2. **+ Add User**
3. Create:
   ```
   Username: testuser
   Password: testpass123
   ```
4. **Save**

## What to Look For in the Dashboard

The EMQX dashboard interface might show:
- Authentication providers with **Enable/Disable** toggles
- **Global Settings** with anonymous access options
- **Save** or **Apply** buttons after making changes
- Status indicators showing if auth is working

## Test n8n After Changes

### Option 1: If Anonymous Works
```
Protocol: mqtt://
Host: 172.17.0.4
Port: 1883
Username: (empty)
Password: (empty)
Client ID: n8n-mqtt-client
SSL: OFF
```

### Option 2: If Built-in User Works
```
Protocol: mqtt://
Host: 172.17.0.4
Port: 1883
Username: testuser
Password: testpass123
Client ID: n8n-mqtt-client
SSL: OFF
```

## Verification Steps

1. **Dashboard Check**: Go to **Monitoring** → **Clients**
2. **Try n8n connection test**
3. **Look for the n8n client** to appear in the clients list

---
**Key Point**: Both Authentication AND Authorization need to be fixed since both were pointing to the non-existent MySQL database.