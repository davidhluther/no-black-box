/**
 * Grants kit weekly sweep (low-cost version). Looks for new federal funding notices on
 * Grants.gov every week and lists them, scored, on a "Sweep" tab of your tracker.
 *
 * What it does
 *   1. Once a week it asks Grants.gov (the US government's public grant listing) for open and
 *      forecasted opportunities that nonprofits can apply for, using the search words below.
 *   2. It scores each notice by simple word rules, and adds new ones to the Sweep tab.
 *   3. It writes a line to the SweepLog tab BEFORE it starts, and another when it ends, so a
 *      run that never finishes still leaves a trace.
 *
 * What it never does
 *   It never contacts a funder, applies for anything, or sends your organization's data
 *   anywhere. The only thing that leaves your sheet is your search words, sent to Grants.gov.
 *
 * If it fails or misses a week
 *   A failure is written to SweepLog and emailed to the address in Settings ("Grants contact
 *   email") the same day. A daily freshness check emails you if no successful run has been
 *   recorded in the last eight days. A missed week counts as a failure even when old results
 *   are still on the tab.
 *
 * To install, follow GR-LC-02 in the kit's setup folder. Edit the search words and scoring
 * words below (between the quotation marks) to fit your organization, then run
 * installSweepTriggers once.
 *
 * @OnlyCurrentDoc
 */

var SWEEP = {
  // Words Grants.gov searches for. Add or remove to fit your work.
  keywords: ['food pantry', 'emergency food assistance', 'community development', 'housing assistance'],
  // Words in a notice's title that raise or lower its score.
  positiveWords: ['community', 'food', 'housing', 'hunger', 'rural', 'families', 'nonprofit'],
  negativeWords: ['research', 'clinical', 'laboratory', 'international', 'foreign'],
  // Agency codes (the start of the code) that raise or lower the score.
  goodAgencies: ['USDA', 'HUD', 'HHS-ACF', 'DOL'],
  badAgencies: ['NSF', 'NASA', 'DOD'],
  rowsPerSearch: 50,
  maxDaysWithoutSuccess: 8,
  sweepTab: 'Sweep',
  logTab: 'SweepLog'
};

var SWEEP_HEADERS = ['Key', 'Agency', 'Title', 'Closes', 'Link', 'Score', 'Tier', 'Why', 'First seen', 'Last seen', 'Status'];
var LOG_HEADERS = ['When', 'Event', 'Detail'];

/** Scores one Grants.gov hit. Returns { score, tier, why }. Pure function. */
function scoreOpportunity_(hit, cfg) {
  var title = String(hit.title || '').toLowerCase();
  var agency = String(hit.agencyCode || hit.agency || '').toUpperCase();
  var score = 20, why = [];
  if (cfg.goodAgencies.some(function (a) { return agency.indexOf(a) === 0; })) { score += 25; why.push('agency often funds community work'); }
  if (cfg.badAgencies.some(function (a) { return agency.indexOf(a) === 0; })) { score -= 30; why.push('research or defense agency'); }
  var pos = cfg.positiveWords.filter(function (w) { return title.indexOf(w) !== -1; });
  var neg = cfg.negativeWords.filter(function (w) { return title.indexOf(w) !== -1; });
  score += 8 * Math.min(pos.length, 4) - 12 * neg.length;
  if (pos.length) { why.push('title: ' + pos.slice(0, 4).join(', ')); }
  if (neg.length) { why.push('off-fit: ' + neg.join(', ')); }
  score = Math.max(0, Math.min(100, score));
  var tier = score >= 70 ? 'Tier 2: look now' : score >= 45 ? 'Tier 3: maybe' : 'skip';
  return { score: score, tier: tier, why: why.join('; ') };
}

/**
 * Merges new hits into existing rows (an object keyed by Key). Pure function.
 * Returns the number of rows that were new.
 */
function mergeCandidates_(existing, hits, today, cfg) {
  var added = 0;
  hits.forEach(function (h) {
    var key = 'grantsgov:' + h.number;
    var s = scoreOpportunity_(h, cfg);
    var row = existing[key];
    if (!row) {
      added++;
      row = existing[key] = { key: key, firstSeen: today, status: 'new' };
    }
    row.agency = h.agency || h.agencyCode || '';
    row.title = h.title || '';
    row.closes = h.closeDate || '';
    row.link = 'https://www.grants.gov/search-results-detail/' + h.id;
    row.score = s.score; row.tier = s.tier; row.why = s.why; row.lastSeen = today;
  });
  return added;
}

