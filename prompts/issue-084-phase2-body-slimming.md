You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.
- This is **Phase 2 of issue #84**. Phase 1 (description rewrites) shipped in PR #86. Phase 3 (sidecar consistency) is a separate later session.

ADR:
- none — this refactor changes internal kit style only, not a target-project-facing convention. Same reasoning as the sibling #83 issue and the Phase 1 prompt: the CLAUDE.md "never edit accepted ADRs in place" rule applies to ADR bodies, not skill body content. Anthropic's 500-line / 5k-token L2 budget is the operative external constraint.

GitHub Issue:
- Title: Apply 2026-05-07 skills-audit recommendations across the cohort
- Number: #84
- Milestone: none
- Labels: docs, refactor

Goal
Phase 2 of issue #84: bring four over-budget skills (`claude-issue-executor`, `pr-review-packager`, `release`, `prepare-issue`) under Anthropic's 500-line / 5k-token L2 SKILL.md budget by lifting content into one-level-deep sidecar files. Voice/structure-only; zero behaviour change. Phase 1 (description rewrites) is shipped (PR #86); Phase 3 (sidecar consistency) is explicitly out of scope for this session — it ships as a separate PR.

Why it matters
SKILL.md files load eagerly into context every session, so any skill over Anthropic's stated L2 budget pays a recurring per-session token cost across every invocation. The 2026-05-07 audit (`notes/skills-audit-2026-05-07/findings-v2.md` Finding #2) measured four skills over budget: `claude-issue-executor` is the largest violation (586L / ~6.7k tokens; well over the 500L hard line and the 5k-token target), and three more (`pr-review-packager` 471L/5.6k, `release` 474L/5.4k, `prepare-issue` 405L/5.2k) exceed the token target while staying under the line budget. `changelog` is at 87% (436L/4.3k) — leave alone unless it grows. Anthropic's progressive-disclosure pattern lifts worked examples and reference material into sidecar files (`example.md`, `criteria.md`, or named like `REFERENCE.md`), keeping SKILL.md focused on the routing description + execution protocol. The sidecar precedent already exists in this repo: `skills/check-plan/criteria.md` is a legitimate progressive-disclosure sidecar.

