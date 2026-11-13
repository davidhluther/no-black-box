# AS-FU-01: Install the Three Skills in Claude Code

Time about 30 minutes. You'll finish with three skills (named instruction sets the [AI model](../glossary.md#ai-model) follows) called ad-copy, social-posts and ad-visuals.

Before you start, work through the shared [Claude install guide](../../../guides/install-claude.md) so [Claude Code](../glossary.md#claude-code) runs on your computer. Claude Code is a program you [control](../glossary.md#control) by typing, instead of clicking.

1. **AS-FU-01-1.** Open Claude Code in the folder where you keep your marketing files. If the install guide's last step worked, this is the same place.
   You'll know it worked when Claude Code shows a prompt waiting for you to type. If the program isn't found, it's E17.
2. **AS-FU-01-2.** Add the kit's collection (the official term is "[marketplace](../glossary.md#marketplace)") by typing the command shown on the repo's front page, then install the Ad and Social kit by name.
   You'll know it worked when asking "Which skills are installed?" lists ad-copy, social-posts and ad-visuals. If one is missing, it's E17.
3. **AS-FU-01-3.** Copy `config.example.json` to a new file named `config.json` in the same folder, and fill in your details. Never put a key in this file.
   You'll know it worked when the file opens as valid text with your organization's name. A typo that breaks the file shows up in step 4 (E19).
4. **AS-FU-01-4.** Ask Claude Code "Use ad-copy to draft search ad text for [offer]." Give it the limits you read from the ad screen.
   You'll know it worked when it answers with counts and a claims list, and asks you for any detail it doesn't have.

> **How to get help.** Write down the step ID where you got stuck (it looks like AS-FU-01-2). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
