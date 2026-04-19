# CLAUDE.md — Kit Repository Rules

This file is the project rules for Claude Code when working **inside the
Claude Code Workflow Kit repository itself**. It is not the `CLAUDE.md`
that gets generated for a target project — that one is rendered from
`templates/claude-md-template.md`.

## Project context

- This repo is the **source** of the workflow kit. It ships skills,
  templates, docs, and examples.
- Users install the kit into a **target project** under `.claude/skills/`.
  See [`docs/repo-structure.md`](docs/repo-structure.md).
- v1 is for **new projects only** (ADR-002). Do not add migration tooling
  for existing repos.
- The workflow is **GitHub-first** (ADR-004) and **plan-first, issue-by-issue**
  for execution (ADR-006).
- The branching and PR model follows [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).

## Guiding documents

- `Design/adr/` — accepted decisions; consult before proposing changes that
  touch installation, scope, PRD intake, GitHub conventions, templates, or
  execution model
- `docs/repo-structure.md` — kit vs. target-project layout
- `generic-project-workflow.md` — the reference workflow the kit implements
- `Claude Code Workflow Kit MVP Spec.md` and `Claude Code Workflow Kit — Build-Out Plan.md`
  — product direction

## Working rules

- Follow the plan-first execution model from ADR-006: propose a plan, wait
  for approval, then implement.
- Keep work scoped to the GitHub issue being worked on. Per-issue prompts
  live in `notes/`.
- Reference ADR numbers and issue numbers in commit messages when the
  change is driven by them.
- Keep the kit lightweight — no premature automation, no speculative
  abstractions.
- Never edit accepted ADRs in place. If a decision needs to change, add a
  new ADR that supersedes the old one.

## Developing the kit on itself (dogfooding)

The kit ships skills under `skills/` as distribution source. To use those
skills while developing the kit itself (so `/prepare-issue`, `/release`,
etc. are invokable in this repo), run once:

```bash
.dev/link-skills.sh
```

This symlinks each `skills/<name>/` directory into `.claude/skills/<name>/`.
Both `.dev/` and `.claude/skills/` are gitignored, so this scaffolding
never ships. Re-run the script only when the set of skill directories
changes (add, rename, delete). Edits to a skill's `SKILL.md` are live on
the next invocation without re-syncing.

See `.dev/README.md` for rationale and mechanics.

## What this file is NOT

This file is a stub added in Issue #1 so Claude Code has a minimal rules
baseline while working on the kit. A fuller `CLAUDE.md` — with commands,
testing expectations, and review conventions — will be written alongside
the template work in later issues.
