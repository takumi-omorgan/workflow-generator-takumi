# Build-Out Plan (archived)

> **Archived — historical only.** This is the original build-out
> plan for the Claude Code Workflow Kit, written before any
> implementation work began. It defined the M1–M5 milestone
> structure that drove the initial build, the eight core skills
> shipped in v1, and the phase-by-phase exit criteria. Most of its
> content has since been superseded by the shipped artefacts and
> the ADRs accepted along the way.
>
> For current direction, read these instead:
>
> - [`README.md`](../README.md) — positioning and what the kit is today
> - [`docs/workflow-guide.md`](../docs/workflow-guide.md) — the action-oriented walkthrough
> - [`docs/skills.md`](../docs/skills.md) — the functional skill reference
> - [`design/adr/`](../design/adr/) — accepted decisions
>
> This file is kept only as audit trail for the kit's original plan.

---

## Objective

Build the first release of the **Claude Code Workflow Kit** as a GitHub-distributed, project-local toolkit for **new software projects**. The kit should help a user start from either a rough idea, a standard PRD, or a custom PRD format and generate a practical GitHub-first workflow using Claude Code, ADRs, issues, pull requests, and lightweight deployment guidance.

## Build strategy

The product should be built in a strict order:

1. define the repository structure,
2. capture the key architectural decisions as ADRs,
3. write the core documentation and templates,
4. create the initial Claude Code skills,
5. test the kit on a sample new project,
6. refine the wording and usage model based on that dry run.

This keeps the workflow aligned with your design-governance-first approach and avoids writing skills before the operating model is stable.

## Scope of this build plan

This build-out plan covers the first release only. It assumes:

- new projects only,
- project-local installation in the target repo,
- one install per new project,
- GitHub-first workflow,
- Claude Code as the primary implementation environment,
- and no support for adapting existing projects in v1.

## Success criteria

The first release is successful if a user can:

1. create a new project repository,
2. install the workflow kit into that project,
3. follow the setup documentation,
4. choose a starting path: no PRD, standard PRD, or custom PRD,
5. generate core planning artifacts,
6. set up the GitHub workflow structure,
7. and begin implementing issue-by-issue in Claude Code.

## Recommended repository structure

The kit repository should be structured so it is easy to copy or install into a new target project.

```text
claude-code-workflow-kit/
  README.md
  CLAUDE.md
  docs/
    install.md
    github-setup.md
    workflow-guide.md
    adr-guide.md
    claude-code-guide.md
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
  templates/
    adr-template.md
    issue-template.md
    pr-template.md
    claude-md-template.md
    ai-summary-template.md
    mvp-template.md
    build-out-plan-template.md
  examples/
    idea-only-example.md
    standard-prd-example.md
    custom-prd-example.md
    sample-adr.md
    sample-issue.md
```

This structure keeps the product understandable and mirrors the way the workflow separates planning, design decisions, implementation prompts, and review artifacts.

## Delivery phases

## Phase 1 — Foundation

### Goal

Define the repository, installation model, and core workflow assumptions before writing skills.

### Deliverables

- final MVP spec,
- build-out plan,
- initial repo structure,
- core README outline,
- and initial ADR list.

### Tasks

- Confirm the product boundary: new projects only, project-local install only.
- Define the exact target-project installation pattern.
- Decide which files are copied into the target project versus kept only in the kit repo.
- Define naming conventions for skills, templates, and generated files.
- Draft the setup sequence the user follows on first install.

### Exit criteria

- product boundary is stable,
- install model is documented,
- repo structure is fixed enough to support ADRs and skills.

## Phase 2 — Core ADRs

### Goal

Create the initial architecture decisions that govern the rest of the build. ADRs should be written before creating the full skill set, because they define how the kit is packaged and used.

### Required ADRs

1. **ADR-001 — Project-local installation model**  
   The kit is installed into each new target project; no global install is required in v1.

2. **ADR-002 — New-project-only scope**  
   The first release supports greenfield adoption only and explicitly excludes retrofitting existing repos.

3. **ADR-003 — PRD intake model**  
   The kit supports three starts: no PRD, standard PRD, and custom PRD.

4. **ADR-004 — GitHub-first workflow model**  
   The generated workflow assumes GitHub issues, labels, PRs, and `main + feature branch`.

5. **ADR-005 — Documentation and template architecture**  
   Core docs and templates are generated into the target repo using a consistent structure.

6. **ADR-006 — Claude Code execution model**  
   Implementation work is issue-by-issue, plan-first, test-alongside-code, evaluation-at-end.

### Exit criteria

- all six ADRs exist in draft or accepted form,
- the workflow assumptions are no longer ambiguous,
- skill authoring can proceed from stable decisions.

