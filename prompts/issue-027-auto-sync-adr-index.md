You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `Design/adr/`.

ADR:
- File: `Design/adr/adr-023-auto-sync-adr-index.md`
- Decision: Build `bin/sync-adr-index` (regenerator script) plus
  marker-fenced `Design/adr/README.md`, plus skill integrations into
  `adr-writer`, `claude-issue-executor`, `pr-review-packager`, and
  `release`. Defer the optional git pre-commit hook (Option C).

GitHub Issue:
- Title: Auto-sync ADR index in Design/adr/README.md (ADR-023)
- Number: #27
- Milestone: v3.0.0 — kit hygiene and licensing
- Labels: feature, infra

Goal
Eliminate ADR-index drift by introducing a regenerator script and
wiring it into the four ADR-touching skills so the index table stays
in sync with `Design/adr/adr-*.md` files automatically.

Why it matters
The index has drifted repeatedly — at one point listed only ADR-006
entries while the directory contained 21 ADRs. Status transitions
cause similar drift. Drift hurts discoverability and adds an
easy-to-forget second-edit step on every ADR change. Making the
sync automatic structurally eliminates the drift class for
skill-driven flows.

Requirements
- Write `bin/sync-adr-index` (bash, no runtime deps). Behaviour:
  - Scan `Design/adr/adr-*.md`. Sort by ADR number (numeric, padded).
  - Parse title from `# ADR-NNN: ...` headline.
  - Parse status from first `**Status:**` line. Render any
    `[ADR-NNN](path)` link in the status as a plain `ADR-NNN`
    reference.
  - Rewrite the region between marker fences
    `<!-- adr-index:start -->` and `<!-- adr-index:end -->` in
    `Design/adr/README.md`. Preserve everything outside the fence.
  - Idempotent. Exit 0 on no-op, 1 if changes were written.
  - Support `--check` for CI/preflight: exit 1 if drift is detected,
    do not modify the file.
  - Set executable bit (`chmod +x`).
- Add the marker fences to `Design/adr/README.md`. Wrap the existing
  index table; add a one-paragraph note above the fence explaining
  the table is generated and edits inside will be overwritten.
- Wire the script into the four skills:
  - `skills/adr-writer/SKILL.md`: run after the batch as the final
    step before commit. Add a self-check item.
  - `skills/claude-issue-executor/SKILL.md`: run before any commit
    that includes a file under `Design/adr/adr-*.md`. Add a bullet
    to the Commit model section.
  - `skills/pr-review-packager/SKILL.md`: include `--check` in the
    pre-PR self-check; refuse if drift is detected.
  - `skills/release/SKILL.md`: include `--check` in prerequisites;
    refuse on drift.
- Update `bin/install-workflow-kit` to copy `bin/sync-adr-index` into
  target projects' `.claude/bin/sync-adr-index`. Preserve executable
  bit. Idempotent without `--force`.
- Update `notes/feature-ideas.md` entry #20 status to `shipped` with
  the ADR link.

Acceptance criteria
- `bin/sync-adr-index --check` exits 0 on a fresh run after manual
  index editing matches the script's output.
- Running `bin/sync-adr-index` on a state with new/modified ADRs
  rewrites only the fenced region; surrounding prose untouched.
- All four skills' `SKILL.md` files document the sync step.
- The installer copy step preserves the executable bit and skips on
  re-run unless `--force`.
- ADR-023 is `accepted` and the ADR index reflects that.
- Marker fences in `Design/adr/README.md` are intact.

Scope and constraints
- Primary folders to touch: `bin/`, `Design/adr/`, `skills/`,
  `notes/`.
- Folders to avoid: `templates/`, `examples/`, anything not directly
  involved in ADR-index workflow.
- Bash 3.2+ compatibility (macOS default). No GNU-only flags. Use
  `awk` carefully — macOS `awk` does not handle multi-line strings
  via `-v`; prefer a temp-file approach for table content.
- Do not introduce a git pre-commit hook (deferred per ADR-023
  Option C).

Evaluation & testing requirements
- Verify the script is idempotent: run twice, second run exits 0.
- Verify `--check` mode: with the file in sync, exits 0; with drift,
  exits 1 and prints a useful message.
- Verify each skill's documentation mentions the sync step.
- Verify the installer copy works end-to-end on a scratch target
  directory.
- All existing tests continue to pass.
- Manual verification is acceptable for the script (no test runner
  for shell in this repo today).

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-023-auto-sync-adr-index.md`
   - existing `Design/adr/README.md` and a couple of ADRs to verify
     the headline / status format
   - the four skills' current `SKILL.md` files
   - `bin/install-workflow-kit`
2. Propose a short, step-by-step PLAN:
   - script structure and key parsing rules,
   - marker-fence placement in `Design/adr/README.md`,
   - exact SKILL.md insertions for each of the four skills,
   - installer change,
   - test cases for verification.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - one logical commit per concern (script, fences, skill wires,
     installer),
   - each commit references ADR-023 and #27.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed (idempotency, `--check`),
   - any follow-up work for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.

---

**Retrospective note (2026-04-26):** This prompt is the canonical
session brief that should have driven this work. The implementation
was performed interactively in a session that did not follow the
formal `/prepare-issue` → `/claude-issue-executor` flow. This file
is preserved as the audit trail and as an exemplar for future
infrastructure-flavoured issues.
