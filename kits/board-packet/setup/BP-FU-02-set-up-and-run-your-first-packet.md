# Set Up and Run Your First Packet

This guide takes about 30 minutes. It assumes guide BP-FU-01 is finished and the Drive folder layout from BP-FR-01 exists.

Each step has an ID. If you get stuck, note the ID. Once the [check-up](../glossary.md#check-up) from guide BP-FR-04 is installed (the full version uses a command named `doctor` instead), it prints a [support code](../glossary.md#support-code) you can send along with the ID.

1. **BP-FU-02-1.** Make your settings file. In the kit folder, copy `config.example.json` to a new file named `config.json`, and open it in any text editor (TextEdit on a Mac in plain text mode, Notepad on Windows). The file is written in [JSON](../glossary.md#json), a plain-text list of settings. Change only the words inside the quotation marks. Fill in your organization, people, meeting details, folder names, report list, and email recipients. Leave `draft_only` set to `true`.
   You'll know it worked when the file still looks like the example, with your words in place of the examples. If a later step says the file cannot be read, a quotation mark or comma is missing. Compare with the example, or paste the file into any AI chat and ask it to find the typo (E46).

2. **BP-FU-02-2.** Let the tool reach your Drive files. Install Google's [Drive for desktop](../glossary.md#drive-for-desktop) app, which makes your Drive show up as an ordinary folder on your computer (find "Drive for desktop" on Google's help site). Sign in with your organization's account and pick the `Board Secretary Files` folder to keep in step.
   You'll know it worked when the month folders show up in Finder or File Explorer. Put your `folders.local_workspace` setting at the matching path.
   If you prefer, add Google Drive and Gmail [connectors](../glossary.md#connector) in [Claude Code](../glossary.md#claude-code)'s settings instead (the shared guide install-claude.md shows where). A connector lets the tool read and write on your behalf, and you can switch it off at any time. Allow only drafts for Gmail. If the only Gmail tool offered can also send, skip it and use the file route in the next step.

3. **BP-FU-02-3.** Practice first. Make a folder called `practice` with the invented sample [transcript](../glossary.md#transcript) from [sample-transcript.md](../free/sample-transcript.md) saved as `2027-01-21_board_meeting_transcript.txt` and two or three made-up report files. Open Claude Code in the kit folder and type: "Run the practice board packet using the files in the practice folder. Do not upload or email anything."
   You'll know it worked when the tool reports the missing reports, writes minutes that match the practice meeting, and builds a combined PDF. If it asks permission before each file it writes, say yes to the ones in the practice folder.

4. **BP-FU-02-4.** Run a real month. Open Claude Code in the kit folder and type "run the February board packet", using your own month. The tool follows the steps in the board-packet [skill](../glossary.md#skill). It will say which route it is using, tell you before it puts any file in a shared folder, and wait for a yes.
   You'll know it worked when it hands back a list of what was gathered, what is missing, where the packet and minutes live, and a note that the email draft is ready for review.

5. **BP-FU-02-5.** Check the draft yourself. Open Gmail, click **Drafts**, and read it. Open every link in a private browser window. Ask your reviewer to read it. Send it only after they approve.
   You'll know it worked when the email is in Drafts and has not been sent. If there is no draft, the tool should have saved `email-draft.html` and `email-draft.txt` in the month folder instead. Paste from those (E44).

> **How to get help.** Write down the step ID where you got stuck (it looks like BP-FU-02-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
