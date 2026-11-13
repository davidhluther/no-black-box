# BK-FU-01: Create Your Intuit Developer Account and App

You will end with a free developer account at Intuit and one [developer app](../glossary.md#developer-app) (a free entry that stands for your own small program and gives you the keys it needs to sign in to your books). About 30 minutes. This is the slow part of the full version, so take it a step at a time.

Nothing in this guide touches your books, since all that happens is registering a program with Intuit. Everything the program does later is [read-only](../glossary.md#read-only) (able to look but not touch).

## What to expect

Intuit's developer site is built for companies that make software, and its screens and wording change. We could not confirm every field from Intuit's public pages today (checked 11/13/2026), so the steps below describe what to look for, not an exact click path. If a field here is not on your screen, or Intuit asks something this guide does not cover, that is normal. Stop and ask for free help (the box at the bottom).

You need the QuickBooks Online administrator login for the company you want to read.

## Steps

1. **BK-FU-01-1.** Open https://developer.intuit.com and click Sign in or Sign up. You can use the same Intuit login you use for QuickBooks. Use an email address your organization will keep, not one tied to a person who might leave.
   You'll know it worked when you reach a developer dashboard, often called My Hub. If sign-up fails or asks for something unexpected, it's E21.

2. **BK-FU-01-2.** On the dashboard, find the place to create a new app (often a card with a plus sign, or a button named Create an app). Choose the platform "QuickBooks Online and Payments". Give the app a plain name such as "Treasurer books check".
   You'll know it worked when the app appears on your dashboard.

3. **BK-FU-01-3.** When Intuit asks for a [scope](../glossary.md#scope) (the kind of access the app asks for), choose only Accounting, written as com.intuit.quickbooks.accounting. Leave Payments and every other scope unchecked.
   You'll know it worked when exactly one scope is selected. The [script](../glossary.md#script) in this kit uses the accounting scope only to read, and no other scope is needed.

4. **BK-FU-01-4.** Open the app's page and find Keys and credentials (or Keys & OAuth). You will see two [tabs](../glossary.md#tab), Development and Production. Development keys work only with a practice company called a [sandbox](../glossary.md#sandbox) (made-up data that touches nothing real). [Production keys](../glossary.md#production-keys) work with your real company file.
   You'll know it worked when you can see both tabs. You do not need to copy anything yet.

5. **BK-FU-01-5.** Optionally, practice first. Intuit gives every developer account a sandbox company with invented data. Doing the next two guides against the sandbox first costs you nothing and risks nothing. In that case choose the Development tab in the next guide and set QBO_ENV to sandbox in guide BK-FU-03.
   You'll know it worked when you have decided: practice first, or go straight to your real company.

6. **BK-FU-01-6.** Find the [Redirect URIs](../glossary.md#redirect-uri) box on the Development or Production keys page. A [redirect URI](../glossary.md#redirect-uri) is the web address Intuit sends you back to after you approve the sign-in. Intuit's own page requires addresses that start with https for production keys, and does not accept plain local addresses there. So you will use an address on Intuit's own site, which guide BK-FU-02 gives you from the Playground.
   You'll know it worked when you have found the box. Leave it empty for now.

## What to do next

Go to BK-FU-02 to get production keys and a sign-in.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-FU-01-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
> The full version's check-up is a command. Run `python3 support/doctor.py books` and copy the support code it prints.
