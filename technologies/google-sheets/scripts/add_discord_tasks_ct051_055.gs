/**
 * Add Discord Deployment Tasks CT-051 through CT-055 to Claude Tasks sheet
 * 
 * Instructions:
 * 1. Open your IoT Stack Progress Master Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Create a new script file and paste this entire content
 * 4. Save and run addDiscordDeploymentTasks()
 */

/**
 * Add Discord deployment tasks CT-051 through CT-055 to existing Claude Tasks tab
 */
function addDiscordDeploymentTasks() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Claude Tasks');
  
  if (!sheet) {
    throw new Error('Claude Tasks sheet not found. Please create it first using addClaudeTasksTab().');
  }
  
  // Discord deployment tasks matching exact format: 
  // Task ID, Instance, Task Type, Priority, Status, Description, Expected Output, Dependencies, Date Added, Completed
  const deploymentTasks = [
    [
      'CT-051',
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
      'CT-052',
      'Server Claude',
      'Task Worker Deploy', 
      'High',
      'Pending',
      'Deploy the Mac Claude task worker as Docker container alongside Discord bot. Ensure proper networking and credential access.',
      'Task worker container running and processing Google Sheets tasks automatically',
      'CT-051 completed (Discord bot deployed)',
      new Date(),
      ''
    ],
    [
      'CT-053',
      'Server Claude',
      'Health Monitoring',
      'Medium',
      'Pending', 
      'Set up health monitoring for Discord bot and task worker containers. Implement auto-restart and alerting capabilities.',
      'Health monitor running and automatically restarting failed services',
      'CT-051, CT-052 completed',
      new Date(),
      ''
    ],
    [
      'CT-054',
      'Server Claude',
      'End-to-End Testing',
      'High',
      'Pending',
      'Test complete workflow: Discord command → Google Sheets task → automated processing → completion. Verify 24/7 persistent operation.',
      'Complete workflow tested and verified working continuously without manual intervention',
      'CT-051, CT-052, CT-053 completed',
      new Date(),
      ''
    ],
    [
      'CT-055',
      'Mac Claude',
      'Documentation Update',
      'Medium',
      'Pending',
      'Update INDEX.md and .claude documentation to reflect successful persistent deployment capabilities and workflow automation.',
      'Documentation updated with deployment procedures and automation workflows',
      'CT-054 completed (testing successful)',
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
  
  // Format Date Added column (column I = 9)
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
    `Added ${deploymentTasks.length} Discord deployment tasks (CT-051 through CT-055)`, 
    'Discord Deployment Tasks Added', 
    5
  );
  
  Logger.log(`✅ Added Discord deployment tasks CT-051 through CT-055`);
  Logger.log(`📋 Tasks focus on Docker deployment, health monitoring, and testing`);
  Logger.log(`🚀 This enables 24/7 persistent Discord bot automation`);
}