---
name: workstream-inventory
description: Lists every project folder in your workspace, read fresh from disk, and compares it with the routing table in your top-level CLAUDE.md file. Reports last commit, idle days, branch, unsaved changes, remote and description for each repository, flags repositories your instructions never mention, and can check that your instruction files point at things that exist. Use before answering any "what are all my projects" question, or when a coordinating session needs a current picture of your workspace.
---

# Workstream inventory

Works in: Claude Code (full version). It needs Python 3 and the project folders on your own computer. It only reads. It changes nothing in any repository.

Settings: if the kit's `config.json` exists, read the `workspace` block (projects folder and routing table path) and pass them as `--projects-dir` and `--routing-table`. Otherwise ask the user.

## Why this exists

A coordinator that undercounts your projects is worse than none, because you cannot tell an omission from a judgment call. The question that started this was "I don't know if that's because you forgot dozens of them or judged that only those were relevant."

Two root causes, and trying harder to remember fixes neither.

1. **The written list is incomplete.** The routing table (a short file of "when the work is about X, go to folder Y") covered eleven of nineteen repositories on the day this was written. Eight projects were invisible to any session that trusted it.
2. **A written inventory goes stale, and a remembered one is worse.** So this derives the list from the folders on disk each time you run it.

## Usage

Run from this skill's folder. Replace the folder paths with your own.

```bash
python3 scripts/inventory.py
python3 scripts/inventory.py --stale 30                 # flag repositories idle 30 days or more
python3 scripts/inventory.py --json                     # for chaining
python3 scripts/inventory.py --json > run1.json         # save a baseline
python3 scripts/inventory.py --diff run1.json           # added, removed or changed since run1
python3 scripts/inventory.py --include-registered-worktrees --index
python3 scripts/inventory.py --projects-dir /path/to/workspace --routing-table /path/to/CLAUDE.md --index
python3 scripts/inventory.py --check-entrypoints --json
python3 scripts/inventory.py --check-routing-tables --json
```

Each repository gets its last commit date, days idle, branch, count of uncommitted changes, whether a remote exists, and a description pulled from its own `CLAUDE.md`, `STATUS.md`, `README.md` or `AGENTS.md`. The run ends with the list of repositories the routing table does not mention. A scan of a large workspace takes a second or two.

Defaults: the workspace is a folder named `Projects` in your home folder, and the routing table is `CLAUDE.md` in your home folder. Use `--projects-dir` and `--routing-table` for anything else.

**Worktrees of one repository count as one repository.** A git worktree is an extra working folder that shares one project's history. If a site is checked out in three folders under your workspace, the report shows one logical repository with three working directories, and gives both counts (`repo_count` and `working_dir_count`). Before this was fixed, three folders of one site made it look like three independent projects.

## The portable routing index

`--include-registered-worktrees` asks git for the linked working folders inside the workspace. It does not search recursively. `--index` prints one compact row per repository (primary branch, links to its instruction files, other docs present, checkout count and issue flags) for a project index file at your workspace root. `--index-full` lists every folder. It writes only to the screen, so save the file on purpose.

The index shows where a session can start. Files being present does not mean they are current, reviewed or approved.

## Optional router checks

`--check-entrypoints` also reads the instruction files (`AGENTS.md`, `CLAUDE.md`, `CODEX_HANDOFF.md`) in each checkout. It checks whole-line `@` includes and local Markdown links, and records whether each target exists using file metadata, without opening it. It reports each target as existing, missing, not checked or outside scope. Web links are not fetched, anchors are not validated and include chains are not followed.

The default advisory size for a router file is 60 lines (`--router-line-limit` changes it, `--exempt-router` exempts a named file from size advice only). Identical router text shared across different repositories is reported by hash without copying it. Identical text can be intentional, so this proves neither redundant work nor that deleting is safe.

`--check-routing-tables` checks Markdown tables with Job and Read columns. For literal paths in backticks it reports Read, Use and Save-to targets that do not exist, a path listed in both Read and Skip in one row, and a table with no Skip column. Existing Read files are scanned for the uppercase markers DRAFT, UNCONFIRMED, SUPERSEDED and DO NOT USE. A marker can appear in an example, so a hit is a prompt to look, not proof the file is wrong. Repeat `--marker-allow path:line` to silence a known intentional marker. Findings return line numbers and paths, never the file's text.

All of these are advisories. The command exits successfully when it can produce them. None overrides your rules, authorizes rewriting a file or records an approval.

## Check a document split before handoff

`scripts/verbatim_move_check.py` answers one question. When you split a long instruction file into several, did every line survive? It reads the original from a chosen git revision (never your possibly edited current copy), and checks that each nonblank line appears word for word in the new files.

```bash
python3 scripts/verbatim_move_check.py --repo /path/to/project --revision main \
  --old CLAUDE.md --new CLAUDE.md --new docs/task-context.md
```

It lists the missing line numbers. Add `--show` only when displaying the source text is safe. Exit code 0 means every line is present, 1 means some are missing, 2 means the inputs could not be checked. It tests presence only, not order, counts, meaning or correctness, and it cannot catch a stale claim that was preserved exactly. An intentional rewrite still needs a person to account for each missing line.

## Rules this encodes

- **Never hand over a bare list.** Run this, then say what you filtered and why. "All 19" and "6 of 19, filtered to active client work" are both fine. An unlabeled 6 is not.
- **A folder named `personal` is reported as existing and nothing else.** Its contents are never read, listed or summarized. Hidden folders and symlink targets are skipped too. A tool that surveys your folders must not become the thing that leaks the ones you keep private.
- **Unrouted repositories are a finding, not noise.** When the report names a repository the routing table lacks, tell the owner. Do not quietly work around the gap. A group of worktrees counts as routed if any of its folder names appears in the table.

## Known limits

- The description is the first prose line after the first heading. A README that opens with an indented code block shows a code line instead. Cosmetic only.
- The routing diff matches on folder name. A repository mentioned only by description, with neither path nor backticked name, shows as unrouted.
- The default scan covers top-level folders in the workspace. The worktree option adds linked checkouts inside it. Separate clones, nested standalone clones and repositories elsewhere stay out of scope. Read `coverage`, `limitations` and `scan_issues` in the report before treating it as complete, and treat a count change after changing coverage as a coverage change, not as work created or lost.
- A failed status read shows as `?`, never as clean.
- `--diff` matches by name. If a worktree group's main folder changes between runs, the diff shows one removed and one added.
