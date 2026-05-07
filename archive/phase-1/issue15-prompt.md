You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-013-prepare-issue-skill.md`
- Decision: Build a /prepare-issue skill that auto-fills an issue prompt from a GitHub issue and its linked ADRs.

GitHub Issue:
- Title: /prepare-issue skill (ADR-013)
- Number: #15
- Milestone: M5 - v-next
- Labels: feature, design

Goal
Build a `/prepare-issue` skill that takes a GitHub issue number, pulls the issue body and ADR references via `gh`, reads the build-out plan, fills the prompt template, and writes the result to `prompts/issue-NNN-short-title.md`.

Why it matters
Manually writing issue prompts is repetitive and risks inconsistency. Automating prompt generation from GitHub issues ensures every session prompt follows the same structure, includes the right context, and is ready to use immediately.

Requirements
- Create the skill in `skills/prepare-issue/`
- The skill must accept a GitHub issue number as input
- Pull the issue title, body, labels, milestone, and linked ADR references via `gh issue view`
- Read `design/build-out-plan.md` to extract additional context for the issue
- Fill the prompt template from `prompts/_template.md` (ADR-008) with the extracted information
- Write the filled prompt to `prompts/issue-NNN-short-title.md`, deriving the short title from the issue title
- Handle edge cases: issue not found, missing ADR references, missing template file
- Show the user the filled prompt for review before writing the file

Acceptance criteria
- `skills/prepare-issue/` exists with the skill implementation
- The skill takes a GitHub issue number and produces a correctly filled prompt file
- The output prompt matches the structure of `prompts/_template.md`
- The prompt file is written to `prompts/issue-NNN-short-title.md` with a sensible short title
- ADR references from the issue are resolved and included in the prompt
- Build-out plan context is incorporated where relevant
- The skill works correctly with the `prompts/` folder structure from ADR-008 / Issue #12
- The user sees the filled prompt before the file is written
- Edge cases are handled gracefully with clear error messages

Scope and constraints
- Primary folders to touch: `skills/prepare-issue/`
- Folders to avoid unless absolutely necessary: `bin/`, `templates/`, `notes/`
- The skill must use `gh` CLI for all GitHub API interactions
- Do not modify the prompt template itself; only read and fill it
- Do not create or modify GitHub issues; this skill is read-only with respect to GitHub
- Keep the skill focused on single-issue prompt generation

Evaluation & testing requirements
- Test the skill with an existing GitHub issue that has ADR references
- Test with an issue that has no ADR references
- Test with a non-existent issue number
- Verify the output prompt matches the template structure
- Verify the short title derivation produces clean filenames
- Confirm that all changes stay aligned with ADR-013
- All existing tests must continue to pass if the repo already contains tests

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-013-prepare-issue-skill.md`
   - `generic-project-workflow.md`
   - `prompts/_template.md` (from ADR-008 / Issue #12)
   - `design/build-out-plan.md` (as reference for the context source)
   - existing skills in `skills/` for style and conventions
   - `notes/issue1-prompt.md` through `notes/issue10-prompt.md` as examples of the desired output
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - how the skill will extract information from the GitHub issue,
   - how ADR references will be resolved,
   - how the short title will be derived,
   - the template-filling logic,
   - your testing plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not modify the prompt template or GitHub issues.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed for later issues,
   - exact commands I should run to test the skill myself.

Do not start editing files until I explicitly approve your plan.
