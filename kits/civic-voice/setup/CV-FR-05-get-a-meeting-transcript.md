# CV-FR-05: Get a Meeting Transcript

Free version, guide 5. You will turn a public meeting video into a searchable, timestamped [transcript](../glossary.md#transcript) using the video site's own transcript panel and a free [AI model](../glossary.md#ai-model). Plan about 30 minutes for a two-hour meeting. A transcript made this way is machine-made and unofficial. The official record is the [adopted minutes](../glossary.md#adopted-minutes).

1. **CV-FR-05-1.** Find the video on the body's own website or video channel. Open your tracker's Transcripts tab and add a row with the meeting date, the body, and the video link. Save the meeting's agenda too, since it spells names correctly.
   You'll know it worked when the row has a link that opens the video.

2. **CV-FR-05-2.** On YouTube, open the description under the video (click "...more"), and look for "Show transcript." Click it. A panel with lines of text and times opens beside or under the video. If there is a way to turn timestamps on, turn them on.
   You'll know it worked when you see a scrolling list of timestamps with text. If there is no transcript button, the video has no [captions](../glossary.md#captions), and it's E13. Other video sites may show a similar "transcript" or "CC" menu.

3. **CV-FR-05-3.** Click inside the panel, select all the text (Command and A on a Mac, Control and A on Windows), copy it, and paste it into a Google Doc named "raw transcript yyyy-mm-dd."
   You'll know it worked when the Doc holds pairs of times and lines of text. If only part came across, scroll the panel to the bottom first and try again.

4. **CV-FR-05-4.** Open `free/prompts.md`. Copy the "Rules block" and [prompt](../glossary.md#prompt) 7 ("Clean a pasted transcript"). Paste both into a free AI model, paste the agenda, then paste the raw transcript. For a long meeting, send it in pieces of about 20 to 30 minutes, and tell the model which part number it is. Copy the result into a new Google Doc.
   You'll know it worked when the result keeps timestamps, has short paragraphs, marks "[unclear]" where it could not tell, lists any name fixes at the end, and begins with the notice that it is machine-made. If the model changed words or named speakers it could not know, it's E08, and the fix is to tell it to follow the rules again. If the names are wrong, it's E14.

5. **CV-FR-05-5.** Spot-check. Pick three timestamps, one near the start, one in the middle, and one near the end. Play the video there and compare it with your text.
   You'll know it worked when the words match closely. If they do not, it's E14.

6. **CV-FR-05-6.** Save the cleaned transcript in "Civic voice/Transcripts" named "yyyy-mm-dd-body-transcript." Write your name and today's date at the top as the person who prepared it. Fill in the rest of the Transcripts row.
   You'll know it worked when the file is saved and the row is complete.

7. **CV-FR-05-7.** (Optional.) To get a summary of one agenda item, use prompt 8, paste in just that part of the transcript, and send. Keep each point tied to its [timestamp](../glossary.md#timestamp). Before you quote anyone, play the video at that moment and confirm the words. When adopted minutes are posted, compare any decisions with them.
   You'll know it worked when each summary point has a timestamp and no summary words sit inside quotation marks.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like CV-FR-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
