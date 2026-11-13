/**
 * AI visibility kit (AV), free version: Help menu with "Run check-up".
 *
 * What this does
 *   Adds a "Help" menu to your Google Sheet. "Run check-up" looks at the
 *   structure of your sheet (are the tabs there, are the column headings
 *   right, are your setup cells filled in, are the question codes in your
 *   results real) and shows one support code, such as
 *   AV-FR-03-2-E06-v0.1.0-7KQ, plus an optional plain-text report.
 *
 * What this never does
 *   It never sends anything anywhere. It never reads passwords or keys, and
 *   the report never contains your business name, your questions, the AI
 *   answers, web addresses, or any other cell contents. It reports tab
 *   names, counts, and problem codes only. The dialog shows you exactly
 *   what the report says before you copy it.
 *
 * Install
 *   In your sheet choose Extensions > Apps Script, delete the sample code,
 *   paste this whole file, and save. Reload the sheet. See setup guide
 *   AV-FR-01, steps 4 and 5.
 *
 * @OnlyCurrentDoc
 */

var KIT_CODE = 'AV';
var KIT_VERSION = '0.1.0';
var VERSION_TAG = 'FR';

var HEADERS = {
  Config: ['key', 'value', 'what to put here'],
  Questions: ['question_id', 'group', 'control_no_town', 'question_template', 'question_to_paste'],
  Runs: ['run_id', 'run_date', 'run_by', 'question_set_version', 'ai_product', 'model_shown',
         'signed_in_state', 'memory_off', 'location_note', 'questions_skipped', 'notes'],
  Results: ['run_id', 'question_id', 'ai_product', 'answer_status', 'named', 'position',
            'your_site_cited', 'cited_domains', 'others_named', 'resolved_to', 'qset_version',
            'notes', 'outcome', 'group'],
  SameNames: ['name_or_word', 'kind', 'where_found', 'how_to_tell_apart', 'severity']
};

// Which setup guide step to look at for each problem code.
var STEP_FOR = {
  E01: 'AV-FR-01-3', E02: 'AV-FR-01-3',
  E03: 'AV-FR-03-1', E04: 'AV-FR-03-2', E05: 'AV-FR-03-2', E06: 'AV-FR-03-3',
  E07: 'AV-FR-03-4', E08: 'AV-FR-05-2', E09: 'AV-FR-06-3', E10: 'AV-FR-05-2',
  E11: 'AV-FR-02-3'
};

