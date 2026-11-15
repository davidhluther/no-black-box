/**
 * AI visibility kit (AV), low-cost version: "Log an answer" menu.
 *
 * What this does
 *   Adds an "AI visibility" menu to the same Google Sheet you built in the
 *   free version. "Log an answer" opens a small form. You paste one AI
 *   answer, and the script
 *     1. saves the full answer on an Answers tab (so you can re-read it),
 *     2. looks for your business name and website address in the answer,
 *     3. looks for names from your SameNames tab (same-name businesses),
 *     4. pulls out the web addresses that were listed as sources,
 *     5. adds one row to your Results tab with its best guess.
 *   Its guesses are only guesses. Read the row and fix anything wrong. The
 *   script does the counting; you stay the judge.
 *
 * What it never does
 *   It sends nothing anywhere. It does not call any AI model. It only
 *   touches this spreadsheet.
 *
 * Install
 *   Extensions > Apps Script, add a second file named LogAnswers (the plus
 *   button, then Script), paste this file, save, reload the sheet. The
 *   check-up file from the free version must already be in the project.
 *   See setup guide AV-LC-01.
 *
 * @OnlyCurrentDoc
 */

var ANSWER_CELL_LIMIT = 45000;

// checkup.gs owns the single onOpen function and calls this one when it
// exists, so the Kit help menu and this menu both appear.
function onOpenLogging() {
  SpreadsheetApp.getUi()
    .createMenu('AI visibility')
    .addItem('Log an answer', 'showLogDialog')
    .addToUi();
}

function showLogDialog() {
  var html = HtmlService.createHtmlOutput(dialogHtml_()).setWidth(560).setHeight(640);
  SpreadsheetApp.getUi().showModalDialog(html, 'Log an answer');
}

function logAnswer(form) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var cfg = readConfig_(ss);
  var qsh = ss.getSheetByName('Questions');
  var rsh = ss.getSheetByName('Results');
  if (!cfg.business_name || !rsh || !qsh) {
    throw new Error('Run the Kit help > Run check-up first. The Config, Questions, or Results tab is not ready.');
  }
  if (!cfg.question_set_version) {
    throw new Error('Freeze your question set first (Config tab, question_set_version). Guide AV-FR-03, step 4.');
  }

  var qid = String(form.questionId || '').trim().toUpperCase();
  var product = String(form.product || '').trim();
  var status = String(form.status || 'ok');
  var runId = String(form.runId || '').trim() ||
    Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM');
  var text = String(form.answer || '');
  var sources = String(form.sources || '');
  var others = String(form.others || '').trim();
  var resolved = String(form.resolved || '').trim();

  // Make sure the question exists.
  var ids = qsh.getRange(1, 1, qsh.getLastRow(), 1).getValues().map(function (r) { return String(r[0]).trim(); });
  if (ids.indexOf(qid) < 0) throw new Error('That question code is not on the Questions tab.');

  // Save the answer text.
  var ash = ss.getSheetByName('Answers') || ss.insertSheet('Answers');
  if (ash.getLastRow() === 0) {
    ash.appendRow(['run_id', 'question_id', 'ai_product', 'answer_text', 'sources_pasted']);
  }
  var stored = text.length > ANSWER_CELL_LIMIT ? text.substring(0, ANSWER_CELL_LIMIT) + ' [cut: too long for one cell]' : text;
  ash.appendRow([avLiteral_(runId), qid, avLiteral_(product), avLiteral_(stored), avLiteral_(sources)]);

  var named = 'n', position = '-', cited = 'none_given', domainsOut = '', note = 'guessed by script, check it';
  if (status === 'ok') {
    var low = text.toLowerCase();
    var nameHit = low.indexOf(cfg.business_name.toLowerCase()) >= 0;
    var domain = cfg.website_domain.toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '');
    var domainHit = domain && (low.indexOf(domain) >= 0 || sources.toLowerCase().indexOf(domain) >= 0);
    var sameHit = sameNameHit_(ss, low);
    if (nameHit || domainHit) named = 'y';
    else if (sameHit) named = 'same-name';
    if (nameHit && sameHit) note = 'name found, and a same-name entry also found: read the answer to be sure';
    if (named === 'y') position = guessPosition_(text, cfg.business_name);

    var domains = extractDomains_(sources + ' ' + text);
    if (domains.length) {
      domainsOut = domains.join('; ');
      cited = (domain && domains.some(function (d) { return d.indexOf(domain) >= 0; })) ? 'y' : 'n';
    }
  } else {
    note = 'answer not collected (' + status + ')';
  }

  var row = rsh.getLastRow() + 1;
  var group = '=IFERROR(VLOOKUP(B' + row + ',Questions!$A:$B,2,FALSE),"")';
  var outcome = '=IF(A' + row + '="","",IF(D' + row + '<>"ok","not scored",IF(E' + row + '="y",IF(G' + row +
    '="y","named and cited","named only"),IF(G' + row + '="y","cited only",IF(I' + row + '<>"","crowded out","absent")))))';
  rsh.getRange(row, 1, 1, 14).setValues([[avLiteral_(runId), qid, avLiteral_(product), avLiteral_(status), named, position, cited, domainsOut,
    avLiteral_(others), avLiteral_(resolved), cfg.question_set_version, note, outcome, group]]);
  return 'Logged ' + qid + ' for ' + product + ': named = ' + named + ', your site cited = ' + cited + '. Check the new row on the Results tab.';
}

