# Team notes for draft-queue

The draft-queue skill is written for one operator at a time. These notes add what a team needs around it. Nothing here changes the skill's hard rules: it never publishes, it runs only with a person present, and one item goes all the way through before the next starts.

## One owner per item

Add four columns to the right of the queue's existing columns: `owner`, `site`, `market`, and `content_type`. Use `new post` or `refresh` for the content type, because the skill routes on it and skips an item whose type is empty or unrecognized.

Claim an item before you start. Write your name in `owner` and move the stage to In production in the same edit. If the owner column is filled and isn't you, skip the item. Two people drafting the same Planned item is the most common team failure, and it costs a day of work to undo.

## One operator per queue

Only one person runs draft-queue against a given queue at a time. If your queue is shared, say in the team channel when you start and when you finish. When you name specific items, the skill still runs them one at a time.

## Many sites and markets

Run the skill once per site config, passing that site's config file. Give each site its own queue export, its own briefs folder, and its own style guide. Don't mix markets in one queue unless the owner and market columns are filled for every row, because the skill's metadata step takes values from the site's allowed list.

## The handoff note is the gate

The skill refuses to start when the handoff note is missing, unreadable, over three weeks old, or BLOCKED. On a team that usually means a scheduled job missed. Run the job log check first, fix the missed job, rerun content-handoff, and start again. Never edit a note's verdict to get past the gate.

## Record failures

Every run ends with a table of exceptions. Copy it into the team's ops notes with the date and the operator's name. An item left In production with a reason is honest state; a quiet zero is not.
