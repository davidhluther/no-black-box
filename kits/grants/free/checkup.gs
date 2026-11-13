/**
 * Grants kit check-up (free version). Adds a "Kit help" menu with "Run check-up".
 *
 * What it does
 *   Looks at the SHAPE of this spreadsheet: are the expected tabs there, are the column
 *   headings right, are the setup cells filled in, do the formulas run. It then shows
 *   one short support code, such as GR-FR-01-4-E02-v0.1.0-7KQ, and an optional plain-text
 *   report you can copy.
 *
 * What it never does
 *   - It never reads or reports what is IN your cells (no funder names, amounts, donor
 *     or client data, names, emails, addresses, the spreadsheet's own title, or file names).
 *     It only counts rows and compares fixed template headings.
 *   - It never sends anything anywhere. There is no email, web request or upload in this
 *     file. You copy the code and report yourself, and you can read them first.
 *   - It never changes your sheet.
 *
 * Support code format
 *   GR-FR-<guide>-<step>-<problem code>-v<kit version>-<check>
 *   guide and step: where the first problem belongs in the setup guides
 *   problem code:   E01, E02 and so on, listed in the kit's fixes.md (E00 means all clear)
 *   check:          three characters made from the other parts, so a typo is easy to spot.
 *                   Method: take the text "<guide>-<step>|<problem code>|<version>", for
 *                   example "01-4|E02|0.1.0". Then h = 0; for each character c:
 *                   h = (h * 31 + charCode(c)) mod 46656; write h in base 36, capitals,
 *                   padded to three characters.
 *
 * To install, follow GR-FR-02 in the kit's setup folder.
 *
 * @OnlyCurrentDoc
 */

var KIT = {
  code: 'GR',
  version: '0.1.0',
  tabs: {
    Settings:   { header: ['Setting', 'Value', 'What it is'], step: 'GR-FR-01-3' },
    Pipeline:   { header: ['Funder', 'Program or purpose', 'Request ($)', 'Status', 'Submitted', 'Decision date', 'Award ($)', 'Eligible (Y or N)', 'Mission fit (1-5)', 'Geography fit (1-5)', 'Fund-area fit (1-5)', 'Relationship (1-5)', 'Reporting ease (1-5)', 'Chance of winning (%)', 'Effort (hours)', 'Deadline', 'Next step', 'Notes and source', 'Funder link', 'Tier', 'Fit (out of 25)', 'Dollars per hour'], step: 'GR-FR-01-4' },
    Funders:    { header: ['Funder', 'EIN', 'City and state', 'Type', 'Tier (1, 2 or 3)', 'Status', 'Our relationship', 'Where we checked', 'Geography rule', 'Typical award ($)', 'Suggested ask ($)', 'Giving priorities (their words)', 'How to apply', 'Deadline or cycle', 'Evidence of local giving', 'Funder website', 'Confidence (verified, secondary or unverified)', 'Date checked', 'Next step'], step: 'GR-FR-01-5' },
    Claims:     { header: ['ID', 'Claim', 'Value', 'As of', 'Source', 'Status'], step: 'GR-FR-01-6' },
    Dashboard:  { header: ['Measure', 'Value', 'How it is figured'], step: 'GR-FR-01-7' },
    Rubric:     { header: ['Topic', 'Rule'], step: 'GR-FR-01-8' },
    DraftCheck: { header: [], step: 'GR-FR-01-9' }
  },
  tabOrder: ['Settings', 'Pipeline', 'Funders', 'Claims', 'Dashboard', 'Rubric', 'DraftCheck'],
  settingsLabels: [
    'Setting', 'Organization short name', 'Legal name', 'EIN', 'Mailing address', 'Website address',
    'Grants contact name', 'Grants contact email', 'Service area', 'Tier 1 minimum request ($)',
    'Tier 2 minimum request ($)', 'Planned grant income this fiscal year ($)',
    'This fiscal year started on (mm/dd/yyyy)', 'Kit version'
  ],
  // Settings rows (1-based) that must be filled in.
  requiredSettingRows: [2, 3, 4, 7, 8, 10, 11, 13],
  statuses: ['Prospect', 'LOI Submitted', 'Submitted', 'Pending Decision', 'Awarded', 'Awarded-Reduced',
             'Declined', 'Not Pursued', 'Outcome Unknown', 'Closed'],
  enterSettingsStep: 'GR-FR-01-11',
  statusStep: 'GR-FR-03-4',
  claimsStep: 'GR-FR-04-2',
  okStep: 'GR-FR-02-7'
};

