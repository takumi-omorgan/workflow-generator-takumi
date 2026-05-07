You are working in my `workflow-kit` repository.

Context:
- This project is a Claude Code Workflow Kit for new software projects.
- It is a GitHub-first, project-local toolkit that helps users go from idea or PRD to MVP scope, ADRs, GitHub issues, Claude Code prompts, templates, and workflow docs.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md`.

ADR:
- File: `design/adr/adr-017-release-skill.md`
- Decision: Build a /release skill for version tagging and GitHub Releases.

GitHub Issue:
- Title: Build /release skill (ADR-017)
- Number: #19
- Milestone: M5 - v-next
- Labels: feature, design

Goal
Build the /release skill for version tagging, release note generation, and GitHub Release creation.

Why it matters
Releases should be consistent, traceable, and low-friction. A dedicated skill that handles semver tagging, calls /changelog for release notes, creates the GitHub Release, and pushes the tag reduces manual steps and ensures every release follows the same process.

Requirements
- Determine next semver version from user input or suggest one based on ADR impact (major for breaking changes, minor for features, patch for fixes)
- Call the /changelog skill to generate release notes for the release body
- Create an annotated git tag with the version and release summary
- Push the tag to the remote
- Create a GitHub Release via `gh release create` with the generated release notes
- Optionally update the build-out plan phase status to reflect the release
- Present the release plan to the user for approval before executing

Acceptance criteria
- The skill produces a tagged release with correct semver version
- Release notes are generated via the /changelog skill and included in the GitHub Release body
- The annotated git tag is created and pushed to the remote
- The GitHub Release is created successfully via `gh release create`
- The user approves the release plan before any tags are created or pushed
- The skill handles edge cases (no changelog skill available, tag already exists, dirty working tree) gracefully

Scope and constraints
- Primary folders to touch: `skills/release/`
- Folders to avoid unless absolutely necessary: `skills/changelog/` (call it, do not modify it), other skills, templates
- Keep the skill focused on the release ceremony; changelog generation is delegated to /changelog
- Do not modify existing tags or force-push tags

Evaluation & testing requirements
- Verify correct semver suggestion logic with different commit/ADR combinations
- Confirm that the /changelog integration produces expected release notes
- Test tag creation and GitHub Release creation in a safe environment (dry-run mode or test repo)
- Confirm the approval gate works (no tag or release created without explicit approval)
- All existing tests must continue to pass

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `design/adr/adr-017-release-skill.md`
   - `generic-project-workflow.md`
   - any existing skills in `skills/` for structure conventions
   - the /changelog skill in `skills/changelog/` for integration points
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - which files and folders you will create,
   - how semver is determined or suggested,
   - how /changelog is called and its output consumed,
   - how the tag and GitHub Release are created,
   - how user approval is handled,
   - your verification plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing ADR-017 and issue #19,
   - write tests alongside implementation.
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed,
   - any follow-up work needed,
   - exact commands I should run to verify the skill.

Do not start editing files until I explicitly approve your plan.