## Phase 3 — Documentation layer

### Goal

Write the documentation that explains how the kit is installed, configured, and used before trying to make the skills do everything automatically.

### Required documents

- `README.md`
- `docs/install.md`
- `docs/github-setup.md`
- `docs/workflow-guide.md`
- `docs/adr-guide.md`
- `docs/claude-code-guide.md`

### Documentation content

#### `README.md`

Should explain:

- what the kit is,
- who it is for,
- that it is for new projects only,
- that it uses a project-local install model,
- and the quick-start sequence.

#### `docs/install.md`

Should explain:

- prerequisites: Git, GitHub CLI, Claude Code, optional Node.js depending on project type,
- how to create a new project repo,
- how to install the kit into that target project,
- where `.claude/skills/` should live,
- and that each new project gets a fresh install.

#### `docs/github-setup.md`

Should explain:

- GitHub repo creation,
- `gh auth login`,
- SSH setup or equivalent auth setup,
- labels,
- milestones,
- PR templates,
- issue templates,
- branch naming,
- optional branch protection,
- and how Claude Code works with the repo workflow.

#### `docs/workflow-guide.md`

Should explain the end-to-end path:

- idea or PRD,
- MVP summary,
- ADRs,
- issue backlog,
- Claude Code implementation,
- PR review,
- merge,
- deploy.

#### `docs/adr-guide.md`

Should explain:

- what ADRs are,
- when to write them,
- lightweight status model,
- the chosen template,
- and examples.

#### `docs/claude-code-guide.md`

Should explain:

- how to use the installed skills,
- how to maintain `CLAUDE.md`,
- how to fill and use issue prompts,
- why plan-before-code matters,
- how to provide evaluation summaries at the end of work.

### Exit criteria

- a user can install and understand the kit without guessing,
- the installation and workflow model are explicit,
- the skills have a documentation baseline to reference.

## Phase 4 — Templates

### Goal

Create the starter artifacts the skills will generate or adapt.

### Required templates

- `templates/adr-template.md`
- `templates/issue-template.md`
- `templates/pr-template.md`
- `templates/claude-md-template.md`
- `templates/ai-summary-template.md`
- `templates/mvp-template.md`
- `templates/build-out-plan-template.md`

### Template requirements

#### ADR template
Should support:
- title,
- status,
- context,
- options considered,
- decision,
- consequences.

#### Issue template
Should support:
- title,
- problem,
- goal,
- requirements,
- acceptance criteria,
- scope,
- labels,
- milestone.

#### PR template
Should support:
- summary,
- ADR link,
- changes,
- test results,
- manual verification,
- closes issue reference.

#### `CLAUDE.md` template
Should include:
- project summary,
- stack,
- repo conventions,
- testing commands,
- dependency/versioning rules,
- secrets guidance,
- review expectations.

### Exit criteria

- templates are clear enough to be useful even without advanced skill automation,
- every major generated file has a starter template.

## Phase 5 — Core skills v1

### Goal

Implement the smallest set of skills that makes the kit truly useful.

### Skill order

#### 1. `idea-to-prd`
Why first: supports the “no PRD” start path and removes the biggest writing burden.

#### 2. `prd-normalizer`
Why second: supports both standard and custom PRD formats.

#### 3. `prd-to-mvp`
Why third: converts planning input into a scoped MVP statement.

#### 4. `adr-writer`
Why fourth: lets the user capture key decisions before issue planning.

#### 5. `issue-planner`
Why fifth: converts the MVP and accepted ADRs into implementable GitHub issues.

#### 6. `workflow-docs`
Why sixth: writes `README.md`, `CLAUDE.md`, and the AI summary.

#### 7. `claude-issue-executor`
Why seventh: supports execution once setup and planning are done.

#### 8. `pr-review-packager`
Why eighth: closes the loop with a clean review and merge process.

### Skill design rules

Each skill should:

- have a narrow purpose,
- state inputs clearly,
- state outputs clearly,
- avoid hidden assumptions,
- and reference the target project files it should read or update.

Each skill should also assume the project is already using the kit locally and should not try to perform migration of older repos.

### Exit criteria

- all eight v1 skills exist,
- each skill has a clearly defined purpose,
- the kit supports all three starting modes,
- the workflow can go from planning to issue execution.

## Phase 6 — Example projects and dry runs

### Goal

Prove that the kit works in real usage, not just in theory.

### Required example flows

1. **Idea-only example**  
   Start with a one-paragraph idea and generate the project workflow.

2. **Standard PRD example**  
   Start with a conventional PRD and produce the workflow artifacts.

