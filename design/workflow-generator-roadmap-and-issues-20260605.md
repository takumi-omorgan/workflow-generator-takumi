# Workflow Generator Kit Roadmap and Issue Backlog

## Executive summary

This roadmap converts the repository review into an execution plan for making the workflow generator kit easier for humans to adopt and easier for AI agents to operate deterministically. The recommended strategy is to dogfood the roadmap: turn this document into the seed backlog for the kit, run the kit’s own planning and execution workflow against it, and measure whether the experience improves with each milestone.

The roadmap is organized around six milestones. M0 establishes baseline health before feature work begins. M1 reduces front-door friction for human users. M2 introduces a machine-readable contract layer for agents. M3 unifies workflow control, state, approval gates, and major feature expansion through follow-up PRDs. M4 hardens the system through validation, receipts, and self-tests. M5 adds an AI PR review capability that can use OpenRouter or another model API to review GitHub PRs and optionally publish review comments. Each issue below is written so it can be copied into GitHub as an issue, or adapted into the kit’s own PRD-to-MVP and issue-planning flow.

## Dogfood strategy

The roadmap should be executed through the workflow generator kit itself. That means the first improvement loop should not only ship changes, but also test whether the kit can manage its own evolution with less friction than before.

### Dogfood loop

1. **Create a roadmap PRD**: Convert this document into `design/prd.md`, `design/roadmap-prd.md`, or a dedicated PRD addendum using the existing `/prd-normalizer` flow.
2. **Run M0 before feature work**: Audit health, install behavior, docs drift, and skill-contract drift before changing the user-facing workflow.
3. **Create ADRs for structural decisions**: Use `/adr-writer` for the decisions that reshape the kit, especially `kit.json`, user-facing verbs, approval gates, feature PRD addenda, and state-machine semantics.
4. **Generate issues in milestone batches**: Use `/issue-planner` to create GitHub issues for M0 first, then M1. Do not create the entire roadmap as issues until the first dogfood pass has taught you what needs to change.
5. **Run the first PR through the current kit**: Pick the smallest safe issue, likely the `Design` casing fix or a baseline-health note, and run `/prepare-issue`, `/claude-issue-executor`, and `/pr-review-packager`.
6. **Capture friction as first-class evidence**: Every time the kit feels confusing while improving itself, capture the problem in `notes/eval-issue-NNN.md` and carry it forward.
7. **Repeat after each milestone**: The success metric is not only whether the changes ship, but whether the next milestone requires fewer manual decisions, fewer remembered commands, and less prose interpretation.

### Dogfood rules

- **Use the current kit before improving it**: The first one or two issues should be executed with the current workflow to establish a baseline.
- **Measure time-to-first-PR**: Record elapsed time from issue selection to PR creation for the first dogfood run.
- **Prefer real workflow pain over speculative polish**: If dogfooding reveals a friction point not listed here, promote it above lower-priority roadmap work.
- **Separate human and agent evidence**: Note whether friction was caused by human confusion, agent ambiguity, or both.
- **Do not batch too much**: Keep early PRs small so the kit’s review and carry-forward mechanisms are exercised frequently.
- **Claude Code should implement, not govern, at first**: Let Claude Code work autonomously inside one bounded issue at a time, but keep milestone selection, PR approval, and merge decisions manual until M2 and M3 make the workflow more machine-readable.
- **No unreviewed milestone sweeps**: Do not ask Claude Code to complete a whole milestone unattended until M0, M1, minimal `kit.json`, and the canonical approval-gate work have landed.

## Roadmap overview

| Milestone | Theme | Outcome | Primary audience | Suggested scope |
|---|---|---|---|---|
| M0 | Baseline health and drift audit | The kit’s current defects, test status, install behavior, and contract drift are known before roadmap feature work begins | Maintainers and agents | 1-3 PRs |
| M1 | Front-door simplification | A new human user can install the kit, understand the happy path, and create a first PR without reading the full reference docs | Humans | 2-4 PRs |
| M2 | Machine-readable agent contract | An agent can discover skills, permissions, inputs, outputs, and next steps from structured data rather than prose | AI agents | 3-5 PRs |
| M3 | Unified workflow control and feature expansion | Plan gates, approval semantics, resume behavior, and follow-up PRDs become one coherent stateful flow | Both | 4-6 PRs |
| M4 | Reliability and self-testing | The kit validates its own schemas, credentials, idempotency, and dogfood metrics | Both | 3-5 PRs |
| M5 | AI PR review integration | Users can run an external-model PR review and safely publish GitHub review comments with explicit approval | Humans and agents | 4-6 PRs |

## Now / Next / Later plan

### Now: Stabilize, then make the first experience smaller

The immediate goal is to establish a reliable baseline, then reduce cognitive load before changing the architecture. This includes auditing existing health and drift, simplifying the README, adding a first-PR tutorial, reducing required template placeholders, fixing obvious doc defects, and introducing a dogfood measurement ritual.

### Next: Add the machine layer

The next phase should introduce `kit.json` or equivalent, enrich skill metadata, and define a standard JSON envelope and exit-code convention for programmatic surfaces. This does not require rewriting the slash-command UX; it creates a lower-level contract that agents and scripts can rely on.

### Later: Turn the kit into a self-validating workflow system and add AI review

The later phase should unify approval gates, make state actionable, add idempotency receipts, centralize carry-forward schemas, introduce CI/self-tests that prove the kit can run on itself without drift, and add a provider-agnostic AI PR review workflow with safe comment publishing.

## Milestone M0: Baseline health and drift audit

### Goal

