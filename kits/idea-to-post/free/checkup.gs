/**
 * Idea to Live Post kit: check-up (version 0.1.0).
 * Adds a "Help" menu with "Run check-up". It checks the workbook's setup
 * (expected tabs, header rows, required Setup values) and shows one support code.
 *
 * Privacy: the report lists tab names, header names and whether a Setup value is
 * filled in or empty. It never includes cell contents, passwords or keys.
 * Nothing is sent anywhere. You copy the report yourself if you choose to share it.
 */
var KIT_ID = 'IP';
var KIT_VERSION = '0.1.0';

var EXPECTED = {
  'Ideas': ['id', 'date_found', 'idea', 'source_name', 'source_link', 'confidence_tier', 'why_it_matters_here', 'status'],
  'Queue': ['id', 'title', 'keyword', 'volume_per_month', 'rationale', 'stage', 'brief_link', 'draft_link', 'live_url', 'live_date', 'notes'],
  'Measure': ['url', 'live_date', 'checkpoint_week', 'impressions', 'clicks', 'average_position', 'top_query', 'notes'],
  'Setup': ['key', 'value', 'required']
};
var REQUIRED_SETUP = ['org_name', 'audience', 'voice_notes', 'site_url', 'blog_path', 'one_call_to_action'];

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
  // Other kit scripts in the same project add their own menus through these hooks.
  if (typeof addIdeasMenu === 'function') { addIdeasMenu(); }
  if (typeof addSearchMenu === 'function') { addSearchMenu(); }
}

function checkHash_(text) {
  var h = 7;
  for (var i = 0; i < text.length; i++) {
    h = (h * 31 + text.charCodeAt(i)) % 46656;
  }
  var s = h.toString(36).toUpperCase();
  while (s.length < 3) { s = '0' + s; }
  return s;
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var lines = [];
  var firstFailure = null; // {step, code}
  var version = 'FR';

  // Read the version flag from the Setup tab if it exists.
  var setupSheet = ss.getSheetByName('Setup');
  if (setupSheet) {
    var rows = setupSheet.getDataRange().getValues();
    for (var r = 1; r < rows.length; r++) {
      if (String(rows[r][0]).trim() === 'version') {
        var v = String(rows[r][1]).trim().toUpperCase();
        if (v === 'LC' || v === 'FR') { version = v; }
      }
    }
  }
  var stepBase = KIT_ID + '-' + version + '-01-';

  function fail(step, code, message) {
    lines.push('FAIL  ' + message + ' (' + code + ')');
    if (!firstFailure) { firstFailure = {step: stepBase + step, code: code}; }
  }

  // 1. Tabs and headers.
  Object.keys(EXPECTED).forEach(function (tab) {
    var sheet = ss.getSheetByName(tab);
    if (!sheet) {
      fail('3', 'E02', 'Tab "' + tab + '" is missing or renamed');
      return;
    }
    lines.push('ok    Tab "' + tab + '" found');
    var lastCol = Math.max(sheet.getLastColumn(), EXPECTED[tab].length);
    var header = sheet.getRange(1, 1, 1, lastCol).getValues()[0].map(function (c) { return String(c).trim(); });
    var missing = EXPECTED[tab].filter(function (h) { return header.indexOf(h) === -1; });
    if (missing.length) {
      fail('4', 'E03', 'Tab "' + tab + '" is missing header(s): ' + missing.join(', '));
    } else {
      lines.push('ok    Tab "' + tab + '" headers match');
    }
  });

  // 2. Setup values: report only filled or empty, never the value itself.
  if (setupSheet) {
    var data = setupSheet.getDataRange().getValues();
    var filled = {};
    for (var i = 1; i < data.length; i++) {
      filled[String(data[i][0]).trim()] = String(data[i][1]).trim() !== '';
    }
    REQUIRED_SETUP.forEach(function (key) {
      if (filled[key]) {
        lines.push('ok    Setup "' + key + '" is filled in');
      } else {
        fail('5', 'E04', 'Setup "' + key + '" is empty or missing');
      }
    });
    // Check the site address shape without printing it.
    var siteRow = null;
    for (var j = 1; j < data.length; j++) {
      if (String(data[j][0]).trim() === 'site_url') { siteRow = String(data[j][1]).trim(); }
    }
    if (siteRow && siteRow.indexOf('https://') !== 0) {
      fail('5', 'E04', 'Setup "site_url" should start with https://');
    }
  }

  var step = firstFailure ? firstFailure.step : (KIT_ID + '-' + version + '-00-0');
  var code = firstFailure ? firstFailure.code : 'OK';
  var support = step + '-' + code + '-v' + KIT_VERSION + '-' + checkHash_(step + '|' + code + '|' + KIT_VERSION);

  var report = 'Idea to Live Post check-up\n' +
    'Support code: ' + support + '\n\n' + lines.join('\n') +
    '\n\nThis report lists tab names, header names and filled/empty flags only.';

  var html = HtmlService.createHtmlOutput(
    '<p><b>Support code</b></p><p style="font-size:16px"><code>' + support + '</code></p>' +
    '<p>This is the full report that would be shared if you copy it. It contains no cell contents, passwords or keys.</p>' +
    '<textarea style="width:100%;height:220px">' + report.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</textarea>'
  ).setWidth(520).setHeight(420);
  SpreadsheetApp.getUi().showModalDialog(html, 'Check-up result');
}
