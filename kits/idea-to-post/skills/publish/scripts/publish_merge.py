#!/usr/bin/env python3
"""Publish one reviewed blog post through GitHub: the owner's exact "merge N" becomes one pinned, verified merge.

What it does, in plain words. Each post travels as its own pull request (a proposed change that waits
for review) on a branch whose name starts with a prefix you chose, such as blog-. When you type the exact
words "merge 12", this script checks pull request 12 is ready, merges exactly the version you reviewed,
waits for the live deployment, and then fetches each post's address to prove it shows the right title.
A merge alone is not publishing, and neither is a page that answers "200 OK" (the web's "found it").

Which sites it serves, and their repository, branch prefix, post path, live address and title shape, come
from the site configs in ../sites (see site_registry.py). A site opts in with publish.authority "merge_n".
Every other site is refused before any GitHub call.

Safety rules built in:
  - Only the exact words "merge N" count, bound to that pull request and its full head SHA (the
    fingerprint of the last saved change). If the pull request changes after you approved it, nothing merges.
  - Every check on the pull request must have finished and passed.
  - One action record per site and pull request, created exclusively, stops a repeated message or a retry
    from merging twice. An uncertain merge is re-read from GitHub, never retried blindly.
  - Nothing is merged unless you pass --yes. Without it, `run` only reports whether the merge would go ahead.

Needs the GitHub command-line tool (gh) signed in to an account that can merge on the repository.
Records are kept in ./.publish-store (or the folder named in PUBLISH_STORE_DIR).

Commands:
    publish_merge.py bind   --site example.org --authority "merge 12" --approval-id 2026-11-13-a --head 3f9c2a1e5b7d4c6a8f0e2b4d6c8a0f1e3b5d7c9a
    publish_merge.py run    --site example.org --approval-id 2026-11-13-a [--yes]
    publish_merge.py status --site example.org 12
"""
from __future__ import annotations

import argparse
import contextlib
import fcntl
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_registry  # noqa: E402

# Case-insensitive, because a phone keyboard capitalizes the first letter ("Merge 12").
AUTHORITY = re.compile(r"merge\s+([1-9][0-9]{0,5})", re.I)
SHA = re.compile(r"^[0-9a-f]{40}$")
GOOD_CHECKS = {"SUCCESS", "NEUTRAL", "SKIPPED"}
STORE_ROOT = Path(os.environ.get("PUBLISH_STORE_DIR") or Path.cwd() / ".publish-store")


class Refused(Exception):
    """Nothing was merged; the reason is safe to show the owner."""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_authority(text) -> int | None:
    """The pull request number from the exact words "merge N" (surrounding whitespace only), else None."""
    if not isinstance(text, str):
        return None
    match = AUTHORITY.fullmatch(text.strip())
    return int(match.group(1)) if match else None


def gh(args, runner=subprocess.run):
    proc = runner(["gh", *args], capture_output=True, text=True, timeout=120)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "gh failed").strip()[-400:])
    out = proc.stdout.strip()
    try:
        return json.loads(out) if out else ""
    except json.JSONDecodeError:
        return out


def merge_site(site_id) -> site_registry.Site:
    """The registered site, only if it publishes through "merge N"."""
    try:
        site = site_registry.load(site_id)
    except ValueError as exc:
        raise Refused(f"{site_id!r} is not a registered site: {exc}.") from None
    if not site.merge_n:
        raise Refused(f"{site.entity} does not publish through \"merge N\" ({site.publish['contract']}).")
    return site


def view(site, number, runner=subprocess.run) -> dict:
    return gh(["pr", "view", str(number), "--repo", site.repo, "--json",
               "number,state,isDraft,baseRefName,headRefName,headRefOid,mergeCommit,statusCheckRollup,files,"
               "isCrossRepository,headRepositoryOwner,title"],
              runner)