Identify features, bugs, refactors, and documentation drift that should be resolved before executing the main roadmap. M0 is a stabilizing gate: it prevents the roadmap from building new abstractions on top of unresolved defects or inconsistent contracts.

### Success metrics

- A baseline health note exists and lists what passed, what failed, and what was not tested.
- Installer idempotency has been tested from a fresh repository and a rerun.
- Existing skill metadata, handoffs, permission categories, and docs have been audited for drift.
- Known low-risk defects are either fixed or captured as issues.
- The first dogfood run has a recorded time, command count, and friction log.

### Issues

#### Issue M0-1: Run and document baseline self-check

**Priority:** P0  
**Audience:** Maintainers and agents  
**Type:** Baseline / test  

**Problem:** The roadmap assumes the kit is healthy enough to improve, but the current test/script/docs baseline needs to be recorded before changes begin.

**Proposal:** Run existing checks, scripts, install smoke tests, markdown validation if available, and any documented verification commands. Record results in a baseline note such as `notes/baseline-health.md`.

**Acceptance criteria:**

- Given the repository has existing checks or scripts, when they are run, then pass/fail/not-run status is recorded.
- Given a check fails, then the failure is either fixed in a small PR or converted into a follow-up issue.
- Given no check exists for an important path, then the gap is explicitly recorded.
- Given Claude Code is executing this issue, then it does not start roadmap feature work until the baseline is documented.

**Dogfood note:** This should be the first Claude Code issue. It tests whether the current workflow can handle a non-feature maintenance task.

#### Issue M0-2: Audit skill metadata, permission, and handoff drift

**Priority:** P0  
**Audience:** AI agents and maintainers  
**Type:** Drift audit / architecture readiness  

**Problem:** Before adding `kit.json`, the current source materials may already disagree about skill names, permission categories, handoff order, or required inputs and outputs.

**Proposal:** Audit all skills and relevant docs for inconsistencies in names, permission categories, handoff sections, input assumptions, output files, and next-step guidance.

**Acceptance criteria:**

- Given each `SKILL.md` exists, then its name, description, permission category, handoff section, and implied outputs are captured in an audit table.
- Given docs describe a workflow order, then the order is compared against skill handoff sections.
- Given drift is found, then each inconsistency is classified as blocking, low-risk fix, or deferred.
- Given M2 work begins, then known blocking drift has been resolved or deliberately accepted.

**Dogfood note:** This issue produces the source evidence for `kit.json` and should precede Issue 6.

#### Issue M0-3: Audit installer idempotency and fresh-start behavior

**Priority:** P0  
**Audience:** Human users and agents  
**Type:** Installer / reliability  

**Problem:** The installer is the first trust boundary. If fresh installs or reruns are confusing, M1 documentation changes may hide rather than solve real problems.

**Proposal:** Test the installer from a fresh repository and rerun it against the same repository. Record whether prompts, generated files, default values, and rerun behavior are safe and predictable.

**Acceptance criteria:**

- Given a fresh repository, when the installer runs, then generated files and prompts are recorded.
- Given the installer is rerun, then file changes are either zero or clearly expected and documented.
- Given unresolved template placeholders are produced, then they are classified as required, optional, or defective.
- Given installer behavior conflicts with README or install docs, then the drift is captured.

#### Issue M0-4: Fix known low-risk defects before roadmap feature work

**Priority:** P1  
**Audience:** Humans and agents  
**Type:** Bugfix / docs cleanup  

**Problem:** Small defects and stale references create noise during dogfooding and can make later UX changes harder to evaluate.

**Proposal:** Fix low-risk defects found during the baseline audit, including stale path casing, broken command examples, outdated references, and missing prerequisites.

**Acceptance criteria:**

- Given a low-risk defect has an obvious correction, then it is fixed before M1 feature work.
- Given a defect requires design judgment, then it is moved to a regular roadmap issue rather than bundled into cleanup.
- Given a correction changes user-visible workflow, then it is documented in the PR body.

#### Issue M0-5: Create first dogfood baseline report

**Priority:** P0  
**Audience:** Humans and agents  
**Type:** Dogfood / measurement  

**Problem:** The roadmap needs a baseline for time, command count, confusion points, and agent ambiguity before improvements can be evaluated.

**Proposal:** Execute one small real issue using the current kit and record the workflow path, elapsed time, commands used, manual interventions, approval moments, and friction points.

**Acceptance criteria:**

- Given one small issue is selected, when the current kit flow is used, then the full path from issue selection to PR package is recorded.
- Given friction occurs, then it is classified as human confusion, agent ambiguity, missing tool support, or documentation drift.
- Given the first dogfood PR is complete, then the baseline report identifies at least three measurable improvements to check after M1 or M2.

**Claude Code instruction:** Do not optimize the workflow while running this baseline. Record pain honestly; improvements belong in later issues.

## Milestone M1: Front-door simplification

### Goal

Reduce time-to-first-success for human users. A new user should understand what the kit does, install it, and create a first PR without reading ADRs or the full workflow guide.

### Success metrics

- README is under 150 lines.
- Quick start has one recommended install path.
- A new user can complete the tutorial PR in under 30 minutes.
- The happy-path tutorial uses no more than five user-facing commands.
- Day-one setup does not require speculative answers to unknown project details.

### Issues

#### Issue 1: Simplify README around one recommended install path

**Priority:** P0  
**Audience:** Human users  
**Type:** Documentation / onboarding  

**Problem:** The README currently asks users to evaluate multiple install paths and absorb too much workflow detail before getting value.

**Proposal:** Rewrite the README as a short front door: who the kit is for, one recommended install path, the first-PR tutorial link, a compact workflow overview, and links to deeper docs.