function runWeeklySweep() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var today = Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), 'MM/dd/yyyy');
  var log = tab_(ss, SWEEP.logTab, LOG_HEADERS);
  var sheet = tab_(ss, SWEEP.sweepTab, SWEEP_HEADERS);
  appendLog_(log, 'attempting', 'slot ' + today);

  var existing = loadRows_(sheet);
  var failed = [], found = 0, hits = [];
  SWEEP.keywords.forEach(function (kw) {
    try {
      var res = UrlFetchApp.fetch('https://api.grants.gov/v1/api/search2', {
        method: 'post',
        contentType: 'application/json',
        payload: JSON.stringify({ keyword: kw, oppStatuses: 'forecasted|posted', eligibilities: '12', rows: SWEEP.rowsPerSearch }),
        muteHttpExceptions: true
      });
      var code = res.getResponseCode();
      if (code !== 200) { throw new Error('Grants.gov answered with status ' + code); }
      var body = JSON.parse(res.getContentText());
      if (body.errorcode) { throw new Error('Grants.gov error ' + body.errorcode); }
      var list = (body.data && body.data.oppHits) || [];
      found += list.length;
      hits = hits.concat(list);
    } catch (e) {
      failed.push(kw);
      appendLog_(log, 'failed', 'search "' + kw + '": ' + String(e).slice(0, 200));
    }
  });
  var added = mergeCandidates_(existing, hits, today, SWEEP);
  writeRows_(sheet, existing);
  var outcome = failed.length === 0 ? 'done' : (failed.length === SWEEP.keywords.length ? 'failed' : 'partial');
  appendLog_(log, outcome, 'found ' + found + ', new ' + added + ', failed searches ' + failed.length);
  if (failed.length > 0) {
    alert_(ss, 'Grants sweep ' + outcome, failed.length + ' of ' + SWEEP.keywords.length +
      ' searches failed on ' + today + '. See the SweepLog tab. Nothing was lost; old results are still on the Sweep tab.');
  }
}

/** Daily. Emails if no successful run was recorded recently, so a silent miss cannot last. */
function checkSweepFreshness() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var log = ss.getSheetByName(SWEEP.logTab);
  var lastOk = null;
  if (log && log.getLastRow() >= 2) {
    var rows = log.getRange(2, 1, log.getLastRow() - 1, 2).getValues();
    rows.forEach(function (r) { if (r[1] === 'done' || r[1] === 'partial') { lastOk = new Date(r[0]); } });
  }
  var ageDays = lastOk ? (new Date() - lastOk) / 86400000 : Infinity;
  if (ageDays > SWEEP.maxDaysWithoutSuccess) {
    alert_(ss, 'Grants sweep has not run', 'No successful sweep has been recorded in the last ' +
      SWEEP.maxDaysWithoutSuccess + ' days. Open the Apps Script Executions page, or run runWeeklySweep by hand.');
  }
}

/** Run once. Sets the weekly sweep (Thursdays, about 8 a.m.) and the daily freshness check. */
function installSweepTriggers() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    var f = t.getHandlerFunction();
    if (f === 'runWeeklySweep' || f === 'checkSweepFreshness') { ScriptApp.deleteTrigger(t); }
  });
  ScriptApp.newTrigger('runWeeklySweep').timeBased().onWeekDay(ScriptApp.WeekDay.THURSDAY).atHour(8).create();
  ScriptApp.newTrigger('checkSweepFreshness').timeBased().everyDays(1).atHour(9).create();
  SpreadsheetApp.getUi().alert('Done. The sweep will run on Thursdays and the freshness check every day.');
}

/* Helpers that touch the spreadsheet. */

function tab_(ss, name, headers) {
  var sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    sheet.setFrozenRows(1);
  }
  return sheet;
}

function appendLog_(sheet, event, detail) {
  sheet.appendRow([new Date(), event, detail]);
}

function loadRows_(sheet) {
  var out = {};
  var last = sheet.getLastRow();
  if (last < 2) { return out; }
  sheet.getRange(2, 1, last - 1, SWEEP_HEADERS.length).getValues().forEach(function (r) {
    if (!r[0]) { return; }
    out[r[0]] = { key: r[0], agency: r[1], title: r[2], closes: r[3], link: r[4], score: r[5], tier: r[6],
                  why: r[7], firstSeen: r[8], lastSeen: r[9], status: r[10] };
  });
  return out;
}

function writeRows_(sheet, rows) {
  var list = Object.keys(rows).map(function (k) { return rows[k]; })
    .sort(function (a, b) { return Number(b.score) - Number(a.score); });
  var last = sheet.getLastRow();
  if (last >= 2) { sheet.getRange(2, 1, last - 1, SWEEP_HEADERS.length).clearContent(); }
  if (!list.length) { return; }
  var values = list.map(function (r) {
    return [r.key, r.agency, r.title, r.closes, r.link, r.score, r.tier, r.why, r.firstSeen, r.lastSeen, r.status];
  });
  sheet.getRange(2, 1, values.length, SWEEP_HEADERS.length).setValues(values);
}

function alert_(ss, subject, text) {
  var settings = ss.getSheetByName('Settings');
  var to = settings ? String(settings.getRange('B8').getDisplayValue()).trim() : '';
  if (!to) { to = Session.getEffectiveUser().getEmail(); }
  MailApp.sendEmail(to, subject, text);
}
