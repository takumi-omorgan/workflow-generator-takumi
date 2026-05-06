You are working in my workflow-kit repository.

Goal:
Reconcile the current GitHub repo state with the approved MVP backlog and setup plan, without creating duplicates.

Execution rules:
- Use GitHub CLI (`gh`) for GitHub operations.
- First run `gh auth status` and confirm the authenticated account and target repository.
- Then inspect the current state before making changes:
  - list labels
  - list open milestones
  - list open issues
- Compare the current state against the required labels, milestones, and issues below.
- Show me:
  1. what already exists,
  2. what is missing,
  3. what appears duplicated or inconsistent,
  4. the exact commands you plan to run.
- Wait for my approval before executing anything.
- Do not recreate issues that already exist.
- If a label already exists, skip it or update it safely.
- If a milestone already exists, reuse it.
- After execution, report:
  - labels created or confirmed,
  - milestones created or confirmed,
  - issues found and matched,
  - any missing issues that were created,
  - and any duplicates or naming mismatches that still need manual review.

Required labels:
- `feature` color `0E8A16`
- `bug` color `D73A4A`
- `design` color `1D76DB`
- `infra` color `FBCA04`
- `security` color `B60205`
- `docs` color `0075CA`

Required milestones:
- `M1 - Foundation + ADRs`
- `M2 - Planning Skills`
- `M3 - Execution Workflow`
- `M4 - Examples + Validation`

Required issues by title:
1. Create repository skeleton and project-local installation structure (ADR-001)
2. Write install guide and document v1 scope constraints (ADR-001, ADR-002)
3. Write GitHub setup guide and define repo workflow assets (ADR-004)
4. Create documentation and template scaffold for generated project artifacts (ADR-005)
5. Implement `idea-to-prd` skill for idea-first project setup (ADR-003)
6. Implement `prd-normalizer` skill for standard and custom PRDs (ADR-003)
7. Implement `prd-to-mvp` and `adr-writer` skills for scoped planning outputs (ADR-003, ADR-005)
8. Implement issue execution workflow assets for Claude Code sessions (ADR-006)
9. Add GitHub issue templates and PR template to the repository (ADR-004, ADR-005)
10. Create example project inputs and dry-run walkthroughs for all three planning entry paths (ADR-002, ADR-003)

If any required issue is missing, ask me to confirm before creating it.
If any existing issue title differs only slightly from the required title, flag it instead of creating a duplicate.
