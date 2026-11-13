# BK-FU-03: Save the Keys, Run the Self-Test, and Make Your First Check

You will end with the [script](../glossary.md#script) proven safe on your own computer and connected to your books. About 40 minutes. The script cannot change your books, and step BK-FU-03-5 proves it before it ever connects.

A [terminal](../glossary.md#terminal) is a window where you type short text commands instead of clicking. On a Mac it is the Terminal app (press Command and Space, type Terminal, press Return). On Windows it is PowerShell (press the Windows key, type PowerShell, press Return). Every command below sits in its own box, and you paste it, then press Return.

## Steps

1. **BK-FU-03-1.** Check that [Python](../glossary.md#python) (a common programming language the script is written in) is installed. On a Mac paste the first command. On Windows paste the second.

   ```
   python3 --version
   ```

   ```
   python --version
   ```

   You'll know it worked when it prints a version such as "Python 3.11" or higher. If it says "command not found" or a number below 3.9, install Python from https://www.python.org/downloads/ and open a fresh terminal (E35). On Windows, wherever this guide says python3, type python.

2. **BK-FU-03-2.** Make a folder for the script. Put the file `qbo_readonly.py` in it. You will find it in the books-check skill's scripts folder in this kit.

   ```
   mkdir -p ~/Desktop/books-check
   ```

   On Windows, create the folder with File Explorer instead (Desktop, then New folder, named books-check) and copy the file in.
   You'll know it worked when the folder shows the file `qbo_readonly.py`. If a later command says "No such file", it's E40.

3. **BK-FU-03-3.** Save your four values as [environment variables](../glossary.md#environment-variable) (named settings kept on your computer outside any file you share). On a Mac, paste this one line to create a private settings file and open it:

   ```
   mkdir -p ~/.config/books-check && touch ~/.config/books-check/env.sh && chmod 600 ~/.config/books-check/env.sh && open -e ~/.config/books-check/env.sh
   ```

   In the file that opens, type these lines, replacing each value with yours from guide BK-FU-02, keeping the quotation marks. Leave QBO_ENV as production, or write [sandbox](../glossary.md#sandbox) if you practiced. Save and close.

   ```
   export QBO_CLIENT_ID="paste-client-id"
   export QBO_CLIENT_SECRET="paste-client-secret"
   export QBO_REFRESH_TOKEN="paste-refresh-token"
   export QBO_REALM_ID="paste-realm-id"
   export QBO_ENV="production"
   ```

   Then load them into the current window (you do this once per new terminal window):

   ```
   source ~/.config/books-check/env.sh
   ```

   On Windows, open Start, search "Edit environment variables for your account", and add five new user variables with the same five names and your values.
   You'll know it worked when this prints your [company ID](../glossary.md#company-id). If it prints nothing, it's E31.

   ```
   echo $QBO_REALM_ID
   ```

   On Windows use `echo $env:QBO_REALM_ID`.
   Do not put these values in a document you share, and never paste them into a chat.

4. **BK-FU-03-4.** Move into the folder:

   ```
   cd ~/Desktop/books-check
   ```

   You'll know it worked when the terminal [prompt](../glossary.md#prompt) shows "books-check". On Windows, `cd $HOME\Desktop\books-check`.

5. **BK-FU-03-5.** Run the self-test. It does not connect to the internet or to QuickBooks.

   ```
   python3 qbo_readonly.py selftest
   ```

   You'll know it worked when the last line says SELFTEST PASSED. Each earlier line says "ok, blocked" for something that would change your books, such as a POST, a delete, or a query that is not a SELECT, plus a count showing the program has exactly one place that sends anything to the internet. If it says FAILED, stop and do not continue (E37).

6. **BK-FU-03-6.** Make the first connection. This is a [GET request](../glossary.md#get-request) (a message that says "show me this" and nothing more) for your company's basic information.

   ```
   python3 qbo_readonly.py check
   ```

   You'll know it worked when it prints "Connected, [read-only](../glossary.md#read-only)" followed by your company name. If Intuit refuses with 401, it's E32. If you see 403, it's E34.

7. **BK-FU-03-7.** Confirm the newest [refresh token](../glossary.md#refresh-token) was saved. Intuit swaps the refresh token each time it is used, and the script keeps the latest copy in `~/.config/books-check/token.json`, readable only by you.
   You'll know it worked when there is no warning about saving. If you saw "could not save the newest token", it's E33.

## What to do next

Go to BK-FU-04 for the checks themselves.

> **How to get help.** Write down the step ID where you got stuck (it looks like BK-FU-03-3). If your kit has a [check-up](../glossary.md#check-up) button or command, run it and copy the [support code](../glossary.md#support-code) it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
> The full version's check-up is a command. Run `python3 support/doctor.py books` and copy the support code it prints.