def check_ready(site, pr: dict) -> None:
    """Refuse unless the pull request is open, on the site's branch prefix, into the site's base, with every check passing."""
    if pr.get("state") != "OPEN":
        raise Refused(f"PR {pr.get('number')} is {str(pr.get('state', 'unknown')).lower()}, not open.")
    if pr.get("isDraft"):
        raise Refused(f"PR {pr['number']} is a draft.")
    base, prefix = site.publish["base"], site.publish["lane_prefix"]
    if pr.get("baseRefName") != base or not str(pr.get("headRefName", "")).startswith(prefix):
        raise Refused(f"PR {pr['number']} is not a {prefix}* branch into {base}.")
    if pr.get("isCrossRepository") or (pr.get("headRepositoryOwner") or {}).get("login") != site.repo.split("/")[0]:
        raise Refused(f"PR {pr['number']} does not come from {site.repo}.")
    if not SHA.match(str(pr.get("headRefOid", ""))):
        raise Refused(f"PR {pr['number']} has no readable head commit.")
    checks = pr.get("statusCheckRollup") or []
    if not checks:
        raise Refused(f"PR {pr['number']} has no checks yet.")
    for check in checks:
        name = check.get("name") or check.get("context") or "check"
        result = (check.get("conclusion") or check.get("state") or "").upper()
        status = (check.get("status") or "COMPLETED").upper()
        if status != "COMPLETED" or result not in GOOD_CHECKS:
            raise Refused(f"PR {pr['number']} check {name} is {result.lower() or status.lower()}.")


def posts(site, pr: dict) -> list[str]:
    pattern = site.post_pattern()
    return sorted({m.group(1) for f in pr.get("files") or []
                   if (m := pattern.match(f.get("path", ""))) and f.get("changeType", "MODIFIED") != "DELETED"})


class Record:
    """The one durable action record for a pull request. Callers hold lock() for the whole read-act-write."""

    def __init__(self, site, number, store=None):
        self.site = site
        self.store = Path(store) if store is not None else STORE_ROOT / site.publish["store"]
        self.path = self.store / f"{int(number)}.json"

    @contextlib.contextmanager
    def lock(self):
        self.store.mkdir(parents=True, exist_ok=True)
        fd = os.open(self.path.with_suffix(".lock"), os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            os.close(fd)

    def read(self) -> dict | None:
        try:
            return json.loads(self.path.read_text())
        except FileNotFoundError:
            return None

    def _write(self, target: Path, data, exclusive=False) -> bool:
        fd, tmp = tempfile.mkstemp(dir=self.store, prefix=target.name, suffix=".tmp")
        with os.fdopen(fd, "w") as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
        try:
            if exclusive:
                try:
                    os.link(tmp, target)  # atomic and exclusive: a reader never sees a partial record
                except FileExistsError:
                    return False
            else:
                os.replace(tmp, target)
                tmp = None
            return True
        finally:
            if tmp:
                os.unlink(tmp)

    def create(self, data) -> bool:
        self.store.mkdir(parents=True, exist_ok=True)
        return self._write(self.path, data, exclusive=True)

    def update(self, **changes) -> dict:
        data = {**(self.read() or {}), **changes, "updated_at": now()}
        self._write(self.path, data)
        return data

    def bind_message(self, message_id, binding: dict) -> dict:
        """First sight of an approval id fixes its binding (PR, time, head SHA) for good.
        Returns the stored binding; a retry must present exactly the same one."""
        marker = self.store / "messages" / (hashlib.sha256(message_id.encode()).hexdigest() + ".json")
        marker.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=marker.parent, suffix=".tmp")
        with os.fdopen(fd, "w") as fh:
            json.dump(binding, fh, sort_keys=True)
        try:
            os.link(tmp, marker)
        except FileExistsError:
            pass
        finally:
            os.unlink(tmp)
        fd = os.open(marker, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd) as fh:
            return json.load(fh)

    def consume_message(self, message_id) -> bool:
        """An approval id drives at most one merge attempt, ever. False if it already did."""
        marker = self.store / "messages" / (hashlib.sha256(message_id.encode()).hexdigest() + ".consumed")
        try:
            os.close(os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600))
        except FileExistsError:
            return False
        return True


