@AGENTS.md

## Code Delivery — Mode Detection

At the start of each conversation, detect which mode you are running in and Read the matching guidance file. Do not load both.

- If you are running as a VSCode extension, you are in **IDE mode** → Read `.claude/instructions/ide-mode.md` and follow its rules.
- If you are running as a CLI tool, you are in **CLI mode** → Read `.claude/instructions/cli-mode.md` and follow its rules.

**How to detect IDE mode** — you are in IDE mode if any of the following are true:
- Your system prompt includes a "VSCode Extension Context" section
- The conversation contains `ide_opened_file` or `ide_selection` tags

If none of the above are present, you are in CLI mode.