# CR-FR-04: Test Your Wording

You will test two or three versions of a headline, sign, or email subject on a simulated panel, then check the best versions with real customers. Time: about 90 minutes plus the real-customer check.

## Read this first: what a simulated panel can tell you

A [simulated respondent](../glossary.md#synthetic-respondent) (an [AI model](../glossary.md#ai-model) answering as if it were a customer) can show where your wording is confusing, cold, or easy to misread. That is useful and cheap. It cannot tell you which version people will act on, how many people will respond, or what customers who never post online would think. Its answers come from text it has read, not from living your customers' week.

A 2025 study (arXiv 2510.08338) compared simulated panels with real survey results for 57 personal-care product concepts. It found that a carefully built simulated panel can rank ideas roughly the way real panels do, but only because the authors had thousands of real answers to check against. Nobody has shown that for a small local organization. Plain asking of an AI model for a score from one to five gives answers that bunch together and do not look like real people's. That is why this guide never asks for scores. In short, the panel has low [validity](../glossary.md#validity) (how far you can trust that a method measures what it claims) for predicting what real people will do, and that is why step 5 exists.

1. **CR-FR-04-1.** Pick one thing to test and write two or three versions. Examples are three names for a service, three versions of a sign, or three email subject lines. Put each in the WordingTests [tab](../glossary.md#tab) with a test_id, a version_label (A, B, C), and the wording.
   You'll know it worked when each version has its own row. If you are tempted to test five versions, cut to three, because more than that is harder to judge.

2. **CR-FR-04-2.** Gather two to four [persona](../glossary.md#persona) cards from [CR-FR-03](CR-FR-03-find-themes.md), step 6. Each must trace to real quotes.
   You'll know it worked when each card's worries point to quote IDs. Without cards built from real quotes, the panel is just an AI model's idea of a customer, so go back and build them first.

3. **CR-FR-04-3.** Paste [prompt](../glossary.md#prompt) P5 from [prompts.md](../free/prompts.md) into a free AI model, with your persona cards and your versions. Read the reactions.
   You'll know it worked when each persona reacts to each version in plain language, flags anything marked GUESS, and the answer says whether the personas agree. If every persona loves every version, or the replies sound alike, it's E17. Run it again and add "be skeptical and tired; you have little time".

4. **CR-FR-04-4.** Record the result in the WordingTests tab: a one-line summary in panel_reaction_summary and the words that caused confusion in confusions_flagged. Circle any version the panel found confusing, because that is the most reliable thing it can tell you.
   You'll know it worked when you can state in one sentence which version looks clearest and which looks riskiest.

5. **CR-FR-04-5.** Check the top two versions with real people. Use prompt P6 to write a three-question script. Ask at least five customers or neighbors. You can ask in person, by text, or with a short Google Forms survey (Google's free survey tool). Offer both versions in random order. Write the answers in the real_customer_result column.
   You'll know it worked when at least five real people have answered. Five is a signal, not proof. If real answers disagree with the panel, the real answers win, every time.

6. **CR-FR-04-6.** Decide, and write the decision and the reason in the decision column. If the real customers split, run a small live test (two versions on two weeks of signs or emails) and keep the winner.
   You'll know it worked when the row shows a decision, who it rests on, and the date.

> **How to get help.** Write down the step ID where you got stuck (it looks like CR-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
