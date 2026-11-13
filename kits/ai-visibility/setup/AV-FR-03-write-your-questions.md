# AV-FR-03: Write Your Questions

Time, about 45 minutes. The Questions tab already holds 28 questions with placeholders. You fill in your details, read every question aloud, then freeze the set. After that you never edit a question.

1. **AV-FR-03-1.** On the Config tab, fill in the rest of column B: `business_type` (what you are, in a customer's words, like "hair salon"), `service` (your most asked-for service, like "balayage color"), `town`, `region` (the county or area around it), `owner_name`, and `competitor_1`.
   You'll know it worked when none of the rows still shows the example text. If the [check-up](../glossary.md#check-up) says E03 afterward, one cell is still empty or still the example.

2. **AV-FR-03-2.** Open the Questions tab. Column E, "question_to_paste", now shows each question with your details filled in. Read all 28 aloud. They should sound like something a real customer would type or say, with lowercase letters and missing apostrophes in places. That is on purpose.
   You'll know it worked when every row in column E reads as a complete question with no curly brackets. If you see `{town}` or a `#` error, it's E04. If the tab does not have 28 rows, it's E05.

3. **AV-FR-03-3.** Check that no question except the brand-check ones names your business. Brand-check questions have group BV in column B. Use Find (Ctrl+F or Cmd+F) to look for your business name and your owner's name. They should appear only in the BV rows. If one appears elsewhere, the question hands the AI your name and spoils that cell. Edit the placeholder text in column D to remove it, then check column E again.
   You'll know it worked when the search finds your name only in the BV rows. If it finds it elsewhere and you cannot see why, it's E06.

4. **AV-FR-03-4.** Freeze the set. This is the point of no return, so read each question once more. If you need to change anything, change it now. Then on the Config tab type `v1` in `question_set_version` and today's date, as mm/dd/yyyy, in `question_set_frozen_on`.
   You'll know it worked when both cells hold values. From now on, never edit column D or column E. If you must retire a question, strike it through, write the date and why in column C, and add a new row with a new code, such as LD-08, and bump the version to v2. A run with a different version cannot be compared with older runs.

5. **AV-FR-03-5.** Run Kit help, Run check-up.
   You'll know it worked when the [support code](../glossary.md#support-code) shows E00, which means no problems found. If another code shows, find it in [fixes.md](../fixes.md).

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FR-03-2). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
