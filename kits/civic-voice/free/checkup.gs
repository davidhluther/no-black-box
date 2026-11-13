/**
 * @OnlyCurrentDoc
 *
 * Civic voice kit: check-up
 * Adds a "Help" menu with "Run check-up". It tests whether this spreadsheet is set up the
 * way the kit expects, then shows one support code and an optional plain-text report.
 *
 * What it reads: tab names, the header row of each tab, and whether three Settings cells are
 * filled or empty. What it never reads or reports: anything you typed in your rows, the
 * contents of the Settings cells, passwords, keys, or file contents. It changes nothing.
 * Nothing is sent anywhere. You decide whether to copy the result and share it.
 */

var KIT_CODE = 'CV';
var KIT_VERSION = '0.1.0';
var VERSION_CODE = 'FR';
var GUIDE = '01';

// Tab name -> expected header row (the first row of the tab).
var EXPECTED = {
  'Meetings': ['Meeting date', 'Body', 'Item number', 'Topic', 'Packet link', 'Packet retrieved on',
    'Comment sign-up deadline', 'Time limit (minutes)', 'Prep memo link', 'Comment status',
    'Outcome record link', 'Next step date', 'Notes'],
  'Comments': ['Meeting date', 'Body', 'Item number', 'Speaking as',
    'Delivered (spoken / written only / not delivered)', 'Written copy sent to', 'Date sent',
    'Confirmation received (yes/no)', 'Outcome summary', 'Lessons'],
  'Records requests': ['Date sent', 'Agency', 'Subject', 'Law cited', 'Method', 'Response due',
    'Follow-up date', 'Status', 'Fee estimate', 'Records received on', 'Link to saved copy', 'Notes'],
  'County numbers': ['Place', 'Measure', 'Estimate', 'Margin of error', 'Unit',
    'Large margin of error (yes/no)', 'Differs from reference (yes/no/unclear)', 'Period',
    'Source link', 'Retrieved on'],
  'Transcripts': ['Meeting date', 'Body', 'Video link', 'Route used (platform transcript / yt-dlp)',
    'Prepared by', 'Prepared on', 'Transcript file link', 'Checked against video (yes/no)', 'Notes'],
  'Settings': ['Setting', 'Value', 'Notes']
};

// Settings that must be filled in, and the guide step where you fill them in.
var REQUIRED_SETTINGS = ['your_name_or_group', 'state', 'body_name'];

// Problem code -> step number inside guide 01 where the fix lives (see fixes.md).
var STEP_FOR = { 'E01': 2, 'E02': 3, 'E03': 4 };

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
  // If you also installed deadlines.gs, this adds its menu too.
  if (typeof addDeadlineMenu_ === 'function') { addDeadlineMenu_(); }
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var findings = []; // {code, text}
  var lines = [];

  // 1. Are all the tabs there?
  var tabNames = ss.getSheets().map(function (s) { return s.getName(); });
  Object.keys(EXPECTED).forEach(function (tab) {
    if (tabNames.indexOf(tab) === -1) {
      findings.push({ code: 'E01', text: 'Tab missing: ' + tab });
      lines.push('Tab "' + tab + '": MISSING');
    } else {
      lines.push('Tab "' + tab + '": found');
    }
  });

  // 2. Do the header rows match? (Only says match or differs, never shows what you typed.)
  Object.keys(EXPECTED).forEach(function (tab) {
    var sheet = ss.getSheetByName(tab);
    if (!sheet) { return; }
    var want = EXPECTED[tab];
    var got = sheet.getRange(1, 1, 1, Math.min(want.length, sheet.getMaxColumns())).getValues()[0];
    var bad = 0;
    for (var i = 0; i < want.length; i++) {
      if (String(got[i]).trim() !== want[i]) { bad++; }
    }
    if (bad > 0) {
      findings.push({ code: 'E02', text: 'Header row differs in ' + bad + ' column(s): ' + tab });
      lines.push('Tab "' + tab + '" header row: differs in ' + bad + ' column(s)');
    } else {
      lines.push('Tab "' + tab + '" header row: matches');
    }
  });

  // 3. Are the required Settings filled in? (Says filled or empty, never the value.)
  var settings = ss.getSheetByName('Settings');
  if (settings) {
    var values = settings.getDataRange().getValues();
    var byName = {};
    for (var r = 1; r < values.length; r++) {
      byName[String(values[r][0]).trim()] = String(values[r][1]).trim();
    }
    REQUIRED_SETTINGS.forEach(function (name) {
      if (!byName[name]) {
        findings.push({ code: 'E03', text: 'Setting empty: ' + name });
        lines.push('Setting "' + name + '": EMPTY');
      } else {
        lines.push('Setting "' + name + '": filled');
      }
    });
  }

  var code;
  if (findings.length === 0) {
    code = makeCode(7, 'OK');
  } else {
    var first = findings[0].code;
    code = makeCode(STEP_FOR[first], first);
  }

  var report = 'Civic voice kit check-up\n' +
    'Kit version: ' + KIT_VERSION + '\n' +
    'Support code: ' + code + '\n' +
    (findings.length ? 'Problems found: ' + findings.length + '\n' : 'Problems found: none\n') +
    '\n' + lines.join('\n') +
    '\n\nThis report lists tab names, whether header rows match, and whether three Settings cells are filled or empty. It contains none of your row contents.';

  showResult(code, report);
}

function makeCode(step, problem) {
  var prefix = KIT_CODE + '-' + VERSION_CODE + '-' + GUIDE + '-' + step;
  var core = prefix + '-' + problem + '-v' + KIT_VERSION;
  return core + '-' + hash3(core);
}

// Three-character check value (letters and digits) so a code typed wrong is easy to spot.
function hash3(text) {
  var h = 7;
  for (var i = 0; i < text.length; i++) {
    h = (h * 31 + text.charCodeAt(i)) % 46656; // 36 * 36 * 36
  }
  var s = h.toString(36).toUpperCase();
  while (s.length < 3) { s = '0' + s; }
  return s;
}

function esc(t) {
  return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function showResult(code, report) {
  var html = '<div style="font-family:Arial,sans-serif;font-size:14px">' +
    '<p><b>Your support code</b></p>' +
    '<p style="font-size:18px"><code>' + esc(code) + '</code></p>' +
    '<p>If you ask for help, send this code and the step ID where you got stuck.</p>' +
    '<p><b>Optional report.</b> This is everything the report contains. Nothing has been sent. ' +
    'Copy it only if you want to share it.</p>' +
    '<textarea readonly style="width:100%;height:220px;font-family:monospace;font-size:12px">' +
    esc(report) + '</textarea></div>';
  SpreadsheetApp.getUi().showModalDialog(
    HtmlService.createHtmlOutput(html).setWidth(560).setHeight(480), 'Check-up result');
}
