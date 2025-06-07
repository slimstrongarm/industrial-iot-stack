# EMQX Dashboard Access - Credentials Reset

## ✅ Dashboard Credentials (Updated)

**EMQX Dashboard URL**: http://localhost:18083

**Login Credentials**:
- **Username**: `admin`
- **Password**: `adminpass123`

## How to Fix MQTT Authentication

Now that you can access the dashboard, follow these steps:

### Step 1: Login to EMQX Dashboard
1. Go to: http://localhost:18083
2. Username: `admin`
3. Password: `adminpass123`

### Step 2: Fix Authentication
1. Click **Access Control** in the left menu
2. Click **Authentication**
3. You'll see a **MySQL** authentication provider that's failing
4. Either:
   - **Option A**: Click the toggle to **Disable** the MySQL provider
   - **Option B**: Click the **Delete** button to remove it

### Step 3: Enable Anonymous Access
1. Look for **"Allow Anonymous"** setting
2. **Enable** it by clicking the toggle
3. Click **Save** or **Update**

### Step 4: Test n8n Connection
Go back to n8n and try these credentials:

```
Protocol: mqtt://
Host: 172.17.0.4
Port: 1883
Username: (leave empty)
Password: (leave empty)
Client ID: n8n-mqtt-client
SSL: OFF
```

## Alternative: Create Built-in User

If you don't want anonymous access:

1. In **Access Control** → **Authentication**
2. Click **+ Add**
3. Choose **Built-in Database**
4. Create it with these settings:
   - Backend: Built-in Database
   - Mechanism: Password-based
5. **Save**

6. Go to **Access Control** → **Users**
7. Click **+ Add User**
8. Create:
   - Username: `n8nuser`
   - Password: `n8npass123`
9. **Save**

Then use these credentials in n8n:
```
Username: n8nuser
Password: n8npass123
```

## Verification

After making changes, you should see in the EMQX dashboard:
- **Monitoring** → **Clients**: n8n connections will appear here
- **Access Control** → **Authentication**: Shows your working authentication method

---
**The authentication issue should now be resolved!**