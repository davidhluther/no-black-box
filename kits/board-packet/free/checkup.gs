/**
 * Board packet check-up (free version of the board-packet kit, MIT license).
 *
 * What it does: adds a "Help" menu to your tracker Google Sheet with one item,
 * "Run check-up". It looks at the shape of your setup (are the four tabs there,
 * are the column headings right, are the required settings filled in, do your
 * Drive folders exist) and prints one support code plus an optional plain-text
 * report you can copy.
 *
 * What it never does: it never reads or reports the text you typed into cells,
 * never reports names, email addresses, folder names or file names, never sends
 * anything anywhere, and never changes your sheet or your Drive. It shows you
 * the full report on screen before you copy a word of it.
 *
 * Support code format: BP-FR-02-2-E01-v0.1.0-7KQ
 *   BP-FR-02-2  the setup step where the first problem starts (kit, version, guide, step)
 *   E01         the problem code (see fixes.md in the kit)
 *   v0.1.0      the kit version
 *   7KQ         a three-character check value made from the full list of problems
 * A clean check-up prints BP-FR-00-0-E00-v0.1.0 plus the check value.
 */

var BP_KIT = 'BP';
var BP_VERSION = '0.1.0';

// The tabs and column headings the kit expects. Step = the setup step that creates it.
var BP_TABS = [
  { name: 'Settings', tabCode: 'E01', headerCode: 'E05', step: 'BP-FR-02-2',
    headers: ['Setting', 'Value', 'Notes'] },
  { name: 'Reports', tabCode: 'E02', headerCode: 'E06', step: 'BP-FR-02-3',
    headers: ['Order', 'Report', 'Owner', 'Role in packet', 'In combined packet',
              'Filename keyword', 'Active', 'Received this month', 'Link or note'] },
  { name: 'Contacts', tabCode: 'E03', headerCode: 'E07', step: 'BP-FR-02-4',
    headers: ['Name', 'Email', 'Group', 'Role', 'Active'] },
  { name: 'Month', tabCode: 'E04', headerCode: 'E08', step: 'BP-FR-02-5',
    headers: ['Item', 'Value', 'Notes'] }
];

// Settings that must have a value. The check-up only asks "is it filled in?".
var BP_REQUIRED_SETTINGS = [
  'org_name', 'board_name', 'meeting_time', 'meeting_location', 'chair_name',
  'secretary_name', 'sender_name', 'root_folder_name', 'transcripts_folder_name',
  'email_subject_pattern'
];

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Help')
    .addItem('Run check-up', 'bpRunCheckup')
    .addToUi();
  // The low-cost version adds its own menu from packet.gs.
  if (typeof bpAddPacketMenu_ === 'function') {
    bpAddPacketMenu_();
  }
}

