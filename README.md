# Claude Code Workflow Kit

A toolkit of Claude Code skills, templates, and workflow docs that
gives **any structured project** — software or otherwise — a
disciplined, GitHub-first delivery flow. The kit takes a user from a
rough idea (or an existing PRD) to an implementation-ready backlog of
ADRs, GitHub issues, and Claude Code session prompts, then drives the
work to a tagged release.

The kit is project-agnostic. Software is one strong use case; it is
not the only one. See [What this is good for](#what-this-is-good-for)
for the range of project shapes the kit fits.

## Who this is for

- A solo founder, indie hacker, researcher, writer, designer, or
  experienced developer starting a **new** project who wants
  explicit decisions, planning, and incremental work without
  reinventing a workflow each time.
- A small team or consultant that wants a reusable, low-ceremony
  operating system for GitHub-based delivery with Claude Code.

## What this is good for

The kit's primitives — define the problem (PRD), scope the first cut
(MVP), record decisions (ADRs), break work into issues, drive
execution through disciplined Claude Code sessions, review via PR —
work for any structured project, not only code. Examples that fit
cleanly:

- **Software** — CLIs, libraries, web apps, services, scripts. The
  obvious case; most of the kit's examples gallery shows this shape.
- **Research projects** — papers, dissertations, technical reports.
  PRD = research proposal; MVP = first complete draft; ADRs =
  methodological decisions; issues = chapter sections.
- **Technical writing and books** — chapter scope, structural
  decisions, draft cycles.
- **Curriculum design** — course outlines, module plans, pedagogy
  decisions captured as ADRs.
- **Content projects** — newsletters, podcasts, video series.
  Editorial choices become ADRs; episode plans become issues.
- **Design system docs** — token decisions, component scope, layout
  rules, accessibility commitments.
- **Internal-policy documents** — HR handbooks, security procedures,
  compliance manuals. Anywhere decisions need to be recorded and
  revisited.

The kit's vocabulary leans software (`product`, `user stories`,
`capabilities`, `MVP`). For non-software projects, the metaphor still
maps: a research paper has a "product" (the paper) and "users"
(audience); a curriculum has "capabilities" (what students can do
after); a book has "user stories" (reader-shaped journeys).

### What the kit assumes

- A **git repository** for the project.
- **GitHub** for issues, milestones, labels, and PRs (per ADR-004).
- **Claude Code** as the LLM driver.

### What the kit does **not** assume

- A specific programming language or stack — markdown-only repos
  work fine.
- A test runner, package manager, or deployment pipeline.
- That deliverables are code at all.

## Who this is **not** for

- Anyone trying to retrofit this workflow onto an **existing**
  repository — the kit is designed for new projects (per ADR-002,
  superseded scope clarification in ADR-022).
- Teams that need non-GitHub providers (GitLab, Bitbucket) or
  non-Claude AI tooling.
- Anyone looking for a hosted UI or a SaaS product — this is a kit
  you install into your own project.