**Acceptance criteria:**

- Given a new user lands on the README, when they read the Quick Start, then they see exactly one recommended install command.
- Given a user wants safer/manual install options, when they follow the install docs link, then alternatives are available outside the README.
- Given `wc -l README.md` is run, then the README is below 150 lines or there is a deliberate documented reason it is not.
- Given ADR references are not necessary for onboarding, then parenthetical ADR citations are absent from the README happy path.

**Dogfood note:** Use the current kit to create and execute this issue first or second. Record where the workflow itself feels over-documented.

#### Issue 2: Add a “first PR in 15 minutes” tutorial

**Priority:** P0  
**Audience:** Human users  
**Type:** Documentation / tutorial  

**Problem:** The kit has strong reference material and examples, but no minimal copy-paste tutorial that proves the happy path quickly.

**Proposal:** Add a tutorial that walks from a new repository to a merged toy PR using the shortest recommended path: idea, PRD, one ADR if needed, one issue, one implementation PR.

**Acceptance criteria:**

- Given a fresh user follows the tutorial, when they complete it, then they have created and merged one PR.
- Given the tutorial is followed, then it uses only the recommended happy path and avoids optional flags such as `--granularity` unless explicitly deferred to a later section.
- Given a user is confused, then the tutorial includes a short “if this fails” section linked to troubleshooting.
- Given dogfood metrics are collected, then the tutorial records expected elapsed time checkpoints.

**Dogfood note:** Run this tutorial against the kit repository itself after the first simplification PR lands.

#### Issue 3: Reduce day-one CLAUDE.md required placeholders

**Priority:** P1  
**Audience:** Humans and agents  
**Type:** Template ergonomics  

**Problem:** The `CLAUDE.md` template requires too many project details before users know the answers, creating friction and stale placeholder values.

**Proposal:** Make only the genuinely required values mandatory on day one. Mark other fields as optional, `_TBD_`, or progressively fillable.

**Acceptance criteria:**

- Given a new project is initialized, when the template is rendered, then only project name, owner, repo, and default branch are treated as required.
- Given optional fields are unknown, then the generated file contains acceptable `_TBD_` markers rather than unresolved template syntax.
- Given an agent reads the generated file, then it can distinguish “unknown but acceptable” from “must be filled before proceeding.”

**Dogfood note:** Track whether fewer prompts are needed during installation after this issue.

#### Issue 4: Create symptom-named troubleshooting page

**Priority:** P2  
**Audience:** Human users  
**Type:** Documentation / support  

**Problem:** Existing troubleshooting material is organized by cause rather than the symptoms users actually see.

**Proposal:** Add a troubleshooting page organized around common visible failures: slash command does not autocomplete, GitHub project creation fails, prompt is stale, skills are not discovered, and install rerun changes files unexpectedly.

**Acceptance criteria:**

- Given a user sees “slash command does not autocomplete,” then the troubleshooting page has that exact symptom as a heading.
- Given `gh project create` fails due to missing scopes, then the page points to the required GitHub scope fix.
- Given a stale prompt is detected, then the page explains why regeneration is expected and safe.

#### Issue 5: Fix stale `Design` casing reference

**Priority:** P2  
**Audience:** Humans and agents  
**Type:** Documentation defect  

**Problem:** `docs/install.md` appears to reference `Design` rather than lowercase `design`.

**Proposal:** Correct the casing and add a lightweight check if there are other stale path references.

**Acceptance criteria:**

- Given install docs reference the design directory, then all examples use lowercase `design`.
- Given a case-sensitive filesystem is used, then copy-paste install commands do not fail because of stale casing.

## Milestone M2: Machine-readable agent contract

### Goal

Make the kit discoverable and composable by agents without requiring them to infer workflow structure from prose.

### Success metrics

- A machine-readable kit index exists.
- Every skill has structured metadata for permission category, inputs, outputs, and next step.
- At least one high-value skill besides `check-plan` has a programmatic `bin/` surface with JSON output.
- Agent-readable metadata and human docs have a single source of truth or a clear synchronization check.

### Issues

#### Issue 6: Add `kit.json` machine-readable workflow index

**Priority:** P0  
**Audience:** AI agents  
**Type:** Architecture / metadata  

**Problem:** Agents currently need to read many prose files to understand skills, permissions, inputs, outputs, and workflow order.

**Proposal:** Add a root-level `kit.json` or `skills/index.yaml` that enumerates skills, permission categories, inputs, outputs, next steps, operating modes, and state transitions.

**Acceptance criteria:**

- Given an agent reads the index, then it can list all skills without reading individual `SKILL.md` bodies.
- Given a skill has a permission category, then the category appears in the index.
- Given a skill normally hands off to another skill, then that relationship appears as structured `next` data.
- Given docs and index disagree, then there is a documented validation path or a follow-up issue to create one.

**Dogfood note:** Use this issue to define the minimum contract an external agent would need to run Milestone M3.

#### Issue 7: Add structured frontmatter fields to all skills

**Priority:** P1  
**Audience:** AI agents  
**Type:** Metadata / consistency  

**Problem:** Skill frontmatter does not yet expose enough structured data for agents to build a workflow graph.

**Proposal:** Add `inputs`, `outputs`, and `next` fields to each skill’s frontmatter, starting with the happy-path skills.

**Acceptance criteria:**

- Given a skill has a handoff section, then the same next step is represented in frontmatter.
- Given a skill creates or modifies files, then expected outputs are listed in frontmatter.
- Given a skill requires arguments, then they are represented as structured inputs.

