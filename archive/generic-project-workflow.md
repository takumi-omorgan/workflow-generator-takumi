# Generic Software Project Workflow — Design Document (archived)

> **Archived — historical only.** This is the original methodology
> design document for the Claude Code Workflow Kit, written before
> the kit was built and refined with an external AI. The kit's
> skills operationalise the discipline described here, but the doc
> is no longer the authoritative reference and parts of it are now
> superseded by ADR decisions.
>
> For current direction, read these instead:
>
> - [`README.md`](../README.md) — positioning and what the kit is today
> - [`docs/workflow-guide.md`](../docs/workflow-guide.md) — the action-oriented walkthrough
> - [`docs/skills.md`](../docs/skills.md) — the functional skill reference
> - [`Design/adr/`](../Design/adr/) — accepted decisions
>
> This file is kept only as audit trail for the kit's original
> methodology framing.

---

> A reusable workflow template for setting up and running software projects with AI-assisted development (Claude Code), GitHub-based project management, and structured design documentation.

---

## 1. Objective

Define a standardised, repeatable workflow for new software projects that covers:

1. **Project bootstrap** — repo creation, tooling, CI, and initial scaffold
2. **Design governance** — ADRs (Architecture Decision Records) for traceable decisions
3. **AI-assisted development** — structured prompts for Claude Code build sessions
4. **Quality gates** — testing, review, and evaluation at every stage
5. **Deployment** — from branch to production with rollback safety

The workflow should be tool-agnostic where possible but optimised for:
- **Source control:** GitHub
- **AI development:** Claude Code
- **Languages:** TypeScript / Node.js (adaptable to others)
- **Solo developer or small team** (not enterprise-scale ceremony)

---

## 2. Prerequisites & Tooling Setup

### 2.1 One-Time Machine Setup

These tools need to be installed once per development machine. The workflow assumes macOS but the tools are cross-platform.

| Tool | Purpose | Install |
|------|---------|---------|
| **Git** | Version control | Ships with macOS (Xcode CLT) or `brew install git` |
| **GitHub CLI (gh)** | Issues, PRs, releases from the terminal | `brew install gh` then `gh auth login` |
| **Node.js 22+** | Runtime (for JS/TS projects) | `brew install node` or nvm |
| **Claude Code** | AI-assisted development | `npm install -g @anthropic-ai/claude-code` |
| **SSH key** | Passwordless git push/pull | `ssh-keygen -t ed25519` → add public key to GitHub |

**Verify setup:**

```bash
git --version          # ≥ 2.x
gh --version           # ≥ 2.x
gh auth status         # Logged in
node --version         # ≥ 22.x
claude --version       # Installed
ssh -T git@github.com  # "Hi <username>! You've successfully authenticated"
```

### 2.2 GitHub Account Configuration

| Setting | Where | What to do |
|---------|-------|------------|
| SSH key | github.com → Settings → SSH keys | Add `~/.ssh/id_ed25519.pub` |
| Default branch | github.com → Settings → Repositories | Set to `main` |
| CodeRabbit (optional) | github.com/marketplace/coderabbit | Install for automated PR review |
| Branch protection (optional) | Repo → Settings → Branches → `main` | Require PR, require reviews, require status checks |

---

## 3. Project Bootstrap

### 3.1 Create the Repository

```bash
# Create locally
mkdir my-project && cd my-project
git init

# Or create on GitHub first
gh repo create my-project --private --clone
cd my-project
```

### 3.2 Initial Scaffold

Every project starts with these files:

