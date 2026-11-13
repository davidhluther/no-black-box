import re
"""Shared helpers for the grants-pipeline engine: config loading, path resolution, name guard.

Every engine script takes --config <org.json>. Paths in the config expand "~"; paths under
"paths" (except drive_map_glob, url_overrides and plugin) are relative to paths.data_dir.
"""
import argparse
import csv
import importlib.util
import json
from pathlib import Path


class ConfigError(Exception):
    pass


FILES = {
    "pipeline_csv": "pipeline-rows.csv",
    "intel_csv": "funder-intel.csv",
    "wider_net_csv": "wider-net.csv",
    "dossier_index_csv": "dossier-index.csv",
    "start_here": "START-HERE.md",
    "links_json": "links.json",
    "research_urls": "research-urls.json",
    "dossier_urls": "dossier-urls.json",
    "dossiers_dir": "funder-dossiers",
    "research_dir": "research",
    "sweep_dir": "sweep",
}

DEFAULT_STATUSES = [
    {"name": "Prospect", "role": "prospect", "class": "open"},
    {"name": "LOI Submitted", "role": "loi", "class": "open"},
    {"name": "Submitted", "role": "submitted", "class": "open"},
    {"name": "Pending Decision", "role": "pending", "class": "open"},
    {"name": "Awarded", "role": "awarded", "class": "won"},
    {"name": "Awarded-Reduced", "role": "awarded_reduced", "class": "won"},
    {"name": "Declined", "role": "declined", "class": "lost"},
    {"name": "Not Pursued", "role": "not_pursued", "class": "open"},
    {"name": "Outcome Unknown", "role": "unknown", "class": "unknown"},
    {"name": "Closed", "role": "closed", "class": "open"},
]


def expand(p):
    return Path(str(p)).expanduser()


def load_config(path):
    """Read an org config, validate the required keys and resolve every path."""
    path = expand(path).resolve()
    try:
        cfg = json.loads(path.read_text())
    except FileNotFoundError:
        raise ConfigError(f"config not found: {path}")
    except json.JSONDecodeError as e:
        raise ConfigError(f"config is not valid JSON ({path}): {e}")
    cfg = {k: v for k, v in cfg.items() if not k.startswith("_")}  # "_comment" keys are notes
    org = cfg.get("org") or {}
    for k in ("name", "full_name"):
        if not org.get(k):
            raise ConfigError(f"config needs org.{k}")
    paths = cfg.get("paths") or {}
    if not paths.get("data_dir"):
        raise ConfigError("config needs paths.data_dir")
    data = expand(paths["data_dir"])
    resolved = {"data_dir": data}
    for key, default in FILES.items():
        resolved[key] = data / paths.get(key, default)
    for key in ("xlsx_out", "html_out"):
        if paths.get(key):
            resolved[key] = data / paths[key]
    if paths.get("drive_map_glob"):
        resolved["drive_map_glob"] = expand(paths["drive_map_glob"])
    for key in ("url_overrides",):
        if paths.get(key):
            resolved[key] = path.parent / paths[key] if not Path(paths[key]).expanduser().is_absolute() \
                else expand(paths[key])
    cfg["paths"] = resolved
    cfg["_config_path"] = path
    cfg.setdefault("statuses", DEFAULT_STATUSES)
    for s in cfg["statuses"]:
        s.setdefault("class", "open")
    cfg.setdefault("exclude_names", [])
    cfg.setdefault("text", {})
    cfg["text"].setdefault("xlsx", {})
    cfg["text"].setdefault("page", {})
    cfg.setdefault("theme", {})
    return cfg


def parse_args(argv, extra=None, desc=None):
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument("--config", required=True, help="path to the org config (orgs/<slug>.json)")
    if extra:
        extra(ap)
    return ap.parse_args(argv)


def read_csv(path):
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def roles(cfg, *wanted):
    """Names of the configured statuses holding any of the given roles."""
    return [s["name"] for s in cfg["statuses"] if s.get("role") in wanted]


def status_name(cfg, role):
    names = roles(cfg, role)
    return names[0] if names else None


def status_class(cfg):
    return {s["name"]: s["class"] for s in cfg["statuses"]}


def contains_excluded(text, names):
    low = (text or "").lower()
    return [n for n in names if n and n.lower() in low]


def assert_clean(cfg, text, what):
    """Refuse to write output that mentions an excluded name (another org, say)."""
    hits = contains_excluded(text, cfg.get("exclude_names", []))
    if hits:
        raise SystemExit(f"refusing to write {what}: it mentions excluded name(s) {hits}")


def load_plugin(cfg):
    """Optional org plugin module (a .py path in config key 'plugin', relative to the config)."""
    p = cfg.get("plugin")
    if not p:
        return None
    path = Path(p).expanduser()
    if not path.is_absolute():
        path = cfg["_config_path"].parent / path
    spec = importlib.util.spec_from_file_location("gp_org_plugin", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def no_formula(v):
    """Data cells never become spreadsheet formulas: a leading '=' (the only prefix openpyxl
    turns into a formula) gets an apostrophe, the usual text marker."""
    return "'" + v if isinstance(v, str) and v.lstrip().startswith("=") else v


def csv_safe(v):
    """For CSVs people open in Excel or Sheets: neutralize =, +, -, @ at the start of text."""
    if not isinstance(v, str) or not v:
        return v
    risky = v[:1] in "\t\r" or v.lstrip()[:1] in ("=", "+", "-", "@")
    return "'" + v if risky and not re.fullmatch(r"-?[\d.,$]+", v) else v