/** Keeps pasted text as plain text: a leading =, +, - or @ would otherwise make a formula. */
function avLiteral_(v) {
  return (typeof v === 'string' && /^[=+\-@]/.test(v)) ? "'" + v : v;
}

function readConfig_(ss) {
  var out = {};
  var sh = ss.getSheetByName('Config');
  if (!sh) return out;
  var v = sh.getDataRange().getValues();
  for (var i = 1; i < v.length; i++) out[String(v[i][0]).trim()] = String(v[i][1]).trim();
  return out;
}

function sameNameHit_(ss, lowText) {
  var sh = ss.getSheetByName('SameNames');
  if (!sh) return false;
  var v = sh.getDataRange().getValues();
  for (var i = 1; i < v.length; i++) {
    var name = String(v[i][0]).trim().toLowerCase();
    var kind = String(v[i][1]).toLowerCase();
    if (name && kind.indexOf('everyday') < 0 && lowText.indexOf(name) >= 0) return true;
  }
  return false;
}

function guessPosition_(text, name) {
  var lines = text.split(/\r?\n/);
  var lowName = name.toLowerCase();
  var numbered = 0, bullets = 0, hitNumber = null, hitBullet = false;
  for (var i = 0; i < lines.length; i++) {
    var m = lines[i].match(/^\s*(\d+)[.)]\s/);
    if (m) {
      numbered++;
      if (lines[i].toLowerCase().indexOf(lowName) >= 0 && hitNumber === null) hitNumber = parseInt(m[1], 10);
    } else if (/^\s*[-*•]\s/.test(lines[i])) {
      bullets++;
      if (lines[i].toLowerCase().indexOf(lowName) >= 0) hitBullet = true;
    } else if (lines[i].toLowerCase().indexOf(lowName) >= 0 && numbered > 0 && hitNumber === null) {
      // Name sits in the text under a numbered item: count it as that item.
      hitNumber = numbered;
    }
  }
  if (hitNumber !== null) return hitNumber >= 3 ? '3+' : String(hitNumber);
  if (hitBullet) return 'list';
  var paragraphs = text.split(/\n\s*\n/);
  var first = paragraphs.length ? paragraphs[0].toLowerCase() : '';
  return first.indexOf(lowName) >= 0 ? '1' : 'aside';
}

function extractDomains_(text) {
  var found = {};
  var re = /(?:https?:\/\/)?(?:www\.)?([a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,})(?:[\/\s)\],;:]|$)/gi;
  var m;
  while ((m = re.exec(text)) !== null) found[m[1].toLowerCase()] = true;
  return Object.keys(found);
}

function dialogHtml_() {
  var products = ['ChatGPT', 'Claude', 'Gemini', 'Perplexity'];
  var opts = products.map(function (p) { return '<option>' + p + '</option>'; }).join('');
  return '<div style="font-family:Arial,sans-serif;font-size:13px;line-height:1.4">' +
    '<p>Paste one answer. One question, one AI product, per log.</p>' +
    '<p>Question code<br><input id="q" placeholder="LD-01" style="width:120px"></p>' +
    '<p>AI product<br><select id="p">' + opts + '</select></p>' +
    '<p>Did you get an answer?<br><select id="s"><option value="ok">ok</option><option value="not_run">not_run (skipped)</option>' +
    '<option value="refused">refused (the AI would not answer)</option><option value="failed">failed (error or timeout)</option></select></p>' +
    '<p>Answer text<br><textarea id="a" style="width:100%;height:150px"></textarea></p>' +
    '<p>Sources shown (paste web addresses or site names, one per line; leave empty if none)<br><textarea id="src" style="width:100%;height:60px"></textarea></p>' +
    '<p>Other businesses named (separate with semicolons)<br><input id="o" style="width:100%"></p>' +
    '<p>What did the answer settle on?<br><select id="r"><option value=""></option><option>person_local</option><option>person_remote</option>' +
    '<option>software</option><option>generic_advice</option><option>nobody</option></select></p>' +
    '<p>Run label (leave empty for this month)<br><input id="run" placeholder="2026-11" style="width:120px"></p>' +
    '<button onclick="go()">Log it</button> <span id="msg" style="color:#444"></span>' +
    '<script>function go(){document.getElementById("msg").textContent="Working...";' +
    'google.script.run.withSuccessHandler(function(t){document.getElementById("msg").textContent=t;document.getElementById("a").value="";document.getElementById("src").value="";document.getElementById("o").value="";})' +
    '.withFailureHandler(function(e){document.getElementById("msg").textContent="Problem: "+e.message;})' +
    '.logAnswer({questionId:document.getElementById("q").value,product:document.getElementById("p").value,status:document.getElementById("s").value,' +
    'answer:document.getElementById("a").value,sources:document.getElementById("src").value,others:document.getElementById("o").value,' +
    'resolved:document.getElementById("r").value,runId:document.getElementById("run").value});}</script></div>';
}
