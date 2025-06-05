# n8n Initial Setup - Owner Account Creation

## What's Happening
n8n is running for the first time and needs an owner account created. This is normal!

## Recommended Setup Details

### Owner Account Information:
- **Email**: admin@localhost.local (or your actual email)
- **First Name**: Admin
- **Last Name**: User (or IoT Admin)
- **Password**: admin (to match our configuration)

### Alternative Setup:
If you prefer to use real information:
- **Email**: Your actual email address
- **First Name**: Your name
- **Last Name**: Your name
- **Password**: Choose a strong password

## Important Notes

1. **This creates the owner account** - it overrides the basic auth settings we configured
2. **Save these credentials** - you'll need them to login going forward
3. **The email doesn't need to be real** unless you plan to use email features

## After Setup

Once you complete the setup:
1. You'll be logged into n8n
2. You can then go to Settings → API to create an API key
3. The credentials you just created will be your login going forward

## Updating Our Configuration

After setup, update STACK_CONFIG.md with the actual credentials you used:
```
### n8n Workflow Automation
- **Web Interface**: http://localhost:5678
- **Username**: [email you entered]
- **Password**: [password you chose]
```

## Why This Happened

When we started n8n with a fresh PostgreSQL database, it needs initial setup. The N8N_BASIC_AUTH_USER and N8N_BASIC_AUTH_PASSWORD environment variables we set are only used after initial setup or in certain deployment modes.