function onOpen() {
  var menu = SpreadsheetApp.getUi()
    .createMenu('Kit help')
    .addItem('Run check-up', 'runCheckup');
  // The optional draft checker (draft-check.gs) adds its own item when it is installed.
  if (typeof addDraftMenuItem_ === 'function') {
    addDraftMenuItem_(menu);
  }
  menu.addToUi();
}

function runCheckup() {
  var result = collectChecks_(SpreadsheetApp.getActiveSpreadsheet());
  showResult_(result);
}

/** Pure helpers (also used by the tests that ship with the kit's maintainers). */

function hash3_(text) {
  var h = 0;
  for (var i = 0; i < text.length; i++) {
    h = (h * 31 + text.charCodeAt(i)) % 46656;
  }
  var s = h.toString(36).toUpperCase();
  while (s.length < 3) { s = '0' + s; }
  return s;
}

function supportCode_(step, problem, version) {
  var parts = step + '|' + problem + '|' + version;
  return step + '-' + problem + '-v' + version + '-' + hash3_(parts);
}

/** Reads a block of display text, clamped to the sheet's size and padded with empty text. */
function display_(sheet, row, col, numRows, numCols) {
  var maxR = sheet.getMaxRows();
  var maxC = sheet.getMaxColumns();
  var out = [];
  for (var r = 0; r < numRows; r++) {
    var line = [];
    for (var c = 0; c < numCols; c++) { line.push(''); }
    out.push(line);
  }
  var rr = Math.min(numRows, maxR - row + 1);
  var cc = Math.min(numCols, maxC - col + 1);
  if (rr < 1 || cc < 1) { return out; }
  var got = sheet.getRange(row, col, rr, cc).getDisplayValues();
  for (var i = 0; i < rr; i++) { for (var j = 0; j < cc; j++) { out[i][j] = got[i][j]; } }
  return out;
}

function sameRow_(actual, expected) {
  if (actual.length < expected.length) { return false; }
  for (var i = 0; i < expected.length; i++) {
    if (String(actual[i]).replace(/^\s+|\s+$/g, '') !== expected[i]) { return false; }
  }
  return true;
}

function looksLikeError_(text) {
  return /^#(REF|VALUE|N\/A|NAME|DIV\/0|NUM|ERROR)/i.test(text) || /^Err:/i.test(text);
}

function parseNumber_(text) {
  var t = String(text).replace(/[$,\s]/g, '');
  if (t === '' || isNaN(Number(t))) { return null; }
  return Number(t);
}

/**
 * Runs every check. Returns { failures: [...], notes: [...], lines: [...], code: '...' }.
 * Each failure is { step, code, what } where `what` is plain words with no cell contents.
 */
