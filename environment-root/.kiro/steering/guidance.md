---
inclusion: always
---

## Code Delivery — Mode Detection

At the start of each conversation, detect which mode you are running in and read the matching guidance file. Do this before responding to the user for the first time. Do not load both.

- If you are running inside an IDE, read `.kiro/instructions/ide-mode.md` and follow its rules.
- Otherwise, you are in **CLI mode** → read `.kiro/instructions/cli-mode.md` and follow its rules.

