/**
 * Customer Research kit: search-suggestion pull (low-cost version, Apps Script)
 *
 * What it does: for each seed term in the Config tab (up to max_seed_terms),
 * asks Google's public search-suggestion address for suggestions, including
 * the term followed by each letter a to z, and appends new ones to the
 * Autocomplete tab. Every run, passed or failed, is recorded in the RunLog tab.
 * If a scheduled run fails, it emails the notify_email address from Config.
 *
 * Honest limits: the suggestion address is not an official Google product, so
 * Google may change or block it. If that happens the run is logged as failed
 * and you can type suggestions in by hand (guide CR-FR-02). The script only
 * reads suggestions. It never posts anything anywhere.
 */

var PAUSE_MS = 2000; // wait between requests, to stay polite

// Called from onOpen in checkup.gs, so the project has only one onOpen.
function addPullMenu_() {
  SpreadsheetApp.getUi()
    .createMenu('Customer research')
    .addItem('Pull search suggestions now', 'pullSuggestionsManual')
    .addItem('Schedule monthly pull', 'installMonthlyTrigger')
    .addItem('Remove monthly schedule', 'removeMonthlyTrigger')
    .addToUi();
}

function readConfig_(ss) {
  var sheet = ss.getSheetByName('Config');
  if (!sheet) { throw new Error('Config tab is missing (step CR-FR-01-2)'); }
  var rows = sheet.getRange(1, 1, sheet.getLastRow(), 2).getValues();
  var cfg = {};
  rows.forEach(function (r) { cfg[String(r[0]).trim()] = String(r[1]).trim(); });
  return cfg;
}

function logRun_(ss, status, rowsAdded, message) {
  var log = ss.getSheetByName('RunLog');
  if (!log) { return; }
  log.appendRow([new Date(), 'search-suggestions', status, rowsAdded, message]);
}

function pullSuggestionsManual() {
  runPull_(false);
}

// Called by the monthly trigger.
function pullSuggestionsScheduled() {
  runPull_(true);
}

function runPull_(scheduled) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var cfg;
  try {
    cfg = readConfig_(ss);
    var seeds = (cfg.seed_terms || '').split(',').map(function (s) { return s.trim(); }).filter(String);
    var maxSeeds = Math.min(parseInt(cfg.max_seed_terms || '3', 10) || 3, 5);
    if (!seeds.length) { throw new Error('seed_terms in Config is blank (step CR-FR-02-1)'); }
    seeds = seeds.slice(0, maxSeeds);

    var tab = ss.getSheetByName('Autocomplete');
    if (!tab) { throw new Error('Autocomplete tab is missing (step CR-LC-02-2)'); }

    var existing = {};
    var last = tab.getLastRow();
    if (last > 1) {
      tab.getRange(2, 2, last - 1, 2).getValues().forEach(function (r) { existing[r[0] + '|' + r[1]] = true; });
    }

    var today = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MM/dd/yyyy');
    var added = [];
    var fetchedAny = false;
    var failedFetches = 0;

    seeds.forEach(function (seed) {
      var queries = [seed];
      'abcdefghijklmnopqrstuvwxyz'.split('').forEach(function (ch) { queries.push(seed + ' ' + ch); });
      queries.forEach(function (q) {
        var url = 'https://suggestqueries.google.com/complete/search?client=firefox&q=' + encodeURIComponent(q);
        try {
          var resp = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
          if (resp.getResponseCode() === 200) {
            fetchedAny = true;
            var data = JSON.parse(resp.getContentText());
            (data[1] || []).forEach(function (sug) {
              var clean = String(sug).trim();
              // Keep only plausible search phrases, never anything that looks like a link or code.
              if (clean && clean.length < 120 && !/https?:|<|>|\{|\}/.test(clean) && !existing[seed + '|' + clean]) {
                existing[seed + '|' + clean] = true;
                added.push([today, seed, literal_(clean), '']);
              }
            });
          } else {
            failedFetches++;
          }
        } catch (err) {
          failedFetches++;
        }
        Utilities.sleep(PAUSE_MS);
      });
    });

    if (!fetchedAny) {
      throw new Error('Google returned no usable answers (it may have blocked or changed the address). Step CR-LC-02-4, fix E12.');
    }
    if (added.length) {
      tab.getRange(tab.getLastRow() + 1, 1, added.length, 4).setValues(added);
    }
    logRun_(ss, 'ok', added.length, failedFetches + ' requests failed');
  } catch (e) {
    logRun_(ss, 'FAILED', 0, String(e.message || e));
    if (scheduled && cfg && cfg.notify_email) {
      MailApp.sendEmail(cfg.notify_email, 'Customer research pull failed',
        'The monthly search-suggestion pull failed. Reason: ' + (e.message || e) +
        '\nOpen the RunLog tab in your Sheet for details. The earlier data is still there.');
    }
    if (!scheduled) { SpreadsheetApp.getUi().alert('The pull failed: ' + (e.message || e)); }
  }
}

function installMonthlyTrigger() {
  removeMonthlyTrigger();
  ScriptApp.newTrigger('pullSuggestionsScheduled').timeBased().onMonthDay(1).atHour(8).create();
  SpreadsheetApp.getUi().alert('Scheduled: this will run on the first of each month, around 8 a.m. Each run is recorded in the RunLog tab.');
}

function removeMonthlyTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'pullSuggestionsScheduled') { ScriptApp.deleteTrigger(t); }
  });
}

/** Keeps outside text as plain text: a leading =, +, - or @ would otherwise make a formula. */
function literal_(v) {
  return (typeof v === 'string' && /^[=+\-@]/.test(v)) ? "'" + v : v;
}
