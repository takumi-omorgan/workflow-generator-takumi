# kb-lookup — MVP

**Last updated:** 2026-02-05

## Product name

kb-lookup

## One-line description

A terminal command that prints the keyboard shortcut for a named action
in a named app, offline, in under a second.

## Product goal

Ship a single `kb` command that answers *"what's the shortcut for X in
Y?"* without leaving the keyboard. The MVP succeeds when a user can
install the tool and get a correct shortcut for any bundled app/action
pair in one command.

## Target users

### Primary user

A solo developer on macOS or Linux who works from the terminal and
installs Python tooling via `pip` or `pipx`.

## Core problem

Forgetting keyboard shortcuts pulls users out of the terminal and into
a browser search — breaking flow for a trivial lookup. Existing
cheatsheets are app-specific, paginated, and ad-supported. A local
command that prints one answer is strictly faster.

## Product principles

1. Offline always. If it needs the network, it doesn't belong in this release.
2. One command, one answer. No interactive prompts, no menus.
3. Platform-aware output — show the modifier keys the user sees.
4. Bundled data beats user-supplied data until real users ask for it.

## MVP scope

### In scope

- `kb <app> <action>` command that prints one shortcut to stdout.
- Bundled shortcut data for three apps: VS Code, Slack, Chrome.
- Platform-aware rendering of modifier keys (⌘ on macOS, Ctrl on Linux).
- `kb <app>` with no action prints all shortcuts for that app.
- Clear error message when app or action is unknown.

### Out of scope

- User-contributed or user-edited shortcut data.
- Fuzzy matching across app names.
- A GUI or TUI.
- Remappable shortcuts (we show defaults).
- Any network access.

## Primary outputs

A single Python package published to PyPI, installable via `pip install
kb-lookup`, exposing one `kb` entry point.

## Success criteria

The MVP succeeds if a user can:

1. Install the tool in under 60 seconds from a clean machine with Python.
2. Look up a shortcut for any bundled app/action with one command.
3. See platform-correct modifier keys without extra configuration.

## Deferred to later

- Adding more apps beyond the initial three — defer until real demand.
- User-editable shortcut data — belongs in a future release scoped
  around editing.
- A `--search` flag that greps across apps — useful but not essential.

## Acceptance criteria for this document

This MVP statement is acceptable when it:

- names a clear product and user,
- lists what is in and out of scope without ambiguity,
- and can drive the build-out plan, ADRs, and issue backlog without
  further interpretation.
