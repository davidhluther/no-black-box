#!/usr/bin/env python3
"""Read-only GSC capture; one site, one key, no writes.

API contract inspected locally: googleapiclient's searchconsole.v1 discovery,
revision 20250714. It supports QUERY, FINAL, 25000/startRow, index inspection,
and sitemap listing with webmasters.readonly. No webmasters v3 fallback.

Only GSC_SA_KEY supplies the service-account key path. No default key,
credential discovery, write scope, sitemap mutation, or model invocation.
Tests inject clients/factories; they never load a key or contact a provider.

Dates are inclusive Pacific provider calendar buckets, NOT UTC/Eastern days.
The three-day lag is readiness guidance, not evidence all days/data are final.
QUERY-only responses cannot independently establish daily availability. All
comparisons describe returned rows, which can be capped or privacy limited.
Missing rows do not prove a query is actually new/gone. Inspections/sitemaps
are current snapshots, not measurements from either historical metric window.
"""
import argparse
import copy
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import sys
import stat
import tempfile
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

# Sites this script may read. Set GSC_SITES to a comma-separated list, for example
# GSC_SITES=sc-domain:example.org,https://www.example.org/
SITES = frozenset(s.strip() for s in os.environ.get('GSC_SITES', '').split(',') if s.strip())
SCOPES = ('https://www.googleapis.com/auth/webmasters.readonly',)
PROVIDER_ZONE = 'America/Los_Angeles'
LAG_DAYS = 3
ROW_LIMIT = 25_000
MAX_QUERY_PAGES = 4
MAX_INSPECTIONS = 20
MAX_OUTPUT_BYTES = 64 * 1024 * 1024
MAX_RESPONSE_BYTES = 32 * 1024 * 1024


class InputError(ValueError):
    pass


