/**
 * Owner's Numbers CSV export (Google Apps Script), for the low cost version.
 *
 * Adds a menu item "Owner's Numbers, Save data tabs as CSV in Drive" (the menu is created by checkup.gs). It
 * writes four files (Sales, Bank, Bookings and Settings as plain CSV) into
 * a Drive folder in your own account so you can attach them to an AI Project.
 * It only writes to your own Drive. It sends nothing anywhere else.
 */
var FOLDER_NAME = 'owners-numbers-data';
var TABS_TO_EXPORT = ['Sales', 'Bank', 'Bookings', 'Settings'];

// The menu is added by onOpen() in checkup.gs, which looks for saveCsvToDrive.

function saveCsvToDrive() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var folders = DriveApp.getFoldersByName(FOLDER_NAME);
  var folder = folders.hasNext() ? folders.next() : DriveApp.createFolder(FOLDER_NAME);
  var saved = [];
  TABS_TO_EXPORT.forEach(function (name) {
    var sh = ss.getSheetByName(name);
    if (!sh) return;
    var values = (name === 'Settings')
      ? sh.getRange(1, 1, sh.getLastRow(), 2).getValues().map(function (r) { return [r[0], r[1]]; })
      : sh.getDataRange().getValues();
    if (name === 'Settings') values[0] = ['name', 'value'];
    var csv = values.map(function (row) {
      return row.map(function (cell) {
        var v = cell instanceof Date
          ? Utilities.formatDate(cell, ss.getSpreadsheetTimeZone(), 'yyyy-MM-dd')
          : String(cell);
        return '"' + v.replace(/"/g, '""') + '"';
      }).join(',');
    }).join('\n');
    var fileName = name.toLowerCase() + '.csv';
    // Create the new file first, then retire the old copies, so a failed write never leaves no file.
    var fresh = folder.createFile(fileName, csv, MimeType.CSV);
    var existing = folder.getFilesByName(fileName);
    while (existing.hasNext()) {
      var old = existing.next();
      if (old.getId() !== fresh.getId()) old.setTrashed(true);
    }
    saved.push(fileName);
  });
  SpreadsheetApp.getUi().alert('Saved ' + saved.join(', ') + ' in the Drive folder "' + FOLDER_NAME + '".');
}
