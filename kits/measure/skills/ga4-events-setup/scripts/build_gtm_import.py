#!/usr/bin/env python3
"""Build an additive Google Tag Manager import file. Stdlib only. Never contacts Google.

Usage:
  python3 build_gtm_import.py --config config.json --out gtm-import.json
  python3 build_gtm_import.py --config config.json --out gtm-import.json --existing container-export.json

Reads config.json keys: ga4_measurement_id, gtm_container_id, tag_prefix (default "Add |"),
sister_site_domains (list), form_success_event_regex (default ".*form\\.success$").
Every new item carries the prefix. With --existing, exits 1 if any new name already exists.
Import it in a NEW workspace with Merge + "Rename conflicting tags, triggers, and variables".
"""
import argparse
import json
import re
import sys


def t(key, value):
    return {"type": "TEMPLATE", "key": key, "value": value}


def cond(kind, arg0, arg1, negate=False, ignore_case=False):
    c = {"type": kind, "parameter": [t("arg0", arg0), t("arg1", arg1)]}
    if ignore_case:
        c["parameter"].append({"type": "BOOLEAN", "key": "ignore_case", "value": "true"})
    if negate:
        c["parameter"].append({"type": "BOOLEAN", "key": "negate", "value": "true"})
    return c


def build(cfg):
    p = cfg.get("tag_prefix", "Add |")
    mid = cfg["ga4_measurement_id"]
    acct, cont = "0", "0"  # GTM assigns real IDs on import
    form_re = cfg.get("form_success_event_regex", r".*form\.success$")
    sisters = [d.replace(".", r"\.") for d in cfg.get("sister_site_domains", [])]

    def var(i, name, code):
        return {"accountId": acct, "containerId": cont, "variableId": str(i), "name": f"{p} JS | {name}",
                "type": "jsm", "parameter": [t("javascript", code)], "formatValue": {}}

    def link(i, name, filters):
        return {"accountId": acct, "containerId": cont, "triggerId": str(i), "name": f"{p} Link | {name}",
                "type": "LINK_CLICK", "filter": filters,
                "waitForTags": {"type": "BOOLEAN", "value": "false"},
                "checkValidation": {"type": "BOOLEAN", "value": "false"},
                "waitForTagsTimeout": {"type": "TEMPLATE", "value": "2000"},
                "uniqueTriggerId": {"type": "TEMPLATE"}}

    def ga4(i, name, event, params, trig):
        rows = [{"type": "MAP", "map": [t("parameter", k), t("parameterValue", v)]} for k, v in params]
        return {"accountId": acct, "containerId": cont, "tagId": str(i), "name": f"{p} GA4 | {name}",
                "type": "gaawe",
                "parameter": [{"type": "BOOLEAN", "key": "sendEcommerceData", "value": "false"},
                              t("eventName", event), t("measurementIdOverride", mid),
                              {"type": "LIST", "key": "eventSettingsTable", "list": rows}],
                "firingTriggerId": [str(trig)], "tagFiringOption": "ONCE_PER_EVENT",
                "monitoringMetadata": {"type": "MAP"}, "consentSettings": {"consentStatus": "NOT_SET"}}

    v_loc = var(9001, "click_location", """function () {
  var el = {{Click Element}};
  if (!el || !el.closest) return 'unknown';
  if (el.closest('footer')) return 'footer';
  if (el.closest('header, nav')) return 'nav';
  return 'body';
}""")
    v_text = var(9002, "link_text", """function () {
  var el = {{Click Element}};
  var a = el && el.closest ? (el.closest('a') || el) : null;
  var s = a ? (a.innerText || a.getAttribute('aria-label') || a.getAttribute('title') || '') : ({{Click Text}} || '');
  return s.replace(/<[^>]*>/g, ' ').replace(/\\s+/g, ' ').trim().slice(0, 100);
}""")
    v_title = var(9003, "asset_title", """function () {
  var u = {{Click URL}} || '';
  var seg = u.split('?')[0].split('#')[0].split('/').pop() || '';
  try { seg = decodeURIComponent(seg); } catch (e) {}
  return seg.replace(/\\.[a-z0-9]{2,5}$/i, '').replace(/[_+-]+/g, ' ').trim().slice(0, 100);
}""")
    v_sister = var(9004, "sister_site_host", """function () {
  var m = ({{Click URL}} || '').toLowerCase().match(/^https?:\\/\\/([^\\/?#]+)/);
  if (!m) return '';
  var h = m[1].replace(/^www\\./, '');
  var re = /(^|\\.)(%s)$/;
  return re.test(h) ? h : '';
}""" % ("|".join(sisters) if sisters else "no-sister-sites-configured\\.invalid"))
    v_dl = {"accountId": acct, "containerId": cont, "variableId": "9005", "name": f"{p} DL | form_id",
            "type": "v", "parameter": [t("dataLayerVersion", "2"), t("name", "form_id")]}

    trig_form = {"accountId": acct, "containerId": cont, "triggerId": "9101", "name": f"{p} CE | Form success",
                 "type": "CUSTOM_EVENT",
                 "customEventFilter": [cond("MATCH_REGEX", "{{_event}}", form_re)]}
    trigs = [
        trig_form,
        link(9102, "File download", [cond("MATCH_REGEX", "{{Click URL}}", r"\.(pdf|docx?|xlsx?|pptx?|zip)([?#]|$)", ignore_case=True)]),
        link(9103, "Phone (tel)", [cond("STARTS_WITH", "{{Click URL}}", "tel:")]),
        link(9104, "Email (mailto)", [cond("STARTS_WITH", "{{Click URL}}", "mailto:")]),
        link(9105, "Call to action", [cond("MATCH_REGEX", "{{Click URL}}", r"/(contact|contact-us|demo|get-started|book|quote)(/|\?|#|$)", ignore_case=True)]),
    ]
    tags = [
        ga4(9201, "generate_lead_form", "generate_lead", [("form_id", f"{{{{{p} DL | form_id}}}}")], 9101),
        ga4(9202, "content_download", "content_download",
            [("asset_title", f"{{{{{p} JS | asset_title}}}}"), ("file_url", "{{Click URL}}")], 9102),
        ga4(9203, "phone_click", "phone_click",
            [("link_url", "{{Click URL}}"), ("click_location", f"{{{{{p} JS | click_location}}}}")], 9103),
        ga4(9204, "email_click", "email_click",
            [("link_url", "{{Click URL}}"), ("click_location", f"{{{{{p} JS | click_location}}}}")], 9104),
        ga4(9205, "cta_click", "cta_click",
            [("cta_text", f"{{{{{p} JS | link_text}}}}"), ("cta_destination", "{{Click URL}}")], 9105),
    ]
    varlist = [v_loc, v_text, v_title, v_sister, v_dl]
    if sisters:
        trigs.append(link(9106, "Sister site", [cond("MATCH_REGEX", f"{{{{{p} JS | sister_site_host}}}}", ".+")]))
        tags.append(ga4(9206, "sister_site_click", "sister_site_click",
                        [("sister_site", f"{{{{{p} JS | sister_site_host}}}}"), ("link_url", "{{Click URL}}")], 9106))
    return {"exportFormatVersion": 2, "exportTime": "2000-01-01 00:00:00",
            "containerVersion": {"accountId": acct, "containerId": cont, "containerVersionId": "0",
                                 "container": {"accountId": acct, "containerId": cont, "name": "example",
                                               "publicId": cfg.get("gtm_container_id", "GTM-XXXXXXX"),
                                               "usageContext": ["WEB"]},
                                 "tag": tags, "trigger": trigs, "variable": varlist}}


def names(doc):
    cv = doc.get("containerVersion", {})
    return {i["name"] for k in ("tag", "trigger", "variable") for i in cv.get(k, [])}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--existing", help="a container export from Tag Manager, to check for name collisions")
    a = ap.parse_args()
    cfg = json.load(open(a.config))
    for k in ("ga4_measurement_id",):
        if not re.fullmatch(r"G-[A-Z0-9]{4,}", cfg.get(k, "")):
            sys.exit(f"config.json: {k} should look like G-XXXXXXX")
    doc = build(cfg)
    new = names(doc)
    if a.existing:
        clash = sorted(new & names(json.load(open(a.existing))))
        if clash:
            print("These new names already exist; change tag_prefix:", *clash, sep="\n  ")
            sys.exit(1)
    json.dump(doc, open(a.out, "w"), indent=2)
    cv = doc["containerVersion"]
    print(f"wrote {a.out}: {len(cv['tag'])} tags, {len(cv['trigger'])} triggers, {len(cv['variable'])} variables; all new, all prefixed")


if __name__ == "__main__":
    main()
