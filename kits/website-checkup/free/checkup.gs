/**
 * Website check-up kit: check-up button (Google Apps Script)
 * Kit code WC, kit version 0.1.0
 *
 * What this does
 *   Adds a "Kit help" menu to your Google Sheet with one item, "Run check-up".
 *   It checks that the tabs and column headings the kit expects are present,
 *   that the Config tab is filled in, and (for the low-cost version) that a
 *   speed-check key has been saved. Then it shows ONE support code and an
 *   optional plain-text report.
 *
 * What it never does
 *   It never reads or shows what you typed into your cells, never shows a key,
 *   and never sends anything anywhere. The report lists tab names, which
 *   column positions differ from the template, and whether each setting is
 *   filled or empty. You copy it yourself if you want to share it.
 *
 * How to add it (the setup guide WC-FR-02 walks through this)
 *   Extensions > Apps Script, delete the sample code, paste this file, save.
 *
 * The line below asks Google for access to this one file only, not all your files.
 * @OnlyCurrentDoc
 */

var KIT_CODE = 'WC';
var KIT_VERSION = '0.1.0';

// Expected tabs and the exact column headings, in order.
var EXPECTED = {
  'Config': ['Setting', 'Value', 'Notes'],
  'Scorecard': ['Section', 'ID', 'Check', 'Result', 'Points', 'Max', 'Evidence link', 'Date checked', 'Confidence', 'Notes'],
  'Summary': ['Section', 'Points', 'Possible', 'Percent', 'Checked', 'Checks in section', 'Reading'],
  'Baseline16': ['Number', 'Phase', 'Item', 'Status', 'Where to check', 'Done on', 'Notes'],
  'Pages': ['URL', 'Page type', 'Title tag', 'Title length', 'Meta description', 'Description length', 'Main heading (H1)', 'Structured data types', 'Mobile score', 'Field LCP (s)', 'Field INP (ms)', 'Field CLS', 'Date checked', 'Notes'],
  'Competitors': ['Business', 'Website', 'Google rating', 'Review count', 'Primary category', 'Mobile score', 'Structured data present', 'Distance (miles)', 'Date checked', 'Notes'],
  'Monthly': ['Month', 'Search clicks (Google)', 'Impressions (Google)', 'Average position', 'Clicks (Bing)', 'Mobile score, home page', 'Review count', 'Rating', 'Form test sent', 'Form test arrived', 'Did anything break?', 'What did search send?', 'Where did people struggle?', 'Notes']
};

// Config settings that must be filled in.
var REQUIRED_SETTINGS = ['business_name', 'site_url', 'business_type', 'city_region'];

// Allowed words in the Scorecard "Result" column.
var ALLOWED_RESULTS = ['Pass', 'Partial', 'Fail', 'Unknown', ''];

function onOpen() {
  var menu = SpreadsheetApp.getUi().createMenu('Kit help').addItem('Run check-up', 'runCheckup');
  // The low-cost version adds monthly-pulls.gs, which defines pullSpeedNow.
  if (typeof pullSpeedNow === 'function') {
    menu.addSeparator().addItem('Pull speed now', 'pullSpeedNow');
  }
  menu.addToUi();
}

/**
 * Each problem has: ver (FR unless it belongs to a low-cost step), step (the printed step ID tail, such as '02-3'),
 * code (such as 'E07'), and a plain-words note for the report.
 * No problem records any cell contents.
 */