function collectChecks_(ss) {
  var failures = [];
  var lines = [];
  var notes = [];
  var present = {};

  function fail(step, code, what) {
    failures.push({ step: step, code: code, what: what });
    lines.push('FAIL ' + code + ' (step ' + step + '): ' + what);
  }
  function pass(what) { lines.push('ok   ' + what); }

  // 1 and 2: tabs and headings, in tab order so the first failure follows the guide.
  KIT.tabOrder.forEach(function (name) {
    var spec = KIT.tabs[name];
    var sheet = ss.getSheetByName(name);
    if (!sheet) {
      fail(spec.step, 'E01', 'tab "' + name + '" is missing');
      return;
    }
    present[name] = sheet;
    if (name === 'DraftCheck') {
      var hdr5 = display_(sheet, 5, 1, 1, 3)[0];
      if (!sameRow_(hdr5, ['Number found', 'Matches your Claims tab?', 'Claim IDs'])) {
        fail(spec.step, 'E02', 'tab "DraftCheck" result headings in row 5 differ from the template');
      } else { pass('tab DraftCheck found, headings match'); }
      return;
    }
    var width = spec.header.length;
    var head = display_(sheet, 1, 1, 1, width)[0];
    if (!sameRow_(head, spec.header)) {
      fail(spec.step, 'E02', 'tab "' + name + '" row 1 headings differ from the template (first mismatch is not shown)');
    } else { pass('tab ' + name + ' found, headings match'); }
  });

  // 3: Settings labels still where the formulas expect them.
  if (present.Settings) {
    var labels = display_(present.Settings, 1, 1, KIT.settingsLabels.length, 1);
    var moved = false;
    for (var i = 0; i < KIT.settingsLabels.length; i++) {
      if (String(labels[i][0]).replace(/^\s+|\s+$/g, '') !== KIT.settingsLabels[i]) { moved = true; }
    }
    if (moved) {
      fail(KIT.tabs.Settings.step, 'E03', 'Settings rows were moved, inserted or renamed; formulas read fixed rows');
    } else { pass('Settings rows are in the expected places'); }
  }

  // 4: formulas run (no error values), looking only at the shape of the display text.
  if (present.Pipeline) {
    var calc = display_(present.Pipeline, 1, 20, 1, 3)[0];
    var bad = false;
    for (var c = 0; c < 3; c++) { if (looksLikeError_(String(calc[c]))) { bad = true; } }
    if (bad || !sameRow_(calc, ['Tier', 'Fit (out of 25)', 'Dollars per hour'])) {
      fail(KIT.tabs.Pipeline.step, 'E04', 'the calculated columns T to V on Pipeline are missing or show an error');
    } else { pass('Pipeline calculated columns run'); }
  }
  if (present.Dashboard) {
    var vals = display_(present.Dashboard, 2, 2, 16, 1);
    var errs = 0;
    for (var r = 0; r < vals.length; r++) { if (looksLikeError_(String(vals[r][0]))) { errs++; } }
    if (errs > 0) {
      fail(KIT.tabs.Dashboard.step, 'E04', errs + ' Dashboard value(s) show a formula error');
    } else { pass('Dashboard formulas run'); }
  }

  // 5 to 8: setup cells in Settings.
  if (present.Settings) {
    var cells = display_(present.Settings, 1, 2, KIT.settingsLabels.length, 1);
    var empty = 0;
    KIT.requiredSettingRows.forEach(function (row) {
      if (String(cells[row - 1][0]).replace(/\s/g, '') === '') { empty++; }
    });
    if (empty > 0) {
      fail(KIT.enterSettingsStep, 'E05', empty + ' required Settings cell(s) are still empty');
    } else { pass('required Settings cells are filled'); }

    var ein = String(cells[3][0]).replace(/\D/g, '');
    if (String(cells[3][0]).replace(/\s/g, '') !== '' && ein.length !== 9) {
      fail(KIT.enterSettingsStep, 'E06', 'the EIN cell does not hold nine digits');
    }

    var t1 = parseNumber_(cells[9][0]);
    var t2 = parseNumber_(cells[10][0]);
    if (t1 === null || t2 === null || t1 <= t2) {
      fail(KIT.enterSettingsStep, 'E07', 'the Tier 1 and Tier 2 minimums must be numbers with Tier 1 larger');
    }

    var fy = String(cells[12][0]).replace(/\s/g, '');
    if (fy !== '' && !/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(fy)) {
      fail(KIT.enterSettingsStep, 'E08', 'the fiscal-year start is not typed as a date like 07/01/2026');
    }

    if (String(cells[13][0]).replace(/\s/g, '') !== KIT.version) {
      fail(KIT.tabs.Settings.step, 'E14', 'the Kit version cell does not match this check-up (' + KIT.version + ')');
    }
  }

  // 10: status words the Dashboard counts. Counts only.
  if (present.Pipeline) {
    var last = present.Pipeline.getLastRow();
    if (last >= 2) {
      var st = display_(present.Pipeline, 2, 4, last - 1, 1);
      var unknown = 0, filled = 0;
      for (var k = 0; k < st.length; k++) {
        var s = String(st[k][0]).replace(/^\s+|\s+$/g, '');
        if (s !== '') {
          filled++;
          if (KIT.statuses.indexOf(s) === -1) { unknown++; }
        }
      }
      notes.push('Pipeline rows with a status: ' + filled);
      if (unknown > 0) {
        fail(KIT.statusStep, 'E12', unknown + ' Pipeline row(s) use a Status word the Dashboard does not count');
      } else { pass('Pipeline status words are all recognized'); }
    }
  }

  // 11: claims marked verified need a source. Counts only.
  if (present.Claims) {
    var lastC = present.Claims.getLastRow();
    if (lastC >= 2) {
      var rows = display_(present.Claims, 2, 5, lastC - 1, 2);
      var noSource = 0, total = 0;
      for (var m = 0; m < rows.length; m++) {
        var stat = String(rows[m][1]).toLowerCase();
        var src = String(rows[m][0]).replace(/\s/g, '');
        if (stat.indexOf('verified') === 0 || stat.indexOf('source-verified') === 0 || stat.indexOf('external-verified') === 0) {
          total++;
          if (src === '') { noSource++; }
        }
      }
      notes.push('Claims marked verified: ' + total);
      if (noSource > 0) {
        fail(KIT.claimsStep, 'E13', noSource + ' verified claim(s) have no Source');
      } else { pass('every verified claim has a source'); }
    }
  }

  // Extra context that is safe to share: counts and spreadsheet settings only.
  notes.push('Tabs found: ' + Object.keys(present).length + ' of ' + KIT.tabOrder.length);
  try {
    notes.push('Spreadsheet locale: ' + ss.getSpreadsheetLocale());
    notes.push('Spreadsheet time zone: ' + ss.getSpreadsheetTimeZone());
  } catch (e) { /* not available in every context */ }

  var first = failures.length ? failures[0] : { step: KIT.okStep, code: 'E00' };
  var code = KIT.code + '-FR-' + supportCode_(first.step.replace(/^GR-FR-/, ''), first.code, KIT.version);
  return { failures: failures, notes: notes, lines: lines, code: code, first: first };
}

