You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.

ADR:
- none — this refactor changes internal kit style only, not a target-project-facing convention. Same reasoning as the sibling #83 issue (type-3 ADR attribution prune): the CLAUDE.md "never edit accepted ADRs in place" rule applies to ADR bodies, not skill frontmatter.

GitHub Issue:
- Title: Apply 2026-05-07 skills-audit recommendations across the cohort
- Number: #84
- Milestone: none
- Labels: docs, refactor

Goal
Phase 1 of issue #84: rewrite all 19 skill description fields in `skills/*/SKILL.md` frontmatter to follow Anthropic's canonical `[what it does]. Use when [trigger].` template, plus boundary clauses for 5 adjacent-skill clusters identified in the audit. Voice/metadata-only; zero behaviour change. Phase 2 (body slimming) and Phase 3 (sidecar consistency) are explicitly out of scope for this session — they ship as separate PRs in later sessions.

Why it matters
Skill metadata loads eagerly into context every session, and Claude routes among the cohort using descriptions alone — so cohort drift carries a recurring routing-accuracy cost on every invocation. The 2026-05-07 audit (`notes/skills-audit-2026-05-07/findings-v2.md`), source-checked against Anthropic's canonical Skills guidance and independently verified by `openai/gpt-5.5`, found three concrete problems: **6 of 19 descriptions lack `has_when` framing entirely** (`adr-writer`, `changelog`, `claude-issue-executor`, `prd-normalizer`, `prd-to-mvp`, `release`); **4 are partial** with positional/chain framing only (`check-plan`, `clarify`, `issue-planner`, `planning`); and **5 adjacent-skill clusters need explicit boundary clauses** to disambiguate routing. The GPT-5.5 routing test confirmed `prepare-issue` ↔ `claude-issue-executor` as the only medium-confidence ambiguity in 10 prompts. Adopting Anthropic's literal "Use when…" pattern across all 19 lifts cold-start routing accuracy uniformly.

Requirements
- Rewrite all 19 description fields per the canonical `[what it does]. Use when [trigger].` template. The audit's `findings-v2.md` and `methodology-v2.md` have the full rubric; the approved plan file has the per-cluster boundary-clause drafts.
- Add boundary clauses for the 5 adjacent-skill clusters: prepare-issue ↔ claude-issue-executor; pause ↔ resume; planning ↔ clarify ↔ adr-writer; changelog ↔ release; audit-milestone ↔ complete-milestone ↔ milestone-summary.
- Re-score `notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv` so all 19 rows show `has_what=yes`, `has_when=yes`, `has_triggers=yes`, `third_person=yes` after the rewrite.

Acceptance criteria
- Every rewritten description scores `has_what=yes`, `has_when=yes`, `has_triggers=yes`, `third_person=yes` under the `methodology-v2.md §4.1` rubric.
- No description exceeds 1,024 chars (Anthropic hard cap; current max is 238 chars, plenty of headroom).
- All 19 use the literal `Use when` phrasing for cohort consistency.
- No behaviour change: each touched skill still drives the same workflow. Smoke check: `/resume`, `/prepare-issue`, `/release` still parse cleanly under their new descriptions.
- Phase 2 (body slimming for over-budget skills) and Phase 3 (sidecar consistency) explicitly NOT performed in this session — they ship as their own PRs in later sessions.

Scope and constraints
- Primary folders to touch: `skills/*/SKILL.md` (19 files, frontmatter only — `description:` field), `notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv` (re-score 19 rows).
- Folders to avoid unless absolutely necessary: SKILL.md bodies (Phase 2 territory), sidecar files (Phase 3 territory), `design/adr/`, `templates/`, `docs/`, `examples/`, `archive/`, `bin/`, `CLAUDE.md`, `notes/refactoring-ideas.md`, `notes/feature-ideas.md`.
- Voice/metadata-only — zero behaviour change. No skill workflow gains or loses a step. No new tooling shipped.

Evaluation & testing requirements
- `python3 notes/skills-audit-2026-05-07/audit.py` after the rewrite — confirm `description_chars` ≤ 1024 for all 19 and no structural regressions.
- `awk -F, 'NR>1 && ($2!="yes" || $3!="yes" || $4!="yes" || $5!="yes")' notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv` returns empty after re-score (all 19 rows pass all four rubric fields).
- `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json` exits 0 (sanity check that nothing broke check-plan's parser).
- All existing tests must continue to pass (kit has no automated test runner — voice/metadata changes covered by audit.py + CSV diff).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `notes/skills-audit-2026-05-07/findings-v2.md` (the audit's analysis and worked examples)
   - `notes/skills-audit-2026-05-07/methodology-v2.md` (the rubric + verbatim Anthropic source quotes)
   - `notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv` (per-skill scores under v2 rubric)
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
   - commit incrementally with messages referencing the ADR and issue (e.g. `refactor(skills): rewrite 19 descriptions to canonical Use-when shape (#84)`).
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues (Phase 2 + Phase 3 are deferred to separate sessions),
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
