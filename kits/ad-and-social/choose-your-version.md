# Choose Your Version

All three versions use the same method. They differ in how much you paste by hand and how much the software does for you. Pick the first column unless you have a reason not to. You can move right any time, and you never lose your [voice sheet](glossary.md#voice-sheet).

| | Free | Low cost | Full |
|---|---|---|---|
| Setup code | AS-FR | AS-LC | AS-FU |
| [AI model](glossary.md#ai-model) | A free chat model (ChatGPT, Claude or Gemini free plan) | One paid plan of about $20 a month, using its [Projects](glossary.md#project) or [Skills](glossary.md#skill) feature | [Claude Code](glossary.md#claude-code) with this kit's three skills |
| Voice sheet | Google Sheet, pasted into each chat | Uploaded once to a Project | Stored in `config.json` and read by the skills |
| Ad copy and [variants](glossary.md#variant) | Paste-in prompt, you copy results to the Variants tab | Same prompt, built in, remembers your voice | Skill writes a variants file for you |
| Social posts | Paste-in prompt per idea | Built in | Skill drafts all platforms in one run |
| Pictures | Free [Canva](glossary.md#canva) by hand, or a [designer brief](glossary.md#designer-brief) | Canva, with the AI plan helping write the prompts | Canva first, then an [image service](glossary.md#image-service) if you add a key, else a designer brief |
| Check-up button | Yes, a Help menu in your Google Sheet | Yes, same sheet | `python3 support/doctor.py ad-and-social` |
| Typical setup time | About 45 minutes | About an hour | About two hours |
| Cost | $0 (see current Canva plans at https://www.canva.com/pricing/) | The AI plan price; see the vendor's page | The AI plan, plus image service use if you choose it |
| What you give up | Some pasting; no memory between chats | Little | Needs a comfortable relationship with typed commands |

Prices change often, so this kit prints none. The [shopping list](shopping-list.md) points to each vendor's own price page.

## How to choose

If you post a few times a month, stay free. The prompts are the same ones the paid versions use.

If you find yourself pasting your voice sheet into every chat, move to low cost. A Project (a saved workspace where the AI model keeps your files and instructions) removes that step.

If you build many campaigns, or want pictures made from a prompt without opening Canva, look at full. It's the only version that can call an image service for you, and it only does so if you put your own key in your own settings.

## Switching later

Free to low cost. Upload your voice sheet and the prompts file to a Project. Nothing else changes.

Low cost to full. Copy your `config.example.json` to `config.json`, fill in the same details, and follow the AS-FU guides.

Going back down is always safe, because every version reads the same voice sheet.

## Room to choose

Each version has places where you decide. Which AI model you use is yours. So is whether to add an image service at all, since Canva or a designer covers most needs. Whether to write ad text and social posts in separate chats is a taste question. Fit matters more than the template, so change the prompts to match how your organization talks.