```
my-project/
  ├── .gitignore              ← Language-appropriate ignores
  ├── CLAUDE.md               ← Instructions for Claude Code (project rules, conventions, structure)
  ├── README.md               ← What, why, how to run
  ├── package.json            ← Dependencies (or equivalent for other languages)
  ├── tsconfig.json           ← TypeScript config (if applicable)
  │
  ├── Design/                 ← Architecture & decisions
  │   ├── adr/                ← Architecture Decision Records
  │   └── ai-summary.md      ← AI-readable project summary (for external AI tools)
  │
  ├── notes/                  ← Process documents & templates
  │   ├── design-workflow.md  ← Design → build → deploy process (this workflow, customised)
  │   └── issue-prompt.md     ← Claude Code issue prompt template (customised)
  │
  ├── src/                    ← Source code
  ├── test/                   ← Tests (mirroring src/ structure)
  └── docs/                   ← User-facing documentation (if needed)
```

### 3.3 CLAUDE.md

This is the most important file for AI-assisted development. It tells Claude Code how to work in your project. Write it at project creation and maintain it as the project evolves.

**Minimum contents:**

```markdown
# Project Name

## What This Is
One paragraph describing the project.

## Technology Stack
- Runtime, language, framework
- Database, storage
- Key libraries

## Conventions
- Module system (ESM, CJS)
- Code style rules
- Dependency versioning policy
- Secret management approach
- Test framework and expectations

## Project Structure
Directory tree with descriptions.

## How to Run
Commands for dev, build, test.

## Current Phase
What's being worked on now.
```

### 3.4 AI Summary Document

Create `Design/ai-summary.md` — a comprehensive, AI-readable description of the entire project. This is what you paste into Perplexity, ChatGPT, or other external AIs when you want them to help design features.

**Contents:** Objectives, architecture, tech stack, constraints, extension points, current status. Written for AI consumption (explicit, structured, no ambiguity). See the Arigato project for a reference example.

**When to update:** After each design doc version bump or significant architectural change. Ask Claude Code to regenerate it based on the current codebase state.

### 3.5 First Commit & Push

```bash
git add .
git commit -m "Initial project scaffold"
git remote add origin git@github.com:<username>/<repo>.git
git push -u origin main
```

---

## 4. Design Governance — ADRs

### 4.1 What is an ADR?

An Architecture Decision Record captures **one decision** with its context, options considered, and consequences. ADRs are the bridge between "I had an idea" and "here's what we're building and why."

### 4.2 When to Write an ADR

| Situation | Write an ADR? |
|-----------|---------------|
| Adding a major feature or subsystem | Yes |
| Changing an architectural pattern | Yes |
| Choosing between two libraries/approaches | Yes |
| Adding a new integration or dependency | Yes |
| Fixing a bug | No — just fix it |
| Refactoring without behaviour change | No — unless it changes the architecture |
| Typo or config tweak | No |

### 4.3 ADR Template

Save as `Design/adr/adr-NNN-short-title.md`:

```markdown
# ADR-NNN: Title

**Status:** proposed | accepted | rejected | superseded by ADR-NNN
**Date:** YYYY-MM-DD

## Context

What problem or opportunity triggered this decision? What constraints exist?

## Options Considered

### Option A: ...
- Pros: ...
- Cons: ...

### Option B: ...
- Pros: ...
- Cons: ...

## Decision

Which option was chosen and why.

## Consequences

What changes as a result. What new constraints or trade-offs are introduced.

## Review Notes

(Added after external review — feedback from Perplexity, ChatGPT, Claude Code, or human reviewers.)
```

### 4.4 ADR Lifecycle

```
proposed → accepted → implemented (via GitHub issue + PR)
         → rejected (kept on file as context)
         → superseded by ADR-NNN
```

- **Rejected ADRs stay in the repo.** They document why something wasn't done — invaluable when the same idea comes up again.
- **Superseded ADRs link to their replacement.** This creates a decision trail.

### 4.5 External AI Review

For non-trivial ADRs, get a second opinion:

1. Paste `Design/ai-summary.md` into Perplexity / ChatGPT / other AI
2. Paste the ADR draft
3. Ask focused questions: "What are the risks?", "What alternatives am I missing?", "Does this conflict with existing constraints?"
4. Record useful feedback in the ADR's `## Review Notes` section

### 4.6 Batching ADRs into Versions (Optional)

