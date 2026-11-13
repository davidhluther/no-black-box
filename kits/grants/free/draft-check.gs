/**
 * Grants kit draft checker (optional). Adds "Check draft numbers" to the Help menu.
 *
 * What it does
 *   Reads the draft you pasted into the DraftCheck tab (cell B1), finds every number and
 *   claim ID in it, and compares them with the Claims tab. A number passes when it matches
 *   the Value of a claim whose Status starts with source-verified or external-verified, or
 *   when you listed it in B2 (the ask amount, deadlines, the funder's own figures).
 *   Small plain counts of ten or fewer ("three staff") are skipped.
 *
 * What it never does
 *   It does not send your draft anywhere. It has no web requests, email or uploads. It only
 *   reads DraftCheck B1 and B2 and the Claims tab, and writes results into DraftCheck rows 6
 *   and down on this same spreadsheet.
 *
 * It needs checkup.gs in the same project, which supplies the Help menu.
 * To install, follow GR-FR-04 in the kit's setup folder.
 *
 * @OnlyCurrentDoc
 */

var DRAFT_NUM = /(?<![\w.])\$?\d[\d,]*(?:\.\d+)?%?/g;
var DRAFT_ID = /\b[A-Z]{2,8}-\d{2,3}\b/g;

function addDraftMenuItem_(menu) {
  menu.addItem('Check draft numbers', 'checkDraftNumbers');
}

/** '$1,234.50' -> ['1234.5']; '35%' -> ['35', '0.35']. Returns [] if not a number. */
function normNumber_(token) {
  var t = token.replace(/\$/g, '').replace(/,/g, '').replace(/\.$/, '');
  var pct = /%$/.test(t);
  t = t.replace(/%$/, '');
  var v = Number(t);
  if (t === '' || isNaN(v)) { return []; }
  var out = [String(v)];
  if (pct) { out.push(String(v / 100)); }
  return out;
}

/**
 * claims: array of [id, value, status] (display text). draft and allowText are strings.
 * Returns an array of [thing, verdict, claimIds] rows, one per distinct number or ID.
 */
function checkDraftText_(draft, allowText, claims) {
  var usable = {};   // normalized value -> [ids]
  var status = {};   // id -> lowercase status
  claims.forEach(function (c) {
    var id = String(c[0]).trim();
    var st = String(c[2]).trim().toLowerCase();
    if (!id) { return; }
    status[id] = st;
    if (st.indexOf('source-verified') === 0 || st.indexOf('external-verified') === 0) {
      (String(c[1]).match(DRAFT_NUM) || []).forEach(function (tok) {
        normNumber_(tok).forEach(function (n) {
          usable[n] = usable[n] || [];
          if (usable[n].indexOf(id) === -1) { usable[n].push(id); }
        });
      });
    }
  });
  var allow = {};
  (String(allowText).match(DRAFT_NUM) || []).forEach(function (tok) {
    normNumber_(tok).forEach(function (n) { allow[n] = true; });
  });

  var seen = {}, rows = [];
  (String(draft).replace(DRAFT_ID, ' ').match(DRAFT_NUM) || []).forEach(function (tok) {
    if (seen[tok]) { return; }
    seen[tok] = true;
    var ns = normNumber_(tok);
    if (!ns.length) { return; }
    var v = Number(ns[0]);
    if (v <= 10 && tok.indexOf('%') === -1 && tok.indexOf('$') === -1) { return; }
    var ids = [], ok = false, allowed = false;
    ns.forEach(function (n) {
      if (usable[n]) { ok = true; usable[n].forEach(function (id) { if (ids.indexOf(id) === -1) { ids.push(id); } }); }
      if (allow[n]) { allowed = true; }
    });
    if (ok) { rows.push([tok, 'matches a verified claim', ids.join(', ')]); }
    else if (allowed) { rows.push([tok, 'on your allowed list', '']); }
    else { rows.push([tok, 'NOT IN REGISTER', '']); }
  });

  var seenId = {};
  (String(draft).match(DRAFT_ID) || []).forEach(function (id) {
    if (seenId[id]) { return; }
    seenId[id] = true;
    if (!(id in status)) { rows.push([id, 'claim ID NOT IN REGISTER', '']); }
    else if (status[id].indexOf('source-verified') !== 0 && status[id].indexOf('external-verified') !== 0) {
      rows.push([id, 'claim status is not usable', '']);
    }
  });
  return rows;
}

function checkDraftNumbers() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('DraftCheck');
  var claimsSheet = ss.getSheetByName('Claims');
  var ui = SpreadsheetApp.getUi();
  if (!sheet || !claimsSheet) {
    ui.alert('The DraftCheck and Claims tabs are needed. Run Help, then Run check-up, and look for code E01.');
    return;
  }
  var draft = sheet.getRange('B1').getDisplayValue();
  if (String(draft).replace(/\s/g, '') === '') {
    ui.alert('Paste your draft into cell B1 of the DraftCheck tab first.');
    return;
  }
  var allowText = sheet.getRange('B2').getDisplayValue();
  var last = claimsSheet.getLastRow();
  var claims = last >= 2 ? claimsSheet.getRange(2, 1, last - 1, 6).getDisplayValues()
    .map(function (r) { return [r[0], r[2], r[5]]; }) : [];
  var rows = checkDraftText_(draft, allowText, claims);

  var oldLast = sheet.getLastRow();
  if (oldLast >= 6) { sheet.getRange(6, 1, oldLast - 5, 3).clearContent(); }
  if (rows.length === 0) {
    sheet.getRange(6, 1, 1, 3).setValues([['(no numbers over ten found)', '', '']]);
  } else {
    sheet.getRange(6, 1, rows.length, 3).setValues(rows);
  }
  var bad = rows.filter(function (r) { return /NOT IN REGISTER|not usable/.test(r[1]); }).length;
  ui.alert(bad === 0
    ? 'Every number in the draft matches a verified claim or your allowed list. Results are in rows 6 and down.'
    : bad + ' item(s) need a source. Fix the draft or add a verified claim, then run this again. Results are in rows 6 and down.');
}