function bpRunCheckup() {
  var problems = [];   // { step, code, text }
  var lines = [];      // report lines
  var ss = SpreadsheetApp.getActiveSpreadsheet();

  lines.push('Board packet check-up');
  lines.push('Kit version: ' + BP_VERSION);
  lines.push('Run at: ' + Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MM/dd/yyyy HH:mm z'));
  lines.push('');

  var sheets = {};
  BP_TABS.forEach(function (t) {
    var sh = ss.getSheetByName(t.name);
    if (!sh) {
      problems.push({ step: t.step, code: t.tabCode, text: 'Tab "' + t.name + '" is missing.' });
      lines.push('Tab ' + t.name + ': missing');
      return;
    }
    sheets[t.name] = sh;
    var bad = [];
    var width = Math.max(t.headers.length, 1);
    var row = sh.getRange(1, 1, 1, width).getValues()[0];
    for (var i = 0; i < t.headers.length; i++) {
      if (String(row[i]).trim() !== t.headers[i]) {
        bad.push('column ' + (i + 1) + ' should be "' + t.headers[i] + '"');
      }
    }
    if (bad.length) {
      problems.push({ step: t.step, code: t.headerCode, text: 'Tab "' + t.name + '" headings are off: ' + bad.join('; ') + '.' });
      lines.push('Tab ' + t.name + ': found, headings need fixing (' + bad.length + ' of ' + t.headers.length + ')');
    } else {
      lines.push('Tab ' + t.name + ': found, headings correct');
    }
  });

  // Settings: filled or blank (never the value itself).
  if (sheets.Settings) {
    var vals = sheets.Settings.getDataRange().getValues();
    var filled = {};
    for (var r = 1; r < vals.length; r++) {
      var key = String(vals[r][0]).trim();
      if (key) { filled[key] = String(vals[r][1]).trim() !== ''; }
    }
    var blank = [];
    BP_REQUIRED_SETTINGS.forEach(function (k) {
      if (!(k in filled)) { blank.push(k + ' (row missing)'); }
      else if (!filled[k]) { blank.push(k); }
    });
    if (typeof bpMakeMonthFolder === 'function' && !filled['combined_packet_filename']) {
      problems.push({ step: 'BP-LC-02-4', code: 'E20', text: 'combined_packet_filename is blank (low-cost version needs it).' });
      lines.push('Low-cost setting combined_packet_filename: blank');
    }
    if (blank.length) {
      problems.push({ step: 'BP-FR-02-6', code: 'E09', text: 'These settings are blank: ' + blank.join(', ') + '.' });
      lines.push('Required settings blank: ' + blank.join(', '));
    } else {
      lines.push('Required settings: all ' + BP_REQUIRED_SETTINGS.length + ' filled in');
    }
  }

  // Reports: shape only.
  if (sheets.Reports) {
    var rv = sheets.Reports.getDataRange().getValues();
    var active = 0, minutesRows = 0, orders = {}, dup = false;
    for (var i2 = 1; i2 < rv.length; i2++) {
      if (String(rv[i2][1]).trim() === '') { continue; }
      var ord = String(rv[i2][0]).trim();
      if (ord in orders) { dup = true; }
      orders[ord] = true;
      if (String(rv[i2][6]).trim().toLowerCase() === 'yes') { active++; }
      if (String(rv[i2][3]).trim().toLowerCase() === 'minutes') { minutesRows++; }
    }
    lines.push('Reports: ' + active + ' active row(s), ' + minutesRows + ' minutes row(s)');
    if (active === 0) {
      problems.push({ step: 'BP-FR-02-8', code: 'E10', text: 'No report is marked Active = Yes.' });
    }
    if (minutesRows === 0) {
      problems.push({ step: 'BP-FR-02-8', code: 'E11', text: 'No row has "minutes" in the Role in packet column.' });
    }
    if (dup) {
      problems.push({ step: 'BP-FR-02-8', code: 'E12', text: 'Two reports share the same Order number.' });
    }
  }

  // Contacts: counts and address shape only.
  if (sheets.Contacts) {
    var cv = sheets.Contacts.getDataRange().getValues();
    var counts = { to: 0, cc: 0, bcc: 0 }, badEmail = 0;
    for (var i3 = 1; i3 < cv.length; i3++) {
      var email = String(cv[i3][1]).trim();
      if (!email) { continue; }
      if (String(cv[i3][4]).trim().toLowerCase() !== 'yes') { continue; }
      var g = String(cv[i3][2]).trim().toLowerCase();
      if (g in counts) { counts[g]++; }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { badEmail++; }
    }
    lines.push('Contacts (active): To ' + counts.to + ', Cc ' + counts.cc + ', Bcc ' + counts.bcc);
    if (counts.to === 0) {
      problems.push({ step: 'BP-FR-02-7', code: 'E13', text: 'No active contact is in the To group.' });
    }
    if (badEmail > 0) {
      problems.push({ step: 'BP-FR-02-7', code: 'E14', text: badEmail + ' email address(es) do not look like an address.' });
    }
  }

  // Drive folders: found or not found, never the names themselves.
  try {
    if (sheets.Settings) {
      var sv = sheets.Settings.getDataRange().getValues();
      var cfg = {};
      for (var r2 = 1; r2 < sv.length; r2++) { cfg[String(sv[r2][0]).trim()] = String(sv[r2][1]).trim(); }
      var root = cfg['root_folder_name'] ? bpFirstFolder_(cfg['root_folder_name']) : null;
      if (cfg['root_folder_name']) {
        if (!root) {
          problems.push({ step: 'BP-FR-01-2', code: 'E15', text: 'The shared packet folder was not found in your Drive.' });
          lines.push('Shared packet folder: not found');
        } else {
          lines.push('Shared packet folder: found');
          var yearFound = false, it = root.getFolders();
          while (it.hasNext()) { if (/^\d{4}$/.test(it.next().getName())) { yearFound = true; break; } }
          if (!yearFound) {
            problems.push({ step: 'BP-FR-01-3', code: 'E16', text: 'No year folder (such as 2027) was found inside the shared packet folder.' });
            lines.push('Year folder: not found');
          } else { lines.push('Year folder: found'); }
        }
      }
      var priv = cfg['transcripts_folder_name'] ? bpFirstFolder_(cfg['transcripts_folder_name']) : null;
      if (cfg['transcripts_folder_name']) {
        if (!priv) {
          problems.push({ step: 'BP-FR-01-4', code: 'E17', text: 'The private transcripts folder was not found in your Drive.' });
          lines.push('Private transcripts folder: not found');
        } else {
          lines.push('Private transcripts folder: found');
          if (root && bpIsInside_(priv, root.getId())) {
            problems.push({ step: 'BP-FR-01-4', code: 'E18', text: 'The private transcripts folder sits inside the shared packet folder.' });
            lines.push('Private transcripts folder: sits INSIDE the shared folder (should be outside)');
          }
        }
      }
    }
  } catch (err) {
    problems.push({ step: 'BP-FR-04-4', code: 'E19', text: 'The check-up could not look at Drive (permission not given yet).' });
    lines.push('Drive: could not be checked (permission)');
  }

  // Build the support code from the earliest step.
  problems.sort(function (a, b) { return a.step < b.step ? -1 : (a.step > b.step ? 1 : (a.code < b.code ? -1 : 1)); });
  var codes = problems.map(function (p) { return p.code; });
  var first = problems.length ? problems[0] : { step: 'BP-FR-00-0', code: 'E00' };
  var hash = bpHash_(codes.join(',') + '|' + BP_VERSION);
  var supportCode = first.step + '-' + first.code + '-v' + BP_VERSION + '-' + hash;

  lines.push('');
  if (problems.length === 0) {
    lines.push('Result: everything the check-up looks at is in place.');
  } else {
    lines.push('Result: ' + problems.length + ' thing(s) to fix, listed in setup order.');
    problems.forEach(function (p) { lines.push('  ' + p.code + ' at ' + p.step + ': ' + p.text); });
  }
  lines.push('');
  lines.push('Support code: ' + supportCode);
  lines.push('This report holds no cell contents, names, email addresses, file names or folder names.');

  bpShowReport_(supportCode, lines.join('\n'), problems.length);
}

function bpFirstFolder_(name) {
  var it = DriveApp.getFoldersByName(name);
  return it.hasNext() ? it.next() : null;
}

// True when folder has the given ancestor id anywhere above it (up to 12 levels).
function bpIsInside_(folder, ancestorId) {
  var level = [folder];
  for (var depth = 0; depth < 12; depth++) {
    var next = [];
    for (var i = 0; i < level.length; i++) {
      var parents = level[i].getParents();
      while (parents.hasNext()) {
        var p = parents.next();
        if (p.getId() === ancestorId) { return true; }
        next.push(p);
      }
    }
    if (!next.length) { return false; }
    level = next;
  }
  return false;
}

// Three base-36 characters from a simple rolling hash.
function bpHash_(text) {
  var h = 7;
  for (var i = 0; i < text.length; i++) { h = (h * 31 + text.charCodeAt(i)) % 46656; }
  var s = h.toString(36).toUpperCase();
  while (s.length < 3) { s = '0' + s; }
  return s;
}

function bpShowReport_(code, report, problemCount) {
  var safe = report.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  var html =
    '<div style="font-family:Arial,sans-serif;font-size:14px;line-height:1.4">' +
    '<p>Your support code:</p>' +
    '<p style="font-size:20px;font-weight:bold;letter-spacing:1px">' + code + '</p>' +
    '<p>' + (problemCount === 0
      ? 'Nothing needs fixing. Keep the code if someone asks for it.'
      : 'Send this code, and the step where you got stuck, to the people helping you.') + '</p>' +
    '<p>Optional report. This is everything that would be shared if you copy it:</p>' +
    '<textarea id="r" readonly style="width:100%;height:220px;font-family:monospace;font-size:12px">' + safe + '</textarea>' +
    '<p><button onclick="var t=document.getElementById(\'r\');t.select();document.execCommand(\'copy\');this.innerText=\'Copied\'">Copy report</button></p>' +
    '</div>';
  var out = HtmlService.createHtmlOutput(html).setWidth(560).setHeight(480);
  SpreadsheetApp.getUi().showModalDialog(out, 'Board packet check-up');
}