class ApiError(RuntimeError):
    def __init__(self, stage):
        self.stage = stage
        super().__init__(stage)


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _clock(now):
    value = now if now is not None else dt.datetime.now(dt.timezone.utc)
    if not isinstance(value, dt.datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise InputError('aware_clock_required')
    return value


def _date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise InputError('invalid_end_date')
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise InputError('invalid_end_date') from None


def windows(*, end=None, now=None):
    today = _clock(now).astimezone(ZoneInfo(PROVIDER_ZONE)).date()
    latest = today - dt.timedelta(days=LAG_DAYS)
    finish = _date(end) if end is not None else latest
    if finish > latest:
        raise InputError('end_after_readiness_bound')
    return dict(provider_today=today.isoformat(), latest_heuristic_end=latest.isoformat(),
                current=dict(start=(finish-dt.timedelta(days=6)).isoformat(), end=finish.isoformat()),
                prior=dict(start=(finish-dt.timedelta(days=13)).isoformat(), end=(finish-dt.timedelta(days=7)).isoformat()))


def _inputs(site, inspect_urls):
    if not isinstance(site, str) or site not in SITES:
        raise InputError('site_not_listed_in_GSC_SITES')
    if not isinstance(inspect_urls, (list, tuple)) or len(inspect_urls) > MAX_INSPECTIONS:
        raise InputError('inspection_limit')
    if any(not isinstance(v, str) for v in inspect_urls) or len(set(inspect_urls)) != len(inspect_urls):
        raise InputError('duplicate_or_invalid_inspection')
    domain = site[len('sc-domain:'):] if site.startswith('sc-domain:') else (urlsplit(site).hostname or '')
    domain = domain[4:] if domain.startswith('www.') else domain
    for value in inspect_urls:
        try:
            parsed = urlsplit(value)
            host = parsed.hostname
            valid = (len(value) <= 4096 and not any(ord(c) <= 32 or ord(c) == 127 for c in value)
                     and '\\' not in value and parsed.scheme in ('http', 'https')
                     and parsed.username is None and parsed.password is None and parsed.port is None
                     and not parsed.fragment and host is not None
                     and (host == domain or host.endswith('.' + domain)))
        except ValueError:
            valid = False
        if not valid:
            raise InputError('inspection_outside_approved_site')


def _execute(request, stage):
    try:
        value = request.execute(num_retries=0)
        if not isinstance(value, dict) or 'error' in value or len(_json(value)) > MAX_RESPONSE_BYTES:
            raise ValueError()
        return value
    except Exception:
        # Never serialize an exception, request URL, key path, token or response body.
        raise ApiError(stage) from None


def _number(value, stage):
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise ApiError(stage)
    return float(value) if value else 0.0


def _row(value, stage):
    if (not isinstance(value, dict) or not isinstance(value.get('keys'), list) or len(value['keys']) != 1
            or not isinstance(value['keys'][0], str) or len(value['keys'][0]) > 4096):
        raise ApiError(stage)
    metrics = {key: _number(value.get(key), stage) for key in ('clicks', 'impressions', 'ctr', 'position')}
    if metrics['ctr'] > 1 or metrics['clicks'] > metrics['impressions']:
        raise ApiError(stage)
    return dict(query=value['keys'][0], **metrics)


def _query(client, site, window, name):
    stage = 'query_' + name
    rows, seen, pages, metadata = [], set(), [], []
    exhausted = False
    for index in range(MAX_QUERY_PAGES):
        body = dict(startDate=window['start'], endDate=window['end'], dimensions=['QUERY'],
                    type='WEB', aggregationType='BY_PROPERTY', dataState='FINAL',
                    rowLimit=ROW_LIMIT, startRow=index*ROW_LIMIT)
        try:
            request = client.searchanalytics().query(siteUrl=site, body=body)
        except Exception:
            raise ApiError(stage) from None
        response = _execute(request, stage)
        raw_rows = response.get('rows', [])
        if not isinstance(raw_rows, list) or len(raw_rows) > ROW_LIMIT:
            raise ApiError(stage)
        for raw in raw_rows:
            row = _row(raw, stage)
            if row['query'] in seen:
                raise ApiError(stage + '_duplicate_rows')
            seen.add(row['query'])
            rows.append(row)
        pages.append(dict(request=body, rows_returned=len(raw_rows),
                          response_aggregation_type=response.get('responseAggregationType')))
        if 'metadata' in response:
            if not isinstance(response['metadata'], dict):
                raise ApiError(stage)
            metadata.append(copy.deepcopy(response['metadata']))
        if len(raw_rows) < ROW_LIMIT:
            exhausted = True
            break
    return dict(**window, inclusive_calendar_days=7, rows=sorted(rows, key=lambda r:r['query']),
                row_count=len(rows), provider_metadata=metadata,
                pagination=dict(row_limit=ROW_LIMIT, max_pages=MAX_QUERY_PAGES, pages=pages,
                                short_page_observed=exhausted, local_limit_reached=not exhausted),
                coverage=dict(query_universe_complete=False, api_returned_rows_only=True,
                              omitted_queries_possible=True, per_day_availability_verified=False),
                requested_data_state='FINAL', provisional=None, finality_verified=False)


def deltas(current_rows, prior_rows):
    """Signed, descriptive comparison; never a recommendation or experiment rule.

    Missing returned row -> new/gone (presence only, even if an existing row's
    impressions are zero). Otherwise spike/drop when signed clicks >=5/<=-5,
    OR impressions change >=50 AND >=50% of positive prior impressions.
    A zero impression baseline skips the percentage test and uses >=50 alone.
    Both directional signals -> neutral/conflicting_metric_signals. Otherwise
    neutral. Only count deltas zero-fill missing rows; rates/positions remain
    unknown when a row is absent. Relative change is None at a zero baseline.
    """
    current = {r['query']:r for r in current_rows}
    prior = {r['query']:r for r in prior_rows}
    out = []
    for query in sorted(set(current) | set(prior)):
        c, p = current.get(query), prior.get(query)
        ci, pi = (c or {}).get('impressions', 0), (p or {}).get('impressions', 0)
        cc, pc = (c or {}).get('clicks', 0), (p or {}).get('clicks', 0)
        impression_delta, click_delta = ci-pi, cc-pc
        relative = impression_delta/pi if pi > 0 else None
        impression_threshold = abs(impression_delta) >= 50 and (pi == 0 or abs(relative) >= .5)
        up = click_delta >= 5 or impression_delta > 0 and impression_threshold
        down = click_delta <= -5 or impression_delta < 0 and impression_threshold
        if p is None:
            classification, reason = 'new', 'absent_from_prior_returned_rows'
        elif c is None:
            classification, reason = 'gone', 'absent_from_current_returned_rows'
        elif up and down:
            classification, reason = 'neutral', 'conflicting_metric_signals'
        elif up:
            classification, reason = 'spike', 'positive_threshold_signal'
        elif down:
            classification, reason = 'drop', 'negative_threshold_signal'
        else:
            classification, reason = 'neutral', 'below_thresholds'
        out.append(dict(query=query, current_row_present=c is not None, prior_row_present=p is not None,
                        clicks=click_delta, impressions=impression_delta,
                        impressions_relative=relative, clicks_relative=click_delta/pc if pc > 0 else None,
                        ctr=c['ctr']-p['ctr'] if c is not None and p is not None else None,
                        position=c['position']-p['position'] if c is not None and p is not None else None,
                        classification=classification, reason=reason,
                        signals=dict(up=bool(up), down=bool(down),
                                     impression_threshold=impression_threshold)))
    return out


def capture(client, *, site, inspect_urls=(), end=None, now=None):
    """Injected read-only client, no filesystem, credentials or provider creation."""
    _inputs(site, inspect_urls)
    clock = _clock(now)
    ranges = windows(end=end, now=clock)
    current = _query(client, site, ranges['current'], 'current')
    prior = _query(client, site, ranges['prior'], 'prior')
    inspections = []
    for index, url in enumerate(inspect_urls):
        stage = 'inspection_' + str(index+1)
        try:
            request = client.urlInspection().index().inspect(body=dict(siteUrl=site, inspectionUrl=url))
        except Exception:
            raise ApiError(stage) from None
        response = _execute(request, stage)
        if not isinstance(response.get('inspectionResult'), dict):
            raise ApiError(stage)
        inspections.append(dict(url=url, result=copy.deepcopy(response['inspectionResult'])))
    try:
        request = client.sitemaps().list(siteUrl=site)
    except Exception:
        raise ApiError('sitemaps') from None
    response = _execute(request, 'sitemaps')
    sitemaps = response.get('sitemap', [])
    if not isinstance(sitemaps, list) or len(sitemaps) > 10_000 or any(not isinstance(v, dict) for v in sitemaps):
        raise ApiError('sitemaps')
    record = dict(version=1, site=site, captured_at_utc=clock.astimezone(dt.timezone.utc).isoformat(),
                  provider_bucket_timezone=PROVIDER_ZONE, api_service='searchconsole', api_version='v1',
                  readiness=dict(lag_days=LAG_DAYS, heuristic_only=True, provider_today=ranges['provider_today'],
                                 latest_heuristic_end=ranges['latest_heuristic_end'], finality_proven=False),
                  windows=dict(current=current, prior=prior),
                  deltas=deltas(current['rows'], prior['rows']),
                  comparison=dict(basis='returned query rows only; absence is not proof of actual query disappearance',
                                  missing_count_fill=0, missing_rate_or_position=None,
                                  click_threshold=5, impression_threshold=50, impression_relative_threshold=.5,
                                  zero_impression_baseline='absolute threshold only',
                                  contradictory_signals='neutral', actions_recommended=False),
                  inspections=inspections, sitemaps=copy.deepcopy(sitemaps),
                  status_temporal_scope='inspections and sitemaps are current snapshots, not either metric window',
                  authorization_scope=SCOPES[0])
    record['capture_sha256'] = _sha(_json(record))
    return record


def _client(key_path, scopes):
    # Executed only by an explicit eventual CLI invocation with GSC_SA_KEY.
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    credentials = service_account.Credentials.from_service_account_file(key_path, scopes=list(scopes))
    return build('searchconsole', 'v1', credentials=credentials, cache_discovery=False, static_discovery=True)


class MovedError(ApiError):
    """The write landed in the pinned folder, but --out no longer names it."""


def _before_replace():
    """Test seam: runs just before the rename ."""


def _before_write():
    """Test seam: runs between validation and the write (TOCTOU tests swap paths here)."""


def _write_pinned(path, raw, root_id):
    """Write inside a parent whose identity was fixed at validation.

    The parent is reopened without following a final symlink and must match (st_dev, st_ino); the temp
    file is created O_EXCL|O_NOFOLLOW relative to that directory fd and renamed within it, and a symlink
    at the final name is refused."""
    dfd = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    temporary = None
    try:
        st = os.fstat(dfd)
        if (st.st_dev, st.st_ino) != root_id:
            raise ApiError('write')
        temporary = '.gsc-capture-' + os.urandom(8).hex()
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=dfd)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
            written = os.fstat(stream.fileno())
        try:
            if stat.S_ISLNK(os.lstat(path.name, dir_fd=dfd).st_mode):
                raise ApiError('write')
        except FileNotFoundError:
            pass
        _before_replace()
        os.replace(temporary, path.name, src_dir_fd=dfd, dst_dir_fd=dfd)
        temporary = None
        try:
            got, parent = os.lstat(path), os.stat(path.parent)
        except OSError:
            raise MovedError('write')
        if (not stat.S_ISREG(got.st_mode) or (got.st_dev, got.st_ino) != (written.st_dev, written.st_ino)
                or (parent.st_dev, parent.st_ino) != root_id):
            raise MovedError('write')
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary, dir_fd=dfd)
            except FileNotFoundError:
                pass
        os.close(dfd)


