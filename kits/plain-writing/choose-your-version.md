# Choose Your Version

Pick the one that matches what you already have today. Moving up later costs nothing, and you keep everything you made in the lower version.

| | Free | Low cost | Full |
|---|---|---|---|
| Code | FR | LC | FU |
| What you need | A Google account and any free AI chat | One paid AI plan, plus Google Docs | A computer, [Python](glossary.md#python), and Claude Code |
| What you do each time | Paste a [prompt](glossary.md#prompt), paste your draft, walk the checklist | Ask the [AI model](glossary.md#ai-model) to use the [skill](glossary.md#skill), or run the word check in your Doc | Run one command on a file, or let it run before you publish |
| [Command line](glossary.md#command-line) needed | No | No | Yes, a little |
| Setup time | About 50 minutes, in four short guides (10, 10, 15 and 15 minutes) | About an hour | About two hours |
| Banned-word check | The AI model checks it from the prompt | The AI model plus a button in your Google Doc | A program checks every word, every time |
| Same result each time | Mostly | Mostly | Yes, the program doesn't get tired or forget |
| Scores a whole folder of writing | No | No | Yes |
| Blocks a bad draft before it publishes | No | No | Yes |
| Checks the finished website text | No | No | Yes |
| Voices | Short versions in the prompt | Full voices in a skill or [Project](glossary.md#project) | Full voices in a skill |
| Claims review | Paste-in prompt | Skill or Project | Skill, plus a written verdict |
| Where the guides are | `setup/PW-FR-01` to `PW-FR-04` | `setup/PW-LC-01` to `PW-LC-04` | `setup/PW-FU-01` to `PW-FU-05` |

## How to decide

Start with free if you write a few things a month and want to see whether this is for you. The prompts and checklist are the real method. Nothing is held back.

Move to low cost if you already pay for an AI plan, or you're tired of pasting the rules each time. The skill holds the rules, so the AI model has them in every chat.

Move to full if several people write for the same organization, if you publish often, or if you want a program, not a person, to catch the mistakes before anything goes out. This is the version the tools were built for.

## Room to choose inside each version

- Free. Use only the checklist, only the prompt, or both. A one-person shop may never need more.
- Low cost. Use the Google Docs word check without uploading a skill, or the skill without the word check. They don't depend on each other.
- Full. Run only article-check, or add the others one at a time. Each skill works alone.

## Switching later

- Free to low cost. Keep your [house style](glossary.md#house-style) and checklist. [Upload](glossary.md#upload) the skills (guide `PW-LC-01`) and move your prompt into a Project (guide `PW-LC-02`).
- Low cost to full. Keep everything. Install Python and the programs (guides `PW-FU-01` and `PW-FU-02`). Your house style file works as is.
- Full to a lower version. Nothing breaks. The prompts and checklist in `free/` are always there.

Your organization's details live in one file, `config.example.json`, which you copy to `config.json`. Every version reads from it, so switching doesn't mean retyping.
