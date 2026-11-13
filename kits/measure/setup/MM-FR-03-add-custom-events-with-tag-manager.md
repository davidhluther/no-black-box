# Add Custom Events With Tag Manager (Free, Guide 3)

You will add tracking for things your site's visitors do, such as downloading a file, without touching the site itself and without changing anything that already works. This guide builds one [event](../glossary.md#event) by hand (a file download) so you learn the pattern; every other event repeats it. About 45 minutes.

The one rule is additive only. Every change adds something new, and nothing existing is edited, renamed, paused or deleted. If an old tracking piece looks wrong, leave it and write a note. Retiring it is a separate decision for later.

1. **MM-FR-03-1.** Decide what to track before opening any tool. Open the kit's `free/checklist-events.md` in a Google Doc and write three to six questions you would act on, such as "which downloads get used" or "who calls us". For each, write in one sentence what counts. Use `overrides/ga4-events-setup/references/event-plan-template.csv` as a model.
   You'll know it worked when each question has an event name (lowercase words with underscores, like `content_download`) beside it. If you cannot say what counts, stop here and ask in the free AI prompt 1 in `free/prompts.md`.

2. **MM-FR-03-2.** Open [Google Tag Manager](../glossary.md#google-tag-manager) at tagmanager.google.com and sign in. Click your site's [container](../glossary.md#container) (the box that holds its tracking pieces; its name looks like GTM-XXXXXXX). Check that you can edit and [publish](../glossary.md#publish): you should see a blue "Submit" button at the top right. Write down the live version number shown under "Overview" so you can go back to it.
   You'll know it worked when you see the Overview page with a "Live" version. If you see only "Read" access, ask the account owner for "Publish" access; it's E10. If you cannot find any container, nobody has installed [Tag Manager](../glossary.md#google-tag-manager) on the site yet, and whoever edits your site needs to add Tag Manager's code once.

3. **MM-FR-03-3.** Make a new [workspace](../glossary.md#workspace) (a draft copy). At the top left click "Default Workspace", then the "+" icon, then name it "Add events 11/13/2026" using today's date. Make all your changes here.
   You'll know it worked when the top-left name shows your new workspace and the Overview says "0 changes". If you already see changes in the workspace, you opened somebody else's draft; switch to your own.

4. **MM-FR-03-4.** Turn on the click information Tag Manager can read. Click [Variables](../glossary.md#variable), then "Configure" under Built-In Variables, and tick Click URL, Click Text and Click Element. A [variable](../glossary.md#variable) is a named value (here, the address of the link that was clicked). Then make the [trigger](../glossary.md#trigger) (the rule for when something fires): click Triggers, "New", name it "Add | Link | File download", click the trigger box, choose "Click - Just Links", choose "Some Link Clicks", set the first dropdown to "Click URL", the second to "matches [RegEx](../glossary.md#regex)", and type this pattern, which matches links ending in common file types (a [regex](../glossary.md#regex) is a short text pattern, like a stencil): `\.(pdf|docx?|xlsx?|pptx?|zip)([?#]|$)`. Save.
   You'll know it worked when the trigger appears in the list with the "Add |" prefix. Every new item gets that prefix so you can find and remove them together.

5. **MM-FR-03-5.** Make the [tag](../glossary.md#tag) (the instruction that sends the information). Click Tags, "New", name it "Add | [GA4](../glossary.md#ga4) | content_download", click the tag box and choose "Google Analytics: GA4 Event". Under "Measurement ID" type your GA4 measurement ID, which looks like G-XXXXXXX (find it in GA4: Admin, Data streams, click your stream). Under "Event Name" type `content_download`. Under "Event Parameters" click "Add row" and add `file_url` with the value `{{Click URL}}`. A [parameter](../glossary.md#parameter) is an extra fact attached to the event. Under Triggering choose "Add | Link | File download". Save.
   You'll know it worked when the tag shows your trigger under it in the list. If you cannot find the tag type, Google may have renamed it; search the tag list for "GA4 Event".

6. **MM-FR-03-6.** Test it in [preview mode](../glossary.md#preview-mode). Click "Preview" at the top right. A new window asks for your site's address; type it and click Connect. Your site opens in a new tab with a small "Connected" badge. Click a download link on your site. Switch back to the Tag Assistant window and look at the left list: you should see a "Link Click" entry, and under "Tags Fired" your "Add | GA4 | content_download".
   You'll know it worked when the tag shows under "Tags Fired" once per click. If it shows under "Tags Not Fired", click the entry to see which trigger condition did not match; it's usually the pattern or a missing built-in variable (step 4). If the Connected badge never appears, it's E12.

7. **MM-FR-03-7.** Check that GA4 received it. In GA4 click the gear (Admin), then "DebugView" under "Data display". With preview mode still connected, click the download link again. You should see `content_download` appear within a minute.
   You'll know it worked when the event shows in DebugView with the `file_url` parameter filled in. If DebugView stays empty, it's E13. Do not type any person's name, email address or form answer into any event; keep every value to facts about the page or file.

8. **MM-FR-03-8.** [Publish](../glossary.md#publish) (make live for everyone) only when the owner of the site has said yes. Write the date and what you added in your Doc. Back in Tag Manager click "Submit", give the version a name like "Add content_download 11/13/2026", add a one-line description, and click Publish.
   You'll know it worked when the Overview shows your new version as "Live". If something breaks, open Versions and choose the version you wrote down in step 2, then "Publish". That puts everything back as it was.

9. **MM-FR-03-9.** Confirm it in GA4 the next day, and mark real goals. In GA4 open Admin, then "Events". Within a day `content_download` appears in the list. A [key event](../glossary.md#key-event) is an event you count as a goal reached. For downloads and form submissions that a real person made on purpose, turn on the "Mark as key event" toggle (Google also calls this area "Key events" in Admin). Do not mark scrolls, page-speed measurements or clicks on menus.
   You'll know it worked when the event is listed with a count above zero after a day. If two events count the same thing, report only one of them and note which. If the count looks doubled, it's E14. Write the date you published in your Config tab's notes, because a tracking change inside a comparison period can make a number look like a gain or a drop; guide 5 explains how to handle that.

To add the other events (phone clicks, email clicks, form submissions), repeat steps 4 to 9 changing the pattern. A phone click matches links starting with `tel:`, an email click matches `mailto:`. If you use the full version, the kit builds all of these at once.

Next: [See AI traffic and build a dashboard](MM-FR-04-see-ai-traffic-and-build-a-dashboard.md).

> **How to get help.** Write down the step ID where you got stuck (it looks like MM-FR-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
