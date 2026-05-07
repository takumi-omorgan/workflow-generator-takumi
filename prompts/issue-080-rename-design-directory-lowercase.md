You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.

ADR:
- File: `design/adr/adr-045-rename-design-directory-lowercase.md`
- Decision: Rename `design/` → `design/` across the kit, the convention it teaches target projects, and inside the 16 affected accepted ADR bodies. Supersedes ADR-005 on the directory-casing question only — ADR-005's substantive decision (generate core docs into the target repo) stands.
- File: `design/adr/adr-044-mechanical-rewrite-immutability-exception.md`
- Decision: Mechanical path-string rewrites are an explicit exception to the "never edit accepted ADRs in place" rule, qualifying when (1) deterministic string substitution, (2) no sentence meaning changes, (3) no altered decisions or rationale, (4) no added or removed requirements, (5) uniform application, and (6) scriptable and reproducible. This ADR provides the authority for the 16-ADR-body rewrite scoped here.
- File: `design/adr/adr-005-documentation-and-template-architecture.md`
- Decision: Generate the core workflow documents and templates directly into the target repository (including ADRs and the AI summary). Superseded on casing only by ADR-045.

GitHub Issue:
- Title: Rename design/ → design/ kit-wide for root-directory casing consistency (ADR-045, supersedes ADR-005)
- Number: #80
- Milestone: none
- Labels: feature

Goal
Rename `design/` → `design/` across the kit (~176 files, ~500+ path-string occurrences) including inside the 16 accepted ADR bodies that cite `design/`. Pure case fix — preserves the directory's current breadth. Supersedes ADR-005 on the casing question only; ADR-005's substantive decision stands.

Why it matters
`design/` is the only TitleCase top-level directory in a kit where every other root directory is lowercase (`docs/`, `notes/`, `skills/`, `templates/`, `bin/`, `prompts/`, `examples/`, `archive/`). The capitalised root *files* (`README.md`, `LICENSE`, `CHANGELOG.md`, `CLAUDE.md`) have well-known external anchors; `design/` has none. Every new target-project install inherits the inconsistency — the paper-cut compounds. A pre-ADR `/clarify` pass settled four open questions: ship the rename (consistency worth the cost), pure case fix not semantic restructure, authorise mechanical ADR-body rewrite via ADR-044, manual `git mv` snippet for migration (no new tooling). PR #79 (now merged) accepted ADR-044 establishing the mechanical-rewrite exception used by this issue.

Requirements
- Rename `design/` → `design/` via a single `git mv` so git tracks it as a rename, not a delete-and-add.
- Rewrite every `design/` path-string occurrence to `design/` across `CLAUDE.md`, `README.md`, `CHANGELOG.md`, `docs/**/*.md`, `templates/**/*.md`, all 19 `skills/*/SKILL.md` plus sibling `example.md` / `examples.md` / `criteria.md`, `bin/lib/check-plan-eval.sh` and any other `bin/` scripts, `examples/projects/**/*`, `archive/**/*` (mechanical only — historical content otherwise untouched), and `notes/**/*`.
- Rewrite path strings inside the 16 accepted ADR bodies that cite `design/` (ADR-001, 005, 008, 009, 018, 022, 023, 024, 025, 026, 027, 028, 031, 032, 033, 035, 037, 042) under ADR-044's mechanical-rewrite exception. Verify each rewrite satisfies ADR-044's six criteria before staging.
- Flip ADR-005's status line to `**Status:** superseded by ADR-045` (status-line edit only — outside the immutability rule).
- Flip ADR-045's status from `proposed` to `accepted`.
- Run `bin/sync-adr-index` after the ADR status changes; commit the regenerated `design/adr/README.md` (note the new path) alongside.
- Add a Breaking Changes entry to `CHANGELOG.md` for the rename version including the migration snippet `git mv Design design && grep -rl 'design/' . | xargs sed -i '' 's|design/|design/|g'`.

