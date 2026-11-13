/**
 * Plain Writing Word Check, for Google Docs (Apps Script).
 *
 * What it does
 *   Adds two menus to a Google Doc:
 *   - "Plain writing": highlight banned words and phrases, clear the highlights, and show a count report.
 *   - "Help": run a check-up that tests this script's setup and prints one support code.
 *
 * What it never does
 *   It never sends your text anywhere, never changes your words, and never reads or
 *   stores anything outside the document it is attached to. Highlighting only changes
 *   the background color of matching words. The check-up report holds test results
 *   and counts, never your text.
 *
 * Kit: plain-writing   Version: 0.1.0   Code: PW
 * Setup guide: setup/PW-LC-03-add-the-word-check.md
 */

var KIT_CODE = 'PW';
var KIT_VERSION = '0.1.0';
var HIGHLIGHT_COLOR = '#ffe599';

// Words that are tells wherever they appear. Each line is one family of forms.
// Edit freely: add your own house-style words, remove any you want to allow.
var BANNED_WORDS = [
  ['delve', 'delves', 'delving', 'delved'], ['tapestry'], ['realm'], ['beacon'],
  ['cacophony'], ['multifaceted'], ['commendable'], ['paramount'], ['commence'],
  ['utilize', 'utilizes', 'utilizing'], ['facilitate', 'facilitates', 'facilitating'],
  ['harness', 'harnessing'], ['illuminate', 'illuminates', 'illuminating'],
  ['testament'], ['underscore', 'underscores', 'underscoring'],
  ['foster', 'fosters', 'fostering'], ['leveraging', 'leverages'],
  ['seamless', 'seamlessly'], ['streamline', 'streamlined', 'streamlining'],
  ['empower', 'empowers', 'empowering'], ['unlock', 'unlocks', 'unlocking', 'unlocked'],
  ['elevate', 'elevates', 'elevating'], ['robust'], ['comprehensive'],
  ['navigate', 'navigates', 'navigating'], ['landscape']
];

// Phrases. Straight and curly apostrophes both match.
var BANNED_PHRASES = [
  'certainly!', 'great question', "i'd be happy to", "let's dive in", "let's explore",
  "let's break it down", 'imagine a world where', 'moreover', 'furthermore', 'in addition',
  'on the other hand', 'that said', 'with that in mind', 'it goes without saying',
  'needless to say', 'at the end of the day', 'in this article', 'this guide walks through',
  "it's important to note", 'it is worth noting', "in today's ever-evolving",
  'in an increasingly digital world', 'in summary', 'in conclusion', 'in essence',
  'to sum up', 'the bottom line is', 'a testament to', 'ai assistant'
];

