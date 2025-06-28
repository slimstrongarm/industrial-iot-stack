/**
 * Quick script to add Claude Tasks tab to existing Google Sheet
 * 
 * Instructions:
 * 1. Open your IoT Stack Progress Master Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Create a new script file and paste this entire content
 * 4. Save and run addClaudeTasksTab()
 */

/**
 * Add the Claude Tasks tab with initial Server Claude tasks
 */
function addClaudeTasksTab() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Create or get the Claude Tasks sheet
  let sheet = ss.getSheetByName('Claude Tasks');
  if (!sheet) {
    sheet = ss.insertSheet('Claude Tasks');
  }
  
  // Clear and setup the sheet
  sheet.clear();
  
  const headers = [
    'Task ID', 'Instance', 'Task Type', 'Priority', 'Status', 
    'Description', 'Expected Output', 'Dependencies', 'Date Added', 'Completed'
  ];
  
  // Set headers
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  
  // Format headers
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#1a73e8');
  headerRange.setFontColor('#ffffff');
  headerRange.setFontWeight('bold');
  headerRange.setHorizontalAlignment('center');
  
  // Add initial Server Claude tasks
  const initialTasks = [
    ['CT-001', 'Server Claude', 'Docker Setup', 'High', 'Pending', 'Run server audit to check existing Docker services', 'List of running containers and services', '-', new Date(), ''],
    ['CT-002', 'Server Claude', 'MQTT Config', 'High', 'Pending', 'Configure EMQX broker (not Mosquitto) on server', 'EMQX running on port 1883 with dashboard on 18083', 'CT-001', new Date(), ''],
    ['CT-003', 'Server Claude', 'Docker Compose', 'High', 'Pending', 'Create comprehensive docker-compose.yml for Ignition + supporting services', 'Working multi-container setup', 'CT-001', new Date(), ''],
    ['CT-004', 'Server Claude', 'Integration Test', 'Medium', 'Pending', 'Test MQTT connection between Mac Mosquitto and Server EMQX', 'Confirmed bidirectional MQTT communication', 'CT-002', new Date(), ''],
    ['CT-005', 'Mac Claude', 'Documentation', 'Medium', 'Pending', 'Update architecture docs with Server Claude findings', 'Updated MQTT_BROKER_ARCHITECTURE.md', 'CT-002', new Date(), '']
  ];
  
  sheet.getRange(2, 1, initialTasks.length, headers.length).setValues(initialTasks);
  
  // Format Date Added column
  sheet.getRange('I:I').setNumberFormat('yyyy-mm-dd hh:mm');
  
  // Format Completed column  
  sheet.getRange('J:J').setNumberFormat('yyyy-mm-dd hh:mm');
  
  // Set column widths
  sheet.setColumnWidth(1, 80);   // Task ID
  sheet.setColumnWidth(2, 120);  // Instance
  sheet.setColumnWidth(3, 120);  // Task Type
  sheet.setColumnWidth(4, 80);   // Priority
  sheet.setColumnWidth(5, 100);  // Status
  sheet.setColumnWidth(6, 350);  // Description
  sheet.setColumnWidth(7, 200);  // Expected Output
  sheet.setColumnWidth(8, 120);  // Dependencies
  sheet.setColumnWidth(9, 120);  // Date Added
  sheet.setColumnWidth(10, 120); // Completed
  
  // Add dropdowns for Instance
  const instanceValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Mac Claude', 'Server Claude', 'Both'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('B2:B1000').setDataValidation(instanceValidation);
  
  // Add dropdowns for Status
  const statusValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Pending', 'In Progress', 'Complete', 'Blocked'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('E2:E1000').setDataValidation(statusValidation);
  
  // Add conditional formatting for status
  const pendingRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Pending')
    .setBackground('#fce4ec')
    .setRanges([sheet.getRange('E2:E1000')])
    .build();
  
  const inProgressRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('In Progress')
    .setBackground('#fff3cd')
    .setRanges([sheet.getRange('E2:E1000')])
    .build();
  
  const completeRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Complete')
    .setBackground('#d4edda')
    .setRanges([sheet.getRange('E2:E1000')])
    .build();
  
  const blockedRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('Blocked')
    .setBackground('#f8d7da')
    .setRanges([sheet.getRange('E2:E1000')])
    .build();
  
  sheet.setConditionalFormatRules([pendingRule, inProgressRule, completeRule, blockedRule]);
  
  // Freeze header row
  sheet.setFrozenRows(1);
  
  SpreadsheetApp.getActiveSpreadsheet().toast('Claude Tasks tab added successfully!', 'Success', 5);
}