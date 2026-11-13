/**
 * @OnlyCurrentDoc
 *
 * Civic voice kit: deadline highlighter (low-cost version, optional)
 * Adds a "Civic voice" menu. "Highlight due dates" colors the Response due cell of each open
 * row on the Records requests tab, and the Comment sign-up deadline cell on the Meetings tab:
 * light red when the date has passed, light yellow when it falls in the next three days.
 *
 * It changes only cell background colors on those two date columns. It sends no email and
 * reads nothing outside this spreadsheet. "Clear highlights" removes the colors it added.
 */

var SOON_DAYS = 3;
var DONE_WORDS = ['received', 'closed', 'withdrawn', 'delivered', 'spoken', 'written only', 'not delivered'];
var RED = '#f4cccc';
var YELLOW = '#fff2cc';

// Called from onOpen() in checkup.gs. A project can have only one onOpen, so this file has none.
function addDeadlineMenu_() {
  SpreadsheetApp.getUi()
    .createMenu('Civic voice')
    .addItem('Highlight due dates', 'highlightDueDates')
    .addItem('Clear highlights', 'clearHighlights')
    .addToUi();
}

function targets() {
  return [
    { tab: 'Records requests', dateHeader: 'Response due', statusHeader: 'Status' },
    { tab: 'Meetings', dateHeader: 'Comment sign-up deadline', statusHeader: 'Comment status' }
  ];
}

function colIndex(headers, name) {
  for (var i = 0; i < headers.length; i++) {
    if (String(headers[i]).trim() === name) { return i; }
  }
  return -1;
}

function highlightDueDates() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var today = new Date();
  today.setHours(0, 0, 0, 0);
  var soon = new Date(today.getTime() + SOON_DAYS * 86400000);
  var changed = 0;
  targets().forEach(function (t) {
    var sheet = ss.getSheetByName(t.tab);
    if (!sheet || sheet.getLastRow() < 2) { return; }
    var data = sheet.getDataRange().getValues();
    var d = colIndex(data[0], t.dateHeader);
    var s = colIndex(data[0], t.statusHeader);
    if (d === -1) { return; }
    for (var r = 1; r < data.length; r++) {
      var value = data[r][d];
      if (!(value instanceof Date)) { continue; }
      var status = s === -1 ? '' : String(data[r][s]).trim().toLowerCase();
      if (DONE_WORDS.indexOf(status) !== -1) { continue; }
      var cell = sheet.getRange(r + 1, d + 1);
      if (value < today) { cell.setBackground(RED); changed++; }
      else if (value <= soon) { cell.setBackground(YELLOW); changed++; }
    }
  });
  SpreadsheetApp.getActive().toast(changed + ' date cell(s) highlighted.', 'Civic voice', 5);
}

function clearHighlights() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  targets().forEach(function (t) {
    var sheet = ss.getSheetByName(t.tab);
    if (!sheet || sheet.getLastRow() < 2) { return; }
    var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    var d = colIndex(headers, t.dateHeader);
    if (d === -1) { return; }
    var range = sheet.getRange(2, d + 1, sheet.getLastRow() - 1, 1);
    var colors = range.getBackgrounds();
    for (var i = 0; i < colors.length; i++) {
      if (colors[i][0] === RED || colors[i][0] === YELLOW) { colors[i][0] = null; }
    }
    range.setBackgrounds(colors);
  });
}
