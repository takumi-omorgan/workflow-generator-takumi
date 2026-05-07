You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `design/adr/`.

ADR:
- File: `design/adr/adr-026-kit-versioning-policy.md`
- Decision: Document explicit semver rules for the kit's
  template-and-skill-shaped "API" — what counts as MAJOR / MINOR /
  PATCH for a product whose contract is files installed into target
  projects rather than imported code.

GitHub Issue:
- Title: Document kit semver versioning policy (ADR-026)
- Number: #30
- Milestone: v3.0.0 — kit hygiene and licensing
- Labels: docs

Goal
Write an ADR that defines what triggers each semver bump for the
kit. The classifications must be mechanical enough for `/changelog`
and `/release` to apply without judgment, and clear enough for
downstream users to know what an upgrade requires of them.

Why it matters
The v3 cut surfaced a real classification question: does ADR-024's
placeholder rename count as breaking? The standard semver intuition
assumes an imported library, which the kit is not. Without a written
policy, the question is relitigated every release. With one,
classifications are mechanical and downstream users get an explicit
upgrade contract.

Requirements
- Write `design/adr/adr-026-kit-versioning-policy.md` covering:
  - **Context:** the kit's "API" surface (templates, placeholders,
    skill-parsed headings, marker fences, installer flags); why
    standard semver intuition needs adaptation; the v3 trigger
    that motivated the ADR.
  - **Options considered:**
    - Option A: don't write a policy, decide case-by-case.
    - Option B: write an explicit policy ADR (recommended).
    - Option C: adopt SemVer.org by reference plus a tooling
      adaptation.
  - **Decision: Option B**, with a classification table:
    - **MAJOR triggers:** placeholder rename in any template,
      parser-relevant heading rename, marker fence rename/removal,
      removed skill/template/installer flag, default-behaviour
      change in installer, canonical-layout change.
    - **MINOR triggers:** new skill, new template, new installer
      flag (backwards-compatible default), new optional
      placeholder, new ADR-status value, new section behind a
      marker fence.
    - **PATCH triggers:** doc fixes, internal refactors, ADR
      additions/status flips, bug fixes for unambiguously-wrong
      behaviour, examples-only updates.
  - **Edge cases and judgment calls:** decorative heading renames
    (default MAJOR if anything outside the kit might depend on the
    old name); output-changing bug fixes (MINOR or MAJOR vs PATCH
    depends on whether the previous behaviour was documented);
    supersession status flips (PATCH; the supersession ADR
    classifies behavioural changes separately); deprecation
    sequencing (deprecate in a MINOR with a removal target;
    removal is a MAJOR bump).
  - **Pre-1.0 exception clause:** the kit is past 1.0, so the
    standard pre-1.0 SemVer permission to make breaking changes
    in MINOR releases does **not** apply — flag for completeness.
  - **Consequences:** changelog/release skills can apply the rules
    mechanically; downstream users get a contract; v3 is correctly
    classified as MAJOR (validates against ADR-024); the policy
    itself may need future revisions when the kit grows new
    artifact types.

Acceptance criteria
- ADR-026 file exists, status `accepted`.
- The policy explicitly classifies the v3 release as MAJOR
  (validates against ADR-024's placeholder + heading rename).
- Each classification (MAJOR / MINOR / PATCH) is documented with
  concrete trigger examples a future release author can match
  against without judgment.
- Edge-case section covers the realistic ambiguities (decorative
  renames, output-changing bug fixes, supersession flips,
  deprecation sequencing).
- ADR index reflects ADR-026 as accepted.

Scope and constraints
- Primary folders to touch: `design/adr/`.
- No code changes. Pure documentation.
- Out of scope: amending `/changelog` or `/release` to enforce the
  policy automatically. ADR-026 sets the contract; tool integration
  is a future follow-up if needed.
- Do not bake project-specific examples into the policy — the rules
  are about the kit's shape, not any particular ADR.

Evaluation & testing requirements
- After commit, walk through the v3 release classification using the
  policy: ADR-024's placeholder rename → MAJOR (matches
  "placeholder rename" trigger), confirms the policy is internally
  consistent.
- Walk through a hypothetical "added a new skill" case → MINOR
  (matches "new skill" trigger).
- Walk through a hypothetical "fix typo in CLAUDE.md template" case →
  PATCH (matches "doc fixes" trigger).
- All existing tests continue to pass (none affected).

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-024-mvp-vocabulary-versus-v1.md` (for the
     classification example),
   - `design/adr/adr-016-changelog-and-release-notes-skill.md` and
     `design/adr/adr-017-release-skill.md` (for how the policy
     ties into existing release tooling),
   - `templates/adr-template.md` (for structure).
2. Propose a short, step-by-step PLAN:
   - the ADR outline (sections + bullets per section),
   - the classification-table content,
   - the edge-case examples,
   - the integration points with `/changelog` / `/release`.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - one commit for the ADR; tag it with `ADR-026, #30`.
5. At the end, provide an evaluation summary:
   - the rendered ADR (or a structural summary),
   - the v3-classification walkthrough as validation,
   - any follow-up work (tool integration is the obvious one),
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.

---

**Retrospective note (2026-04-26):** This prompt is the canonical
session brief that should have driven this work. The implementation
was performed interactively in a session that did not follow the
formal `/prepare-issue` → `/claude-issue-executor` flow. This file
is preserved as the audit trail and as an exemplar for future
policy ADRs.