var PROBLEM_TEXT = {
  E01: 'A tab is missing or named differently from the kit.',
  E02: 'A tab has column headings that do not match the kit.',
  E03: 'A setup cell on the Config tab is empty or still has the example text.',
  E04: 'A question on the Questions tab still has curly brackets or shows a formula error.',
  E05: 'The Questions tab does not have exactly 28 questions, or two share a code.',
  E06: 'A question that should not name your business does name it.',
  E07: 'The question set is not frozen yet (no version or no freeze date on Config).',
  E08: 'The Results tab has question codes that are not on the Questions tab.',
  E09: 'Your runs or results mix more than one question set version. Do not compare them.',
  E10: 'The Results tab has a value in a coded column that the kit does not use.',
  E11: 'The SameNames tab is empty or still has the example rows.'
};

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
  // The low-cost version adds a second file with its own menu.
  if (typeof onOpenLogging === 'function') { onOpenLogging(); }
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var found = []; // {code, count}

  function add(code, count) {
    found.push({ code: code, count: count || 1 });
  }

  // E01 and E02: tabs and headings.
  var sheets = {};
  Object.keys(HEADERS).concat(['Summary']).forEach(function (name) {
    var sh = ss.getSheetByName(name);
    if (!sh) { add('E01'); } else { sheets[name] = sh; }
  });
  Object.keys(HEADERS).forEach(function (name) {
    var sh = sheets[name];
    if (!sh) return;
    var want = HEADERS[name];
    var have = sh.getRange(1, 1, 1, want.length).getValues()[0].map(function (v) { return String(v).trim(); });
    for (var i = 0; i < want.length; i++) {
      if (have[i] !== want[i]) { add('E02'); break; }
    }
  });

  // Config values by key.
  var cfg = {};
  if (sheets.Config) {
    var cv = sheets.Config.getDataRange().getValues();
    for (var r = 1; r < cv.length; r++) {
      cfg[String(cv[r][0]).trim()] = String(cv[r][1]).trim();
    }
  }
  var examples = {
    business_name: 'Maple Hair Studio', business_type: 'hair salon', service: 'balayage color',
    town: 'Maple Town', region: 'Example County', owner_name: 'Alex Example',
    competitor_1: 'Riverside Salon', website_domain: 'example.org'
  };
  var emptyOrExample = 0;
  Object.keys(examples).forEach(function (k) {
    var v = cfg[k];
    if (!v || v.toLowerCase() === examples[k].toLowerCase()) emptyOrExample++;
  });
  if (sheets.Config && emptyOrExample > 0) add('E03', emptyOrExample);

  // Questions.
  var ids = [];
  var brandName = (cfg.business_name || '').toLowerCase();
  var ownerName = (cfg.owner_name || '').toLowerCase();
  if (sheets.Questions) {
    var qv = sheets.Questions.getDataRange().getValues();
    var unfilled = 0, contaminated = 0, dupes = 0, seen = {};
    for (var q = 1; q < qv.length; q++) {
      var id = String(qv[q][0]).trim();
      if (!id) continue;
      ids.push(id);
      if (seen[id]) dupes++;
      seen[id] = true;
      var text = String(qv[q][4]);
      if (text.indexOf('{') >= 0 || text.indexOf('}') >= 0 || text.charAt(0) === '#') unfilled++;
      var group = String(qv[q][1]).trim();
      if (group !== 'BV') {
        var low = text.toLowerCase();
        if ((brandName && low.indexOf(brandName) >= 0) || (ownerName && low.indexOf(ownerName) >= 0)) contaminated++;
      }
    }
    if (unfilled > 0) add('E04', unfilled);
    if (ids.length !== 28 || dupes > 0) add('E05', Math.abs(ids.length - 28) + dupes);
    if (contaminated > 0) add('E06', contaminated);
  }

  // E07: frozen?
  if (sheets.Config && (!cfg.question_set_version || !cfg.question_set_frozen_on)) add('E07');

  // E11: same-name preflight done?
  if (sheets.SameNames) {
    var sv = sheets.SameNames.getDataRange().getValues();
    var rows = 0, exampleRows = 0;
    for (var s = 1; s < sv.length; s++) {
      var nm = String(sv[s][0]).trim();
      if (!nm) continue;
      rows++;
      if (nm === 'Maple Studio' || nm === 'maple') exampleRows++;
    }
    if (rows === 0 || rows === exampleRows) add('E11');
  }

  // Runs and Results.
  var okStatus = { ok: 1, not_run: 1, refused: 1, failed: 1 };
  var okNamed = { y: 1, n: 1, 'same-name': 1 };
  var okCited = { y: 1, n: 1, none_given: 1 };
  var okResolved = { person_local: 1, person_remote: 1, software: 1, generic_advice: 1, nobody: 1 };
  var versions = {};
  if (sheets.Runs) {
    var rv = sheets.Runs.getDataRange().getValues();
    for (var a = 1; a < rv.length; a++) {
      var ver = String(rv[a][3]).trim();
      if (String(rv[a][0]).trim() && ver) versions[ver] = true;
    }
  }
  if (sheets.Results) {
    var res = sheets.Results.getDataRange().getValues();
    var idSet = {}; ids.forEach(function (i) { idSet[i] = true; });
    var badIds = 0, badVals = 0;
    for (var b = 1; b < res.length; b++) {
      var row = res[b];
      if (!String(row[0]).trim()) continue;
      var qid = String(row[1]).trim();
      if (sheets.Questions && !idSet[qid]) badIds++;
      var status = String(row[3]).trim();
      if (!okStatus[status]) { badVals++; continue; }
      if (status === 'ok') {
        if (!okNamed[String(row[4]).trim()]) badVals++;
        if (!/^(\d+\+?|list|aside|-)$/.test(String(row[5]).trim())) badVals++;
        if (!okCited[String(row[6]).trim()]) badVals++;
        var rt = String(row[9]).trim();
        if (rt && !okResolved[rt]) badVals++;
      }
      var rver = String(row[10]).trim();
      if (rver) versions[rver] = true;
    }
    if (badIds > 0) add('E08', badIds);
    if (badVals > 0) add('E10', badVals);
  }
  if (Object.keys(versions).length > 1) add('E09', Object.keys(versions).length);

  showResult_(ss, found);
}

