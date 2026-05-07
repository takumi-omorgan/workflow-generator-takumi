# MVP Spec (archived)

> **Archived — historical only.** This is the original MVP spec for
> the Claude Code Workflow Kit, written before the kit was built. It
> framed the initial scope and the first six ADRs (ADR-001 through
> ADR-006) but is no longer the authoritative source. The kit has
> since grown well beyond the eight core skills described here — it
> now ships 19 skills, with milestone-lifecycle, session-continuity,
> and quality-gate additions — and several structural decisions have
> evolved through later ADRs.
>
> For current direction, read these instead:
>
> - [`README.md`](../README.md) — positioning and what the kit is today
> - [`docs/workflow-guide.md`](../docs/workflow-guide.md) — the action-oriented walkthrough
> - [`docs/skills.md`](../docs/skills.md) — the functional skill reference
> - [`design/adr/`](../design/adr/) — accepted decisions
>
> This file is kept only as audit trail for the kit's original framing.

---

## Product name

**Claude Code Workflow Kit**

A GitHub-distributed toolkit of Claude Code skills, templates, starter documents, and workflow guides that helps a solo developer or small team set up a GitHub-first software delivery workflow for a **new project** using ADRs, issues, pull requests, testing, and deployment checklists.

## Product goal

The product helps users go from:

- a rough idea with no PRD,
- a PRD written in a standard format,
- or a user-defined PRD in their own format,

to a structured, implementation-ready workflow for building a **new software project** with Claude Code and GitHub.

The MVP should minimize manual writing by providing reusable project-local Claude Code skills that generate or refine the key planning and delivery artifacts inside the target repository.

## Product type

This MVP is **not a standalone app**. It is a **downloadable GitHub repository** containing:

- Claude Code skills,
- templates,
- example files,
- starter documentation,
- and setup instructions.

The intended usage model is:

- create or open a new target project,
- install the workflow kit into that project,
- use the skills from inside that project,
- generate the project workflow artifacts there,
- and repeat this process for each new project.

## Installation model

The MVP should use a **project-local installation model**.

That means:

- the user installs the kit into the target project directory,
- the active skills live in that project’s `.claude/skills/` folder,
- the generated docs are written into that same repository,
- and each new project gets its own fresh install of the kit.

This model should be treated as the default and explicitly documented throughout the product.

The MVP should **not** require users to manage a global skill library.

Global or reusable personal installation can be considered in a later iteration.

## Target users

### Primary user

A solo technical founder, indie hacker, or experienced developer who wants to:

- move quickly,
- use Claude Code heavily,
- keep architectural decisions traceable,
- work in GitHub,
- and avoid inventing a workflow from scratch for every new project.

### Secondary user

A small software team or consultant who wants a reusable, low-ceremony operating system for GitHub-based delivery with Claude Code.

## Core problem

Most developers can describe what they want to build, but they do not want to manually write and maintain:

- PRDs,
- ADRs,
- GitHub issues,
- Claude Code prompts,
- `README.md`,
- `CLAUDE.md`,
- PR templates,
- issue templates,
- and deployment or review checklists.

Existing tools often focus only on planning or only on coding. This product bridges the gap by packaging a practical workflow directly as Claude Code skills and project templates.

## Product principles

1. **New projects only**  
   The MVP is for setting up the workflow at the beginning of a new project, not for adapting an existing codebase.

2. **Claude Code first**  
   The MVP is explicitly designed around Claude Code as the primary implementation environment.

3. **GitHub first**  
   The workflow assumes GitHub repositories, issues, branches, pull requests, and optional GitHub integration setup.

4. **Project-local by default**  
   The kit is installed into each target project rather than globally.

5. **Docs first, but lightweight**  
   The kit should generate useful documents without enterprise ceremony.

6. **Minimal user writing**  
   The user should be able to start from a rough idea and let the kit generate most of the project documentation.

## MVP scope

The MVP includes:

1. Claude Code skills for planning and workflow setup,
2. support for starting with or without a PRD,
3. support for standard-format and user-defined PRDs,
4. project-local installation into a new target repository,
5. starter templates for project docs and GitHub workflow files,
6. documentation for GitHub and Claude Code setup,
7. examples and sample project flows,
8. and a recommended project structure for new repos.

The MVP does **not** include:

- a standalone web UI,
- a hosted service,
- adapting existing projects to this workflow,
- global skill installation as the primary model,
- direct cloud sync,
- team collaboration features,
- or a generic tool-agnostic workflow product.

