You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-043-programmatic-check-plan.md`
- Decision: Adopt Path 1 — ship a programmatic equivalent of `/check-plan` (likely `bin/check-plan`) so skills with documented chain points can invoke the deterministic check logic without the slash-command surface. Both surfaces share one source of truth for criteria evaluation; the five skill specs (`/adr-writer`, `/prepare-issue`, `/changelog`, `/milestone-summary`, `/pr-review-packager`) migrate to reference the programmatic surface and drop the transparency-note caveat language.

GitHub Issue:
- Title: Ship bin/check-plan programmatic surface for in-skill chain points (ADR-043)
- Number: #72
- Milestone: v3.4.0 - eval baseline fixes
- Labels: feature

Goal
Make every documented `/check-plan` chain point actually run the kit's canonical check logic, so spec aligns with runtime and skill specs stop accumulating "would invoke /check-plan but runs inline because …" caveats.

Why it matters
Five skills currently document a chain point that the runtime cannot fulfil (slash-commands aren't invokable from inside another skill). They self-flag and substitute inline — works, but the criteria list ends up duplicated across five specs and the spec reads like fiction. Path 1 fixes the spec-runtime gap structurally and also unlocks the deferred drift-checker for ADR-040's §6 schema (per ADR-040 *Maintain*) and ADR-041's §7 permission contract (per ADR-041 *Schema-drift enforcement*) — both kit-wide structural rules are queued behind this issue's framework.

## Design questions carried forward from PR #73

The following question was raised by issue #69's eval summary and preserved in PR #73's body. Address it in the plan you propose:

- **Notes for #N section grammar**: Issue #69 ships the kit-canonical PR-body section header `## Notes for #<N>` as the anchor that prepare-issue scans for via grep. Issue #72 implements ADR-043 (programmatic /check-plan) which may define a formal grammar for PR-body sections that downstream skills consume. If #72's grammar rules end up listing canonical section headers (it would be a natural place for ADR-references checks already present in pr-review-packager), the `## Notes for #<N>` shape should be added so the prepare-issue scanner can lean on a parser rather than ad-hoc grep. The downside of grep is fragility around minor markdown variations (extra whitespace, alternate hash counts); a parser closes that gap.

Requirements
- Refactor `skills/check-plan/` evaluation logic into a shared module (location TBD during implementation — likely `skills/check-plan/lib/` or a kit-internal helper).
- Create `bin/check-plan` executable wrapping the shared module with `--criteria-set <name>` and `--input <path-or-stdin>` flags, emitting structured machine-readable pass/fail output per criterion (exit 0 on pass, 1 on fail).
- Update `skills/check-plan/SKILL.md` so its slash-command surface delegates to the shared module — both surfaces share one source of truth for the criteria list and evaluation logic.
- Implement non-interactive variant: `bin/check-plan` fails closed on ambiguous input rather than blocking on operator confirmation (the slash-command surface keeps interactive behaviour).
- Migrate `skills/adr-writer/SKILL.md` chain point to call `bin/check-plan`; remove transparency-note caveat language.
- Migrate `skills/prepare-issue/SKILL.md` chain point; remove caveat.
- Migrate `skills/changelog/SKILL.md` chain point; remove caveat.
- Migrate `skills/milestone-summary/SKILL.md` chain point; remove caveat.
- Migrate `skills/pr-review-packager/SKILL.md` ADR-references check; remove caveat.
- Add `bin/check-plan` to ADR-041's permission contract (`docs/workflow-guide.md` §7) as a category-1 (substitutable) operation.
- Add an example invocation to `skills/check-plan/example.md` showing both surfaces (slash-command + `bin/check-plan`) producing identical results for the same input.
- Address the carried-forward design question above: decide whether ADR-043's grammar rules list the `## Notes for #<N>` shape as a canonical section header so `prepare-issue`'s scanner can lean on a parser; if yes, scope the parser change in this issue or as a follow-up.

Acceptance criteria
- `bin/check-plan --criteria-set <name> --input <path>` emits structured pass/fail output and exits 0/1 cleanly.
- All five migrated skills' specs reference `bin/check-plan` rather than describing inline substitution; the transparency-note caveat language is removed from all five.
- `/check-plan` slash-command continues to work and produces identical results to `bin/check-plan` for the same input (single source of truth confirmed — verifiable by running both against the same fixture).
- Non-interactive variant fails closed on the ambiguous-input cases that today block on operator confirmation.
- `docs/workflow-guide.md` §7 permission-contract table lists `bin/check-plan` as a category-1 operation.
- The carried-forward grammar question is answered explicitly in the plan and either resolved in scope or deferred with a clear rationale.

Scope and constraints
- Primary folders to touch: `bin/`, `skills/check-plan/`, `skills/adr-writer/`, `skills/prepare-issue/`, `skills/changelog/`, `skills/milestone-summary/`, `skills/pr-review-packager/`, `docs/workflow-guide.md` (the §7 cat-1 classification line).
- Folders to avoid unless absolutely necessary: `design/adr/` (ADR-043 is accepted; do not edit), `templates/`, other `skills/*/SKILL.md` files not named in primary folders.
- Per ADR-039, this issue is **significant** (creates a new `bin/` script, modifies 5+ `skills/*/SKILL.md` files plus the workflow guide). Plan mode (`shift+tab shift+tab`) should be entered before any mutating edit.
- This is the **first kit script that skills invoke programmatically** — establishes a precedent. Scope the bin/ subprocess interface (argument shape, output schema, exit codes) deliberately; future kit scripts will follow it.

Evaluation & testing requirements
- Verify by running: `bin/check-plan --criteria-set adr --input <path-to-known-good-ADR>` exits 0; same against a known-bad ADR exits 1 with a structured failure list.
- Verify by inspection: each of the five migrated skills no longer contains the "would invoke /check-plan but runs inline because …" caveat language.
- Verify equivalence: pick one criteria set (e.g. `prompt`), run both `/check-plan` and `bin/check-plan` against the same input, confirm identical pass/fail output (single source of truth).
- Verify by spec read: `docs/workflow-guide.md` §7 lists `bin/check-plan` as cat-1; the ADR-041 permission-contract table is exhaustive again.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-043-programmatic-check-plan.md`
   - `design/adr/adr-034-plan-checker.md` (the original `/check-plan` ADR — content boundary for the criteria list)
   - `design/adr/adr-041-auto-mode-permission-contract.md` (the §7 permission contract this issue extends)
   - `skills/check-plan/SKILL.md` (the existing skill being refactored)
   - The five skills to migrate: `skills/adr-writer/SKILL.md`, `skills/prepare-issue/SKILL.md`, `skills/changelog/SKILL.md`, `skills/milestone-summary/SKILL.md`, `skills/pr-review-packager/SKILL.md` — survey the existing transparency-note language before editing
   - `docs/workflow-guide.md` §7 (the cat-1 classification target)
2. Propose a short, step-by-step implementation PLAN for this issue. Before listing files and commits, **answer the carried-forward design question explicitly** in the plan: does ADR-043's grammar list canonical PR-body section headers (including `## Notes for #<N>`) for downstream skills to parse, or is that deferred to a follow-up issue? The decision affects whether `prepare-issue`'s scanner switches from grep to a parser in scope.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue (e.g. "feat(bin): add bin/check-plan programmatic surface (ADR-043, #72)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.
   - per ADR-040, persist the summary to `notes/eval-issue-072.md`. If the session raises any cross-issue design questions affecting upcoming issues, add them as a `### design-questions` block under `## Follow-ups`.

Do not start editing files until I explicitly approve your plan.