function onOpen() {
  var ui = DocumentApp.getUi();
  ui.createMenu('Plain writing')
    .addItem('Highlight banned words', 'highlightBanned')
    .addItem('Clear highlights', 'clearHighlights')
    .addItem('Show count report', 'showReport')
    .addToUi();
  ui.createMenu('Help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
}

// ---- patterns ---------------------------------------------------------------

function escapeRegex_(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function wordPattern_(forms) {
  return '(?i)\\b(?:' + forms.map(escapeRegex_).join('|') + ')\\b';
}

function phrasePattern_(phrase) {
  return '(?i)' + escapeRegex_(phrase).replace(/'/g, "['’]");
}

function allPatterns_() {
  var out = [];
  BANNED_WORDS.forEach(function (forms) {
    out.push({ label: forms[0], pattern: wordPattern_(forms) });
  });
  BANNED_PHRASES.forEach(function (p) {
    out.push({ label: p, pattern: phrasePattern_(p) });
  });
  return out;
}

// ---- actions ----------------------------------------------------------------

function paint_(color) {
  var body = DocumentApp.getActiveDocument().getBody();
  var counts = {};
  allPatterns_().forEach(function (item) {
    var found = body.findText(item.pattern);
    while (found) {
      var text = found.getElement().asText();
      text.setBackgroundColor(found.getStartOffset(), found.getEndOffsetInclusive(), color);
      counts[item.label] = (counts[item.label] || 0) + 1;
      found = body.findText(item.pattern, found);
    }
  });
  return counts;
}

function highlightBanned() {
  var counts = paint_(HIGHLIGHT_COLOR);
  var total = 0;
  Object.keys(counts).forEach(function (k) { total += counts[k]; });
  DocumentApp.getUi().alert(
    total === 0
      ? 'No banned words or phrases found. This check only covers word lists. Read the checklist for structure.'
      : total + ' match(es) highlighted in yellow. Rewrite each one with a plain word, then run "Clear highlights".');
}

function clearHighlights() {
  paint_(null);
  DocumentApp.getUi().alert('Highlights cleared.');
}

function showReport() {
  var body = DocumentApp.getActiveDocument().getBody();
  var text = body.getText();
  var counts = {};
  allPatterns_().forEach(function (item) {
    var n = 0;
    var found = body.findText(item.pattern);
    while (found) { n++; found = body.findText(item.pattern, found); }
    if (n > 0) counts[item.label] = n;
  });
  var lines = Object.keys(counts).sort().map(function (k) { return k + ': ' + counts[k]; });
  var emDashes = (text.match(/—/g) || []).length;
  var curly = (text.match(/[‘’“”]/g) || []).length;
  var words = text.split(/\s+/).filter(String).length;
  var per200 = words ? (emDashes / (words / 200)).toFixed(1) : '0.0';
  var msg = (lines.length ? lines.join('\n') : 'No banned words or phrases found.') +
    '\n\nEm-dashes: ' + emDashes + ' (about ' + per200 + ' per 200 words; the style guide asks for about one or fewer)' +
    '\nCurly quotes and apostrophes: ' + curly + ' (the style guide asks for straight quotes; Google Docs often adds curly ones, so check the Tools, then Preferences, then Automatically use smart quotes setting)';
  DocumentApp.getUi().alert('Plain writing count report', msg, DocumentApp.getUi().ButtonSet.OK);
}

// ---- check-up ---------------------------------------------------------------

/**
 * Each test returns null when it passes, or {step, code, plain} when it fails.
 * step is the setup step to revisit (guide PW-LC-03). code is a row in fixes.md.
 */
function checkupTests_() {
  var tests = [];

  tests.push(function () {
    var doc = null;
    try { doc = DocumentApp.getActiveDocument(); } catch (e) { doc = null; }
    return doc ? null : { step: 2, code: 'E10', plain: 'This script is not attached to a Google Doc. Open it from inside a Doc: Extensions, then Apps Script.' };
  });

  tests.push(function () {
    return (BANNED_WORDS.length > 0 && BANNED_PHRASES.length > 0) ? null
      : { step: 3, code: 'E11', plain: 'The word lists are empty. The paste was probably cut short.' };
  });

  tests.push(function () {
    var bad = 0;
    try {
      allPatterns_().forEach(function (item) { new RegExp(item.pattern.replace('(?i)', ''), 'i'); });
    } catch (e) { bad++; }
    return bad === 0 ? null
      : { step: 3, code: 'E12', plain: 'One of the word patterns is not valid. A quote or bracket was probably changed during copying.' };
  });

  tests.push(function () {
    try {
      var t = DocumentApp.getActiveDocument().getBody().getText();
      return typeof t === 'string' ? null : { step: 6, code: 'E13', plain: 'The script could not read the Doc.' };
    } catch (e) {
      return { step: 6, code: 'E13', plain: 'The script could not read the Doc. It may need permission, so run any menu item once and approve it.' };
    }
  });

  return tests;
}

function hash3_(s) {
  var h = 0;
  for (var i = 0; i < s.length; i++) { h = (h * 31 + s.charCodeAt(i)) % 46656; }
  var out = h.toString(36).toUpperCase();
  while (out.length < 3) out = '0' + out;
  return out.slice(-3);
}

function runCheckup() {
  var ui = DocumentApp.getUi();
  var tests = checkupTests_();
  var failures = [];
  for (var i = 0; i < tests.length; i++) {
    var r;
    try { r = tests[i](); } catch (e) { r = { step: 6, code: 'E13', plain: 'A test could not run.' }; }
    if (r) failures.push(r);
  }
  var first = failures[0];
  var step = first ? first.step : 0;
  var code = first ? first.code : 'OK';
  var base = KIT_CODE + '-LC-03-' + step + '-' + code + '-v' + KIT_VERSION;
  var support = base + '-' + hash3_(base);
  var report = [
    'Kit: ' + KIT_CODE + ' (plain-writing)',
    'Version: ' + KIT_VERSION,
    'Tests run: ' + tests.length,
    'Tests failed: ' + failures.length,
    failures.length ? failures.map(function (f) { return '- ' + f.code + ' (step PW-LC-03-' + f.step + '): ' + f.plain; }).join('\n') : '- None. Setup looks right.'
  ].join('\n');
  ui.alert(
    'Plain writing check-up',
    'Your support code:\n' + support + '\n\n' +
    'Optional report. If you want to send it, copy exactly this text. It holds test results only. It does not include your document text, your name, or any passwords:\n\n' + report,
    ui.ButtonSet.OK);
}
