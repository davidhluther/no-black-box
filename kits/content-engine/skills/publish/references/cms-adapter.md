# The CMS adapter pattern

Some sites keep posts in a CMS (a content management system, the kind of admin screen where people type and publish pages) instead of in a git repository. WordPress, Contentful, Sanity and Webflow are examples. The checks before publishing and the proof that the page is live work the same way. Only the middle step changes: how the post reaches the CMS.

This page describes the approach, not any one vendor's code. Build your own adapter around your CMS's documented interface.

## What an adapter does

An adapter is a small program (or a careful manual procedure) with five jobs.

1. **Parse the deliverable.** Read the finished article. Its first block is a table of CMS fields (name, page title, permalink, SEO title, SEO description, topic, author, hero image). Everything after the heading is the body. Keep this table in the final markdown file so the article carries its own settings.
2. **Validate against a profile.** Keep a JSON profile of the CMS's content types: each field's name, whether it is required, its allowed values, and which fields to skip. Check every field before sending anything. Refuse on a missing required field or a value not in the allowed list. Put your site's non-negotiable rules here too, such as "every post uses this one country value" or "never publish into this protected section".
3. **Convert the body.** Turn markdown into whatever the CMS stores (rich text JSON, HTML, blocks). Test the converter on a post with a table, a numbered list, bold text inside a bullet and a link, because those are what break.
4. **Create, never auto-publish.** Make the entry in the CMS as a draft or unpublished entry, so a human reviews it in the CMS's own preview. If a post needs several linked entries (a page, its author link and its image), create them as a bundle and roll back every one if any step fails, so a half-made post never lingers.
5. **Ask before every write.** Show a dry run first: the fields that will be sent, the body's size, the images, the links. Make no CMS call until the owner confirms in plain words. Never upload assets without being asked.

## What stays the same as the git path

- Run the `article-check` skill first, with the site's rules.
- Show the draft on a phone for review.
- Prove it is live. Fetch the live address, check for 200, and check that the page title matches the post's title. Draft status, "saved" messages and a 200 on an old page do not count.
- Record what you published, where, and when.

## Choosing the safety level

| Level | How it works | When to choose it |
|---|---|---|
| Manual | A person pastes the article into the CMS. | One post a month. |
| Dry run plus manual | The adapter prints the exact fields and the converted body, and a person pastes them. | Starting out, or a CMS with no good interface. |
| Draft creation | The adapter creates the unpublished entry after a yes. A person presses Publish in the CMS. | Most teams. |
| Full publish | The adapter also publishes. | Only with a written approval rule like "merge N" and a live check that can roll back. |

Start at the first level your CMS allows and move down the table only when the earlier level has run cleanly several times.

## Keys

The adapter needs an API key for your CMS. Keep it in an environment variable, never in the profile file or the article. Create the key with the least access that works (create drafts only, no delete). See the shared guide on keys and accounts.
