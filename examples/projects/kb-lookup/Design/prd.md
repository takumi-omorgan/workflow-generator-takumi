# kb-lookup — PRD

**Last updated:** 2026-02-03

## Problem

I jump between VS Code, Slack, and a browser all day and can never
remember the less-common keyboard shortcuts. The existing options are
all bad in the same way: either a shortcut cheatsheet PDF I have to
hunt for, or a Google search that loads a page full of ads. I want to
stay on the keyboard and get an answer in under a second.

## Goals

- One command: `kb <app> <action>` prints the shortcut for that action.
- Works offline. No network calls, ever.
- Ships with shortcuts for three apps: VS Code, Slack, and Chrome.
- Installs via a single `pip install` (or equivalent) with no config.

## Non-goals

- No GUI. This is a terminal tool.
- No fuzzy matching across apps. You must name the app.
- No user-contributed shortcuts. Data is bundled.
- No support for customised/rebound shortcuts. We show defaults only.

## Target user

A solo developer who lives in the terminal and prefers keyboard
navigation over a mouse. Comfortable with `pip install`.

## Success criteria

- A new user can install and run a lookup in under 60 seconds.
- The common case — "I forgot the shortcut for X in Slack" — is served
  in one command, without scrolling.
- The tool works on macOS and Linux. Windows is best-effort.

## Constraints and preferences

- Python 3.10+ so we can use modern argparse features.
- Bundled shortcut data ships in the package so offline works from day one.
- Platform-aware output: on macOS show ⌘/⌥/⇧, on Linux/Windows show Ctrl/Alt/Shift.
