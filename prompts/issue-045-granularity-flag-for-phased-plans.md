You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project — software or otherwise — a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-036-granularity-control.md`
- Decision: Both `prd-to-mvp` and `/planning` accept `--granularity={coarse|standard|fine}`, default `standard` (5-8 phases); the choice is recorded in `build-out-plan.md` metadata so re-runs and downstream skills are consistent. Bands are targets not hard caps; the planning skill picks the actual count within the band and justifies it inline.

GitHub Issue:
- Title: Add --granularity flag for phased plans (ADR-036)
- Number: #45
- Milestone: none
- Labels: feature

Goal
Give first-time authors a sane default for phase count without forcing exact decomposition decisions, and keep example projects comparable across the kit.

Why it matters
ADR-032 introduces phases but leaves count to author judgment. Without a knob, decomposition varies project-to-project and the workflow guide cannot prescribe a default. A small three-tier knob gives `prd-to-mvp` and `/planning` a target band and lets the kit's worked examples and docs all rest on the same shape.

Requirements
- Add `--granularity={coarse|standard|fine}` to `skills/prd-to-mvp/SKILL.md` (argument parsing, default behaviour, propagation into the rendered `build-out-plan.md`).
- Add the same flag to `skills/planning/SKILL.md` (per ADR-031), with consistent semantics.
- Default tier: `standard` (5–8 phases).
- Tier bands: `coarse` (1–3 phases), `standard` (5–8), `fine` (8–12). Bands are *targets*, not hard caps; the planning skill picks the actual count and justifies it inline.
- Record the granularity choice in `build-out-plan.md` metadata so a re-run without `--granularity` reuses the prior choice and downstream skills can read it.
- Document the knob in `docs/workflow-guide.md` with an explicit anti-pattern warning ("don't tune granularity to dodge scope decisions").

Acceptance criteria
- Running each tier (`--granularity=coarse`, `=standard`, `=fine`) produces a `build-out-plan.md` whose phase count sits within the documented band.
- Re-running without `--granularity` reads the recorded choice from the existing `build-out-plan.md` metadata and reuses it (no surprise tier flips).
- The workflow guide describes when each tier fits and explicitly warns against tuning granularity to avoid fixing scope.

Scope and constraints
- Primary folders to touch: `skills/prd-to-mvp/SKILL.md`, `skills/planning/SKILL.md`, `templates/build-out-plan-template.md` (add the metadata field), `docs/workflow-guide.md`.
- Folders to avoid unless absolutely necessary: `Design/adr/` (do not edit accepted ADR-036), `bin/`, `examples/projects/` (the worked examples are reference data; refresh only if the metadata shape requires it), `prompts/` (other than this issue's own prompt).
- Bands and the default must match ADR-036's Decision verbatim — `coarse` 1–3, `standard` 5–8 (default), `fine` 8–12. Do not silently use the ADR's Context-section figures (which mention 3–5 for coarse) — the Decision is canonical.
- Do not introduce a `--phases=N` exact-count flag (rejected as Option B in the ADR). The three-tier knob is the contract.
- Re-run reuse must be a *read* of `build-out-plan.md` metadata, not a flag passed through some other channel — the file is the canonical store.

Evaluation & testing requirements
- Demonstrate each tier: run the skills with `--granularity=coarse` / `=standard` / `=fine` (or simulate by walking the protocol against a fixture PRD) and confirm phase counts fall in 1–3 / 5–8 / 8–12 respectively, with an inline justification line in each generated plan.
- Demonstrate re-run reuse: re-run `prd-to-mvp` (and `/planning`) without `--granularity` against a build-out-plan.md that records `coarse`, and confirm the second run keeps `coarse` rather than reverting to the default `standard`.
- Verify the metadata field shape is read-back-safe: an explicit `--granularity` flag on a re-run *overrides* the stored value (override > stored > default).
- Verify the workflow-guide anti-pattern warning is present and points the reader at the underlying scope decision rather than the knob.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-036-granularity-control.md`
   - `Design/adr/adr-031-deeper-planning-workflow.md` and `Design/adr/adr-032-implementation-phases.md` (parents — depended on)
   - existing modules under `skills/prd-to-mvp/`, `skills/planning/`, `templates/build-out-plan-template.md`, `docs/workflow-guide.md`
   - any existing tests related to the modules you will change
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - new files or modules to create,
   - existing files to modify,
   - key functions or structures (especially the metadata-read precedence: flag > stored > default),
   - your verification or test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue (e.g. "feat(scope): add thing (ADR-036, #45)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
