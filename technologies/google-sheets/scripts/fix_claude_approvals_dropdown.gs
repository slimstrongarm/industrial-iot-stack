/**
 * Quick fix for Claude Approvals dropdown
 * Copy this to Apps Script and run fixClaudeApprovalsDropdown()
 */

function fixClaudeApprovalsDropdown() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Claude Approvals');
  
  if (!sheet) {
    SpreadsheetApp.getUi().alert('Claude Approvals sheet not found!');
    return;
  }
  
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
  
  // Apply to entire Your Response column (column E)
  sheet.getRange('E2:E').setDataValidation(responseValidation);
  
  SpreadsheetApp.getActiveSpreadsheet().toast('Dropdown fixed! Click on any cell in column E to see the options.', 'Success', 5);
}