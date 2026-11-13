# Install the Tools

This guide takes about 30 minutes. It is for the full version, where an AI tool runs the whole monthly cycle for you. Free and low-cost setup are not required first, but the folder layout from guide BP-FR-01 is, because the skills expect it.

Each step has an ID. If you get stuck, note the ID. Once the [check-up](../glossary.md#check-up) from guide BP-FR-04 is installed (the full version uses a command named `doctor` instead), it prints a [support code](../glossary.md#support-code) you can send along with the ID.

The full version runs on a computer you control, using [Claude Code](../glossary.md#claude-code), a program that lets the Claude [AI model](../glossary.md#ai-model) read and change files in a folder you pick. It needs the [command line](../glossary.md#command-line), meaning you type a few short instructions into a window called the [terminal](../glossary.md#terminal). You only type the ones shown here, and each is a copy and paste. If that sounds like too much, the low-cost version gets you most of the way with menus only.

The five [skills](../glossary.md#skill) in this kit (small instruction folders the AI tool follows) are board-packet, meeting-minutes, packet-pdf, transcribe, and meeting-digest. Their start-of-file notes say they work in Claude Code. The meeting-digest skill also works in Claude.ai and ChatGPT.

1. **BP-FU-01-1.** Install Claude Code and add this kit by following the shared guide [install-claude.md](../../../guides/install-claude.md). It needs a paid Claude plan or a pay-as-you-go account. See [keys-and-accounts.md](../../../guides/keys-and-accounts.md) for where to sign up and what it costs.
   You'll know it worked when you can open a terminal, type `claude`, and get a welcome screen. If the guide's steps fail, tell the person helping you which step ID you reached.

2. **BP-FU-01-2.** Install [LibreOffice](../glossary.md#libreoffice) (a free office program). Download it from libreoffice.org and drag it to your Applications folder, or run the installer on Windows. The kit uses it in the background to turn Word and Excel files into PDFs.
   You'll know it worked when you can open the LibreOffice app once and close it. If the later PDF step says LibreOffice was not found, it's E30.

3. **BP-FU-01-3.** Install the two Python add-ons. Open the terminal and paste this line, then press Enter.
   ```
   pip install pypdf python-docx
   ```
   [pypdf](../glossary.md#pypdf) joins PDFs, and python-docx makes Word files. If your computer says `pip` is not found, try `pip3` in its place.
   You'll know it worked when the last line says "Successfully installed". If it says the command is not found, you need Python first. Ask for help with this step ID.

4. **BP-FU-01-4.** Install [Whisper](../glossary.md#whisper) and ffmpeg. Whisper turns a recording into text on your own computer. ffmpeg is a free helper that reads audio and video files. You only need this if you record meetings and have no [transcript](../glossary.md#transcript). On a Mac, if you have Homebrew (a free installer for Mac programs), paste these two lines. Otherwise follow the install pages at ffmpeg.org and the Whisper project page on GitHub.
   ```
   brew install ffmpeg
   pip install openai-whisper
   ```
   You'll know it worked when `whisper --help` prints a list of options. If it says command not found, close and reopen the terminal and try again (E37, E38).

5. **BP-FU-01-5.** Run the kit's own check. In the terminal, move into the kit folder as the shared guide shows, then paste:
   ```
   python3 support/doctor.py board-packet
   ```
   You'll know it worked when it prints a [support code](../glossary.md#support-code) such as `BP-FU-00-0-E00-v0.1.0-7KQ`. If it prints anything else, the report lists what to fix. Keep the code if you ask for help.

> **How to get help.** Write down the step ID where you got stuck (it looks like BP-FU-01-3). If your kit has a check-up button or command, run it and copy the support code it prints. Then send both to Pigasus Group at https://pigasus.group/contact. Setup questions are free.
