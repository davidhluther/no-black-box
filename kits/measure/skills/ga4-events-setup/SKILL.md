---
name: ga4-events-setup
description: Plan and add custom Google Analytics 4 events (form submissions, file downloads, phone and email clicks, call-to-action clicks, outbound links) through Google Tag Manager without breaking anything already running, test them in Tag Manager's preview mode before publishing, and build a GA4 channel group that shows AI referral traffic (ChatGPT, Perplexity, Gemini, Claude, Copilot) as its own line. Use when someone says "we aren't tracking leads", "set up GA4 events", "track downloads", "what counts as a conversion", "show me AI traffic", or when event counts look inflated or duplicated.
---

# GA4 events setup

Works in: Claude Code, Claude.ai, ChatGPT for the planning and the guides. The optional helper script `scripts/build_gtm_import.py` needs Claude Code (full version) or any computer with Python 3.

Plain words used below:
- GA4 (Google Analytics 4, Google's free tool that counts visits to a website)
- tag (one tracking instruction, such as "report that a download was clicked")
- Google Tag Manager (a free Google tool for adding and changing tracking on a website without editing the site)
- trigger (the rule that says when a tag fires, such as "when a link ending in .pdf is clicked")
- variable (a named value a tracking rule can use, such as the address of the link that was clicked)
- event (one recorded action, such as a page view, a download click or a form being sent)
- container (the box that holds all of one site's tracking pieces)
- workspace (a draft copy where you make changes before anything goes live)
- data layer (a short list a website keeps in the background to announce things that happened, such as a form being sent)
- parameter (an extra labeled fact attached to an event, such as which file was downloaded)
- key event (an event you count as a goal reached, such as a completed contact form)
- preview mode (the Preview button, which opens your real site with your draft changes loaded for you only)
- publish (making your draft changes live for every visitor)
- regex (short for regular expression, a compact pattern for matching text, like a stencil)
- channel group (a way of sorting visits into labeled buckets such as Organic Search, Direct and Email)
- session (one visit to your site)
- referrer (the address of the page a visitor came from)
- skill (a folder of written instructions an AI tool follows to do one job the same way each time)




This skill helps a person with a website add the few Google Analytics 4 events that answer real questions, and see AI traffic as its own line. It is a method plus a script that writes the setup file. It never logs in to anything for you and never publishes anything.

## Read config first

Read `config.json` (copy of `config.example.json`) for the site address, the GA4 measurement ID (looks like `G-XXXXXXX`), the Tag Manager container ID (looks like `GTM-XXXXXXX`) and the list of sister sites. If it is missing, ask for those four things. Never ask for a password.

## The one rule: additive only

Every change adds something new. Nothing existing is edited, renamed, paused or deleted.

1. Give every new item the same prefix, for example `Add |`. A prefix makes new items easy to find and easy to remove as a group.
2. Import with "Merge" and "Rename conflicting tags, triggers, and variables". Never choose "Overwrite".
3. Refer to existing items by name only; do not copy their settings.
4. Do not turn off an older event that counts the same thing. Report both, label which is canonical, and retire the old one only when the owner says so, later, as its own change.
5. Do the work in a new Tag Manager workspace (a separate draft, like a copy of a document you edit before saving over the original).

## Method

### 1. Write the question list before any tag

Ask: what three to six things would you act on if you knew them? Typical answers: which pages produce leads, which downloads get used, who calls or emails, which buttons lead to the contact form, which AI tools send visitors. Write each as "event name | what counts | where it fires | what we will do with it". Use `references/event-plan-template.csv`.

### 2. Define each measure in plain words

State what counts. "A lead is a completed contact or demo form. A newsletter signup, a login and a site search are not leads." Give forms a class: prospect, existing customer, partner, event signup, internal test, other. If one event name already counts the same thing under two names, say so and pick one canonical event.

### 3. Name events the way GA4 expects

Lowercase words with underscores, under 40 characters, no spaces, no personal data in any value (no names, emails or phone numbers). Prefer Google's recommended names where one fits (`generate_lead`, `file_download`). Keep custom names few. Put detail in parameters (extra labeled facts attached to an event), such as `form_id` or `link_url`.

### 4. Build the setup file

Run `scripts/build_gtm_import.py --config config.json --out gtm-import.json`. It writes a Tag Manager import file with new variables, triggers and tags for: form success (from a data layer event your forms already push), file downloads, phone clicks, email clicks, call-to-action clicks and sister-site clicks. Add `--existing container-export.json` to check that no new name collides with an existing one. The script never contacts Google.

### 5. Import into a new workspace

Walk the user through Tag Manager: Admin, Import Container, choose the file, choose a new workspace, choose Merge, choose "Rename conflicting tags, triggers, and variables". The guide for this is in the kit's setup folder.

### 6. Test in preview mode before publishing

Preview mode (Tag Manager's "Preview" button) opens the real site with the draft loaded, only for you. Click through each event yourself and tick it off in `references/preview-test-log.md`. For each event confirm: it fires once, on the right action, with the right parameters, and no personal data. Form events can be tested without creating a real lead only if you push a test message to the data layer; otherwise use a test form or tell the owner a test lead will appear.

### 7. Publish, then watch

Publish only after the test log is complete and the owner says yes. Within a day open GA4 Admin, Events, and confirm the new names appear. Mark only the events that mean "a real person took the step we care about" as key events (GA4's word for conversion). Do not mark scroll, click or page-speed events.

## AI referral traffic channel group

GA4's default channels have no line for AI tools, so visits from ChatGPT or Perplexity hide inside "Referral". A custom channel group (a second way of sorting the same visits into labeled buckets) fixes the reading without changing any data.

1. GA4, Admin, Data display, Channel groups, Create new channel group. Name it "Channels with AI".
2. Add a channel "AI Traffic" with the condition Source matches regex `references/ai-sources-regex.txt` (one line).
3. Copy the default channels in below it, with AI Traffic above Referral so it wins. Channels are checked top to bottom and the first match wins.
4. Save. Channel groups apply to reporting, so past data is re-sorted too (confirm in Google's own help, since the menus change).
5. In reports pick "Channels with AI" in the primary dimension picker.

Report AI Traffic as a floor, never the total. Many AI answers send visitors with no referrer, and an AI Overview click looks like ordinary Google search. Say so in every report that shows it.

## Check your work

- Event count is not a goal. Page-speed beacons and automatic events add up to most of it. Compare pages on sessions, engaged sessions and key events.
- If two key events count the same form fill, report one.
- A tracking change inside a comparison window is never a drop or a gain. Mark the date. See the `metric-check` skill.
- If a number looks wrong, check the test log first, then the data layer, then filters in GA4 (internal traffic, developer traffic).
