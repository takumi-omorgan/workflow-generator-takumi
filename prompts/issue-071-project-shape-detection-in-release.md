You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-042-project-shape-detection-in-release.md`
- Decision: Adopt Option A — add project-shape detection to `/release`'s preflight, with operator override.

GitHub Issue:
- Title: Add project-shape detection to /release for non-product projects (ADR-042)
- Number: #71
- Milestone: v3.4.0 - eval baseline fixes
- Labels: feature

Goal
`/release` should match the project's actual shape automatically, with override flags for borderline cases — turning the workflow-agnostic claim from a doc-level reframing into a structural enforcement point in the release surface.

Why it matters
Research-tracker explicitly disclaimed being a product, yet `/release` still produced product-shaped notes ("first tagged release of …"). The kit's claim to be workflow-agnostic loses credibility every time the release skill does this. Closes F26 (silent v0.1.0 + product-framing leak on non-product projects) — the strongest ADR-028-leakage signal in the release surface across the v3.3.0 baseline eval.

Requirements
- Implement detection signals in `skills/release/SKILL.md` preflight: PRD/normalized-PRD language scan ("not [shipping|building] a product" / "workflow" / "folder of markdown"), build-out-plan Build strategy ("no compile / build / deploy step"), success-criteria shape (user-outcome vs test-result), repo-root package manifest absence (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `Gemfile`, `requirements.txt`).
- Two-or-more signal threshold triggers the non-product code path; document the threshold in SKILL.md.
- Add a non-product release-body template variant with the workflow-shaped clarifier banner from ADR-042's Decision section (the "This is a workflow tag for documentation drift-tracking…" copy).
- Add `--force-product-shape` flag for override (forces standard product framing on a project the heuristic flagged).
- Add `--force-workflow-shape` flag for symmetric opt-in (forces workflow framing on a project the heuristic did not flag).
- Make the canonical signal list in `skills/release/SKILL.md` the single source of truth; cross-reference from `docs/workflow-guide.md`.
- Add a worked example to `skills/release/example.md` showing the workflow-shape path.

Acceptance criteria
- `/release` on a project matching ≥2 non-product signals emits the workflow-shaped clarifier without operator action.
- `/release --force-product-shape` overrides detection and produces standard product framing.
- `/release --force-workflow-shape` opts into workflow framing on a project that did not trip detection.
- The signal list in SKILL.md is exhaustive and matches the workflow-guide cross-reference (no drift between the two surfaces).
- A worked example demonstrates each path (product, auto-detected workflow, both override flags).

Scope and constraints
- Primary folders to touch: `skills/release/`, `docs/workflow-guide.md` (cross-reference only).
- Folders to avoid unless absolutely necessary: other skills (extending detection to `/changelog` or `/audit-milestone` is explicitly deferred per ADR-042 Consequences), `design/adr/` (never edit accepted ADRs in place), `templates/` (no installer changes needed for this issue).
- Detection is spec-level: documented in `skills/release/SKILL.md` and executed by the skill itself. Do not add a `bin/` script for detection unless the implementation genuinely calls for one — ADR-042 explicitly leaves a shared cross-skill helper as deferred. Per CLAUDE.md, keep the kit lightweight; no premature automation.

Evaluation & testing requirements
- Verify the four detection signals fire correctly on at least one fixture matching ≥2 signals (the v3.3.0 baseline eval's `research-tracker` fixture is the canonical one — its PRD has explicit "I'm not shipping a product" language, build-out plan has "no compile / build / deploy step", success criteria are user-outcomes, repo root has no package manifest — should trigger 4/4 signals).
- Verify a product-shape project (e.g. the kit itself, or any fixture with a `package.json` / `pyproject.toml`) produces standard framing.
- Verify both override flags work end-to-end: `--force-product-shape` on a workflow-detected project, `--force-workflow-shape` on a product-detected project.
- Run `/check-plan` (or `bin/check-plan --criteria-set <type> --input <path>`) against the modified `skills/release/SKILL.md` and any new content under `skills/release/example.md` to confirm structural coherence.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-042-project-shape-detection-in-release.md`
   - `design/adr/adr-028-workflow-agnostic-framing.md` (the framing this enforces)
   - `design/adr/adr-017-release-skill.md` (the skill scope being amended)
   - `skills/release/SKILL.md` and `skills/release/example.md` (current surface)
   - `docs/workflow-guide.md` (for the cross-reference target)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - key functions or structures,
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits. This is **significant per ADR-039** — plan mode is required.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue
     (e.g. "feat(release): add project-shape detection (ADR-042, #71)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
