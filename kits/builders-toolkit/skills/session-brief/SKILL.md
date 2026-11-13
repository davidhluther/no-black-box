---
name: session-brief
description: Keeps long AI-assisted work from losing its thread. Sets up a short brief file with an unchanging purpose line, a compaction count and a "Settled, never re-ask" section, and gives the rules for one session per task, when and how to compact, and how to hand work to a fresh session. Use at the start of any piece of work that will span more than one sitting, when the conversation is getting long, before a compaction, and when handing work to a new session.
---

# Session brief

Works in: Claude Code (full version). The brief is a plain Markdown file, and the checker needs Python 3. The habits apply in any tool, but the compaction and handoff rules are written for Claude Code.

Settings: if the kit's `config.json` exists, read the `brief` block (brief path and line limit). Otherwise ask the user.

## The problem

A long conversation with an AI model has a memory limit. When the conversation fills the model's context window (the amount of text it can hold in mind at once), Claude Code compacts it: the earlier conversation is replaced with a summary so work can continue. Summaries lose things. Decisions you made an hour ago, warnings you gave, the exact reason a path was rejected. Then the session asks you the same question again, or quietly undoes a choice.

The fix is to keep anything that must survive in a file on disk, because a file does not get summarized. Nothing needed after compaction may exist only in the chat.

## One session per task

Use one session per task or topic. Start it by reading the project's capability ledger, its status file and its latest brief. Durable context belongs in files, not in anyone's memory.

Never reopen a large, idle session and keep going. Start fresh from its handoff. A session built for one high-stakes judgment call closes when that call is made.

## The brief

Copy `assets/BRIEF.template.md` to the project, named `BRIEF-<topic>.md`. Keep exactly one active brief for each session. It opens with three header lines.

```
Purpose: <the original task or topic, one sentence>
Session: <a name or ID that identifies this session>
Compactions: <number of completed compactions in this session>
```

- **Purpose** is written once and never edited. If the work drifts from it, that is a signal to hand off (see below), not to rewrite the line. A purpose that follows the work stops saying what the session was for.
- **Compactions** counts compactions that actually finished, whether you triggered them or Claude Code did. A warning that the window is nearly full is not a compaction. If you know one is coming, note it separately as pending.
- **Session** lets a person, or a script, match this brief to this session. If two briefs claim one session, or none does, you have to resolve that by hand before you can rely on either.

Below the header, keep these sections short.

**Settled, never re-ask.** Decisions the owner has made that must survive compaction and handoff, each with its date and, where it helps, the reason. Standing preferences go here too ("write dates as month/day", "never publish without an explicit yes"). Anything in this section is not reopened without the owner raising it. When a session starts, read this section first. When a decision is made in conversation, write it here the same hour.

**State.** What is done, what is in progress, what is verified and what is not.

**Open items.** What is still to do, in order, with any blocker named exactly (what it waits on, and until when).

**Next step.** The one thing to do first on resume.

**Location.** Where the ledger, status file and any generated files live.

Keep the whole brief short enough to read in one minute. If it is longer, the detail belongs in a separate file the brief points to.

## Compaction routine

When the context warning appears (or the owner asks for compaction):

1. Refresh the brief's State, Settled, Open items and Next step.
2. Update the capability ledger for anything shipped.
3. Save and commit your work safely, so nothing sits only in an uncommitted change.
4. Let compaction run. Then add one to `Compactions`.

After every compaction:

1. First reread the brief and the ledger, before anything else.
2. Trust them over the compaction summary, and say which brief you reread ("Reread BRIEF-site-redesign.md, Compactions: 2").
3. Continue from Next step.

## When to hand off

Hand off to a fresh session when any of these is true:

- The topic has changed from the Purpose.
- The owner asks for a fresh session.
- The third compaction would otherwise occur.

After two completed compactions, the next full-window warning starts a handoff and not another stretch of task work. If a third compaction happens before the handoff, do the handoff immediately afterward, before resuming the task. At that point only handoff work remains in the session.

Why a cap: every compaction loses some detail, so by the third the summary is a summary of summaries. A fresh session reading a good brief is more reliable than a long one reading its own history.

**"Stay in this session" expires.** If the owner says to stay in the session, that holds only until the next compaction. Record its expiry in the brief, and after the compaction mark it expired. It does not renew itself by silence, it does not reset the compaction count, and the cap still applies.

## Handoff protocol

Run it without being asked once handoff is due. Keep every artifact short.

1. Refresh the ledger, the status file and the brief. Commit the handoff state. Leave nothing the successor needs only in chat or in an uncommitted change.
2. Name the successor by taking this session's title, removing any existing ` · vN` suffix, and adding ` · v<N+1>` (the first successor is ` · v2`).
3. Start the successor as a new session. Do not use a background helper as the successor, and do not ask the owner to choose a delivery method first.
4. Give the successor a thin brief: the file paths of the handoff documents, the standing rules (point it at "Settled, never re-ask"), this session's name, and the names of every predecessor that is still open.
5. Tell the successor to archive the predecessors once it is running: "Once in flight, archive <names>, reason: superseded by v<N+1>. If refused because a session is still running, retry each turn, and if still refused at your first report, tell the owner which session to archive."
6. End your last message with the successor's title and where to start it.

The successor verifies current assignments and ownership before acting. A historical "done" note in the brief does not authorize repeating or resuming earlier work.

## Finishing a unit without dropping work

Before ending a turn or a unit of work, check these four things and write the result in the brief.

1. **Reconcile.** Compare what you were assigned with what is done. Look at the latest handoff, any failure that was assigned to you and what peers have said. A pending list may be stale. An approval or merge you already received removes its blocker.
2. **Continue.** Start the highest-priority task that is authorized and runnable, within its scope, in the same turn. Do not invent work to stay busy.
3. **Pass dependencies on.** If a task waits on someone else, give them the exact dependency or the ready file through a channel that exists, then continue with independent work. Do not send the same request twice or send an acknowledgment and nothing else.
4. **Record the stop.** End only when nothing you own is runnable, or a real limit forces a handoff. Write the exact dependency, dated gate, hold or limit, and the next task, in the brief.

An acknowledgment, a queued message or a revised pending list is not proof of progress. Proof is a finished unit followed by the first real work on the next one. None of this creates new permissions, extra loops, duplicate workers or invented scope.

## Checking a brief

```bash
python3 scripts/check_brief.py BRIEF-site-redesign.md
```

Read only. It checks that the file opens with `Purpose:`, `Session:` and `Compactions:`, that `Compactions` is a whole number, that a "Settled, never re-ask" section exists, and warns when the brief is long (over 150 lines by default; `--max-lines` changes it). With `--purpose-was "text"` it confirms the Purpose line is unchanged from the text you recorded elsewhere, which catches drift.