## User starting modes

The product should support three starting paths.

### Mode 1 — No PRD yet

The user starts with a rough idea or short description.

The kit should include a skill that helps the user:

- clarify the idea,
- draft a lightweight PRD,
- identify scope boundaries,
- and convert the result into a practical MVP definition.

### Mode 2 — Standard-format PRD

The user already has a PRD in a recognized structure.

Examples include:

- product overview,
- goals,
- target users,
- requirements,
- non-goals,
- and success criteria.

The kit should include a skill that reads this format, extracts the implementation implications, and turns it into workflow artifacts.

### Mode 3 — User-defined PRD format

The user has an informal or custom document format.

This may be:

- markdown notes,
- a long-form design document,
- rough bullet points,
- or mixed project notes.

The kit should include a skill that normalizes the input into a structured internal planning format before generating ADRs, issues, and prompts.

## Primary outputs

The MVP should generate a practical **workflow starter pack** inside the target repo.

### Workflow starter pack contents

1. **MVP summary**
2. **Build-out plan**
3. **ADR set**
4. **GitHub issue backlog**
5. **Implementation milestones**
6. **Claude Code issue prompts**
7. **`README.md` draft**
8. **`CLAUDE.md` draft**
9. **AI-readable summary document**
10. **PR template draft**
11. **Issue template draft**
12. **Deploy checklist**
13. **Review checklist**

## Core skills

The MVP should include a small set of focused Claude Code skills.

### 1. `idea-to-prd`

Helps users start without a PRD.

Responsibilities:

- ask clarifying questions,
- define user/problem/scope,
- generate a lightweight PRD,
- and produce a clean MVP statement.

### 2. `prd-normalizer`

Accepts either a standard PRD or a user-defined format.

Responsibilities:

- analyze the input,
- normalize it into a consistent structure,
- highlight missing information,
- and produce a concise implementation-ready summary.

### 3. `prd-to-mvp`

Turns the PRD or normalized summary into an MVP plan.

Responsibilities:

- identify scope boundaries,
- separate must-have vs later,
- suggest delivery phases,
- and define the likely implementation path.

### 4. `adr-writer`

Generates ADR drafts for major architectural and workflow decisions.

Responsibilities:

- identify ADR-worthy decisions,
- draft context/options/decision/consequences,
- and keep ADRs small and traceable.

### 5. `issue-planner`

Converts the MVP and accepted ADRs into GitHub issues and milestones.

Responsibilities:

- define issue order,
- split large work into smaller issues,
- add acceptance criteria,
- and suggest labels and milestone grouping.

### 6. `claude-issue-executor`

Supports the implementation workflow inside Claude Code.

Responsibilities:

- use the filled issue prompt format,
- require plan-before-code,
- write tests alongside implementation,
- and produce an evaluation summary at the end.

### 7. `workflow-docs`

Generates or updates project documentation.

Responsibilities:

- write `README.md`,
- write `CLAUDE.md`,
- write the AI-readable project summary,
- and write workflow support docs for the new repo.

### 8. `pr-review-packager`

Prepares pull request support artifacts.

Responsibilities:

- summarize changes,
- organize test evidence,
- generate manual verification steps,
- and produce a clean PR-ready summary.

## Core user flow

### Step 1 — Create a new target project

The user creates a new local project directory or clones a newly created repository.

### Step 2 — Install the workflow kit into the target project

The user downloads or clones the workflow kit into the target project and places the skills in `.claude/skills/`.

This must be documented clearly as the standard usage model:

- one install per new project,
- project-local skills,
- project-local generated docs,
- no global installation required.

### Step 3 — Complete environment setup

The user follows the setup guide.

This documentation must include:

- installing Claude Code,
- installing Git and GitHub CLI if needed,
- authenticating GitHub CLI with `gh auth login`,
- creating or choosing a GitHub repository,
- setting up Claude Code and GitHub so the repo workflow can be used effectively,
- and creating a root `CLAUDE.md` so Claude Code has project rules and context.

### Step 4 — Choose a starting mode

The user chooses:

- no PRD,
- standard-format PRD,
- or user-defined PRD.

### Step 5 — Generate planning artifacts

The relevant skills generate:

- MVP summary,
- build plan,
- ADR drafts,
- issue backlog,
- and project documents.

### Step 6 — Set up the repo workflow

The user applies the generated docs and templates to the target repository.

This may include:

