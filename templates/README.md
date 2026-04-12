# Templates

Starter templates for the artifacts that the kit generates into a new target
project. Each template is a markdown file with `{{UPPER_SNAKE}}` placeholders;
skills fill the placeholders when they run, and humans can fill them by hand
when a skill is not yet available.

Every template starts with an HTML comment block explaining what it is, who
fills it in, and where the rendered output should live in a target project.

Templates are reference material in this kit repo. They are copied into target
projects as-is, or transformed by a skill. See
[ADR-005](../Design/adr/adr-005-documentation-and-template-architecture.md)
for the documentation-and-template architecture.

## Templates

| File | Purpose | Output location in target project | Filled by |
|---|---|---|---|
| [`adr-template.md`](adr-template.md) | Architecture Decision Record | `Design/adr/adr-NNN-short-title.md` | `adr-writer` skill (Issue #7) / human |
| [`issue-template.md`](issue-template.md) | GitHub issue body | Pasted into `gh issue create --body` | `issue-planner` skill / human |
| [`pr-template.md`](pr-template.md) | Pull request body | `.github/pull_request_template.md` (shipped by Issue #9) | PR author / `pr-review-packager` skill |
| [`claude-md-template.md`](claude-md-template.md) | Project rules for Claude Code | `CLAUDE.md` at target project root | `workflow-docs` skill / human |
| [`ai-summary-template.md`](ai-summary-template.md) | AI-readable project summary | `Design/ai-summary.md` | `workflow-docs` skill / human |
| [`mvp-template.md`](mvp-template.md) | MVP statement | `Design/mvp.md` | `prd-to-mvp` skill (Issue #7) / human |
| [`build-out-plan-template.md`](build-out-plan-template.md) | Phased build-out plan | `Design/build-out-plan.md` | `prd-to-mvp` skill (Issue #7) / human |

## Conventions

- Placeholders use `{{UPPER_SNAKE}}`.
- Section headings use `##` for top-level blocks and `###` only inside
  "Options considered" / "Phases" etc.
- Inline `_italic hints_` describe what to write where an upper-snake
  placeholder would be clumsy.
- Every template is a valid standalone markdown file — a user can
  commit it to a target project before any placeholder is filled.
