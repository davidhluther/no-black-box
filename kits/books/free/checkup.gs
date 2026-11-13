/**
 * Books kit check-up (Google Apps Script), kit code BK, free version.
 *
 * Adds a "Help" menu to the sheet with "Run check-up". The check-up tests the
 * sheet's setup and shows ONE support code, plus an optional plain-text report.
 *
 * What it looks at: tab names, whether each tab's header row matches, whether
 * the required Settings cells are filled, and how many formula cells show an
 * error. What it never does: read out or report any cell's contents, any
 * name, amount, or account. It reports counts and yes/no answers only, and it
 * shows you the full report on screen before you decide to copy it.
 *
 * It only reads this sheet. It does not touch QuickBooks and changes nothing.
 *
 * Support code format: BK-FR-<guide>-<step>-<problem>-v<kit version>-<check>
 *   step     the first setup step that failed (guide BK-FR-02 or BK-FR-03)
 *   problem  an E-code from fixes.md, or E00 when everything passes
 *   check    three characters computed from the other parts, so a typo shows
 *            up: base-36 of ((hash * 31 + character code) mod 46656), run over
 *            the text "<step>|<problem>|<version>".
 */
var KIT_VERSION = '0.1.0';
var KIT_CODE = 'BK-FR';

var EXPECTED = {
  'Settings': ['Setting', 'Value', 'Note'],
  'Accounts': ['Account', 'Kind', 'Restricted', 'Books balance', 'Bank balance', 'Difference', 'As of', 'Note'],
  'Commitments': ['Item', 'Amount', 'Due', 'Restricted use', 'Note'],
  'Monthly cash': ['Month', 'Cash in', 'Cash out', 'Net', 'Ending cash', 'Note'],
  'Runway': ['Measure', 'Value', 'How it is worked out'],
  'QB Profit and Loss': [],
  'QB Balance Sheet': []
};

// Settings cells that must be filled: row number on the Settings tab.
var SETTINGS_ROWS = [2, 3, 4, 5, 6, 7];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
}

function checkHash_(text) {
  var h = 0;
  for (var i = 0; i < text.length; i++) {
    h = (h * 31 + text.charCodeAt(i)) % 46656;
  }
  var s = h.toString(36).toUpperCase();
  while (s.length < 3) { s = '0' + s; }
  return s;
}

function makeCode_(step, problem) {
  var base = step + '|' + problem + '|' + KIT_VERSION;
  return step + '-' + problem + '-v' + KIT_VERSION + '-' + checkHash_(base);
}

function runChecks_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var lines = [];
  var failStep = null;
  var failCode = null;
  function fail(step, code) {
    if (failStep === null) { failStep = step; failCode = code; }
  }

  // 1. Tabs present, exact names.
  var missing = [];
  var names = Object.keys(EXPECTED);
  for (var i = 0; i < names.length; i++) {
    var present = ss.getSheetByName(names[i]) !== null;
    lines.push('Tab "' + names[i] + '": ' + (present ? 'found' : 'MISSING'));
    if (!present) { missing.push(names[i]); }
  }
  if (missing.length) { fail('BK-FR-02-1', 'E04'); }

  // 2. Header rows match.
  var headerProblems = 0;
  for (var j = 0; j < names.length; j++) {
    var want = EXPECTED[names[j]];
    var sh = ss.getSheetByName(names[j]);
    if (!sh || want.length === 0) { continue; }
    var got = sh.getRange(1, 1, 1, want.length).getDisplayValues()[0];
    var ok = true;
    for (var k = 0; k < want.length; k++) {
      if (String(got[k]).trim() !== want[k]) { ok = false; }
    }
    lines.push('Header row on "' + names[j] + '": ' + (ok ? 'matches' : 'DIFFERENT'));
    if (!ok) { headerProblems++; }
  }
  if (headerProblems) { fail('BK-FR-02-2', 'E08'); }

  // 3. Required Settings cells filled (yes/no only; values never reported).
  var settings = ss.getSheetByName('Settings');
  var blank = 0;
  if (settings) {
    for (var r = 0; r < SETTINGS_ROWS.length; r++) {
      var v = settings.getRange(SETTINGS_ROWS[r], 2).getDisplayValue();
      var filled = String(v).trim() !== '';
      lines.push('Settings row ' + SETTINGS_ROWS[r] + ' value: ' + (filled ? 'filled' : 'EMPTY'));
      if (!filled) { blank++; }
    }
  }
  if (blank) { fail('BK-FR-02-3', 'E07'); }

  // 4. Formula error counts (counts only).
  var errCount = 0;
  var spots = [['Monthly cash', 'D2:E13'], ['Runway', 'B2:B12'], ['Accounts', 'F2:F6']];
  for (var m = 0; m < spots.length; m++) {
    var tab = ss.getSheetByName(spots[m][0]);
    if (!tab) { continue; }
    var vals = tab.getRange(spots[m][1]).getDisplayValues();
    var here = 0;
    for (var a = 0; a < vals.length; a++) {
      for (var b = 0; b < vals[a].length; b++) {
        if (/^#(REF|NAME|VALUE|DIV\/0|N\/A|ERROR|NUM)/.test(String(vals[a][b]))) { here++; }
      }
    }
    lines.push('Formula errors on "' + spots[m][0] + '": ' + here);
    errCount += here;
  }
  if (errCount) { fail('BK-FR-02-4', 'E03'); }

  var step = failStep === null ? 'BK-FR-03-5' : failStep;
  var problem = failCode === null ? 'E00' : failCode;
  return { code: makeCode_(step, problem), lines: lines, passed: failCode === null };
}

function esc_(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function runCheckup() {
  var res = runChecks_();
  var report = [
    'Books kit check-up report',
    'Kit version: ' + KIT_VERSION,
    'Support code: ' + res.code,
    'Result: ' + (res.passed ? 'all checks passed' : 'a problem was found')
  ].concat(res.lines).join('\n');

  var html =
    '<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.4">' +
    '<p><b>Your support code</b></p>' +
    '<p style="font-size:18px"><code>' + esc_(res.code) + '</code></p>' +
    '<p>' + (res.passed ? 'All checks passed.' : 'A problem was found. Look up the E-code in fixes.md, or send this code with the step ID where you got stuck.') + '</p>' +
    '<p><b>Optional report.</b> This is exactly what would be shared if you copy it. It holds tab names from the kit, yes/no answers, and counts. It holds no amounts, names, account names, or cell contents. Nothing is sent anywhere unless you copy it and send it yourself.</p>' +
    '<textarea readonly style="width:100%;height:210px;font-family:monospace;font-size:12px">' + esc_(report) + '</textarea>' +
    '</div>';
  SpreadsheetApp.getUi().showModalDialog(HtmlService.createHtmlOutput(html).setWidth(560).setHeight(470), 'Check-up');
}
