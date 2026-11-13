# What David Built

David Luther built these [skills](glossary.md#skill) while running AI-assisted work for real, and this page tells that story in plain terms for clients and hiring managers.

## The problem

Anyone who runs real work through an AI model for more than a day hits the same walls. The conversation gets too long and the model forgets what was decided. Pages look wrong to a visitor even though every automatic check passed. And a confident "that doesn't exist" turns out to be wrong because nobody had looked in the right place. Then a [scheduled job](glossary.md#scheduled-job) dies quietly and nobody finds out for a week.

David Luther runs a large amount of search, measurement and site work through [Claude Code](glossary.md#claude-code), across many projects at once, including work for his employer Corpay and for small clients. At that scale the walls come up weekly. He needed habits that held up without him watching each session.

## What David built

This is a set of working skills, each born from a specific incident and then written down as a rule so it could not recur.

- **Every project gets a [capability ledger](glossary.md#capability-ledger).** A single file says what the project can do and what proves it. It ended a run of wrong "this doesn't exist" answers, including one involving email that sent but whose records looked fine. David wrote the rule that "not found" is a search result and never a fact, and that the ledger is updated in the same change that ships the capability.
- **The [session brief](glossary.md#session-brief) keeps a purpose line that never changes.** It counts completed [compactions](glossary.md#compaction), keeps a "settled, never re-ask" list that survives every summary, and forces a [handoff](glossary.md#handoff) before the summaries pile up. It came from sessions that kept asking the same questions after a summary dropped the answer.
- **The scheduled-jobs rule.** After a weekly data pull died on a full disk while an older success made it look healthy, David set the rule that a missed [slot](glossary.md#slot) is a failure, every run writes an outcome, retries happen the same day, and the owner hears about it only when it is truly stuck. The kit includes a small working runner for it.
- **Layered [design gate](glossary.md#design-gate).** A page once shipped with every check green and a list of visual defects. David built a browser check that measures what can be measured, then requires a reviewer who did not build the page to judge the rest. He added a fingerprint check after a stale local server nearly handed a broken change a green.
- **Workstream inventory.** A coordinator that undercounted his projects made him unable to tell an omission from a judgment call. The inventory is read fresh from disk each time and compared with the written routing notes.

He also wrote data habits into the jobs skill. Predict then grade means forecasts are published before they are good and scored against what happened. A single capture point means each paid data source is pulled by exactly one script.

## What it changed

Long sessions stopped repeating themselves. Quiet failures became visible the same day, with the evidence attached. Claims about what a project can do began to cite proof. Pages stopped shipping with defects that only a person looking at the layout could see. None of it needed a bigger model or a new product. It needed rules written down and small tools that enforce them.

## Skills it shows

- Running AI-assisted work as an engineering practice, with ledgers, briefs and handoffs in place of hope.
- Turning every incident into a rule and a tool so the same failure cannot recur.
- Reliability for scheduled and automated work, including recording, retrying and escalating.
- Evidence discipline, meaning no claim of absence without the scope searched.
- Front-end quality control that combines automated measurement with an impartial human or agent review.
- Writing technical practice in plain language that a nontechnical owner can follow.

## The point of view

Most of how this kind of work gets done sits in a black box, because the people who learned it sell it back as a service. David's view is that these habits are short and teachable, and that a small organization should get them for free and in full. The kit is that view made concrete. Paid help is for fitting the habits to one team's situation, never for holding steps back.
