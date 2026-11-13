# IP-FR-02: Pick Ideas and Topics

You will collect post ideas from sources you choose, decide how far to trust each one, and screen them so you only plan posts worth the time. About 40 minutes the first time, then about 20 minutes a week.

1. **IP-FR-02-1.** Open a free AI model (ChatGPT, Claude, or Gemini) in your browser. Open [prompts.md](../free/prompts.md), copy [prompt](../glossary.md#prompt) 0 (the context block), fill in the brackets from your Setup tab, and paste it as your first message. Save the filled-in version in a Google Doc called "Context block" so you can paste it in each new chat.
   You'll know it worked when the AI model replies "ready". If it ignores your rules in later answers, it's E07.

2. **IP-FR-02-2.** Choose three to five sources of ideas. Good ones are the questions people ask you in person and by email, a local news site, one newsletter in your field, and the searches already listed in [Search Console](../glossary.md#search-console). Write them at the top of the Ideas tab in a note cell or on a sticky list.
   You'll know it worked when you have a written list of sources. Fewer is better than more.

3. **IP-FR-02-3.** (Optional.) To pull in a news site's newest headlines without any script, make a scratch tab named Feeds-scratch and, in cell A1, type `=IMPORTFEED("https://www.example.org/feed.xml", "items title", FALSE, 10)` using the real [feed](../glossary.md#feed) address of a site you chose. A feed (the machine-readable list of a site's newest posts) usually lives at the site's address with /feed or /rss on the end.
   You'll know it worked when ten headlines fill the column. If you see an error or an empty cell, it's E09.

4. **IP-FR-02-4.** Collect this week's items (titles, links, and a sentence each) and paste them into prompt 1. Read what the AI model says is worth a post. Then open the original source for each idea you might use and read it yourself.
   You'll know it worked when each kept idea has a link to the original and a rating of A, B, C, or D. A summary that disagrees with its source is common; write down which is right. If the AI model gives a rating it could not know, it's E08.

5. **IP-FR-02-5.** Add each idea you will keep as a row on the Ideas tab with its source link, rating, and one line on why your readers care. Never use a D-rated fact in a post.
   You'll know it worked when each row has all eight columns filled except status, which says New.

6. **IP-FR-02-6.** Make a list of the posts you already have. Copy the titles from your website's blog page (or from your [sitemap](../glossary.md#sitemap), the list of all pages, usually at your web address followed by /sitemap.xml). Paste the titles into a Google Doc called "Existing and planned posts".
   You'll know it worked when the Doc lists every live post, plus any in your [Queue](../glossary.md#queue).

7. **IP-FR-02-7.** Run prompt 2 with your list of existing posts and your ideas. Add monthly search numbers if you have them from Search Console or [Bing Webmaster Tools](../glossary.md#bing-webmaster-tools). Prompt 3 (content gaps) is optional now.
   You'll know it worked when you have three lists: go, look again, and drop. If the AI model says your message is too long, it's E12.

8. **IP-FR-02-8.** For every "go" idea, add a row to the Queue tab with the title, the keyword (the main search, in a reader's words), the monthly search number if known, and the stage "Screened". For every "look again" idea, write what you must settle first in the notes column.
   You'll know it worked when the Queue tab shows each go idea at stage Screened.

Next, [IP-FR-03, research and brief](IP-FR-03-research-and-brief.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like IP-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
