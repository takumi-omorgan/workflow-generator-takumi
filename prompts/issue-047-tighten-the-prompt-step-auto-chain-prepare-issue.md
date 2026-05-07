You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-038-tighten-prompt-step.md`
- Decision: Two changes to `claude-issue-executor` — (1) auto-chain `prepare-issue` when no prompt exists for the issue, and regenerate with confirmation when an existing prompt is stale relative to the issue body or its linked ADRs; (2) add a `--no-prompt` flag that runs from the issue body alone for trivial issues (auto-detected on `chore`/`docs`/`bugfix-trivial` labels with zero ADR refs; explicit flag overrides detection; commit-message breadcrumb `issue executed without prompt per ADR-038`). The ADR also imposes a mandatory alignment review against ADR-031/032/033/034/035/037 before implementation, with any resulting prompt-template boundary changes recorded in a follow-up amendment ADR.

GitHub Issue:
- Title: Tighten the prompt step: auto-chain prepare-issue, add --no-prompt mode (ADR-038)
- Number: #47
- Milestone: none
- Labels: feature

Goal
Reduce ceremony for the common case (auto-chain `prepare-issue` so the prompt is a side-effect of starting work) while keeping the prompt artefact as the audit-trail anchor and the natural anchor for `/check-plan` (ADR-034) and `design/state.md` (ADR-035), and remove ADR-shaped overhead from genuinely-trivial issues via `--no-prompt`.

Why it matters
Plan mode is good but synthesises from whatever's in front of it; without a prompt, quality varies by author and session. The prompt's cost is already near-zero thanks to `prepare-issue` — the friction is in the two-command split and in trivial issues paying ADR-shaped overhead. ADR-038 is also load-bearing for keeping the executor's significance checklist (ADR-039) in lockstep with the trivial-issue criteria documented here, per the alignment-review obligation.

Requirements

**Phase 0 — alignment review (mandatory, blocks implementation).**
- Audit `prompts/_template.md` against the artefacts produced by ADR-031 (`design/planning.md`), ADR-032 (`## Phase N` blocks in `design/build-out-plan.md`), ADR-033 (`design/decisions.md`), ADR-034 (`/check-plan` criteria & contract), ADR-035 (`design/state.md`), and ADR-037 (`/milestone-summary` outputs — currently only ADR-accepted, implementation pending in #46).
- For each artefact, decide: does the prompt currently duplicate this content? If yes, trim the prompt's content boundary so each artefact has one canonical home and the prompt *links* rather than restates. If no, document why no change is needed.
- Record the result either as an inline section in the issue body, a one-page audit note under `notes/adr-038-alignment-review.md`, or — if any of the prompt-template changes are architectural in shape — a *follow-up amendment ADR* (per ADR-038's "Record the resulting boundary changes in this ADR or a follow-up amendment ADR before implementing" line; accepted ADRs cannot be edited per `CLAUDE.md`).
- The audit must complete and any resulting prompt-template trimming must land *before* the executor changes below are coded. Implementation is gated on it.

**Phase 1 — auto-chain `prepare-issue`.**
- Update `skills/claude-issue-executor/SKILL.md` so that on session start, when no `prompts/issue-NNN-*.md` exists for the resolved issue, the skill auto-invokes `prepare-issue` and proceeds. The prep step must be logged prominently so the user sees it happen.
- Add a staleness check: when an existing prompt's mtime is older than the issue body's `updated_at` (via `gh`) or any linked ADR's mtime, ask the user whether to regenerate. Default action: regenerate with confirmation, never silently.
- The auto-chain runs *before* the existing significance classification (ADR-039) so plan-mode rhythm gates the regenerated prompt as well.

**Phase 2 — `--no-prompt` mode.**
- Add a `--no-prompt` flag to `claude-issue-executor` that skips prompt generation entirely and runs from the issue body alone.
- Document criteria: single-PR scope, no design decisions, no ADR linkage. The criteria must stay in lockstep with the executor's own *trivial* checklist (per ADR-039) — the two are the single source of truth shared with this flag.
- Auto-detect (with user confirmation) when the issue has zero ADR references *and* carries one of the labels `chore`, `docs`, or `bugfix-trivial`. Explicit `--no-prompt` overrides detection.
- Leave a one-line breadcrumb in the resulting commit message: `issue executed without prompt per ADR-038`.

**Phase 3 — documentation.**
- Document the auto-chain, the staleness check, the `--no-prompt` criteria, and the auto-detect labels in `docs/workflow-guide.md` (likely as additions to section 2.d "One issue at a time to a prompt" and 2.e "Prompt to implementation").

Acceptance criteria
- Alignment review documented (location: see Phase 0 options) and any prompt-template trimming applied *before* code lands. The recorded result names each of the six ADRs and the boundary decision per ADR.
- Running `/claude-issue-executor 99` against an issue without `prompts/issue-099-*.md` auto-generates the prompt; no extra command is required, and the prep step is visibly logged.
- Stale prompt is regenerated with user confirmation, never silently. The staleness check correctly compares mtimes against the issue body and linked ADRs.
- `--no-prompt` runs against a labelled chore/docs/bugfix-trivial issue produce a clean commit with the documented breadcrumb. Auto-detection prompts for confirmation; explicit flag overrides without prompt.
- The `--no-prompt` criteria checklist matches the executor's *trivial* checklist (ADR-039) item-for-item; any divergence is treated as a bug.
- Documented criteria for when `--no-prompt` is appropriate appear in `docs/workflow-guide.md`.

Scope and constraints
- Primary folders to touch: `skills/claude-issue-executor/SKILL.md`, `docs/workflow-guide.md`, plus a possible new ADR file `design/adr/adr-NNN-*.md` if Phase 0 surfaces architectural prompt-boundary changes, plus `prompts/_template.md` if Phase 0 surfaces non-architectural trimming, plus a possible new audit note `notes/adr-038-alignment-review.md`.
- Folders to avoid unless absolutely necessary: accepted ADRs in `design/adr/` (do not edit ADR-038 or any other accepted ADR in place — use a follow-up amendment ADR), `bin/`, `examples/`, `templates/` (other than `_template.md` if Phase 0 requires it; treat trimming surgically).
- The alignment review is mandatory and must precede any executor edits. A plan that begins by editing `claude-issue-executor/SKILL.md` is the wrong shape.
- The `--no-prompt` criteria must be a single source of truth shared with the executor's trivial-checklist (ADR-039). Do not duplicate the criteria in two places; reference the trivial-checklist by anchor or extract a shared snippet that both sections include.
- Auto-detection of trivial issues is *suggestive*, not authoritative — always confirm with the user before short-circuiting the prompt step.
- The auto-chain must not bypass the plan-mode rhythm (ADR-039). Significance classification still gates plan-mode entry; only the prompt-write step is automated.
- Stale-prompt detection compares mtimes; do not embed a content-diff or hash check (out of scope).

Evaluation & testing requirements
- **Phase 0 deliverable** — show the audit-result document (whichever location) listing each of the six ADRs with a boundary decision and rationale; explicitly call out any follow-up amendment ADR drafted.
- **Auto-chain happy path** — simulate (or walk the protocol against a fixture) `/claude-issue-executor 99` with no `prompts/issue-099-*.md` present; confirm `prepare-issue` is invoked and the prep step is logged; confirm execution then proceeds.
- **Auto-chain stale-prompt path** — set up a prompt whose mtime is older than the issue body; invoke executor; confirm the user is asked (not silently regenerated) and that on `yes` the prompt is regenerated.
- **`--no-prompt` explicit** — invoke `/claude-issue-executor 99 --no-prompt`; confirm no prompt is generated and the commit-message breadcrumb is present.
- **`--no-prompt` auto-detect** — invoke against an issue with a `chore` label and zero ADR references; confirm the skill suggests `--no-prompt` mode and waits for confirmation; on `yes`, proceeds; on `no`, falls back to the standard prompt path.
- **`--no-prompt` rejected for a significant issue** — invoke against an issue with `feature` label and ADR references; confirm auto-detect does *not* trigger.
- **Lockstep verification** — read both the trivial-checklist in `claude-issue-executor/SKILL.md` (ADR-039) and the `--no-prompt` criteria; confirm they are textually identical or one is the canonical source the other includes.
- **Documentation** — `docs/workflow-guide.md` sections 2.d and 2.e mention auto-chain, staleness, and `--no-prompt` criteria.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-038-tighten-prompt-step.md`
   - `design/adr/adr-031-deeper-planning-workflow.md`, `adr-032-implementation-phases.md`, `adr-033-clarify-step.md`, `adr-034-plan-checker.md`, `adr-035-state-md-session-continuity.md`, `adr-037-milestone-lifecycle.md` (the alignment-review targets)
   - `design/adr/adr-039-plan-mode-for-significant-tasks.md` (sibling for trivial-checklist lockstep)
   - `prompts/_template.md` (the artefact under audit)
   - `skills/claude-issue-executor/SKILL.md` (the skill under modification)
   - `skills/prepare-issue/SKILL.md` (the auto-chained skill)
   - `docs/workflow-guide.md` sections 2.d / 2.e (the doc targets)
2. Propose a short, step-by-step implementation PLAN for this issue, structured as four phases — **Phase 0** (alignment review and any prompt-template trimming or follow-up amendment ADR), **Phase 1** (auto-chain), **Phase 2** (`--no-prompt`), **Phase 3** (docs). For Phase 0, include the audit-result location decision (inline, `notes/`, or new ADR) and the rationale.
3. Wait for my approval of the plan before making any edits — and especially before drafting any follow-up amendment ADR, since that is itself an architectural step.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue (e.g. "feat(scope): add thing (ADR-038, #47)"),
   - if a follow-up amendment ADR is required, draft it first via `/adr-writer` and accept it before any executor edits land.
5. At the end, provide an evaluation summary:
   - what changed,
   - the alignment-review result and any boundary trimming applied,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
