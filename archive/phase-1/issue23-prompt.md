You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-021-example-starter-projects-gallery.md`
- Decision: Add 2-3 complete worked example projects under examples/ showing the kit end-to-end.

GitHub Issue:
- Title: Add example / starter projects gallery (ADR-021)
- Number: #23
- Milestone: M5 - v-next
- Labels: docs, feature

Goal
Add 2-3 complete worked example projects under examples/ that demonstrate the full workflow kit end-to-end, giving users concrete references they can study and adapt.

Why it matters
Users learn best from examples. Having complete worked projects that show every artifact — from initial PRD through shipped PR — makes the kit dramatically easier to adopt. Without examples, users must imagine how the pieces fit together.

Requirements
- Create 2-3 small example projects under examples/ (e.g., a CLI utility, a web app, a library)
- Each example includes the full artifact set: PRD, MVP spec, ADRs, issues, PRs
- Projects are kept deliberately small to stay readable
- Each example demonstrates the full workflow from install to shipped PR
- Update README.md to reference the new examples directory and its contents

Acceptance criteria
- 2-3 complete example projects exist under examples/
- Each example includes PRD, MVP spec, ADRs, issues, and PR artifacts
- Each example is small enough to read through in one sitting
- Each example demonstrates the full workflow from idea to shipped PR
- README.md is updated to reference the examples

Scope and constraints
- Primary folders to touch: `examples/`
- Folders to avoid unless absolutely necessary: `skills/`, `templates/`, `design/`, `docs/`
- Keep each example minimal — the goal is to show the workflow, not to build real software
- Use realistic but simple project ideas that are easy to follow
- Do not modify the kit's core files; only add example content and update README.md

Evaluation & testing requirements
- Verify each example contains all required artifacts (PRD, MVP spec, ADRs, issues, PRs)
- Verify the examples are internally consistent (ADRs reference the MVP spec, issues reference ADRs, etc.)
- Confirm README.md links to the examples directory
- Check that examples are small and self-contained

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-021-example-starter-projects-gallery.md`
   - `generic-project-workflow.md`
   - `README.md`
   - existing content under `examples/` if any
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which example projects you will create and why,
   - which artifacts each example will include,
   - the folder structure under examples/,
   - what changes are needed in README.md,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue,
   - do not modify kit core files beyond updating README.md.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed,
   - exact commands I should run to inspect the results.

Do not start editing files until I explicitly approve your plan.
