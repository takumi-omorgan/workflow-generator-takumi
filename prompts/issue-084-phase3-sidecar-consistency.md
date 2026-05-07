You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.
- This is **Phase 3 of issue #84**, the final phase. Phase 1 (description rewrites) shipped in PR #86. Phase 2 (body slimming) shipped in PR #87 — all 19 cohort skills now under Anthropic's L2 budget. Phase 3 ships the cohort-consistency cleanup that closes the issue.

ADR:
- none — same reasoning as Phases 1 and 2: this refactor changes internal kit style only, not a target-project-facing convention. The CLAUDE.md "never edit accepted ADRs in place" rule applies to ADR bodies, not skill sidecar filenames or docs/skills.md sections.

GitHub Issue:
- Title: Apply 2026-05-07 skills-audit recommendations across the cohort
- Number: #84
- Milestone: none
- Labels: docs, refactor

Goal
Phase 3 of issue #84: cohort-consistency cleanup. Rename `skills/prd-normalizer/examples.md` → `example.md` (one drift; 16 of 17 sidecar-bearing skills use the singular), and decide cohort policy on the two skills currently without a worked-example sidecar (`complete-milestone`, `milestone-summary`) — either add `example.md` to each (matches the 17/19 cohort default) or document in `docs/skills.md` why they're orchestration-only and don't need one. Voice/structure-only; zero behaviour change. After this PR ships, issue #84 closes.

