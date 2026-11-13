# Fixes

Find the code in the guide's step (it says "it's E03"), or look up what you see. If none fits, send the step ID and your check-up code to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

| Code | What you see | Why | The fix | Step |
|---|---|---|---|---|
| E01 | You sign in to Google, [Canva](glossary.md#canva) or an [AI model](glossary.md#ai-model) and land back on the sign-in page | The browser blocks the small files sites use to remember you, or you have two accounts open | Open a private window, sign in once there, and allow cookies for that site. Try one account at a time | AS-FR-01-1, AS-FR-02-1, AS-FR-03-1 |
| E02 | The AI model writes a [voice sheet](glossary.md#voice-sheet) or ad without asking you anything, or sounds like every other ad | Your prompt or voice sheet wasn't pasted, or the chat is too long | Start a new chat, paste the voice sheet first, then the prompt. Add "Use my words from the voice sheet" | AS-FR-01-2 |
| E03 | A [headline](glossary.md#headline) or caption is longer than the platform allows | AI models miscount characters | Tell the model which line is over and by how much, and count again in the platform's own box. Its counter is final | AS-FR-01-6, AS-LC-01-5, AS-FU-03-1 |
| E04 | The numbers on the sizes checklist differ from the ad screen | Platforms change limits and show different numbers by ad type | Use what the ad screen shows today and update your checklist | AS-FR-01-6 |
| E05 | A Canva picture is the wrong shape, or no Canva connection appears | The template had a different size, or your plan or vendor doesn't offer the connection | Resize in Canva by the platform's pixel numbers, or work by hand without the connection | AS-FR-03-3, AS-LC-02-1 |
| E06 | The check says an image key is "not set" | The [environment variable](glossary.md#environment-variable) isn't saved, or you opened the [terminal](glossary.md#terminal) before saving it | Close the terminal, open a new one, and set the variable again as the keys guide shows | AS-FU-02-3, AS-FU-03-3 |
| E07 | The [image service](glossary.md#image-service) refuses the request (billing, limit, permission or model name) | No payment method, spending limit reached, or the model name is out of date | Open your account on the vendor's site, fix billing or limits, and copy the current model name into `config.json` | AS-FU-03-3 |
| E08 | A picture has garbled letters, a fake logo or a strange hand | Image services draw text badly and invent details | Make the picture with no text and add words in Canva, or use the [designer brief](glossary.md#designer-brief) | AS-FR-03-8, AS-FU-03-3 |
| E09 | There's no Help menu in your sheet | The script isn't saved, or the sheet wasn't reloaded | Save the script, close the sheet tab and open the sheet again, then wait a few seconds | AS-FR-02-7, AS-LC-03-1 |
| E10 | The check-up says a tab is missing | The tab has a different name | Rename the tab to exactly Voice, [Variants](glossary.md#variant) or Config | AS-FR-02-2, AS-FR-02-3, AS-FR-02-4 |
| E11 | The check-up says headings do not match | A heading was changed, or the paste split wrongly | Paste the matching [CSV](glossary.md#csv) file's first row into row 1 again | AS-FR-02-2, AS-FR-02-3, AS-FR-02-4 |
| E12 | The check-up says settings are not filled in | A required Config row has no value | Fill in column B of each row | AS-FR-02-5 |
| E13 | Google asks for permission or warns the app isn't verified | Scripts you add yourself aren't reviewed by Google | Choose your account, then Advanced, then continue. The script reads only this sheet | AS-FR-02-7 |
| E14 | A claim in an ad has no proof | The model added a flattering claim, or your sheet lacks proof | Remove it, or add the proof (a document, receipt or public page) to the voice sheet | AS-FR-01-4, AS-LC-02-4, AS-FU-03-1 |
| E15 | The chat says your paste or file is too large | Free plans and [Projects](glossary.md#project) limit size | Paste only the voice sheet and the one prompt, or split the file | AS-LC-01-3 |
| E16 | The terminal says it can't find `python3` | Python (a free language the script runs on) isn't installed | Install it from python.org, then open a new terminal | AS-FU-03-4 |
| E17 | [Claude Code](glossary.md#claude-code) or one of the [skills](glossary.md#skill) isn't found | The install didn't finish or the kit wasn't added | Repeat the install guide and the [marketplace](glossary.md#marketplace) step, then restart Claude Code | AS-FU-01-1, AS-FU-01-2 |
| E18 | The Project doesn't remember your voice sheet | The file wasn't uploaded, the plan lacks Projects, or you're chatting outside the Project | Start the chat inside the Project and re-upload the file | AS-LC-01-1, AS-LC-01-4 |
| E19 | A skill says `config.json` is unreadable | A comma or quote is missing | Compare with `config.example.json` and fix, or paste into a [JSON](glossary.md#json) checker (a tool that finds typos in this kind of file) | AS-FU-01-3 |
