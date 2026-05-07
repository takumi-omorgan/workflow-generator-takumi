You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `design/adr/`.

ADR:
- File: `design/adr/adr-027-prd-template.md`
- Decision: Ship `templates/prd-template.md` mirroring
  `prd-normalizer`'s 11 canonical fields one-to-one, so users can
  draft a PRD offline (by hand or via any external LLM) and hand
  the result to `prd-normalizer` as a near-pass-through. The
  template is **model-agnostic** — no specific LLM is named in the
  template body or directive contexts.

GitHub Issue:
- Title: Ship a PRD template for offline / external-LLM drafting (ADR-027)
- Number: #32
- Milestone: v3.1.0 — PRD template for offline drafting
- Labels: feature, docs

Goal
Add a canonical PRD template to the kit that gives users a concrete
shape to fill out — by hand or via any external LLM — and produces
output `prd-normalizer` can consume as a pass-through.

Why it matters
ADR-003's "standard PRD" intake path is currently shape-implicit.
Users either improvise (forcing `prd-normalizer` to do avoidable
reshaping work) or have to read the skill's docs to discover the
expected shape. Offline drafters get no concrete starting point.
A canonical template makes the path explicit and offline drafting
trivial. The template is model-agnostic so any external LLM, or no
LLM at all, works equally well.

Requirements
- Create `templates/prd-template.md` with sections matching the 11
  canonical fields from `skills/prd-normalizer/SKILL.md`'s
  "Normalized PRD structure":
  1. Product name
  2. One-line description
  3. Problem
  4. Target users (Primary + optional Secondary)
  5. Goal
  6. User stories / scenarios (2–5 stories)
  7. Core capabilities
  8. Non-goals
  9. Constraints and preferences
  10. Success signals
  11. Open questions
- Leading HTML-comment header that:
  - explains the template's purpose,
  - notes the file is filled by the user or by an external LLM
    (no specific provider named),
  - notes the output path is `design/prd.md` in target projects,
  - names the consumer (`prd-normalizer`),
  - lists hard-required fields explicitly: Product name, Problem,
    Primary user, ≥1 core capability, ≥1 user story,
  - notes soft fields tolerate `[TBD]`.
- Placeholders use `{{...}}` style, consistent with other kit
  templates.
- Update `templates/README.md` with an index row pointing at the
  new template and naming `prd-normalizer` as the consumer.
- Update `skills/prd-normalizer/SKILL.md` "Intake protocol —
  standard PRD path" section: note that a faithfully-filled
  `templates/prd-template.md` makes the normaliser
  near-pass-through.
- Update `skills/idea-to-prd/SKILL.md` "When to use this skill"
  section: note that users with a PRD already drafted (by any
  means) should skip directly to `prd-normalizer` and may find
  `templates/prd-template.md` useful as a canonical shape to
  follow.
- Update `notes/feature-ideas.md` entry #16: flip status from
  `idea` to `shipped` with the ADR-027 link.

Acceptance criteria
- The 11 section headings in the new template match
  `prd-normalizer`'s canonical-field names exactly.
- A user can fill the template end-to-end without ambiguity about
  required vs optional fields.
- No specific external LLM (Perplexity, ChatGPT, Claude.ai, Gemini,
  etc.) is named in any directive context — only generic "external
  LLM or human" language.
- `templates/README.md` row links to the new file and names the
  consumer correctly.
- `prd-normalizer/SKILL.md` and `idea-to-prd/SKILL.md` reference
  the new template at the appropriate decision points.
- ADR-027 is `accepted` and `design/adr/README.md` reflects that
  (handled by `bin/sync-adr-index`).
- Feature-ideas #16 is marked `shipped` with the ADR link.

Scope and constraints
- Primary folders to touch: `templates/`, `skills/prd-normalizer/`,
  `skills/idea-to-prd/`, `design/adr/`, `notes/`.
- Folders to avoid: `bin/`, `examples/`, `docs/`, anything
  unrelated.
- Do not name a specific external LLM in directive contexts.
  Provider names may appear ONLY in this ADR's Context section as
  illustrations of "external LLM" in general, never in the
  template body or skill instructions.
- Do not introduce a new PRD-intake path. The three paths from
  ADR-003 remain. The template is one artefact along the existing
  "standard PRD" path.

Evaluation & testing requirements
- After commit, run `bin/sync-adr-index --check` to confirm the
  ADR index reflects ADR-027 as accepted.
- Open `templates/prd-template.md` in an editor and verify the
  section headings match `prd-normalizer/SKILL.md`'s canonical
  field names exactly.
- Walk through a hypothetical fill: pick a real product idea, fill
  every hard-required field, leave one or two soft fields as
  `[TBD]`, and confirm the resulting file shape would feed into
  `prd-normalizer`'s standard-PRD path without reshaping.
- All existing tests continue to pass.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-003-prd-intake-model.md` (the parent decision)
   - `design/adr/adr-027-prd-template.md` (this issue's decision)
   - `skills/prd-normalizer/SKILL.md` for the canonical 11-field
     structure
   - `skills/idea-to-prd/SKILL.md` for the parallel structure
   - `templates/mvp-template.md` and `templates/readme-template.md`
     for placeholder-style conventions
   - `templates/README.md` for the index row format
2. Propose a short, step-by-step PLAN:
   - the exact section structure of the new template,
   - the leading HTML-comment header content,
   - the `templates/README.md` row,
   - the SKILL.md insertion points and copy,
   - the feature-ideas update.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - one commit per logical concern (template, index row, skill
     references, feature-ideas),
   - each commit references ADR-027 and #32.
5. At the end, provide an evaluation summary:
   - files changed,
   - the rendered template structure (section headings list),
   - the walk-through fill validation,
   - any follow-up work for later issues,
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
