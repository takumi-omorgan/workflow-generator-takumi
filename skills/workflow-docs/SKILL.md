---
name: workflow-docs
description: Generate README.md, design/architecture.md, and design/ai-summary.md for a target project from PRD, MVP, ADRs, planning docs, and CLAUDE.md — re-runnable with marker-fenced sections that preserve manual edits. Use when generating or refreshing the project's user-facing and AI-facing docs.
permission-category: 1  # substitutable — generates README.md, design/architecture.md, and design/ai-summary.md locally, per workflow-guide §7
inputs: []
outputs:
  - artefact: "README.md"
    description: "Generated (marker-fenced)"
  - artefact: "design/architecture.md"
    description: "Current architecture/design reference (marker-fenced)"
  - artefact: "design/ai-summary.md"
    description: "AI-readable project summary (marker-fenced)"
next: []
---

# workflow-docs

Generate three project-level documents in a target project from the kit's
existing artifacts:

- `README.md` — public entry point for humans
- `design/architecture.md` — current architecture/design reference
- `design/ai-summary.md` — AI-readable project summary

The skill is **re-runnable**: generated regions are marker-fenced, so a
re-run updates them without clobbering edits outside them. A section with no
source data is **omitted** entirely — never left blank or placeholder-filled.

Operator reference (rationale, source tables, edge cases, example):
[`docs/skills/workflow-docs.md`](../../docs/skills/workflow-docs.md) — not
needed at runtime; the body suffices.

## When to use

Invoke `/workflow-docs` with no arguments; everything is inferred from the
target project root (CWD). Run it after `prd-to-mvp`, after landing ADRs, or
whenever the PRD, MVP, `CLAUDE.md`, planning docs, or architecture changed.

## Inputs (read-only)

All inputs live in the target project and are optional; a missing input
omits its derived sections. Never modify them.

| Source | Contributes |
|---|---|
| `design/prd.md` or `design/prd-normalized.md` (prefer normalized) | description, primary user, problem |
| `design/mvp.md` | product name, tagline, principles, In/Out-of-scope, success criteria |
| `design/adr/adr-*.md` | "Key decisions" — one bullet per ADR, newest first |
| `design/build-out-plan.md` | roadmap / phase context |
| `design/planning.md`, `design/decisions.md` | architecture context, constraints, current decisions, open questions |
| `design/milestones/*.md`, `design/state.md` | recent evolution, in-flight status |
| `CLAUDE.md` | project name, tech stack, commands, current phase, milestone |

If **none** exist, stop with: "No PRD, MVP, ADRs, or CLAUDE.md found — run
`prd-normalizer` / `prd-to-mvp` first." Do not write empty docs.

## Outputs

Written to the target project root, rendered from the kit's templates
(installed under `.claude/skills/workflow-docs/`, or `templates/` in the kit
repo):

- `README.md` ← `templates/readme-template.md`
- `design/architecture.md` ← `templates/architecture-template.md`
- `design/ai-summary.md` ← `templates/ai-summary-template.md`

Fill each template's `{{PLACEHOLDER}}` from the matching-meaning Inputs
source — e.g. `{{PROJECT_NAME}}` ← MVP product name / `CLAUDE.md` heading /
repo basename; `{{KEY_ADR_BULLETS}}` ← one `- ADR-NNN: <decision>` per ADR,
newest first; `{{YYYY-MM-DD}}` ← today. A placeholder whose source is
missing stays unfilled and **forces its section's omission** — never
substitute placeholder or TODO text. (Full source tables: reference doc.)

## Markers and section omission

The agent never writes markers by hand — `bin/docs-render` owns them. You
hand it a `{id, body}` array; it fences each section as
`<!-- workflow-docs:start:<id> -->` / `:end` (ids stable kebab-case) and
preserves content outside markers byte-for-byte on re-run. Include a section
**iff** at least one of its source fields is present; otherwise omit it by
leaving it out of the array. Special cases: README `roadmap` appears only
with **2+** `### Phase N` blocks in `design/build-out-plan.md` (ADR-032);
`more` (static pointers) always appears.

## Execution protocol

Run in order; stop on the first failure unless noted.

1. **Detect target.** CWD must be the target project root (has `.git/`); if
   absent, ask the user to `cd` in and stop.
2. **Collect inputs.** Read the Inputs-table files that exist; if none, stop
   with the message above.
3. **Parse into one context dict.** A missing source stays `None`; never
   substitute placeholder text.
4. **Choose sections.** Apply the omission rule per output; produce an
   ordered `(section_id, body)` list per file.
5. **Render sections.** Fill each included section's template placeholders
   from the context (heading included); collect a JSON array of `{id, body}`
   per file, in template order.
6. **Splice with `bin/docs-render`** (never hand-edit markers):
   ```
   bin/docs-render --file <output> --sections <sections.json> --dry-run --format json
   ```
   First run wraps sections in markers; re-run updates only marked regions
   (dropping omitted sections, inserting new ones) and never touches content
   outside them. If it exits 1 (file has **no** markers, or **malformed**
   markers), do not overwrite — show the diff and ask the user to consent or
   restore markers.
7. **Review before write.** Show every generated file in full (or a diff if
   it exists) and ask "Write these files? (yes / edit / cancel)". Default no.
8. **Write only after confirmation.** Re-run `bin/docs-render` without
   `--dry-run` to write each file atomically; report absolute paths and a
   one-line per-file summary from `sectionsReplaced` / `sectionsAdded` /
   `sectionsOmitted`.

## Hard rules

- Inputs (PRD, MVP, ADRs, `CLAUDE.md`) are **read-only**; never modify them,
  and never manage `CLAUDE.md` (it is rendered at install time).
- Never invent content: a missing source omits its section — no placeholder,
  no TODO.
- Never write without the explicit review-before-write approval (ADR-018
  gate), even if the content looks clean.
- All three files go out together after one confirmation, or none do.
- Never overwrite a file with no markers or malformed markers without
  explicit consent; content inside a marker block is regenerated (warn on a
  non-trivial change inside one).
- Output is local files only — never publish, deploy, or push.
- Do **not** run this skill on the kit repo itself (maintain
  `docs/architecture.md` directly).

## Handoff

After writing, the user edits freely outside markers; re-runs touch only
marked regions.
