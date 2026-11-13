"""Static routing-table checks. Never execute tools or return document text."""
import os
from pathlib import Path
import re
import stat

MAX_READ_BYTES = 512 * 1024
MAX_DIRECTORY_CHILDREN = 25
MAX_DIRECTORY_ENTRIES = 1000
MARKER = re.compile(r"\b(?:DRAFT|UNCONFIRMED|SUPERSEDED)\b|\bDO[ \t]+NOT[ \t]+USE\b")


def cells(line, expected_columns=None):
    """Split pipes; expected width disambiguates an empty final data cell."""
    result, current, ticks, escaped = [], [], 0, False
    i = 0
    while i < len(line):
        char = line[i]
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            current.append(char)
            escaped = True
        elif char == "`":
            end = i
            while end < len(line) and line[end] == "`":
                end += 1
            count = end - i
            ticks = 0 if ticks == count else (count if not ticks else ticks)
            current.append(line[i:end])
            i = end - 1
        elif char == "|" and not ticks:
            result.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        i += 1
    result.append("".join(current).strip())
    if result and line.lstrip().startswith("|"):
        result.pop(0)
    if result and not result[-1] and line.rstrip().endswith("|") and (expected_columns is None or len(result) > expected_columns):
        result.pop()
    return result


def tables(text):
    lines = text.splitlines()
    fence = None
    i = 0
    while i < len(lines):
        marker = re.match(r"^\s*(`{3,}|~{3,})", lines[i])
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = (token[0], len(token))
            elif token[0] == fence[0] and len(token) >= fence[1]:
                fence = None
            i += 1
            continue
        if fence or "|" not in lines[i] or i + 1 >= len(lines):
            i += 1
            continue
        header = [re.sub(r"[^a-z]", "", c.lower()) for c in cells(lines[i])]
        separator = cells(lines[i + 1])
        if not {"job", "read"}.issubset(header) or len(separator) != len(header) or not all(re.fullmatch(r":?-{3,}:?", c) for c in separator):
            i += 1
            continue
        start = i + 1
        i += 2
        rows = []
        while i < len(lines) and "|" in lines[i] and lines[i].strip():
            rows.append((i + 1, cells(lines[i], expected_columns=len(header))))
            i += 1
        yield start, header, rows


def marker_lines(path, dir_fd=None):
    """Only regular local text, bounded reads, and source line numbers."""
    try:
        info = os.stat(path, dir_fd=dir_fd, follow_symlinks=False)
        if not stat.S_ISREG(info.st_mode):
            return {"status": "not_checked"}
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0), dir_fd=dir_fd)
        with os.fdopen(fd, "rb") as handle:
            if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
                return {"status": "not_checked"}
            data = handle.read(MAX_READ_BYTES + 1)
        if len(data) > MAX_READ_BYTES:
            return {"status": "not_checked"}
        text = data.decode("utf-8")
    except (OSError, UnicodeError):
        return {"status": "not_checked"}
    return {"status": "checked", "lines": [n for n, line in enumerate(text.splitlines(), 1) if MARKER.search(line)]}


def routed_read(target, source, root, resolve):
    """Inspect a file, or only immediate regular Markdown directory children."""
    path = root / target
    try:
        mode = path.lstat().st_mode
        if stat.S_ISREG(mode):
            return {"status": "checked", "files": [{"path": target, **marker_lines(path)}]}
        if not stat.S_ISDIR(mode):
            return {"status": "not_checked", "files": []}
        if not getattr(os, "O_NOFOLLOW", 0) or not getattr(os, "O_DIRECTORY", 0):
            return {"status": "not_checked", "files": []}
        directory_fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_DIRECTORY | getattr(os, "O_NONBLOCK", 0))
        try:
            if not stat.S_ISDIR(os.fstat(directory_fd).st_mode):
                return {"status": "not_checked", "files": []}
            candidates, partial = [], False
            with os.scandir(directory_fd) as entries:
                for number, child in enumerate(entries, 1):
                    if number > MAX_DIRECTORY_ENTRIES:
                        partial = True
                        break
                    if not child.name.lower().endswith(".md") or child.is_symlink() or not child.is_file(follow_symlinks=False):
                        continue
                    ref = resolve(source, root, str(path / child.name))
                    if ref["status"] == "exists":
                        candidates.append((ref["target"], child.name))
                    elif ref["status"] == "not_checked":
                        partial = True
            candidates.sort()
            if len(candidates) > MAX_DIRECTORY_CHILDREN:
                partial = True
            files = [{"path": child, **marker_lines(name, dir_fd=directory_fd)}
                     for child, name in candidates[:MAX_DIRECTORY_CHILDREN]]
        finally:
            os.close(directory_fd)
        partial = partial or any(child["status"] != "checked" for child in files)
        return {"status": "partly_checked" if partial else "checked", "directory": True, "files": files}
    except (OSError, TypeError, NotImplementedError):
        return {"status": "not_checked", "files": []}