#### Issue 8: Define standard JSON envelope and exit codes for bin scripts

**Priority:** P1  
**Audience:** AI agents  
**Type:** CLI contract  

**Problem:** `bin/check-plan` has a useful structured interface, but the convention is not generalized across the kit.

**Proposal:** Define a shared JSON response envelope and exit-code convention for current and future `bin/*` scripts.

**Acceptance criteria:**

- Given a `bin/*` script supports `--format json`, then it returns `skill`, `version`, `status`, `outputs`, `next`, and `errors`.
- Given a script exits, then exit codes distinguish success, domain failure, invocation error, auth/service failure, and user cancellation.
- Given a new script is added, then its contract follows the shared convention.

#### Issue 9: Add programmatic surface for `prepare-issue`

**Priority:** P0  
**Audience:** AI agents  
**Type:** CLI / automation  

**Problem:** `prepare-issue` is central to the workflow but currently behaves primarily as an interactive/prose-driven skill.

**Proposal:** Add `bin/prepare-issue --issue N --format json` that emits prompt path, detected gaps, stale state, ADR references, and the recommended next action.

**Acceptance criteria:**

- Given a valid issue number, when `bin/prepare-issue --issue N --format json` runs, then it emits a stable JSON envelope.
- Given the issue body changed after a prompt was generated, then the script reports stale prompt status in structured data.
- Given the script succeeds, then `next.skill` points to `claude-issue-executor`.

**Dogfood note:** Use this script in a later dogfood issue to prove an agent can prepare work without prose interpretation.

#### Issue 10: Add central GitHub credential scope documentation

**Priority:** P1  
**Audience:** Humans and agents  
**Type:** Setup / reliability  

**Problem:** GitHub CLI credential expectations are scattered across skill docs and discovered late.

**Proposal:** Create or update `docs/github-setup.md` with the required `gh` scopes and one command to refresh them.

**Acceptance criteria:**

- Given a user wants to run all GitHub-integrated skills, then one doc lists the required scopes.
- Given an agent starts a run, then it has a preflight checklist for `gh auth status` and scope refresh.
- Given project-board operations require extra scopes, then this is visible before `issue-planner` fails.

## Milestone M3: Unified workflow control and feature expansion

### Goal

Collapse overlapping flow-control concepts into one coherent operating model that works for both humans and agents. Add a first-class follow-up PRD workflow so major feature updates can be introduced incrementally without pretending the project is starting from scratch.

### Success metrics

- There is one named approval-gate sequence.
- Approval uses deterministic tokens where appropriate.
- `/resume` or `/start` can propose the next valid action from project state.
- User-facing verbs hide internal skill complexity.
- Major feature updates can be captured as additive PRD addenda rather than replacements for the original PRD.

### Issues

#### Issue 11: Define one canonical approval gate

**Priority:** P0  
**Audience:** Humans and agents  
**Type:** Workflow semantics  

**Problem:** The executor currently combines chat-level plan gates, harness plan mode, and significance routing, which creates ambiguity.

**Proposal:** Define a single approval-gate sequence: classify work, determine whether approval is required, produce a plan, wait for deterministic approval if needed, then proceed.

**Acceptance criteria:**

- Given significant work is detected, then the gate sequence is described in one canonical location.
- Given approval is required, then the accepted approval token is deterministic and documented.
- Given work is trivial, then the bypass behavior is explicit and testable.
- Given skill docs reference approval behavior, then they point to the canonical gate rather than redefining it.

**Dogfood note:** Apply this to the issue-executor flow during a real kit improvement PR and capture whether it reduces ambiguity.

#### Issue 12: Add `/start` or `/next` meta-skill

**Priority:** P0  
**Audience:** Humans first, agents second  
**Type:** UX / orchestration  

**Problem:** Users have to remember which skill to run next.

**Proposal:** Add a meta-skill that inspects available project state and recommends or invokes the next appropriate skill.

**Acceptance criteria:**

- Given a new project has only an idea, then `/start` routes toward PRD creation.
- Given a project has a prepared issue prompt, then `/next` recommends the executor.
- Given a project has an open PR needing packaging, then `/next` recommends ship/review packaging.
- Given the next step is ambiguous, then the skill asks one clarifying question rather than dumping the full skill list.

#### Issue 13: Compress 19 skills into a smaller human-facing verb layer

**Priority:** P0  
**Audience:** Humans  
**Type:** UX / information architecture  

**Problem:** The skill inventory is accurate but too granular for the front door.

**Proposal:** Introduce or document a smaller set of human-facing verbs such as `/start`, `/decide`, `/backlog`, `/work`, `/ship`, `/finish-milestone`, `/release`, `/resume`, and `/pause`.

**Acceptance criteria:**

- Given a new user asks what to run, then docs present the small verb layer before the full skill list.
- Given an advanced user needs the precise underlying skill, then reference docs still expose it.
- Given an agent needs exact skill names, then the machine index preserves the full skill list.

#### Issue 14: Add structured `next-action` zone to `design/state.md`

**Priority:** P1  
**Audience:** AI agents and returning humans  
**Type:** State management  

**Problem:** `state.md` points to current context but does not expose an actionable next step in structured form.

**Proposal:** Add a marker-fenced `next-action` zone containing skill name, args, and preconditions.

**Acceptance criteria:**

- Given `state.md` is updated, then it includes a machine-readable next action where appropriate.
- Given `/resume` reads state, then it can propose the next action directly.
- Given preconditions are not met, then the next action reports what is blocking execution.

#### Issue 15: Define three operating modes

**Priority:** P1  
**Audience:** Humans and agents  
**Type:** Workflow semantics  

