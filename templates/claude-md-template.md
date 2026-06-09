<!--
  Template: CLAUDE.md — project rules for Claude Code
  Filled by:  the workflow-docs skill (later), or a human at project bootstrap
  Output in a target project: CLAUDE.md at the repo root
  Source:     templates/claude-md-template.md in the Claude Code Workflow Kit

  CLAUDE.md is the single most important file for AI-assisted work in a
  project. Claude Code reads it on every session. Keep it current — stale
  rules create worse output than no rules.

  ------------------------------------------------------------------------
  PLACEHOLDERS (all use {{UPPER_SNAKE}} syntax; grep them with:
      grep -E '\{\{[A-Z_]+\}\}' CLAUDE.md
  ------------------------------------------------------------------------

  The installer (bin/install-workflow-kit) gathers only the four day-one
  required fields below and fills every other placeholder with the marker
  `_TBD_`. A rendered CLAUDE.md therefore never contains unresolved
  {{...}} syntax: a value is either real or an explicit `_TBD_` that means
  "unknown but acceptable — fill in when the answer is known." (This whole
  authoring comment is stripped from the rendered file.)

  Required on day one — the installer prompts for these (deriving a default
  where it can) because a new project always knows them:
    {{PROJECT_NAME}}          Human-readable project name. Example: "Acme Notes"
    {{GITHUB_OWNER}}          GitHub user or org. Example: "acme-labs"
    {{GITHUB_REPO}}           Repo slug. Example: "acme-notes"
    {{DEFAULT_BRANCH}}        Example: "main"

  Optional / progressively fillable — left as `_TBD_` until known. Replace
  each with a real value (or `--set KEY=VALUE` at install time) as the
  project's stack and conventions settle:
    {{PROJECT_TAGLINE}}       One-line elevator pitch. Example: "A local-first
                              Markdown note-taking app for researchers."
    {{PRIMARY_LANGUAGE}}      Main runtime / language. Example: "Node.js 22 + TypeScript"
    {{FRAMEWORK}}             Primary framework, or "none". Example: "Next.js 15"
    {{DATA_LAYER}}            Database / storage, or "none yet". Example: "Postgres 16"
    {{KEY_LIBRARIES}}         Comma-separated top 3–5 libraries a reviewer
                              must know. Example: "Prisma, tRPC, Tailwind"
    {{PACKAGE_MANAGER}}       Example: "pnpm", "npm", "uv", "cargo"
    {{INSTALL_COMMAND}}       Example: "pnpm install"
    {{DEV_COMMAND}}           Example: "pnpm dev"
    {{BUILD_COMMAND}}         Example: "pnpm build"
    {{TEST_COMMAND}}          Example: "pnpm test"
    {{LINT_COMMAND}}          Example: "pnpm lint", or "none" if you haven't
                              picked a linter yet
    {{TEST_FRAMEWORK}}        Example: "vitest", "pytest", "go test"
    {{TEST_LOCATION}}         Example: "test/ mirroring src/"
    {{FORMATTER}}             Example: "prettier", "black", "rustfmt", "none"
    {{MODULE_SYSTEM}}         Example: "ESM", "CommonJS", "N/A"
    {{CURRENT_MILESTONE}}     Example: "Foundation", "MVP", "v0.2"
    {{CURRENT_PHASE}}         One short line describing what the project is
                              focused on right now. Update as work moves.
    {{DEPLOY_TARGET}}         Example: "Vercel", "Fly.io", "n/a (local only)"
    {{SECRETS_LOCATION}}      Example: ".env.local (gitignored), 1Password vault
                              'Acme Notes'"
    {{COMMIT_STYLE}}          Example: "conventional commits", "plain prose"
    {{BRANCH_NAMING}}         Example: "kebab-case, one branch per issue"

  Free-form slots use {{prose hints}} or _italic hints_ — fill them with
  plain English, not a single token.
-->

# {{PROJECT_NAME}}

> {{PROJECT_TAGLINE}}

This file is the project rules for [Claude Code](https://claude.com/product/claude-code).
Claude reads it on every session. Keep it current — stale rules produce
worse output than no rules.

> Any field still showing `_TBD_` is an optional value left to fill in
> later. `_TBD_` means "unknown but acceptable" — safe to defer, not a
> blocker. Replace it with a real answer once the project settles.

## What this is

<!-- FILL: one paragraph describing what this project does, for whom, and roughly how. Link to the PRD, MVP doc, or AI summary once they exist. -->

## First run

New project? Open Claude Code in this repo and run `/start`. It will inspect
the installed kit surface and route you to the next workflow step.

## Current phase

{{CURRENT_PHASE}}

Active milestone: `{{CURRENT_MILESTONE}}`.

## Technology stack

- Runtime / language: {{PRIMARY_LANGUAGE}}
- Framework: {{FRAMEWORK}}
- Database / storage: {{DATA_LAYER}}
- Key libraries: {{KEY_LIBRARIES}}
- Package manager: {{PACKAGE_MANAGER}}
- Module system: {{MODULE_SYSTEM}}
- Deployment target: {{DEPLOY_TARGET}}

## How to run

```bash
{{INSTALL_COMMAND}}
{{DEV_COMMAND}}
{{BUILD_COMMAND}}
```

## Testing

- Framework: {{TEST_FRAMEWORK}}
- Location: {{TEST_LOCATION}}
- Run: `{{TEST_COMMAND}}`
- Coverage expectations: new modules include unit tests for the happy
  path, edge cases, and error handling. Existing tests must continue to
  pass on every PR.

## Code style

- Formatter: {{FORMATTER}}
- Linter: {{LINT_COMMAND}}
- Commit style: {{COMMIT_STYLE}}
- Secret management: {{SECRETS_LOCATION}}

## Project structure

```
{{PROJECT_NAME}}/
  src/            <!-- FILL: application/library code, if applicable -->
  test/           <!-- FILL: unit/integration tests, if applicable -->
  design/         architecture, ADRs, and workflow design artefacts
  prompts/        per-issue prompts (`prompts/issue-NNN-short-title.md`)
  notes/          working notes and evaluation logs
  .claude/skills/ installed workflow skills
```

See also:

- `design/architecture.md` — current architecture/design reference, maintained by `/workflow-docs`
- `design/adr/` — ADRs and ADR index, available on day one
- `design/prd.md` — product requirements, created later by the workflow
- `design/mvp.md` — MVP scope, created later by the workflow
- `design/build-out-plan.md` — phased backlog plan, created later by the workflow
- `design/ai-summary.md` — compact project summary, created later by the workflow
- `prompts/` — per-issue prompts (`prompts/issue-NNN-short-title.md`)
- `notes/` — working notes and evaluation logs
- `.claude/skills/` — installed workflow skills (do not edit by hand)

## Workflow rules

This project follows the [Claude Code Workflow Kit](https://github.com/olivermorgan2/workflow-generator)
model. The rules below are load-bearing — Claude Code should treat them
as hard requirements unless a human overrides them in the session.

- **Plan-first execution.** When given a non-trivial task, propose a short
  step-by-step plan and wait for explicit approval before editing files.
- **Issue-by-issue.** Work is scoped to one GitHub issue at a time.
  Per-issue prompts live in `prompts/issue-NNN-short-title.md`.
- **Keep architecture docs current.** If a change materially alters the
  system shape, update or re-run `/workflow-docs` so `design/architecture.md`
  and `design/ai-summary.md` reflect reality.
- **Consult ADRs before changing load-bearing behaviour.** If a change
  touches architecture, installation, or conventions, check
  `design/adr/` first. Never edit an accepted ADR in place — supersede it
  with a new ADR, then refresh `design/architecture.md`.
- **Stay in scope.** Do not refactor unrelated code, rename files, or add
  speculative abstractions while working on an issue. If something is
  out of scope, note it for a follow-up issue.
- **Tests stay green.** Run `{{TEST_COMMAND}}` before declaring a task
  done. Fix regressions in the same PR that caused them.
- **Ask when ambiguous.** Prefer a clarifying question over a plausible
  guess on anything that affects scope, public API, or data shape.

## GitHub conventions

This project uses GitHub Flow — `{{DEFAULT_BRANCH}}` is always
deployable; all work lands via pull requests.

- **Repository:** `{{GITHUB_OWNER}}/{{GITHUB_REPO}}`
- **Default branch:** `{{DEFAULT_BRANCH}}`
- **Branch naming:** {{BRANCH_NAMING}}. Branch from `{{DEFAULT_BRANCH}}`,
  never commit to it directly, delete branches after merge.
- **One issue per branch / PR.** Split PRs that grow to cover multiple
  issues.
- **Labels:** `feature`, `bug`, `design`, `infra`, `security`, `docs`.
  Every issue gets exactly one primary label.
- **Milestones:** `Foundation`, `MVP`, `Post-MVP` (add more only when the
  list gets crowded).
- **Pull requests** include the sections defined in
  [`.github/pull_request_template.md`](.github/pull_request_template.md):
  Summary, `Closes #N`, ADR reference, Changes, Test results, Manual
  verification.
- **Commit messages** reference the ADR and issue when the change is
  driven by them. Example: `feat(auth): add session middleware (ADR-003, #15)`.
  Commit style: {{COMMIT_STYLE}}.

## Review expectations

- Every change lands via PR linked to a GitHub issue with `Closes #N`.
- Plan-first: propose a plan, wait for approval, then implement.
- Keep PRs small and focused. A PR should be reviewable in ~15 minutes.
- No direct commits to `{{DEFAULT_BRANCH}}`.
- Existing tests must pass; new behaviour has new tests.

## Definitions of done

A task is **done** when:

1. Code compiles / type-checks cleanly.
2. `{{TEST_COMMAND}}` passes locally.
3. `{{LINT_COMMAND}}` passes locally (skip if `none`).
4. The PR body fills in every required section.
5. The ADR (if any) and the issue number are referenced in the commit.
6. A human has approved the PR or explicitly waived review.

## What this file is NOT

- Not the architecture reference — that is `design/architecture.md`.
- Not a spec — architectural decision history lives in `design/adr/`.
- Not a roadmap — phased plans live in `design/build-out-plan.md`.
- Not an AI-readable summary — that is `design/ai-summary.md`.

Keep this file focused on rules and conventions Claude Code needs to do
its job. When in doubt, link out.
