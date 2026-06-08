# Workflow Kit Evaluation Fix Blueprint — 2026-06-06

## Purpose

This blueprint turns the three-project evaluation findings into a concrete fix plan for the Workflow Kit. It is derived from `design/workflow-kit-three-project-evaluation-20260606.md` and is scoped to kit issues found while evaluating:

- `web-task-board` — long-running HTTP service
- `cli-expense-tool` — batch CLI/package
- `data-quality-pipeline` — file-in/artifacts-out data quality gate

The eval projects themselves are not part of this repo and should not be pushed here. This file captures only the kit remediation plan.

## Executive summary

The kit worked: install, templates, project rules, docs, ADR flow, and verification all supported real project work across three different shapes.

The fix work is mostly day-one onboarding and consistency hardening:

1. Fix contradictory prompt-path guidance in generated `CLAUDE.md`.
2. Fix `sync-adr-index` rewrite exit-code semantics.
3. Remove or clearly mark unresolved template guidance blocks in rendered `CLAUDE.md`.
4. Make fresh installs stop pointing at missing day-one artifacts without context.
5. Add a clearer next-step path after install.
6. Add regression checks so these issues do not reappear.

## Non-goals

- Do not import or commit the three generated eval projects.
- Do not redesign the kit workflow model.
- Do not change accepted ADRs in place except for mechanical path-string fixes allowed by ADR-044.
- Do not add heavyweight automation where a small doc/template fix is enough.

## Source findings

### F1 — `CLAUDE.md` prompt-path contradiction

Severity: Medium

The rendered `CLAUDE.md` says per-issue prompts live in `notes/issueNN-prompt.md`, while the rest of the kit uses `prompts/issue-NNN-short-title.md`:

- `prepare-issue` skill
- `prompts/_template.md`
- `start` skill
- `state-template.md`
- installer-created `prompts/` directory

Impact: a user following `CLAUDE.md` can create prompt files in a directory the skills do not use.

Fix:

- Update `templates/claude-md-template.md` to use `prompts/issue-NNN-short-title.md` everywhere.
- Update project-tree examples and “See also” references accordingly.
- Add a grep/self-test gate for stale `notes/issueNN-prompt.md` references in generated artifacts.

Acceptance:

- Fresh install renders no `notes/issueNN-prompt.md` guidance.
- `CLAUDE.md`, `prepare-issue`, `start`, `state-template.md`, and `prompts/_template.md` agree on prompt location and filename shape.

### F2 — `sync-adr-index` exits 1 after successful rewrite

Severity: High for automation; Low/Medium for manual use

The eval saw `sync-adr-index` print a successful rewrite message but return exit code 1 on the normal rewrite path. This breaks `set -e`, Makefiles, and CI even though the command succeeded.

Fix:

- Change normal rewrite success to exit 0.
- Keep `--check` drift as non-zero.
- Reserve non-zero for genuine failure or check-mode drift.
- Update script header/docs to describe the contract.
- Add a regression test:
  - first generate/rewrite exits 0
  - second no-op generate exits 0
  - `--check` in sync exits 0
  - `--check` drift exits non-zero

Acceptance:

- `sync-adr-index && next-command` is safe after a successful rewrite.
- CI can distinguish successful rewrite from check-mode drift.

### F3 — rendered `CLAUDE.md` retains unresolved `{{...}}` guidance blocks

Severity: Medium

The installed `CLAUDE.md` claims a freshly rendered file should not carry unresolved `{{PLACEHOLDER}}` syntax, but some multi-line guidance blocks remain in mustache braces. These are guidance blocks, not token placeholders, but they look like rendering bugs.

Fix options:

- Preferred: convert guidance blocks to clear HTML comments, for example `<!-- FILL: describe the project here -->`.
- Alternative: render them as `_TBD_`-style markers with explicit explanation.
- If intentionally retained, update docs/logs so the guarantee is not false.

Acceptance:

- A fresh rendered `CLAUDE.md` does not contain ambiguous `{{...}}` guidance blocks.
- Any remaining fill-in markers are documented in the file itself.

### F4 — fresh install points to missing day-one files

Severity: Medium/Low

Fresh installs reference workflow outputs that do not exist yet:

- `design/state.md`
- `design/mvp.md`
- `design/ai-summary.md`
- `design/build-out-plan.md`

Some are intentionally produced later, but a new user sees dead links and a front-door skill that reads a missing state file.

Fix:

- Make `start` / `resume` degrade gracefully when `design/state.md` is missing:
  - say there is no state yet
  - recommend `/start`, `/idea-to-prd`, or creating/filling the PRD depending on context
- Either scaffold a minimal `design/state.md` at install time or explicitly document that it is created later.
- Annotate day-one missing links in `CLAUDE.md` as “created later by workflow”.
- Prefer conditional link rendering if the installer has enough context.

Acceptance:

- A user opening a fresh install knows what exists now and what will be created later.
- No first-run skill fails confusingly because `design/state.md` is missing.

