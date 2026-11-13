# IP-FU-03: Ideas to Brief

You will run the first half of the flow: gather ideas, screen them, and produce a complete brief. Each command is exact. Allow an afternoon the first time.

1. **IP-FU-03-1.** Gather the week's [feed](../glossary.md#feed) items. The simplest way is to say to [Claude Code](../glossary.md#claude-code): "Run the feed fetch from industry-intel for the last seven days." It runs the line below from your content-work folder. The words in angle brackets stand for the folder where the [plugin](../glossary.md#plugin) keeps that [skill](../glossary.md#skill), which Claude Code knows; ask it to tell you if you want to see it.

   ```bash
   python3 <industry-intel folder>/tools/fetch_feeds.py --config config.json --days 7 --out ideas/pasted/raw-bundle.md
   ```

   You'll know it worked when it prints a list of your feeds as ok, empty, or FAILED. A failed feed is E09. A week where every feed says empty may mean a broken schedule or feed, not a quiet week.

2. **IP-FU-03-2.** Open Claude Code and say: "Run industry-intel on ideas/pasted/raw-bundle.md." Read the note it writes in ideas/notes, and open the original source of every item you plan to use.
   You'll know it worked when the note has the key takeaways, a what-to-do table, and a confidence tier for each item.

3. **IP-FU-03-3.** Export your [Queue](../glossary.md#queue) tab to a [CSV](../glossary.md#csv) file named queue-export.csv in the queue folder (File, Download, Comma-separated values). Make a candidates file called ideas.csv with the columns title, [keyword](../glossary.md#keyword), volume, rationale, and id. Then say "Run topic-screen on ideas.csv", which runs the line below.

   ```bash
   python3 <topic-screen folder>/topic_screen.py --candidates ideas.csv --config config.json
   ```

   You'll know it worked when each candidate shows clear or REVIEW. A notice that a source is INCOMPLETE is E17.

4. **IP-FU-03-4.** Say to Claude Code: "Run content-gap using my [Search Console](../glossary.md#search-console) data and the competitors in config.[json](../glossary.md#json)."
   You'll know it worked when a content-gap report appears in the briefs folder with true gaps, opportunity gaps, and defensive positions.

5. **IP-FU-03-5.** For the topic you picked, say: "Run seo-research for <keyword>, then content-brief." If you want a brainstorm with pretend readers, add "and use synthetic-research in brainstorming mode". The brief must carry a verdict and every statistic must name a source you open.
   You'll know it worked when a brief_<keyword>.md file appears in the briefs folder. Open every statistic's source.

6. **IP-FU-03-6.** Check the brief with the gate. Say "Check this brief", which runs the line below.

   ```bash
   python3 <draft-queue folder>/scripts/check_brief.py briefs/brief_<keyword-slug>.md
   ```

   You'll know it worked when it prints "brief complete". A BRIEF PARTIAL message lists what is missing; this is E24.

7. **IP-FU-03-7.** Say: "Run content-handoff." It writes a note that says which inputs are fresh, stale, or missing.
   You'll know it worked when the note's header shows a verdict of CLEAR or DEGRADED. A BLOCKED note lists what to fix first.

Next, [IP-FU-04, draft, check, and images](IP-FU-04-draft-check-and-images.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-FU-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