function reportText_(result) {
  var out = [];
  out.push('Grants kit check-up report');
  out.push('Support code: ' + result.code);
  out.push('Kit version: ' + KIT.version);
  out.push('');
  out.push(result.failures.length === 0 ? 'Result: all checks passed.' :
           'Result: ' + result.failures.length + ' check(s) failed. The first one sets the code above.');
  out.push('');
  out.push('Checks');
  out = out.concat(result.lines);
  out.push('');
  out.push('Counts and settings');
  out = out.concat(result.notes);
  out.push('');
  out.push('This report contains no cell contents, names, emails, amounts, passwords or keys.');
  return out.join('\n');
}

function escapeHtml_(t) {
  return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function showResult_(result) {
  var report = reportText_(result);
  var plain = result.failures.length === 0
    ? 'Everything checks out. Your support code is below if anyone asks for it.'
    : 'Something needs a look. Find ' + result.first.code + ' in fixes.md, or send the code below with the step you were on.';
  var html =
    '<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.4">' +
    '<p>' + escapeHtml_(plain) + '</p>' +
    '<p><b>Your support code</b></p>' +
    '<p style="font-size:18px"><code>' + escapeHtml_(result.code) + '</code></p>' +
    '<p><b>Optional report.</b> This is everything that would be shared if you copy it. ' +
    'Nothing is sent from here. You choose whether to paste it into an email.</p>' +
    '<textarea readonly style="width:100%;height:230px;font-family:monospace;font-size:12px">' +
    escapeHtml_(report) + '</textarea>' +
    '</div>';
  var ui = HtmlService.createHtmlOutput(html).setWidth(560).setHeight(520);
  SpreadsheetApp.getUi().showModalDialog(ui, 'Grants kit check-up');
}
