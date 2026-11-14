/**
 * Website check-up kit: monthly speed pull (Google Apps Script)
 * Kit code WC, low-cost version, kit version 0.1.0
 *
 * What this does
 *   Once a month (or when you pick "Pull speed now" from the Kit help menu) it asks
 *   Google's PageSpeed Insights for the mobile result of each address listed on
 *   the Pages tab (column A) and of your home page, then writes the numbers
 *   into the Pages tab and adds one line to the Monthly tab.
 *
 * Put this file in the same Apps Script project as checkup.gs. The Kit help menu
 * in checkup.gs adds the "Pull speed now" item when this file is present.
 *
 * Your key
 *   Save it under Project Settings > Script Properties, with the name
 *   PAGESPEED_API_KEY. This script reads it but never prints it, never writes
 *   it into a cell, and never sends it anywhere except Google's own address.
 *
 * Failure rule
 *   If a pull fails, the failure is written in the Notes column that same day.
 *   A blank month never passes quietly.
 */

var PSI_URL = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed';
var MAX_PAGES = 20;

function getSetting_(ss, name) {
  var rows = ss.getSheetByName('Config').getDataRange().getValues();
  for (var r = 1; r < rows.length; r++) {
    if (String(rows[r][0]).trim() === name) return String(rows[r][1]).trim();
  }
  return '';
}

function psiRequest_(address) {
  var key = PropertiesService.getScriptProperties().getProperty('PAGESPEED_API_KEY');
  var url = PSI_URL + '?strategy=mobile&category=performance&url=' + encodeURIComponent(address);
  if (key) url += '&key=' + encodeURIComponent(key);
  var data;
  try {
    var response = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
    var code = response.getResponseCode();
    if (code !== 200) return { error: 'HTTP ' + code };
    data = JSON.parse(response.getContentText());
  } catch (e) {
    // A timeout, a network error or an unreadable answer. The message never carries the key.
    return { error: safeMessage_(e) };
  }
  var score = null;
  try { score = Math.round(data.lighthouseResult.categories.performance.score * 100); } catch (e) {}
  var field = (data.loadingExperience && data.loadingExperience.metrics) || {};
  function p75(name) { return field[name] && field[name].percentile !== undefined ? field[name].percentile : ''; }
  var lcp = p75('LARGEST_CONTENTFUL_PAINT_MS');
  var inp = p75('INTERACTION_TO_NEXT_PAINT');
  var cls = p75('CUMULATIVE_LAYOUT_SHIFT_SCORE');
  return {
    score: score,
    lcpSeconds: lcp === '' ? '' : Math.round(lcp / 100) / 10,
    inpMs: inp,
    cls: cls === '' ? '' : cls / 100
  };
}

function safeMessage_(e) {
  return String((e && e.message) || e).replace(/https?:\/\/\S+/g, '(address)').slice(0, 200);
}

function pullSpeedNow() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var monthly = ss.getSheetByName('Monthly');
  var today = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MM/dd/yyyy');
  var month = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MM/yyyy');
  try {
    pullSpeed_(ss, monthly, today, month);
  } catch (e) {
    // Even a run that stops early leaves this month's failure on the Monthly tab.
    monthly.appendRow([month, '', '', '', '', '', '', '', '', '', '', '', '', 'Speed pull stopped on ' + today + ': ' + safeMessage_(e)]);
    throw e;
  }
}

function pullSpeed_(ss, monthly, today, month) {
  var pages = ss.getSheetByName('Pages');
  var home = getSetting_(ss, 'site_url');

  // Addresses from the Pages tab, column A, from row 2 down.
  var last = pages.getLastRow();
  var addresses = [];
  if (last > 1) {
    pages.getRange(2, 1, last - 1, 1).getValues().forEach(function (row, i) {
      var a = String(row[0]).trim();
      if (a) addresses.push({ row: i + 2, url: a });
    });
  }
  addresses = addresses.slice(0, MAX_PAGES);

  var failures = 0;
  var homeScore = '';
  addresses.forEach(function (item) {
    var result = psiRequest_(item.url);
    if (result.error) {
      failures++;
      pages.getRange(item.row, 14).setValue('Speed pull failed ' + today + ': ' + result.error);
    } else {
      pages.getRange(item.row, 9, 1, 4).setValues([[result.score, result.lcpSeconds, result.inpMs, result.cls]]);
      pages.getRange(item.row, 13).setValue(today);
      if (item.url.replace(/\/$/, '') === home.replace(/\/$/, '')) homeScore = result.score;
    }
    Utilities.sleep(1500); // be polite to the service
  });

  if (homeScore === '' && home) {
    var homeResult = psiRequest_(home);
    if (homeResult.error) failures++; else homeScore = homeResult.score;
  }

  var note = failures ? failures + ' speed pull(s) failed on ' + today + '. See the Pages tab, Notes column.' : '';
  monthly.appendRow([month, '', '', '', '', homeScore, '', '', '', '', '', '', '', note]);
  SpreadsheetApp.getActive().toast(failures ? 'Done, with ' + failures + ' failure(s). See the Notes column.' : 'Speed pull finished.', 'Website check-up', 6);
}

// Run this once to set up the monthly timer (see setup guide WC-LC-02).
function createMonthlyTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'pullSpeedNow') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('pullSpeedNow').timeBased().onMonthDay(1).atHour(6).create();
}