def fetch(url, opener=urllib.request.urlopen) -> tuple[int, str]:
    try:
        with opener(urllib.request.Request(url, headers={"User-Agent": "publish-merge-check"}), timeout=30) as resp:
            return resp.status, resp.read(400_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, ""
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, ""


def frontmatter(site, slug, sha, runner=subprocess.run) -> dict:
    """The post's top-level frontmatter (the settings block at the top of the file) at the merge commit."""
    text = gh(["api", "-H", "Accept: application/vnd.github.raw",
               f"repos/{site.repo}/contents/{site.post_file(slug)}?ref={sha}"], runner)
    text = text if isinstance(text, str) else ""
    return site_registry.parse_frontmatter(text)


def production_state(site, sha, runner=subprocess.run) -> str:
    """success when a Production deployment whose LATEST status is success contains the merge commit
    (its own, or a later one that superseded it); otherwise the merge commit's own latest state."""
    env = site.publish["production_environment"]
    recent = gh(["api", f"repos/{site.repo}/deployments?environment={env}&per_page=10"], runner) or []
    own = None
    for deployment in recent:
        statuses = gh(["api", f"repos/{site.repo}/deployments/{deployment['id']}/statuses?per_page=1"], runner) or []
        latest = statuses[0]["state"] if statuses else "pending"
        if deployment.get("sha") == sha and own is None:
            own = latest
        if latest != "success":
            continue
        if deployment.get("sha") == sha:
            return "success"
        compare = gh(["api", f"repos/{site.repo}/compare/{sha}...{deployment['sha']}", "--jq", ".status"], runner)
        if compare in ("ahead", "identical"):
            return "success"
    return own or "absent"


def verify(record: Record, data: dict, runner=subprocess.run, opener=urllib.request.urlopen,
           wait=900, sleep=time.sleep) -> dict:
    """Production deployment of the merge commit, then every post address serves its own title."""
    merge_sha = data["merge_commit"]
    deadline = time.monotonic() + wait
    site = record.site
    state = production_state(site, merge_sha, runner)
    while state in ("absent", "pending", "queued", "in_progress") and time.monotonic() < deadline:
        sleep(20)
        state = production_state(site, merge_sha, runner)
    if state != "success":
        return record.update(status="deploy_unconfirmed", deployment=state)
    checks = []
    for slug in data["posts"]:
        meta = frontmatter(site, slug, merge_sha, runner)
        url, title = site.post_url(slug, meta), site.title(meta)
        if url is None:
            checks.append({"url": f"{site.origin} ({slug}: URL field missing)", "http": 0, "title": title, "ok": False})
            continue
        code, body = fetch(url, opener)
        page = re.search(r"<title>([^<]*)", body)
        shown = html.unescape(page.group(1)) if page else ""
        checks.append({"url": url, "http": code, "title": title,
                       "ok": code == 200 and bool(title) and site.shows_title(shown, title)})
    status = "published" if checks and all(c["ok"] for c in checks) else (
        "deployed_no_posts" if not checks else "live_check_failed")
    return record.update(status=status, deployment=state, live=checks)


def head_seen_at(site, sha, runner=subprocess.run):
    """When GitHub first recorded anything for this head: the earliest check suite or commit status
    created for it. Both are server times, created only after the push, so unlike a commit's own
    date they cannot be backdated. None when GitHub has recorded nothing yet."""
    suites = gh(["api", f"repos/{site.repo}/commits/{sha}/check-suites", "--jq", "[.check_suites[].created_at]"], runner)
    statuses = gh(["api", f"repos/{site.repo}/commits/{sha}/statuses?per_page=100", "--jq", "[.[].created_at]"], runner)
    stamps = [t for t in (suites or []) + (statuses or []) if isinstance(t, str)]
    return min(datetime.fromisoformat(t.replace("Z", "+00:00")) for t in stamps) if stamps else None


def bind(site_id, authority, approval_id, reviewed_head=None, runner=subprocess.run) -> dict:
    """Record the owner's approval: the pull request number, the time, and the head the owner reviewed.

    reviewed_head is the full 40-character commit id the owner looked at (a short prefix can be forged). If PR N's head on
    GitHub is anything else now, nothing is bound, so a push made after the review can't ride along."""
    site = merge_site(site_id)
    number = parse_authority(authority)
    if number is None:
        raise Refused(f'Only the exact words "merge N" can publish a {site.entity} pull request.')
    if not isinstance(approval_id, str) or not approval_id.strip():
        raise Refused("The approval needs an id (any unique text, such as today's date and a letter).")
    record = Record(site, number)
    with record.lock():
        head = view(site, number, runner).get("headRefOid")
        if not isinstance(head, str) or not SHA.match(head):
            raise Refused(f"PR {number} has no readable head; nothing was merged.")
        want = (reviewed_head or "").strip().lower()
        if not re.fullmatch(r"[0-9a-f]{40}", want):
            raise Refused("Give the full 40-character commit id you reviewed (--head); nothing was bound.")
        if head.lower() != want:
            raise Refused(f"PR {number} is now at {head[:12]}, not the {want[:12]} you reviewed. "
                          f"Review the new version and approve again; nothing was bound.")
        binding = {"pr": number, "authority_at": datetime.now(timezone.utc).isoformat(), "head_sha": head}
        stored = record.bind_message(approval_id, binding)
        if stored["pr"] != number:
            raise Refused("That approval id is already bound to a different pull request; nothing was merged.")
        return stored


def run(site_id, approval_id, runner=subprocess.run, opener=urllib.request.urlopen, store=None, wait=900,
        sleep=time.sleep, yes=False) -> dict:
    """Use a stored binding. Without yes, only report whether the merge would go ahead."""
    site = merge_site(site_id)
    root = Path(store) if store is not None else STORE_ROOT / site.publish["store"]
    marker = root / "messages" / (hashlib.sha256(approval_id.encode()).hexdigest() + ".json")
    if not marker.is_file():
        raise Refused("That approval id has no recorded binding. Run bind first; nothing was merged.")
    found = json.loads(marker.read_text())
    number, bound_head = found["pr"], found["head_sha"]
    said_at = datetime.fromisoformat(found["authority_at"])
    record = Record(site, number, store)
    with record.lock():
        existing = record.read()
        if existing is not None and (existing.get("message_id") == approval_id
                                     or existing.get("status") != "merge_refused"):
            return reconcile(record, existing, runner, opener, wait, sleep)
        if existing is not None:
            pr = view(site, number, runner)
            if pr.get("state") == "MERGED":
                return finish(record, runner, opener, wait, sleep)
        pr = view(site, number, runner)
        check_ready(site, pr)
        if pr["headRefOid"] != bound_head:
            raise Refused(f"PR {number} changed after you approved it. Review the new version and send merge {number} again.")
        head_at = head_seen_at(site, bound_head, runner)
        if head_at is None or head_at > said_at:
            raise Refused(f"PR {number}'s head was not on GitHub before your approval; nothing was merged.")
        if not yes:
            return {"status": "ready", "pr": number, "head_sha": bound_head, "posts": posts(site, pr),
                    "note": "Everything checks out. Run again with --yes to merge."}
        if not record.consume_message(approval_id):
            raise Refused("That approval id already drove a merge attempt; a new merge needs a new approval.")
        if existing is not None:
            os.replace(record.path, record.path.with_name(f"{number}-refused-{time.time_ns()}-{os.getpid()}.json"))
        data = {"site": site.site_id, "pr": number, "repo": site.repo, "head_sha": bound_head, "branch": pr["headRefName"],
                "message_id": approval_id, "authority_at": said_at.isoformat(), "bound_at": now(),
                "status": "merging", "posts": posts(site, pr)}
        if not record.create(data):
            raise Refused(f"PR {number} already has an action in progress.")
        try:
            gh(["pr", "merge", str(number), "--repo", site.repo, "--squash", "--match-head-commit", bound_head], runner)
        except RuntimeError as exc:
            record.update(merge_error=str(exc))
        return finish(record, runner, opener, wait, sleep)


def reconcile(record, existing, runner, opener, wait, sleep) -> dict:
    """This approval (or an earlier one) already acted: never merge again, only re-read and verify."""
    if existing.get("status") == "merged" and existing.get("merge_commit"):
        return {**verify(record, existing, runner, opener, wait, sleep), "duplicate": True}
    if existing.get("status") in ("merging", "merge_uncertain", "deploy_unconfirmed", "live_check_failed"):
        return {**finish(record, runner, opener, wait, sleep), "duplicate": True}
    return {**existing, "duplicate": True}


def finish(record, runner, opener, wait, sleep, confirm=3) -> dict:
    """Read the pull request's own state: merged at the pinned head -> verify; otherwise report, never re-merge.
    A failed merge counts as refused only after the pull request reads open at the same head several times."""
    data = record.read()
    for attempt in range(confirm):
        pr = view(record.site, data["pr"], runner)
        if pr.get("state") == "MERGED":
            break
        if attempt < confirm - 1:
            sleep(10)
    merged_oid = (pr.get("mergeCommit") or {}).get("oid")
    if pr.get("state") == "MERGED" and pr.get("headRefOid") == data["head_sha"] and merged_oid:
        data = record.update(status="merged", merge_commit=merged_oid, merged_seen_at=now())
        return verify(record, data, runner, opener, wait, sleep)
    if pr.get("state") == "MERGED":
        return record.update(status="merged_other_head", pr_head=pr.get("headRefOid"))
    if (pr.get("state") == "OPEN" and data.get("merge_error") and not merged_oid
            and pr.get("headRefOid") == data["head_sha"]):
        return record.update(status="merge_refused", pr_state="OPEN")
    return record.update(status="merge_uncertain", pr_state=pr.get("state"))


def summary(data: dict) -> str:
    n, status = data.get("pr"), data.get("status")
    if status == "ready":
        return f"PR {n} is ready to merge at {str(data['head_sha'])[:12]}. {data['note']}"
    if status == "published":
        urls = "\n".join(c["url"] for c in data.get("live", []))
        return (f"PR {n} merged at {data['head_sha'][:12]} and published. Production deployment confirmed.\n{urls}")
    if status == "deployed_no_posts":
        return f"PR {n} merged and Production deployed; it changed no post pages to check."
    if status == "merge_refused":
        return f"PR {n} was not merged: {data.get('merge_error', 'GitHub refused the merge')}. Nothing was published."
    if status == "deploy_unconfirmed":
        return f"PR {n} merged, but the Production deployment is {data.get('deployment')}. Not yet published."
    if status == "live_check_failed":
        bad = ", ".join(c["url"] for c in data.get("live", []) if not c["ok"])
        return f"PR {n} merged and deployed, but these pages did not show their post: {bad}."
    return f"PR {n}: {status}. Nothing further was merged."


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("bind", help="record your approval and the exact version you reviewed")
    b.add_argument("--site", required=True, help="site id from the sites folder, e.g. example.org")
    b.add_argument("--authority", required=True, help='the exact words "merge N"')
    b.add_argument("--approval-id", required=True, help="any unique text for this approval")
    b.add_argument("--head", required=True, help="the full 40-character commit id you reviewed")
    r = sub.add_parser("run", help="check readiness, and merge and verify when --yes is given")
    r.add_argument("--site", required=True)
    r.add_argument("--approval-id", required=True)
    r.add_argument("--yes", action="store_true", help="actually merge")
    r.add_argument("--wait", type=int, default=900, help="seconds to wait for the live deployment")
    s = sub.add_parser("status", help="show the stored record for a pull request")
    s.add_argument("--site", required=True)
    s.add_argument("number", type=int)
    args = parser.parse_args(argv)
    try:
        if args.cmd == "bind":
            print(json.dumps({"ok": True, **bind(args.site, args.authority, args.approval_id, args.head)}))
            return 0
        if args.cmd == "run":
            data = run(args.site, args.approval_id, yes=args.yes, wait=args.wait)
        else:
            data = Record(merge_site(args.site), args.number).read() or {}
    except Refused as exc:
        print(json.dumps({"ok": False, "refused": str(exc)}))
        return 2
    print(json.dumps({"ok": True, "summary": summary(data) if data else "No record.", "record": data}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