function showResult_(ss, found) {
  var first = found.length ? found[0].code : null;
  var step = first ? (STEP_FOR[first] || (KIT_CODE + '-' + VERSION_TAG + '-00-0')) : (KIT_CODE + '-' + VERSION_TAG + '-00-0');
  var codeForSupport = first || 'E00';
  var fingerprint = found.map(function (f) { return f.code + 'x' + f.count; }).join(',') || 'clear';
  var code = step + '-' + codeForSupport + '-v' + KIT_VERSION + '-' + hash3_(fingerprint + '|' + KIT_VERSION);

  var lines = [];
  lines.push('AI visibility kit check-up report');
  lines.push('Support code: ' + code);
  lines.push('Kit version: ' + KIT_VERSION + ' (' + VERSION_TAG + ')');
  lines.push('Tabs found: ' + ss.getSheets().map(function (s) { return s.getName(); }).filter(function (n) {
    return n === 'Config' || n === 'Questions' || n === 'Runs' || n === 'Results' || n === 'SameNames' || n === 'Summary';
  }).join(', '));
  if (!found.length) {
    lines.push('Problems found: none');
  } else {
    lines.push('Problems found: ' + found.length);
    found.forEach(function (f) {
      lines.push('  ' + f.code + ' (count ' + f.count + '), look at step ' + (STEP_FOR[f.code] || 'unknown') + ': ' + PROBLEM_TEXT[f.code]);
    });
  }
  lines.push('This report contains no business names, questions, answers, links, or other cell contents.');
  var report = lines.join('\n');

  var html = '<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.4">' +
    '<p><b>Your support code</b></p>' +
    '<p style="font-size:18px;font-family:monospace">' + esc_(code) + '</p>' +
    '<p>' + (found.length ? 'The first thing to fix is ' + esc_(first) + ': ' + esc_(PROBLEM_TEXT[first]) +
      ' It points to step ' + esc_(STEP_FOR[first]) + ' of the setup guides.' : 'No problems found.') + '</p>' +
    '<p><b>Optional report.</b> This is everything that would be shared if you copy it. Nothing is sent for you.</p>' +
    '<textarea style="width:100%;height:210px;font-family:monospace;font-size:12px" readonly>' + esc_(report) + '</textarea>' +
    '<p>To get help, send the support code (and the report if you like) to the contact address in the How to get help box at the end of any setup guide. Setup questions are free.</p>' +
    '</div>';
  SpreadsheetApp.getUi().showModalDialog(HtmlService.createHtmlOutput(html).setWidth(560).setHeight(520), 'Check-up');
}

function hash3_(text) {
  var h = 5381;
  for (var i = 0; i < text.length; i++) { h = ((h * 33) ^ text.charCodeAt(i)) >>> 0; }
  var alphabet = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ';
  var out = '';
  for (var k = 0; k < 3; k++) { out += alphabet.charAt(h % alphabet.length); h = Math.floor(h / alphabet.length); }
  return out;
}

function esc_(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
