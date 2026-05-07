# Templates

Starter templates for the artifacts that the kit generates into a new target
project. Each template is a markdown file with `{{UPPER_SNAKE}}` placeholders;
skills fill the placeholders when they run, and humans can fill them by hand
when a skill is not yet available.

Every template starts with an HTML comment block explaining what it is, who
fills it in, and where the rendered output should live in a target project.

Templates are reference material in this kit repo. They are copied into target
projects as-is, or transformed by a skill. See
[ADR-005](../design/adr/adr-005-documentation-and-template-architecture.md)
for the documentation-and-template architecture.

## Templates

| File | Purpose | Output location in target project | Filled by |
|---|---|---|---|
| [`adr-template.md`](adr-template.md) | Architecture Decision Record | `design/adr/adr-NNN-short-title.md` | `adr-writer` skill (Issue #7) / human |
| [`issue-template.md`](issue-template.md) | GitHub issue body | Pasted into `gh issue create --body` | `issue-planner` skill / human |
| [`pr-template.md`](pr-template.md) | Pull request body | [`.github/pull_request_template.md`](../.github/pull_request_template.md) | PR author / `pr-review-packager` skill |
| [`claude-md-template.md`](claude-md-template.md) | Project rules for Claude Code | `CLAUDE.md` at target project root | `workflow-docs` skill / human |
| [`ai-summary-template.md`](ai-summary-template.md) | AI-readable project summary | `design/ai-summary.md` | `workflow-docs` skill / human |
| [`prd-template.md`](prd-template.md) | Product Requirements Document | `design/prd.md` | external LLM / human; consumed by `prd-normalizer` |
| [`mvp-template.md`](mvp-template.md) | MVP statement | `design/mvp.md` | `prd-to-mvp` skill (Issue #7) / human |
| [`build-out-plan-template.md`](build-out-plan-template.md) | Phased build-out plan | `design/build-out-plan.md` | `prd-to-mvp` skill (Issue #7) / human |
| [`planning-template.md`](planning-template.md) | Deeper planning artefact (decomposition, risks, assumptions, sequencing, research questions) — opt-in for non-trivial projects | `design/planning.md` | `planning` skill (ADR-031, Issue #40) / human |
| [`decisions-template.md`](decisions-template.md) | Append-only decisions log capturing informal-but-settled context (gray areas resolved before ADR drafting) — opt-in, below-ADR-weight by design | `design/decisions.md` | `clarify` skill (ADR-033, Issue #42) / human |
| [`state-template.md`](state-template.md) | Session-continuity pointer (current phase, in-flight issue, recent work, blockers, continue-here) — committed, capped at ~100 lines | `design/state.md` | `prepare-issue` / `claude-issue-executor` / `pr-review-packager` / `pause` (ADR-035, Issue #44) |
| [`licenses/`](licenses/) | License-text templates (currently `mit.txt`) with `{{YEAR}}` and `{{COPYRIGHT_HOLDER}}` placeholders | `LICENSE` at target project root | `bin/install-workflow-kit --license=mit` (ADR-030) |

## Conventions

- Placeholders use `{{UPPER_SNAKE}}`.
- Section headings use `##` for top-level blocks and `###` only inside
  "Options considered" / "Phases" etc.
- Inline `_italic hints_` describe what to write where an upper-snake
  placeholder would be clumsy.
- Every template is a valid standalone markdown file — a user can
  commit it to a target project before any placeholder is filled.
