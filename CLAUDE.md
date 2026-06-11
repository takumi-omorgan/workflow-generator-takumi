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
- The kit is scoped to **new projects only**. Do not add migration
  tooling for existing repos.
- The workflow is **GitHub-first** and **plan-first, issue-by-issue**
  for execution.
- The branching and PR model follows [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).

## Guiding documents

- [`docs/repo-structure.md`](docs/repo-structure.md) — kit vs. target-project layout
- [`docs/workflow-guide.md`](docs/workflow-guide.md) — action-oriented walkthrough of the kit
- [`docs/skills.md`](docs/skills.md) — functional skill reference
- [`docs/architecture.md`](docs/architecture.md) — how the kit itself is organized
- [`README.md`](README.md) — positioning and product direction

## Working rules

- Follow the plan-first execution model: propose a plan, wait for
  approval, then implement.
- Keep work scoped to the GitHub issue being worked on.
- Reference issue numbers in commit messages when the change is driven by
  them.
- Keep the kit lightweight — no premature automation, no speculative
  abstractions.

## Source-repo contributor notes

The notes below are for contributors working in the kit's **source**
repository. They reference material that is intentionally not part of the
published distribution, so this whole section is stripped from the public
export.

- `design/adr/` — accepted decisions; consult before proposing changes that
  touch installation, scope, PRD intake, GitHub conventions, templates, or
  execution model. Key decisions: new-projects-only scope (ADR-002),
  GitHub-first (ADR-004), and plan-first issue-by-issue execution (ADR-006).
- `archive/` — archived original framing (historical audit
  trail only; do not treat as current direction). Includes
  `mvp-spec.md`, `build-out-plan.md`, and
  `generic-project-workflow.md` (the original methodology design doc
  the kit operationalises), plus `phase-1/` historical issue prompts.
- Per-issue prompts live in `notes/`. Reference ADR numbers alongside issue
  numbers in commit messages when the change is driven by an ADR.
- SKILL.md bodies should not include parenthetical ADR attributions
  (`(per ADR-NNN)`, `(ADR-NNN)`) for traceability alone. Cite an ADR
  only when the reader needs the link to do the task — in which case
  use a markdown link in body text, not an inline parenthetical.
- Never edit accepted ADRs in place. If a decision needs to change, add a
  new ADR that supersedes the old one. Mechanical path-string rewrites
  are an explicit exception (ADR-044).

## Developing the kit on itself (dogfooding)

The kit ships skills under `skills/` as distribution source. To use those
skills while developing the kit itself (so `/prepare-issue`, `/release`,
etc. are invokable in this repo), run once:

```bash
~/dotfiles/claude-config/bin/link-skills
```

This symlinks each `skills/<name>/` directory into `.claude/skills/<name>/`.
`.claude/skills/` is gitignored, so the symlinks never ship. Re-run the
script only when the set of skill directories changes (add, rename, delete).
Edits to a skill's `SKILL.md` are live on the next invocation without
re-syncing.

The `link-skills` tool lives in the personal dotfiles repo so it syncs
across machines; it is intentionally NOT part of the kit. See the
dogfooding playbook at `~/dotfiles/claude-config/docs/dogfooding-playbook.md`
for the full methodology (kit dogfooding and app dogfooding).
