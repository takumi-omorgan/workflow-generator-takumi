# workflow-docs — operator reference

Reference material for the `workflow-docs` skill: rationale, the exhaustive
source mappings, edge cases, and background. The agent operates from
`skills/workflow-docs/SKILL.md` alone and never reads this file; everything
here is for the human operator. If a rule here is needed to produce a
correct result, it belongs in the body — this file must stay
non-load-bearing.

## Why one skill

[ADR-018](../../design/adr/adr-018-workflow-docs-skill.md) consolidates all
three generated documents (`README.md`, `design/architecture.md`,
`design/ai-summary.md`) into a single skill rather than two, and establishes
the review-before-write approval gate as the ADR-018 contract.

## When to use it (expanded)

- After `prd-to-mvp` has produced `design/mvp.md`, to generate a real
  README, current architecture reference, and AI summary.
- After landing one or more ADRs, to refresh the current architecture and
  "Key decisions" sections in generated docs.
- Whenever `CLAUDE.md`, the PRD, the MVP statement, planning docs, or the
  implemented architecture has materially changed and the generated docs
  should reflect that change.

The skill takes no arguments; it infers everything from files in the
current working directory (the target project root).

## What the skill does not do

- Does not modify the PRD, MVP statement, ADRs, or `CLAUDE.md` — read-only
  inputs.
- Does not invent content. A missing section source omits the section; it
  is never filled with a placeholder or TODO.
- Does not overwrite files without explicit user approval. All generated
  files are shown in full before any write.
- Does not publish, deploy, or push. Output is local files only.
- Does not touch content outside its
  `<!-- workflow-docs:start:... -->` / `:end` markers on re-run.
- Does not manage `CLAUDE.md` — that is rendered from
  `templates/claude-md-template.md` at install time or by a human.

## Marker format (exact)

The agent never writes markers by hand — `bin/docs-render` owns them. This
is the exact shape it produces, for operators inspecting or repairing a
generated file. Every generated section is wrapped by two HTML-comment
markers, each on its own line with no leading whitespace:

```markdown
<!-- workflow-docs:start:overview -->
## Overview

...body...
<!-- workflow-docs:end:overview -->
```

- Markers are always on their own line, no leading whitespace.
- The section id (`overview`) is kebab-case and stable across releases.
- The `start` marker precedes the heading (not inside it), so the heading is
  regeneratable — this is what lets the skill cleanly omit a section on
  re-run when its source disappears.
- Content outside markers is never touched on re-run — `bin/docs-render`
  guarantees this byte-for-byte.
- If the user has moved markers or deleted a closing `end` marker,
  `bin/docs-render` exits 1 (malformed / no markers); the skill then flags
  the file as "manual edits — cannot safely update" and asks the user to
  restore the markers or delete the generated file and regenerate.

## Section omission logic (exhaustive)