def _write(path, record, root_id=None):
    raw = _json(record) + b'\n'
    if len(raw) > MAX_OUTPUT_BYTES:
        raise ApiError('output_budget')
    _before_write()
    if root_id is not None:
        return _write_pinned(path, raw, root_id)
    fd, temporary = tempfile.mkstemp(prefix='.gsc-capture-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        # Publication is the commit point. No fallible operation follows it:
        # an API/input/write failure must never publish a new "fresh" output.
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            os.unlink(temporary)


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise InputError('invalid_arguments')


def main(argv=None, *, client_factory=None, environ=None, now=None, stderr=None):
    """0 atomic publication; 2 input/key-env; 1 auth/API/write stage, no new output."""
    stderr = stderr if stderr is not None else sys.stderr
    env = os.environ if environ is None else environ
    parser = _Parser(description=__doc__, allow_abbrev=False)
    parser.add_argument('--site', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--inspect', nargs='+', action='append', default=[])
    parser.add_argument('--end')
    parser.add_argument('--out-root', help='if set, --out must sit directly in this directory, checked again at write time')
    stage = 'input'
    try:
        args = parser.parse_args(argv)
        urls = [url for group in args.inspect for url in group]
        _inputs(args.site, urls)
        clock = _clock(now)
        windows(end=args.end, now=clock)
        key_path = env.get('GSC_SA_KEY')
        if not isinstance(key_path, str) or not key_path.strip():
            raise InputError('missing_GSC_SA_KEY')
        output = Path(args.out)
        if (not output.name or not output.parent.is_dir() or output.is_symlink() or output.is_dir()
                or os.path.abspath(output) == os.path.abspath(key_path)):
            raise InputError('invalid_output_path')
        root_id = None
        if args.out_root is not None:
            try:
                rfd = os.open(args.out_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
            except OSError:
                raise InputError('invalid_output_path')
            try:
                rst, pst = os.fstat(rfd), os.stat(output.parent)
            finally:
                os.close(rfd)
            if (rst.st_dev, rst.st_ino) != (pst.st_dev, pst.st_ino):
                raise InputError('invalid_output_path')
            root_id = (rst.st_dev, rst.st_ino)
        stage = 'auth'
        client = (client_factory or _client)(key_path, SCOPES)
        stage = 'capture'
        record = capture(client, site=args.site, inspect_urls=urls, end=args.end, now=clock)
        stage = 'write'
        _write(output, record, root_id)
        return 0
    except InputError as exc:
        print('gsc_read: input: ' + str(exc), file=stderr)
        return 2
    except MovedError:
        print('gsc_read: write: output path moved during write', file=stderr)
        return 1
    except ApiError as exc:
        print('gsc_read: ' + exc.stage + ': failed; no output published', file=stderr)
        return 1
    except Exception:
        print('gsc_read: ' + stage + ': failed; no output published', file=stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
