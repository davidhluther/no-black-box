# Team notes for publish

The publish skill's rules stand: one post per change, an exact-words approval, a dry run first, and proof that the live page shows the post's own title. These notes cover running it across several sites and people.

## One site file per site

Keep each site's settings in its own file under `sites/`, named for the site. Never copy another site's file and forget to change `origin`, the repository, or the branch prefix. After adding a site, run the one-line config check in the skill and confirm the new site's id is in the list it prints.

## Who types the approval

Name one publisher per site and one backup, and write both in the team's owner table. Only that person says `merge 12` for pull request 12. The editor can say a draft is ready; they can't approve a merge. If the publisher and the editor are the same person on a small team, say that on purpose in the owner table.

## Start with authority off

Keep `authority` at `none` for a new site until the team has opened one pull request per post for several posts and reviewed each on a phone. Then switch to `merge_n`. For a CMS site, don't skip levels: manual paste, then dry run plus manual, then draft creation, and full publish only with a written approval rule.

## Never from a schedule

A scheduled job never merges or publishes. The job log can run checks and audits on a schedule, and the publisher does the rest by hand.

## When the result isn't "published"

Treat deploy_unconfirmed, live_check_failed, and merge_uncertain as not published. Re-read the pull request's state or the CMS entry before doing anything else, never retry a merge blindly, and record what happened, who looked, and when.
