/**
 * Measure what matters: check-up (kit MM, free version, v0.1.0)
 *
 * Adds a "Help" menu with "Run check-up". It looks at the STRUCTURE of this sheet only:
 * which tabs exist, whether each tab's header row matches, and whether the Config cells
 * are filled in. It never reads, shows or sends the contents of your data rows, and it
 * never shows what you typed into Config (only "filled" or "empty").
 *
 * It prints one support code, for example MM-FR-01-2-E02-v0.1.0-7KQ:
 *   MM-FR-01-2  the step of the first problem (kit, version, guide, step)
 *   E02         the problem code (see fixes.md)
 *   v0.1.0      kit version
 *   7KQ         a short fingerprint of the check result, so a helper can tell which checks passed
 * If nothing is wrong the code ends in E00.
 */
var KIT_VERSION = 'v0.1.0';

// Tab name -> expected header row (must match the CSV templates in this folder).
var EXPECTED_TABS = {
  'Monthly traffic': ['month', 'organic_sessions', 'organic_users', 'engaged_sessions', 'key_events', 'search_clicks', 'search_impressions', 'search_ctr', 'search_avg_position', 'data_through'],
  'Search queries': ['month', 'query', 'clicks', 'impressions', 'ctr', 'position', 'page'],
  'Top pages': ['month', 'page_url', 'organic_sessions', 'key_events', 'engagement_rate', 'search_clicks', 'search_impressions', 'search_position'],
  'AI referrals': ['month', 'ai_source', 'sessions', 'engaged_sessions', 'key_events', 'note'],
  'Flagged moves': ['month', 'measure', 'move', 'top_cause', 'grade', 'sources_checked', 'sources_agree', 'action', 'owner', 'due']
};
// Config tab: column A holds these keys, column B the value.
var CONFIG_KEYS = ['org_name', 'site_url', 'ga4_property_id', 'report_month'];

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Help').addItem('Run check-up', 'runCheckup').addToUi();
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var results = []; // {step, code, label, ok}

  // Step MM-FR-01-2: tabs exist and headers match.
  Object.keys(EXPECTED_TABS).forEach(function (name) {
    var sheet = ss.getSheetByName(name);
    if (!sheet) {
      results.push({step: 'MM-FR-01-2', code: 'E01', label: 'Tab "' + name + '": missing', ok: false});
      return;
    }
    var want = EXPECTED_TABS[name];
    var got = sheet.getRange(1, 1, 1, want.length).getValues()[0].map(function (v) { return String(v).trim(); });
    var same = want.every(function (h, i) { return got[i] === h; });
    results.push({step: 'MM-FR-01-2', code: 'E02', label: 'Tab "' + name + '": ' + (same ? 'headers match' : 'headers do not match'), ok: same});
  });

  // Step MM-FR-01-3: Config tab and cells.
  var config = ss.getSheetByName('Config');
  if (!config) {
    results.push({step: 'MM-FR-01-3', code: 'E01', label: 'Tab "Config": missing', ok: false});
  } else {
    var rows = config.getDataRange().getValues();
    var values = {};
    rows.forEach(function (r) { values[String(r[0]).trim()] = String(r[1]).trim(); });
    CONFIG_KEYS.forEach(function (k) {
      var filled = values[k] !== undefined && values[k] !== '';
      results.push({step: 'MM-FR-01-3', code: 'E03', label: 'Config "' + k + '": ' + (filled ? 'filled' : 'empty'), ok: filled});
    });
    var url = values['site_url'] || '';
    if (url) {
      var urlOk = /^(sc-domain:[a-z0-9.-]+|https?:\/\/[^ ]+\/)$/i.test(url);
      results.push({step: 'MM-FR-01-3', code: 'E27', label: 'Config "site_url": ' + (urlOk ? 'shape looks right' : 'shape looks wrong'), ok: urlOk});
    }
    var pid = values['ga4_property_id'] || '';
    if (pid) {
      var pidOk = /^\d{6,}$/.test(pid);
      results.push({step: 'MM-FR-01-3', code: 'E28', label: 'Config "ga4_property_id": ' + (pidOk ? 'shape looks right' : 'shape looks wrong'), ok: pidOk});
    }
  }

  var first = null;
  for (var i = 0; i < results.length; i++) { if (!results[i].ok) { first = results[i]; break; } }
  var fingerprint = hash3_(results.map(function (r) { return r.code + (r.ok ? '1' : '0'); }).join(''));
  var code = first
    ? first.step + '-' + first.code + '-' + KIT_VERSION + '-' + fingerprint
    : 'MM-FR-01-3-E00-' + KIT_VERSION + '-' + fingerprint;

  var report = 'Measure what matters check-up ' + KIT_VERSION + '\n' +
    'Support code: ' + code + '\n\n' +
    results.map(function (r) { return (r.ok ? 'ok     ' : 'PROBLEM ') + r.step + ' ' + r.code + ' ' + r.label; }).join('\n') +
    '\n\nThis report lists tab names, whether headers match, and whether Config cells are filled. ' +
    'It contains no cell contents, no passwords and no keys.';

  var ui = SpreadsheetApp.getUi();
  ui.alert('Check-up result',
    (first ? 'Something needs attention.' : 'Everything checked looks right.') + '\n\nSupport code (copy this):\n' + code +
    '\n\nWhat the optional report would share is shown on the next screen.', ui.ButtonSet.OK);
  ui.alert('Optional plain-text report (select all, copy, paste into your message)', report, ui.ButtonSet.OK);
}

// Three characters, 0-9 and A-Z, from a simple sum. Not secret; just a fingerprint.
function hash3_(s) {
  var n = 7;
  for (var i = 0; i < s.length; i++) { n = (n * 31 + s.charCodeAt(i)) % 46656; }
  var out = n.toString(36).toUpperCase();
  while (out.length < 3) { out = '0' + out; }
  return out;
}
