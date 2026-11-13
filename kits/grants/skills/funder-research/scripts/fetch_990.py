#!/usr/bin/env python3
"""
fetch_990.py - pull any e-filed Form 990 / 990-EZ / 990-PF as IRS XML, without ProPublica downloads.

Why this exists: ProPublica's PDF and XML download links sit behind a Cloudflare
security check that scripts and the in-app browser can't pass (hit 10/30/2026).
ProPublica's JSON API still works for summaries, but for line-level detail
(contribution types, Schedule M, fundraising, cash) go to the IRS's own data:

  1. Find the filing in the IRS annual index  apps.irs.gov/pub/epostcard/990/xml/<year>/index_<year>.csv
     (cached in ~/.cache/fetch_990/; one ~60 MB CSV per filing year).
  2. Fetch the XML from the GivingTuesday 990 data lake (one small file per filing).
  3. If the lake doesn't have it yet (newest filings), pull just that one member out of
     the IRS batch zip with HTTP range requests - a few MB of traffic, not the 500 MB zip.

Examples:
  python3 fetch_990.py 620670972                      # list every filing found for the EIN
  python3 fetch_990.py 620670972 --summary            # key figures for each 990 / 990-PF
  python3 fetch_990.py 561442966 --period 202506 --out ./990s --summary
"""
import argparse
import csv
import io
import json
import re
import struct
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from datetime import date
from pathlib import Path

IRS = "https://apps.irs.gov/pub/epostcard/990/xml/{y}/"
LAKE = "https://gt990datalake-rawdata.s3.amazonaws.com/EfileData/XmlFiles/{oid}_public.xml"
CACHE = Path.home() / ".cache" / "fetch_990"
UA = {"User-Agent": "fetch_990/1.0 (nonprofit research)"}
FIRST_YEAR = 2019  # IRS publishes indexes from 2019 on

# Tags pulled for --summary. Group tags print their child values; missing tags are skipped.
SUMMARY_TAGS = [
    "TaxPeriodEndDt", "ReturnTypeCd", "CYTotalRevenueAmt", "TotalContributionsAmt",
    "GovernmentGrantsAmt", "NoncashContributionsAmt", "FederatedCampaignsAmt",
    "FundraisingEventsAmt", "RelatedOrganizationsAmt", "AllOtherContributionsAmt",
    "TotalProgramServiceRevenueAmt", "CYTotalExpensesAmt", "CYTotalFundraisingExpenseAmt",
    "CYSalariesCompEmpBnftPaidAmt", "TotalEmployeeCnt", "TotalVolunteersCnt",
    "NetAssetsOrFundBalancesEOYAmt", "NoDonorRestrictionNetAssetsGrp",
    "CashNonInterestBearingGrp", "SavingsAndTempCashInvstGrp",
    # 990-PF
    "TotalRevAndExpnssAmt", "ContriPaidRevAndExpnssAmt", "FMVAssetsEOYAmt",
]