See [`docs/install.md`](docs/install.md#what-this-kit-does-not-support)
for the full list of non-goals.

## At a glance

- **New projects only** — does not adapt existing repos.
- **Project-local install** — each new project gets its own copy of
  the skills under `.claude/skills/`. No global install required.
- **GitHub-first** — issues, labels, milestones, PRs, `main + feature`
  branch model aligned with [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).
- **Plan-first execution** — Claude Code proposes a plan, you
  approve, then it implements (per ADR-006 / ADR-014).
- **Three starting paths** — rough idea, standard PRD, or custom PRD.
- **Full lifecycle** — covers initial scaffolding *and* ongoing
  development: new ADRs as decisions arise, issue-by-issue work
  through the executor, PR packaging, changelog, and tagged
  releases.

## Quick start

### One-time setup (per machine)

> **Skip this section if you already have Git, the GitHub CLI, and
> Claude Code installed and `gh` authenticated.** This setup runs
> once per machine, not once per project — and there is no
> long-lived kit clone to maintain.

Install Git, GitHub CLI, and Claude Code, then authenticate `gh`.
Verification commands are in
[`docs/install.md`](docs/install.md#1-prerequisites).

### Per new project

Throughout these steps, replace `my-project` with the name you want
for your new project (e.g. `invoice-tracker`). That name becomes
both the GitHub repo and the local folder.

1. `cd` into the directory where you want the new project folder to
   live (e.g. `cd ~/src`). The next command creates the project
   folder inside your current working directory.

2. Create the project on GitHub, clone it locally, and `cd` into it.
   `my-project` here is a placeholder — use your own name:

   ```bash
   gh repo create my-project --public --clone
   cd my-project
   ```

3. Run the kit's bootstrap installer. It fetches the kit at a pinned
   version from GitHub, scaffolds the folders, copies the skills
   into `.claude/skills/`, renders `CLAUDE.md` from the template,
   makes the initial commit, and discards the temporary kit copy
   when done:

   ```bash
   bash <(curl -fsSL https://github.com/olivermorgan2/workflow-generator/releases/download/v3.3.0/bootstrap-workflow-kit) \
     --project-name=my-project
   ```

   Add `--with-docs` if you want the kit's reference docs copied
   into `docs/workflow-kit/` alongside the project. See `--help`
   for the full flag list. The installer is idempotent —
   re-running it on an already-installed project skips existing
   files.

   Prefer to inspect the script before running, or pipe-to-bash
   makes you nervous? Download it first, then run:

   ```bash
   gh release download v3.3.0 -p bootstrap-workflow-kit \
     -R olivermorgan2/workflow-generator
   chmod +x bootstrap-workflow-kit
   ./bootstrap-workflow-kit --project-name=my-project
   ```

   See the [explicit-fetch alternative](docs/install.md#explicit-fetch-alternative)
   in `docs/install.md` for an even more transparent three-line form
   (no bootstrap script — `gh repo clone` directly into a temp dir
   and run the installer).

   > **Note — hidden folders.** `.claude/` starts with a dot, so it
   > is hidden by default in macOS Finder and Windows Explorer.
   > Verify the install from the terminal: `ls .claude/skills`
   > should show the skill directories (`idea-to-prd`,
   > `prd-normalizer`, `prd-to-mvp`, `adr-writer`, …).

4. Open Claude Code in the project and run the skill that matches
   what you have in hand:

   | You have… | Run |
   |---|---|
   | A rough idea | `/idea-to-prd` |
   | A standard or custom PRD | `/prd-normalizer`, then `/prd-to-mvp` |
   | A PRD already drafted (by hand or via any external LLM) using `templates/prd-template.md` | `/prd-normalizer` |

Prefer the manual copy flow (or need to see exactly what the
installer does)? The manual steps are preserved in
[`docs/install.md`](docs/install.md#3b-manual-install-alternative).

### Worked example

Installing the kit into a new project called `invoice-tracker`,
starting from `~/src`:

```bash
cd ~/src                                                       # step 1
gh repo create invoice-tracker --public --clone                # step 2
cd invoice-tracker
bash <(curl -fsSL https://github.com/olivermorgan2/workflow-generator/releases/download/v3.3.0/bootstrap-workflow-kit) \
  --project-name=invoice-tracker                               # step 3
ls .claude/skills                                              # verify
# → adr-writer  idea-to-prd  prd-normalizer  prd-to-mvp
claude                                                         # step 4
# then inside Claude Code: /idea-to-prd
```

Pinning the kit version is recommended — `v3.3.0` in the URL above
locks the install to that release, so re-scaffolding produces the
same result. To check for newer versions, see the
[releases page](https://github.com/olivermorgan2/workflow-generator/releases).

> **Working on the kit itself, or contributing to it?** You'll want
> a long-lived local clone, not the bootstrap flow. See
> [Contributor / kit-developer setup](docs/install.md#contributor--kit-developer-setup)
> in `docs/install.md`.

Full step-by-step guide, including the manual install path,
`CLAUDE.md` details, and troubleshooting:
[`docs/install.md`](docs/install.md). For the end-to-end flow from
idea to shipped release, see
[`docs/workflow-guide.md`](docs/workflow-guide.md).

## Ongoing development

The kit isn't only for initial scaffolding. After the first
`prd-to-mvp` and ADR-writing pass, the same skills cover the
project's lifetime:

- **New decisions arise during the project.** Use `/adr-writer` to
  draft a new ADR for any architectural or methodological choice
  you make as work progresses. Status starts at `proposed`; the
  human review and approval makes it `accepted`. Existing accepted
  ADRs are never edited in place — to change a decision, write a
  new ADR that supersedes the old one (per ADR-022's convention).
- **The ADR index keeps itself in sync.** `bin/sync-adr-index`
  regenerates the table in `design/adr/README.md` from the ADR
  files on disk. The four ADR-touching skills run it automatically;
  manual edits inside the marker fences are overwritten on the next
  sync (per ADR-023).
- **Plan-first issue execution.** For each GitHub issue, run
  `/prepare-issue <NN>` to scaffold a session prompt under
  `prompts/issue-NNN-short-title.md`, then run
  `/claude-issue-executor` to drive a disciplined session: plan
  proposed and approved before any edit, branch from `main`,
  incremental commits referencing the ADR and issue, tests
  alongside, evaluation summary at the end (per ADR-006 / ADR-014).
- **PR packaging.** `/pr-review-packager` reads
  `templates/pr-template.md`, fills `Closes #N` and ADR references
  from the branch and commit history, shows the body for approval,
  and opens the PR via `gh pr create` (per ADR-015).
- **Releases.** `/changelog` produces grouped release notes from
  `git log`; `/release` tags a semver release, generates the notes,
  and publishes a GitHub Release (per ADR-016 / ADR-017).
  Versioning follows ADR-026's MAJOR/MINOR/PATCH classification.
- **Documentation that stays current.** `/workflow-docs`
  regenerates `README.md` and `design/ai-summary.md` from the
  project's PRD, MVP, ADRs, and `CLAUDE.md`. Re-run after any
  meaningful change; manual edits outside the marker fences are
  preserved (per ADR-018).
- **Deeper planning for non-trivial projects (opt-in).**
  `/planning` adds a `design/planning.md` between MVP scoping and
  ADR drafting (decomposition, risks, sequencing — per ADR-031);
  `/clarify` resolves gray areas into a `design/decisions.md`
  append-only log (below ADR weight, per ADR-033). The build-out
  plan can be split into `## Phase N` blocks (per ADR-032), each
  becoming its own GitHub milestone and release boundary; tune the
  phase count with `--granularity={coarse|standard|fine}` on
  `prd-to-mvp` and `/planning` (per ADR-036). `/check-plan` runs
  a structural quality gate over ADRs and issue prompts before
  they're written; chained from `/adr-writer` and `/prepare-issue`,
  with `--skip-check` to opt out (per ADR-034).
- **Session continuity across context resets.**
  `design/state.md` is a small committed pointer (~100 lines) with
  five marker-fenced zones: phase, in-flight issue, recent PRs,
  blockers, continue-here. `/resume` reads it at the start of a
  fresh session; `/pause` refreshes it before a context reset and
  optionally writes a longer `notes/handoff-YYYY-MM-DD.md`
  (per ADR-035).
- **Milestone lifecycle (multi-phase delivery checkpoints).**
  `/audit-milestone <N>` verifies a GitHub milestone is finishable
  (issues closed, ADRs linked to merged PRs, phase exit criteria
  met); `/milestone-summary <N>` generates
  `design/milestones/<N>-<slug>.md` from `git log` + the milestone
  + accepted ADRs; `/complete-milestone <N> [--release]` closes
  the GitHub milestone, archives state.md, and optionally chains
  `/release --milestone-phase=N` (per ADR-037).
- **Lower-friction prompt step for trivial work.**
  `/claude-issue-executor` auto-chains `/prepare-issue` if no
  prompt exists yet, and accepts a `--no-prompt` flag for genuinely
  trivial issues (typo fixes, dependency bumps) — leaving a
  one-line audit-trail breadcrumb in the first commit (per
  ADR-038). Significant sessions use Claude Code's harness-level
  plan mode (`shift+tab shift+tab`); the executor pauses at the
  threshold and asks the user to enter plan mode before proposing
  a plan (per ADR-039).

The full flow from idea to release is documented end-to-end in
[`docs/workflow-guide.md`](docs/workflow-guide.md).

## What is in this repo

| Path | What it is |
|---|---|
| `design/adr/` | Accepted ADRs that govern the kit |
| `docs/` | Kit documentation |
| `skills/` | Source of the Claude Code skills shipped by the kit |
| `templates/` | Starter templates rendered into target projects |
| `examples/` | Planning-path walkthroughs and a gallery of end-to-end [worked projects](examples/README.md) |
| `notes/` | Working notes for building the kit |

See [`docs/repo-structure.md`](docs/repo-structure.md) for the full
map of what lives in the kit versus what gets generated inside a
target project.

## Status

Latest release: see the
[releases page](https://github.com/olivermorgan2/workflow-generator/releases).
The kit is in active development. Versioning follows
[ADR-026](design/adr/adr-026-kit-versioning-policy.md): MAJOR for
breaking changes (placeholder/heading renames, removed skills),
MINOR for additive changes (new skills, new templates, new flags),
PATCH for docs and bug fixes.

Ongoing work and proposed features are tracked in
[`notes/feature-ideas.md`](notes/feature-ideas.md) and as issues
under future milestones.

## License

The kit is released under the [MIT License](LICENSE) (see
[ADR-025](design/adr/adr-025-license.md) for the rationale).

The MIT license covers the **kit itself**: the templates, skills,
scripts, and documentation shipped in this repository. It does not
propagate to projects you build with the kit.

When you run the kit, you author your own content — your
`design/mvp.md`, your `design/prd.md`, your individual ADRs, your
prompts, and the source code, tests, and build artifacts of the
project you are building. **That work is yours.** You choose its
license (or none) independently of the kit's.

The installer can scaffold a starter `LICENSE` into a target project
with `--license=mit --license-holder="Your Name"`, but does not do
so by default — license choice is the project author's call.