For projects with a central design document (not all projects need one):

- Periodically batch accepted ADRs into a new version of the design doc
- Update `CLAUDE.md` to point to the latest version
- Regenerate `Design/ai-summary.md`

---

## 5. GitHub Issues

### 5.1 Creating Issues from ADRs

Once an ADR is accepted, create one or more GitHub Issues to track implementation:

```bash
gh issue create \
  --title "Add feature X (ADR-NNN)" \
  --body "$(cat <<'EOF'
## Summary
Brief description of what's being built.

## ADR
See `Design/adr/adr-NNN-short-title.md`

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Acceptance criteria
- Criterion 1
- Criterion 2

## Test requirements
- Unit tests for ...
- Edge case coverage for ...
- Manual verification steps (if any)
EOF
)"
```

### 5.2 Issue Sizing

| ADR size | Issues to create |
|----------|-----------------|
| Small (config change, single file) | 1 issue |
| Medium (new module, new integration) | 1 parent issue + 2-3 sub-issues |
| Large (new subsystem) | 1 epic issue linking to multiple sub-issues |

### 5.3 Labels

Keep labels simple and consistent across projects:

| Label | Use for |
|-------|---------|
| `feature` | New functionality |
| `bug` | Something broken |
| `design` | ADR or architecture work |
| `infra` | CI, deployment, tooling |
| `security` | Security-related changes |
| `docs` | Documentation only |

```bash
# Create labels on a new repo
gh label create feature --color 0E8A16
gh label create bug --color D73A4A
gh label create design --color 1D76DB
gh label create infra --color FBCA04
gh label create security --color B60205
gh label create docs --color 0075CA
```

---

## 6. Branch Strategy

### 6.1 Model

Simple **main + feature branches**, aligned with [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow). No develop, no release branches, no gitflow.

```
main (stable, always deployable)
  |
  ├── add-feature-x       ← feature branch
  ├── fix-bug-y            ← bugfix branch
  └── refactor-module-z    ← refactor branch
```

### 6.2 Rules

| Rule | Rationale |
|------|-----------|
| Always branch from `main` | Start from stable, known-good code |
| One branch per issue (or related group) | Keeps PRs focused and reviewable |
| Descriptive branch names | `<verb>-<short-description>` referencing the issue, e.g. `add-auth-middleware`, `fix-rate-limiter-reset`, `refactor-db-layer`. Avoid generic names like `feature-1`. Include the issue number for traceability when useful: `42-add-auth-middleware`. |
| Never commit directly to `main` | All changes go through PRs |
| Delete branches after merge | Prevents branch clutter |

### 6.3 Commands

```bash
# Start work on an issue
git checkout main
git pull
git checkout -b add-feature-x

# Push branch to remote
git push -u origin add-feature-x

# After merge, clean up locally
git checkout main
git pull
git branch -d add-feature-x
```

---

## 7. AI-Assisted Development with Claude Code

### 7.1 Issue Prompt Framework

The issue prompt framework (`notes/issue-prompt.md`) is a structured template you fill in and paste into Claude Code at the start of each build session. It ensures every session:

- Reads the right context (CLAUDE.md, ADR, design docs, existing code)
- Proposes a plan before writing code
- Waits for your approval
- Writes tests alongside implementation
- Provides a full evaluation summary at the end

### 7.2 Generic Issue Prompt Template

Save as `notes/issue-prompt.md` and customise the project-specific sections:

```markdown
You are working in my `{{PROJECT_NAME}}` repository.

Context:
- {{ONE_LINE_PROJECT_DESCRIPTION}}
- Follow the rules in `CLAUDE.md`.
- Architecture is described in {{ARCHITECTURE_DOC_PATH}}.
- AI-readable summary is at `Design/ai-summary.md`.

ADR:
- File: `Design/adr/{{ADR_FILE}}`
- Decision: {{ADR_SUMMARY}}

GitHub Issue:
- Title: {{ISSUE_TITLE}}
- Number: #{{ISSUE_NUMBER}}
- Labels: {{LABELS}}

Goal
{{GOAL}}

Why it matters
{{WHY_IT_MATTERS}}

Requirements
{{REQUIREMENTS_LIST}}

Acceptance criteria
{{ACCEPTANCE_CRITERIA_LIST}}

Scope and constraints
- Primary folders to touch: {{PRIMARY_FOLDERS}}
- Folders to avoid unless absolutely necessary: {{AVOID_FOLDERS}}
- {{PROJECT_SPECIFIC_CONSTRAINTS}}

Evaluation & testing requirements
- Every new module or significant function MUST have corresponding unit tests.
- Tests go in `test/` mirroring the `src/` structure.
- Cover at minimum:
  - Happy path — expected inputs produce expected outputs.
  - Edge cases — empty inputs, boundary values, malformed data.
  - Error handling — invalid config, missing dependencies, network failures.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification steps.

Instructions for you
1. Read the relevant docs and existing code:
   - `CLAUDE.md`
   - `Design/adr/{{ADR_FILE}}`
   - `Design/ai-summary.md`
   - Any existing modules under {{PRIMARY_FOLDERS}}.
   - Any existing tests related to the modules you will change.
2. Propose a step-by-step implementation PLAN including:
   - new files/modules to create,
   - existing files to modify,
   - config or schema changes,
   - key functions/classes and their structure,
   - your test plan: which test files, what scenarios, what edge cases.
3. Wait for my approval before making any edits.
4. After I approve, implement the plan:
   - write tests ALONGSIDE the implementation, not as an afterthought,
   - keep changes focused on this issue's scope,
   - commit incrementally with messages referencing the ADR and issue
     (e.g. "Add auth middleware (ADR-003, #15)").
5. At the end, provide an evaluation summary:
   - what changed (files and key functions),
   - test results: paste the test runner output (total, passed, failed, skipped),
   - test coverage: list each new test file and what it validates,
   - regression check: confirm all pre-existing tests still pass,
   - manual verification steps (if any behaviour cannot be unit tested),
   - exact commands I should run to verify everything myself.

Do not start editing files until I explicitly approve your plan.
```

### 7.3 Build Session Best Practices

| Practice | Why |
|----------|-----|
| Start each session with the filled issue prompt | Consistent context and quality |
| One issue per Claude Code session | Prevents scope creep and context confusion |
| Approve the plan before code is written | Catches design mistakes early, before they're embedded in code |
| Commit incrementally during the session | Small commits are easier to review and revert |
| Push regularly | Backs up your work; enables CR on partial progress |
| Keep sessions under ~2 hours | Long sessions degrade context quality; commit, push, start fresh |
| Run the full test suite before finishing | Catch regressions before the PR stage |

### 7.4 What Claude Code Can Do For You

Beyond writing code, Claude Code can handle project management tasks directly:

```
"Create a GitHub issue for ADR-003"
"Create a branch for the auth work"
"Commit what we have so far"
"Push and create a PR"
"Merge PR #15"
"Switch to main and pull"
"Review the diff on this branch against main"
"Run the tests"
```

---

## 8. Commits

### 8.1 Message Format

```
<verb> <what> (<ADR and/or issue reference>)

Optional body explaining why, not what.
```

### 8.2 Good Verbs

| Verb | Use for |
|------|---------|
| Add | New feature, file, or module |
| Fix | Bug fix |
| Update | Enhancement to existing feature |
| Remove | Deleting code, files, or features |
| Refactor | Restructuring without behaviour change |
| Implement | Building out a designed feature (ADR) |

### 8.3 Examples

```
Add auth middleware with JWT validation (ADR-003, #15)

Fix rate limiter not resetting after window expiry (#22)

Update user schema to include email verification flag (ADR-007)

Remove deprecated v1 API endpoints (#30)
```

### 8.4 Co-Authorship