def _get(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def index_rows(ein, years):
    """Yield IRS index rows for an EIN across filing years, caching each index locally."""
    ein = re.sub(r"\D", "", str(ein)).zfill(9)
    CACHE.mkdir(parents=True, exist_ok=True)
    for y in years:
        path = CACHE / f"index_{y}.csv"
        if not path.exists() or (y == date.today().year and path.stat().st_size and
                                 (date.today() - date.fromtimestamp(path.stat().st_mtime)).days > 7):
            try:
                path.write_bytes(_get(IRS.format(y=y) + f"index_{y}.csv"))
            except Exception as e:  # a missing future-year index is normal
                print(f"[skip] index {y}: {e}", file=sys.stderr)
                continue
        with path.open(newline="", encoding="utf-8", errors="replace") as f:
            for row in csv.DictReader(f):
                if row.get("EIN", "").zfill(9) == ein:
                    row["FILING_YEAR"] = str(y)
                    yield row


class HTTPRangeFile(io.RawIOBase):
    """Seekable read-only view of a remote file, fetched in cached blocks via HTTP Range."""
    BLOCK = 1 << 20

    def __init__(self, url):
        self.url, self.pos, self.cache = url, 0, {}
        req = urllib.request.Request(url, method="HEAD", headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            self.size = int(r.headers["Content-Length"])

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.pos

    def seek(self, off, whence=0):
        self.pos = {0: off, 1: self.pos + off, 2: self.size + off}[whence]
        return self.pos

    def _block(self, i):
        if i not in self.cache:
            lo = i * self.BLOCK
            hi = min(lo + self.BLOCK, self.size) - 1
            self.cache[i] = _get(self.url, {"Range": f"bytes={lo}-{hi}"})
        return self.cache[i]

    def read(self, n=-1):
        if n is None or n < 0:
            n = self.size - self.pos
        out = bytearray()
        while n > 0 and self.pos < self.size:
            i, off = divmod(self.pos, self.BLOCK)
            chunk = self._block(i)[off:off + n]
            out += chunk
            self.pos += len(chunk)
            n -= len(chunk)
        return bytes(out)

    def readinto(self, b):
        data = self.read(len(b))
        b[:len(data)] = data
        return len(data)


def _read_member(z, rf, name):
    """Read one zip member. Recent IRS batches use Deflate64 (method 9), which Python's
    zipfile can't decode, so for those copy the raw member into a one-entry zip and let
    the system `unzip` (Info-ZIP built with USE_DEFLATE64, as on macOS) decompress it."""
    zi = z.getinfo(name)
    if zi.compress_type != 9:
        return z.read(name)
    rf.seek(zi.header_offset)
    hdr = rf.read(30)
    nlen, xlen = struct.unpack("<HH", hdr[26:30])
    local = hdr + rf.read(nlen + xlen)
    data = rf.read(zi.compress_size)
    fname = zi.filename.encode()
    cd = struct.pack("<IHHHHHHIIIHHHHHII", 0x02014B50, 20, 21, zi.flag_bits, 9,
                     *_dostime(zi.date_time), zi.CRC, zi.compress_size, zi.file_size,
                     len(fname), 0, 0, 0, 0, 0, 0) + fname
    # Local header may carry ZIP64 placeholder sizes; the central record has the real ones.
    eocd = struct.pack("<IHHHHIIH", 0x06054B50, 0, 0, 1, 1, len(cd), len(local) + len(data), 0)
    with tempfile.TemporaryDirectory() as td:
        mini = Path(td) / "one.zip"
        mini.write_bytes(local + data + cd + eocd)
        r = subprocess.run(["unzip", "-p", str(mini)], capture_output=True)
        if r.returncode != 0 or not r.stdout:
            raise RuntimeError(f"unzip failed on Deflate64 member {name}: {r.stderr.decode()[:200]}")
        return r.stdout


def _dostime(dt):
    y, mo, d, h, mi, s = dt
    return (h << 11) | (mi << 5) | (s // 2), ((y - 1980) << 9) | (mo << 5) | d


def fetch_xml(row):
    """Return (xml_text, source) for an index row: data lake first, IRS batch zip second."""
    oid = row["OBJECT_ID"]
    try:
        data = _get(LAKE.format(oid=oid))
        if data.lstrip().startswith(b"<?xml") or b"<Return" in data[:2000]:
            return data.decode("utf-8", "replace"), "givingtuesday-datalake"
    except Exception:
        pass
    batch = row.get("XML_BATCH_ID")
    if not batch:
        raise RuntimeError(f"{oid}: not in the data lake and the index row has no XML_BATCH_ID")
    # The index names one batch ("..._05A") even when the IRS split it into 05A, 05B, ...
    # zips, so try the named batch, then its lettered siblings.
    stem = batch[:-1] if batch[-1].isalpha() else batch
    tried = []
    for b in dict.fromkeys([batch] + [stem + c for c in "ABCDEFGH"]):
        url = IRS.format(y=row["FILING_YEAR"]) + f"{b}.zip"
        try:
            rf = HTTPRangeFile(url)
        except Exception:
            continue  # sibling doesn't exist
        tried.append(b)
        with zipfile.ZipFile(rf) as z:
            name = next((n for n in z.namelist() if n.endswith(f"{oid}_public.xml")), None)
            if name:
                return _read_member(z, rf, name).decode("utf-8", "replace"), f"irs-zip:{b}"
    raise RuntimeError(f"{oid}: not found in {', '.join(tried) or batch}")


def summarize(xml):
    out = {}
    for tag in SUMMARY_TAGS:
        m = re.search(rf"<{tag}>([\s\S]*?)</{tag}>", xml)
        if not m:
            continue
        inner = m.group(1)
        kids = re.findall(r"<(\w+)>([^<]*)</\1>", inner)
        out[tag] = {k: v for k, v in kids} if kids else inner.strip()
    sm = re.search(r"<IRS990ScheduleM[\s\S]*?</IRS990ScheduleM>", xml)
    if sm:  # noncash gift types, e.g. SecuritiesPubliclyTradedGrp for stock gifts
        out["ScheduleM"] = {
            g: re.findall(r"<(?:ContributionCnt|NoncashContributionsRptF990Amt)>([^<]+)<", body)
            for g, body in re.findall(r"<(\w+Grp)>([\s\S]*?)</\1>", sm.group(0))
        }
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ein")
    ap.add_argument("--years", default=f"{FIRST_YEAR}-{date.today().year}",
                    help="filing (submission) years to search, e.g. 2023-2026")
    ap.add_argument("--period", help="only this tax period, YYYYMM (e.g. 202506)")
    ap.add_argument("--out", help="directory to save each XML as <ein>_<period>_<type>.xml")
    ap.add_argument("--summary", action="store_true", help="print key figures as JSON")
    a = ap.parse_args(argv)

    lo, _, hi = a.years.partition("-")
    rows = list(index_rows(a.ein, range(int(lo), int(hi or lo) + 1)))
    if a.period:
        rows = [r for r in rows if r["TAX_PERIOD"] == a.period]
    rows.sort(key=lambda r: r["TAX_PERIOD"], reverse=True)
    if not rows:
        print(f"No e-filed returns found for EIN {a.ein} in filing years {a.years} "
              f"(searched the IRS indexes only; paper filers and pre-{FIRST_YEAR} returns aren't covered).")
        return 1
    for r in rows:
        line = f"{r['TAX_PERIOD']}  {r['RETURN_TYPE']:7} {r['TAXPAYER_NAME']}  object_id={r['OBJECT_ID']}"
        if not (a.out or a.summary) or r["RETURN_TYPE"] not in ("990", "990EZ", "990PF"):
            print(line)
            continue
        xml, src = fetch_xml(r)
        print(f"{line}  [{src}]")
        if a.out:
            p = Path(a.out)
            p.mkdir(parents=True, exist_ok=True)
            (p / f"{r['EIN']}_{r['TAX_PERIOD']}_{r['RETURN_TYPE']}.xml").write_text(xml)
        if a.summary:
            print(json.dumps(summarize(xml), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