**Problem:** Flags such as plan mode, no-prompt, skip-check, and non-interactive mode are scattered across skills.

**Proposal:** Define three named modes: `interactive`, `assisted`, and `autonomous`, with clear permission boundaries and defaults.

**Acceptance criteria:**

- Given a session starts, then the active mode can be stated in one place.
- Given cat-3 work is reached, then all modes require explicit approval.
- Given `autonomous` mode is used, then cat-1 and cat-2 behavior is clearly documented.

#### Issue 21: Add follow-up PRD workflow for major feature updates

**Priority:** P0  
**Audience:** Humans and agents  
**Type:** Product workflow / feature expansion  

**Problem:** The initial PRD-to-MVP flow is useful for starting a project, but mature projects need a way to introduce major feature updates incrementally. Without a follow-up PRD workflow, users may either overwrite the original PRD or try to force large strategic changes through ordinary issues without enough context.

**Proposal:** Add a first-class follow-up PRD pattern and optional `/feature-prd` user-facing verb. A follow-up PRD should extend the existing project definition, reference current state and ADRs, identify changed assumptions, and decompose the feature into phased issues.

**Recommended artifact structure:**

```text
design/prd.md
design/prd-addenda/
  001-agent-contract-layer.md
  002-follow-up-prd-workflow.md
  003-major-feature-name.md
```

**Recommended flow:**

```text
/feature-prd
→ /adr-writer
→ /issue-planner
→ /prepare-issue
→ /claude-issue-executor
→ /pr-review-packager
```

**Acceptance criteria:**

- Given an existing project with `design/prd.md`, when a user introduces a major feature, then the kit creates a PRD addendum rather than replacing the original PRD.
- Given the feature affects prior decisions, then the output identifies ADRs that need creation, revision, or explicit supersession.
- Given the feature is large, then the output decomposes it into phased issues with dependencies and non-goals.
- Given existing scope should remain stable, then the addendum includes a “does not change” section.
- Given an agent reads the addendum, then it can determine the next planning step and whether an ADR or issue-planning pass is required.
- Given a user asks for a major feature update after the MVP is underway, then docs point them to the follow-up PRD flow rather than the initial PRD flow.

**Dogfood note:** Use this roadmap itself as the first test case. Treat the machine-readable agent contract work as a major feature update to the kit, and represent it as a PRD addendum before creating the M2 issue batch.

## Follow-up PRD model

Major feature updates should be incremental but not under-specified. The follow-up PRD model lets the kit support mature product evolution without resetting the original product definition.

### When to use a follow-up PRD

Use a follow-up PRD when the requested change:

- Adds a new capability area rather than a small enhancement.
- Changes assumptions in the original PRD.
- Requires multiple issues or phases.
- Requires one or more ADRs.
- Introduces compatibility, migration, or permission-boundary concerns.
- Needs to preserve existing scope while extending the product.

Do not use a follow-up PRD for one-off bugs, small docs fixes, obvious refactors, or a single self-contained issue.

### Follow-up PRD template

```markdown
# PRD Addendum: <feature name>

## Context

- Original PRD:
- Current milestone/state:
- Trigger for this update:

## Problem

## Goals

## Non-goals

## What changes

## What does not change

## Affected assumptions

## ADR impact

## User stories

## Requirements

## Migration and compatibility notes

## Issue decomposition

## Success metrics

## Open questions
```

### Claude Code instruction for major updates

When Claude Code is asked to implement a major feature that is not already represented in the original PRD or current backlog, it should not jump directly into implementation. It should first propose a follow-up PRD addendum, identify ADR impact, and ask for approval before creating or executing implementation issues.

## Milestone M4: Reliability, validation, and self-testing

### Goal

Make the kit robust enough for repeated human and agent use by validating schemas, recording receipts, and testing core flows.

### Success metrics

- Carry-forward schema has one canonical source.
- Mutating skills produce receipts or equivalent audit records.
- CI can validate docs/schema consistency.
- Dogfood metrics are tracked release over release.

### Issues

#### Issue 16: Create canonical carry-forward schema

**Priority:** P1  
**Audience:** AI agents  
**Type:** Schema / continuity  

**Problem:** Carry-forward data is replicated across multiple prose and markdown formats, which risks silent drift.

**Proposal:** Add a canonical schema file such as `schemas/design-questions.v1.yaml` and update relevant skills to refer to it.

**Acceptance criteria:**

- Given carry-forward data is produced, then it conforms to the canonical schema.
- Given PR body and next prompt represent carry-forward data, then they can be traced back to the same schema.
- Given schema drift occurs, then validation catches it before release.

#### Issue 17: Add `bin/validate-carry-forward`

**Priority:** P1  
**Audience:** AI agents and maintainers  
**Type:** Validation / tooling  

**Problem:** There is no machine check that producer, preserver, and consumer agree on carry-forward structure.

**Proposal:** Add a validation script that checks eval notes, PR-body carry-forward sections, and next prompts for conformance.

**Acceptance criteria:**

- Given an eval note contains design questions, then validation confirms required fields.
- Given a PR body omits required carry-forward content, then validation fails with a clear error.
- Given validation passes, then the script emits JSON in the standard envelope.

#### Issue 18: Add idempotency receipts for mutating skills

**Priority:** P1  
**Audience:** AI agents and maintainers  
**Type:** Reliability / auditability  

**Problem:** Agents need a deterministic way to recover from partial runs and avoid duplicate work.

**Proposal:** Add receipts under `.claude/receipts/` for mutating skills, capturing inputs, outputs, status, timestamp, and next action.

**Acceptance criteria:**

