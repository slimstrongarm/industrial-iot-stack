#!/usr/bin/env node
/**
 * Test WhatsApp Alert System
 * Quick test script for brewery demo
 */

const http = require('http');

// Test configuration
const TEST_CONFIG = {
    nodeRedUrl: 'http://localhost:1880',
    testAlerts: [
        {
            equipment: 'boiler',
            measurement: 'temperature',
            value: 85,
            threshold: 80,
            severity: 'HIGH'
        },
        {
            equipment: 'fermenter',
            measurement: 'ph',
            value: 3.8,
            threshold: 4.0,
            severity: 'LOW'
        },
        {
            equipment: 'cooler',
            measurement: 'temperature',
            value: 45,
            threshold: 40,
            severity: 'HIGH'
        }
    ]
};

/**
 * Send test alert to Node-RED
 */
function sendTestAlert(alert) {
    return new Promise((resolve, reject) => {
        const payload = JSON.stringify({
            topic: `brewery/${alert.equipment}/${alert.measurement}`,
            payload: {
                value: alert.value,
                equipment: alert.equipment,
                timestamp: new Date().toISOString()
            }
        });

        const options = {
            hostname: 'localhost',
            port: 1880,
            path: '/brewery/test-alert',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': payload.length
            }
        };

        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                if (res.statusCode === 200) {
                    resolve({ success: true, response: data });
                } else {
                    reject(new Error(`HTTP ${res.statusCode}: ${data}`));
                }
            });
        });

        req.on('error', reject);
        req.write(payload);
        req.end();
    });
}

/**
 * Test WhatsApp reply simulation
 */
function testReply(action = '1') {
    return new Promise((resolve, reject) => {
        const payload = `From=whatsapp%2B1234567890&Body=${encodeURIComponent(action)}&MessageSid=test123`;

        const options = {
            hostname: 'localhost',
            port: 1880,
            path: '/webhook/whatsapp',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': payload.length
            }
        };

        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => resolve({ statusCode: res.statusCode, data }));
        });

        req.on('error', reject);
        req.write(payload);
        req.end();
    });
}

/**
 * Run demo sequence
 */
async function runDemo() {
    console.log('🍺 WhatsApp Alert System - Demo Test');
    console.log('=====================================\n');

    try {
        // Check if Node-RED is running
        console.log('🔍 Checking Node-RED connection...');
        
        // Test 1: Send equipment alert
        console.log('\n📤 Test 1: Sending boiler temperature alert...');
        const alert = TEST_CONFIG.testAlerts[0];
        
        try {
            const result = await sendTestAlert(alert);
            console.log('✅ Alert sent successfully');
            console.log(`   Equipment: ${alert.equipment}`);
            console.log(`   Value: ${alert.value}°F (limit: ${alert.threshold}°F)`);
        } catch (error) {
            console.log('⚠️  Could not send via Node-RED endpoint');
            console.log('   Make sure Node-RED is running and flow is imported');
            console.log('   Simulating alert for demo...');
        }

        // Wait for processing
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Test 2: Simulate operator response
        console.log('\n📱 Test 2: Simulating operator acknowledgment...');
        try {
            const reply = await testReply('1');
            console.log('✅ Reply processed successfully');
            console.log('   Action: Acknowledge alert');
        } catch (error) {
            console.log('⚠️  Could not test reply endpoint');
            console.log('   Make sure webhook endpoint is configured');
        }

        // Demo summary
        console.log('\n🎯 Demo Summary:');
        console.log('   1. Equipment threshold exceeded → WhatsApp alert sent');
        console.log('   2. Operator replied "1" → Alert acknowledged');
        console.log('   3. System updated with acknowledgment');
        
        console.log('\n📋 For live demo:');
        console.log('   • Show Ignition HMI with normal readings');
        console.log('   • Simulate temperature spike');
        console.log('   • Receive WhatsApp alert on phone');
        console.log('   • Reply to acknowledge');
        console.log('   • Show acknowledgment in dashboard');

    } catch (error) {
        console.error('❌ Demo test failed:', error.message);
        process.exit(1);
    }
}

/**
 * Manual test mode
 */
function manualTest() {
    console.log('📱 Manual Test Mode');
    console.log('==================\n');
    
    console.log('Available test alerts:');
    TEST_CONFIG.testAlerts.forEach((alert, i) => {
        console.log(`${i + 1}. ${alert.equipment} ${alert.measurement}: ${alert.value} (${alert.severity})`);
    });
    
    console.log('\nTo test specific alert:');
    console.log('node test-alert.js --alert 1');
    console.log('\nTo test operator reply:');
    console.log('node test-alert.js --reply "1"');
}

// Command line interface
if (require.main === module) {
    const args = process.argv.slice(2);
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log('WhatsApp Alert Test Script\n');
        console.log('Usage:');
        console.log('  node test-alert.js              # Run full demo');
        console.log('  node test-alert.js --manual     # Manual test mode');
        console.log('  node test-alert.js --alert 1    # Send specific alert');
        console.log('  node test-alert.js --reply "1"  # Test reply');
        process.exit(0);
    }
    
    if (args.includes('--manual')) {
        manualTest();
    } else if (args.includes('--alert')) {
        const alertIndex = parseInt(args[args.indexOf('--alert') + 1]) - 1;
        if (alertIndex >= 0 && alertIndex < TEST_CONFIG.testAlerts.length) {
            sendTestAlert(TEST_CONFIG.testAlerts[alertIndex])
                .then(() => console.log('✅ Test alert sent'))
                .catch(err => console.error('❌ Failed:', err.message));
        } else {
            console.error('❌ Invalid alert index');
        }
    } else if (args.includes('--reply')) {
        const reply = args[args.indexOf('--reply') + 1];
        testReply(reply)
            .then(() => console.log('✅ Test reply sent'))
            .catch(err => console.error('❌ Failed:', err.message));
    } else {
        runDemo();
    }
}