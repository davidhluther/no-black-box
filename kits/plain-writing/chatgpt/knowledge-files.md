# Knowledge Files to Upload

A [knowledge file](../glossary.md#knowledge-file) is a document you give a [Custom GPT](../glossary.md#custom-gpt) or a [Project](../glossary.md#project) so it can read it before answering. The Custom GPT builder accepts up to 20 files. [Upload](../glossary.md#upload) these, in this order of importance.

| # | File from this kit | Why it helps | Required |
|---|---|---|---|
| 1 | `skills/plain-writing/references/styleguide.md` | The full rule set, with the reasoning. The instructions box has the short version. | Yes |
| 2 | Your house style (start from `skills/plain-writing/references/house-style-template.md`) | The rules particular to your organization. | Yes, if you have one |
| 3 | `free/banned-words.csv` | The word list with what to say instead. | Recommended |
| 4 | `free/checklist.md` | The one-page checklist the GPT can walk you through. | Recommended |
| 5 | `skills/voice-presets/references/quick-take.md` | The full Quick Take voice, with an example. | If you use voices |
| 6 | `skills/voice-presets/references/analyst-memo.md` | The full Analyst Memo voice, with an example. | If you use voices |
| 7 | `skills/voice-presets/references/straight-talk.md` | The full Straight Talk voice, with an example. | If you use voices |
| 8 | `skills/evidence-review/SKILL.md` | The method for grading claims and statistics. | If you review claims |
| 9 | `skills/evidence-review/assets/known-bad-claims-template.md`, filled in | Claims your organization has already caught and barred. | Optional |
| 10 | `free/example-draft.md` and `free/example-draft-fixed.md` | A before and after the GPT can learn from. | Optional |

Leave out the [Python](../glossary.md#python) files. A Custom GPT cannot run them from knowledge files. If your plan allows code and file uploads, you can upload `skills/article-check/` and ask the GPT to run it. Whether that works on your plan is not confirmed in this kit, so test it with the example draft before relying on it.

Keep your organization's own documents (donor lists, private notes) out of knowledge files. A Custom GPT you share can expose them.

## If the knowledge files do not load

If the GPT says it cannot see a file, check that the file is under the size limit and is plain text or [markdown](../glossary.md#markdown). Then ask the GPT to quote the first line of the [style guide](../glossary.md#style-guide). If it can, the file loaded.
