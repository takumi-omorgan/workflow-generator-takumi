You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.

ADR:
- none — this refactor changes internal kit style only, not a target-project-facing convention. The CLAUDE.md "never edit accepted ADRs in place" rule applies to ADR bodies, not skill bodies. The new style-guide line in CLAUDE.md is a one-line addition, not a kit-convention shift.

GitHub Issue:
- Title: Prune parenthetical ADR attributions from SKILL.md bodies
- Number: #83
- Milestone: none
- Labels: docs, refactor

Goal
Prune attribution-style ADR references — `(ADR-NNN)`, `(per ADR-NNN)`, `implements ADR-NNN` — from the bodies of `skills/*/SKILL.md`, where they exist for internal traceability rather than for the reader. Voice/clarity-only refactor: zero behaviour change.

Why it matters
Skill metadata and bodies load eagerly into context every session — every parenthetical attribution pays a token cost on every invocation. The audit harness at `notes/skills-audit-2026-05-07/adr-audit.py` found **71 high-confidence + 5 medium-confidence type-3 candidates across 17 of 19 skills.** Three high-density skills (`claude-issue-executor` 21, `prepare-issue` 12, `adr-writer` 8) account for 41 (~58%) of the high-confidence matches. Beyond the token cost, the noise obscures the user-facing voice — *"Optional: design/planning.md (per ADR-031)"* is harder to scan than *"Optional: design/planning.md"*. The same prune was applied recently to `docs/workflow-guide.md` with markedly cleaner reading voice. This issue applies the same audit to the 19 skill files. Pairs with `notes/refactoring-ideas.md` entry #9 (broader SKILL.md style audit) and entry #10 (kit-wide token-economy framework) but is independently shippable.

Requirements
- Apply the per-match plan in `notes/skills-audit-2026-05-07/adr-attributions.md` across the 17 affected SKILL.md files: prune pure parentheticals and heading attributions; reformat genuine drill-downs to inline markdown links; spot-check the 5 medium-confidence matches case-by-case.
- Add a one-line style-guide entry to `CLAUDE.md` under Working rules: *"SKILL.md bodies should not include parenthetical ADR attributions (`(per ADR-NNN)`, `(ADR-NNN)`) for traceability alone. Cite an ADR only when the reader needs the link to do the task — in which case use a markdown link in body text, not an inline parenthetical."*
- Preserve type-2 schema-name phrases — `ADR-040 carry-forward`, `ADR-035 zones`, `ADR-041 permission contract`, `ADR-038 ... checklist` — these are not attribution noise.

Acceptance criteria
- `python3 notes/skills-audit-2026-05-07/adr-audit.py` reports `high_conf_count` ≤ 5 across all 19 skills, with each remaining hit annotated in the PR description as a deliberate drill-down kept by reformatting (not by leaving the original parenthetical).
- `CLAUDE.md` contains the new one-line style-guide entry under Working rules.
- No type-2 schema-name phrases (`ADR-040 carry-forward`, `ADR-035 zones`, `ADR-041 permission contract`) are removed.
- No behaviour change: the 19 SKILL.md files still drive the same workflows. Smoke check: `/resume`, `/prepare-issue`, `/release` still parse cleanly.
- The PR body cross-references `notes/refactoring-ideas.md` entry #2 and links the per-match listing.

Scope and constraints
- Primary folders to touch: `skills/` (17 of 19 SKILL.md files), `CLAUDE.md` (1 new bullet).
- Folders to avoid unless absolutely necessary: `design/adr/`, `templates/`, `docs/`, `examples/`, `archive/`, `bin/`, `prompts/` (out of scope), `notes/refactoring-ideas.md` (pre-existing modification, separate concern), `notes/skills-audit-2026-05-07/` (consumed but not edited).
- Voice-only — zero behaviour change. No skill workflow gains or loses a step. No new tooling shipped.

Evaluation & testing requirements
- Re-run `python3 notes/skills-audit-2026-05-07/adr-audit.py` after each commit and log the new `high_conf_count` so the trend is auditable.
- Final `high_conf_count` ≤ 5; remaining hits annotated.
- `grep -rn 'ADR-040 carry-forward\|ADR-035 zones\|ADR-041 permission contract' skills/` returns matches (type-2 phrases preserved).
- `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json` exits 0 (eval module intact — sanity check that nothing in the prune broke check-plan's parser).
- All existing tests must continue to pass (kit has no automated test runner — voice-only changes covered by adr-audit.py + grep checks).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `notes/skills-audit-2026-05-07/adr-attributions.md` (the per-match work plan)
   - any existing modules under `skills/`
   - any existing tests related to the modules you will change (none — kit has no automated test runner)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - key functions or structures,
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue (e.g. `refactor(skills): prune ADR attributions in <skill> (#83)`).
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
