You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-035-state-md-session-continuity.md`
- Decision: Adopt Option A — ship `design/state.md` as a lightweight committed artefact tracking current phase, in-flight issue, recent work, blockers, and a "continue here" pointer; updated by `prepare-issue`, `claude-issue-executor`, and `pr-review-packager`; new `/resume` skill briefs the next session and new `/pause` skill writes a richer handoff for context-exhausting sessions.

GitHub Issue:
- Title: Add design/state.md plus /resume and /pause skills (ADR-035)
- Number: #44
- Milestone: none
- Labels: feature

Goal
Give long-running projects cross-session memory beyond what's in git, and reduce context-reconstruction time at session start.

Why it matters
Today every fresh session reconstructs state from `gh` calls and prompt files. For multi-month projects spanning many issues and phases this is real friction; the state file gives `/resume` a fast path and gives ADR-038's executor somewhere to record progress.

Requirements
- Add `templates/state-template.md` (under ~100 lines, fields: current phase, in-flight issue, recent work, blockers, continue-here pointer).
- Add `skills/resume/SKILL.md` that reads `design/state.md` and emits a one-message brief.
- Add `skills/pause/SKILL.md` that writes a richer handoff plus optional `notes/handoff-YYYY-MM-DD.md`.
- Update `skills/prepare-issue/SKILL.md` to set the in-flight issue in `design/state.md`.
- Update `skills/claude-issue-executor/SKILL.md` to mark progress in `design/state.md` (per ADR-038).
- Update `skills/pr-review-packager/SKILL.md` to close out the issue and update recent work.
- Document the conflict-resolution rule: most-recently-merged PR wins; `/resume` re-derives from `gh` if the file looks suspect.
- CI sanity check that `design/state.md` stays under the line cap (or document as a manual rule).

Acceptance criteria
- `design/state.md` round-trips through prepare → execute → review without manual editing.
- `/resume` produces a useful brief from `state.md` alone (no `gh` calls required for the happy path).
- `/pause` produces a session handoff that lets a fresh Claude Code instance pick up cleanly.
- File stays under ~100 lines on a representative multi-issue project.

Scope and constraints
- Primary folders to touch: `templates/`, `skills/resume/`, `skills/pause/`, `skills/prepare-issue/`, `skills/claude-issue-executor/`, `skills/pr-review-packager/`, `skills/README.md`, `templates/README.md`, `docs/workflow-guide.md` (light update if helpful).
- Folders to avoid unless absolutely necessary: `design/adr/` (do not edit accepted ADR-035), `bin/`, `examples/`, `prompts/` (other than this issue's own prompt).
- The kit ships skills as distribution source under `skills/`; do not commit anything under `.claude/skills/` (gitignored, populated by `link-skills`).

Evaluation & testing requirements
- Demonstrate the round-trip: dry-run `prepare-issue` → `claude-issue-executor` → `pr-review-packager` updates against a representative `design/state.md` and confirm each writes the expected fields idempotently.
- Verify `/resume` produces a coherent brief from `state.md` only (no `gh` fallback) on the happy path, and that the documented `gh`-fallback path triggers when the file is empty/missing/suspect.
- Verify `/pause` writes a usable handoff (and the optional dated `notes/handoff-YYYY-MM-DD.md`) that a fresh Claude Code session can read to pick up cleanly.
- Confirm the line cap: a representative multi-issue `state.md` stays under ~100 lines; document or enforce via CI as the issue requires.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-035-state-md-session-continuity.md`
   - any existing modules under `templates/`, `skills/resume/`, `skills/pause/`, `skills/prepare-issue/`, `skills/claude-issue-executor/`, `skills/pr-review-packager/`
   - any existing tests related to the modules you will change
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - key functions or structures,
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue (e.g. "feat(scope): add thing (ADR-035, #44)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
