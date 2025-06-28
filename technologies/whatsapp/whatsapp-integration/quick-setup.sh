#!/bin/bash
# Quick WhatsApp Integration Setup for Brewery Demo

echo "🍺 Brewery WhatsApp Alert System - Quick Setup"
echo "=============================================="
echo ""

# Check if Node-RED is installed
if ! command -v node-red &> /dev/null; then
    echo "❌ Node-RED not found. Please install Node-RED first."
    exit 1
fi

# Install required Node-RED nodes
echo "📦 Installing Node-RED dependencies..."
cd ~/.node-red || exit
npm install node-red-contrib-twilio

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "📋 Next Steps:"
echo "1. Sign up for Twilio account (free): https://www.twilio.com/try-twilio"
echo "2. Get your Account SID and Auth Token from Twilio Console"
echo "3. Join WhatsApp Sandbox: Send 'join <word>' to Twilio WhatsApp number"
echo "4. Set environment variables:"
echo ""
echo "   export TWILIO_ACCOUNT_SID='your-account-sid'"
echo "   export TWILIO_AUTH_TOKEN='your-auth-token'"
echo "   export TWILIO_WHATSAPP_FROM='whatsapp:+14155238886'"
echo "   export BREWERY_ALERT_TO='whatsapp:+1234567890' # Your WhatsApp number"
echo ""
echo "5. Import brewery-demo-flow.json into Node-RED"
echo "6. Configure webhook URL in Twilio: http://your-server:1880/webhook/whatsapp"
echo ""
echo "🚀 Ready to demo in < 15 minutes!"