When Claude Code creates a commit, it appends a `Co-Authored-By` trailer. This is normal and expected — it attributes AI-assisted work transparently.

---

## 9. Pull Requests

### 9.1 Creating a PR

```bash
# From Claude Code:
# "Push and create a PR"

# Or manually:
git push -u origin add-feature-x
gh pr create --title "Add feature X (ADR-NNN)" --body "$(cat <<'EOF'
## Summary
- Bullet point changes

## ADR
Design/adr/adr-NNN-short-title.md

## Changes
- `src/file.ts` — what changed
- `config/file.json` — what changed

## Test results
- X tests passed, Y skipped, 0 failed
- New tests: `test/file.test.ts`

## Test plan (manual verification)
- [ ] Step 1
- [ ] Step 2

Closes #NN
EOF
)"
```

### 9.1.1 Draft PRs

For early feedback before implementation is complete, create the PR as a draft:

```bash
gh pr create --draft --title "Add feature X (ADR-NNN)" --body "..."
```

Draft PRs signal that the work is in progress and not ready for final review. Convert to ready when implementation and tests are complete: `gh pr ready <number>`.

### 9.2 PR Body Template

Every PR should include:

| Section | Purpose |
|---------|---------|
| **Summary** | What changed and why (1-3 bullets) |
| **ADR** | Link to the decision that drove this work |
| **Changes** | File-level changelog |
| **Test results** | Automated test output summary |
| **Test plan** | Manual verification checklist (if needed) |
| **Closes #NN** | Auto-close the linked issue on merge |

### 9.3 Review Process

| Reviewer | What it catches |
|----------|----------------|
| **Self-review** | Read the full diff on GitHub before requesting review |
| **CodeRabbit** (automated) | Style issues, potential bugs, security concerns |
| **Claude Code** | Ask: "Review the diff on this branch against main" |
| **External AI** | Paste diff + AI summary into Perplexity/ChatGPT for architectural review |
| **Human reviewer** (if team project) | Business logic, UX, domain correctness |

### 9.4 Merge Strategy

| Method | When to use |
|--------|-------------|
| **Squash merge** | Default. Collapses branch commits into one clean commit on main. |
| **Regular merge** | Large features where individual commit history is valuable. |

```bash
# Squash merge (preferred)
gh pr merge <number> --squash --delete-branch

# Regular merge
gh pr merge <number> --merge --delete-branch
```

After merging, sync locally:

```bash
git checkout main
git pull
```

---

## 10. Testing & Evaluation

### 10.1 Test Strategy

| Level | What | When |
|-------|------|------|
| **Unit tests** | Individual functions and modules | Written alongside every code change |
| **Integration tests** | Modules working together, database, external APIs | Written for cross-module features |
| **Manual verification** | UI, deployment, hardware-dependent behaviour | Documented in PR test plan; executed at deploy |

### 10.2 Test Standards

- Every new module has a corresponding test file
- Test file structure mirrors source: `src/auth/middleware.ts` → `test/auth/middleware.test.ts`
- Minimum coverage per test file:
  - Happy path (expected behaviour)
  - Edge cases (empty input, boundaries, malformed data)
  - Error handling (missing deps, network failure, invalid config)
- All existing tests must pass after every change (regression check)

### 10.3 Evaluation Summary

Every Claude Code build session ends with an evaluation summary. This is your quality gate before creating a PR:

```
Evaluation Summary
==================
Files changed:
  - src/auth/middleware.ts (new)
  - src/config.ts (modified)
  - config/auth.json (new)

Test results:
  ✓ 52 passed, 0 failed, 3 skipped
  (paste full test runner output)

New tests:
  - test/auth/middleware.test.ts
    - validates JWT token format
    - rejects expired tokens
    - handles missing Authorization header
    - rejects malformed tokens

Regression check:
  All 49 pre-existing tests pass.

Manual verification (at deploy):
  - [ ] Login flow works end-to-end in browser
  - [ ] Token refresh works after 1 hour

Commands to verify:
  npx vitest run
  npm run build
```