function collectProblems_(ss, version) {
  var problems = [];

  // Tabs and headings
  Object.keys(EXPECTED).forEach(function (tabName) {
    var sheet = ss.getSheetByName(tabName);
    if (!sheet) {
      problems.push({ step: '02-2', code: 'E07', note: 'Tab missing: ' + tabName });
      return;
    }
    var want = EXPECTED[tabName];
    var have = sheet.getRange(1, 1, 1, want.length).getValues()[0];
    var differ = [];
    for (var i = 0; i < want.length; i++) {
      if (String(have[i]).trim() !== want[i]) differ.push(i + 1);
    }
    if (differ.length) {
      problems.push({ step: '02-3', code: 'E07', note: 'Tab "' + tabName + '": heading differs from the template in column(s) ' + differ.join(', ') });
    }
  });

  // Config filled in
  var config = ss.getSheetByName('Config');
  if (config) {
    var rows = config.getDataRange().getValues();
    var settings = {};
    for (var r = 1; r < rows.length; r++) {
      settings[String(rows[r][0]).trim()] = String(rows[r][1]).trim();
    }
    REQUIRED_SETTINGS.forEach(function (name) {
      if (!settings[name]) {
        problems.push({ step: '02-4', code: 'E08', note: 'Config setting empty: ' + name });
      }
    });
    if (settings['site_url'] && !/^https:\/\/[^\s]+\.[^\s]+/.test(settings['site_url'])) {
      problems.push({ step: '02-4', code: 'E21', note: 'Config setting site_url is not in the form https://www.example.org' });
    }
  }

  // Scorecard: only allowed words in the Result column
  var score = ss.getSheetByName('Scorecard');
  if (score && score.getLastRow() > 1) {
    var results = score.getRange(2, 4, score.getLastRow() - 1, 1).getValues();
    var bad = 0;
    results.forEach(function (row) {
      if (ALLOWED_RESULTS.indexOf(String(row[0]).trim()) === -1) bad++;
    });
    if (bad) {
      problems.push({ step: '03-7', code: 'E22', note: bad + ' Result cell(s) hold a word other than Pass, Partial, Fail, or Unknown' });
    }
  }

  // Summary: any formula error cells
  var summary = ss.getSheetByName('Summary');
  if (summary && summary.getLastRow() > 1) {
    var vals = summary.getRange(2, 1, summary.getLastRow() - 1, EXPECTED['Summary'].length).getDisplayValues();
    var errs = 0;
    vals.forEach(function (row) {
      row.forEach(function (cell) {
        if (/^#(REF|DIV\/0|VALUE|NAME|N\/A|ERROR)/.test(cell)) errs++;
      });
    });
    if (errs) {
      problems.push({ step: '02-3', code: 'E14', note: errs + ' cell(s) on the Summary tab show a formula error' });
    }
  }

  // Low-cost version: a speed-check key must be saved in Script Properties (value is never read out)
  if (version === 'LC') {
    var key = PropertiesService.getScriptProperties().getProperty('PAGESPEED_API_KEY');
    if (!key) {
      problems.push({ ver: 'LC', step: '02-2', code: 'E18', note: 'No speed-check key saved in Script Properties (name PAGESPEED_API_KEY)' });
    }
  }
  return problems;
}

function readVersion_(ss) {
  var config = ss.getSheetByName('Config');
  if (!config) return 'FR';
  var rows = config.getDataRange().getValues();
  for (var r = 1; r < rows.length; r++) {
    if (String(rows[r][0]).trim() === 'version') {
      var v = String(rows[r][1]).trim().toUpperCase();
      return v === 'LC' ? 'LC' : 'FR';
    }
  }
  return 'FR';
}

// Three-character check value from the list of problem codes (not from any cell contents).
function checkHash_(text) {
  var h = 5381;
  for (var i = 0; i < text.length; i++) {
    h = ((h << 5) + h + text.charCodeAt(i)) & 0x7fffffff;
  }
  var s = h.toString(36).toUpperCase();
  while (s.length < 3) s = '0' + s;
  return s.slice(-3);
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var version = readVersion_(ss);
  var problems = collectProblems_(ss, version);

  var first = problems.length ? problems[0] : null;
  var codes = problems.map(function (p) { return (p.ver || 'FR') + p.step + p.code; }).sort().join('|');
  var hash = checkHash_(KIT_CODE + version + KIT_VERSION + codes);
  var supportCode = first
    ? KIT_CODE + '-' + (first.ver || 'FR') + '-' + first.step + '-' + first.code + '-v' + KIT_VERSION + '-' + hash
    : KIT_CODE + '-' + version + '-00-0-E00-v' + KIT_VERSION + '-' + hash;

  var lines = [];
  lines.push('Website check-up report');
  lines.push('Kit ' + KIT_CODE + ', version ' + version + ', kit release ' + KIT_VERSION);
  lines.push('Run on ' + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MM/dd/yyyy'));
  lines.push('');
  if (!problems.length) {
    lines.push('All checks passed. Tabs, headings, and settings look right.');
  } else {
    lines.push(problems.length + ' problem(s) found, in the order they were checked:');
    problems.forEach(function (p, i) {
      lines.push((i + 1) + '. [' + p.code + '] step ' + KIT_CODE + '-' + (p.ver || 'FR') + '-' + p.step + '. ' + p.note);
    });
    lines.push('');
    lines.push('Look up each [E..] code in fixes.md.');
  }
  var report = lines.join('\n');

  var html = HtmlService.createHtmlOutput(
    '<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.4">' +
    '<p><b>Your support code</b></p>' +
    '<p style="font-size:18px;font-family:monospace;margin:4px 0 12px">' + supportCode + '</p>' +
    '<p>This report lists tab names, which column positions differ from the template, and whether settings are filled or empty. ' +
    'It does not include anything you typed into your cells, and nothing has been sent anywhere. ' +
    'If you want help, copy the code and the report below and send them with the step ID where you got stuck.</p>' +
    '<textarea readonly style="width:100%;height:190px;font-family:monospace;font-size:12px">' +
    report.replace(/&/g, '&amp;').replace(/</g, '&lt;') +
    '</textarea></div>'
  ).setWidth(520).setHeight(420);
  SpreadsheetApp.getUi().showModalDialog(html, 'Check-up result');
}
