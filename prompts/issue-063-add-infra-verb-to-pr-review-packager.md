You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: none — no ADR for this bug fix; the issue is a spec-consistency change with no architectural decision required.

GitHub Issue:
- Title: Spec inconsistency: infra label not in /pr-review-packager verb classifier
- Number: #63
- Milestone: v3.4.0 - eval baseline fixes
- Labels: bug

Goal
Add `infra` to `/pr-review-packager`'s commit-verb classifier so kit-shape commits with `infra(scope):` prefix categorize under their own group rather than landing in **Other**.

Why it matters
The kit's CLAUDE.md template advertises `infra` as one of the canonical issue labels (`feature, bug, design, infra, security, docs`), and the kit's commit-conventional shape encourages `infra(scope):` prefixes for infra-labeled issues. But `/pr-review-packager`'s change-summary classifier only recognizes the strict conventional-commit verbs (`feat, fix, docs, refactor, chore, test, perf, ci, build, style`). The mismatch means commits the kit *itself* encourages get miscategorized in PR change-summaries — exactly the spec-vs-runtime drift class the v3.3.0 baseline eval surfaced. Research-tracker's issue #3 (smoke-test, infra-labeled, used `infra(papers):`) was the first fixture to hit it.

Requirements
- Add `infra` to the conventional-commit-verb regex in `skills/pr-review-packager/SKILL.md` § *Change-summary derivation* (currently lists `feat|fix|docs|refactor|chore|test|perf|ci|build|style`).
- Decide where `infra` sits in the group-output order. Recommended: alongside `chore`, `build`, `ci` (operational changes), e.g. `feat → fix → refactor → perf → docs → test → ci → build → infra → chore → style → other`. Document the choice inline.
- Update any inline references to the verb list elsewhere in the SKILL.md (edge cases, self-check, examples) to keep the spec internally consistent.
- Per the issue's *Proposed fix*, this is **fix (a)** (add to the verb list — the recommended option). Do not adopt fix (b) (drop `infra` from the kit's CLAUDE.md label set) — it would break cross-fixture consistency in already-shipped eval fixtures (md-notes, podcast-pipeline, research-tracker all use `infra` labels).

Acceptance criteria
- The verb list and matching regex in `skills/pr-review-packager/SKILL.md` § *Change-summary derivation* include `infra`.
- The group-output order section names `infra`'s position explicitly.
- A walk-through against a synthetic commit list containing `infra(scope): subject (#N)` produces an **Infra** group (not **Other**), with the `(#N)` suffix stripped per the existing rule.
- No other skill spec needs changing for this fix (the kit's CLAUDE.md template's label set already advertises `infra` and that is the source of the inconsistency the fix closes).

Scope and constraints
- Primary folders to touch: `skills/pr-review-packager/`.
- Folders to avoid unless absolutely necessary: `Design/adr/`, `templates/`, `bin/`, other `skills/*/`.
- Per ADR-039, this is **significant** because it edits `skills/*/SKILL.md`. Plan mode (`shift+tab shift+tab`) should be entered before any mutating edit. The edit itself is small (single verb addition + group-order placement), but the significance gate fires on file-class, not edit size.

Evaluation & testing requirements
- Verify by inspection: `grep -n "infra" skills/pr-review-packager/SKILL.md` shows the verb in the regex and in the group-output order list.
- Verify by walk-through: apply the change-summary derivation rules manually to three synthetic commit subjects:
  - `infra(papers): add smoke-test example` → **Infra** group, bullet text "add smoke-test example"
  - `feat(skills): add foo` → **Features** group (existing behaviour, regression check)
  - `something-weird: blah` → **Other** group (existing behaviour, regression check)
  Confirm placement matches the documented rules.
- All existing tests must continue to pass (no test runner; spec-only verification).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `skills/pr-review-packager/SKILL.md` (especially § *Change-summary derivation*)
   - `templates/claude-md-template.md` if it documents the `infra` label as part of the kit's canonical label set (alignment-check)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the specific lines in `skills/pr-review-packager/SKILL.md` that change,
   - where `infra` slots into the group-output order and why,
   - the verification walk-through.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the issue (e.g. "fix(skills): add infra verb to pr-review-packager classifier (#63)"). Since there is no governing ADR, use `(#63)` only — do not invent an ADR token.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.
   - per ADR-040, persist the summary to `notes/eval-issue-063.md`. If the session raises any cross-issue design questions affecting upcoming issues (e.g. #61's F29 categorization fix), add them as a `### design-questions` block under `## Follow-ups`.

Do not start editing files until I explicitly approve your plan.