### F5 — missing “what next?” instruction after install

Severity: Low; high onboarding value

The installer's final output ends with `done. target: ...` but does not tell the user the next action.

Fix:

- Add a short final stanza to `bin/install-workflow-kit` output:

```text
Next steps:
1. Open the project in Claude Code.
2. Run /start.
3. If GitHub metadata is unknown, fill GITHUB_OWNER / repo settings when ready.
```

- Add the same guidance to rendered `CLAUDE.md` or a generated `GETTING-STARTED.md` if that is preferable.

Acceptance:

- A first-time user can install the kit and know the next command without reading the full docs first.

### F6 — `.gitignore` language defaults are too generic

Severity: Low

For Python eval projects, `__pycache__/` and `*.pyc` were commented out by default, so tests created would-be-committed noise.

Fix options:

- Add `--lang python|node|generic` to installer and uncomment matching ignore rules.
- Or auto-detect from existing files like `pyproject.toml`, `package.json`, etc.
- Keep generic behavior as default when uncertain.

Acceptance:

- Python target projects do not show `__pycache__/` or `*.pyc` as untracked after test runs when Python mode is selected/detected.

### F7 — local-only / no-GitHub path is under-documented

Severity: Low

The kit is intentionally GitHub-first, but local-only evals are useful. Docs should explicitly say which steps degrade gracefully when there is no remote.

Fix:

- Add a short “local-only / no GitHub remote” subsection to `docs/install.md` or `docs/workflow-guide.md`.
- Explain that `_TBD_` GitHub values are acceptable temporarily.
- Explain which GitHub-dependent skills are skipped until a remote exists.

Acceptance:

- Local-only users understand that install success with `_TBD_` GitHub metadata is valid and temporary.

### F8 — target-side validation surface is thin

Severity: Low/Medium

Target projects receive `sync-adr-index`, but not a broader local health check for workflow state.

Fix:

- Consider installing a lightweight target-side validation command, for example `.claude/bin/validate-design`.
- Initial checks:
  - `design/state.md` fences present if file exists
  - ADR index in sync
  - required PRD/MVP fields non-empty when those files exist
  - generated `CLAUDE.md` has no ambiguous unresolved template syntax
  - prompt path convention is consistent

Acceptance:

- A target project can run one local command to catch common workflow-shape drift without needing the kit repo.

## Proposed implementation sequence

### PR 1 — Template consistency and onboarding copy

Scope:

- F1: prompt path contradiction
- F3: unresolved `{{...}}` guidance blocks
- F4: annotate or conditionally render missing day-one links
- F5: installer next-step stanza
- F7: local-only docs note

Why first: these are mostly docs/templates and directly improve first-run usability.

Suggested files:

- `templates/claude-md-template.md`
- `bin/install-workflow-kit`
- `docs/install.md`
- `docs/workflow-guide.md`
- relevant tests/self-tests for rendered output

### PR 2 — `sync-adr-index` exit-code correction

Scope:

- F2 only

Why separate: exit-code behavior is executable behavior and should have focused tests.

Suggested files:

- `bin/sync-adr-index` or source template used to install it
- tests covering rewrite/no-op/check drift
- docs that describe exit codes

### PR 3 — Fresh-state and target-side validation

Scope:

- F4 deeper fix
- F8 target-side validation

Why third: this may require deciding whether to scaffold `design/state.md` on install or make skills degrade gracefully. Keep it separate from simple template fixes.

Suggested files:

- `skills/start/SKILL.md`
- `skills/resume/SKILL.md`
- `templates/state-template.md`
- optional `.claude/bin/validate-design` installer surface
- `docs/self-test.md`
- `docs/workflow-control.md`

### PR 4 — Language-aware ignore defaults

Scope:

- F6

Why last: useful but less important than onboarding correctness and validation semantics.

Suggested files:

- `bin/install-workflow-kit`
- `.gitignore` template/source
- installer docs
- tests for Python detection or `--lang python`

## Regression checks to add

At minimum, add a fixture install test that asserts:

- rendered `CLAUDE.md` contains `prompts/issue-NNN-short-title.md`
- rendered `CLAUDE.md` does not contain `notes/issueNN-prompt.md`
- rendered `CLAUDE.md` has no ambiguous unresolved `{{...}}` blocks unless explicitly allowed
- installer output includes a next-step hint
- missing GitHub owner renders as `_TBD_` with a clear warning
- `sync-adr-index` rewrite exits 0
- `sync-adr-index --check` exits non-zero only on drift

## Priority recommendation

Do PR 1 and PR 2 before any new feature work. They are small, high-confidence, and directly address the most confusing or automation-breaking evaluation findings.

PR 3 is the design-choice item. Decide whether the kit wants to scaffold state files immediately or teach the front-door skills to handle their absence gracefully. The latter is probably simpler and less noisy.

PR 4 is opportunistic. It improves quality of life but should not block higher-value workflow fixes.