Acceptance criteria
- No `design/` path string remains in any current doc (verify: `grep -r "design/" --exclude-dir=.git --exclude-dir=.claude` returns empty); `archive/` historical content may retain unchanged occurrences if the surrounding text describes a historical state.
- ADR-005 status reads `superseded by ADR-045`; ADR-045 status reads `accepted`.
- All 16 ADR bodies that previously cited `design/` now cite `design/`, every occurrence rewritten uniformly per ADR-044's mechanical criteria (1)–(6); no editorial-meaning changes.
- `bin/sync-adr-index --check` exits 0; `design/adr/README.md` (new path) reflects ADR-005 superseded and ADR-045 accepted.
- `bin/check-plan --criteria-set adr` passes against both ADR-005 and ADR-045 after the rewrite.
- All skills load and run unchanged. Smoke test: invoke `/resume`, `/prepare-issue`, `/adr-writer`, `/release` against `examples/projects/kb-lookup` and confirm no path-resolution failures.
- `CHANGELOG.md` carries the Breaking Changes entry with the migration snippet.
- The PR description satisfies ADR-044's procedural requirements: states (a) it invokes ADR-044, (b) the exact transformation rule (`design/ → design/`), (c) the runnable command applied (the `sed` invocation above), and (d) the list of affected ADR numbers.

Scope and constraints
- Primary folders to touch: `design/` (renamed to `design/`) and every directory listed in Requirements (root files, `docs/`, `templates/`, `skills/`, `bin/`, `examples/`, `archive/`, `notes/`).
- Folders to avoid unless absolutely necessary: `.git/`, `.claude/skills/` (gitignored symlinks managed by `~/dotfiles/claude-config/bin/link-skills`), any external dependencies.
- Mechanical only. Per ADR-044 criteria (1)–(6), no editorial-meaning changes inside ADR bodies. If any rewrite would force a re-reading of *what* an ADR decided or *why*, stop and surface — that's a supersession, not a rewrite.
- Single PR. Splitting the rename across multiple PRs creates a half-renamed working tree and breaks intermediate skill invocations. The PR is large but cohesive.
- No tooling shipped. Migration is a documented snippet in CHANGELOG, not a script.
- Plan-first per ADR-006. Propose a batched plan: kit code → root files → docs → templates → skills → ADR bodies → CHANGELOG → index regen → status flips. Review can spot-check each batch.
- Plan-mode rhythm per ADR-039. This session is **clearly significant** (3+ files, edits all 19 SKILL.md, edits templates/, edits bin/, edits 16 ADR bodies). Request plan-mode entry before proposing the plan.

Evaluation & testing requirements
- Run `bin/sync-adr-index --check` post-rename and confirm exit 0.
- Run `bin/check-plan --criteria-set adr --input design/adr/adr-005-documentation-and-template-architecture.md` and `bin/check-plan --criteria-set adr --input design/adr/adr-045-rename-design-directory-lowercase.md`; confirm both pass deterministic criteria.
- Smoke-test the renamed kit against `examples/projects/kb-lookup`: invoke `/resume`, `/prepare-issue 1`, `/adr-writer`, `/release` and confirm no path-resolution failures or stale `design/` references in skill output.
- All existing tests must continue to pass (kit is docs-only; verification is the manual checks above).
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-045-rename-design-directory-lowercase.md`
   - `design/adr/adr-044-mechanical-rewrite-immutability-exception.md` (its six criteria define what counts as mechanical)
   - `design/adr/adr-005-documentation-and-template-architecture.md` (the superseded ADR)
   - `bin/sync-adr-index` and `bin/lib/check-plan-eval.sh` (paths to update inside scripts)
   - existing `docs/workflow-guide.md` and `docs/skills.md` for path-reference patterns
2. Propose a step-by-step PLAN that includes:
   - the branch name (suggested: `rename-design-directory-lowercase`),
   - the ordered batches of files to touch and the commit-per-batch plan,
   - the exact `git mv` and `sed` commands you'll run,
   - which 16 ADR files will be rewritten and a sample diff confirming the rewrite is mechanical (criteria 1–6),
   - the ADR-005 and ADR-045 status flips and where they fall in the commit sequence,
   - the CHANGELOG entry wording,
   - your verification plan (the four `bin/check-plan` / `bin/sync-adr-index` / smoke-test commands above).
3. Wait for my approval of the plan before making any edits. The session is clearly significant per ADR-039 — request plan-mode entry first.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope (no semantic restructures, no opportunistic cleanups inside ADR bodies),
   - commit per batch with messages referencing both ADRs and the issue (e.g. `refactor(skills): rename design/ → design/ in skills/ (ADR-044, ADR-045, #80)`),
   - the PR description must enumerate ADR-044 invocation, exact transformation rule, runnable command, and affected ADR numbers (per ADR-044's Consequences).
5. At the end, provide an evaluation summary:
   - what changed (grouped by directory),
   - verification steps performed (paste exit codes for `bin/check-plan` runs, `bin/sync-adr-index --check`, and smoke-test output),
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
