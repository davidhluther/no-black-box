# BK-FU-02: Get Your Keys and Sign In Once

You will end with four values the [script](../glossary.md#script) needs, kept private: a [client ID](../glossary.md#client-id), a [client secret](../glossary.md#client-secret), a [refresh token](../glossary.md#refresh-token), and a [company ID](../glossary.md#company-id). About 45 minutes, plus waiting if Intuit reviews your app. The sign-in happens on Intuit's own website, so your QuickBooks password never goes to this kit or to any program on your computer.

This guide only gets you the keys. Nothing in it changes your books.

Four terms, in plain words. Your app's public label is its [client ID](../glossary.md#client-id), and the private password that goes with it is the [client secret](../glossary.md#client-secret). A [refresh token](../glossary.md#refresh-token) is a long-lived pass that lets the script get a short-lived [access token](../glossary.md#access-token) each time it runs, so you do not sign in again. A [company ID](../glossary.md#company-id) is the number that identifies your company inside QuickBooks.

## Steps

1. **BK-FU-02-1.** Decide whether you are doing the [sandbox](../glossary.md#sandbox) or your real company. If you are practicing, stay on the Development keys [tab](../glossary.md#tab) and skip step 2. If you are going straight to your real books, you need [production keys](../glossary.md#production-keys) (the keys that work on your real company file).
   You'll know it worked when you have written down "sandbox" or "real".

2. **BK-FU-02-2.** For production keys, open your app's page and look for Production settings, Get production keys, or a similar button. Intuit asks for details about the app and for answers to a security questionnaire that its own staff review. It may ask for web addresses such as a privacy policy. Tell the truth: this is a private program that reads one organization's books for its own treasurer, and it stores nothing on a server. If you have no website, ask for help rather than inventing addresses.
   You'll know it worked when Intuit shows your production keys, or says the app is under review. Third-party guides report reviews taking one to two weeks. We have not confirmed that on Intuit's pages, so do not plan a board meeting around it. If the Production tab stays locked, it's E22.

3. **BK-FU-02-3.** Open Intuit's [OAuth Playground](../glossary.md#oauth-playground) from your developer dashboard (it is under the developer tools menu; search "OAuth Playground" at developer.intuit.com if you cannot find it). The [OAuth Playground](../glossary.md#oauth-playground) (Intuit's own page for signing in once and getting the keys a program needs) shows a [Redirect URI](../glossary.md#redirect-uri) near the top. It looks like https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl, but copy yours from the page.
   You'll know it worked when you have the exact redirect address copied.

4. **BK-FU-02-4.** Go back to your app's Keys and credentials page, open the tab (Development or Production) you are using, and add the Playground's redirect address to the Redirect URIs box. Save.
   You'll know it worked when the address appears in the list. If the Playground later says "redirect URI mismatch", it's E23.

5. **BK-FU-02-5.** On the same page, find the Client ID and click the control that shows the Client secret. Copy both into a private note on your own computer (not a shared document, an email, or a chat). Do not take a screenshot.
   You'll know it worked when you have both values saved privately. Treat the client secret like a bank PIN. If it ever lands in a shared place, come back to this page and generate a new one.

6. **BK-FU-02-6.** In the OAuth Playground, choose your app, select the Accounting [scope](../glossary.md#scope) only, and click the button to get an authorization code. A QuickBooks sign-in opens on Intuit's site. Sign in, pick the company, and approve.
   You'll know it worked when the Playground shows an authorization code and a company ID (labeled `Realm ID` on Intuit's page). If your company is not offered, you may be signed in as a user who cannot see it (E24).

7. **BK-FU-02-7.** Click the button to get tokens. Copy the Refresh token and the company ID into your private note. You can ignore the access token, because it expires in about an hour.
   You'll know it worked when you have a long refresh token and a company ID of digits only. Intuit says refresh tokens last about 100 days and that each refresh can issue a newer one. The script saves the newest one for you. If you do not run the script for more than 100 days, repeat this step.

8. **BK-FU-02-8.** Read the screen that lists what you approved. Confirm it says accounting only.
   You'll know it worked when nothing about payments or payroll was granted. If it was, go back to step 6 and untick the extra scopes.

## What to do next

Go to BK-FU-03 to put the values where the script can read them and run the first check.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-FU-02-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
> The full version's check-up is a command. Run `python3 support/doctor.py books` and copy the support code it prints.
