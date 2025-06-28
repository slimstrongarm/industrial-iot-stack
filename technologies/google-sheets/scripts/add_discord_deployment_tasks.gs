/**
 * Add Discord Deployment Tasks to Claude Tasks tab
 * 
 * Instructions:
 * 1. Open your IoT Stack Progress Master Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Create a new script file and paste this entire content
 * 4. Save and run addDiscordDeploymentTasks()
 */

/**
 * Add Discord deployment tasks to existing Claude Tasks tab
 */
function addDiscordDeploymentTasks() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Claude Tasks');
  
  if (!sheet) {
    throw new Error('Claude Tasks sheet not found. Please create it first.');
  }
  
  // Get existing data to find next task ID
  const existingData = sheet.getDataRange().getValues();
  const taskIds = existingData.slice(1).map(row => row[0]).filter(id => id.startsWith('CT-'));
  const nextId = taskIds.length + 1;
  
  // Discord deployment tasks based on our deployment package
  const deploymentTasks = [
    [
      `CT-${String(nextId).padStart(3, '0')}`,
      'Server Claude',
      'Discord Docker Deploy',
      'High',
      'Pending',
      'Deploy Discord bot using Docker Compose on server infrastructure. Follow SERVER_CLAUDE_DEPLOYMENT_PACKAGE.md instructions for containerized deployment.',
      'Discord bot running as persistent Docker service with auto-restart capabilities',
      'Docker and docker-compose installed on server',
      new Date(),
      ''
    ],
    [
      `CT-${String(nextId + 1).padStart(3, '0')}`,
      'Server Claude',
      'Task Worker Deploy', 
      'High',
      'Pending',
      'Deploy the Mac Claude task worker as Docker container alongside Discord bot. Ensure proper networking and credential access.',
      'Task worker container running and processing Google Sheets tasks automatically',
      `CT-${String(nextId).padStart(3, '0')} completed (Discord bot deployed)`,
      new Date(),
      ''
    ],
    [
      `CT-${String(nextId + 2).padStart(3, '0')}`,
      'Server Claude',
      'Health Monitoring',
      'Medium',
      'Pending', 
      'Set up health monitoring for Discord bot and task worker containers. Implement auto-restart and alerting capabilities.',
      'Health monitor running and automatically restarting failed services',
      `CT-${String(nextId).padStart(3, '0')}, CT-${String(nextId + 1).padStart(3, '0')} completed`,
      new Date(),
      ''
    ],
    [
      `CT-${String(nextId + 3).padStart(3, '0')}`,
      'Server Claude',
      'End-to-End Testing',
      'High',
      'Pending',
      'Test complete workflow: Discord command → Google Sheets task → automated processing → completion. Verify 24/7 persistent operation.',
      'Complete workflow tested and verified working continuously without manual intervention',
      `CT-${String(nextId).padStart(3, '0')}, CT-${String(nextId + 1).padStart(3, '0')}, CT-${String(nextId + 2).padStart(3, '0')} completed`,
      new Date(),
      ''
    ],
    [
      `CT-${String(nextId + 4).padStart(3, '0')}`,
      'Mac Claude',
      'Documentation Update',
      'Medium',
      'Pending',
      'Update INDEX.md and .claude documentation to reflect successful persistent deployment capabilities and workflow automation.',
      'Documentation updated with deployment procedures and automation workflows',
      `CT-${String(nextId + 3).padStart(3, '0')} completed (testing successful)`,
      new Date(),
      ''
    ]
  ];
  
  // Add tasks to sheet
  const lastRow = sheet.getLastRow();
  const startRow = lastRow + 1;
  
  sheet.getRange(startRow, 1, deploymentTasks.length, deploymentTasks[0].length)
    .setValues(deploymentTasks);
  
  // Apply formatting to new rows
  const newRange = sheet.getRange(startRow, 1, deploymentTasks.length, deploymentTasks[0].length);
  
  // Format Date Added column
  sheet.getRange(startRow, 9, deploymentTasks.length, 1).setNumberFormat('yyyy-mm-dd hh:mm');
  
  // Apply dropdowns to new rows
  const instanceValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Mac Claude', 'Server Claude', 'Both'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange(startRow, 2, deploymentTasks.length, 1).setDataValidation(instanceValidation);
  
  const statusValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(['Pending', 'In Progress', 'Complete', 'Blocked'], true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange(startRow, 5, deploymentTasks.length, 1).setDataValidation(statusValidation);
  
  SpreadsheetApp.getActiveSpreadsheet().toast(
    `Added ${deploymentTasks.length} Discord deployment tasks (CT-${String(nextId).padStart(3, '0')} through CT-${String(nextId + 4).padStart(3, '0')})`, 
    'Discord Deployment Tasks Added', 
    5
  );
  
  Logger.log(`✅ Added Discord deployment tasks CT-${String(nextId).padStart(3, '0')} through CT-${String(nextId + 4).padStart(3, '0')}`);
}