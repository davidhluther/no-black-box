/**
 * Board packet helper (low-cost version of the board-packet kit, MIT license).
 *
 * Paste this into the same Apps Script project as free/checkup.gs, as a second file.
 * It adds a "Board packet" menu to your tracker Google Sheet with three items:
 *
 *   1. Make this month's folder   creates (or finds) the year and month folders in Drive.
 *   2. Make PDF copies            saves a numbered PDF copy of each report, in packet order.
 *   3. Make the email draft       writes the board email as a Gmail DRAFT.
 *
 * Safety promises, all checkable by reading this file:
 *   - It never sends email. The only mail call it makes is the one that creates
 *     a draft. Guide BP-LC-02 shows how to confirm that with the search box.
 *   - It never deletes your files. The only thing it trashes is its own earlier
 *     PDF copies in the "PDF copies" folder, so a re-run does not pile up duplicates.
 *   - It never changes who can open a file or folder.
 *   - It only reads the Settings, Month, Reports and Contacts tabs of this sheet.
 *
 * Honest limit: Apps Script has no built-in way to merge PDFs into one file.
 * Step 2 makes the numbered copies and the list in the "Last run" tab;
 * guide BP-LC-03 shows the simplest free way to merge them.
 */

var BP_PDF_FOLDER = 'PDF copies';
var BP_GOOGLE_TYPES = [
  'application/vnd.google-apps.document',
  'application/vnd.google-apps.spreadsheet',
  'application/vnd.google-apps.presentation'
];

function bpAddPacketMenu_() {
  SpreadsheetApp.getUi()
    .createMenu('Board packet')
    .addItem('1. Make this month\'s folder', 'bpMakeMonthFolder')
    .addItem('2. Make PDF copies', 'bpMakePdfCopies')
    .addItem('3. Make the email draft', 'bpMakeEmailDraft')
    .addToUi();
}

/* ---------- reading the tabs ---------- */

function bpKeyValues_(tabName) {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(tabName);
  var out = {};
  if (!sh) { return out; }
  var v = sh.getDataRange().getValues();
  for (var i = 1; i < v.length; i++) {
    var k = String(v[i][0]).trim();
    if (k) { out[k] = v[i][1]; }
  }
  return out;
}

function bpText_(v) { return (v === null || v === undefined) ? '' : String(v).trim(); }

function bpReports_() {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Reports');
  var v = sh.getDataRange().getValues();
  var rows = [];
  for (var i = 1; i < v.length; i++) {
    if (!bpText_(v[i][1])) { continue; }
    rows.push({
      order: Number(v[i][0]) || 0,
      name: bpText_(v[i][1]),
      role: bpText_(v[i][3]).toLowerCase(),
      inPacket: bpText_(v[i][4]).toLowerCase() === 'yes',
      keyword: bpText_(v[i][5]).toLowerCase(),
      active: bpText_(v[i][6]).toLowerCase() === 'yes'
    });
  }
  rows.sort(function (a, b) { return a.order - b.order; });
  return rows;
}

function bpContacts_() {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Contacts');
  var v = sh.getDataRange().getValues();
  var g = { to: [], cc: [], bcc: [] };
  for (var i = 1; i < v.length; i++) {
    var email = bpText_(v[i][1]);
    if (!email || bpText_(v[i][4]).toLowerCase() !== 'yes') { continue; }
    var grp = bpText_(v[i][2]).toLowerCase();
    if (grp in g) { g[grp].push(email); }
  }
  return g;
}

function bpToDate_(v) {
  if (Object.prototype.toString.call(v) === '[object Date]') { return v; }
  var m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(bpText_(v));
  return m ? new Date(Number(m[3]), Number(m[1]) - 1, Number(m[2])) : null;
}

function bpFolderByName_(parent, name) {
  var it = parent.getFoldersByName(name);
  return it.hasNext() ? it.next() : null;
}

/* ---------- 1. the month folder ---------- */

