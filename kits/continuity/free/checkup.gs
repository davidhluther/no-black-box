/**
 * Continuity Kit check-up (Google Apps Script).
 *
 * Adds a Help menu with "Run check-up". It checks the structure of the
 * bus-test sheet only: the two tabs exist, the header rows match, the five
 * function names are in place, the answers are yes or no, and the score
 * formulas are still there. It counts things. It never reads, copies or
 * shows the sentences you typed in the sheet, so nothing about your
 * business can leave it.
 *
 * Output: one support code such as CK-FR-01-5-E04-v0.1.0-7KQ (kit and
 * version, the guide step where the first problem sits, the problem code,
 * the kit version, a three-character check) plus an optional plain-text
 * report you can read before you share it.
 */
var KIT = 'CK';
var VERSION = 'v0.1.0';

var BUSTEST_HEADERS = ['function', 'q1_written_down', 'q2_stranger_could_follow', 'q3_tested_by_someone_else',
  'score', 'target_score', 'if_you_vanished', 'what_breaks_first', 'next_step'];
var CHURN_HEADERS = ['name', 'your_value', 'example_value', 'used_value', 'basis'];
var FUNCTIONS = ['Money and billing', 'Operations and fulfillment', 'Customers and relationships',
  'Suppliers and tools', 'People and knowledge'];

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var results = [];
  function add(step, code, ok, note) { results.push({step: step, code: code, ok: ok, note: note}); }

  var bus = ss.getSheetByName('BusTest');
  var churn = ss.getSheetByName('Churn');
  add('CK-FR-01-2', 'E01', !!bus, 'Tab "BusTest" ' + (bus ? 'found' : 'missing or misspelled'));
  add('CK-FR-01-2', 'E01', !!churn, 'Tab "Churn" ' + (churn ? 'found' : 'missing or misspelled'));

  function headersOk(sh, want) {
    var got = sh.getRange(1, 1, 1, want.length).getValues()[0].map(function (v) { return String(v).trim().toLowerCase(); });
    return want.every(function (w, i) { return got[i] === w; });
  }
  if (bus) {
    add('CK-FR-01-2', 'E02', headersOk(bus, BUSTEST_HEADERS), 'BusTest header row ' + (headersOk(bus, BUSTEST_HEADERS) ? 'matches' : 'does not match the template'));
    var names = bus.getRange(2, 1, 5, 1).getValues().map(function (r) { return String(r[0]).trim(); });
    var namesOk = FUNCTIONS.every(function (f, i) { return names[i] === f; });
    add('CK-FR-01-2', 'E05', namesOk, 'The five function names ' + (namesOk ? 'are in place' : 'were changed or moved'));

    var answers = bus.getRange(2, 2, 5, 3).getValues();
    var blanks = 0, invalid = 0;
    answers.forEach(function (row) {
      var stop = false;
      row.forEach(function (v, i) {
        var s = String(v).trim().toLowerCase();
        if (s !== '' && s !== 'yes' && s !== 'no') invalid++;
        if (!stop) {
          if (s === '') blanks++;
          if (s !== 'yes') stop = true;
        }
      });
    });
    add('CK-FR-01-5', 'E04', invalid === 0, invalid + ' answer cells hold something other than yes or no');
    add('CK-FR-01-5', 'E03', blanks === 0, blanks + ' questions still need an answer');

    var scoreF = bus.getRange(2, 5, 5, 1).getFormulas().filter(function (r) { return r[0] === ''; }).length;
    add('CK-FR-01-7', 'E06', scoreF === 0, scoreF + ' score cells have lost their formula');
    var sumF = bus.getRange(8, 2, 6, 1).getFormulas().filter(function (r) { return r[0] === ''; }).length;
    add('CK-FR-01-7', 'E07', sumF === 0, sumF + ' summary cells have lost their formula');
  }
  if (churn) {
    add('CK-FR-01-2', 'E02', headersOk(churn, CHURN_HEADERS), 'Churn header row ' + (headersOk(churn, CHURN_HEADERS) ? 'matches' : 'does not match the template'));
  }
  showResult(results);
}

function showResult(results) {
  var first = null;
  results.forEach(function (r) { if (!r.ok && !first) first = r; });
  var step = first ? first.step : 'CK-FR-03-6';
  var code = first ? first.code : 'E00';
  var support = step + '-' + code + '-' + VERSION + '-' +
    checkChars(results.map(function (r) { return r.code + (r.ok ? '1' : '0'); }).join(''));

  var lines = ['Continuity Kit check-up ' + VERSION, 'Support code ' + support, ''];
  results.forEach(function (r) { lines.push((r.ok ? 'OK   ' : 'FIX  ') + r.code + ' ' + r.note); });
  lines.push('', 'This report lists only tab names, counts and pass or fail. It has no sentences from your sheet, no names, no passwords and no keys.');
  var report = lines.join('\n');

  var html = HtmlService.createHtmlOutput(
    '<p><b>Your support code</b></p><p style="font-size:16px"><code>' + support + '</code></p>' +
    '<p>' + (first ? 'The first thing to fix is ' + first.code + ' at step ' + first.step + '. Look it up in fixes.md.' : 'Everything checked out.') + '</p>' +
    '<p>Optional report. Read it first, then copy it if you want to share it.</p>' +
    '<textarea style="width:100%;height:220px" readonly>' + report.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</textarea>'
  ).setWidth(520).setHeight(420);
  SpreadsheetApp.getUi().showModalDialog(html, 'Check-up result');
}

function checkChars(s) {
  var h = 7;
  for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 46656;
  var t = h.toString(36).toUpperCase();
  while (t.length < 3) t = '0' + t;
  return t.slice(-3);
}
