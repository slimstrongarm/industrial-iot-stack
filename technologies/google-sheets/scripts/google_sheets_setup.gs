/**
 * Google Apps Script for Industrial IoT Stack Progress Tracker
 * Copy this entire script into Google Sheets: Extensions > Apps Script
 * 
 * Setup Instructions:
 * 1. Create a new Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Delete any existing code
 * 4. Paste this entire script
 * 5. Save and run setupProgressTracker()
 * 6. Grant necessary permissions when prompted
 */

// Configuration
const CONFIG = {
  sheetName: 'IoT Stack Progress Master',
  tabs: [
    'Docker Migration Tasks',
    'System Components Status', 
    'Project Migration Tracker',
    'Agent Activities',
    'Integration Checklist',
    'Claude Approvals',
    'Human Tasks',
    'Claude Tasks',
    'Dashboard'
  ],
  colors: {
    header: '#1a73e8',
    pending: '#fce4ec',
    inProgress: '#fff3cd',
    complete: '#d4edda',
    error: '#f8d7da'
  }
};

/**
 * Quick function to add just the Claude Tasks tab - run this if you already have the sheet set up
 */
function addClaudeTasksTab() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  
  // Create the tab if it doesn't exist
  createOrGetSheet(ss, 'Claude Tasks');
  
  // Setup the Claude Tasks tab
  setupClaudeTasks(ss);
  
  SpreadsheetApp.getActiveSpreadsheet().toast('Claude Tasks tab added successfully!', 'Success', 5);
}

/**
 * Main setup function - run this first
 */
function setupProgressTracker() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.rename(CONFIG.sheetName);
  
  // Create all tabs
  CONFIG.tabs.forEach((tabName, index) => {
    createOrGetSheet(ss, tabName);
  });
  
  // Setup each tab with proper structure
  setupDockerMigrationTasks(ss);
  setupSystemComponentsStatus(ss);
  setupProjectMigrationTracker(ss);
  setupAgentActivities(ss);
  setupIntegrationChecklist(ss);
  setupClaudeApprovals(ss);
  setupHumanTasks(ss);
  setupClaudeTasks(ss);
  setupDashboard(ss);
  
  // Setup triggers
  setupAutomationTriggers();
  
  // Create custom menu
  createCustomMenu();
  
  SpreadsheetApp.getActiveSpreadsheet().toast('Setup complete! Your IoT Stack Progress Tracker is ready.', 'Success', 10);
}

/**
 * Create or get existing sheet
 */
function createOrGetSheet(ss, sheetName) {
  let sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    sheet = ss.insertSheet(sheetName);
  }
  return sheet;
}

/**
 * Setup Docker Migration Tasks tab
 */
function setupDockerMigrationTasks(ss) {
  const sheet = ss.getSheetByName('Docker Migration Tasks');
  sheet.clear();
  
  const headers = [
    'Task ID', 'Task Description', 'Status', 'Priority', 
    'Assigned To', 'Start Date', 'Due Date', 'Completion %', 
    'Notes', 'Dependencies'
  ];
  
  // Set headers
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  // Add sample data
  const sampleData = [
    ['DM-001', 'Create Docker Compose for Ignition', 'In Progress', 'High', 'Server Claude', '2025-06-01', '2025-06-03', '25%', 'Base config done', '-'],
    ['DM-002', 'Research Flint Docker integration', 'Pending', 'High', 'MacBook Claude', '-', '2025-06-02', '0%', '-', 'DM-001'],
    ['DM-003', 'Design modular stack architecture', 'Pending', 'High', 'MacBook Claude', '-', '2025-06-04', '0%', '-', '-']
  ];
  
  sheet.getRange(2, 1, sampleData.length, headers.length).setValues(sampleData);
  
  // Apply conditional formatting
  applyStatusFormatting(sheet, 3);
  
  // Set column widths
  sheet.setColumnWidth(2, 300); // Task Description
  sheet.setColumnWidth(9, 200); // Notes
}

/**
 * Setup System Components Status tab
 */