function bpFindMonthFolder_(create) {
  var s = bpKeyValues_('Settings'), m = bpKeyValues_('Month');
  var rootName = bpText_(s.root_folder_name), monthName = bpText_(m.month_folder_name);
  var d = bpToDate_(m.meeting_date);
  if (!rootName || !monthName || !d) {
    throw new Error('E20: fill in root_folder_name (Settings) and meeting_date and month_folder_name (Month).');
  }
  var rootIt = DriveApp.getFoldersByName(rootName);
  if (!rootIt.hasNext()) { throw new Error('E15: the shared packet folder was not found in Drive.'); }
  var root = rootIt.next();
  var yearName = String(d.getFullYear());
  var year = bpFolderByName_(root, yearName);
  if (!year) {
    if (!create) { throw new Error('E16: the ' + yearName + ' folder was not found.'); }
    year = root.createFolder(yearName);
  }
  var month = bpFolderByName_(year, monthName);
  if (!month) {
    if (!create) { throw new Error('E21: this month\'s folder was not found. Use "1. Make this month\'s folder" first.'); }
    month = year.createFolder(monthName);
  }
  return month;
}

function bpMakeMonthFolder() {
  var ui = SpreadsheetApp.getUi();
  try {
    var f = bpFindMonthFolder_(true);
    ui.alert('Month folder ready', 'This month\'s folder is ready:\n' + f.getUrl() + '\n\nDrop the reports into it, then use "2. Make PDF copies".', ui.ButtonSet.OK);
  } catch (e) { ui.alert('Stopped', String(e.message || e), ui.ButtonSet.OK); }
}

/* ---------- 2. PDF copies ---------- */

function bpMakePdfCopies() {
  var ui = SpreadsheetApp.getUi();
  try {
    var s = bpKeyValues_('Settings');
    var combinedName = bpText_(s.combined_packet_filename);
    var month = bpFindMonthFolder_(false);
    var reports = bpReports_();
    var minutes = reports.filter(function (r) { return r.role === 'minutes'; })[0];
    var unmatchedOrder = minutes ? minutes.order - 0.5 : 98;

    var out = bpFolderByName_(month, BP_PDF_FOLDER) || month.createFolder(BP_PDF_FOLDER);
    var old = [], oldIt = out.getFiles();   // our own earlier copies only; retired after the new ones exist
    while (oldIt.hasNext()) { old.push(oldIt.next()); }

    var items = [], skipped = [];
    var files = month.getFiles();
    while (files.hasNext()) {
      var f = files.next(), name = f.getName(), lower = name.toLowerCase();
      if (name === combinedName || name.charAt(0) === '.' || name.indexOf('~$') === 0) { continue; }
      var match = null;
      for (var i = 0; i < reports.length; i++) {
        if (reports[i].keyword && lower.indexOf(reports[i].keyword) !== -1) { match = reports[i]; break; }
      }
      var type = f.getMimeType(), blob = null;
      if (BP_GOOGLE_TYPES.indexOf(type) !== -1) { blob = f.getAs(MimeType.PDF); }
      else if (type === 'application/pdf') { blob = f.getBlob(); }
      if (!blob) { skipped.push(name); continue; }
      items.push({
        order: match ? match.order : unmatchedOrder,
        label: match ? match.name : name.replace(/\.[^.]+$/, ''),
        inPacket: match ? (match.inPacket && match.active) : false,  // unmatched files stay out until a report row claims them
        matched: !!match,
        inactive: !!match && !match.active,
        blob: blob
      });
    }
    items.sort(function (a, b) { return a.order - b.order; });

    var lines = [['Packet order', 'File made', 'In combined packet', 'Matched a report row']];
    var n = 0;
    items.forEach(function (it) {
      var prefix;
      if (it.inPacket) { n++; prefix = (n < 10 ? '0' : '') + n + ' - '; } else { prefix = 'Separate - '; }
      var fileName = prefix + it.label + '.pdf';
      it.blob.setName(fileName);
      out.createFile(it.blob);
      lines.push([it.inPacket ? n : '', fileName, it.inPacket ? 'Yes' : (it.inactive ? 'No, its report row is not active' : (it.matched ? 'No, share by its own link' : 'No, no report row matches it')), it.matched ? 'Yes' : 'No, check the keyword']);
    });
    old.forEach(function (f) { f.setTrashed(true); });
    skipped.forEach(function (nm) { lines.push(['', nm, 'Not converted (E22)', '']); });
    bpWriteLastRun_(lines);

    var msg = items.length + ' PDF copies saved in the "' + BP_PDF_FOLDER + '" folder.\n';
    if (skipped.length) { msg += '\n' + skipped.length + ' file(s) could not be converted (E22). Open each in Drive, choose File > Save as Google Docs (or Sheets), then run this step again.\n'; }
    if (!items.length) { msg = 'No files to copy were found in this month\'s folder (E23).'; }
    msg += '\nSee the "Last run" tab for the merge order.';
    ui.alert('PDF copies', msg, ui.ButtonSet.OK);
  } catch (e) { ui.alert('Stopped', String(e.message || e), ui.ButtonSet.OK); }
}

