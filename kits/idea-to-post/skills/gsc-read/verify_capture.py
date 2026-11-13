#!/usr/bin/env python3
"""verify_capture.py — decide whether a gsc_read.py capture may be adopted this run. No network, no model.

A person or an AI model cannot recompute a hash by eye, so run this instead of trusting the file:
exit 0 only when the file is this run's capture for the expected site, its capture_sha256 matches the canonical
JSON of everything else (gsc_read's own serialization), and neither window hit the local row cap. Anything else
exits 1 with one reason line, and you fall back to reading Search Console directly. An older file is never adopted.

CLI:  verify_capture.py --site sc-domain:example.org --file F [--today YYYY-MM-DD]   (today: UTC date)
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def problems(record, site, today):
    if not isinstance(record, dict):
        return ['not_a_capture']
    out = []
    if record.get('site') != site:
        out.append('site_mismatch')
    stamp = record.get('captured_at_utc')
    try:
        when = dt.datetime.fromisoformat(stamp)
        if when.tzinfo is None or when.astimezone(dt.timezone.utc).date() != today:
            out.append('not_captured_this_run')
    except (TypeError, ValueError):
        out.append('captured_at_unreadable')
    body = {k: v for k, v in record.items() if k != 'capture_sha256'}
    try:
        if hashlib.sha256(canonical(body)).hexdigest() != record.get('capture_sha256'):
            out.append('hash_mismatch')
    except (TypeError, ValueError):
        out.append('hash_unverifiable')
    windows = record.get('windows') if isinstance(record.get('windows'), dict) else {}
    for name in ('current', 'prior'):
        w = windows.get(name)
        pag = w.get('pagination') if isinstance(w, dict) else None
        if not isinstance(pag, dict) or pag.get('local_limit_reached') is not False:
            out.append(f'{name}_rows_capped_or_unknown')
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--site', required=True)
    ap.add_argument('--file', required=True)
    ap.add_argument('--today')
    a = ap.parse_args(argv)
    try:
        today = dt.date.fromisoformat(a.today) if a.today else dt.datetime.now(dt.timezone.utc).date()
        record = json.loads(Path(a.file).read_text(encoding='utf-8'))
    except (OSError, ValueError):
        print('gsc capture: not adoptable: unreadable')
        return 1
    bad = problems(record, a.site, today)
    if bad:
        print('gsc capture: not adoptable: ' + ', '.join(bad))
        return 1
    print('gsc capture: adoptable')
    return 0


if __name__ == '__main__':
    sys.exit(main())