Each generated section has a deterministic rule for when it appears. The
body states the general rule ("include a section iff at least one of its
source fields is present"); these tables are the precise per-section
mapping the general rule expands to.

### `README.md`

| Section | Appears when |
|-----------------|-------------------------------------------------------------|
| `tagline` | `design/mvp.md` has a one-line description, **or** PRD has a tagline |
| `overview` | `design/prd.md` / `prd-normalized.md` or `design/mvp.md` exists |
| `who-for` | PRD / MVP identifies a primary user |
| `status` | `CLAUDE.md` has a non-placeholder `{{CURRENT_PHASE}}` or milestone |
| `scope` | `design/mvp.md` has an "In scope" and/or "Out of scope" section |
| `how-to-run` | `CLAUDE.md` has non-placeholder commands |
| `key-decisions` | `design/adr/` contains at least one ADR |
| `roadmap` | `design/build-out-plan.md` has 2+ `### Phase N` blocks (per ADR-032). Single-phase / no-phase plans omit this section. |
| `more` | Always — static pointers to `CLAUDE.md`, `design/` |

### `design/architecture.md`

| Section | Appears when |
|---|---|
| `overview` | PRD, MVP, `CLAUDE.md`, planning docs, or ADRs describe the system shape |
| `system-boundaries` | PRD/MVP/planning docs define in-scope, out-of-scope, users, integrations, or deployment boundaries |
| `major-components` | `CLAUDE.md`, planning docs, or repo structure identify components/modules/services |
| `data-and-control-flow` | Sources describe data flow, request flow, jobs, agents, pipelines, or state transitions |
| `external-dependencies` | Sources mention APIs, vendors, databases, hosted services, models, or infrastructure |
| `key-constraints` | MVP principles, PRD constraints, ADR consequences, or `CLAUDE.md` rules apply to architecture |
| `extension-points` | Sources identify plugin/module boundaries or safe places to add features |
| `current-decisions` | ADRs or `design/decisions.md` contain current load-bearing decisions |
| `open-questions` | Planning docs, state, milestones, or PR follow-ups list unresolved architecture questions |

### `design/ai-summary.md`

| Section | Appears when |
|------------------|-----------------------------------------------------------|
| `objectives` | `design/mvp.md` has a product goal or success criteria |
| `architecture` | `CLAUDE.md` has a "Project structure" or tech stack block |
| `tech-stack` | `CLAUDE.md` has any of runtime / framework / data layer |
| `constraints` | `design/mvp.md` has principles, or PRD has constraints |
| `extension-points` | `CLAUDE.md` or PRD notes extension points (rare on first run — usually omitted) |
| `current-status` | `CLAUDE.md` has a current phase, or ADRs are dated |
| `key-decisions` | `design/adr/` contains at least one ADR |

### Roadmap section content

When the `roadmap` section appears, render a compact table sourced from
`design/build-out-plan.md`'s `### Phase N: <name>` blocks:

| # | Phase | Goal | Exit criterion |
|---|-------|------|----------------|
| 1 | Foundation | one-line goal | observable exit |
| 2 | Core feature | one-line goal | observable exit |
| 3 | Polish | one-line goal | observable exit |

Single-phase projects omit the roadmap section entirely — phase metadata is
implicit and adds no information to the README.

## Template variables (exhaustive)

Every field is optional; a missing field drives its section's omission. The
body gives the filling rule and representative examples; these tables are
the full mapping.

### README (`templates/readme-template.md`)

| Placeholder | Source |
|------------------------|-----------------------------------------------------------|
| `{{PROJECT_NAME}}` | `design/mvp.md` "Product name", else `CLAUDE.md` first `#` heading, else repo basename |
| `{{PROJECT_TAGLINE}}` | `design/mvp.md` "One-line description", else PRD tagline |
| `{{PROJECT_DESCRIPTION}}` | `design/mvp.md` "Product goal", else PRD "Goal" / "Problem" paragraph |
| `{{PRIMARY_USER}}` | `design/mvp.md` "Primary user", else PRD "Target user" |
| `{{CURRENT_PHASE}}` | `CLAUDE.md` "Current phase" section |
| `{{CURRENT_MILESTONE}}`| `CLAUDE.md` active milestone |
| `{{IN_SCOPE_BULLETS}}` | `design/mvp.md` "In scope" bullets |
| `{{OUT_OF_SCOPE_BULLETS}}` | `design/mvp.md` "Out of scope" bullets |
| `{{INSTALL_COMMAND}}` | `CLAUDE.md` install command |
| `{{DEV_COMMAND}}` | `CLAUDE.md` dev command |
| `{{TEST_COMMAND}}` | `CLAUDE.md` test command |
| `{{KEY_ADR_BULLETS}}` | One bullet per `design/adr/adr-NNN-*.md`, newest first: `- ADR-NNN: <one-line decision>` |

### Architecture (`templates/architecture-template.md`)

| Placeholder | Source |
|---|---|
| `{{PROJECT_NAME}}` | Same as README |
| `{{YYYY-MM-DD}}` | Today's date |
| `{{ARCHITECTURE_OVERVIEW}}` | PRD/MVP goal plus `CLAUDE.md` project structure and tech stack |
| `{{SYSTEM_BOUNDARIES}}` | MVP in/out-of-scope, PRD users/integrations, deploy target |
| `{{MAJOR_COMPONENTS}}` | `CLAUDE.md` repo structure, planning docs, implemented module/service names |
| `{{DATA_AND_CONTROL_FLOW}}` | Planning docs, PRD workflows, ADR consequences, relevant milestone summaries |
| `{{EXTERNAL_DEPENDENCIES}}` | Tech stack, APIs, databases, vendors, hosted services, infra |
| `{{KEY_CONSTRAINTS}}` | MVP principles, PRD constraints, ADR consequences, `CLAUDE.md` rules |
| `{{EXTENSION_POINTS}}` | PRD/CLAUDE/planning notes about module, plugin, API, or workflow boundaries |
| `{{CURRENT_DECISION_BULLETS}}` | Concise current decisions from ADRs and `design/decisions.md`; not every historical detail |
| `{{OPEN_ARCHITECTURE_QUESTIONS}}` | Open questions from planning docs, `design/state.md`, milestone summaries, or PR follow-ups |

### AI summary (`templates/ai-summary-template.md`)

| Placeholder | Source |
|------------------------|-----------------------------------------------------------|
| `{{PROJECT_NAME}}` | Same as README |
| `{{YYYY-MM-DD}}` | Today's date |
| "Objectives" bullets | `design/mvp.md` "Product goal" + "Success criteria" |
| "Architecture" paragraph | `CLAUDE.md` "Project structure" + "Technology stack" |
| "Tech stack" bullets | `CLAUDE.md` runtime / framework / data layer / libraries / deploy target |
| "Constraints" bullets | `design/mvp.md` "Product principles", PRD "Constraints" |
| "Extension points" bullets | PRD / `CLAUDE.md` extension-point notes (usually omitted on first run) |
| "Current status" bullets | `CLAUDE.md` "Current phase", ADR dates, issue activity if available |
| "Key decisions" bullets | One bullet per ADR, newest first |

For the AI summary, also wrap each section of
`templates/ai-summary-template.md` in the same marker format before
rendering. Section ids mirror the template headings in kebab-case.

## Edge cases

- **No PRD, no MVP, no ADRs, no CLAUDE.md** → stop; tell the user to run
  `prd-normalizer` / `prd-to-mvp` first. Do not write empty docs.
- **Only `CLAUDE.md` exists** → generate a minimal README (tagline +
  how-to-run + more), a minimal architecture doc (system shape from project
  structure / tech stack), and a minimal AI summary (tech stack + current
  status). Omit all other sections.
- **Only ADRs exist** → generate only the `key-decisions` section in all
  outputs. Ask the user whether that is useful before writing.
- **Existing README has no markers** → treat as first run; show diff;
  require explicit confirmation; do not silently overwrite.
- **Existing README has markers but they are malformed** (missing `end`,
  duplicated `start`, moved out of order) → stop and ask the user to restore
  or delete the file.
- **Existing file has manual content inside a marker block** → that content
  is regenerated (markers are the contract for "this is regenerated").
  Manual edits belong outside markers. Warn the user if the diff shows any
  non-trivial change inside a marker block.
- **ADR files missing a `# ADR-NNN:` heading** → skip that ADR with a
  warning; do not stop.
- **`CLAUDE.md` still has `{{PLACEHOLDER}}` tokens** → treat those fields as
  missing; drive section omission accordingly.
- **Multiple PRD files (`prd.md` + `prd-normalized.md`)** → prefer
  `prd-normalized.md` (the kit's canonical form).

## Self-check before writing (operator checklist)

For each output file:

- Every `{{PLACEHOLDER}}` is either filled or its enclosing section has been
  omitted.
- Every included section is wrapped in matching `start:`/`end:` markers with
  the same section id.
- No omitted section has left a stray heading, body, or marker behind.
- On re-run: content outside markers in the existing file is byte-identical
  to what it was before.
- The user explicitly confirmed the write.

If any fail, fix and re-show before writing.

## Running against the kit repo itself

This repo (`workflow-generator`) has its own public architecture document at
`docs/architecture.md`, and has `CLAUDE.md` and `design/adr/*.md` but no
`design/prd.md` or `design/mvp.md`. Running the skill here would produce a
sparse, source-heavy result: for `README.md` only `key-decisions` and `more`
would be included (and the rich hand-written README's missing markers would
make the skill refuse to overwrite without an explicit "yes, replace"); for
`design/architecture.md`, a sparse doc — maintain `docs/architecture.md`
directly instead; for `design/ai-summary.md`, only `key-decisions` and a
minimal `current-status`. In practice the kit repo should **not** run
`/workflow-docs` on itself. The skill is aimed at target projects that have
already run `prd-to-mvp`.

## Worked example

See [`../../skills/workflow-docs/example.md`](../../skills/workflow-docs/example.md)
for a worked run on a small sample project.
