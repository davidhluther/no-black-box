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
  traffic.appendRow([month, '', '', '', '', clicks, imps, ctr, pos, end]);

  var qs = ss.getSheetByName('Search queries');
  (all.rows || []).forEach(function (r) { qs.appendRow([month, r.keys[0], r.clicks, r.impressions, r.ctr, r.position, '']); });
  var tp = ss.getSheetByName('Top pages');
  // Columns: month, page_url, organic_sessions, key_events, engagement_rate, search_clicks, search_impressions, search_position
  (pages.rows || []).forEach(function (r) { tp.appendRow([month, r.keys[0], '', '', '', r.clicks, r.impressions, r.position]); });
  SpreadsheetApp.getUi().alert('Added Search Console rows for ' + start + ' to ' + end + '. Fill the GA4 columns with the GA4 pull or by hand.');
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
