/**
 * Idea to Live Post kit: pull feeds into the Ideas tab (low-cost version).
 * Reads the "Feeds" tab (columns: name, url), fetches each feed, and adds new items
 * from the last N days to the "Ideas" tab. Failures are recorded in the "Log" tab,
 * never skipped silently. Read-only: it only reads public feeds.
 */
var WINDOW_DAYS = 7;

function addIdeasMenu() {
  SpreadsheetApp.getUi().createMenu('Ideas')
    .addItem('Fetch feeds now', 'fetchFeeds')
    .addItem('Run every Monday morning', 'installWeeklyTrigger')
    .addToUi();
}

function logRow_(ss, what, status, detail) {
  var log = ss.getSheetByName('Log') || ss.insertSheet('Log');
  if (log.getLastRow() === 0) { log.appendRow(['when', 'what', 'status', 'detail']); }
  log.appendRow([new Date(), what, status, String(detail || '').substring(0, 300)]);
}

function fetchFeeds() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var feeds = ss.getSheetByName('Feeds');
  var ideas = ss.getSheetByName('Ideas');
  if (!feeds || !ideas) {
    logRow_(ss, 'fetchFeeds', 'FAILED', 'Missing Feeds or Ideas tab');
    SpreadsheetApp.getUi().alert('Missing a "Feeds" or "Ideas" tab. See fix E02.');
    return;
  }
  var cutoff = new Date(Date.now() - WINDOW_DAYS * 24 * 3600 * 1000);
  var existing = {};
  ideas.getDataRange().getValues().forEach(function (row) { existing[String(row[4])] = true; });

  var rows = feeds.getDataRange().getValues();
  var added = 0, failed = 0;
  for (var i = 1; i < rows.length; i++) {
    var name = String(rows[i][0]).trim(), url = String(rows[i][1]).trim();
    if (!url) { continue; }
    if (url.indexOf('https://') !== 0 && url.indexOf('http://') !== 0) {
      logRow_(ss, name, 'FAILED', 'Feed address must start with https://');
      failed++;
      continue;
    }
    try {
      var resp = UrlFetchApp.fetch(url, {muteHttpExceptions: true, followRedirects: true});
      if (resp.getResponseCode() !== 200) {
        throw new Error('HTTP ' + resp.getResponseCode());
      }
      var items = parseFeed_(resp.getContentText());
      var count = 0;
      items.forEach(function (it) {
        if (it.date && it.date < cutoff) { return; }
        if (existing[it.link]) { return; }
        existing[it.link] = true;
        var id = 'F' + Utilities.formatDate(new Date(), 'UTC', 'yyMMddHHmmss') + '-' + (ideas.getLastRow() + 1);
        ideas.appendRow([id, Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'MM/dd/yyyy'),
          it.title, name, it.link, '', '', 'New']);
        count++;
      });
      added += count;
      logRow_(ss, name, count ? 'ok' : 'empty', count + ' new item(s)');
    } catch (e) {
      failed++;
      logRow_(ss, name, 'FAILED', e.message);
    }
  }
  if (failed) {
    SpreadsheetApp.getUi().alert(failed + ' feed(s) failed. See the Log tab and fix E09.');
  }
  return added;
}

function parseFeed_(text) {
  var doc = XmlService.parse(text);
  var root = doc.getRootElement();
  var out = [];
  if (root.getName() === 'rss') {
    var channel = root.getChild('channel');
    channel.getChildren('item').forEach(function (item) {
      var d = item.getChildText('pubDate');
      out.push({
        title: item.getChildText('title') || '',
        link: item.getChildText('link') || '',
        date: d ? new Date(d) : null
      });
    });
  } else {
    var ns = XmlService.getNamespace('http://www.w3.org/2005/Atom');
    root.getChildren('entry', ns).forEach(function (entry) {
      var linkEl = entry.getChild('link', ns);
      var d = entry.getChildText('updated', ns) || entry.getChildText('published', ns);
      out.push({
        title: entry.getChildText('title', ns) || '',
        link: linkEl ? linkEl.getAttribute('href').getValue() : '',
        date: d ? new Date(d) : null
      });
    });
  }
  return out;
}

function installWeeklyTrigger() {
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'fetchFeeds') { ScriptApp.deleteTrigger(t); }
  });
  ScriptApp.newTrigger('fetchFeeds').timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(7).create();
  SpreadsheetApp.getUi().alert('Done. The feeds will be fetched every Monday morning. Check the Log tab each week; a quiet Log means the schedule may have stopped.');
}
