# Fixes

Find the code the [check-up](glossary.md#check-up) or a guide gave you, read what you see, and follow the fix. If it is still stuck, send the [support code](glossary.md#support-code) and the step ID to Pigasus Group at https://pigasus.group/contact. Setup questions are free.

| Code | What you see | Why | The fix | Step |
|---|---|---|---|---|
| E01 | The check-up says the Settings tab is missing | The tab was not imported, or it has another name | Import `Settings.csv` again and name the tab exactly `Settings` | BP-FR-02-2 |
| E02 | The Reports tab is missing | Same as E01 | Import `Reports.csv`, name the tab `Reports` | BP-FR-02-3 |
| E03 | The Contacts tab is missing | Same as E01 | Import `Contacts.csv`, name the tab `Contacts` | BP-FR-02-4 |
| E04 | The Month tab is missing | Same as E01 | Import `Month.csv`, name the tab `Month` | BP-FR-02-5 |
| E05 | Settings headings are off, or everything sits in one column | A heading was retyped, or the import used the wrong separator | Row 1 must read Setting, Value, Notes. Re-import and choose Comma as the separator | BP-FR-02-2 |
| E06 | Reports headings are off | A heading was changed | Row 1 must read Order, Report, Owner, Role in packet, In combined packet, Filename keyword, Active, Received this month, Link or note | BP-FR-02-3 |
| E07 | Contacts headings are off | A heading was changed | Row 1 must read Name, Email, Group, Role, Active | BP-FR-02-4 |
| E08 | Month headings are off, or the missing_reports_auto cell shows an error | A heading was changed, the Reports tab has another name, or the import did not convert formulas | Row 1 must read Item, Value, Notes. Re-import with "Convert text to numbers, dates, and formulas" ticked. Make sure the other tab is named `Reports` | BP-FR-02-5 |
| E09 | The check-up lists settings that are blank | A required value was left empty | Type a value for each name listed in column B of the Settings tab | BP-FR-02-6 |
| E10 | No report is marked Active | Every Active cell is empty or No | Type Yes under Active for the reports you expect | BP-FR-02-8 |
| E11 | No row has "minutes" under Role in packet | The minutes row was deleted or retyped | Keep one row whose Role in packet reads minutes | BP-FR-02-8 |
| E12 | Two reports share an Order number | A row was copied without changing its number | Give each row its own Order number | BP-FR-02-8 |
| E13 | No active contact is in the To group | The chair row was removed or marked No | Add or fix a row with Group To and Active Yes | BP-FR-02-7 |
| E14 | An email address does not look like an address | A typo, a missing @, or a trailing space | Retype the address | BP-FR-02-7 |
| E15 | The shared packet folder was not found | The folder name in Settings does not match the folder in Drive, or the folder lives in someone else's Drive | Make the name in `root_folder_name` identical to the folder's name, including capitals and spaces | BP-FR-01-2 |
| E16 | No year folder was found inside the packet folder | The year folder is missing, misnamed, or inside another folder | Make a folder named with four digits, such as 2027, directly inside the packet folder | BP-FR-01-3 |
| E17 | The private transcripts folder was not found | The name does not match, or the folder was never made | Make the name in `transcripts_folder_name` identical to the folder's name | BP-FR-01-4 |
| E18 | The private transcripts folder sits inside the shared packet folder | It was made or dragged inside the shared tree, so anyone with the packet link can reach transcripts | Drag it back out to My Drive, beside the packet folder, not inside it | BP-FR-01-4 |
| E19 | The check-up says it could not look at Drive | You have not given permission yet, or you clicked Cancel on the permission screen | Run the check-up again and approve the permission screens | BP-FR-04-4 |
| E20 | A box says to fill in a setting, or the date is missing or not mm/dd/yyyy | `combined_packet_filename`, `root_folder_name`, `meeting_date`, or `month_folder_name` is blank | Fill the named cell and use dates like 01/21/2027 | BP-LC-02-4 |
| E21 | This month's folder was not found | `month_folder_name` does not match any folder in the year folder | Make the name match, or run "1. Make this month's folder" | BP-LC-03-1 |
| E22 | A file shows "Not converted" on the Last run tab | The file is Word, Excel, or another type [Apps Script](glossary.md#apps-script) cannot turn into a PDF | Open it in Drive, choose File then Save as Google Docs (or Sheets), then run "2. Make PDF copies" again. Or save it as a PDF yourself and drop that in | BP-LC-03-5 |
| E23 | "No files to copy were found" | The month folder holds no Docs, Sheets, Slides, or PDFs | Put the reports in the month folder, not in a subfolder | BP-LC-03-5 |
| E24 | The draft step says no active contact is in the To group | Same as E13 | Fix the Contacts tab | BP-LC-03-7 |
| E25 | The draft warns the combined packet was not found | The merged PDF is not in the month folder, or its name differs from `combined_packet_filename` | Save the merged PDF with exactly that name in the month folder | BP-LC-03-7 |
| E26 | Google keeps sending you back to the sign-in page | A cookie problem, or two Google accounts are signed in at once | Open a private browser window, sign in with only the organization's account, and try again | BP-FR-01-1 |
| E27 | A board member can't open a shared link, or "Anyone with the link" is greyed out | The member's email address was not added to the folder, the month folder sits outside the shared folder, or your Google administrator blocked link sharing | Add the address they use for Google under Add people on the packet folder, and test in a private window. If link sharing is greyed out, keep the folder Restricted and add each board member by email | BP-FR-01-5 |
| E28 | No Apps Script item, no Advanced link, or "Authorization required" will not clear | Your administrator switched Apps Script off, or the permission screen was dismissed | Ask your administrator to allow Apps Script, or use a personal Google account for the [tracker sheet](glossary.md#tracker-sheet). On the permission screen click Advanced, then Go to the project | BP-FR-04-4 |
| E29 | The Help or Board packet menu does not appear | The page was not reloaded, the script has an error, or onOpen never ran | Reload the sheet and wait ten seconds. In the editor, choose onOpen and click Run | BP-FR-04-5 |
| E30 | [LibreOffice](glossary.md#libreoffice) was not found | It is not installed, or the packet-pdf script cannot see it | Install LibreOffice, then close and reopen the [terminal](glossary.md#terminal) | BP-FU-01-2 |
| E31 | A file could not be converted | LibreOffice was already open, or the file is damaged | Close LibreOffice and run again. If one file keeps failing, export it to PDF by hand | BP-FU-02-4 |
| E32 | The packet-pdf script says the folder was not found | The path was mistyped | Check the path to the month folder | BP-FU-02-4 |
| E33 | No files to combine | The month folder is empty or holds only unsupported types | Put the reports in the folder | BP-FU-02-4 |
| E34 | Neither [pypdf](glossary.md#pypdf) nor pdfunite is installed | The merge helper is missing | Run `pip install pypdf` | BP-FU-01-3 |
| E35 | The transcribe script says the date is wrong | The date was not written like 2027-01-21 | Use year, month, day with dashes | BP-FU-02-4 |
| E36 | The recording was not found, or the type is not supported | The path is wrong, or the file is not audio or video | Check the path and the file type | BP-FU-02-4 |
| E37 | The [whisper](glossary.md#whisper) command was not found | Whisper is not installed | Run `pip install openai-whisper`, then reopen the terminal | BP-FU-01-4 |
| E38 | ffmpeg was not found | It is not installed | Install ffmpeg, then reopen the terminal | BP-FU-01-4 |
| E39 | A [transcript](glossary.md#transcript) with that name already exists | The recording was transcribed before | Move or rename the old file. The script refuses to overwrite it | BP-FU-02-4 |
| E40 | Whisper finished but no transcript appeared | The recording had no speech, or Whisper stopped early | Listen to the recording, then try the `medium` model | BP-FU-02-4 |
| E41 | The Word-file script says python-docx is missing | The add-on is not installed | Run `pip install python-docx` | BP-FU-01-3 |
| E42 | The [AI model](glossary.md#ai-model)'s minutes have a name, number, or vote that is not in the transcript | AI models sometimes fill gaps with plausible guesses | Run the checking prompt (Prompt 3), read the draft against the transcript, and fix or bracket every difference. Never send unchecked minutes | BP-FR-05-5 |
| E43 | The AI model says the text is too long, or stops partway | The transcript is bigger than the chat can hold | Paste it in smaller parts, about 6,000 words each, and ask for notes before minutes | BP-FR-05-4 |
| E44 | No draft appears in Gmail | The script or tool stopped before the draft step, or you are looking in the wrong account | Look in the account whose sheet you used, check the Drafts folder and the All Mail view, and read any box the step showed. For the full version, look for `email-draft.html` in the month folder | BP-LC-03-8 |
| E45 | There is no Projects option in the AI tool | Your plan or country does not show it, or the page looks different | See the company's pricing page for which plans include Projects. A Custom GPT with the same instructions works as a substitute | BP-LC-01-1 |
| E46 | The full version says the settings file cannot be read | A comma or quotation mark is missing in `config.json` | Compare with `config.example.json`, or paste the file into any AI chat and ask it to find the typo | BP-FU-02-1 |

## Reading a support code

A code such as `BP-FR-02-2-E01-v0.1.0-7KQ` reads in five parts.

- `BP-FR-02-2` is the setup step where the first problem begins: the kit, the version (FR free, LC low cost, FU full), the guide, and the step.
- `E01` is the problem from the table above.
- `v0.1.0` is the kit version.
- `7KQ` is a check value that changes when the list of problems changes.

A code that starts `BP-FR-00-0-E00` means the check-up found nothing wrong.
