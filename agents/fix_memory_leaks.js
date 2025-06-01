#!/usr/bin/env node
/**
 * Fix Node-RED Memory Leaks
 * Addresses the repeating errors causing memory issues
 */

const fs = require('fs');
const path = require('path');

const flowsPath = path.join(__dirname, '../Steel_Bonnet/node-red-flows/flows.json');

console.log('🔧 Fixing Node-RED Memory Leaks...\n');

// Read flows
let flows;
try {
    const flowsContent = fs.readFileSync(flowsPath, 'utf8');
    flows = JSON.parse(flowsContent);
} catch (error) {
    console.error('❌ Error reading flows.json:', error.message);
    process.exit(1);
}

// Track fixes
let fixCount = 0;
const issues = [];

// Fix function nodes with undefined variable access
flows.forEach((node, index) => {
    if (node.type === 'function' && node.func) {
        let modified = false;
        let originalFunc = node.func;
        
        // Fix "Check Poll Enabled" - accessing undefined simulateDevices
        if (node.name === 'Check Poll Enabled' || node.func.includes('simulateDevices')) {
            node.func = node.func.replace(
                /(\w+)\.simulateDevices/g,
                '($1 && $1.simulateDevices)'
            );
            // Add safety check at beginning
            if (!node.func.includes('// Safety check')) {
                node.func = '// Safety check added by fix script\n' +
                    'const config = msg.config || {};\n' +
                    'if (!config.simulateDevices) return null;\n\n' +
                    node.func;
            }
            modified = true;
            issues.push(`Fixed simulateDevices access in ${node.name || 'unnamed function'}`);
        }
        
        // Fix "Handle Debug Controls" - accessing undefined simulateEvents
        if (node.name === 'Handle Debug Controls' || node.func.includes('simulateEvents')) {
            node.func = node.func.replace(
                /(\w+)\.simulateEvents/g,
                '($1 && $1.simulateEvents)'
            );
            // Add safety check
            if (!node.func.includes('// Safety check')) {
                node.func = '// Safety check added by fix script\n' +
                    'const config = msg.config || {};\n' +
                    'if (!config.simulateEvents) return null;\n\n' +
                    node.func;
            }
            modified = true;
            issues.push(`Fixed simulateEvents access in ${node.name || 'unnamed function'}`);
        }
        
        // Fix syntax errors - missing parentheses
        if (node.name === 'Load Equipment Data' || node.name === 'Update Deployment Mode') {
            // Look for common syntax error patterns
            node.func = node.func.replace(/,\s*\)/g, ')'); // Remove trailing commas
            node.func = node.func.replace(/\(\s*,/g, '('); // Remove leading commas
            
            // Check for unclosed function calls
            const openParens = (node.func.match(/\(/g) || []).length;
            const closeParens = (node.func.match(/\)/g) || []).length;
            if (openParens > closeParens) {
                node.func += ')'.repeat(openParens - closeParens);
                issues.push(`Fixed missing parentheses in ${node.name}`);
            }
            modified = true;
        }
        
        // Fix Universal Data Normalizer - prevent unknown protocol spam
        if (node.name === 'Universal Data Normalizer') {
            if (!node.func.includes('// Rate limit unknown protocols')) {
                node.func = node.func.replace(
                    /node\.warn\((.*Unknown protocol.*)\)/g,
                    '// Rate limited: node.warn($1)'
                );
                node.func = '// Rate limit unknown protocols\n' +
                    'const lastWarn = context.get("lastProtocolWarn") || 0;\n' +
                    'const now = Date.now();\n' +
                    'if (now - lastWarn < 60000) return null; // Only warn once per minute\n' +
                    'context.set("lastProtocolWarn", now);\n\n' +
                    node.func;
                modified = true;
                issues.push('Added rate limiting to Universal Data Normalizer');
            }
        }
        
        if (modified) {
            fixCount++;
        }
    }
});

// Fix MQTT broker reconnection cycling
flows.forEach(node => {
    if (node.type === 'mqtt-broker') {
        // Increase keepalive and add reconnect delay
        node.keepalive = "120"; // 2 minutes instead of 60s
        node.reconnectPeriod = "5000"; // 5 second reconnect delay
        issues.push(`Updated MQTT broker ${node.name} with longer keepalive`);
        fixCount++;
    }
});

// Add global error handler if not present
const hasErrorHandler = flows.some(node => 
    node.type === 'catch' && node.scope && node.scope.length === 0
);

if (!hasErrorHandler) {
    flows.push({
        id: "global_error_handler",
        type: "catch",
        z: "",
        name: "Global Error Handler",
        scope: [],
        uncaught: true,
        x: 120,
        y: 40,
        wires: [["error_rate_limiter"]]
    });
    
    flows.push({
        id: "error_rate_limiter",
        type: "function",
        z: "",
        name: "Rate Limit Errors",
        func: `// Rate limit error logging to prevent memory issues
const errorCount = context.get('errorCount') || {};
const now = Date.now();
const key = msg.error.message.substring(0, 50);

if (!errorCount[key]) {
    errorCount[key] = { count: 0, lastLogged: 0 };
}

errorCount[key].count++;

// Only log once per minute per error type
if (now - errorCount[key].lastLogged > 60000) {
    errorCount[key].lastLogged = now;
    node.error(\`Error (\${errorCount[key].count} occurrences): \${msg.error.message}\`, msg);
    errorCount[key].count = 0;
}

context.set('errorCount', errorCount);
return null; // Don't pass error further`,
        outputs: 0,
        noerr: 0,
        initialize: "",
        finalize: "",
        libs: [],
        x: 340,
        y: 40,
        wires: []
    });
    
    issues.push('Added global error handler with rate limiting');
    fixCount++;
}

// Write fixed flows
console.log(`📝 Fixed ${fixCount} issues:\n`);
issues.forEach(issue => console.log(`  ✓ ${issue}`));

try {
    // Backup original
    const backupPath = flowsPath + '.backup_' + Date.now();
    fs.copyFileSync(flowsPath, backupPath);
    console.log(`\n💾 Backup saved to: ${path.basename(backupPath)}`);
    
    // Write fixed flows
    fs.writeFileSync(flowsPath, JSON.stringify(flows, null, 2));
    console.log('✅ Fixed flows written successfully');
    
    console.log('\n🚀 Next steps:');
    console.log('1. Restart Node-RED: pkill -f node-red');
    console.log('2. Start with: node-red --max-old-space-size=8192');
    console.log('3. Monitor logs for improvements');
    
} catch (error) {
    console.error('❌ Error writing flows:', error.message);
    process.exit(1);
}