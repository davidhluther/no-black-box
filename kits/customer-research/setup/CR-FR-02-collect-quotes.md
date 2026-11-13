# CR-FR-02: Collect Quotes

You will gather 30 to 50 real customer statements into the Quotes [tab](../glossary.md#tab) of your Sheet. Time: one to two hours spread over a few days. The [prompts](../glossary.md#prompt) (messages you paste into an [AI model](../glossary.md#ai-model)) you use here are in [prompts.md](../free/prompts.md).

1. **CR-FR-02-1.** Open the [Config](../glossary.md#config) [tab](../glossary.md#tab) and fill in the value column: your organization's name, what you offer in one sentence, who you serve, the area you serve, and two to five phrases a customer might type into a search box. Leave max_seed_terms and notify_email alone for now. Each row's note column gives an example.
   You'll know it worked when no value cell for those first five rows is empty. Run Kit help, then "Run [check-up](../glossary.md#check-up)", and look for "Config settings are filled in". If it names blank settings instead, it's E08.

2. **CR-FR-02-2.** Choose three to five places where real people have already described what you do or what you offer. Good places are reviews of your own business on Google Maps or Facebook, reviews of one or two nearby alternatives, one or two public threads on [Reddit](../glossary.md#reddit) (a site of public discussion boards, each called a [subreddit](../glossary.md#subreddit)) or a neighborhood forum, emails or notes customers sent you that you own, and the suggestions a search box offers as you type your own phrases (the suggestion list is called [autocomplete](../glossary.md#autocomplete)). For each one, add a row to the Sources tab with an ID such as S01, the type, the page name, and the link.
   You'll know it worked when the Sources tab has at least three rows. If a page will not load or demands a sign-in, it's E16, so pick another source instead.

3. **CR-FR-02-3.** Open one source, select a screenful of comments, copy them, and remove any names or usernames. Paste prompt P1 from [prompts.md](../free/prompts.md) into a free AI model (a program such as ChatGPT, Claude, or Gemini), put the copied comments between START and END, and send. Read the table it returns.
   You'll know it worked when you get a table of quotes with the columns named in the prompt. If the AI model stops mid-table, send fewer comments, which is E15. If a quote is not word for word in what you pasted, tell the model "that quote is not in the text, remove it," which is E14.

4. **CR-FR-02-4.** Check three quotes by hand. For each of three rows, find the exact words in the page you copied. Delete any row that does not match.
   You'll know it worked when all remaining checked quotes appear word for word in the original. Anything else is E14.

5. **CR-FR-02-5.** Copy the table into the Quotes tab, starting under the heading row. Give every row a quote_id (Q001, Q002, and so on), today's date in date_collected, and the source_id from your Sources tab. Put the date as mm/dd/yyyy. Type the number of comments you read into the how_many_read column of the Sources tab.
   You'll know it worked when every row has an ID and a source. The Quotes headings must stay exactly as they are, or the check-up reports E03.

6. **CR-FR-02-6.** Repeat steps 3 through 5 for each source until the Quotes tab holds 30 to 50 rows from at least three different sources. In the Sources tab, mark whichever source gave the most rows.
   You'll know it worked when no single source supplies more than half the quotes. A single source can reflect one loud person rather than a pattern, so add another source if you are over half.

7. **CR-FR-02-7.** Talk to two or three real customers for five minutes each, with permission. Ask "What made you decide to come to us?" and "What almost stopped you?" Jot their exact words (or record with permission), and add them to the Quotes tab with the source type "conversation".
   You'll know it worked when you have at least two quotes from people you spoke to. Their words are the most valuable rows in the sheet, because they are not filtered by what people bother to post online.

When you have 30 or more quotes, go on to [CR-FR-03](CR-FR-03-find-themes.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like CR-FR-01-3). If your kit has a check-up button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
