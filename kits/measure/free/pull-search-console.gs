/**
 * Pull last month's Search Console numbers into this sheet (low-cost version, kit MM v0.1.0).
 * Read-only: it asks Google for numbers and writes rows to two tabs. It never changes Search Console.
 *
 * Needs, in this script project:
 *   Project Settings > "Show appsscript.json manifest file in editor" ticked, and
 *   oauthScopes in appsscript.json containing
 *     "https://www.googleapis.com/auth/webmasters.readonly" and "https://www.googleapis.com/auth/spreadsheets"
 *     and "https://www.googleapis.com/auth/script.external_request"
 * Config tab (column A key, column B value): site_url (sc-domain:example.org or https://www.example.org/)
 * Not tested against a live account when this kit was written. If it fails, see fixes.md E11 and E13.
 */
function pullSearchConsoleLastMonth() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var site = readConfig_(ss, 'site_url');
  if (!site) { throw new Error('Config site_url is empty (E03)'); }
  var now = new Date();
  var first = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  var last = new Date(now.getFullYear(), now.getMonth(), 0);
  var tz = Session.getScriptTimeZone();
  var start = Utilities.formatDate(first, tz, 'yyyy-MM-dd');
  var end = Utilities.formatDate(last, tz, 'yyyy-MM-dd');
  var month = start;

  var all = query_(site, {startDate: start, endDate: end, dimensions: ['query'], rowLimit: 50});
  var pages = query_(site, {startDate: start, endDate: end, dimensions: ['page'], rowLimit: 30});

  // Site-wide totals: add up the daily rows.
  var dayRows = query_(site, {startDate: start, endDate: end, dimensions: ['date'], rowLimit: 100}).rows || [];
  var clicks = 0, imps = 0, posWeighted = 0;
  dayRows.forEach(function (r) { clicks += r.clicks; imps += r.impressions; posWeighted += r.position * r.impressions; });
  var ctr = imps ? clicks / imps : '';
  var pos = imps ? posWeighted / imps : '';
  var traffic = ss.getSheetByName('Monthly traffic');
  // Columns: month, organic_sessions, organic_users, engaged_sessions, key_events, search_clicks, search_impressions, search_ctr, search_avg_position, data_through
  upsertTrafficGsc_(traffic, month, {6: clicks, 7: imps, 8: ctr, 9: pos, 10: end}, tz);

  var qs = ss.getSheetByName('Search queries');
  replaceMonthGsc_(qs, month, (all.rows || []).map(function (r) { return [month, r.keys[0], r.clicks, r.impressions, r.ctr, r.position, '']; }), [6], tz);
  var tp = ss.getSheetByName('Top pages');
  // Columns: month, page_url, organic_sessions, key_events, engagement_rate, search_clicks, search_impressions, search_position
  replaceMonthGsc_(tp, month, (pages.rows || []).map(function (r) { return [month, r.keys[0], '', '', '', r.clicks, r.impressions, r.position]; }), [2, 3, 4], tz);
  SpreadsheetApp.getUi().alert('Wrote Search Console rows for ' + start + ' to ' + end + '. Fill the GA4 columns with the GA4 pull or by hand.');
}

// Rerunning a month replaces that month's rows instead of adding a second copy.
function monthKeyGsc_(v, tz) {
  return (v instanceof Date) ? Utilities.formatDate(v, tz, 'yyyy-MM-dd') : String(v).trim();
}

// Monthly traffic: one row per month. Sets only this pull's columns (1-based col to value), creating the row if needed.
function upsertTrafficGsc_(sheet, month, cols, tz) {
  var rows = sheet.getDataRange().getValues();
  var at = -1;
  for (var i = 1; i < rows.length; i++) { if (monthKeyGsc_(rows[i][0], tz) === month) { at = i + 1; break; } }
  if (at < 0) {
    var blank = ['', '', '', '', '', '', '', '', '', ''];
    blank[0] = month;
    sheet.appendRow(blank);
    at = sheet.getLastRow();
  }
  Object.keys(cols).forEach(function (c) { sheet.getRange(at, Number(c)).setValue(cols[c]); });
}

// Write this month's new rows first, then retire the old ones. Values in keepCols (0-based) that a person
// typed on an old row with the same key (column B) carry over when the new row leaves them blank.
function replaceMonthGsc_(sheet, month, fresh, keepCols, tz) {
  var rows = sheet.getDataRange().getValues();
  var old = [], kept = {};
  for (var i = 1; i < rows.length; i++) {
    if (monthKeyGsc_(rows[i][0], tz) === month) { old.push(i + 1); kept[String(rows[i][1])] = rows[i]; }
  }
  fresh.forEach(function (row) {
    var prev = kept[String(row[1])];
    if (prev) { keepCols.forEach(function (c) { if (row[c] === '') { row[c] = prev[c]; } }); }
    sheet.appendRow(row);
  });
  for (var j = old.length - 1; j >= 0; j--) { sheet.deleteRow(old[j]); }
}

function query_(site, body) {
  var url = 'https://www.googleapis.com/webmasters/v3/sites/' + encodeURIComponent(site) + '/searchAnalytics/query';
  var res = UrlFetchApp.fetch(url, {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    headers: {Authorization: 'Bearer ' + ScriptApp.getOAuthToken()},
    payload: JSON.stringify(body)
  });
  if (res.getResponseCode() !== 200) {
    throw new Error('Search Console answered ' + res.getResponseCode() + ' (see fixes.md E13)');
  }
  return JSON.parse(res.getContentText());
}

function readConfig_(ss, key) {
  var sheet = ss.getSheetByName('Config');
  if (!sheet) { return ''; }
  var rows = sheet.getDataRange().getValues();
  for (var i = 0; i < rows.length; i++) { if (String(rows[i][0]).trim() === key) { return String(rows[i][1]).trim(); } }
  return '';
}
