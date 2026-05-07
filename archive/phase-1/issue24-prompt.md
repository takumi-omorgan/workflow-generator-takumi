You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- None — this is a bookkeeping task to update notes/feature-ideas.md entries from "idea" to "adr-drafted" with ADR links for all 15 entries that now have accepted ADRs.

GitHub Issue:
- Title: Update feature-ideas.md statuses to reflect accepted ADRs
- Number: #24
- Milestone: M5 - v-next
- Labels: chore

Goal
Update all v-next feature-ideas.md entries to reflect their accepted ADR status, so the feature tracking document stays accurate and useful as a quick reference.

Why it matters
The feature-ideas.md file is the central tracking document for planned work. With 15 ADRs now accepted, the entries still showing "idea" status are stale and misleading. Keeping this file current ensures anyone reviewing the project can quickly see what has been scoped and where to find the details.

Requirements
- Update each of the 15 v-next entries in notes/feature-ideas.md from status "idea" to "adr-drafted"
- Add an ADR link to each entry pointing to the corresponding ADR file under design/adr/
- Ensure ADR links are correct and match the right feature entry
- Do not change any other content in the file (descriptions, priorities, etc.)

Acceptance criteria
- All 15 v-next entries in notes/feature-ideas.md show status "adr-drafted"
- Each entry includes a correct link to its corresponding ADR file
- No other content in the file has been changed
- All ADR file references are valid paths

Scope and constraints
- Primary folders to touch: `notes/`
- Folders to avoid unless absolutely necessary: `docs/`, `skills/`, `templates/`, `design/`
- This is a purely mechanical update — do not rewrite descriptions or re-order entries
- Verify ADR filenames by checking the actual files under design/adr/

Evaluation & testing requirements
- Verify all 15 entries have been updated to "adr-drafted"
- Verify each ADR link points to a file that exists
- Confirm no unrelated changes were made to the file
- Cross-check ADR-to-feature mapping for correctness

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `notes/feature-ideas.md`
   - list the files under `design/adr/` to confirm ADR filenames
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the mapping of each feature entry to its ADR file,
   - the format you will use for the ADR link in each entry,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit with a message referencing the issue,
   - do not modify any other files.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any entries that could not be matched to an ADR,
   - exact commands I should run to inspect the results.

Do not start editing files until I explicitly approve your plan.
