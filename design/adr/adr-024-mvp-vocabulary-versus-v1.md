# ADR-024: MVP scoping vocabulary — neutral "In scope / Out of scope" headings

**Status:** accepted
**Date:** 2026-04-26

## Context

ADR-022 removed kit-self "v1" qualifiers because they became
misleading once the kit shipped v2.0.0 — "v1 of the kit is for new
projects only" reads as version-gated when no scope decision actually
changed at the v1→v2 boundary.

The same wording — "In v1 / Not in v1" — survives in the kit's
**MVP scoping framework** with a different meaning: there it refers
to the *target project's* first release, not the kit's version. It
appears throughout product surface:

- `templates/mvp-template.md` — section headings.
- `templates/readme-template.md` — `{{IN_V1_BULLETS}}` and
  `{{NOT_IN_V1_BULLETS}}` placeholders, plus rendered headings.
- `skills/prd-to-mvp/`, `skills/idea-to-prd/`,
  `skills/prd-normalizer/` — instructions and examples reference
  the headings throughout.
- `skills/issue-planner/` — uses the lists to validate proposed
  issue scope.
- `skills/workflow-docs/` — extracts the lists for generated
  documentation.
- `examples/projects/*/design/mvp.md` and
  `examples/projects/*/README.md` — concrete MVP docs use the
  headings.
- `generic-project-workflow.md` — the reference workflow uses the
  vocabulary in narrative form.

There were two real concerns with keeping "v1":

1. **Cosmetic confusion.** A reader who has just learned the kit is
   at v2 may pause when they open an MVP doc and see "In v1 / Not in
   v1." The two uses of "v1" mean different things, and the
   distinction is real but subtle.
2. **Project-shape mismatch.** "v1" assumes the target project
   uses a versioning model that matches the term. It fits SaaS apps
   and product-shaped work; it fits awkwardly for libraries (where
   `v1` already means a specific semver release), CLIs, internal
   tools, websites, refactors, infrastructure projects, and research
   code. The kit aims to be useful for the widest range of project
   shapes, and a heading that excludes half of them is a real cost.

A countervailing concern — the surface area of the change — was
real when the kit had shipped users and migration cost was a factor.
**As of this decision the kit has not yet shipped to external
users**, so backwards-compatibility shims are not required and the
migration cost is one-off rather than recurring.

## Options considered

### Option A: Keep "In v1 / Not in v1"

- Pros: no migration; vocabulary is stable and shared with downstream
  product practice; "v1" carries the "first cut, more later"
  connotation cleanly.
- Cons: cosmetic confusion with kit-self version language; excludes
  project shapes that don't use a versioning model; assumes
  product-shaped work.

### Option B: Rebrand to "In MVP / Not in MVP"

- Pros: makes the meaning explicit (it's the MVP scope); removes the
  version-shaped collision; the file is already named `mvp.md` so
  the heading reinforces the concept.
- Cons: "MVP" is product-team vocabulary; awkward fit for libraries,
  refactors, infrastructure, hobby projects, research code; slight
  filename/heading redundancy.

### Option C: Rebrand to "In scope / Out of scope"

- Pros: works across every project shape — apps, libraries, CLIs,
  internal tools, websites, refactors, documentation projects,
  research code; mirrors common decision-doc vocabulary; the kit's
  goal of widest applicability is best served by neutral phrasing.
- Cons: loses the temporal "first cut, more later" connotation that
  "v1" carries — recoverable in surrounding prose, the filename
  (`design/mvp.md`), and the skill name (`prd-to-mvp`).

### Option D: Rebrand to "Initial release / Deferred"

- Pros: explicit about the temporal axis.
- Cons: wordier; "Deferred" is softer than "Not in v1" — less
  decisive about things that are explicitly excluded; assumes a
  release model that not all projects use.

## Decision

Adopt **Option C — `In scope / Out of scope`** for the MVP scoping
framework's section headings, with one refinement: the filename
(`design/mvp.md`) and the skill name (`prd-to-mvp`) stay unchanged.
The "MVP" concept earns its keep at those layers and is stable; the
heading-level phrasing goes neutral so the document reads correctly
for every project shape.

The temporal "first cut, more later" signal is preserved in:

- The filename `design/mvp.md`.
- The skill name `prd-to-mvp`.
- The intro prose of the generated MVP doc, which still frames
  scope as "the first release" or "what ships first" depending on
  context.

This decision applies to the kit's product surface (templates,
skills, examples, reference workflow). Kit-self ADRs and docs are
already covered by ADR-022.

This decision **does not rename `design/mvp.md`** to a more neutral
filename. The filename is internal to the kit's convention, doesn't
appear in target projects' public READMEs, and renaming would ripple
into skill names (`prd-to-mvp` → `prd-to-scope`?) for negligible
benefit.

The kit has not yet shipped to external users, so no
backwards-compatibility shim is needed for old placeholder names.
The change is a single sweep across templates, skills, examples,
and the reference workflow.

## Consequences

- Templates rewritten:
  - `templates/mvp-template.md` — `### In v1` / `### Not in v1` →
    `### In scope` / `### Out of scope`. Guidance prose updated to
    keep the temporal signal in surrounding text.
  - `templates/readme-template.md` — placeholders renamed
    (`{{IN_V1_BULLETS}}` → `{{IN_SCOPE_BULLETS}}`,
    `{{NOT_IN_V1_BULLETS}}` → `{{OUT_OF_SCOPE_BULLETS}}`); rendered
    headings updated.
  - `templates/prd-template.md` — line that references "v1 is the
    MVP's job" reworded.
- Skills updated: `prd-to-mvp`, `idea-to-prd`, `prd-normalizer`,
  `issue-planner`, `workflow-docs` — instructions, validation
  logic, and worked examples updated to use the new headings.
- Example projects rebuilt: `examples/projects/kb-lookup/` and
  `examples/projects/slug-utils/` — `design/mvp.md`, `README.md`,
  PRD, and any in-project ADR/issue references rewritten to use
  the new headings.
- Top-level example walkthroughs updated:
  `examples/idea-only-example.md`, `examples/custom-prd-example.md`,
  `examples/standard-prd-example.md`.
- Reference workflow narrative updated:
  `generic-project-workflow.md`. References to "v1" that are
  *target-project domain examples* (e.g., a hypothetical issue
  titled "Remove deprecated v1 API endpoints") are kept — those
  are real product use cases the kit doesn't need to neutralise.
- Filenames stay: `design/mvp.md` and the `prd-to-mvp` skill
  name are unchanged.
- No backwards-compat shim. The kit has not shipped externally;
  any existing internal target projects can be rebuilt from the
  new templates.
- Easier going forward: the kit reads correctly for the widest
  range of project shapes; no project-type assumption baked into
  headings.
- One-off cost: a sweep across the surfaces listed above. Tracked
  via `notes/feature-ideas.md` entry #21.
