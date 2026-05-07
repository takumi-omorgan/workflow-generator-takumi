You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It supports three planning entry paths: idea-only, standard PRD, and custom PRD.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADRs:
- File: `design/adr/adr-002-new-project-only-scope.md`
- Decision: Limit v1 to new projects only.
- File: `design/adr/adr-003-prd-intake-model.md`
- Decision: Support three PRD intake paths.

GitHub Issue:
- Title: Create example project inputs and dry-run walkthroughs for all three planning entry paths (ADR-002, ADR-003)
- Number: #10
- Milestone: M4 - Examples + Validation
- Labels: docs, feature

Goal
Make the workflow easier to understand by showing realistic examples for all three planning paths.

Why it matters
Examples are the fastest way to reduce ambiguity in a new toolkit. They also help validate that the workflow works as intended across the three supported entry modes.

Requirements
- Add `examples/idea-only-example.md`
- Add `examples/standard-prd-example.md`
- Add `examples/custom-prd-example.md`
- Add a short walkthrough for how each example moves through the workflow
- Confirm examples align with the current docs and skills

Acceptance criteria
- All three entry modes are represented by examples
- The examples are coherent and easy to follow
- The walkthroughs make the workflow feel concrete
- The examples help validate the MVP documentation and skills

Scope and constraints
- Primary folders to touch: `examples/`, possibly `docs/`
- Folders to avoid unless absolutely necessary: `.github/`, unrelated implementation assets
- Keep examples realistic but lightweight
- Make sure the examples reflect the actual current state of the skills and templates in the repo

Evaluation & testing requirements
- If no executable code is added, validate by checking alignment across docs, skills, and examples
- If helper scripts or structured validation are added, include appropriate tests
- Ensure the examples do not promise workflows that the current repo cannot yet support

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-002-new-project-only-scope.md`
   - `design/adr/adr-003-prd-intake-model.md`
   - `generic-project-workflow.md`
   - current planning skills, docs, and templates
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which example files you will create,
   - what scenario each example will represent,
   - how the walkthroughs will be structured,
   - how you will validate them against the current docs and skills.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - how example consistency was checked,
   - any gaps exposed by the examples,
   - exact files I should review.

Do not start editing files until I explicitly approve your plan.
