/**
 * Idea to Live Post kit: pull Search Console data into a tab (low-cost version).
 * Reads the Setup tab key "search_console_property" and writes the last 28 days of
 * page + query rows to a "SearchData" tab. Read-only against Google: it only asks
 * for data. Failures are written to the "Log" tab.
 *
 * Needs these permissions in appsscript.json (see setup guide IP-LC-03):
 *   https://www.googleapis.com/auth/spreadsheets
 *   https://www.googleapis.com/auth/script.external_request
 *   https://www.googleapis.com/auth/webmasters.readonly
 *
 * Status: written for this kit and not yet tested against a live account in the
 * build that produced it. Run it on a small test first.
 */
function addSearchMenu() {
  SpreadsheetApp.getUi().createMenu('Search data')
    .addItem('Pull last 28 days', 'pullSearchData')
    .addItem('Pull every Monday morning', 'installTrigger')
    .addToUi();
}

function setupValue_(ss, key) {
  var sheet = ss.getSheetByName('Setup');
  if (!sheet) { return ''; }
  var rows = sheet.getDataRange().getValues();
  for (var i = 1; i < rows.length; i++) {
    if (String(rows[i][0]).trim() === key) { return String(rows[i][1]).trim(); }
  }
  return '';
}

function log_(ss, status, detail) {
  var log = ss.getSheetByName('Log') || ss.insertSheet('Log');
  if (log.getLastRow() === 0) { log.appendRow(['when', 'what', 'status', 'detail']); }
  log.appendRow([new Date(), 'pullSearchData', status, String(detail || '').substring(0, 300)]);
}

function pullSearchData() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var property = setupValue_(ss, 'search_console_property');
  if (!property) {
    log_(ss, 'FAILED', 'search_console_property is empty on the Setup tab');
    SpreadsheetApp.getUi().alert('Fill in search_console_property on the Setup tab first (fix E10).');
    return;
  }
  var tz = Session.getScriptTimeZone();
  var end = new Date(Date.now() - 3 * 24 * 3600 * 1000);   // recent days are incomplete
  var start = new Date(end.getTime() - 27 * 24 * 3600 * 1000);
  var body = {
    startDate: Utilities.formatDate(start, tz, 'yyyy-MM-dd'),
    endDate: Utilities.formatDate(end, tz, 'yyyy-MM-dd'),
    dimensions: ['page', 'query'],
    rowLimit: 1000
  };
  var url = 'https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent(property) + '/searchAnalytics/query';
  try {
    var resp = UrlFetchApp.fetch(url, {
      method: 'post',
      contentType: 'application/json',
      headers: {Authorization: 'Bearer ' + ScriptApp.getOAuthToken()},
      payload: JSON.stringify(body),
      muteHttpExceptions: true
    });
    var code = resp.getResponseCode();
    if (code !== 200) { throw new Error('HTTP ' + code + ' (see fix E11)'); }
    var rows = JSON.parse(resp.getContentText()).rows || [];
    var sheet = ss.getSheetByName('SearchData') || ss.insertSheet('SearchData');
    sheet.clear();
    sheet.appendRow(['date_pulled', 'page', 'query', 'clicks', 'impressions', 'ctr', 'position']);
    var today = Utilities.formatDate(new Date(), tz, 'MM/dd/yyyy');
    var out = rows.map(function (r) {
      return [today, gscLiteral_(r.keys[0]), gscLiteral_(r.keys[1]), r.clicks, r.impressions, r.ctr, r.position];
    });
    if (out.length) { sheet.getRange(2, 1, out.length, 7).setValues(out); }
    log_(ss, out.length ? 'ok' : 'empty', out.length + ' row(s)');
  } catch (e) {
    log_(ss, 'FAILED', e.message);
    SpreadsheetApp.getUi().alert('The pull failed. See the Log tab and fix E11.');
  }
}

/** Keeps search text as plain text: a query starting with =, +, - or @ would otherwise make a formula. */
function gscLiteral_(v) {
  return (typeof v === 'string' && /^[=+\-@]/.test(v)) ? "'" + v : v;
}

function installTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'pullSearchData') { ScriptApp.deleteTrigger(t); }
  });
  ScriptApp.newTrigger('pullSearchData').timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(6).create();
  SpreadsheetApp.getUi().alert('Done. Search data will be pulled every Monday morning. A Monday with no new Log row means the schedule failed; check it.');
}
