# Support Code Format

A support code is one short line a check-up prints, so a helper can tell which step stopped you and why without a long back-and-forth. This page explains how to read one and, for kit authors, how to describe what a kit's check-up should look for.

Terms are in the [glossary](../guides/glossary.md).

## Reading a code

Example: `GR-FU-03-2-E14-v0.1.0-7KQ`

| Part | Example | Meaning |
|---|---|---|
| Kit code | GR | Which kit (GR grants, BP board packet, BK books, PW plain writing, and so on) |
| Version | FU | FR free, LC low cost, FU full |
| Guide and step | 03-2 | The first step that failed: guide three, step two |
| Problem | E14 | The kit's fixes table row, or a shared code from E90 up |
| Kit version | v0.1.0 | The kit release you have |
| Check hash | 7KQ | Three characters made from the pass or fail result of every check, which tells a helper whether your results match theirs |

When nothing failed, the step is `00-0` and the problem is `E00`. The Google Sheets version of the check-up prints the same shape with FR or LC in the version slot.

## What the report holds

The full version's check-up, `python3 support/doctor.py <kit-id>`, offers a plain-text report. Before saving, it prints the whole report on screen. It contains the kit name and version, your Python version, your operating system's name, and a list of checks with ok, skip, or FAIL beside each name. It never contains key values, passwords, file contents, folder paths, or your organization's details. It sends nothing anywhere. It saves `support-report.txt` in your current folder, and you choose whether to send it.

Use `--report` to save without being asked and `--no-prompt` to skip all questions.

## What the check-up looks at

1. The Python version (the program that runs kit scripts) is new enough.
2. The kit's folder exists.
3. `config.json` exists and is valid JSON (a strict text format), with required keys filled in.
4. Each required key name is set, in your environment or a `.env` file in the kit folder. Only the name is looked up.
5. Optional tools are on your PATH (the list of places your computer looks for programs). A missing optional tool shows as skip and never changes the code.

## Shared problem codes

| Code | Meaning |
|---|---|
| E90 | Python too old |
| E91 | Kit folder not found |
| E92 | config.json not found |
| E93 | config.json invalid or a required key is empty |
| E94 | A required key name isn't set |
| E95 | An optional tool is missing |

Each kit's `fixes.md` lists its own codes from E01 up. Fixes for E90 to E95 are in [getting help](../guides/getting-help.md#shared-fixes).

## Per-kit settings: doctor.json

A kit can describe what to check in `kits/<id>/doctor.json`. Every field is optional. Without the file, the check-up still tests Python, the kit folder, and `config.json`.

```json
{
  "code": "GR",
  "version": "0.1.0",
  "python_min": "3.9",
  "config_file": "config.json",
  "config_required_keys": ["org_name", "site_url"],
  "required_env": ["OPENAI_API_KEY"],
  "optional_commands": ["ffmpeg"],
  "steps": {
    "python": "01-1",
    "kit": "01-3",
    "config": "03-2",
    "env": "03-3",
    "command": "03-4"
  }
}
```

| Field | Meaning |
|---|---|
| code | Two-letter kit code. Defaults to the first two letters of the kit id, uppercased. |
| version | Kit version. Defaults to the plugin's version, then 0.0.0. |
| python_min | Lowest Python version, such as 3.9. |
| config_file | Name of the settings file. Defaults to config.json. |
| config_required_keys | Top-level keys in config.json that must not be empty. |
| required_env | Key names that must be set. Names only, never values. |
| optional_commands | Programs the kit can use if present. |
| steps | Which guide and step each kind of failure points to, in the form guide-step. Keys are python, kit, config, env, and command. |

The kit's own setup guides define these numbers, so point each kind of failure at the step where the reader fixes it.
