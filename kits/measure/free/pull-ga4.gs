/**
 * Pull last month's GA4 numbers into this sheet (low-cost version, kit MM v0.1.0).
 * Read-only. Needs the "Google Analytics Data API" advanced service switched on:
 *   Apps Script editor > Services (the + beside "Services") > Google Analytics Data API > Add.
 * Config tab: ga4_property_id (digits only, from GA4 Admin > Property details).
 * Writes monthly totals to "Monthly traffic" (one row per month; a rerun updates only the GA4 columns)
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
  upsertTrafficGa4_(ss.getSheetByName('Monthly traffic'), start, {2: m[0], 3: m[1], 4: m[2], 5: m[3], 10: end}, tz);

  // AI sources by referring site.
  var ai = AnalyticsData.Properties.runReport({
    dateRanges: [{startDate: start, endDate: end}],
    dimensions: [{name: 'sessionSource'}],
    metrics: [{name: 'sessions'}, {name: 'engagedSessions'}, {name: 'keyEvents'}],
    dimensionFilter: {filter: {fieldName: 'sessionSource', stringFilter: {matchType: 'FULL_REGEXP', value: AI_SOURCE_REGEX}}},
    limit: 50
  }, property);
  var sheet = ss.getSheetByName('AI referrals');
  replaceMonthGa4_(sheet, start, (ai.rows || []).map(function (r) {
    return [start, r.dimensionValues[0].value, Number(r.metricValues[0].value), Number(r.metricValues[1].value), Number(r.metricValues[2].value), 'floor, not total'];
  }), [], tz);
  SpreadsheetApp.getUi().alert('Wrote GA4 rows for ' + start + ' to ' + end + '.');
}

// Rerunning a month replaces that month's rows instead of adding a second copy.
function monthKeyGa4_(v, tz) {
  return (v instanceof Date) ? Utilities.formatDate(v, tz, 'yyyy-MM-dd') : String(v).trim();
}

// Monthly traffic: one row per month. Sets only this pull's columns (1-based col to value), creating the row if needed.
function upsertTrafficGa4_(sheet, month, cols, tz) {
  var rows = sheet.getDataRange().getValues();
  var at = -1;
  for (var i = 1; i < rows.length; i++) { if (monthKeyGa4_(rows[i][0], tz) === month) { at = i + 1; break; } }
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
function replaceMonthGa4_(sheet, month, fresh, keepCols, tz) {
  var rows = sheet.getDataRange().getValues();
  var old = [], kept = {};
  for (var i = 1; i < rows.length; i++) {
    if (monthKeyGa4_(rows[i][0], tz) === month) { old.push(i + 1); kept[String(rows[i][1])] = rows[i]; }
  }
  fresh.forEach(function (row) {
    var prev = kept[String(row[1])];
    if (prev) { keepCols.forEach(function (c) { if (row[c] === '') { row[c] = prev[c]; } }); }
    sheet.appendRow(row);
  });
  for (var j = old.length - 1; j >= 0; j--) { sheet.deleteRow(old[j]); }
}

function readConfigGa4_(ss, key) {
  var sheet = ss.getSheetByName('Config');
  if (!sheet) { return ''; }
  var rows = sheet.getDataRange().getValues();
  for (var i = 0; i < rows.length; i++) { if (String(rows[i][0]).trim() === key) { return String(rows[i][1]).trim(); } }
  return '';
}
