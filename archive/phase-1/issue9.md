## Summary
Add the repository-level GitHub issue templates and pull request template needed to support the workflow in practice.

## ADR
Related ADRs:
- `design/adr/adr-004-github-first-workflow-model.md`
- `design/adr/adr-005-documentation-and-template-architecture.md`

## Goal
Create the `.github` templates that standardize issue creation and pull request quality.

## Why it matters
GitHub templates are one of the simplest ways to enforce consistency in issue reporting and PR review. GitHub supports issue and PR templates directly when they are committed on the default branch.

## Tasks
- [ ] Add `.github/ISSUE_TEMPLATE/feature-request.md`
- [ ] Add `.github/ISSUE_TEMPLATE/docs-task.md`
- [ ] Add `.github/pull_request_template.md`
- [ ] Ensure the template structure aligns with the workflow docs and ADR references
- [ ] Add brief usage notes in documentation

## Acceptance criteria
- The repository contains issue and PR templates in supported GitHub locations
- Templates reflect the project workflow structure
- Contributors opening issues and PRs are guided into consistent formats
- The docs mention where these templates live and how they are used

## Notes
Labels: `docs`, `infra`, `feature`
Milestone: `M3 - Execution Workflow`