function setupSystemComponentsStatus(ss) {
  const sheet = ss.getSheetByName('System Components Status');
  sheet.clear();
  
  const headers = [
    'Component', 'Docker Status', 'Health Check', 'Version', 
    'Last Updated', 'Uptime', 'CPU Usage', 'Memory Usage', 'Alerts'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  // Add component rows
  const components = [
    ['Ignition Gateway', 'Running', '✅ Healthy', '8.1.43', '=NOW()', '-', '-', '-', 'None'],
    ['Node-RED', 'Running', '✅ Healthy', '3.1.9', '=NOW()', '-', '-', '-', 'None'],
    ['MQTT Broker', 'Running', '✅ Healthy', '2.0.18', '=NOW()', '-', '-', '-', 'None'],
    ['Portainer', 'Not Deployed', '⚠️ Pending', '-', '=NOW()', '-', '-', '-', 'Pending Setup'],
    ['Grafana', 'Not Deployed', '⚠️ Pending', '-', '=NOW()', '-', '-', '-', 'Pending Setup']
  ];
  
  sheet.getRange(2, 1, components.length, headers.length).setValues(components);
  
  // Format timestamp columns
  sheet.getRange(2, 5, components.length, 1).setNumberFormat('yyyy-mm-dd hh:mm');
}

/**
 * Setup Project Migration Tracker tab
 */
function setupProjectMigrationTracker(ss) {
  const sheet = ss.getSheetByName('Project Migration Tracker');
  sheet.clear();
  
  const headers = [
    'Project Name', 'Local Status', 'Export Status', 'Transfer Status', 
    'Import Status', 'Validation', 'VS Code Access', 'Notes'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  // Add project placeholders
  const projects = [
    ['test_run_01', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'Main test project'],
    ['brewery_control', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'Production templates'],
    ['steel_bonnet_hmi', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'HMI screens'],
    ['equipment_registry', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'Equipment management'],
    ['mqtt_integration', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'MQTT configurations'],
    ['reporting_dashboards', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'Reporting screens'],
    ['alarm_management', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'Alarm configurations'],
    ['user_management', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'User/role configs'],
    ['data_historian', '✅ Ready', '⏳ Pending', '-', '-', '-', '-', 'Historical data setup']
  ];
  
  sheet.getRange(2, 1, projects.length, headers.length).setValues(projects);
}

/**
 * Setup Agent Activities tab
 */
function setupAgentActivities(ss) {
  const sheet = ss.getSheetByName('Agent Activities');
  sheet.clear();
  
  const headers = [
    'Timestamp', 'Agent Type', 'Task', 'Status', 
    'Duration', 'Output', 'Next Action'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  // Format timestamp column
  sheet.getRange('A:A').setNumberFormat('yyyy-mm-dd hh:mm:ss');
  
  // Set column widths
  sheet.setColumnWidth(3, 300); // Task
  sheet.setColumnWidth(6, 300); // Output
  sheet.setColumnWidth(7, 200); // Next Action
}

/**
 * Setup Integration Checklist tab
 */
function setupIntegrationChecklist(ss) {
  const sheet = ss.getSheetByName('Integration Checklist');
  sheet.clear();
  
  const headers = [
    'Integration Point', 'Status', 'Test Result', 
    'Documentation', 'Production Ready'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  const integrations = [
    ['Ignition ↔ Flint', '🔄 In Progress', '-', '✅ Complete', '❌ No'],
    ['Node-RED ↔ MQTT', '✅ Complete', '✅ Pass', '✅ Complete', '✅ Yes'],
    ['MQTT ↔ Ignition', '🔄 In Progress', '⚠️ Partial', '📝 In Progress', '❌ No'],
    ['Ignition ↔ Database', '📋 Planned', '-', '📝 In Progress', '❌ No'],
    ['VS Code ↔ Ignition', '🔄 In Progress', '-', '✅ Complete', '❌ No'],
    ['Docker ↔ Tailscale', '📋 Planned', '-', '📝 In Progress', '❌ No']
  ];
  
  sheet.getRange(2, 1, integrations.length, headers.length).setValues(integrations);
}

/**
 * Setup Claude Approvals tab with conversational responses
 */
function setupClaudeApprovals(ss) {
  const sheet = ss.getSheetByName('Claude Approvals');
  sheet.clear();
  
  const headers = [
    'Request ID', 'Type', 'Description', 'Status', 
    'Your Response', 'Requested At', 'Responded At'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  // Enhanced conversational responses
  const responseValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList([
      '✅ Yes, proceed',
      '🤝 Yes, but let\'s discuss details',
      '⏸️ Hold on, need more info',
      '📅 Not now, maybe later',
      '🔄 Let\'s try a different approach',
      '❌ No, not a good idea',
      '💬 Need to chat about this',
      '🚀 Fast track this!',
      '⚠️ Proceed with caution'
    ], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('E2:E').setDataValidation(responseValidation);
  
  // Status validation
  const statusValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['PENDING', 'APPROVED', 'DISCUSS', 'POSTPONED', 'REJECTED'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('D2:D').setDataValidation(statusValidation);
  
  // Format timestamp columns
  sheet.getRange('F:F').setNumberFormat('yyyy-mm-dd hh:mm');
  sheet.getRange('G:G').setNumberFormat('yyyy-mm-dd hh:mm');
  
  // Set column widths
  sheet.setColumnWidth(1, 120);  // Request ID
  sheet.setColumnWidth(2, 150);  // Type
  sheet.setColumnWidth(3, 350);  // Description
  sheet.setColumnWidth(4, 100);  // Status
  sheet.setColumnWidth(5, 200);  // Your Response
  sheet.setColumnWidth(6, 150);  // Requested At
  sheet.setColumnWidth(7, 150);  // Responded At
  
  sheet.setFrozenRows(1);
}

/**
 * Setup Human Tasks tab
 */
function setupHumanTasks(ss) {
  const sheet = ss.getSheetByName('Human Tasks');
  sheet.clear();
  
  const headers = [
    'Role', 'Task Type', 'Priority', 'Status', 
    'Assigned To', 'Dependencies', 'Notes', 'Date Added'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  // Format Date Added column
  sheet.getRange('H:H').setNumberFormat('yyyy-mm-dd hh:mm');
  
  // Set column widths
  sheet.setColumnWidth(1, 120);  // Role
  sheet.setColumnWidth(2, 150);  // Task Type
  sheet.setColumnWidth(3, 80);   // Priority
  sheet.setColumnWidth(4, 100);  // Status
  sheet.setColumnWidth(5, 150);  // Assigned To
  sheet.setColumnWidth(6, 200);  // Dependencies
  sheet.setColumnWidth(7, 300);  // Notes
  sheet.setColumnWidth(8, 120);  // Date Added
  
  sheet.setFrozenRows(1);
}

/**
 * Setup Claude Tasks tab - for automated tasks assigned to Mac Claude and Server Claude
 */
function setupClaudeTasks(ss) {
  const sheet = ss.getSheetByName('Claude Tasks');
  sheet.clear();
  
  const headers = [
    'Task ID', 'Instance', 'Task Type', 'Priority', 'Status', 
    'Description', 'Expected Output', 'Dependencies', 'Date Added', 'Completed'
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  // Add initial Server Claude tasks
  const initialTasks = [
    ['CT-001', 'Server Claude', 'Docker Setup', 'High', 'Pending', 'Run server audit to check existing Docker services', 'List of running containers and services', '-', new Date(), ''],
    ['CT-002', 'Server Claude', 'MQTT Config', 'High', 'Pending', 'Configure EMQX broker (not Mosquitto) on server', 'EMQX running on port 1883 with dashboard on 18083', 'CT-001', new Date(), ''],
    ['CT-003', 'Server Claude', 'Docker Compose', 'High', 'Pending', 'Create comprehensive docker-compose.yml for Ignition + supporting services', 'Working multi-container setup', 'CT-001', new Date(), ''],
    ['CT-004', 'Server Claude', 'Integration Test', 'Medium', 'Pending', 'Test MQTT connection between Mac Mosquitto and Server EMQX', 'Confirmed bidirectional MQTT communication', 'CT-002', new Date(), ''],
    ['CT-005', 'Mac Claude', 'Documentation', 'Medium', 'Pending', 'Update architecture docs with Server Claude findings', 'Updated MQTT_BROKER_ARCHITECTURE.md', 'CT-002', new Date(), '']
  ];
  
  sheet.getRange(2, 1, initialTasks.length, headers.length).setValues(initialTasks);
  
  // Apply conditional formatting for status
  applyStatusFormatting(sheet, 5);
  
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
  
  // Add instance color coding
  const instanceValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Mac Claude', 'Server Claude', 'Both'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('B2:B').setDataValidation(instanceValidation);
  
  // Add status validation
  const statusValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Pending', 'In Progress', 'Complete', 'Blocked'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('E2:E').setDataValidation(statusValidation);
  
  sheet.setFrozenRows(1);
}

/**
 * Handle edits to the Claude Approvals sheet
 */
function onApprovalEdit(e) {
  const sheet = e.source.getActiveSheet();
  if (sheet.getName() !== 'Claude Approvals') return;
  
  const range = e.range;
  const column = range.getColumn();
  const row = range.getRow();
  
  // Process response in Your Response column
  if (column === 5 && row > 1) {
    const response = sheet.getRange(row, 5).getValue();
    let newStatus = 'PENDING';
    
    // Map responses to statuses
    if (response.includes('Yes, proceed') || response.includes('Fast track')) {
      newStatus = 'APPROVED';
    } else if (response.includes('discuss') || response.includes('chat') || response.includes('info') || response.includes('caution')) {
      newStatus = 'DISCUSS';
    } else if (response.includes('later') || response.includes('different approach')) {
      newStatus = 'POSTPONED';
    } else if (response.includes('No,')) {
      newStatus = 'REJECTED';
    }
    
    // Update status and timestamp
    sheet.getRange(row, 4).setValue(newStatus);
    sheet.getRange(row, 7).setValue(new Date());
  }
}

/**
 * Setup Dashboard tab with summary formulas
 */
function setupDashboard(ss) {
  const sheet = ss.getSheetByName('Dashboard');
  sheet.clear();
  
  // Title
  sheet.getRange('A1').setValue('Industrial IoT Stack Progress Dashboard');
  sheet.getRange('A1').setFontSize(20).setFontWeight('bold');
  
  // Summary metrics
  const metrics = [
    ['Overall Progress', '=AVERAGE(\'Docker Migration Tasks\'!H:H)'],
    ['Active Tasks', '=COUNTIF(\'Docker Migration Tasks\'!C:C,"In Progress")'],
    ['Pending Tasks', '=COUNTIF(\'Docker Migration Tasks\'!C:C,"Pending")'],
    ['Completed Tasks', '=COUNTIF(\'Docker Migration Tasks\'!C:C,"Complete")'],
    ['Healthy Components', '=COUNTIF(\'System Components Status\'!C:C,"✅ Healthy")'],
    ['Components with Issues', '=COUNTIF(\'System Components Status\'!C:C,"⚠️*")'],
    ['Projects Ready', '=COUNTIF(\'Project Migration Tracker\'!B:B,"✅ Ready")'],
    ['Projects Migrated', '=COUNTIF(\'Project Migration Tracker\'!E:E,"✅ Complete")']
  ];
  
  sheet.getRange('A3').setValue('Key Metrics');
  sheet.getRange('A3').setFontSize(16).setFontWeight('bold');
  
  const metricsRange = sheet.getRange(4, 1, metrics.length, 2);
  metricsRange.setValues(metrics);
  
  // Format percentages
  sheet.getRange('B4').setNumberFormat('0%');
  
  // Add last update timestamp
  sheet.getRange('A13').setValue('Last Updated:');
  sheet.getRange('B13').setValue('=NOW()');
  sheet.getRange('B13').setNumberFormat('yyyy-mm-dd hh:mm:ss');
}

/**
 * Format headers consistently
 */
function formatHeaders(sheet, numColumns) {
  const headerRange = sheet.getRange(1, 1, 1, numColumns);
  headerRange.setBackground(CONFIG.colors.header);
  headerRange.setFontColor('#ffffff');
  headerRange.setFontWeight('bold');
  headerRange.setHorizontalAlignment('center');
  sheet.setFrozenRows(1);
}

/**
 * Apply conditional formatting for status columns
 */
function applyStatusFormatting(sheet, statusColumn) {
  const rules = [
    { text: 'Pending', color: CONFIG.colors.pending },
    { text: 'In Progress', color: CONFIG.colors.inProgress },
    { text: 'Complete', color: CONFIG.colors.complete },
    { text: 'Error', color: CONFIG.colors.error }
  ];
  
  rules.forEach(rule => {
    const range = sheet.getRange(2, statusColumn, sheet.getLastRow() - 1, 1);
    const formatRule = SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(rule.text)
      .setBackground(rule.color)
      .setRanges([range])
      .build();
    
    const currentRules = sheet.getConditionalFormatRules();
    currentRules.push(formatRule);
    sheet.setConditionalFormatRules(currentRules);
  });
}

/**
 * Create custom menu for easy access to functions
 */
function createCustomMenu() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🏭 IoT Stack Tools')
    .addItem('📊 Refresh Dashboard', 'refreshDashboard')
    .addItem('➕ Add Docker Task', 'showAddTaskDialog')
    .addItem('📝 Log Agent Activity', 'showLogActivityDialog')
    .addItem('🔄 Update Component Status', 'updateComponentStatus')
    .addSeparator()
    .addItem('📧 Send Status Report', 'sendStatusReport')
    .addItem('⚙️ Settings', 'showSettings')
    .addToUi();
}

/**
 * Setup automation triggers
 */
function setupAutomationTriggers() {
  // Remove existing triggers
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));
  
  // Create new triggers
  ScriptApp.newTrigger('refreshDashboard')
    .timeBased()
    .everyMinutes(5)
    .create();
  
  ScriptApp.newTrigger('checkHealthAlerts')
    .timeBased()
    .everyMinutes(15)
    .create();
  
  // Add trigger for Claude Approvals
  ScriptApp.newTrigger('onApprovalEdit')
    .forSpreadsheet(SpreadsheetApp.getActiveSpreadsheet())
    .onEdit()
    .create();
}

/**
 * Refresh dashboard data
 */
function refreshDashboard() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Dashboard');
  const now = new Date();
  sheet.getRange('B13').setValue(now);
  
  // Force recalculation of formulas
  SpreadsheetApp.flush();
}

/**
 * Check for health alerts
 */
function checkHealthAlerts() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const statusSheet = ss.getSheetByName('System Components Status');
  const data = statusSheet.getDataRange().getValues();
  
  const alerts = [];
  
  for (let i = 1; i < data.length; i++) {
    if (data[i][2] && data[i][2].toString().includes('⚠️')) {
      alerts.push(`${data[i][0]} requires attention: ${data[i][8]}`);
    }
  }
  
  if (alerts.length > 0) {
    // Log to Agent Activities
    const agentSheet = ss.getSheetByName('Agent Activities');
    agentSheet.appendRow([
      new Date(),
      'System Monitor',
      'Health Check Alert',
      'Alert',
      '1 min',
      alerts.join('; '),
      'Investigate issues'
    ]);
  }
}

/**
 * Show dialog to add new task
 */
function showAddTaskDialog() {
  const html = HtmlService.createHtmlOutput(getAddTaskDialogHtml())
    .setWidth(400)
    .setHeight(500);
  SpreadsheetApp.getUi().showModalDialog(html, 'Add New Docker Task');
}

/**
 * Add new task from form data
 */
function addDockerTask(taskData) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Docker Migration Tasks');
  const lastRow = sheet.getLastRow();
  const taskId = 'DM-' + String(lastRow).padStart(3, '0');
  
  sheet.appendRow([
    taskId,
    taskData.description,
    taskData.status,
    taskData.priority,
    taskData.assignedTo,
    taskData.startDate,
    taskData.dueDate,
    '0%',
    taskData.notes,
    taskData.dependencies
  ]);
  
  return taskId;
}

/**
 * Update component status (can be called from external scripts)
 */
function updateComponentStatus(componentName, status, health, alerts) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('System Components Status');
  const data = sheet.getDataRange().getValues();
  
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === componentName) {
      sheet.getRange(i + 1, 2).setValue(status);
      sheet.getRange(i + 1, 3).setValue(health);
      sheet.getRange(i + 1, 5).setValue(new Date());
      sheet.getRange(i + 1, 9).setValue(alerts || 'None');
      break;
    }
  }
}