Why it matters
The 2026-05-07 audit (`notes/skills-audit-2026-05-07/findings-v2.md` Findings #3 + #4) flagged two cohort-consistency drifts that survive Phases 1 and 2: (a) `prd-normalizer` is the only skill whose worked-example sidecar uses the plural form `examples.md` — every other sidecar-bearing skill uses `example.md` (single canonical worked example, matching Anthropic's progressive-disclosure convention seen in the existing 16-skill majority); (b) `complete-milestone` and `milestone-summary` are the only two skills in the 19-cohort with no worked-example sidecar at all, with no documented reason. Both are routing-orchestration skills (chain other skills; thin direct-action surface), so "no example" may be the right call — but the reason should be documented so future audits don't re-flag them, and so newcomers reading the cohort can tell the omission from a drift. After Phase 1's description-uniformity pass and Phase 2's budget-uniformity pass, this consistency pass closes the cohort cleanup.

Requirements
- Rename `skills/prd-normalizer/examples.md` → `skills/prd-normalizer/example.md` via `git mv` (preserves blame). Update any internal references that point at the old plural filename: search `skills/prd-normalizer/SKILL.md` for `examples.md` references; search `docs/`, `notes/skills-audit-2026-05-07/findings-v2.md`, and any other docs/notes that might link to the old name. Adjust accordingly.
- Decide cohort policy on `complete-milestone` and `milestone-summary` orchestration-only-ness. Two viable options:
  - **Option A (matches 17/19 cohort default):** Author a worked `example.md` for each. Each example shows a typical session walkthrough — for `complete-milestone`, the close-out flow (audit → close → optional release chain); for `milestone-summary`, generating the retrospective doc from `gh` + ADR sources. Length matches the cohort norm (~80–150 lines, similar shape to existing examples).
  - **Option B (document the exception):** Add a short section to `docs/skills.md` titled "Skills without a worked-example sidecar" (or similar) listing both skills and the reason — they're routing-orchestration, the SKILL.md execution protocol is itself the worked walkthrough. Cross-link from each skill's SKILL.md "Handoff" or equivalent section back to the docs/skills.md note so the omission is discoverable from inside the skill.
- Pick one of A or B explicitly during plan-mode. Both options are mechanically valid; the choice is a cohort-aesthetic call (uniformity vs. accurate documentation). Recommend B (less ceremony, accurate to the skills' actual shape, no risk of stale invented examples), but defer to the user.
- No SKILL.md frontmatter description changes (Phase 1 territory; shipped). No body-slimming or sidecar-restructuring (Phase 2 territory; shipped).

Acceptance criteria
- `skills/prd-normalizer/example.md` exists; `skills/prd-normalizer/examples.md` does not.
- All references to the old plural filename in tracked files are updated to the singular form. Verify: `grep -rn 'prd-normalizer/examples.md' .` returns zero hits (excluding `.git/` and any historical eval/audit files that name it as a then-current path).
- For Option A: `skills/complete-milestone/example.md` and `skills/milestone-summary/example.md` both exist and follow the cohort example shape. Smoke test: each new file is one-level-deep (no references to other sidecars), under ~150 lines, and references back to its own `SKILL.md`.
- For Option B: `docs/skills.md` has a section that names both `complete-milestone` and `milestone-summary` with the orchestration-only reason. Cross-links from each affected SKILL.md are present and resolve.
- `python3 notes/skills-audit-2026-05-07/audit.py` reports `over_500_lines == 0` and `over_5k_tokens_est == 0` across all 19 skills (Phase 2's budget pass survives intact).
- `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json` exits 0 (parser sanity).
- v2-rubric still passes for all 19: `awk -F, 'NR>1 && ($2!="yes" || $3!="yes" || $4!="yes" || $5!="yes")' notes/skills-audit-2026-05-07/skills-audit-judgment-v2.csv` returns empty.

Scope and constraints
- Primary folders to touch: `skills/prd-normalizer/` (rename one file), and EITHER `skills/complete-milestone/` + `skills/milestone-summary/` (add `example.md` to each — Option A) OR `docs/skills.md` + light cross-links from `skills/complete-milestone/SKILL.md` and `skills/milestone-summary/SKILL.md` (Option B). Pick one before any edits.
- Folders to avoid unless absolutely necessary: SKILL.md frontmatter `description:` fields (Phase 1 territory, shipped), the over-budget skills' bodies and their new sidecars from Phase 2 (Phase 2 territory, shipped — `claude-issue-executor/{plan-mode,reference}.md`, `pr-review-packager/reference.md`, `release/reference.md`, `prepare-issue/reference.md` are not Phase 3 concerns), `design/adr/`, `templates/`, `examples/`, `archive/`, `bin/`, `CLAUDE.md`, `notes/refactoring-ideas.md`, `notes/feature-ideas.md`.
- Single PR for both decisions (rename + policy). They're independent acceptance criteria but ship together as the cohort-consistency closeout.
- Voice/structure-only — zero behaviour change. No skill workflow gains or loses a step. No description changes.
- Plan-mode is required per ADR-006 plan-first. The Option A vs Option B choice should surface as the headline plan decision before any edits.

Evaluation & testing requirements
- `python3 notes/skills-audit-2026-05-07/audit.py` after each commit — confirm `over_500_lines == 0` and `over_5k_tokens_est == 0` across all 19, and no regressions in `desc_*` columns from Phase 1.
- `grep -rn 'prd-normalizer/examples.md' .` returns zero hits in tracked files after the rename.
- `bin/check-plan --criteria-set adr --input design/adr/adr-046-ai-pr-review-module.md --format json` exits 0 (parser sanity).
- For Option A: spot-check each new `example.md` for depth-1 (`grep -nE '\]\([^)]*(reference|plan-mode|criteria|examples?)\.md' skills/{complete-milestone,milestone-summary}/example.md | grep -v '\](SKILL\.md)'` returns empty).
- For Option B: spot-check `docs/skills.md` cross-links resolve, and the SKILL.md back-links point at the right anchor.
- All existing tests must continue to pass (kit has no automated test runner — voice/structure changes covered by `audit.py` + manual verification).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `notes/skills-audit-2026-05-07/findings-v2.md` (Findings #3 + #4 have the cohort-consistency rationale)
   - `skills/prd-normalizer/examples.md` (the file being renamed)
   - `skills/prd-normalizer/SKILL.md` (check for any `examples.md` reference inside)
   - `skills/complete-milestone/SKILL.md` and `skills/milestone-summary/SKILL.md` (the two no-sidecar skills)
   - `docs/skills.md` (target for Option B)
   - one or two existing `example.md` files for the cohort norm if Option A is picked (e.g. `skills/audit-milestone/example.md` matches the milestone-cluster shape closest to the targets)
   - any existing tests related to the modules you will change (none — kit has no automated test runner)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - **The Option A vs Option B decision**, with your recommendation and reasoning. This is the headline plan call.
   - The `git mv` for the rename.
   - The list of files that reference the old plural path and the corresponding edits.
   - For Option A: per-file outline of each new `example.md` (which existing example to mirror, ~length, what session shape).
   - For Option B: the docs/skills.md section text and the cross-link wording in each affected SKILL.md.
   - Verification plan: which audit.py columns / grep checks confirm each acceptance criterion per commit.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on Phase 3 scope (no Phase 1 re-touching, no Phase 2 sidecar edits),
   - commit incrementally with messages referencing the issue (e.g. `refactor(skills/prd-normalizer): rename examples.md to example.md (#84 Phase 3)`).
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work (Phase 3 closes #84; post-merge bookkeeping flips entry #9 to fully `shipped-#PR`),
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
