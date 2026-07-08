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

## Hermes hardened workflow (overlay — non-negotiable)

These rules extend the Workflow rules above. They exist because of the
llm-wiki-kit Phase 5–7 failure (July 2026): a review outage plus an
"autonomous mandate" let three phases land on `main` unreviewed, unbuildable,
and with fabricated closeout docs. No session may waive these.

### Gates cannot be skipped, only failed

- **Adversarial review is a hard gate.** Every ADR, PRD/normalization
  output, and phase closeout gets an independent adversarial review (Codex
  or equivalent) reaching `READY` before acceptance/merge. If the reviewer
  is unavailable (usage limit, outage, missing CLI): **HALT the phase and
  report to Oliver.** "Review deferred, covered by tests" is exactly the
  rationalization that caused the failure — it is forbidden.
- **No mandate may remove a gate.** An autonomous-phase mandate can
  delegate *who operates* a gate, never whether it runs. Plan-first
  approval, issue-per-PR, adversarial review, and green tests apply in
  every session, supervised or not.

### Ratification debt

- At most **one phase** of ADRs may be "accepted under mandate, awaiting
  Oliver's async ratification" at any time. The next phase's issues may
  not be filed until the backlog is ratified. (In the failure, five
  unratified ADRs had normalized "accept now, ask later".)

### Mechanical enforcement assumed

- `main` has branch protection: PRs only, required status checks
  (`guard` + full test matrix), no force pushes, enforced for admins.
  Never attempt to bypass it, and treat its absence as a setup bug to fix
  before feature work.
- An unexpected committer identity in `git log main` is a stop-the-line
  event: halt, report, do not build on top of it.

### Phase and closeout discipline

- A phase's prerequisite ADRs are drafted **and accepted** before its
  implementation issues open. No implementation commit may cite an ADR
  that does not exist.
- Closeouts are atomic: `design/state.md`, `knowledge/log.md`, and
  `knowledge/index.md` update in the **same** closeout PR, and a phase is
  "closed" only when that PR merges. If these three files disagree, the
  most conservative one is true and the disagreement is a bug to fix first.
- **Evidence honesty.** Never write a coverage number, CI verdict, PR
  link, or "criterion satisfied" claim that was not directly observed;
  cite the run ID / commit. A `pull/new/...` URL is not a PR.

### Repo hygiene

- No compiled binaries or files >1 MB in commits (guard-enforced).
- No new runtime dependency without an ADR. Replacing a dependency an
  accepted ADR chose (e.g. the YAML library) requires a superseding ADR
  first — never edit or contradict an accepted ADR in place.
- Rewrites that delete exported API used elsewhere in the repo are
  architecture changes: ADR first, then a plan, then a PR.
