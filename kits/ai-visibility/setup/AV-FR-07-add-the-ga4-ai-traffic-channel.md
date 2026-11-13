# AV-FR-07: Add the GA4 AI Traffic Channel

Time, about 20 minutes. Your website analytics can show visits that come from AI products. You will add one rule to [GA4](../glossary.md#ga4) that sorts them into their own line. It needs editor access to your GA4 property. If your website does not use GA4, skip this guide. Nothing else in the kit depends on it.

The recipe, with the full pattern and the reasons behind each step, is in `free/ga4-ai-traffic-channel.md`.

1. **AV-FR-07-1.** Sign in to analytics.google.com. Use the property picker at the top left to open your website's property. Click the gear icon (Admin) at the bottom left.
   You'll know it worked when the Admin page shows your property name. If you only see Reports and no gear icon, or you cannot open Admin, it's E19.

2. **AV-FR-07-2.** Under Data display (some accounts call it Data settings), click [Channel groups](../glossary.md#channel-group). Click Create new [channel group](../glossary.md#channel-group). Name it "Default plus [AI models](../glossary.md#ai-model)".
   You'll know it worked when a list of the default channels appears (Direct, Organic Search, Referral, and others). If the Create button is missing or greyed out, it's E19.

3. **AV-FR-07-3.** Click Add new channel and name it "AI models". Add a condition. Choose Source as the dimension, "matches [regex](../glossary.md#regex)" as the operator, and paste the pattern from `free/ga4-ai-traffic-channel.md`. Click Apply.
   You'll know it worked when the new channel shows its condition in the list. If the pattern is rejected, check that you copied all of it, and it's E19.

4. **AV-FR-07-4.** Drag "AI models" above Referral. GA4 gives each visit to the first rule that matches, from the top, so if Referral is first it keeps these visits. Click Save group.
   You'll know it worked when the list shows AI models above Referral and a message confirms the group saved.

5. **AV-FR-07-5.** Open Reports, Acquisition, Traffic acquisition. Above the table, change "Session primary channel group (Default)" to your new group. Set the dates to the past three months.
   You'll know it worked when the table lists channel names including AI models, even if the number is small or zero. If AI models stays at zero while you are sure someone arrived from an AI product, it's E20.

6. **AV-FR-07-6.** Write down this month's AI models session count in your monthly checklist. Remember that it is a lower bound. Visits where the source name was stripped land in Direct, and people who ask an [AI model](../glossary.md#ai-model) and never click do not show here at all.
   You'll know it worked when you have a number, or "zero", written down with the date.

> **How to get help.** Write down the [step ID](../glossary.md#step-id) where you got stuck (it looks like AV-FR-07-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
