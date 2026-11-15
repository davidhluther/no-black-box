/**
 * Owner's Numbers CSV export (Google Apps Script), for the low cost version.
 *
 * Adds a menu item "Owner's Numbers, Save data tabs as CSV in Drive" (the menu is created by checkup.gs). It
 * writes four files (Sales, Bank, Bookings and Settings as plain CSV) into
 * a Drive folder you own, so you can attach them to an AI Project. It never
 * writes into a folder someone else owns, even one with the same name.
 * It only writes to your own Drive. It sends nothing anywhere else.
 */
var FOLDER_NAME = 'owners-numbers-data';
var TABS_TO_EXPORT = ['Sales', 'Bank', 'Bookings', 'Settings'];
var FOLDER_ID_KEY = 'owners_numbers_folder_id';

// The menu is added by onOpen() in checkup.gs, which looks for saveCsvToDrive.

function saveCsvToDrive() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var folder = ownFolder_();
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
  SpreadsheetApp.getUi().alert('Saved ' + saved.join(', ') + ' in your Drive folder "' + FOLDER_NAME + '":\n' + folder.getUrl());
}

// Your numbers go only into a folder you own. The folder is remembered by its ID for you alone,
// so a folder with the same name that someone else shared with you is never used.
function ownFolder_() {
  var props = PropertiesService.getUserProperties();
  var id = props.getProperty(FOLDER_ID_KEY);
  if (id) {
    try {
      var saved = DriveApp.getFolderById(id);
      // If Google will not say who you are, trust the folder this script saved for you before.
      if (!saved.isTrashed() && isMine_(saved) !== false) return saved;
    } catch (e) { /* deleted or no longer reachable: pick or make another below */ }
  }
  var found = null, it = DriveApp.getFoldersByName(FOLDER_NAME);
  while (!found && it.hasNext()) {
    var f = it.next();
    if (!f.isTrashed() && isMine_(f) === true) found = f;
  }
  if (!found) found = DriveApp.createFolder(FOLDER_NAME);
  props.setProperty(FOLDER_ID_KEY, found.getId());
  return found;
}

// true if you own it, false if someone else does, null if Google did not give your address.
function isMine_(item) {
  var me = Session.getEffectiveUser().getEmail();
  if (!me) return null;
  var owner = item.getOwner();
  return !!owner && owner.getEmail() === me;
}
