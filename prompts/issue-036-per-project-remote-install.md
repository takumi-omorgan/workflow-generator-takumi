You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development
  workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `design/adr/`.

ADR:
- File: `design/adr/adr-029-per-project-remote-install.md`
- Decision: refine ADR-009 — make per-project remote install (gh
  repo clone --depth=1 --branch=vX.Y.Z, run installer, cleanup) the
  documented default. Add `bin/bootstrap-workflow-kit` as a
  one-command convenience wrapper. Local-clone path stays for kit
  contributors only.

GitHub Issue:
- Title: Recommend per-project remote install over local-clone-once (ADR-029)
- Number: #36
- Milestone: v3.2.0 — project-agnostic framing, remote install, license flag
- Labels: feature, docs, infra

Goal
Replace the "clone the kit once locally, reuse forever" user flow
with a fetch-on-demand, version-pinned per-project install. End
users no longer need a long-lived local kit clone. Contributors
still do (for dogfooding).

Why it matters
The local-clone-once model has real friction: stale clones,
cross-machine setup, implicit kit version per scaffolded project.
Per-project remote install is reproducible (version-pinned via
`--branch=vX.Y.Z`), zero-state on the machine, and removes a
"setup before setup" step from new users.

Requirements
- Write `bin/bootstrap-workflow-kit` (~30 lines, bash, no runtime
  deps beyond `git`/`gh`):
  - `set -euo pipefail`.
  - Resolve target version: `WORKFLOW_KIT_VERSION` env var if set,
    else `--version=` flag if passed, else "latest" (resolved via
    `gh release view --json tagName` or `git ls-remote --tags
    --sort=-v:refname` fallback).
  - Make a temp dir via `mktemp -d`. Trap to clean up on exit
    (success or failure).
  - Detect `gh` via `command -v gh`. If present, use `gh repo
    clone REPO TMPDIR -- --depth=1 --branch=VERSION`. Else, fall
    back to `git clone --depth=1 --branch=VERSION
    https://github.com/REPO.git TMPDIR`.
  - Verify the cloned tree has `bin/install-workflow-kit`. If not,
    error out.
  - Forward all remaining CLI args to the installer.
  - Document `WORKFLOW_KIT_REPO` env var for forks (default
    `olivermorgan2/workflow-generator`).
  - `chmod +x` the script.
- Rewrite README's "Quick start" section:
  - Replace the "clone the kit once" subsection with a "Quick
    start" that shows the per-project remote install. Keep the
    "One-time setup (per machine)" prerequisites section but
    remove the kit-clone step from it.
  - Show two install variants:
    1. The bootstrap one-liner: `bash <(curl -fsSL
       https://github.com/.../releases/download/vX.Y.Z/bootstrap-workflow-kit)
       --project-name=NAME`.
    2. The explicit gh-clone form: three lines, version-pinned,
       cleanup at the end.
  - Keep the worked example but use the new commands.
- Rewrite `docs/install.md`:
  - Two install paths:
    - **Per-project remote install** (recommended for users) —
      Option B from ADR-029. Step-by-step, version-pinned.
    - **Local kit clone** (for kit contributors) — moved to its
      own clearly-labelled subsection. Reference the dogfooding
      playbook at `~/dotfiles/claude-config/docs/dogfooding-playbook.md`.
  - Update the "Manual install alternative" section to reflect
    the new fetch path (manual = clone, copy files yourself, no
    bootstrap script).
- Update `skills/release/SKILL.md`:
  - Under the release flow (probably step 8 or so where the
    GitHub Release is created), add a step to upload
    `bin/bootstrap-workflow-kit` as a release asset via
    `gh release upload TAG bin/bootstrap-workflow-kit`.
- Run `bin/sync-adr-index` after the ADR lands.

Acceptance criteria
- `bin/bootstrap-workflow-kit` exists, is executable, and (when
  pointed at a tagged release that exists) successfully scaffolds
  a target project end-to-end.
- The README's primary install flow no longer requires a
  pre-existing local kit clone.
- The local-clone path is preserved in `docs/install.md` under a
  contributor-flagged section.
- `skills/release/SKILL.md` documents the bootstrap-asset upload
  step.
- ADR-029 is `accepted`; ADR index reflects that.

Scope and constraints
- Primary folders: `bin/`, `README.md`, `docs/install.md`,
  `skills/release/`, `design/adr/`, `prompts/`, `notes/` (only
  if a feature-ideas entry should be marked).
- Folders to avoid: `templates/`, `examples/`, other skills.
- Do not modify `bin/install-workflow-kit`'s behaviour; ADR-029
  explicitly does not supersede ADR-009.
- Bash 3.2+ compatibility on macOS. Trap-based cleanup must
  fire on both success and failure paths.
- Document the script clearly at the top with usage and env vars.

Evaluation & testing requirements
- Run the bootstrap script on a scratch directory pointed at the
  in-flight v3.2.0 tag (will need a dry-run mode or running
  after the tag lands; for the issue's session, manual testing
  via local clone simulating the fetch is acceptable).
- Verify the trap cleans up the temp dir even when the installer
  exits non-zero.
- Verify `gh`-fallback path works (test by temporarily aliasing
  `gh` to a no-op).
- All existing tests pass.

Instructions for you
1. Read the relevant docs:
   - `CLAUDE.md`
   - `design/adr/adr-009-installer-script.md` (the parent decision)
   - `design/adr/adr-029-per-project-remote-install.md` (this
     issue's decision)
   - existing `bin/install-workflow-kit` (especially how it
     resolves `KIT_ROOT` from script location)
   - existing `README.md` (post ADR-028 rewrite)
   - existing `docs/install.md`
   - `skills/release/SKILL.md`
2. Propose a short, step-by-step PLAN:
   - the bootstrap script's exact shape (function structure, error
     handling, fallbacks),
   - the new README "Quick start" structure,
   - the docs/install.md restructure (two-path layout),
   - the skills/release/SKILL.md additions.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - one logical commit per concern (bootstrap script, README,
     docs/install.md, release-skill update, ADR-index sync).
   - each commit references ADR-029 and #36.
5. At the end, provide an evaluation summary:
   - the bootstrap script (shown in full or summarized),
   - the new README quick-start (quoted),
   - the new docs/install.md structure,
   - testing notes,
   - exact commands I should run to verify.

Do not start editing files until I explicitly approve your plan.
