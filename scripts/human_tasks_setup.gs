/**
 * Human Tasks Google Sheets Setup
 * Add this to your existing Google Apps Script project
 */

/**
 * Setup Human Tasks tab for tracking manual tasks
 */
function setupHumanTasks(ss) {
  // Create or get the Human Tasks sheet
  const sheet = createOrGetSheet(ss || SpreadsheetApp.getActiveSpreadsheet(), 'Human Tasks');
  sheet.clear();
  
  // Define headers
  const headers = [
    'Role', 'Task Type', 'Priority', 'Status', 
    'Assigned To', 'Dependencies', 'Notes', 'Date Added'
  ];
  
  // Set headers
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  formatHeaders(sheet, headers.length);
  
  // Set up data validation for Role column (A)
  const roleValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Architect', 'Controls Engineer', 'Both'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('A2:A').setDataValidation(roleValidation);
  
  // Set up data validation for Task Type column (B)
  const taskTypeValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList([
      'Architecture', 
      'Ignition Screens', 
      'PLC Logic', 
      'Docker Setup', 
      'Testing', 
      'Documentation'
    ], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('B2:B').setDataValidation(taskTypeValidation);
  
  // Set up data validation for Priority column (C)
  const priorityValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['High', 'Medium', 'Low'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('C2:C').setDataValidation(priorityValidation);
  
  // Set up data validation for Status column (D)
  const statusValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Pending', 'In Progress', 'Complete', 'On Hold'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange('D2:D').setDataValidation(statusValidation);
  
  // Format Date Added column (H) for datetime
  sheet.getRange('H:H').setNumberFormat('yyyy-mm-dd hh:mm');
  
  // Apply conditional formatting for Status column
  const statusRules = [
    { text: 'Pending', color: '#fce4ec' },      // Light red
    { text: 'In Progress', color: '#fff3cd' },   // Light yellow
    { text: 'Complete', color: '#d4edda' },      // Light green
    { text: 'On Hold', color: '#e2e3e5' }        // Light gray
  ];
  
  statusRules.forEach(rule => {
    const range = sheet.getRange('D2:D');
    const formatRule = SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(rule.text)
      .setBackground(rule.color)
      .setRanges([range])
      .build();
    
    const currentRules = sheet.getConditionalFormatRules();
    currentRules.push(formatRule);
    sheet.setConditionalFormatRules(currentRules);
  });
  
  // Apply conditional formatting for Priority column
  const priorityRules = [
    { text: 'High', color: '#f8d7da' },         // Light red
    { text: 'Medium', color: '#fff3cd' },        // Light yellow
    { text: 'Low', color: '#d1ecf1' }           // Light blue
  ];
  
  priorityRules.forEach(rule => {
    const range = sheet.getRange('C2:C');
    const formatRule = SpreadsheetApp.newConditionalFormatRule()
      .whenTextEqualTo(rule.text)
      .setBackground(rule.color)
      .setRanges([range])
      .build();
    
    const currentRules = sheet.getConditionalFormatRules();
    currentRules.push(formatRule);
    sheet.setConditionalFormatRules(currentRules);
  });
  
  // Set column widths for better readability
  sheet.setColumnWidth(1, 120);  // Role
  sheet.setColumnWidth(2, 150);  // Task Type
  sheet.setColumnWidth(3, 80);   // Priority
  sheet.setColumnWidth(4, 100);  // Status
  sheet.setColumnWidth(5, 150);  // Assigned To
  sheet.setColumnWidth(6, 200);  // Dependencies
  sheet.setColumnWidth(7, 300);  // Notes
  sheet.setColumnWidth(8, 120);  // Date Added
  
  // Add sample data to demonstrate the structure
  const sampleData = [
    ['Architect', 'Architecture', 'High', 'Pending', 'You', '-', 'Finalize Docker deployment strategy and module selection for Customer A', new Date()],
    ['Controls Engineer', 'PLC Logic', 'High', 'Pending', 'Controls Engineer', 'Docker Setup Complete', 'Implement failover logic for critical brewery systems', new Date()],
    ['Both', 'Testing', 'Medium', 'Pending', 'Team', 'Architecture design complete', 'Integration testing between PLC and Ignition Docker containers', new Date()],
    ['Architect', 'Architecture', 'Medium', 'In Progress', 'You', '-', 'Design Controls Engineer onboarding workflow for Docker/server access', new Date()]
  ];
  
  if (sheet.getLastRow() === 1) {
    sheet.getRange(2, 1, sampleData.length, headers.length).setValues(sampleData);
  }
  
  // Freeze the header row
  sheet.setFrozenRows(1);
}

/**
 * Add new human task from form data
 */
function addHumanTask(taskData) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Human Tasks');
  
  sheet.appendRow([
    taskData.role,
    taskData.taskType,
    taskData.priority,
    taskData.status,
    taskData.assignedTo,
    taskData.dependencies,
    taskData.notes,
    new Date()
  ]);
  
  return 'Task added successfully';
}

/**
 * Helper function to filter Human Tasks by role
 */
function filterHumanTasksByRole(role) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Human Tasks');
  const filter = sheet.getFilter();
  
  if (!filter) {
    const dataRange = sheet.getRange(1, 1, sheet.getMaxRows(), 8);
    dataRange.createFilter();
  }
  
  // Clear existing criteria
  const filterCriteria = SpreadsheetApp.newFilterCriteria();
  
  if (role && role !== 'All') {
    // Set filter criteria for the Role column (column 1)
    filterCriteria.whenTextEqualTo(role);
    sheet.getFilter().setColumnFilterCriteria(1, filterCriteria);
  } else {
    // Remove filter to show all
    sheet.getFilter().removeColumnFilterCriteria(1);
  }
}