def inspect(text, source, root, resolve, marker_allow=(), seen_markers=None):
    """`resolve` supplies the inventory's existing metadata/privacy policy."""
    findings, checked_tables, read_cache = [], [], {}
    seen_markers = seen_markers if seen_markers is not None else set()
    for table_line, header, rows in tables(text):
        checked_tables.append({"line": table_line, "has_skip": "skip" in header})
        if "skip" not in header:
            findings.append({"kind": "missing_skip_column", "line": table_line})
        for row_line, values in rows:
            if len(values) != len(header):
                findings.append({"kind": "unparsed_row", "line": row_line})
                continue
            paths = {column: set() for column in ("read", "skip", "use", "saveto")}
            for column in paths:
                if column not in header:
                    continue
                for token in re.findall(r"`([^`]+)`", values[header.index(column)]):
                    token = token.strip()
                    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", token) or any(s in token for s in (" --", " &&", " |")):
                        ref = {"target": "unverified routing token", "status": "not_checked"}
                    elif any(c.isspace() for c in token) and not any(c in token.split()[0] for c in ("/", ".", "~")):
                        ref = {"target": "unverified routing token", "status": "not_checked"}
                    else:
                        ref = resolve(source, root, token)
                        # A bare skill/tool name is not necessarily a file path.
                        if ref["status"] == "missing" and not any(c in token for c in ("/", ".", "~")):
                            ref = {"target": "unverified routing token", "status": "not_checked"}
                    if ref["status"] in ("exists", "missing"):
                        paths[column].add(ref["target"])
                    if column != "skip" and ref["status"] != "exists":
                        findings.append({"kind": "missing_path" if ref["status"] == "missing" else "path_not_checked",
                                         "line": row_line, "column": column, "path": ref["target"]})
                    if column == "read" and ref["status"] == "exists":
                        target = ref["target"]
                        if target not in read_cache:
                            read_cache[target] = routed_read(target, source, root, resolve)
                        scan = read_cache[target]
                        if scan["status"] == "not_checked":
                            findings.append({"kind": "read_not_checked", "line": row_line, "path": target})
                        elif scan["status"] == "partly_checked":
                            findings.append({"kind": "directory_partly_checked", "line": row_line, "path": target})
                        for child in scan["files"]:
                            if child["status"] != "checked":
                                findings.append({"kind": "read_not_checked", "line": row_line, "path": child["path"]})
                            for marked_line in child.get("lines", []):
                                key = (child["path"], marked_line)
                                allowed = any(p == key[0] and (line is None or line == marked_line) for p, line in marker_allow)
                                if key not in seen_markers and not allowed:
                                    seen_markers.add(key)
                                    findings.append({"kind": "explicit_marker", "line": row_line, "path": key[0], "target_line": marked_line})
            for overlap in sorted(paths["read"] & paths["skip"]):
                findings.append({"kind": "read_skip_overlap", "line": row_line, "path": overlap})
    return {"status": "checked" if checked_tables else "not_applicable", "tables": checked_tables,
            "advisories": findings,
            "marker_allow": [{"path": path, "line": line} for path, line in marker_allow],
            "limits": ["Only Job/Read pipe tables and literal backticked paths are checked; unsupported tokens remain unverified.",
                       "Unparsed rows have a cell-count mismatch and remain unverified.",
                       "Read directories open immediate regular Markdown children only, with child-count, entry-count, and per-file byte caps; partly checked directories stay explicit.",
                       "The inventory's existing scope exclusions apply; symlinks and nested directories are never followed.",
                       "Marker findings are deduplicated by target path and line; explicit allows affect only those marker findings.",
                       "Explicit uppercase marker occurrences are advisories, not proof of factual error or unsafe content.",
                       "No content text, web fetch, tool execution, recursive includes, or approval inference.",
                       "A missing Save-to path may be an intentional output location that has not been created."]}
