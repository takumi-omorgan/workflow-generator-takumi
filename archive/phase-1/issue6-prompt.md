You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It supports both standard PRDs and custom user-defined planning documents.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `Design/adr/adr-003-prd-intake-model.md`
- Decision: Support three PRD intake paths: no PRD, standard PRD, and custom PRD.

GitHub Issue:
- Title: Implement prd-normalizer skill for standard and custom PRDs (ADR-003)
- Number: #6
- Milestone: M2 - Planning Skills
- Labels: design, feature

Goal
Support multiple PRD intake paths while keeping downstream workflow generation consistent.

Why it matters
The MVP promises to accept both standard and custom PRD formats. This skill is what makes that promise practical.

Requirements
- Define the normalization target structure
- Create `skills/prd-normalizer/SKILL.md`
- Describe how standard PRDs are handled
- Describe how custom PRDs are interpreted and normalized
- Add example transformations

Acceptance criteria
- The skill clearly supports both standard and custom PRD inputs
- The normalized output is predictable and reusable
- Example transformations make the behavior easy to understand
- The skill reduces ambiguity for downstream planning steps

Scope and constraints
- Primary folders to touch: `skills/prd-normalizer/`, possibly supporting docs/examples
- Folders to avoid unless absolutely necessary: unrelated skills, `.github/`, app/demo code
- Keep the focus on normalization rather than MVP scoping or ADR generation
- Be explicit about assumptions and fallback behavior for incomplete user input

Evaluation & testing requirements
- If no executable code is added, validate via examples and clear transformation rules
- If structured schemas or helper code are introduced, include appropriate tests or validation
- Verify that the normalized output can be consumed by `prd-to-mvp` later

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-003-prd-intake-model.md`
   - `generic-project-workflow.md`
   - `skills/idea-to-prd/SKILL.md` if it already exists
   - existing templates and examples relevant to planning
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the normalization target structure,
   - which files you will create or update,
   - how standard and custom PRDs will be treated,
   - the examples you will add,
   - your validation approach.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan and keep changes focused on this issue only.
5. At the end, provide an evaluation summary including:
   - what changed,
   - how normalization behavior was validated,
   - downstream assumptions for later skills,
   - exact files I should review.

Do not start editing files until I explicitly approve your plan.