---

## 11. Deployment

### 11.1 Deployment Models

This workflow supports multiple deployment models. Choose the one that fits your project:

| Model | Suits | How |
|-------|-------|-----|
| **Git pull** | Personal projects, single server | SSH into server, `git pull && npm install && restart` |
| **GitHub Actions → deploy** | SaaS, web apps | CI/CD pipeline triggered on merge to main |
| **Manual build + upload** | Static sites, mobile apps | Build locally, upload artifact |
| **Container** | Microservices, complex deps | Build image, push to registry, deploy |

### 11.2 Deploy Checklist (Generic)

Regardless of deployment model:

1. **Pre-deploy:**
   - All tests pass on main
   - PR merged and branch deleted
   - No unresolved review comments
   
2. **Deploy:**
   - Pull/push latest code to production
   - Install dependencies
   - Run build step (if applicable)
   - Restart service

3. **Post-deploy:**
   - Run manual verification steps from PR test plan
   - Check logs for errors
   - Confirm the feature works as expected

4. **Rollback (if needed):**
   ```bash
   git revert HEAD
   git push
   # Restart service
   ```

### 11.3 Separate Dev and Production Machines

If development and production are on different machines (e.g. laptop for dev, server for production):

- All code changes happen on the dev machine via Claude Code
- Changes are committed, pushed, reviewed, and merged on the dev machine
- Production deployment happens when you have access to the production machine
- Manual verification steps (from PR test plans) are executed on the production machine
- Keep a running list of "deploy when at production machine" items

---

## 12. Workflow Summary — Full Lifecycle

