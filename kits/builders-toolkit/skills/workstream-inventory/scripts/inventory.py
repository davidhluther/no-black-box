#!/usr/bin/env python3
"""Enumerate every workstream on this machine, derived fresh from disk.

Exists because a written inventory goes stale and a remembered one is worse.
This reads the filesystem every run, so "what projects does David have" is a
question with a current answer rather than a recalled one.

It also diffs what it finds against the routing table in CLAUDE.md and
reports repos the canon doesn't mention -- the failure that actually caused
this to be written (2026-08-23: 17 repos on disk, 10 in the routing table,
7 invisible to any session that trusted the canon).

WORKTREES ARE ONE REPO. A repo can appear as several directories directly
under your workspace folder when it's checked out as multiple git worktrees
(for example three folders of one site that share one git-common-dir). Those are grouped and reported as a single logical repo
with N working directories, not N separate repos -- counting directories
instead of repos overstated the estate's size and made the same repo look
like independent workstreams. Both counts are reported: logical repos and
physical working directories.

PRIVACY: a folder named 'personal' is reported as existing and nothing more. Its contents
are never read, listed, or summarized -- that repo is local-only by a hard
standing rule.

Usage:
    python3 inventory.py                       # human-readable table
    python3 inventory.py --json                # machine-readable
    python3 inventory.py --stale 30             # flag repos untouched in 30+ days
    python3 inventory.py --json > run1.json
    python3 inventory.py --diff run1.json        # added/removed/changed since run1
    python3 inventory.py --include-registered-worktrees --index
    python3 inventory.py --projects-dir /path/to/workspace --routing-table /path/to/router.md
"""

import argparse
import hashlib
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote, unquote

PROJECTS_DIR = Path.home() / "Projects"
ROUTING_TABLE = Path.home() / "CLAUDE.md"
PRIVATE_DIRS = {"personal"}
DESCRIPTION_FILES = ["CLAUDE.md", "STATUS.md", "README.md", "AGENTS.md"]
ENTRYPOINT_FILES = ["AGENTS.md", "CLAUDE.md", "CODEX_HANDOFF.md", "CAPABILITIES.md", "STATUS.md", "README.md"]
ROUTER_FILES = ("AGENTS.md", "CLAUDE.md", "CODEX_HANDOFF.md")
MAX_ROUTER_BYTES = 512 * 1024
_ROUTING_CHECKER = None


def routing_checks(text, source, root, marker_allow=(), seen_markers=None):
    global _ROUTING_CHECKER
    if _ROUTING_CHECKER is None:
        spec = importlib.util.spec_from_file_location("workstream_routing_checks", Path(__file__).with_name("routing_checks.py"))
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except OSError:
            return {"status": "not_checked", "advisories": [], "reason": "routing checker module unavailable"}
        _ROUTING_CHECKER = module
    return _ROUTING_CHECKER.inspect(text, source, root, check_reference, marker_allow, seen_markers)


def parse_marker_allows(values):
    result = []
    for value in values:
        path, line = value, None
        if ":" in value:
            path, suffix = value.rsplit(":", 1)
            if not suffix.isdecimal() or int(suffix) < 1:
                raise ValueError("--marker-allow requires ROOT_RELATIVE_FILE[:POSITIVE_LINE]")
            line = int(suffix)
        candidate = Path(path)
        if not candidate.parts or candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError("--marker-allow paths must stay relative to the workspace root")
        pair = (candidate.as_posix(), line)
        if pair not in result:
            result.append(pair)
    return result


def router_references(text):
    """Explicit whole-line @ includes and inline Markdown links outside fences.

    Does not interpret prose, execute includes, fetch URLs, or load targets.
    Reference-style Markdown and anchors are intentionally outside this check.
    """
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1] and not line[marker.end():].strip():
                fence = None
            continue
        if fence:
            continue
        pointer = re.fullmatch(r'\s*@(?:"([^"]+)"|\x27([^\x27]+)\x27|([^\s]+))\s*', line)
        if pointer:
            target = next(v for v in pointer.groups() if v is not None)
            kind = "pointer" if any(c in target for c in (".", "/", "\\", "~")) else "ambiguous_at_mention"
            yield number, kind, target
        line = re.sub(r"(`+).*?\1", lambda match: " " * len(match.group(0)), line)
        # Balanced parentheses support paths such as notes/meeting(final).md.
        for match in re.finditer(r"!?\[[^\]\n]*\]\(", line):
            start = match.end()
            depth, escaped, end = 1, False, start
            for end in range(start, len(line)):
                char = line[end]
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == "(":
                    depth += 1
                elif char == ")":
                    depth -= 1
                    if depth == 0:
                        break
            if depth:
                continue
            payload = line[start:end].strip()
            if payload.startswith("<"):
                close = payload.find(">")
                if close < 0:
                    continue
                target = payload[1:close]
            else:
                token = re.match(r"(?:\\.|[^\s])+", payload)
                target = token.group(0) if token else ""
                target = re.sub(r"\\([\\ ()])", r"\1", target)
            if target and not target.startswith("#") and not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                yield number, "markdown", target