function bpWriteLastRun_(rows) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName('Last run') || ss.insertSheet('Last run');
  sh.clear();
  sh.getRange(1, 1, rows.length, rows[0].length).setValues(rows);
  sh.getRange(1, 1, 1, rows[0].length).setFontWeight('bold');
  sh.autoResizeColumns(1, rows[0].length);
}

/* ---------- 3. the email draft ---------- */

function bpEsc_(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }

// A line such as "Budget for approval | https://example.org/budget" becomes a link.
function bpLine_(line) {
  var parts = line.split('|');
  if (parts.length === 2 && /^https?:\/\//.test(parts[1].trim())) {
    return { text: parts[0].trim() + ' (' + parts[1].trim() + ')',
             html: '<a href="' + bpEsc_(parts[1].trim()) + '">' + bpEsc_(parts[0].trim()) + '</a>' };
  }
  return { text: line.trim(), html: bpEsc_(line.trim()) };
}

function bpLines_(v) {
  return bpText_(v).split(/\r?\n/).map(function (x) { return x.trim(); }).filter(function (x) { return x; });
}

function bpFindFile_(folder, keyword) {
  if (!keyword) { return null; }
  var it = folder.getFiles();
  while (it.hasNext()) {
    var f = it.next();
    if (f.getName().toLowerCase().indexOf(keyword.toLowerCase()) !== -1) { return f; }
  }
  return null;
}