```
┌─────────────────────────────────────────────────────────┐
│                    DESIGN PHASE                         │
│                                                         │
│  1. Idea / problem / feature request                    │
│  2. Write ADR → Design/adr/adr-NNN-title.md            │
│  3. (Optional) Review with external AI                  │
│  4. Accept or reject ADR                                │
│  5. (Optional) Bump design doc version                  │
│  6. Update AI summary + CLAUDE.md                       │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    BUILD PHASE                          │
│                                                         │
│  7. Create GitHub issue from accepted ADR               │
│     gh issue create --title "..." --body "..."          │
│                                                         │
│  8. Create feature branch                               │
│     git checkout main && git pull                       │
│     git checkout -b add-feature-x                       │
│                                                         │
│  9. Fill in issue prompt template                       │
│     notes/issue-prompt.md → fill {{placeholders}}       │
│                                                         │
│  10. Build with Claude Code                             │
│      Paste prompt → approve plan → implement + test     │
│      Commit incrementally throughout                    │
│                                                         │
│  11. Evaluate                                           │
│      Run full test suite                                │
│      Review evaluation summary                         │
│      Confirm: all tests pass, no regressions            │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    REVIEW PHASE                         │
│                                                         │
│  12. Push branch + create PR                            │
│      git push -u origin add-feature-x                   │
│      gh pr create --title "..." --body "..."            │
│                                                         │
│  13. Review                                             │
│      Self-review diff on GitHub                         │
│      CodeRabbit auto-review                             │
│      (Optional) Claude Code or external AI review       │
│                                                         │
│  14. Merge                                              │
│      gh pr merge N --squash --delete-branch             │
│      Closes linked issue automatically                  │
│                                                         │
├─────────────────────────────────────────────────────────┤
│                    DEPLOY PHASE                         │
│                                                         │
│  15. Deploy to production                               │
│      Pull latest main, install deps, restart            │
│                                                         │
│  16. Verify                                             │
│      Run manual verification from PR test plan          │
│      Check logs for errors                              │
│                                                         │
│  17. Cleanup                                            │
│      Confirm issues closed                              │
│      Update project tracking docs                       │
│      Sync local main                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 13. New Project Checklist

Use this checklist when starting a new project:

### One-time setup (if not already done)
- [ ] Git installed
- [ ] GitHub CLI installed and authenticated (`gh auth login`)
- [ ] SSH key generated and added to GitHub
- [ ] Node.js installed (for JS/TS projects)
- [ ] Claude Code installed
- [ ] CodeRabbit installed on GitHub account (optional)

### Per-project setup
- [ ] Create repo (`gh repo create` or `git init`)
- [ ] Add `.gitignore`
- [ ] Write `CLAUDE.md` (project rules, conventions, structure)
- [ ] Write `README.md`
- [ ] Create `Design/adr/` directory
- [ ] Write `Design/ai-summary.md` (AI-readable project context)
- [ ] Customise `notes/issue-prompt.md` (fill project-specific sections)
- [ ] Customise `notes/design-workflow.md` (adapt process to project)
- [ ] Set up test framework (`vitest`, `jest`, `pytest`, etc.)
- [ ] Create standard labels (`gh label create ...`)
- [ ] Initial commit and push to GitHub
- [ ] (Optional) Configure branch protection on `main`
- [ ] (Optional) Set up CI/CD (GitHub Actions)

### Per-feature workflow
- [ ] Write ADR
- [ ] (Optional) External AI review
- [ ] Accept ADR
- [ ] Create GitHub issue
- [ ] Create feature branch
- [ ] Fill issue prompt, paste into Claude Code
- [ ] Approve plan, build, test
- [ ] Review evaluation summary — all tests pass
- [ ] Push + create PR
- [ ] Review PR (self + automated)
- [ ] Merge to main
- [ ] Deploy to production
- [ ] Verify + cleanup

---

## 14. Customisation Points

When adapting this workflow to a specific project, these are the sections that need project-specific content:

| What to customise | Where | Example |
|-------------------|-------|---------|
| Project description and stack | `CLAUDE.md` | "React SPA with Supabase backend" |
| Architecture reference | `Design/ai-summary.md` | Full system overview for external AIs |
| Coding constraints | `notes/issue-prompt.md` → Scope section | "No direct SQL — use Prisma ORM" |
| Test framework and commands | `notes/issue-prompt.md` → Evaluation section | `npx vitest run` vs `pytest` vs `go test` |
| Deployment method | `notes/design-workflow.md` → Deploy section | Git pull vs GitHub Actions vs Docker |
| Labels and milestones | GitHub repo settings | Project-specific categories |
| Branch protection rules | GitHub repo settings | Required reviewers, status checks |
| CI pipeline | `.github/workflows/` | Build, test, lint, deploy |

---

## 15. Open Questions for Refinement

These were areas where this workflow could be extended or where decisions
needed to be made per-project. Several have been resolved by accepted ADRs;
the remaining open questions are kept here as historical context.

**Resolved by the kit (as of v3.3.0):**

1. ~~**Milestones vs. labels for release planning**~~ — resolved by ADR-032
   (one milestone per phase) and ADR-037 (milestone lifecycle skills).
2. ~~**GitHub Projects board**~~ — resolved by ADR-012 (project board created
   by `/issue-planner`).
3. ~~**Changelog generation**~~ — resolved by ADR-016 (`/changelog` skill).
4. ~~**Semantic versioning**~~ — resolved by ADR-026 (kit versioning policy)
   and ADR-017 (`/release` skill).
7. ~~**Issue templates**~~ — resolved by `templates/issue-template.md`.
8. ~~**PR templates**~~ — resolved by `templates/pr-template.md` and ADR-015
   (`/pr-review-packager`).

**Still open (per-project decisions):**

5. **CI/CD pipeline** — what's the minimal useful GitHub Actions workflow?
   (lint + test on PR, deploy on merge to main?) See feature-ideas.md for
   "Starter GitHub Actions CI/CD workflows".
6. **Multiple environments** — staging vs. production? Or just main =
   production for solo projects?
9. **Dependabot / Renovate** — automated dependency updates?
10. **Secret management** — project-specific approach (env vars, Keychain,
    Vault, GitHub Secrets)?