def check_reference(source, root, target, require_file=False):
    """Metadata-only target check; never follow a symlink or read a target."""
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target or any(c in target for c in ("\0", "\n", "\r", "*", "{", "}", "<", ">")):
        return {"target": "dynamic or invalid target", "status": "not_checked"}
    target = re.sub(r":\d+(?::\d+)?$", "", target)
    supplied = Path(target).expanduser()
    candidate = Path(os.path.abspath(supplied if supplied.is_absolute() else source.parent / supplied))
    try:
        relative = candidate.relative_to(root)
    except ValueError:
        return {"target": "outside workspace", "status": "outside_scope"}
    display = relative.as_posix()
    if any(part in PRIVATE_DIRS or part.startswith(".") for part in relative.parts):
        return {"target": "private or hidden target", "status": "outside_scope"}
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return {"target": display, "status": "not_checked", "reason": "symlink target not inspected"}
    try:
        info = candidate.stat()
    except FileNotFoundError:
        return {"target": display, "status": "missing"}
    except OSError:
        return {"target": display, "status": "not_checked", "reason": "target metadata unreadable"}
    if require_file and not stat.S_ISREG(info.st_mode):
        return {"target": display, "status": "not_checked", "reason": "instruction pointer target is not a regular file"}
    return {"target": display, "status": "exists"}


def audit_routers(directory, root, line_limit, exempt_paths=(), global_rules=False, check_routing_tables=False,
                  marker_allow=(), seen_markers=None):
    exempt_paths = {Path(path).as_posix() for path in exempt_paths}
    seen_markers = seen_markers if seen_markers is not None else set()
    checks = []
    for name in ROUTER_FILES:
        source = directory / name
        relative = source.relative_to(root).as_posix()
        if source.is_symlink():
            checks.append({"path": relative, "status": "not_checked", "reason": "router symlink not inspected"})
            continue
        if not source.is_file():
            continue
        try:
            with source.open("rb") as handle:
                data = handle.read(MAX_ROUTER_BYTES + 1)
            if len(data) > MAX_ROUTER_BYTES:
                checks.append({"path": relative, "status": "not_checked", "reason": "router exceeds inspection byte limit"})
                continue
            text = data.decode("utf-8")
        except (OSError, UnicodeError):
            checks.append({"path": relative, "status": "not_checked", "reason": "router text unreadable"})
            continue
        role = "handoff" if name == "CODEX_HANDOFF.md" else "router"
        exempt = global_rules or role == "handoff" or relative in exempt_paths
        if global_rules:
            tracking = {"tracked": None, "ignored": None, "tracking_checked": False}
        else:
            tracked_files = git_result(directory, "ls-files", "--cached", "--", name)
            ignored_files = git_result(directory, "ls-files", "--others", "--ignored", "--exclude-standard", "--", name)
            tracking = {"tracked": bool(tracked_files) if tracked_files is not None else None,
                        "ignored": bool(ignored_files) if ignored_files is not None else None,
                        "tracking_checked": tracked_files is not None and ignored_files is not None}
        checks.append({"path": relative, "status": "checked", "sha256": hashlib.sha256(data).hexdigest(),
                       "role": role, **tracking,
                       "line_count": len(text.splitlines()), "size_exempt": exempt,
                       "size_advisory": not exempt and len(text.splitlines()) > line_limit,
                       "references": [{"line": line, "kind": kind,
                                       **({"target": "ambiguous @ mention", "status": "not_checked"}
                                          if kind == "ambiguous_at_mention" else check_reference(source, root, target, require_file=kind == "pointer"))}
                                      for line, kind, target in router_references(text)]})
        if check_routing_tables and role == "router":
            checks[-1]["routing_checks"] = routing_checks(text, source, root, marker_allow, seen_markers)
    return checks


