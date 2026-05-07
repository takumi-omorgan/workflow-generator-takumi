You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It needs to turn planning inputs into both an MVP scope artifact and draft ADRs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADRs:
- File: `design/adr/adr-003-prd-intake-model.md`
- Decision: Support three PRD intake paths.
- File: `design/adr/adr-005-documentation-and-template-architecture.md`
- Decision: Generate documentation and templates directly into the target repository.

GitHub Issue:
- Title: Implement prd-to-mvp and adr-writer skills for scoped planning outputs (ADR-003, ADR-005)
- Number: #7
- Milestone: M2 - Planning Skills
- Labels: design, feature

Goal
Create the bridge from PRD-level planning into actionable architecture and implementation planning artifacts.

Why it matters
A normalized PRD is not enough on its own. The workflow needs structured MVP scoping and lightweight ADR drafting to move toward issue planning.

Requirements
- Create `skills/prd-to-mvp/SKILL.md`
- Create `skills/adr-writer/SKILL.md`
- Define the MVP summary structure
- Define the ADR drafting structure and template usage
- Add examples showing PRD → MVP and MVP → ADR draft flows

Acceptance criteria
- Both skills exist and have clearly defined purposes
- The MVP output is scoped and practical
- The ADR drafting behavior aligns with the repository ADR format
- Examples show how the planning chain fits together

Scope and constraints
- Primary folders to touch: `skills/prd-to-mvp/`, `skills/adr-writer/`, maybe `templates/` or `docs/` if needed
- Folders to avoid unless absolutely necessary: `.github/`, unrelated execution assets
- Keep `prd-to-mvp` and `adr-writer` separate but coordinated
- Make sure ADR output aligns with the accepted six ADRs already in the repo

Evaluation & testing requirements
- If executable code is not introduced, validate through strong examples and structural consistency
- If schemas/helpers are added, include tests or validation where appropriate
- Confirm that outputs are suitable inputs for issue planning later

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-003-prd-intake-model.md`
   - `design/adr/adr-005-documentation-and-template-architecture.md`
   - `generic-project-workflow.md`
   - existing planning skills and templates
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the boundaries between the two skills,
   - files to create or update,
   - the MVP structure,
   - the ADR drafting structure,
   - the examples you will include,
   - your validation approach.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - how the outputs were validated,
   - any assumptions for issue planning,
   - exact files I should review.

Do not start editing files until I explicitly approve your plan.