- Given a mutating skill completes, then it writes a receipt.
- Given a run is interrupted, then a later run can inspect receipts to avoid duplicating completed work.
- Given a human reviews agent activity, then receipts provide a concise audit trail.

#### Issue 19: Add workflow self-test for time-to-first-PR

**Priority:** P1  
**Audience:** Humans and agents  
**Type:** Test / dogfooding  

**Problem:** The kit needs a repeatable way to prove it is becoming more frictionless.

**Proposal:** Add a manual or automated self-test that measures the time and command count required to create a toy PR.

**Acceptance criteria:**

- Given the self-test is run manually, then it records elapsed time, commands used, and points of friction.
- Given automation is feasible, then a stub project can be used to test at least non-mutating parts of the flow.
- Given a release is prepared, then recent self-test results are summarized in release notes.

#### Issue 20: Add consistency checks for docs and metadata

**Priority:** P2  
**Audience:** Maintainers and agents  
**Type:** Validation / CI  

**Problem:** Once `kit.json`, skill frontmatter, and docs coexist, they can drift.

**Proposal:** Add lightweight checks that verify skill names, permission categories, next steps, and documented surfaces agree.

**Acceptance criteria:**

- Given a skill exists in `skills/`, then it appears in the machine index.
- Given a permission category appears in frontmatter, then it matches the machine index.
- Given a documented user-facing verb maps to underlying skills, then those skills exist.

## Milestone M5: AI PR review integration

### Goal

Enable users to run an AI-assisted review of a GitHub PR using OpenRouter or another model provider, produce a structured review report, and optionally publish comments to the PR. The workflow must be safe by default: review generation can be automated, but writing comments to GitHub should require explicit approval unless the user has deliberately configured an autonomous policy.

### Success metrics

- A user can configure OpenRouter or another model provider without pasting secrets into chat or committing keys.
- A user can run a dry-run PR review that produces a local Markdown/JSON review artifact without posting comments.
- The review output distinguishes blocking findings, non-blocking suggestions, questions, and praise.
- GitHub comment publishing is idempotent enough to avoid duplicate comment spam.
- Posting comments requires explicit approval by default and records what was posted.
- The model/provider layer is abstract enough to support OpenRouter first and other OpenAI-compatible APIs later.

### Issues

#### Issue 22: Create follow-up PRD for AI PR review capability

**Priority:** P0  
**Audience:** Humans and agents  
**Type:** Product workflow / PRD addendum  

**Problem:** AI PR review is a major feature that crosses credentials, GitHub write actions, model-provider integration, review quality, and safety policy. It should not be added as an ad hoc implementation issue.

**Proposal:** Use the follow-up PRD workflow from Issue 21 to create a PRD addendum for AI PR review before implementation begins. The addendum should define users, workflows, non-goals, safety constraints, provider requirements, and success metrics.

**Acceptance criteria:**

- Given the original kit PRD exists, when AI PR review is introduced, then a PRD addendum is created under `design/prd-addenda/`.
- Given the feature includes GitHub comment publishing, then the PRD distinguishes dry-run review generation from write-to-GitHub actions.
- Given external model APIs are involved, then the PRD includes credential, privacy, cost-control, and rate-limit requirements.
- Given the feature may affect permission categories, then the PRD identifies which steps are cat-1, cat-2, or cat-3.
- Given implementation issues are created, then they trace back to the PRD addendum.

**Dogfood note:** This should be the first real use of the follow-up PRD workflow. If Issue 21 has not landed yet, create the addendum manually and record what the eventual `/feature-prd` skill should have automated.

#### Issue 23: Define provider-agnostic model configuration for PR review

**Priority:** P0  
**Audience:** Humans and agents  
**Type:** Model integration / configuration  

**Problem:** OpenRouter is a good first provider, but the kit should not hard-code a single vendor or require users to expose API keys unsafely.

**Proposal:** Add a provider configuration model for AI PR review. Support OpenRouter first, but design the interface around OpenAI-compatible chat/completions APIs where possible. Store only provider name, base URL, model name, and non-secret defaults in repo files. Keep API keys in environment variables, local secret stores, or documented user-provided credential mechanisms.

**Acceptance criteria:**

- Given a user wants OpenRouter, then docs explain how to configure `OPENROUTER_API_KEY`, provider base URL, and model name without committing secrets.
- Given a user wants another OpenAI-compatible provider, then the config model can represent base URL, model, headers, and timeout.
- Given no credential is configured, then the review command fails safely with a clear setup message.
- Given a provider is configured, then a non-mutating smoke test can verify authentication and model availability.
- Given provider settings are committed, then no secret values are present in tracked files.

#### Issue 24: Add dry-run AI PR review command

**Priority:** P0  
**Audience:** Humans and agents  
**Type:** CLI / review generation  

**Problem:** Users need a safe way to generate an AI review before anything is posted to GitHub.

**Proposal:** Add a dry-run command such as `bin/review-pr --pr N --provider openrouter --model <model> --format json` or a slash command wrapper such as `/review-pr`. The command should fetch the PR diff and relevant metadata, call the configured model, and write a local review artifact.

**Acceptance criteria:**

- Given a valid PR number, when the command runs in dry-run mode, then it fetches the PR diff and produces a local review artifact without posting comments.
- Given the output is requested as JSON, then it includes summary, findings, severity, file path, line number where available, suggested fix, confidence, and whether the finding is commentable.
- Given the output is requested as Markdown, then it produces a human-readable review report suitable for PR body or manual review.
- Given the PR diff is too large, then the command chunks or summarizes safely rather than failing silently.
- Given model invocation fails, then the command reports provider error, retry guidance, and whether any partial review artifact was created.