/**
 * Send status report via email
 */
function sendStatusReport() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const dashboardSheet = ss.getSheetByName('Dashboard');
  const metricsData = dashboardSheet.getRange('A4:B11').getValues();
  
  let emailBody = 'Industrial IoT Stack Status Report\n\n';
  
  metricsData.forEach(row => {
    emailBody += `${row[0]}: ${row[1]}\n`;
  });
  
  emailBody += `\nView full dashboard: ${ss.getUrl()}`;
  
  // Get email from user properties or prompt
  const userProperties = PropertiesService.getUserProperties();
  let email = userProperties.getProperty('notificationEmail');
  
  if (!email) {
    email = Browser.inputBox('Enter email address for status reports:');
    userProperties.setProperty('notificationEmail', email);
  }
  
  MailApp.sendEmail({
    to: email,
    subject: 'IoT Stack Status Report - ' + new Date().toLocaleDateString(),
    body: emailBody
  });
  
  SpreadsheetApp.getActiveSpreadsheet().toast('Status report sent to ' + email, 'Success', 5);
}

/**
 * Show dialog to add new task
 */
function showAddTaskDialog() {
  const html = HtmlService.createHtmlOutput(getAddTaskDialogHtml())
    .setWidth(400)
    .setHeight(500);
  SpreadsheetApp.getUi().showModalDialog(html, 'Add New Docker Task');
}