function bpMakeEmailDraft() {
  var ui = SpreadsheetApp.getUi();
  try {
    var s = bpKeyValues_('Settings'), m = bpKeyValues_('Month');
    var tz = Session.getScriptTimeZone();
    var d = bpToDate_(m.meeting_date);
    if (!d) { throw new Error('E20: meeting_date on the Month tab is missing or not in mm/dd/yyyy form.'); }
    var month = bpFindMonthFolder_(false);
    var contacts = bpContacts_();
    if (!contacts.to.length) { throw new Error('E24: no active contact is in the To group on the Contacts tab.'); }
    var warnings = [];

    var timeText = bpText_(s.meeting_time);
    var startTime = timeText.split(/\s+to\s+|\s*-\s*/)[0];
    var subject = bpText_(s.email_subject_pattern)
      .replace('[org_name]', bpText_(s.org_name))
      .replace('[date]', Utilities.formatDate(d, tz, 'M/d/yy'))
      .replace('[start_time]', startTime)
      .replace('[time]', timeText);
    var longDate = Utilities.formatDate(d, tz, 'EEEE, MMMM d, yyyy');

    var text = [], html = [];
    function para(t, h) { text.push(t, ''); html.push('<p>' + (h || bpEsc_(t)) + '</p>'); }

    para(bpText_(s.org_name) + ' ' + bpText_(s.board_name) + ' and Staff,');
    para('Please find the read-ahead materials for the ' + longDate + ' board meeting at ' + timeText +
         '. ' + bpText_(s.meeting_location) + '. Video details are at the end of this email.');
    if (bpText_(m.notes_for_email)) { para(bpText_(m.notes_for_email)); }

    var missing = bpText_(m.missing_reports_auto);
    if (missing) {
      para(missing + ' did not arrive in time for this send, so ' + (missing.indexOf(',') === -1 ? 'it is' : 'they are') + ' not included in this month\'s packet. All other materials appear as normal.');
    }

    var callouts = bpLines_(m.approval_items).concat(bpLines_(m.callouts));
    if (callouts.length) {
      var ct = ['For approval or attention this month:'], ch = ['<p><b>For approval or attention this month:</b></p><ul>'];
      callouts.forEach(function (l) { var x = bpLine_(l); ct.push('- ' + x.text); ch.push('<li>' + x.html + '</li>'); });
      text.push(ct.join('\n'), ''); html.push(ch.join('') + '</ul>');
    }

    // Standing links
    var linkText = ['Reports and documents:'], linkHtml = ['<p><b>Reports and documents:</b></p>'];
    if (bpText_(s.recurring_ask)) { linkText.push(bpText_(s.recurring_ask)); linkHtml.push('<p>' + bpEsc_(bpText_(s.recurring_ask)) + '</p>'); }
    linkHtml.push('<ul>');
    function addLink(label, url) {
      linkText.push('- ' + label + ': ' + url);
      linkHtml.push('<li><a href="' + bpEsc_(url) + '">' + bpEsc_(label) + '</a></li>');
    }
    var combined = bpFindFile_(month, bpText_(s.combined_packet_filename)) ||
                   (bpFolderByName_(month, BP_PDF_FOLDER) ? bpFindFile_(bpFolderByName_(month, BP_PDF_FOLDER), bpText_(s.combined_packet_filename)) : null);
    if (combined) { addLink('Combined packet (one file, easy to print)', combined.getUrl()); }
    else { warnings.push('The combined packet file was not found in this month\'s folder (E25). The draft has no link for it.'); }
    addLink('Files folder (every individual document)', month.getUrl());

    var pdfFolder = bpFolderByName_(month, BP_PDF_FOLDER);
    bpReports_().forEach(function (r) {
      if (!r.active || r.inPacket || r.role === 'minutes') { return; }
      var f = (pdfFolder && bpFindFile_(pdfFolder, r.name)) || bpFindFile_(month, r.keyword);
      if (f) { addLink(r.name, f.getUrl()); }
      else { warnings.push('No file found for the separate report "' + r.name + '". The draft has no link for it.'); }
    });
    if (bpText_(s.contact_list_url)) { addLink('Board contact list', bpText_(s.contact_list_url)); }
    [1, 2].forEach(function (n) {
      if (bpText_(s['extra_link_' + n + '_label']) && bpText_(s['extra_link_' + n + '_url'])) {
        addLink(bpText_(s['extra_link_' + n + '_label']), bpText_(s['extra_link_' + n + '_url']));
      }
    });
    text.push(linkText.join('\n'), ''); html.push(linkHtml.join('') + '</ul>');

    if (bpText_(s.video_details)) { para(bpText_(s.video_details)); }
    para(bpText_(s.sender_name));

    if (month.getSharingAccess() === DriveApp.Access.PRIVATE) {
      warnings.push('This month\'s folder may not be link-shared yet. Open the links in a private browser window before you send the draft.');
    }

    var options = { htmlBody: html.join('\n') };
    if (contacts.cc.length) { options.cc = contacts.cc.join(','); }
    if (contacts.bcc.length) { options.bcc = contacts.bcc.join(','); }
    GmailApp.createDraft(contacts.to.join(','), subject, text.join('\n'), options);

    var msg = 'A draft is waiting in Gmail > Drafts. It has NOT been sent.\n\nSubject: ' + subject +
      '\nTo: ' + contacts.to.length + ' | Cc: ' + contacts.cc.length + ' | Bcc: ' + contacts.bcc.length;
    if (bpText_(s.reviewer_name)) { msg += '\n\nAsk ' + bpText_(s.reviewer_name) + ' to read it before it goes out.'; }
    if (warnings.length) { msg += '\n\nCheck before sending:\n- ' + warnings.join('\n- '); }
    ui.alert('Draft ready', msg, ui.ButtonSet.OK);
  } catch (e) { ui.alert('Stopped', String(e.message || e), ui.ButtonSet.OK); }
}
