/**
 * Pull last month's GA4 numbers into this sheet (low-cost version, kit MM v0.1.0).
 * Read-only. Needs the "Google Analytics Data API" advanced service switched on:
 *   Apps Script editor > Services (the + beside "Services") > Google Analytics Data API > Add.
 * Config tab: ga4_property_id (digits only, from GA4 Admin > Property details).
 * Writes monthly totals to "Monthly traffic" (it adds a new row; fill search columns with the Search Console pull)
 * and AI sources to "AI referrals". The AI rows rely on a custom channel group; see the setup guide.
 * Not tested against a live account when this kit was written. See fixes.md E12.
 */
var AI_SOURCE_REGEX = '(^|\\.)(chatgpt\\.com|chat\\.openai\\.com|perplexity\\.ai|copilot\\.microsoft\\.com|gemini\\.google\\.com|claude\\.ai|you\\.com|poe\\.com|phind\\.com|chat\\.mistral\\.ai|deepseek\\.com|grok\\.com|meta\\.ai)$';

function pullGa4LastMonth() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var pid = readConfigGa4_(ss, 'ga4_property_id');
  if (!pid) { throw new Error('Config ga4_property_id is empty (E03)'); }
  var tz = Session.getScriptTimeZone();
  var now = new Date();
  var first = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  var last = new Date(now.getFullYear(), now.getMonth(), 0);
  var start = Utilities.formatDate(first, tz, 'yyyy-MM-dd');
  var end = Utilities.formatDate(last, tz, 'yyyy-MM-dd');
  var property = 'properties/' + pid;

  // Organic search totals.
  var organic = AnalyticsData.Properties.runReport({
    dateRanges: [{startDate: start, endDate: end}],
    metrics: [{name: 'sessions'}, {name: 'totalUsers'}, {name: 'engagedSessions'}, {name: 'keyEvents'}],
    dimensionFilter: {filter: {fieldName: 'sessionDefaultChannelGroup', stringFilter: {matchType: 'EXACT', value: 'Organic Search'}}}
  }, property);
  var m = (organic.rows && organic.rows[0]) ? organic.rows[0].metricValues.map(function (v) { return Number(v.value); }) : ['', '', '', ''];
  ss.getSheetByName('Monthly traffic').appendRow([start, m[0], m[1], m[2], m[3], '', '', '', '', end]);

  // AI sources by referring site.
  var ai = AnalyticsData.Properties.runReport({
    dateRanges: [{startDate: start, endDate: end}],
    dimensions: [{name: 'sessionSource'}],
    metrics: [{name: 'sessions'}, {name: 'engagedSessions'}, {name: 'keyEvents'}],
    dimensionFilter: {filter: {fieldName: 'sessionSource', stringFilter: {matchType: 'FULL_REGEXP', value: AI_SOURCE_REGEX}}},
    limit: 50
  }, property);
  var sheet = ss.getSheetByName('AI referrals');
  (ai.rows || []).forEach(function (r) {
    sheet.appendRow([start, r.dimensionValues[0].value, Number(r.metricValues[0].value), Number(r.metricValues[1].value), Number(r.metricValues[2].value), 'floor, not total']);
  });
  SpreadsheetApp.getUi().alert('Added GA4 rows for ' + start + ' to ' + end + '.');
}

function readConfigGa4_(ss, key) {
  var sheet = ss.getSheetByName('Config');
  if (!sheet) { return ''; }
  var rows = sheet.getDataRange().getValues();
  for (var i = 0; i < rows.length; i++) { if (String(rows[i][0]).trim() === key) { return String(rows[i][1]).trim(); } }
  return '';
}