/**
 * Create HTML template for Add Task Dialog
 */
function getAddTaskDialogHtml() {
  return `
<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
    <style>
      body { font-family: Arial, sans-serif; padding: 20px; }
      .form-group { margin-bottom: 15px; }
      label { display: block; margin-bottom: 5px; font-weight: bold; }
      input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
      textarea { resize: vertical; }
      .button-group { margin-top: 20px; text-align: right; }
      button { padding: 10px 20px; margin-left: 10px; border: none; border-radius: 4px; cursor: pointer; }
      .submit { background-color: #1a73e8; color: white; }
      .cancel { background-color: #e0e0e0; }
    </style>
  </head>
  <body>
    <form id="taskForm">
      <div class="form-group">
        <label for="description">Task Description</label>
        <input type="text" id="description" name="description" required>
      </div>
      
      <div class="form-group">
        <label for="status">Status</label>
        <select id="status" name="status">
          <option value="Pending">Pending</option>
          <option value="In Progress">In Progress</option>
          <option value="Complete">Complete</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="priority">Priority</label>
        <select id="priority" name="priority">
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="assignedTo">Assigned To</label>
        <select id="assignedTo" name="assignedTo">
          <option value="MacBook Claude">MacBook Claude</option>
          <option value="Server Claude">Server Claude</option>
          <option value="Human">Human</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="startDate">Start Date</label>
        <input type="date" id="startDate" name="startDate">
      </div>
      
      <div class="form-group">
        <label for="dueDate">Due Date</label>
        <input type="date" id="dueDate" name="dueDate">
      </div>
      
      <div class="form-group">
        <label for="notes">Notes</label>
        <textarea id="notes" name="notes" rows="3"></textarea>
      </div>
      
      <div class="form-group">
        <label for="dependencies">Dependencies</label>
        <input type="text" id="dependencies" name="dependencies" placeholder="e.g., DM-001, DM-002">
      </div>
      
      <div class="button-group">
        <button type="button" class="cancel" onclick="google.script.host.close()">Cancel</button>
        <button type="submit" class="submit">Add Task</button>
      </div>
    </form>
    
    <script>
      document.getElementById('taskForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
          description: document.getElementById('description').value,
          status: document.getElementById('status').value,
          priority: document.getElementById('priority').value,
          assignedTo: document.getElementById('assignedTo').value,
          startDate: document.getElementById('startDate').value,
          dueDate: document.getElementById('dueDate').value,
          notes: document.getElementById('notes').value,
          dependencies: document.getElementById('dependencies').value
        };
        
        google.script.run
          .withSuccessHandler(function(taskId) {
            alert('Task ' + taskId + ' added successfully!');
            google.script.host.close();
          })
          .withFailureHandler(function(error) {
            alert('Error: ' + error);
          })
          .addDockerTask(formData);
      });
    </script>
  </body>
</html>
  `;
}