/**
 * Owner's Numbers check-up (Google Apps Script).
 *
 * Adds a Kit help menu with "Run check-up". It checks the structure of the
 * sheet only: tab names, header rows, whether the Settings dates are real
 * dates, whether Bank rows have a known category, and whether result cells
 * show an error. It counts things. It never reads, copies or shows the
 * words or numbers inside your cells, so no sales, bank, client or staff
 * details can leave the sheet.
 *
 * Output: one support code such as ON-FR-02-6-E07-v0.1.0-7KQ
 * (kit and version, the guide step where the first problem sits, the
 * problem code, the kit version, a three-character check) plus an optional
 * plain-text report you can read before you share it.
 *
 * The line below asks Google for access to this one file only, not all your files.
 * @OnlyCurrentDoc
 */
var KIT = 'ON';
var VERSION = 'v0.1.0';

var TABS = {
  Settings: ['name', 'your_value', 'example_value', 'used_value', 'basis'],
  Sales: ['date', 'item', 'category', 'quantity', 'net_sales', 'client_id'],
  Bank: ['date', 'description', 'amount', 'category'],
  Bookings: ['date', 'service', 'staff', 'booked_minutes', 'status', 'client_id', 'price'],
  Scorecard: null,
  Metrics: ['metric', 'value', 'basis', 'plain reading']
};

