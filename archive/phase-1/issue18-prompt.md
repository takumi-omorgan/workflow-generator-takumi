You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-016-changelog-skill.md`
- Decision: Build a /changelog skill that auto-generates release notes from git history.

GitHub Issue:
- Title: Build /changelog skill (ADR-016)
- Number: #18
- Milestone: M5 - v-next
- Labels: feature, design

Goal
Build the /changelog skill that auto-generates release notes from git history between two refs, grouped by type, ADR, and issue.

Why it matters
Manually writing release notes is tedious and error-prone. A skill that parses git history and groups changes by verb, ADR reference, and issue number produces consistent, readable changelogs that keep stakeholders informed without extra effort from the developer.

Requirements
- Parse `git log` between two refs (tags, SHAs, or since-last-release)
- Group commits by verb (add, fix, update, refactor, etc.), ADR reference, and issue number
- Output formatted markdown suitable for release notes
- Support multiple output targets: stdout, file, and GitHub Release body
- Handle squash merges gracefully (extract meaningful info from squash commit messages)
- Support a `--since-last-release` convenience flag that auto-detects the latest tag

Acceptance criteria
- The skill produces readable, well-grouped changelog output
- Grouping by verb/ADR/issue is correct and consistent
- Squash merge commits are handled without producing garbled output
- All three output targets (stdout, file, GitHub Release body) work correctly
- The skill handles repos with no tags, no commits in range, or unconventional commit messages gracefully

Scope and constraints
- Primary folders to touch: `skills/changelog/`
- Folders to avoid unless absolutely necessary: other skills, templates, docs
- Keep the skill focused on changelog generation; do not add release tagging or publishing logic (that belongs in the /release skill)
- Do not require a specific commit message convention beyond what the repo already uses

Evaluation & testing requirements
- Verify correct grouping with a sample git history containing mixed commit types
- Test the `--since-last-release` flag with and without existing tags
- Confirm file output writes correctly and stdout output is clean
- Test with a repo that uses squash merges
- All existing tests must continue to pass

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-016-changelog-skill.md`
   - `generic-project-workflow.md`
   - any existing skills in `skills/` for structure conventions
   - the current git log to understand commit message patterns in this repo
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files and folders you will create,
   - how git log is parsed and commits are grouped,
   - how each output target is handled,
   - how squash merges are detected and processed,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing ADR-016 and issue #18,
   - write tests alongside implementation.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed,
   - exact commands I should run to verify the skill.

Do not start editing files until I explicitly approve your plan.