Requirements
- Lift content from each of the four over-budget SKILL.md files into one or more sidecar files under the same `skills/<name>/` directory until SKILL.md is **≤500 lines AND ≤5k estimated tokens**. Per-skill targets (per `findings-v2.md` Finding #2):
  - `claude-issue-executor`: target ≤300 lines / ≤3,500 tokens. Lift "Failure modes & recovery" + worked example. Currently 586L / ~6.7k tokens.
  - `pr-review-packager`: lift extensive worked examples and the branch-state matrices. Currently 471L / ~5.6k tokens.
  - `release`: lift extensive worked examples. Currently 474L / ~5.4k tokens.
  - `prepare-issue`: lift extensive worked examples. Currently 405L / ~5.2k tokens.
- Each sidecar must be **one level deep from SKILL.md** — Anthropic's rule "Keep references one level deep from SKILL.md". Sidecars may NOT reference other sidecars; they may only link back to SKILL.md or out-of-skill paths.
- Use the existing cohort sidecar convention: prefer `example.md` for worked examples (matches 17/19 skills today). If reference material is genuinely separate from worked examples (e.g. failure-modes / recovery for `claude-issue-executor`), introduce a named sidecar (`reference.md` or similar) and document the choice in the SKILL.md "Handoff" or equivalent section.
- Preserve all existing inline ADR links and cross-skill links in SKILL.md bodies. The Phase 1 description rewrite intentionally left bodies untouched; Phase 2 lifts content but does not change wording or workflow steps.
- No description changes (Phase 1 territory, shipped). No sidecar renames or `complete-milestone` / `milestone-summary` policy decisions (Phase 3 territory).

Acceptance criteria
- `python3 notes/skills-audit-2026-05-07/audit.py` reports `over_500_lines == 0` AND `over_5k_tokens_est == 0` across all 19 skills (i.e. all four over-budget skills are now under both thresholds, and the previously-passing 15 skills haven't regressed).
- No sidecar produced links to another sidecar (reference depth ≤1 per Anthropic). Verify by greping each new sidecar file for relative paths into `skills/*/` other than its own SKILL.md.
- No behaviour change: each touched skill still drives the same workflow end-to-end. Smoke test: run a typical end-to-end flow (`/resume` → `/prepare-issue` → `/claude-issue-executor` → `/pr-review-packager`) and confirm each skill activates and produces the same artefact shape as before.
- All four touched skills still pass the Phase 1 v2-rubric scoring (frontmatter description unchanged) — `awk -F, 'NR>1 && ($2!="yes" || $3!="yes" || $4!="yes" || $5!="yes")' notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv` returns empty.

Scope and constraints
- Primary folders to touch: `skills/claude-issue-executor/`, `skills/pr-review-packager/`, `skills/release/`, `skills/prepare-issue/` — SKILL.md bodies and any new sidecar files in those four directories only.
- Folders to avoid unless absolutely necessary: SKILL.md files for the other 15 skills (Phase 2 is scoped to over-budget only); SKILL.md frontmatter descriptions (Phase 1 territory, shipped); `skills/prd-normalizer/examples.md` rename and `complete-milestone` / `milestone-summary` orchestration-only policy (Phase 3 territory); `design/adr/`, `templates/`, `docs/`, `examples/`, `archive/`, `bin/`, `CLAUDE.md`, `notes/refactoring-ideas.md`, `notes/feature-ideas.md`.
- **Plan-mode is required** per the issue body's "Phases are independent" + ADR-006 plan-first rule. Phase 2 is mechanical-but-large; surface lift decisions (which sections lift to which sidecar; what the sidecar is named) before applying.
- Voice/structure-only — zero behaviour change. No skill workflow gains or loses a step. No description changes.
- Single PR for all four skills (matches Phase 1's single-PR shape). Intra-phase splitting creates half-cohort states.

Evaluation & testing requirements
- `python3 notes/skills-audit-2026-05-07/audit.py` after each commit — confirm `over_500_lines == 0` and `over_5k_tokens_est == 0` across all 19 skills, and no regressions in `desc_*` columns from Phase 1.
- `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json` exits 0 (sanity check that nothing broke check-plan's parser).
- Smoke check: invoke `/prepare-issue` (or any of the four touched skills) in a fresh session and confirm the SKILL.md still loads cleanly and routes correctly — no broken references after content lift.
- All existing tests must continue to pass (kit has no automated test runner — voice/structure changes covered by `audit.py` + smoke checks).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `notes/skills-audit-2026-05-07/findings-v2.md` (Finding #2 has the per-skill targets and lift hints)
   - `notes/skills-audit-2026-05-07/methodology-v2.md` (sidecar / progressive-disclosure rubric)
   - `notes/skills-audit-2026-05-07/skills-audit.csv` (auto-regenerated; current per-skill measurements)
   - the four target SKILL.md files: `skills/claude-issue-executor/SKILL.md`, `skills/pr-review-packager/SKILL.md`, `skills/release/SKILL.md`, `skills/prepare-issue/SKILL.md`
   - existing sidecar convention: `skills/check-plan/criteria.md` (precedent for progressive-disclosure sidecars in this repo)
   - any existing tests related to the modules you will change (none — kit has no automated test runner)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - per-skill: which sections lift to which sidecar file, and what the sidecar is named (`example.md` for examples, named sidecar for reference material)
   - new sidecar files to create (with proposed names and rough section outline),
   - existing SKILL.md bodies to modify (which sections deleted, what replacement reference link inserted),
   - verification plan: which `audit.py` columns confirm budget compliance per commit.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's Phase 2 scope (no Phase 3 work, no Phase 1 re-touching),
   - commit incrementally with messages referencing the issue (e.g. `refactor(skills/claude-issue-executor): lift failure-modes to reference.md (#84 Phase 2)`).
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed (with `audit.py` output table for the 4 touched skills),
   - any follow-up work needed for Phase 3 or later issues (Phase 3 is deferred to a separate session),
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
