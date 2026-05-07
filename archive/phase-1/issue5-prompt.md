You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- One supported planning path is starting from only a rough idea with no formal PRD.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-003-prd-intake-model.md`
- Decision: Support three PRD intake paths: no PRD, standard PRD, and custom PRD.

GitHub Issue:
- Title: Implement idea-to-prd skill for idea-first project setup (ADR-003)
- Number: #5
- Milestone: M2 - Planning Skills
- Labels: design, feature

Goal
Support the “no PRD yet” path by creating a structured `idea-to-prd` skill.

Why it matters
Many users will not start with a polished PRD. This skill lowers adoption friction and makes the workflow useful earlier in the product lifecycle.

Requirements
- Define the purpose and boundaries of the `idea-to-prd` skill
- Create `skills/idea-to-prd/SKILL.md`
- Define required inputs and expected outputs
- Ensure the output is suitable for later normalization or MVP scoping
- Add one example input/output pair

Acceptance criteria
- The repository contains a working first draft of the `idea-to-prd` skill
- The skill is clearly scoped to rough idea capture
- The output is compatible with the later planning workflow
- An example demonstrates expected usage

Scope and constraints
- Primary folders to touch: `skills/idea-to-prd/`, possibly `docs/` if cross-references are needed
- Folders to avoid unless absolutely necessary: `.github/`, unrelated skills, app/demo code
- Keep the skill focused on idea-to-PRD only
- Do not merge normalization or MVP scoping into this skill

Evaluation & testing requirements
- If there is no executable code, validate through examples and document behavior clearly
- If helper code or structured schema files are added, include tests or validation where appropriate
- Ensure the skill boundaries are explicit and do not overlap too much with later skills

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-003-prd-intake-model.md`
   - `generic-project-workflow.md`
   - any existing skills under `skills/`
   - the templates created for planning artifacts
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - what the skill will do and not do,
   - which files you will create or update,
   - the structure of `skills/idea-to-prd/SKILL.md`,
   - the example you will include,
   - how you will validate that the output is useful for downstream steps.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - how the skill was validated,
   - any interface assumptions for the next skills,
   - exact files I should review.

Do not start editing files until I explicitly approve your plan.
