<!--
  Reusable Claude Code session prompt — one issue, one session.
  Copy this file, fill the {{...}} placeholders, paste into Claude Code.
  See docs/issue-prompt-guide.md for how to fill it and what the
  end-of-session evaluation summary must contain. Underlying decision:
  Design/adr/adr-006-claude-code-execution-model.md.
-->

You are working in my `{{PROJECT_NAME}}` repository.

Context:
- {{ONE_LINE_PROJECT_DESCRIPTION}}
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `{{WORKFLOW_DOC_PATH}}`.
- AI-readable summary is at `Design/ai-summary.md`.

ADR:
- File: `Design/adr/{{ADR_FILE}}`
- Decision: {{ADR_ONE_LINE_SUMMARY}}
<!-- If multiple ADRs apply, repeat the two lines per ADR.
     If no ADR applies, replace this section with: "ADR: none — {{REASON}}." -->

GitHub Issue:
- Title: {{ISSUE_TITLE}}
- Number: #{{ISSUE_NUMBER}}
- Milestone: {{MILESTONE}}
- Labels: {{LABELS}}

Goal
{{ONE_OR_TWO_SENTENCES}}

Why it matters
{{ONE_PARAGRAPH}}

Requirements
- {{REQUIREMENT_1}}
- {{REQUIREMENT_2}}
- {{REQUIREMENT_3}}

Acceptance criteria
- {{CRITERION_1}}
- {{CRITERION_2}}
- {{CRITERION_3}}

Scope and constraints
- Primary folders to touch: {{PRIMARY_FOLDERS}}
- Folders to avoid unless absolutely necessary: {{AVOID_FOLDERS}}
- {{PROJECT_SPECIFIC_CONSTRAINT_OR_DELETE_THIS_LINE}}

Evaluation & testing requirements
- Every new module or significant function MUST have unit tests.
- Tests go in `test/` mirroring `src/`.
- Cover at minimum: happy path, edge cases, error handling.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing code:
   - `CLAUDE.md`
   - `Design/adr/{{ADR_FILE}}`
   - `Design/ai-summary.md`
   - any existing modules under {{PRIMARY_FOLDERS}}
   - any existing tests related to the modules you will change
2. Propose a step-by-step implementation PLAN, including:
   - new files/modules to create,
   - existing files to modify,
   - key functions/classes and their structure,
   - your test plan: which test files, what scenarios, what edge cases.
3. Wait for my approval before making any edits.
4. After I approve, implement the plan:
   - write tests alongside the implementation, not as an afterthought,
   - keep changes focused on this issue's scope,
   - commit incrementally with messages that reference the ADR and issue
     (e.g. "Add GPX parser (ADR-001, #11)").
5. At the end, provide the evaluation summary specified in
   docs/issue-prompt-guide.md.

Do not start editing files until I explicitly approve your plan.
