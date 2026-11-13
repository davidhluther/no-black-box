/**
 * Idea to Live Post kit: draft check for a Google Doc (free version).
 * Adds a "Draft check" menu to a Google Doc. It counts a few things a plain-language
 * edit should fix: banned words, long paragraphs, curly quotes, colons, and numbers
 * with no nearby source word. It only reads the open document and shows a message.
 * It changes nothing and sends nothing anywhere.
 */
var BANNED = ['delve', 'tapestry', 'realm', 'beacon', 'multifaceted', 'paramount', 'commence',
  'utilize', 'facilitate', 'harness', 'illuminate', 'testament', 'underscore', 'foster',
  'leverage', 'leveraging', 'seamless', 'seamlessly', 'streamline', 'empower', 'unlock', 'elevate',
  'moreover', 'furthermore', 'in conclusion', 'in summary', 'needless to say', 'at the end of the day'];

function onOpen() {
  DocumentApp.getUi().createMenu('Draft check').addItem('Check this draft', 'checkDraft').addToUi();
}

function checkDraft() {
  var body = DocumentApp.getActiveDocument().getBody();
  var text = body.getText();
  var lower = text.toLowerCase();
  var report = [];

  var hits = [];
  BANNED.forEach(function (w) {
    var re = new RegExp('\\b' + w + '\\b', 'g');
    var m = lower.match(re);
    if (m) { hits.push(w + ' (' + m.length + ')'); }
  });
  report.push(hits.length ? 'Banned or tell-tale words found: ' + hits.join(', ') : 'No banned words found.');

  var longParas = 0;
  body.getParagraphs().forEach(function (p) {
    var sentences = p.getText().split(/[.!?]+\s/).filter(function (s) { return s.trim().length > 0; });
    if (sentences.length > 6) { longParas++; }
  });
  report.push(longParas ? longParas + ' paragraph(s) run longer than six sentences. Split them.' : 'No paragraph is longer than six sentences.');

  var curly = (text.match(/[‘’“”]/g) || []).length;
  report.push(curly ? curly + ' curly quote mark(s). Replace with straight quotes.' : 'Quotes are straight.');

  var colons = (text.match(/:\s/g) || []).length;
  report.push('Colons in body text: ' + colons + '. Reword most of them into plain sentences.');

  var words = text.split(/\s+/).filter(function (w) { return w.length; }).length;
  report.push('Word count: ' + words + '.');

  var numbers = text.match(/\b\d[\d,.]*%?/g) || [];
  report.push(numbers.length + ' number(s) in the text. Every figure needs a named source; check each one by hand.');

  DocumentApp.getUi().alert('Draft check', report.join('\n\n'), DocumentApp.getUi().ButtonSet.OK);
}
