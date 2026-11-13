"""One registry of every site you publish a blog to.

Each site is one JSON file in the sites folder, named <site_id>.json. It says where the site's posts
live (a git repository or a CMS, which is a content management system such as WordPress or Contentful),
the live address and title shape of a post, how a post goes live, whether the owner's exact "merge N"
may publish it, and which checks apply. Scripts read a Site from here and never hard-code one
organization. Adding a site means adding one JSON file; see sites/example.org.json.

The sites folder is `../sites` next to this file, or the folder named in the PUBLISH_SITES_DIR
environment variable.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = SKILL_ROOT.parent  # the folder that holds every skill of this kit
SITES = Path(os.environ.get("PUBLISH_SITES_DIR") or SKILL_ROOT / "sites")
SITE_ID = re.compile(r"[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*")
REPO = re.compile(r"[A-Za-z0-9-]{1,39}/[A-Za-z0-9._-]{1,100}")
FIELD = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")
TOP = {"schema_version", "site_id", "entity", "origin", "blog", "publish", "checks"}
BLOG = {"source", "post_path", "url", "title_fields", "title_suffixes"}
BLOG_OPTIONAL = {"routes"}
ROUTE = {"field", "contains", "url"}
PUBLISH = {"kind", "authority", "repo", "base", "lane_prefix", "production_environment", "contract", "store"}
KINDS = {"git_pr": "git", "cms": "cms"}


@dataclass(frozen=True)
class Site:
    site_id: str
    entity: str
    origin: str
    blog: dict
    publish: dict
    checks: dict

    @property
    def merge_n(self) -> bool:
        return self.publish["authority"] == "merge_n"

    @property
    def repo(self) -> str:
        return self.publish["repo"]

    def post_pattern(self) -> re.Pattern:
        """Matches a changed file that is a post and captures its slug."""
        head, tail = self.blog["post_path"].split("{slug}")
        return re.compile("^" + re.escape(head) + r"([a-z0-9][a-z0-9-]{0,120})" + re.escape(tail) + "$")

    def post_file(self, slug: str) -> str:
        return self.blog["post_path"].replace("{slug}", slug)

    def url_template(self, frontmatter: dict) -> str:
        """The first route whose frontmatter field holds its value (a list member or the scalar), else url."""
        for route in self.blog.get("routes", []):
            held = frontmatter.get(route["field"])
            held = held if isinstance(held, list) else [held]
            if route["contains"] in [str(v).strip() for v in held if v is not None]:
                return route["url"]
        return self.blog["url"]

    def post_url(self, slug: str, frontmatter: dict) -> str | None:
        """The live URL of a post; None when its URL needs a frontmatter field the post lacks."""
        template = self.url_template(frontmatter)
        values = {"slug": slug}
        for name in FIELD.findall(template):
            if name != "slug":
                value = str(frontmatter.get(name, "")).strip()
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,80}", value):
                    return None
                values[name] = value
        return self.origin + template.format(**values)

    def title(self, frontmatter: dict) -> str | None:
        for name in self.blog["title_fields"]:
            value = str(frontmatter.get(name) or "").strip()
            if value:
                return value
        return None

    def shows_title(self, shown: str, title: str) -> bool:
        return shown in [title] + [title + suffix for suffix in self.blog["title_suffixes"]]

    def check_path(self, name: str) -> Path | None:
        """A path-valued setting in checks (for example brand_rules), or None when unset.
        Values start with @SKILLS/ (inside this kit's skills folder) or @CWD/ (your working folder)."""
        value = self.checks.get(name)
        if not isinstance(value, str) or not value:
            return None
        if value.startswith("@SKILLS/"):
            return SKILLS_DIR / value[len("@SKILLS/"):]
        if value.startswith("@CWD/"):
            return Path.cwd() / value[len("@CWD/"):]
        raise ValueError(f"checks.{name} must start with @SKILLS/ or @CWD/")


def parse_frontmatter(text: str) -> dict:
    """A post's top-level frontmatter: flat key: value scalars, and lists of plain scalar items (`key:` then
    `  - item` lines) such as topics. Nested mappings and folded blocks are skipped."""
    block = re.match(r"---\n(.*?)\n---", text or "", re.S)
    out, listing = {}, None
    for line in (block.group(1) if block else "").splitlines():
        if (m := re.match(r"([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", line)):
            listing = None
            if m.group(2):
                out[m.group(1)] = m.group(2).strip("'\"")
            else:
                listing = m.group(1)
        elif listing and (m := re.match(r"\s+-\s+(.+?)\s*$", line)) and not re.match(r"[A-Za-z_]\w*:\s", m.group(1)):
            out.setdefault(listing, []).append(m.group(1).strip("'\""))
        elif not line.startswith(" "):
            listing = None
    return out


def _strict(raw: str) -> dict:
    def pairs(rows):
        out = {}
        for key, value in rows:
            if key in out:
                raise ValueError("duplicate key in site config")
            out[key] = value
        return out
    return json.loads(raw, object_pairs_hook=pairs)


def _exact_keys(block, keys, name, optional=frozenset()):
    if not isinstance(block, dict) or not keys <= set(block) <= keys | optional:
        raise ValueError(f"site config {name} must have exactly {sorted(keys)}"
                         + (f" (optional {sorted(optional)})" if optional else ""))


def _url_path(url, name):
    if not isinstance(url, str) or not url.startswith("/") or "{slug}" not in url:
        raise ValueError(f"{name} must be a path containing {{slug}}")


def validate(data: dict, site_id: str) -> Site:
    _exact_keys(data, TOP, "top level")
    if data["schema_version"] != 1 or data["site_id"] != site_id or not SITE_ID.fullmatch(site_id):
        raise ValueError("site config id or schema version is wrong")
    origin = data["origin"]
    if not isinstance(origin, str) or not re.fullmatch(r"https://[a-z0-9.-]+\.[a-z]{2,}", origin):
        raise ValueError("site origin must be a bare https origin")
    blog, publish = data["blog"], data["publish"]
    _exact_keys(blog, BLOG, "blog", BLOG_OPTIONAL)
    _exact_keys(publish, PUBLISH, "publish")
    if not isinstance(data["checks"], dict):
        raise ValueError("site checks must be an object")
    kind = publish["kind"]
    if kind not in KINDS or blog["source"] != KINDS[kind]:
        raise ValueError("publish kind and blog source disagree")
    _url_path(blog["url"], "blog url")
    routes = blog.get("routes", [])
    if not isinstance(routes, list):
        raise ValueError("blog routes must be a list")
    for route in routes:
        _exact_keys(route, ROUTE, "blog route")
        if not all(isinstance(route[k], str) and route[k].strip() for k in ("field", "contains")):
            raise ValueError("blog route field and contains must be text")
        _url_path(route["url"], "blog route url")
    if (not isinstance(blog["title_fields"], list) or not blog["title_fields"]
            or not all(isinstance(t, str) and t for t in blog["title_fields"])
            or not isinstance(blog["title_suffixes"], list)
            or not all(isinstance(t, str) for t in blog["title_suffixes"])):
        raise ValueError("blog title fields and suffixes must be lists of text")
    if publish["authority"] not in ("merge_n", "none"):
        raise ValueError("publish authority must be merge_n or none")
    if kind == "git_pr":
        post_path = blog["post_path"]
        if (not isinstance(post_path, str) or post_path.count("{slug}") != 1 or post_path.startswith("/")
                or ".." in post_path.split("/")):
            raise ValueError("git post_path must be a relative path with one {slug}")
        if not REPO.fullmatch(str(publish["repo"])) or not re.fullmatch(r"[a-z][a-z0-9_]*", str(publish["store"])):
            raise ValueError("git publish needs an owner/name repo and a store name")
        prefix = publish["lane_prefix"]
        if not isinstance(prefix, str) or not re.fullmatch(r"[a-z][a-z0-9]*-", prefix):
            raise ValueError("git publish needs a lane prefix like blog-")
        if not publish["base"] or not publish["production_environment"]:
            raise ValueError("git publish needs a base branch and a production environment")
    elif publish["authority"] == "merge_n":
        raise ValueError("merge N applies only to git pull request lanes")
    return Site(site_id, str(data["entity"]), origin, blog, publish, data["checks"])


def load(site_id: str, sites: Path = SITES) -> Site:
    if not isinstance(site_id, str) or not SITE_ID.fullmatch(site_id):
        raise ValueError("unknown site")
    path = sites / f"{site_id}.json"
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"no site config for {site_id}")
    return validate(_strict(path.read_text()), site_id)


def all_sites(sites: Path = SITES) -> list[Site]:
    return [load(p.stem, sites) for p in sorted(sites.glob("*.json"))]


def merge_n_sites(sites: Path = SITES) -> list[Site]:
    return [s for s in all_sites(sites) if s.merge_n]