3. **Custom PRD example**  
   Start with mixed notes and normalize them before generating the workflow.

### Dry-run validation

For each example, confirm that the kit can produce:

- MVP summary,
- build-out plan,
- ADRs,
- issue backlog,
- `README.md`,
- `CLAUDE.md`,
- and issue prompt support.

### Exit criteria

- all three example modes work,
- the docs and skills make sense for a first-time user,
- confusing steps are identified and fixed.

## Phase 7 — GitHub workflow assets

### Goal

Package the GitHub-specific parts that make the workflow concrete.

### Deliverables

- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/feature-request.md`
- label recommendations
- milestone guidance
- branch naming guidance
- optional branch protection guidance

### Notes

These assets do not need to be automatically pushed to GitHub in v1. The user can copy them into the repo and apply the settings manually.

### Exit criteria

- the kit includes enough GitHub-specific material to make the workflow actionable.

## Phase 8 — Final packaging

### Goal

Prepare the repository for public or private reuse.

### Deliverables

- polished README,
- installation instructions,
- usage examples,
- release notes,
- version tag,
- and a clear statement of scope and non-goals.

### Final checklist

- new-project-only positioning is explicit,
- project-local install is explicit,
- all three PRD entry paths are documented,
- skill names and templates are consistent,
- GitHub setup instructions are complete,
- and the issue-execution model matches the plan-first workflow.

## GitHub milestone recommendation

I would organize the work into these milestones:

| Milestone | Focus |
|---|---|
| M1 | Foundation + ADRs |
| M2 | Docs + templates |
| M3 | Planning skills |
| M4 | Execution skills |
| M5 | Example projects + packaging |

This keeps the early work mostly architectural and documentation-driven before skill complexity increases.

## Suggested issue backlog

### Milestone M1 — Foundation + ADRs
- Create repo skeleton
- Write final MVP spec into repo
- Draft ADR-001 through ADR-006
- Approve installation model and scope
- Define generated file structure

### Milestone M2 — Docs + templates
- Write README
- Write install guide
- Write GitHub setup guide
- Write workflow guide
- Write ADR guide
- Write Claude Code guide
- Create all template files

### Milestone M3 — Planning skills
- Implement `idea-to-prd`
- Implement `prd-normalizer`
- Implement `prd-to-mvp`
- Implement `adr-writer`
- Implement `issue-planner`

### Milestone M4 — Execution skills
- Implement `workflow-docs`
- Implement `claude-issue-executor`
- Implement `pr-review-packager`

### Milestone M5 — Examples + packaging
- Create idea-only example
- Create standard PRD example
- Create custom PRD example
- Run dry-run validation
- Refine docs from test findings
- Tag v0.1.0

## Testing strategy

The product is mostly documentation, templates, and skill behavior, so testing should focus on:

- correctness of generated file structure,
- clarity of instructions,
- consistency of outputs,
- and successful dry-run use on example projects.

### Test categories

- **Documentation tests** — can a new user follow the install and setup docs without guesswork?
- **Template tests** — do templates produce sensible files with minimal manual editing?
- **Skill behavior tests** — do skills produce the expected outputs for each start mode?
- **Workflow tests** — can a user move from planning to issue execution cleanly?
- **GitHub workflow tests** — are the labels, issue structures, PR structure, and branch guidance practical?

## Implementation conventions

The build should follow these conventions:

- keep artifacts in markdown where possible,
- keep skills small and composable,
- avoid broad “do everything” skills,
- make generated file paths explicit,
- and preserve plan-before-code discipline in anything related to execution.

## Risks and mitigations

### Risk 1 — Too much scope in v1
Mitigation: keep the boundary strict: new projects only, no migration support, no hosted UI.

### Risk 2 — Skills become vague
Mitigation: define narrow responsibilities and clear expected outputs for each skill.

### Risk 3 — Documentation is still too implicit
Mitigation: write install and GitHub setup docs before relying on skills to explain usage.

### Risk 4 — The workflow feels too heavy
Mitigation: keep ADRs lightweight, issues focused, and templates concise.

## Recommended immediate next actions

1. Add this build-out plan to the Space.
2. Draft ADR-001 through ADR-006.
3. Finalize the repository structure.
4. Write the install guide and GitHub setup guide first.
5. Then begin writing the planning skills in order.

## Acceptance criteria

This build-out plan is acceptable when it:

- matches the revised MVP direction,
- assumes project-local installation per new project,
- excludes existing-project adaptation,
- defines phases in implementation order,
- identifies the initial ADRs,
- includes documentation and template work before advanced skills,
- and provides a practical milestone and issue structure for GitHub.