#### Issue 25: Add safe GitHub PR comment publishing workflow

**Priority:** P0  
**Audience:** Humans and agents  
**Type:** GitHub integration / safety  

**Problem:** Posting AI comments directly to a PR can create spam, duplicate comments, or low-quality feedback if not gated carefully.

**Proposal:** Add a publishing step that takes a dry-run review artifact and prepares GitHub review comments. By default, it should show the exact comments to be posted and require explicit approval before writing to GitHub.

**Acceptance criteria:**

- Given a dry-run review artifact exists, when publishing is requested, then the command previews the exact top-level review body and inline comments.
- Given comments are to be posted, then explicit approval is required by default before any GitHub write action.
- Given a finding lacks a valid diff line, then it is included in the top-level review body rather than posted as a broken inline comment.
- Given the publisher has already posted a review for the same artifact, then it detects the prior receipt or marker and avoids duplicate comments unless forced.
- Given comments are posted, then a receipt records PR number, artifact hash, comment IDs or review ID, timestamp, provider, and model.

#### Issue 26: Define AI review quality rubric and prompt pack

**Priority:** P1  
**Audience:** Humans and agents  
**Type:** Review quality / prompts  

**Problem:** A generic model prompt will produce inconsistent code-review quality and may over-comment on style rather than useful risks.

**Proposal:** Create a review rubric and prompt pack optimized for actionable PR feedback. The rubric should prioritize correctness, security, data loss, regressions, test coverage, API compatibility, maintainability, and docs impact. It should discourage nitpicks unless requested.

**Acceptance criteria:**

- Given a PR is reviewed, then findings are classified as blocking, non-blocking, question, or praise.
- Given a finding is blocking, then it includes a concrete failure mode and suggested fix.
- Given a finding is speculative, then confidence is marked and the comment is not posted inline by default.
- Given the PR touches docs only, then the rubric adapts to docs accuracy, command correctness, and user-flow clarity.
- Given the user requests “strict”, “balanced”, or “lightweight” review, then the prompt pack changes comment threshold accordingly.

#### Issue 27: Add evaluation harness for AI PR review

**Priority:** P1  
**Audience:** Maintainers and agents  
**Type:** Evaluation / testing  

**Problem:** AI PR review quality needs regression tests. Otherwise prompt or model changes can make the reviewer noisier or less useful without detection.

**Proposal:** Add a small fixture-based evaluation harness using representative PR diffs: docs-only, simple bugfix, risky behavior change, and large noisy diff. Evaluate whether the review finds seeded issues and avoids duplicate/noisy comments.

**Acceptance criteria:**

- Given fixture diffs exist, when the review command runs in offline or mocked mode, then expected finding categories are checked.
- Given a docs-only fixture is reviewed, then the reviewer does not invent code-level bugs.
- Given a risky fixture is reviewed, then at least one seeded high-severity issue is detected.
- Given publishing is tested, then duplicate-comment prevention is verified without writing to a real PR.

#### Issue 28: Add `/review-pr` user-facing workflow

**Priority:** P1  
**Audience:** Human users  
**Type:** UX / slash command  

**Problem:** The AI PR review capability should be accessible through the same human-friendly verb layer as the rest of the kit, not only through `bin/`.

**Proposal:** Add a `/review-pr` skill or wrapper that guides the user through provider selection, dry-run review, review artifact inspection, and optional approved publishing.

**Acceptance criteria:**

- Given a user runs `/review-pr #N`, then the skill explains whether it will dry-run or publish.
- Given provider configuration is missing, then the skill points to setup instructions rather than asking for secrets in chat.
- Given a dry-run artifact is generated, then the user can choose whether to publish comments.
- Given publishing is requested, then the skill requires explicit approval and shows the comments first.
- Given review completes, then the skill records the artifact path and next recommended action.

## Suggested sequencing

### Sprint 0: Baseline health and drift audit

- Issue M0-1: Run and document baseline self-check.
- Issue M0-2: Audit skill metadata, permission, and handoff drift.
- Issue M0-3: Audit installer idempotency and fresh-start behavior.
- Issue M0-4: Fix known low-risk defects before roadmap feature work.
- Issue M0-5: Create first dogfood baseline report.

### Sprint 1: Front-door quick wins

- Issue 5: Fix stale `Design` casing reference.
- Issue 1: Simplify README around one install path.
- Issue 2: Add “first PR in 15 minutes” tutorial.
- Compare against M0 dogfood baseline: time, command count, confusion points.

### Sprint 2: Human UX compression

- Issue 3: Reduce day-one CLAUDE.md required placeholders.
- Issue 4: Create symptom-named troubleshooting page.
- Issue 13: Compress 19 skills into a smaller human-facing verb layer.

### Sprint 3: Agent contract foundation

- Issue 6: Add `kit.json` machine-readable workflow index.
- Issue 7: Add structured frontmatter fields to all skills.
- Issue 8: Define standard JSON envelope and exit codes.
- Issue 10: Add central GitHub credential scope documentation.

### Sprint 4: First executable agent path

- Issue 9: Add programmatic surface for `prepare-issue`.
- Issue 14: Add structured `next-action` zone to `design/state.md`.
- Issue 12: Add `/start` or `/next` meta-skill.

### Sprint 5: Workflow control and safety

- Issue 11: Define one canonical approval gate.
- Issue 21: Add follow-up PRD workflow for major feature updates.
- Issue 15: Define three operating modes.
- Issue 18: Add idempotency receipts for mutating skills.

### Sprint 6: Validation and release hardening

