---
name: publish
description: Publish a finished, checked blog post to your website through one repeatable path. Reads a site config (one JSON file per site), runs the pre-publish checks, opens each post as its own reviewable change, and after you type the exact words "merge 12" merges that one reviewed version, waits for the live deployment, and proves the live page shows the right title. Also documents the pattern for sites that publish through a CMS (a content management system such as WordPress or Contentful). Use when asked to publish, ship, post or put an article live.
---

# Publish

Works in: Claude Code (full version). It uses the GitHub command-line tool (`gh`, signed in to an account that can merge on your repository) and Python scripts. A site that publishes through a CMS follows the "CMS adapter" pattern in `references/cms-adapter.md` instead.

Publishing is the one step in the whole flow that other people see, so this skill is built around one idea: **a merge or a "200 OK" alone is not publication.** A post counts as published only when the change is merged, the live deployment of that exact merge is confirmed, and the live page shows the post's own title.

## One config file per site

Everything specific to one website lives in `sites/<site-id>.json`, and the shared scripts never name an organization. The worked example is `sites/example.org.json` (a made-up site). Adding a site means adding one file. `references/site-config.md` explains each field.

The fields at a glance:

- `origin`: the live site, such as `https://example.org`.
- `blog`: where posts live (`post_path` such as `content/posts/{slug}.md`), the live address shape (`url` such as `/blog/{slug}`), optional `routes` that send some topics to a different path, optional `asset_paths` (the folders a post's images may live in; "merge N" refuses a pull request that touches anything else), and the page-title shape (`title_fields`, `title_suffixes`).
- `publish`: how a post goes live. `kind` is `git_pr` (a pull request, meaning a proposed change that waits for review) or `cms`. `authority` is `merge_n` (the exact words "merge N" may publish) or `none`. Git sites also name the repository, the base branch, a branch prefix for post changes, and the deployment environment to confirm.
- `checks`: which shared checks apply. `brand_rules` points the article checker at this site's rules (`@SKILLS/...` means a path inside this kit's skills folder; `@CWD/...` means your working folder). `tell_thresholds` and `copy_lint` point at the other quality gates.

Check that every config loads (it prints the site ids, or says which key is wrong):

```bash
python3 -c "import sys; sys.path.insert(0,'scripts'); import site_registry as r; print([s.site_id for s in r.all_sites()])"
```

## The flow, step by step

1. **Pre-publish checks.** On the final article, run the `article-check` skill with `--site <id>` and require zero errors. Then run the `tell-scorer` gate if the site names thresholds, and `copy-lint` if the site sets `copy_lint: true`.
2. **Images.** Every post needs its hero image. If the site sets content gates, make sure each one passes.
3. **One change per post.** Put each post on its own branch, named with the site's prefix (for example `blog-my-topic`), and open one pull request for it. Never bundle two posts in one pull request: "merge N" publishes exactly one thing.
4. **Review.** Look at the preview deployment on your phone and check the title, the images, the links, and the page's address.
5. **Approve.** When you are happy, say the exact words `merge 12` (the number of that pull request). Only those words count. "Looks good" does not.
6. **Bind the approval.** This records which pull request you approved, when, and the exact version you were looking at. Pass `--head` with the commit id shown on the preview or the pull request (the head SHA, a fingerprint of the last saved change; use the full 40 characters, shown on the pull request's Commits tab or by `gh pr view 12 --json headRefOid`; a short prefix can be forged). If anyone pushed after your review, bind refuses and you review again:

   ```bash
   python3 scripts/publish_merge.py bind --site example.org --authority "merge 12" --approval-id 2026-11-13-a --head 3f9c2a1e5b7d4c6a8f0e2b4d6c8a0f1e3b5d7c9a
   ```

7. **Check, then merge.** Without `--yes` the script only reports whether the merge would go ahead:

   ```bash
   python3 scripts/publish_merge.py run --site example.org --approval-id 2026-11-13-a
   python3 scripts/publish_merge.py run --site example.org --approval-id 2026-11-13-a --yes
   ```

8. **Read the result.** `published` means the merge landed, the Production deployment of that merge is confirmed, and every post address returned 200 with its own title. Anything else (`deploy_unconfirmed`, `live_check_failed`, `merge_uncertain`) is not publication, and the script says why.
9. **Follow up.** Record the live addresses, update your content tracker, and remove the post's branch.

## Safety rules the script enforces

- The site must have `authority: merge_n`. Every other site is refused before any call to GitHub.
- The pull request must be open, not a draft, on the site's branch prefix, into the site's base branch, from the same repository, with at least one check and every check finished and passing.
- If the pull request changed after you approved it, nothing merges. You review the new version and approve again.
- Your approval must come after the change first appeared on GitHub, which a commit's own date cannot fake.
- The merge is `gh pr merge --squash --match-head-commit <sha>`, so GitHub itself refuses a different version.
- One record per site and pull request prevents a repeated message or a retry from merging twice. An uncertain merge is re-read from GitHub and never retried blindly.
- Nothing merges without `--yes`.

Records live in `./.publish-store` (or the folder in `PUBLISH_STORE_DIR`).

## Adding a site

1. Copy `sites/example.org.json` to `sites/<your-site>.json` and fill in your values. Keep `authority` at `none` until your repository has a one-pull-request-per-post habit and you are ready to use "merge N".
2. Confirm it loads with the one-line Python check above.
3. Copy `../article-check/data/brand-rules/example.json`, edit it, and point `checks.brand_rules` at it.

## CMS sites

If your posts live in a CMS rather than a git repository, read `references/cms-adapter.md`. The checks and the "prove it is live" step stay the same. Only the way a post reaches the CMS changes.
