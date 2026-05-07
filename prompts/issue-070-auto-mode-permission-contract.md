You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-041-auto-mode-permission-contract.md`
- Decision: Adopt Option A — define a kit-wide auto-mode permission contract that classifies skill operations into three categories (substitutable, operator-acknowledged-bypass, non-substitutable), codified as a new section of the workflow guide and instanced by `claude-issue-executor` and `pr-review-packager`.

GitHub Issue:
- Title: Define auto-mode permission contract for strict-mode skill operations (ADR-041)
- Number: #70
- Milestone: v3.4.0 - eval baseline fixes
- Labels: feature

Goal
Give the kit a single source of truth for what auto-mode is allowed to substitute for, so silent-bypass regressions on hard-to-reverse skill operations become structurally impossible rather than author-convention-dependent.

Why it matters
ADR-039 narrowly fixed the executor's plan-mode bypass. The same shape appears in F23 (`/pr-review-packager` strict-mode mismatch) and will recur in any future strict-mode skill — the kit needs a generalised rule, not per-skill patches. ADR-041 generalises the principle into a kit-wide three-category contract; this issue ships the workflow-guide section + the two skill-spec instances + a per-skill-front-matter classification line that makes the categorisation operator-visible.

## Design questions carried forward from PR #73

The following questions were raised by issue #69's eval summary and preserved in PR #73's body. Address each in the plan you propose:

- **Schema-evolution governance for design-questions**: The ADR-040 schema is documented as version 1 in docs/workflow-guide.md §6, with a lockstep-update obligation that says "when the schema evolves, update §6 first then update the three SKILL.md cross-references in the same change." No machine-checkable enforcement exists — drift between the canonical §6 schema and any one SKILL.md cross-reference silently breaks the carry-forward loop. Issue #70 implements ADR-041 (auto-mode permission contract) which lands kit-wide classification machinery; consider whether that work should also include a sibling drift-checker (e.g. a CI step or a bin/check-design-questions-schema-drift script), or whether the long-term home is the ADR-034 plan-checker once #72 lands a generic structural-rule framework. Decide before #70 starts so the scope is explicit.
- **--no-prompt interaction with carry-forward**: ADR-040 (and §6 of the workflow guide) document that --no-prompt skips prepare-issue and therefore the carry-forward consumer step. This is acceptable because the trivial-issue criteria (single typo, dependency bump, ADR status flip) by definition do not raise cross-issue design questions. ADR-041 (issue #70) generalises auto-mode behaviour into a kit-wide permission contract with three categories (substitutable, operator-acknowledged-bypass, non-substitutable). If ADR-041's auto-mode introduces new bypass code paths for non-trivial reasons (e.g. CI-driven implementations, bulk migrations), the --no-prompt-skips-carry-forward exemption needs revisiting: bypassing carry-forward silently on a non-trivial issue would re-open the gap ADR-040 was written to close. Decide whether ADR-041's permission categories cover this case explicitly, or whether a follow-up ADR amendment is needed.

Requirements
- Add an "Auto-mode permission contract" section to `docs/workflow-guide.md` with the three categories (substitutable, operator-acknowledged-bypass, non-substitutable) and concrete examples for each.
- Classify every current shipped skill's operations into category 1 / 2 / 3 in the workflow-guide section as the canonical list.
- Update `skills/claude-issue-executor/SKILL.md`: under auto-mode, ask once at session start (`"Enter plan mode? yes / no / decide-from-scope"`) rather than auto-classify; the "no" branch requires written acknowledgement in chat output.
- Update `skills/pr-review-packager/SKILL.md`: codify the confirmed-yes pattern (already followed in practice on every shipped PR) as the canonical category-3 behaviour.
- Cross-reference ADR-039's significant-task checklist as the per-skill instance of the category-2 rule; document the alignment-review obligation between the contract and ADR-039.
- Document `--no-prompt` (ADR-038) interaction: `--no-prompt` is itself a category-1 operator-pre-authorization for the trivial-issue path; it does not bypass category-3 operations.
- Add a "permission category" line to the front-matter of every shipped skill's SKILL.md so the classification is operator-visible at glance.

Acceptance criteria
- The contract appears in `docs/workflow-guide.md` as a single source of truth, with the three categories named and each shipped-skill operation classified.
- Every shipped skill's SKILL.md front-matter declares its operations' permission categories.
- `claude-issue-executor` under auto-mode asks the plan-mode question at session start (not silently auto-classifies); a "no" answer requires written acknowledgement.
- `pr-review-packager` continues to require explicit `yes` for category-3 operations regardless of mode (codified, not just observed).
- A new skill author has one document to consult when adding a strict-mode gate.

Scope and constraints
- Primary folders to touch: `docs/workflow-guide.md`, `skills/claude-issue-executor/`, `skills/pr-review-packager/`, plus the front-matter of every shipped `skills/*/SKILL.md`
- Folders to avoid unless absolutely necessary: `design/adr/` (ADR-041 is accepted; do not edit), `bin/`, `templates/`, the bodies of `skills/*/SKILL.md` files not named in primary folders (front-matter only, per the per-skill-classification requirement)
- Per ADR-039, this issue is **significant** (modifies 2 `skills/*/SKILL.md` bodies plus front-matter changes across all shipped skills plus the workflow guide). Plan mode (`shift+tab shift+tab`) should be entered before any mutating edit.
- Address both carry-forward design questions in the plan you propose — they have direct scope implications for this issue (drift-checker decision affects scope; --no-prompt category coverage affects the contract content).

Evaluation & testing requirements
- Verify by reading: every shipped skill's SKILL.md front-matter has a permission-category line; the workflow-guide section names every shipped operation's category exhaustively.
- Verify by inspection: the three categories' boundaries are concrete enough to classify a hypothetical new skill operation without operator judgment (mirror ADR-040's AC4 standard for the when-NOT-to-populate rule — apply the categories mentally to 3 hypothetical skill operations and confirm clear placement).
- Verify by spec read: ADR-039's significant-task checklist is cited from the new section as the category-2 instance, and the alignment-review obligation between the two checklists is documented.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-041-auto-mode-permission-contract.md`
   - `design/adr/adr-039-plan-mode-for-significant-tasks.md` (this issue generalises ADR-039's per-skill rule)
   - `design/adr/adr-038-tighten-prompt-step.md` (--no-prompt interaction question)
   - `design/adr/adr-040-cross-skill-design-question-carry-forward.md` (drift-checker question; just shipped, fresh in repo)
   - `docs/workflow-guide.md` (host of the new section; §6 is the most recent precedent for adding a top-level section)
   - `skills/claude-issue-executor/SKILL.md`, `skills/pr-review-packager/SKILL.md`
   - The front-matter of every shipped skill under `skills/*/SKILL.md` (read-only survey before editing)
2. Propose a short, step-by-step implementation PLAN for this issue. Before listing files and commits, **answer the two carried-forward design questions explicitly** in the plan: (a) does the drift-checker for the §6 schema land in this issue, in #72 with ADR-043's structural-rule framework, or as a follow-up; (b) does the contract's category coverage account for non-trivial auto-mode bypass paths, or does that need a follow-up ADR amendment.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue (e.g. "feat(skills): add auto-mode permission contract section to workflow guide (ADR-041, #70)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.
   - per ADR-040, persist the summary to `notes/eval-issue-070.md`. If the session raises any cross-issue design questions affecting #71 or #72, add them as a `### design-questions` block under `## Follow-ups`.

Do not start editing files until I explicitly approve your plan.