// Filter helper functions
function showAllHumanTasks() {
  filterHumanTasksByRole('All');
}

function showArchitectTasks() {
  filterHumanTasksByRole('Architect');
}

function showControlsEngineerTasks() {
  filterHumanTasksByRole('Controls Engineer');
}

function showSharedTasks() {
  filterHumanTasksByRole('Both');
}

/**
 * Update existing menu to include Human Tasks options
 * Call this after your existing menu setup
 */
function addHumanTasksToMenu() {
  const ui = SpreadsheetApp.getUi();
  const menu = ui.createMenu('👥 Human Tasks')
    .addItem('Show All Tasks', 'showAllHumanTasks')
    .addItem('Show Architect Tasks', 'showArchitectTasks')
    .addItem('Show Controls Engineer Tasks', 'showControlsEngineerTasks')
    .addItem('Show Shared Tasks', 'showSharedTasks')
    .addSeparator()
    .addItem('➕ Add Human Task', 'showAddHumanTaskDialog');
  
  menu.addToUi();
}

/**
 * Show dialog to add new human task
 */
function showAddHumanTaskDialog() {
  const html = HtmlService.createHtmlOutput(getAddHumanTaskDialogHtml())
    .setWidth(450)
    .setHeight(600);
  SpreadsheetApp.getUi().showModalDialog(html, 'Add New Human Task');
}

/**
 * HTML template for Add Human Task Dialog
 */
function getAddHumanTaskDialogHtml() {
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
      textarea { resize: vertical; height: 80px; }
      .button-group { margin-top: 20px; text-align: right; }
      button { padding: 10px 20px; margin-left: 10px; border: none; border-radius: 4px; cursor: pointer; }
      .submit { background-color: #1a73e8; color: white; }
      .cancel { background-color: #e0e0e0; }
      .submit:hover { background-color: #1557b0; }
      .cancel:hover { background-color: #cccccc; }
    </style>
  </head>
  <body>
    <form id="humanTaskForm">
      <div class="form-group">
        <label for="role">Role</label>
        <select id="role" name="role" required>
          <option value="">Select Role</option>
          <option value="Architect">Architect</option>
          <option value="Controls Engineer">Controls Engineer</option>
          <option value="Both">Both</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="taskType">Task Type</label>
        <select id="taskType" name="taskType" required>
          <option value="">Select Task Type</option>
          <option value="Architecture">Architecture</option>
          <option value="Ignition Screens">Ignition Screens</option>
          <option value="PLC Logic">PLC Logic</option>
          <option value="Docker Setup">Docker Setup</option>
          <option value="Testing">Testing</option>
          <option value="Documentation">Documentation</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="priority">Priority</label>
        <select id="priority" name="priority" required>
          <option value="">Select Priority</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="status">Status</label>
        <select id="status" name="status" required>
          <option value="Pending">Pending</option>
          <option value="In Progress">In Progress</option>
          <option value="Complete">Complete</option>
          <option value="On Hold">On Hold</option>
        </select>
      </div>
      
      <div class="form-group">
        <label for="assignedTo">Assigned To</label>
        <input type="text" id="assignedTo" name="assignedTo" placeholder="Enter name or team">
      </div>
      
      <div class="form-group">
        <label for="dependencies">Dependencies</label>
        <input type="text" id="dependencies" name="dependencies" placeholder="e.g., Task IDs or descriptions">
      </div>
      
      <div class="form-group">
        <label for="notes">Notes</label>
        <textarea id="notes" name="notes" placeholder="Additional details about the task"></textarea>
      </div>
      
      <div class="button-group">
        <button type="button" class="cancel" onclick="google.script.host.close()">Cancel</button>
        <button type="submit" class="submit">Add Task</button>
      </div>
    </form>
    
    <script>
      document.getElementById('humanTaskForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
          role: document.getElementById('role').value,
          taskType: document.getElementById('taskType').value,
          priority: document.getElementById('priority').value,
          status: document.getElementById('status').value,
          assignedTo: document.getElementById('assignedTo').value || '-',
          dependencies: document.getElementById('dependencies').value || '-',
          notes: document.getElementById('notes').value || '-'
        };
        
        google.script.run
          .withSuccessHandler(function(result) {
            alert(result);
            google.script.host.close();
          })
          .withFailureHandler(function(error) {
            alert('Error: ' + error);
          })
          .addHumanTask(formData);
      });
    </script>
  </body>
</html>
  `;
}