- `README.md`,
- `CLAUDE.md`,
- `design/adr/`,
- `design/ai-summary.md`,
- `.github/pull_request_template.md`,
- and issue templates.

### Step 7 — Implement issue by issue

Claude Code works through the backlog using the issue prompt framework and project docs as context.

### Step 8 — Review and merge

The workflow uses:

- focused branches,
- small pull requests,
- test evidence,
- and manual verification where needed.

## Recommended repository structure

The workflow kit should be installed into the target project and create or use a structure like this:

```text
my-project/
  CLAUDE.md
  README.md
  .claude/
    skills/
      idea-to-prd/
        SKILL.md
      prd-normalizer/
        SKILL.md
      prd-to-mvp/
        SKILL.md
      adr-writer/
        SKILL.md
      issue-planner/
        SKILL.md
      claude-issue-executor/
        SKILL.md
      workflow-docs/
        SKILL.md
      pr-review-packager/
        SKILL.md
  design/
    adr/
    ai-summary.md
  docs/
    workflow-guide.md
    github-setup.md
    adr-guide.md
    claude-code-guide.md
  templates/
    adr-template.md
    issue-template.md
    pr-template.md
    mvp-template.md
    build-out-plan-template.md
```

## Documentation requirements

The documentation should be a first-class part of the MVP and must make the installation model explicit.

### Required docs

- **Install guide** — explains that the kit is installed into each new target project and reused per project, not as a global dependency.
- **GitHub setup guide** — repository creation, `gh auth login`, auth basics, labels, branches, PR flow, and any Claude-to-GitHub setup needed.
- **Workflow guide** — the end-to-end process from idea/PRD to ADR to issue to PR to deploy.
- **ADR guide** — what ADRs are, when to write them, lifecycle, template, examples.
- **Claude Code guide** — how to use the skills from inside the target project, how to keep `CLAUDE.md` updated, and how to work issue-by-issue.

## Explicit non-goal

The MVP should **not** include a skill for adapting existing projects to this workflow.

That problem should be deferred because it introduces more ambiguity around legacy structure, inconsistent conventions, missing documents, and partial workflow adoption than is appropriate for a simple first release.

## GitHub-specific guidance

Because the product is GitHub-specific, the docs must explain:

- creating a repository,
- setting `main` as the stable branch,
- using a `main + feature branch` model,
- creating issues from accepted ADRs,
- using labels and milestones,
- opening focused pull requests,
- using PR templates,
- merging and deleting feature branches,
- and optionally enabling branch protection.

## Technical approach

### Delivery model

- GitHub repository distribution
- Markdown-based documentation
- Claude Code skills in project-local `.claude/skills/`
- reusable templates and examples
- no backend

### Project constraints

- must be easy to install into a new project,
- must be understandable to solo developers,
- must not require a separate app to get value,
- and must keep the onboarding path simple.

## Success criteria

The MVP succeeds if a user can:

1. start a new project,
2. install the workflow kit into that project,
3. follow the setup docs,
4. start from either a rough idea or a PRD,
5. generate a usable project documentation pack,
6. create a GitHub-first implementation workflow,
7. and begin working issue-by-issue in Claude Code with minimal manual writing.

## Out of scope

The following are intentionally deferred:

- adapting existing projects,
- global skill installation as the main model,
- a standalone web app,
- a hosted UI,
- generic support for non-Claude AI coding tools,
- multi-user workflow management,
- and polished SaaS-style product surfaces.

## Future phases

### Phase 2

- better install automation for project-local setup,
- richer skill library,
- improved templates for different project types,
- and optional support for promoting some skills into a reusable global library.

### Phase 3

- broader tool support beyond Claude Code,
- optional hosted configuration UI,
- migration tooling for existing repos,
- template marketplace,
- and deeper GitHub automation.

## Launch strategy

The first release should target a narrow use case:

> A solo builder starting a new GitHub project and using Claude Code to turn a rough idea or PRD into a disciplined software delivery workflow with minimal writing.

That keeps the product simple, opinionated, and achievable.

## Acceptance criteria for the MVP spec

The MVP spec is acceptable when it:

- clearly defines the product as a Claude Code skills kit,
- supports no-PRD, standard-PRD, and custom-PRD entry paths,
- uses project-local installation as the default model,
- makes it explicit that each new project gets its own install,
- excludes existing-project adaptation from v1,
- includes GitHub setup and GitHub-specific workflow guidance,
- and can directly drive the repository structure, skills list, ADRs, and implementation plan.


