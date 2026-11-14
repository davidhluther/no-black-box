# Site config fields

One file per site in `../sites/`, named `<site-id>.json`. The loader (`scripts/site_registry.py`) checks every key and stops on an unknown or missing one, so a typo cannot quietly weaken a safety rule.

```json
{
  "schema_version": 1,
  "site_id": "example.org",
  "entity": "Example Org",
  "origin": "https://example.org",
  "blog": {
    "source": "git",
    "post_path": "content/posts/{slug}.md",
    "url": "/blog/{slug}",
    "routes": [{"field": "topics", "contains": "Guides", "url": "/guides/{slug}"}],
    "title_fields": ["title"],
    "title_suffixes": [" | Example Org"]
  },
  "publish": {
    "kind": "git_pr",
    "authority": "merge_n",
    "repo": "example-org/website",
    "base": "main",
    "lane_prefix": "blog-",
    "production_environment": "Production",
    "contract": "One pull request per post. Merge only on the exact words merge N.",
    "store": "example_merges"
  },
  "checks": {
    "tell_thresholds": null,
    "copy_lint": true,
    "live_title": true,
    "brand_rules": "@SKILLS/article-check/data/brand-rules/example.json"
  }
}
```

## Fields

| Field | Meaning |
|---|---|
| `site_id` | Must equal the file name without `.json`. Lowercase letters, digits, hyphens and dots. |
| `entity` | The organization's display name, used in messages. |
| `origin` | The live site's bare address, `https://` plus the domain, no path. |
| `blog.source` | `git` for a repository, `cms` for a content management system. It must agree with `publish.kind` (`git_pr` goes with `git`, `cms` with `cms`). |
| `blog.post_path` | Where a post file lives in the repository, with exactly one `{slug}`. Not used for a CMS site (set it to `null`). |
| `blog.url` | The live address path with `{slug}`. It may use other frontmatter fields too, such as `/guides/{category}/{slug}`. Frontmatter is the settings block at the top of a post file. |
| `blog.asset_paths` | Optional. Folders, each ending in `/`, where a post's images and other files may live, such as `public/images/blog/`. "merge N" refuses a pull request that changes any file outside the post path and these folders, or that changes no post. |
| `blog.routes` | Optional. The first route whose frontmatter `field` holds `contains` (a list member such as a topic, or the exact value) wins; otherwise `url` is used. |
| `blog.title_fields` | Frontmatter fields the page title comes from, tried in order. |
| `blog.title_suffixes` | What your site adds after the title in the browser tab, such as ` | Example Org`. The live check accepts the bare title or the title plus any suffix. |
| `publish.authority` | `merge_n` lets the exact words "merge N" publish. `none` refuses. Only git sites may use `merge_n`. |
| `publish.repo` | `owner/name` on GitHub. |
| `publish.base` | The branch posts merge into, usually `main`. |
| `publish.lane_prefix` | The prefix every post branch starts with, ending in a hyphen, such as `blog-`. |
| `publish.production_environment` | The name GitHub shows for your live deployment environment, usually `Production`. |
| `publish.contract` | A sentence on the rule that governs publishing for this site. It is shown when a request is refused. |
| `publish.store` | A short name (lowercase letters, digits and the _ character) for this site's folder of action records. |
| `checks.brand_rules` | The article checker's rules file for this site, written as `@SKILLS/...` or `@CWD/...`. |
| `checks.tell_thresholds` | A gate-thresholds file for `tell-scorer`, or `null`. |
| `checks.copy_lint` | `true` if the built site should pass `copy-lint`. |
| `checks.live_title` | `true` to fetch each post's live page and compare its title. |

Any other keys under `checks` are allowed and are yours to use.

## A CMS site

Set `blog.source` to `cms`, `blog.post_path` to `null`, and `publish.kind` to `cms` with `authority` `none`. The git-only fields (`repo`, `base`, `lane_prefix`, `production_environment`, `store`) stay in the file and are set to `null`. The file then records the site's address, title shape and checks, and the CMS adapter (see `cms-adapter.md`) does the publishing.
