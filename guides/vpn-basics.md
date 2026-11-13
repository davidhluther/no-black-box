# VPN Basics

A VPN (virtual private network) is a protected tunnel between your device and another network. Think of an armored car between your front door and the bank, so nobody on the street sees what you carry. Most readers of these kits never need one. This guide is here for two cases, and tells you which one you are in.

Terms are in the [glossary](glossary.md).

## Do you need a VPN?

You need one when you must reach something that only lets people in from inside your organization's network, such as a shared file server at the office, while you are at home. Some small organizations also use one to protect work on public Wi-Fi (the free wireless internet in cafes and hotels).

You don't need one to use any free [kit](glossary.md#kit). Google Sheets, Docs, Claude, and ChatGPT already encrypt (scramble so only the right reader can open) your traffic.

A VPN doesn't make you anonymous, and it doesn't stop a scam email from working. It protects the stretch between your device and the VPN's other end, nothing more.

## Set one up for your organization

Your organization's IT person or provider may already run one. If so, ask them for the app and your sign-in. If nobody does, here is the shape of the job.

1. **NB-FR-04-1.** Decide what you want to reach and from where. Write one sentence, like "From my home laptop to the shared drive at the office."
   You'll know it worked when your sentence names a thing and a place. If you can't name them, you probably don't need a VPN yet.
2. **NB-FR-04-2.** Choose one kind. A business VPN service gives you apps for each device and an admin page. A [router](glossary.md#router)'s built-in VPN (a setting inside your office's internet box) keeps everything in-house. Ask your internet provider or router's maker which one your router supports.
   You'll know it worked when you have picked one and found its instructions page.
3. **NB-FR-04-3.** Install the VPN app on one device and sign in with the account the administrator made for you.
   You'll know it worked when the app shows "Connected." If it shows an error, see E10 in the [shared fixes](getting-help.md#shared-fixes).
4. **NB-FR-04-4.** Test it. With the VPN on, open the thing you need to reach, such as the shared drive.
   You'll know it worked when it opens. Turn the VPN off and try again. It should now fail, which proves the VPN is what lets you in.
5. **NB-FR-04-5.** Add the remaining devices one at a time, testing each, and write down who has access.
   You'll know it worked when your list of people matches who should have access. Remove anyone who leaves the same week.

## Staying safe

Choose a provider whose pricing and ownership you can read on its own website. A free VPN from an unknown maker can read your traffic, so it can be worse than none. Prices change, so see each provider's current plans on its own page.

> **How to get help.** Write down the [step ID](glossary.md#step-id) where you got stuck (it looks like NB-FR-04-3). If your kit has a [check-up](glossary.md#check-up) button or command, run it and copy the [support code](glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