- Issue 16: Create canonical carry-forward schema.
- Issue 17: Add `bin/validate-carry-forward`.
- Issue 19: Add workflow self-test for time-to-first-PR.
- Issue 20: Add consistency checks for docs and metadata.

### Sprint 7: AI PR review capability

- Issue 22: Create follow-up PRD for AI PR review capability.
- Issue 23: Define provider-agnostic model configuration for PR review.
- Issue 24: Add dry-run AI PR review command.
- Issue 26: Define AI review quality rubric and prompt pack.

### Sprint 8: Safe PR comment publishing

- Issue 25: Add safe GitHub PR comment publishing workflow.
- Issue 27: Add evaluation harness for AI PR review.
- Issue 28: Add `/review-pr` user-facing workflow.

## Recommended first three PRs

1. **PR 1: Baseline health and drift report**  
   This establishes what currently works, what fails, and what should be fixed before roadmap feature work. It is the safest first Claude Code task because it should mostly inspect and document rather than redesign.

2. **PR 2: README front-door simplification plus casing fix**  
   This is the smallest meaningful user-facing dogfood test. It improves the human first impression while exercising the current issue-to-PR loop.

3. **PR 3: First-PR tutorial**  
   This creates the measurement harness for future dogfooding. The tutorial becomes the artifact used to verify later improvements.

4. **PR 4: `kit.json` minimal index**  
   This begins the machine-readable layer without needing to build every `bin/<skill>` surface immediately. Start with skill names, permission categories, and next-step relationships.

5. **PR 5: Follow-up PRD workflow**  
   This lets future major feature work enter through PRD addenda rather than ad hoc issue batches.

6. **PR 6: AI PR review PRD addendum**  
   This captures the OpenRouter/GitHub-review feature as a major product update before code is written. It should define safety boundaries, credential handling, model-provider abstraction, and the dry-run-before-publish workflow.

## Issue labels

Use a small label set to keep triage simple:

- `area:docs`
- `area:ux`
- `area:agent-contract`
- `area:cli`
- `area:state`
- `area:safety`
- `area:validation`
- `area:prd`
- `area:dogfood`
- `area:baseline`
- `area:ai-review`
- `area:model-provider`
- `area:github-review`
- `priority:p0`
- `priority:p1`
- `priority:p2`
- `kind:bug`
- `kind:refactor`
- `kind:feature`
- `kind:docs`
- `dogfood`
- `good-first-pr`

## Milestone definitions for GitHub

### Milestone: M0 Baseline health and drift audit

Issues: M0-1, M0-2, M0-3, M0-4, M0-5  
Exit condition: current health, installer behavior, skill-contract drift, and dogfood baseline are documented before roadmap feature work begins.

### Milestone: M1 Front-door simplification

Issues: 1, 2, 3, 4, 5  
Exit condition: a new human user can follow the README to the tutorial and create a first PR without reading reference docs.

### Milestone: M2 Machine-readable agent contract

Issues: 6, 7, 8, 9, 10  
Exit condition: an agent can inspect the kit’s structured metadata and prepare at least one issue using a JSON-producing command.

### Milestone: M3 Unified workflow control and feature expansion

Issues: 11, 12, 13, 14, 15, 21  
Exit condition: users and agents have one canonical way to determine the next step, one canonical approval-gate model, and a follow-up PRD flow for major feature additions.

### Milestone: M4 Reliability and self-testing

Issues: 16, 17, 18, 19, 20  
Exit condition: core schemas, state transitions, and mutating actions are validated or auditable.

### Milestone: M5 AI PR review integration

Issues: 22, 23, 24, 25, 26, 27, 28  
Exit condition: users can run a dry-run AI PR review through OpenRouter or another configured provider, inspect structured findings, and publish GitHub review comments only after explicit approval by default.

## Final recommendation

Dogfood this roadmap in four passes. First, run M0 with the current kit and measure pain honestly before changing anything. Second, run M1 and compare whether the human front door is visibly easier. Third, after M1 and the minimal `kit.json` land, rerun the same flow and compare time, command count, approval ambiguity, and agent-readable state. Fourth, after the follow-up PRD workflow exists, introduce AI PR review as a PRD addendum before implementation. If the later passes are not visibly easier, pause feature expansion and fix the workflow layer before adding more surface area.

## Claude Code handoff prompt

Use this prompt when handing the roadmap to Claude Code:

```text
You are helping improve the workflow-generator kit by dogfooding the kit itself. Start with the roadmap file and do not jump directly into implementation.

Working rules:
- Begin with M0 only. Do not start M1-M4 until M0 is documented.
- Do not start M5 AI PR review implementation until a follow-up PRD addendum exists for it.
- Work one bounded issue at a time.
- Create a branch per issue.
- Prefer small PRs.
- Do not merge PRs yourself.
- Record dogfood friction in the relevant eval note or baseline note.
- If a requested change is a major feature not already represented in the current PRD/backlog, propose a follow-up PRD addendum first.
- Treat AI PR review as a major feature. Start with Issue 22, not implementation.
- For OpenRouter or other model APIs, never ask the user to paste secrets into chat and never commit API keys.
- For GitHub PR comments, generate dry-run artifacts first and require explicit approval before posting comments by default.
- For cat-3 or irreversible GitHub actions, stop and ask for explicit approval.
- After each issue, summarize files changed, tests/checks run, remaining risks, and whether the roadmap should be adjusted.

First task:
Create or execute Issue M0-1: Run and document baseline self-check. Inspect available scripts and documented checks, run what is safe, record pass/fail/not-run status, and propose the next smallest issue. Do not begin feature work.
```
