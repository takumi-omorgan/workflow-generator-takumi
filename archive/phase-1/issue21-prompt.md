You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-019-claude-code-guide.md`
- Decision: Write a dedicated docs/claude-code-guide.md covering how to use Claude Code with the kit.

GitHub Issue:
- Title: Write docs/claude-code-guide.md (ADR-019)
- Number: #21
- Milestone: M5 - v-next
- Labels: docs

Goal
Write docs/claude-code-guide.md covering how to use Claude Code effectively with the workflow kit, so users have a single reference for Claude Code interaction patterns.

Why it matters
Users need clear guidance on how to interact with Claude Code in plan mode, invoke skills, follow the approve-then-implement loop, and avoid common pitfalls. Without this doc, users must piece together information from multiple sources or learn through trial and error.

Requirements
- Cover plan mode and how to use it during implementation
- Cover skill invocation via /skill-name
- Cover the approve-then-implement loop (propose plan → user approves → implement)
- Cover common pitfalls: destructive commands, forgetting to stage files, overwriting existing work
- Link to but do not duplicate content from the workflow guide or individual SKILL.md files
- Update docs/install.md to point to this doc instead of "a later issue"

Acceptance criteria
- docs/claude-code-guide.md exists and is well-structured
- The doc covers all listed topics: plan mode, skill invocation, approve-then-implement, common pitfalls
- docs/install.md reference is updated to link to the new guide
- No duplication with the workflow guide or SKILL.md files

Scope and constraints
- Primary folders to touch: `docs/`
- Folders to avoid unless absolutely necessary: `skills/`, `templates/`, `design/`
- Keep the doc practical and concise — prefer examples over abstract descriptions
- Do not rewrite or restructure existing docs beyond updating the install.md reference

Evaluation & testing requirements
- Verify all listed topics are covered in the guide
- Verify docs/install.md now links to the new guide
- Confirm no content duplication with generic-project-workflow.md or SKILL.md files
- Check that all internal links resolve correctly

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-019-claude-code-guide.md`
   - `generic-project-workflow.md`
   - `docs/install.md`
   - existing SKILL.md files under `skills/`
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the structure and sections of the new guide,
   - what content goes in each section,
   - what changes are needed in docs/install.md,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not restructure existing docs beyond what is required.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed,
   - exact commands I should run to inspect the results.

Do not start editing files until I explicitly approve your plan.