def entrypoint_audit(repos, root, line_limit=60, exempt_paths=(), check_routing_tables=False, marker_allow=()):
    """Attach read-only diagnostics. Identical text is advisory, not redundancy."""
    hashes = {}
    same_worktree = []
    seen_markers = set()
    for repo in repos:
        if repo.get("private"):
            continue
        for worktree in repo["worktrees"]:
            checks = audit_routers(root / worktree["path"], root, line_limit, exempt_paths, check_routing_tables=check_routing_tables,
                                   marker_allow=marker_allow, seen_markers=seen_markers)
            worktree["router_checks"] = checks
            local_hashes = {}
            for check in checks:
                if check.get("sha256") and check.get("line_count") and check["role"] == "router":
                    hashes.setdefault(check["sha256"], []).append((repo["path"], check["path"]))
                    local_hashes.setdefault(check["sha256"], []).append(check["path"])
            pairs = [sorted(paths) for paths in local_hashes.values() if len(paths) > 1]
            worktree["identical_router_pairs"] = pairs
            same_worktree.extend({"worktree": worktree["path"], "paths": paths} for paths in pairs)
    duplicates = [{"sha256": digest, "paths": sorted(path for _, path in rows),
                   "git_identity_count": len({identity for identity, _ in rows})}
                  for digest, rows in sorted(hashes.items()) if len({identity for identity, _ in rows}) > 1]
    return {"mode": "report-only", "line_limit": line_limit,
            "global_routers": audit_routers(root, root, line_limit, exempt_paths, global_rules=True, check_routing_tables=check_routing_tables,
                                            marker_allow=marker_allow, seen_markers=seen_markers),
            "identical_router_groups": duplicates,
            "same_worktree_identical_router_groups": same_worktree,
            "limits": ["Checks whole-line @ includes and inline local Markdown links outside fenced code only.",
                       "Does not fetch web links, validate anchors or line suffixes, parse reference-style Markdown, or follow includes recursively.",
                       "Private, hidden, outside-workspace, and symlink targets are not inspected.",
                       "Identical text across separate Git common directories is advisory; it may be intentional.",
                       "Tracking metadata is local only; workspace-global rules have no repository tracking verdict.",
                       "Size advisories never override mandatory rules or authorize a rewrite."]}


