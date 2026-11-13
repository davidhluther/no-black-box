# AS-FU-03: Your First Run and the Check-Up

Time about 20 minutes. You'll make one ad, one set of posts and one picture, then run the check-up command.

1. **AS-FU-03-1.** Ask [Claude Code](../glossary.md#claude-code) "Use ad-copy to write three test versions of an ad for [offer], and log them." Check the character counts in the platform's own ad screen.
   You'll know it worked when each version differs in one thing, and a claims list sits beside it (E03, E14).
2. **AS-FU-03-2.** Ask "Use social-posts to adapt this idea for X, Facebook and Instagram: [idea]." Read each post aloud.
   You'll know it worked when the three posts sound different, not shortened copies of each other.
3. **AS-FU-03-3.** Ask "Use ad-visuals to make a picture for the Instagram post, shape 4:5." It tries [Canva](../glossary.md#canva) first, then an [image service](../glossary.md#image-service) if your key is set, and otherwise writes a [designer brief](../glossary.md#designer-brief).
   You'll know it worked when you get a picture or a brief file. If a key problem shows up, it's E06 or E07. If text in the picture is garbled, it's E08.
4. **AS-FU-03-4.** Run the check-up by typing `python3 support/doctor.py ad-and-social` in your terminal (a window where you type commands). Copy the support code it prints.
   You'll know it worked when it prints a code and says what it checked. If it can't find python3, it's E16.
5. **AS-FU-03-5.** Check every claim and every picture against the [claims checklist](../free/claims-checklist.md), then post through each platform's own screens.
   You'll know it worked when nothing is published that you can't prove.

> **How to get help.** Write down the step ID where you got stuck (it looks like AS-FU-03-4). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
