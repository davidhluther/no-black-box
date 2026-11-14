#!/usr/bin/env python3
"""Check that original nonblank lines still exist after a document split.

Read the old file from a pinned Git commit and compare it with explicitly
selected local files. Text is never printed without --show. This is a line
presence check, not a judgment about meaning, order, permissions, or approval.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys

MAX_BYTES = 2 * 1024 * 1024


class CheckError(Exception):
    pass


def git_bytes(repo, *args):
    env = dict(os.environ)
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        env.pop(key, None)
    env.update(GIT_OPTIONAL_LOCKS="0", GIT_NO_REPLACE_OBJECTS="1")
    try:
        result = subprocess.run(
            ["git", "--literal-pathspecs", "-c", "core.fsmonitor=false", "-C", str(repo), *args],
            capture_output=True, timeout=15, env=env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CheckError("The local Git read could not finish.") from exc
    if result.returncode:
        # Do not echo Git stderr, document contents, or an arbitrary object body.
        raise CheckError("The requested Git revision or source file could not be read.")
    return result.stdout


def baseline(repo, revision, old_file):
    old = PurePosixPath(old_file)
    if old.is_absolute() or not old.parts or ".." in old.parts or "\0" in old_file:
        raise CheckError("The old file must be a repository-relative file path.")
    oid = git_bytes(repo, "rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
    listing = git_bytes(repo, "ls-tree", "--full-tree", "-z", oid, "--", old.as_posix())
    if not listing or listing.split(b" ", 1)[0] not in (b"100644", b"100755"):
        raise CheckError("The old path must be a regular file tracked at that revision.")
    object_name = oid + ":" + old.as_posix()
    size = int(git_bytes(repo, "cat-file", "-s", object_name))
    if size > MAX_BYTES:
        raise CheckError("The old file exceeds the inspection byte limit.")
    data = git_bytes(repo, "cat-file", "blob", object_name)
    try:
        text = data.decode("utf-8")
    except UnicodeError as exc:
        raise CheckError("The old file must be UTF-8 text.") from exc
    return oid, data, text


def local_text(path):
    try:
        if not stat.S_ISREG(path.lstat().st_mode):
            raise CheckError("Each new path must be a regular file, not a symlink or directory.")
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                raise CheckError("Each new path must be a regular file, not a symlink or directory.")
            data = handle.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise CheckError("A new file exceeds the inspection byte limit.")
        return data.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise CheckError("A new file could not be read as UTF-8 text.") from exc


def compare_lines(old_text, new_texts, show=False):
    """Ignore blank lines and line endings; preserve all other whitespace."""
    present = {line for text in new_texts for line in text.splitlines() if line.strip()}
    original = [(number, line) for number, line in enumerate(old_text.splitlines(), 1) if line.strip()]
    missing = [{"line": number, **({"text": line} if show else {})}
               for number, line in original if line not in present]
    return {"result": "missing_lines" if missing else "all_lines_found",
            "nonblank_source_lines": len(original), "missing_lines": missing,
            "limits": "Line presence only: ignores blank lines and line endings; does not check order, occurrence counts, meaning, or approval."}


def check(repo, revision, old_file, new_files, show=False):
    repo = Path(repo).expanduser().resolve()
    repo = Path(git_bytes(repo, "rev-parse", "--show-toplevel").decode().strip())
    oid, source_bytes, old_text = baseline(repo, revision, old_file)
    paths = [Path(path).expanduser() for path in new_files]
    paths = [path if path.is_absolute() else repo / path for path in paths]
    texts = [local_text(path) for path in paths]
    result = compare_lines(old_text, texts, show)
    result.update(revision=oid, old_file=PurePosixPath(old_file).as_posix(),
                  source_sha256=hashlib.sha256(source_bytes).hexdigest(), new_file_count=len(paths))
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository containing the saved old file")
    parser.add_argument("--revision", required=True, help="Git revision to resolve and pin for the old file")
    parser.add_argument("--old", required=True, help="Old repository-relative file path")
    parser.add_argument("--new", action="append", required=True, help="Local new file, relative to --repo unless absolute; repeat for a split")
    parser.add_argument("--show", action="store_true", help="Explicitly print missing source text; default output is line numbers only")
    parser.add_argument("--json", action="store_true", help="Print a structured result")
    args = parser.parse_args(argv)
    try:
        result = check(args.repo, args.revision, args.old, args.new, args.show)
    except (CheckError, ValueError) as exc:
        print(f"Cannot check: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['result']}: {result['old_file']} at {result['revision']}")
        for row in result["missing_lines"]:
            print(f"  source line {row['line']}" + (f": {row['text']}" if args.show else ""))
        print(result["limits"])
    return 1 if result["missing_lines"] else 0


if __name__ == "__main__":
    sys.exit(main())