var BANK_CATEGORIES = ['sales_deposit', 'other_income', 'cogs', 'supplies', 'payroll', 'rent',
  'utilities', 'software', 'insurance', 'marketing', 'loan_payment', 'tax', 'other_fixed',
  'other_variable', 'owner_draw', 'transfer'];

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Kit help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
  // Only present when export-csv.gs is also in this project (low cost version).
  if (typeof saveCsvToDrive === 'function') {
    SpreadsheetApp.getUi().createMenu('Owner\'s Numbers')
      .addItem('Save data tabs as CSV in Drive', 'saveCsvToDrive')
      .addToUi();
  }
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var results = []; // {step, code, ok, note}
  function add(step, code, ok, note) { results.push({step: step, code: code, ok: ok, note: note}); }

  // 1. Tabs exist
  var tabs = {};
  Object.keys(TABS).forEach(function (name) {
    var sh = ss.getSheetByName(name);
    tabs[name] = sh;
    add('ON-FR-01-3', 'E01', !!sh, 'Tab "' + name + '" ' + (sh ? 'found' : 'missing or misspelled'));
  });

  // 2. Header rows
  ['Settings', 'Sales', 'Bank', 'Bookings', 'Metrics'].forEach(function (name) {
    var sh = tabs[name];
    if (!sh) return;
    var want = TABS[name];
    var got = sh.getRange(1, 1, 1, want.length).getValues()[0].map(function (v) {
      return String(v).trim().toLowerCase();
    });
    var ok = want.every(function (w, i) { return got[i] === w; });
    add(name === 'Settings' ? 'ON-FR-03-1' : (name === 'Metrics' ? 'ON-FR-01-3' : 'ON-FR-02-4'), 'E02', ok,
      name + ' header row ' + (ok ? 'matches' : 'does not match the template'));
  });

  // 3. Settings
  var st = tabs.Settings;
  if (st) {
    var name = String(st.getRange('B2').getValue()).trim();
    add('ON-FR-03-1', 'E04', name !== '', 'Business name ' + (name !== '' ? 'is filled' : 'is blank'));
    var s3 = st.getRange('B3').getValue(), s4 = st.getRange('B4').getValue();
    var datesOk = (s3 instanceof Date) && (s4 instanceof Date) && s3 <= s4;
    add('ON-FR-03-1', 'E03', datesOk, 'Month start and end ' + (datesOk ? 'are real dates' : 'are missing, out of order or text'));
    var formulas = st.getRange('D5:E29').getFormulas();
    var missing = 0;
    formulas.forEach(function (r) { r.forEach(function (f) { if (!f) missing++; }); });
    add('ON-FR-03-7', 'E13', missing === 0, 'Settings formulas in D5:E29 ' + (missing === 0 ? 'present' : missing + ' cells have no formula'));
    if (datesOk) {
      ['Sales', 'Bank'].forEach(function (n) {
        var sh = tabs[n];
        if (!sh || sh.getLastRow() < 2) return;
        var vals = sh.getRange(2, 1, sh.getLastRow() - 1, 1).getValues();
        var inMonth = vals.filter(function (r) { return r[0] instanceof Date && r[0] >= s3 && r[0] <= s4; }).length;
        add('ON-FR-03-2', 'E12', inMonth > 0, n + ': ' + inMonth + ' rows fall inside the month');
      });
    }
  }

  // 4. Data tabs
  ['Sales', 'Bank'].forEach(function (n) {
    var sh = tabs[n];
    if (!sh) return;
    var rows = Math.max(0, sh.getLastRow() - 1);
    add(n === 'Sales' ? 'ON-FR-02-4' : 'ON-FR-02-5', n === 'Sales' ? 'E05' : 'E06', rows > 0, n + ' has ' + rows + ' data rows');
    if (rows > 0) {
      var dates = sh.getRange(2, 1, rows, 1).getValues();
      var text = dates.filter(function (r) { return r[0] !== '' && !(r[0] instanceof Date); }).length;
      add('ON-FR-02-8', 'E09', text === 0, n + ': ' + text + ' dates are stored as text');
    }
  });
  var bk = tabs.Bookings;
  if (bk) {
    var br = Math.max(0, bk.getLastRow() - 1);
    add('ON-FR-02-7', 'E11', br > 0, 'Bookings has ' + br + ' rows' + (br > 0 ? '' : ' (customer and capacity numbers will stay empty)'));
  }
  var bank = tabs.Bank;
  if (bank && bank.getLastRow() > 1) {
    var cats = bank.getRange(2, 4, bank.getLastRow() - 1, 1).getValues();
    var blank = 0, unknown = 0;
    cats.forEach(function (r) {
      var c = String(r[0]).trim();
      if (c === '') blank++;
      else if (BANK_CATEGORIES.indexOf(c) < 0) unknown++;
    });
    add('ON-FR-02-6', 'E07', blank === 0, blank + ' bank rows have no category');
    add('ON-FR-02-6', 'E08', unknown === 0, unknown + ' bank rows use a category that is not on the list');
  }

  // 5. Result tabs: count error cells (values are never read out)
  [['Scorecard', 'E10'], ['Metrics', 'E14']].forEach(function (p) {
    var sh = tabs[p[0]];
    if (!sh) return;
    var rng = sh.getDataRange().getDisplayValues();
    var bad = 0;
    rng.forEach(function (r) { r.forEach(function (v) { if (/^#(N\/A|VALUE!|REF!|NAME\?|DIV\/0!|ERROR!|NUM!)/.test(v)) bad++; }); });
    add('ON-FR-03-7', p[1], bad === 0, p[0] + ' shows ' + bad + ' error cells');
  });

  showResult(results);
}

function showResult(results) {
  var first = null;
  results.forEach(function (r) { if (!r.ok && r.code !== 'E11' && !first) first = r; });
  var step = first ? first.step : 'ON-FR-04-6';
  var code = first ? first.code : 'E00';
  var base = step + '-' + code + '-' + VERSION;
  var support = base + '-' + checkChars(results.map(function (r) { return r.code + (r.ok ? '1' : '0'); }).join(''));

  var lines = ['Owner\'s Numbers check-up ' + VERSION, 'Support code ' + support, ''];
  results.forEach(function (r) {
    lines.push((r.ok ? 'OK   ' : 'FIX  ') + r.code + ' ' + r.note);
  });
  lines.push('', 'This report lists only tab names, counts and pass or fail. It has no cell contents, names, amounts, passwords or keys.');
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
