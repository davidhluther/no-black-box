/**
 * Customer Research kit: check-up (Apps Script)
 * Adds a "Kit help" menu with "Run check-up". It tests that the expected tabs and
 * column headings exist and that the Config tab is filled in, then shows one
 * support code and an optional plain-text report.
 *
 * Privacy: the report lists tab names, which column positions differ, which
 * Config setting names are blank, and row counts. It never includes cell
 * contents, quotes, email addresses, passwords, or keys. The dialog shows the
 * exact report text before you decide to copy it.
 *
 * The line below asks Google for access to this one file only, not all your files.
 * @OnlyCurrentDoc
 */

var KIT = 'CR';
var VERSION = '0.1.0';
var VERSION_LABEL = 'FR'; // 'FR' for the free version, 'LC' if you added the low-cost files

// step = the printed step ID where that tab is created.
var REQUIRED_TABS = [
  { name: 'Config', step: 'CR-FR-01-2', code: 'E01', headers: ['key', 'value', 'note'] },
  { name: 'Sources', step: 'CR-FR-01-3', code: 'E02', headers: ['source_id', 'source_type', 'name_or_page', 'url', 'date_checked', 'how_many_read', 'notes'] },
  { name: 'Quotes', step: 'CR-FR-01-4', code: 'E03', headers: ['quote_id', 'date_collected', 'source_id', 'verbatim', 'who_said_it', 'what_it_is_about', 'customer_word_or_phrase', 'theme', 'sentiment', 'keep'] },
  { name: 'Themes', step: 'CR-FR-01-5', code: 'E04', headers: ['theme', 'plain_description', 'quote_count', 'example_quote_ids', 'customer_words', 'our_current_words', 'gap', 'action'] },
  { name: 'WordingTests', step: 'CR-FR-01-6', code: 'E05', headers: ['test_id', 'date', 'what_is_being_tested', 'version_label', 'wording', 'panel_reaction_summary', 'confusions_flagged', 'real_customers_planned', 'real_customer_result', 'decision'] }
];

// Only checked if the tab exists (low-cost version).
var OPTIONAL_TABS = [
  { name: 'Autocomplete', step: 'CR-LC-02-2', code: 'E06', headers: ['date_collected', 'seed_term', 'suggestion', 'kept'] },
  { name: 'RunLog', step: 'CR-LC-02-3', code: 'E07', headers: ['run_time', 'job', 'status', 'rows_added', 'message'] }
];

var REQUIRED_CONFIG_KEYS = ['organization_name', 'what_we_offer', 'who_we_serve', 'area_served', 'seed_terms'];
var CONFIG_STEP = 'CR-FR-02-1';
var CONFIG_CODE = 'E08';

// The only onOpen in the project. If autocomplete.gs is also installed
// (low-cost version), its menu is added here too.
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Kit help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
  if (typeof addPullMenu_ === 'function') { addPullMenu_(); }
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var lines = [];
  var failures = [];

  function fail(step, code, text) {
    failures.push({ step: step, code: code });
    lines.push('FAIL ' + code + ' (step ' + step + '): ' + text);
  }

  function checkTab(spec, optional) {
    var sheet = ss.getSheetByName(spec.name);
    if (!sheet) {
      if (optional) {
        lines.push('SKIP optional tab "' + spec.name + '" not present');
        return;
      }
      fail(spec.step, spec.code, 'tab "' + spec.name + '" is missing');
      return;
    }
    var width = spec.headers.length;
    var lastCol = Math.max(sheet.getLastColumn(), 1);
    var first = sheet.getRange(1, 1, 1, Math.max(width, lastCol)).getValues()[0];
    var badPositions = [];
    for (var i = 0; i < width; i++) {
      if (String(first[i]).replace(/^\s+|\s+$/g, '').toLowerCase() !== spec.headers[i]) {
        badPositions.push(i + 1);
      }
    }
    var dataRows = Math.max(sheet.getLastRow() - 1, 0);
    if (badPositions.length) {
      fail(spec.step, spec.code, 'tab "' + spec.name + '" has headings that differ at column position(s) ' + badPositions.join(', '));
    } else {
      lines.push('PASS tab "' + spec.name + '" headings match (' + dataRows + ' data rows)');
    }
  }

  REQUIRED_TABS.forEach(function (t) { checkTab(t, false); });
  OPTIONAL_TABS.forEach(function (t) { checkTab(t, true); });

  // Config cells: report which setting NAMES are blank, never the values.
  var cfg = ss.getSheetByName('Config');
  if (cfg) {
    var rows = cfg.getRange(1, 1, Math.max(cfg.getLastRow(), 1), 2).getValues();
    var values = {};
    rows.forEach(function (r) { values[String(r[0]).replace(/^\s+|\s+$/g, '')] = String(r[1]).replace(/^\s+|\s+$/g, ''); });
    var blanks = REQUIRED_CONFIG_KEYS.filter(function (k) { return !values[k]; });
    if (blanks.length) {
      fail(CONFIG_STEP, CONFIG_CODE, 'Config settings still blank: ' + blanks.join(', '));
    } else {
      lines.push('PASS Config settings are filled in');
    }
  }

  var first = failures.length ? failures[0] : null;
  var stepPart = first ? first.step : (KIT + '-' + VERSION_LABEL + '-00-0');
  var codePart = first ? first.code : 'E00';
  var hash = shortHash(lines.join('|'));
  var supportCode = stepPart + '-' + codePart + '-v' + VERSION + '-' + hash;

  var report = [
    'Kit: ' + KIT + '  Version: v' + VERSION,
    'Support code: ' + supportCode,
    'Result: ' + (failures.length ? failures.length + ' problem(s) found' : 'all checks passed'),
    ''
  ].concat(lines).join('\n');

  showReport(supportCode, report);
}

function shortHash(text) {
  var alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  var h = 7;
  for (var i = 0; i < text.length; i++) {
    h = (h * 31 + text.charCodeAt(i)) % 32768;
  }
  return alphabet.charAt(h % 32) + alphabet.charAt(Math.floor(h / 32) % 32) + alphabet.charAt(Math.floor(h / 1024) % 32);
}

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function showReport(supportCode, report) {
  var html = HtmlService.createHtmlOutput(
    '<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.4">' +
    '<p><b>Your support code</b></p>' +
    '<p style="font-size:18px"><code>' + escapeHtml(supportCode) + '</code></p>' +
    '<p>Optional report. This is everything that would be shared if you copy it. ' +
    'It lists tab names, column positions, setting names, and row counts. ' +
    'It contains no quotes, names, emails, passwords, or keys.</p>' +
    '<textarea style="width:100%;height:200px" readonly>' + escapeHtml(report) + '</textarea>' +
    '<p>To get help, send the support code and the step ID where you got stuck to the contact page in the guide.</p>' +
    '</div>'
  ).setWidth(520).setHeight(470);
  SpreadsheetApp.getUi().showModalDialog(html, 'Check-up');
}
