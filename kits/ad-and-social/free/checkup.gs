/**
 * Ad and Social check-up (kit AS, free version, kit version 0.1.0).
 *
 * Adds a "Kit help" menu with "Run check-up". It looks only at tab names, header
 * rows, and whether the Config values are filled in. It never reads or shows
 * what you typed in any cell, and it never sees passwords or keys.
 *
 * The line below asks Google for access to this one file only, not all your files.
 * @OnlyCurrentDoc
 */

var KIT_VERSION = 'v0.1.0';
var GUIDE = 'AS-FR-02';

var EXPECTED = {
  'Voice': { step: 2, headers: ['Section', 'Entry', 'Notes'] },
  'Variants': { step: 3, headers: ['Date', 'Campaign', 'Platform', 'Version', 'What changed', 'Run dates', 'Audience and budget', 'Metric chosen before starting', 'Result', 'What we learned'] },
  'Config': { step: 4, headers: ['Setting', 'Value'] }
};

var REQUIRED_SETTINGS = ['Organization name', 'Website address', 'Main audience', 'Offer we advertise most', 'Brand colors (names and hex codes)', 'Platforms we use', 'Tone in three words'];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Kit help')
    .addItem('Run check-up', 'runCheckup')
    .addToUi();
}

function runCheckup() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var lines = [];
  var firstFail = null;

  function fail(step, code) {
    if (!firstFail) { firstFail = { step: step, code: code }; }
  }

  Object.keys(EXPECTED).forEach(function (name) {
    var spec = EXPECTED[name];
    var sheet = ss.getSheetByName(name);
    if (!sheet) {
      lines.push('Tab "' + name + '": missing');
      fail(spec.step, 'E10');
      return;
    }
    var width = spec.headers.length;
    var row = sheet.getRange(1, 1, 1, width).getValues()[0];
    var ok = true;
    for (var i = 0; i < width; i++) {
      if (String(row[i]).trim() !== spec.headers[i]) { ok = false; }
    }
    lines.push('Tab "' + name + '": ' + (ok ? 'found, headings match' : 'found, headings do not match'));
    if (!ok) { fail(spec.step, 'E11'); }
  });

  var config = ss.getSheetByName('Config');
  if (config) {
    var data = config.getDataRange().getValues();
    var filled = 0;
    var seen = 0;
    for (var r = 1; r < data.length; r++) {
      var label = String(data[r][0]).trim();
      if (REQUIRED_SETTINGS.indexOf(label) !== -1) {
        seen++;
        if (String(data[r][1]).trim() !== '') { filled++; }
      }
    }
    lines.push('Config settings filled in: ' + filled + ' of ' + REQUIRED_SETTINGS.length + ' (' + seen + ' of the expected labels found)');
    if (seen < REQUIRED_SETTINGS.length) { fail(4, 'E11'); }
    else if (filled < REQUIRED_SETTINGS.length) { fail(5, 'E12'); }
  }

  var code;
  if (firstFail) {
    code = buildCode(firstFail.step, firstFail.code);
  } else {
    code = buildCode(7, 'OK');
  }
  var report = 'Ad and Social check-up\n' + lines.join('\n') + '\nSupport code: ' + code +
    '\n(This report lists tab names and counts only. It contains none of your text, keys, or contacts.)';

  var html = HtmlService.createHtmlOutput(
    '<p><b>Your support code</b></p><p style="font-size:16px"><code>' + code + '</code></p>' +
    '<p>If you ask for help, send the code. You can also send the report below, which is exactly what will be shared.</p>' +
    '<textarea style="width:100%;height:160px" readonly>' + report.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</textarea>'
  ).setWidth(480).setHeight(380);
  SpreadsheetApp.getUi().showModalDialog(html, 'Check-up result');
}

function buildCode(step, problem) {
  var base = GUIDE + '-' + step + '-' + problem + '-' + KIT_VERSION;
  return base + '-' + checkHash(base);
}

// Three letters or digits from a simple fingerprint of the first part of the code.
function checkHash(text) {
  var h = 7;
  for (var i = 0; i < text.length; i++) {
    h = (h * 31 + text.charCodeAt(i)) % 46656; // 36 * 36 * 36
  }
  var chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  return chars.charAt(Math.floor(h / 1296) % 36) + chars.charAt(Math.floor(h / 36) % 36) + chars.charAt(h % 36);
}