def git_result(repo, *args):
    """Local Git only; optional index refreshes must not write the checkout."""
    try:
        out = subprocess.run(
            ["git", "-c", "core.fsmonitor=false", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=10,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        )
        return out.stdout.strip() if out.returncode == 0 else None
    except (subprocess.TimeoutExpired, OSError):
        return None


def git(repo, *args):
    return git_result(repo, *args) or ""


def entrypoints(repo):
    """Names only. A file's presence establishes neither currency nor approval."""
    return [name for name in ENTRYPOINT_FILES
            if not (repo / name).is_symlink() and (repo / name).is_file()]


def common_dir(repo):
    """Absolute, resolved path to this worktree's shared git-common-dir.

    The main worktree of a repo reports its common-dir as the relative
    literal ".git"; a linked worktree (git worktree add) reports the main
    worktree's absolute .git path. Resolving both to an absolute, symlink-
    resolved path gives a stable grouping key: every worktree of the same
    repo resolves to the identical path.
    """
    out = git(repo, "rev-parse", "--git-common-dir")
    if not out:
        return None
    p = Path(out)
    if not p.is_absolute():
        p = repo / p
    try:
        return p.resolve()
    except OSError:
        return p


def describe(repo):
    """First meaningful prose line from the repo's own docs, if any."""
    for name in DESCRIPTION_FILES:
        f = repo / name
        if f.is_symlink() or not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("# "):
                in_fence = False
                for follow in lines[i + 1:]:
                    stripped = follow.strip()
                    # Track fenced code blocks -- otherwise the first "prose"
                    # line found is something like "yarn dev" out of a setup
                    # snippet, which described four repos identically.
                    if stripped.startswith("```"):
                        in_fence = not in_fence
                        continue
                    if in_fence:
                        continue
                    if stripped and not stripped.startswith(("#", "|", "-", "*", ">", "`")):
                        return (stripped[:150], name)
                return (line[2:].strip()[:150], name)
    return ("", "")


def _worktree_detail(d, root=None):
    status = git_result(d, "status", "--porcelain")
    return {
        "dir": d.name,
        "path": d.relative_to(root).as_posix() if root else d.name,
        "kind": "main" if (d / ".git").is_dir() else "linked",
        "branch": git(d, "rev-parse", "--abbrev-ref", "HEAD") or "?",
        "last_commit": git(d, "log", "-1", "--format=%cs") or "no commits",
        "uncommitted": len(status.splitlines()) if status is not None else None,
        "status_checked": status is not None,
        "entrypoints": entrypoints(d),
    }


def _group_worktrees(dirs_with_common, root=None):
    """Group top-level directories sharing a git-common-dir into one logical
    repo entry each. dirs_with_common: list of (Path, common_dir_key_str)."""
    groups = {}
    for entry, key in dirs_with_common:
        groups.setdefault(key, []).append(entry)

    repos = []
    for key, dirs in groups.items():
        dirs = sorted(set(dirs), key=lambda d: d.as_posix())
        # The main worktree is the one whose own .git IS the common dir --
        # that's the directory whose docs/description should represent the
        # logical repo (linked worktrees rarely carry their own README).
        primary = None
        for d in dirs:
            own_git = d / ".git"
            own_key = str(own_git.resolve()) if own_git.exists() else None
            if own_key == key:
                primary = d
                break
        if primary is None:
            primary = dirs[0]

        worktree_details = [_worktree_detail(d, root) for d in dirs]
        desc, desc_src = describe(primary)
        commit_dates = [w["last_commit"] for w in worktree_details
                         if w["last_commit"] != "no commits"]
        last = max(commit_dates) if commit_dates else "no commits"

        repos.append({
            "name": primary.name,
            "path": primary.relative_to(root).as_posix() if root else primary.name,
            "private": False,
            "worktree_count": len(dirs),
            "worktree_names": [d.name for d in dirs],
            "worktree_paths": [w["path"] for w in worktree_details],
            "worktrees": worktree_details,
            "last_commit": last,
            "branch": worktree_details[0]["branch"] if len(worktree_details) == 1 else None,
            "uncommitted": (sum(w["uncommitted"] for w in worktree_details)
                            if all(w["status_checked"] for w in worktree_details) else None),
            "entrypoints": entrypoints(primary),
            "has_remote": bool(git(primary, "remote")),
            "description": desc,
            "description_from": desc_src,
        })
    repos.sort(key=lambda r: r["name"])
    return repos


def _eligible_worktree(path, root):
    """Never traverse outside root, a private directory, or a symlink bridge."""
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    if not relative.parts or any(p in PRIVATE_DIRS or p.startswith(".") for p in relative.parts):
        return False
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            return False
    return path.is_dir() and (path / ".git").exists()


def scan(projects_dir=None, include_registered_worktrees=False, issues=None):
    """Returns (repos, plain_dirs, working_dir_count).

    repos: one entry per LOGICAL repo (worktrees of the same repo merged).
    working_dir_count: physical Git working directories inspected, excluding
    personal. With the opt-in flag, this also includes registered nested
    worktrees inside the root. Standalone nested clones remain outside scope.
    """
    requested_root = Path(os.path.abspath(Path(projects_dir or PROJECTS_DIR).expanduser()))
    projects_dir = requested_root.resolve()
    issues = issues if issues is not None else []
    repos, plain_dirs = [], []
    if not projects_dir.is_dir():
        return repos, plain_dirs, 0

    dirs_with_common = []
    working_dir_count = 0
    for entry in sorted(projects_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        if entry.name in PRIVATE_DIRS:
            repos.append({
                "name": entry.name, "private": True,
                "note": "local-only by standing rule; contents never read",
            })
            continue
        if entry.is_symlink():
            issues.append({"path": entry.name, "reason": "symlink not followed"})
            continue
        if not (entry / ".git").exists():
            plain_dirs.append(entry.name)
            continue
        cdir = common_dir(entry)
        if cdir is None:
            issues.append({"path": entry.name, "reason": "Git metadata could not be read"})
            continue
        working_dir_count += 1
        key = str(cdir)
        dirs_with_common.append((entry, key))

    if include_registered_worktrees:
        # Git's registry, not recursive filesystem walking, identifies candidates.
        # This includes worktrees/<repo>/<task> without inspecting arbitrary data.
        seen = {d for d, _ in dirs_with_common}
        checked = set()
        for entry, key in list(dirs_with_common):
            if key in checked:
                continue
            checked.add(key)
            listing = git_result(entry, "worktree", "list", "--porcelain", "-z")
            if listing is None:
                issues.append({"path": entry.name, "reason": "registered worktrees could not be read"})
                continue
            for field in listing.split("\0"):
                if not field.startswith("worktree "):
                    continue
                candidate = Path(os.path.abspath(field[len("worktree "):]))
                if candidate in seen:
                    continue
                if requested_root != projects_dir and candidate.is_relative_to(requested_root):
                    issues.append({"path": entry.name, "reason": "registered path uses a symlinked workspace alias; not followed"})
                    continue
                if not _eligible_worktree(candidate, projects_dir):
                    continue
                candidate_common = common_dir(candidate)
                if candidate_common is None or str(candidate_common) != key:
                    issues.append({"path": candidate.relative_to(projects_dir).as_posix(),
                                   "reason": "registered worktree identity could not be confirmed"})
                    continue
                seen.add(candidate)
                dirs_with_common.append((candidate, key))
                working_dir_count += 1

    repos.extend(_group_worktrees(dirs_with_common, projects_dir))
    return repos, plain_dirs, working_dir_count


def routed_names():
    """Repo names the routing table (CLAUDE.md in your home folder, by default) actually mentions."""
    if not ROUTING_TABLE.exists():
        return None
    text = ROUTING_TABLE.read_text(encoding="utf-8", errors="replace")
    found = set()
    for match in re.finditer(r"~/" + re.escape(PROJECTS_DIR.name) + r"/([A-Za-z0-9._-]+)", text):
        found.add(match.group(1))
    for match in re.finditer(r"`([A-Za-z0-9._-]+)/`", text):
        found.add(match.group(1))
    return found


def days_since(datestr):
    try:
        return (date.today() - datetime.strptime(datestr, "%Y-%m-%d").date()).days
    except (ValueError, TypeError):
        return None


def run(stale_days=None, projects_dir=None, routing_table=None, include_registered_worktrees=False,
        check_entrypoints=False, router_line_limit=60, exempt_routers=(), check_routing_tables=False, marker_allow=()):
    global ROUTING_TABLE
    prior_routing_table = ROUTING_TABLE
    if routing_table is not None:
        ROUTING_TABLE = routing_table
    try:
        issues = []
        repos, plain_dirs, working_dir_count = scan(projects_dir, include_registered_worktrees, issues)
        routed = routed_names()
    finally:
        ROUTING_TABLE = prior_routing_table

    tracked = [r for r in repos if not r.get("private")]

    unrouted = []
    routed_real = None
    if routed is not None:
        # A grouped repo counts as routed if ANY of its working-directory
        # names appear in the table -- a site checked out as "site-a" and "site-b" is routed
        # if either name (the main worktree's, say) is named.
        all_names = {n for r in tracked for n in r.get("worktree_names", [r["name"]])}
        routed_real = sorted(routed & all_names)
        unrouted = [
            r["name"] for r in tracked
            if not (set(r.get("worktree_names", [r["name"]])) & routed)
        ]

    for r in tracked:
        d = days_since(r.get("last_commit", ""))
        r["days_idle"] = d
        r["stale"] = (stale_days is not None and d is not None and d >= stale_days)

    report = {
        "schema_version": 2,
        "scanned_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "coverage": "top-level plus in-root registered worktrees" if include_registered_worktrees else "top-level only",
        "limitations": ["No recursive repository search; nested standalone clones are not discovered.",
                        "Personal contents, symlink targets, hidden paths, and out-of-root worktrees are excluded.",
                        "Git working directories sharing a common directory are grouped; separate clones remain separate.",
                        "Entry-point presence is not proof of current instructions, review, or authorization.",
                        "No runtime references, unique commits, or safe-to-archive decisions are checked."],
        "scan_issues": issues,
        "repo_count": len(tracked),
        "working_dir_count": working_dir_count,
        "private_count": len([r for r in repos if r.get("private")]),
        "routed_count": len(routed_real) if routed_real is not None else None,
        "unrouted": unrouted,
        "repos": repos,
        "non_repo_dirs": plain_dirs,
    }
    if check_entrypoints or check_routing_tables:
        report["entrypoint_audit"] = entrypoint_audit(repos, Path(projects_dir or PROJECTS_DIR).expanduser().resolve(),
                                                     router_line_limit, exempt_routers, check_routing_tables, marker_allow)
    return report


def print_human(rep, stale_days):
    extra = ""
    if rep["working_dir_count"] != rep["repo_count"]:
        extra = f"  ({rep['working_dir_count']} working directories -- some repos are checked out as multiple worktrees)"
    print(f"\n{rep['repo_count']} git repos  (scanned {rep['scanned_at']}; {rep['coverage']}){extra}")
    if rep["routed_count"] is not None:
        print(f"CLAUDE.md routing table mentions {rep['routed_count']}")
    print()

    rows = [r for r in rep["repos"] if not r.get("private")]
    rows.sort(key=lambda r: r.get("last_commit", ""), reverse=True)

    print(f"{'repo':<32} {'last commit':<12} {'idle':>5}  {'wip':>3} {'rmt':>3} {'wt':>3}  description")
    print("-" * 122)
    for r in rows:
        idle = f"{r['days_idle']}d" if r["days_idle"] is not None else "-"
        wip = "?" if r["uncommitted"] is None else (str(r["uncommitted"]) if r["uncommitted"] else "")
        rmt = "yes" if r["has_remote"] else "no"
        wt = str(r["worktree_count"]) if r["worktree_count"] > 1 else ""
        flag = " *" if r.get("stale") else ""
        print(f"{r['name']:<32} {r['last_commit']:<12} {idle:>5}  {wip:>3} {rmt:>3} {wt:>3}  {r['description'][:40]}{flag}")
        if r["worktree_count"] > 1:
            print(f"    worktrees: {', '.join(r['worktree_paths'])}")

    for r in rep["repos"]:
        if r.get("private"):
            print(f"\n{r['name']:<32} [{r['note']}]")

    if rep["non_repo_dirs"]:
        print(f"\nNon-repo directories: {', '.join(rep['non_repo_dirs'])}")

    if rep["unrouted"]:
        print(f"\n!! {len(rep['unrouted'])} repos NOT in the CLAUDE.md routing table:")
        for name in rep["unrouted"]:
            print(f"     {name}")
        print("   A session trusting the routing table alone would never see these.")

    if stale_days:
        stale = [r["name"] for r in rows if r.get("stale")]
        if stale:
            print(f"\n* {len(stale)} repos idle {stale_days}+ days: {', '.join(stale)}")
    for issue in rep["scan_issues"]:
        print(f"\nCheck: {issue['path']} -- {issue['reason']}")
    if "entrypoint_audit" in rep:
        audit = rep["entrypoint_audit"]
        print("\nRouter checks (report-only; size advice never overrides mandatory rules):")
        checks = audit["global_routers"] + [c for r in rep["repos"] if not r.get("private")
                                             for w in r["worktrees"] for c in w.get("router_checks", [])]
        for check in checks:
            if check["status"] != "checked":
                print(f"  {check['path']}: not checked ({check['reason']})")
            if check.get("size_advisory"):
                print(f"  {check['path']}: advisory size exceeded; inspect task routing before rewriting")
            if check.get("tracked") is False:
                print(f"  {check['path']}: untracked document; verify rollback and sharing before rewriting")
            for ref in check.get("references", []):
                if ref["status"] != "exists":
                    print(f"  {check['path']}:{ref['line']}: {ref['target']} -- {ref['status']}")
            route_check = check.get("routing_checks", {})
            if route_check.get("status") == "not_checked":
                print(f"  {check['path']}: routing not checked ({route_check.get('reason', 'unverified')})")
            for issue in route_check.get("advisories", []):
                location = f"{check['path']}:{issue['line']}"
                target = ""
                if "path" in issue:
                    suffix = f":{issue['target_line']}" if "target_line" in issue else ""
                    target = f" ({issue['path']}{suffix})"
                print(f"  {location}: {issue['kind']}{target}")
        for duplicate in audit["identical_router_groups"]:
            print(f"  Identical router text across repository identities (may be intentional): {', '.join(duplicate['paths'])}")
        for duplicate in audit["same_worktree_identical_router_groups"]:
            print(f"  Identical router copies in one checkout (may be intentional): {', '.join(duplicate['paths'])}")


def render_index(rep, full=False):
    """Markdown intended for CODEX_PROJECT_INDEX.md at the workspace root."""
    lines = ["# Project routing index", "", f"Generated {rep['scanned_at']}. Scope: {rep['coverage']}.", "",
             "Read the workspace instructions first, then the project's instructions and handoff.",
             "Links show files present at scan time. Their contents and currency have not been verified.",
             "This index authorizes no edits, moves, archive actions, installs, or publication.",
             "Working dirs counts checkouts, not active jobs. Use --index-full or --json for individual worktrees.", ""]
    if full:
        lines.extend(["| Working directory | Role | Branch | Docs present |", "|---|---|---|---|"])
    else:
        lines.extend(["| Primary checkout | Branch | Start here | Other docs present | Working dirs | Issues |",
                      "|---|---|---|---|---|---|"])
    def cell(value):
        return str(value).replace("|", "&#124;").replace("\n", " ").replace("\r", " ")
    for repo in rep["repos"]:
        if repo.get("private"):
            lines.append(f"| {cell(repo['name'])} | Private, excluded | Contents not inspected | |" + ("" if full else " | |"))
            continue
        if not full:
            primary = next(w for w in repo["worktrees"] if w["path"] == repo["path"])
            docs = primary["entrypoints"]
            routers = [n for n in ("AGENTS.md", "CLAUDE.md", "CODEX_HANDOFF.md") if n in docs]
            if not routers and "README.md" in docs:
                routers = ["README.md"]
            labels = {"AGENTS.md": "Rules", "CLAUDE.md": "Claude", "CODEX_HANDOFF.md": "Handoff", "README.md": "README"}
            links = ", ".join(f"[{labels[n]}]({quote(repo['path'] + '/' + n, safe='/')})" for n in routers)
            other = ", ".join(n.removesuffix(".md") for n in docs if n not in routers)
            flags = []
            if any(not w["status_checked"] for w in repo["worktrees"]):
                flags.append("status unknown")
            if any(i["path"] in repo["worktree_paths"] for i in rep["scan_issues"]):
                flags.append("scan issue")
            if primary["kind"] != "main":
                flags.append("main checkout outside scope")
            if any(check.get("size_advisory") or check.get("status") != "checked"
                   or any(ref["status"] != "exists" for ref in check.get("references", []))
                   for w in repo["worktrees"] for check in w.get("router_checks", [])):
                flags.append("router advisory")
            if any(c.get("tracked") is False and c.get("role") == "router"
                   for w in repo["worktrees"] for c in w.get("router_checks", [])):
                flags.append("untracked router")
            if any(c.get("status") == "checked" and c.get("role") == "router" and not c.get("tracking_checked")
                   for w in repo["worktrees"] for c in w.get("router_checks", [])):
                flags.append("tracking unknown")
            if any(w.get("identical_router_pairs") for w in repo["worktrees"]):
                flags.append("identical router copies")
            if any(c.get("routing_checks", {}).get("advisories") for w in repo["worktrees"] for c in w.get("router_checks", [])):
                flags.append("routing advisory")
            if any(c.get("routing_checks", {}).get("status") == "not_checked" for w in repo["worktrees"] for c in w.get("router_checks", [])):
                flags.append("routing unknown")
            lines.append(f"| {cell(repo['path'])} | {cell(primary['branch'])} | {links or 'No standard router found'} | {cell(other)} | {repo['worktree_count']} | {', '.join(flags)} |")
            continue
        for worktree in repo["worktrees"]:
            path = worktree["path"]
            role = "Repository checkout" if worktree["kind"] == "main" else f"Linked worktree (group {repo['path']})"
            links = ", ".join(f"[{name}]({quote(path + '/' + name, safe='/')})" for name in worktree["entrypoints"])
            lines.append(f"| {cell(path)} | {cell(role)} | {cell(worktree['branch'])} | {links or 'No standard entry point found'} |")
    lines.extend(["", "## Scope limits", ""] + [f"- {s}" for s in rep["limitations"]])
    if rep["scan_issues"]:
        lines.extend(["", "## Scan issues", ""] + [f"- {cell(i['path'])}: {i['reason']}" for i in rep["scan_issues"]])
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# --diff: compare this run's report against a previously saved --json report.
# ---------------------------------------------------------------------------
_DIFF_FIELDS = ("last_commit", "branch", "uncommitted", "worktree_count",
                 "has_remote", "description", "worktree_paths", "worktrees", "entrypoints")
_WORKTREE_DIFF_FIELDS = ("dir", "path", "kind", "branch", "last_commit", "uncommitted", "status_checked", "entrypoints")


def _diff_value(repo, field):
    value = repo.get(field)
    if field == "worktrees" and value is not None:
        # Compare checkout metadata, never diagnostics added by optional audits.
        value = [{key: row[key] for key in _WORKTREE_DIFF_FIELDS if key in row} for row in value]
        value.sort(key=lambda row: row.get("path", row.get("dir", "")))
    return value


def diff_reports(previous, current):
    """Added/removed/changed logical repos between two `run()` reports."""
    prev_repos = {r["name"]: r for r in previous["repos"] if not r.get("private")}
    curr_repos = {r["name"]: r for r in current["repos"] if not r.get("private")}

    added = sorted(set(curr_repos) - set(prev_repos))
    removed = sorted(set(prev_repos) - set(curr_repos))

    changed = []
    for name in sorted(set(curr_repos) & set(prev_repos)):
        p, c = prev_repos[name], curr_repos[name]
        deltas = {}
        for field in _DIFF_FIELDS:
            before, after = _diff_value(p, field), _diff_value(c, field)
            if before != after:
                deltas[field] = {"before": before, "after": after}
        if deltas:
            changed.append({"name": name, "changes": deltas})

    return {
        "previous_scanned_at": previous.get("scanned_at"),
        "current_scanned_at": current.get("scanned_at"),
        "added": added,
        "removed": removed,
        "changed": changed,
        "unrouted_added": sorted(set(current.get("unrouted", [])) - set(previous.get("unrouted", []))),
        "unrouted_removed": sorted(set(previous.get("unrouted", [])) - set(current.get("unrouted", []))),
    }


def print_diff_human(d):
    print(f"\nDiff: {d['previous_scanned_at']} -> {d['current_scanned_at']}")
    if not (d["added"] or d["removed"] or d["changed"]):
        print("No changes.")
    if d["added"]:
        print(f"\n+ {len(d['added'])} new repo(s):")
        for n in d["added"]:
            print(f"    + {n}")
    if d["removed"]:
        print(f"\n- {len(d['removed'])} removed repo(s):")
        for n in d["removed"]:
            print(f"    - {n}")
    if d["changed"]:
        print(f"\n~ {len(d['changed'])} changed repo(s):")
        for entry in d["changed"]:
            print(f"    ~ {entry['name']}")
            for field, delta in entry["changes"].items():
                print(f"        {field}: {delta['before']!r} -> {delta['after']!r}")
    if d["unrouted_added"]:
        print(f"\n!! newly unrouted: {', '.join(d['unrouted_added'])}")
    if d["unrouted_removed"]:
        print(f"\nno longer unrouted (routing table updated): {', '.join(d['unrouted_removed'])}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true")
    p.add_argument("--index", action="store_true", help="Print a root-relative Markdown routing index to stdout")
    p.add_argument("--index-full", action="store_true", help="Print the detailed Markdown index with every worktree")
    p.add_argument("--projects-dir", type=Path, default=PROJECTS_DIR, help="Workspace root to inspect")
    p.add_argument("--routing-table", type=Path, default=ROUTING_TABLE, help="Routing table to compare with")
    p.add_argument("--include-registered-worktrees", action="store_true",
                   help="Include Git-registered worktrees within the workspace, without a recursive scan")
    p.add_argument("--check-entrypoints", action="store_true", help="Report router pointer/link validity and size advisories")
    p.add_argument("--check-routing-tables", action="store_true", help="Opt in to static path/overlap/marker advisories for Job/Read tables")
    p.add_argument("--marker-allow", action="append", default=[], metavar="ROOT_RELATIVE_FILE[:LINE]",
                   help="Silence intentional marker findings for one exact file or line only; repeat as needed")
    p.add_argument("--router-line-limit", type=int, default=60, help="Advisory router line limit; never a failure gate")
    p.add_argument("--exempt-router", action="append", default=[], metavar="ROOT_RELATIVE_PATH",
                   help="Exempt a router from size advice only; root global routers are always size-exempt")
    p.add_argument("--stale", type=int, default=None, help="Flag repos idle this many days or more")
    p.add_argument("--diff", metavar="PREVIOUS.json", default=None,
                    help="Compare against a previous --json report; prints added/removed/changed repos")
    args = p.parse_args()

    if (args.index or args.index_full) and (args.json or args.diff or (args.index and args.index_full)):
        p.error("choose only one of --index, --index-full, --json, or --diff")
    if not args.projects_dir.expanduser().is_dir():
        p.error("--projects-dir must be an existing directory")
    if args.router_line_limit < 1:
        p.error("--router-line-limit must be positive")
    if any(Path(path).is_absolute() or ".." in Path(path).parts for path in args.exempt_router):
        p.error("--exempt-router paths must stay relative to the workspace root")
    exempt_routers = [Path(path).as_posix() for path in args.exempt_router]
    if args.marker_allow and not args.check_routing_tables:
        p.error("--marker-allow requires --check-routing-tables")
    try:
        marker_allow = parse_marker_allows(args.marker_allow)
    except ValueError as exc:
        p.error(str(exc))
    report = run(args.stale, args.projects_dir, args.routing_table.expanduser(), args.include_registered_worktrees,
                 args.check_entrypoints, args.router_line_limit, exempt_routers, args.check_routing_tables, marker_allow)

    if args.diff:
        try:
            with open(args.diff, encoding="utf-8") as f:
                previous = json.load(f)
        except (OSError, ValueError) as e:
            sys.stderr.write(f"FATAL: could not read --diff baseline {args.diff}: {e}\n")
            sys.exit(2)
        d = diff_reports(previous, report)
        if args.json:
            print(json.dumps(d, indent=2))
        else:
            print_diff_human(d)
    elif args.index or args.index_full:
        print(render_index(report, full=args.index_full), end="")
    elif args.json:
        print(json.dumps(report, indent=2))
    else:
        print_human(report, args.stale)
