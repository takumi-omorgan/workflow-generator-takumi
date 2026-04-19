# Claude Code Workflow Kit

A GitHub-distributed toolkit of Claude Code skills, templates, and workflow
docs that helps a solo developer or small team set up a GitHub-first software
delivery workflow for a **new** software project. The kit takes a user from a
rough idea, a standard PRD, or a custom PRD to an implementation-ready backlog
of ADRs, GitHub issues, and Claude Code prompts.

## Who this is for

- A solo technical founder, indie hacker, or experienced developer starting a
  **new** project who wants to move fast without reinventing a workflow.
- A small team or consultant that wants a reusable, low-ceremony operating
  system for GitHub-based delivery with Claude Code.

## Who this is **not** for (in v1)

- Anyone trying to retrofit this workflow onto an **existing** repository.
- Teams that need non-GitHub providers (GitLab, Bitbucket) or non-Claude AI
  tooling.
- Anyone looking for a hosted UI or a SaaS product — this is a kit you
  install into your own project.

See [ADR-002](Design/adr/adr-002-new-project-only-scope.md) for why v1 is
new-projects-only and [`docs/install.md`](docs/install.md#what-v1-does-not-support)
for the full list of non-goals.

## At a glance

- **New projects only** — v1 will not adapt existing repos.
- **Project-local install** — each new project gets its own copy of the
  skills under `.claude/skills/`. No global install required.
- **GitHub-first** — issues, labels, milestones, PRs, `main + feature`
  branch model aligned with [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).
- **Plan-first execution** — Claude Code proposes a plan, you approve,
  then it implements.
- **Three starting paths** — rough idea, standard PRD, or custom PRD.
- **Full end-to-end flow** — see [`docs/workflow-guide.md`](docs/workflow-guide.md)
  for idea → PRD → MVP → ADRs → issues → PRs → release in one pass.

## Quick start

### One-time setup (per machine)

Install Git, GitHub CLI, and Claude Code, then authenticate `gh`. Verification
commands are in [`docs/install.md`](docs/install.md#1-prerequisites).

Clone this kit once, anywhere outside your projects. You reuse this clone
for every new project you start:

```bash
git clone git@github.com:olivermorgan2/workflow-generator.git ~/src/workflow-generator
```

### Per new project

Throughout these steps, replace `my-project` with the name you want for
your new project (e.g. `invoice-tracker`). That name becomes both the
GitHub repo and the local folder.

1. `cd` into the directory where you want the new project folder to live
   (e.g. `cd ~/src`). The next command creates the project folder inside
   your current working directory.

2. Create the project on GitHub, clone it locally, and `cd` into it.
   `my-project` here is a placeholder — use your own name:

   ```bash
   gh repo create my-project --public --clone
   cd my-project
   ```

3. Run the installer from your kit clone. It scaffolds the folders,
   copies the skills into `.claude/skills/`, renders `CLAUDE.md` from the
   template, and makes the initial commit:

   ```bash
   ~/src/workflow-generator/bin/install-workflow-kit --project-name=my-project
   ```

   Add `--with-docs` if you want the kit's reference docs copied into
   `docs/workflow-kit/` alongside the project ([ADR-010](Design/adr/adr-010-optional-with-docs-flag.md)).
   See `--help` for the full flag list. The installer is idempotent —
   re-running it on an already-installed project skips existing files.

   > **Note — hidden folders.** `.claude/` starts with a dot, so it is
   > hidden by default in macOS Finder and Windows Explorer. Verify the
   > install from the terminal instead: `ls .claude/skills` should show
   > the skill directories (`idea-to-prd`, `prd-normalizer`, `prd-to-mvp`,
   > `adr-writer`, …).

4. Open Claude Code in the project and run the skill that matches what you
   have in hand:

   | You have… | Run |
   |---|---|
   | A rough idea | `/idea-to-prd` |
   | A standard or custom PRD | `/prd-normalizer`, then `/prd-to-mvp` |

Prefer the manual copy flow (or need to see exactly what the installer
does)? The manual steps are preserved in
[`docs/install.md`](docs/install.md#3b-manual-install-alternative).

### Worked example

Installing the kit into a new project called `invoice-tracker`, starting
from `~/src` with the kit already cloned at `~/src/workflow-generator`:

```bash
cd ~/src                                                       # step 1
gh repo create invoice-tracker --public --clone                # step 2
cd invoice-tracker
~/src/workflow-generator/bin/install-workflow-kit \
  --project-name=invoice-tracker                               # step 3
ls .claude/skills                                              # verify
# → adr-writer  idea-to-prd  prd-normalizer  prd-to-mvp
claude                                                         # step 4
# then inside Claude Code: /idea-to-prd
```

Full step-by-step guide, including the manual install path,
`CLAUDE.md` details, and troubleshooting:
[`docs/install.md`](docs/install.md). For the end-to-end flow from idea
to shipped release, see [`docs/workflow-guide.md`](docs/workflow-guide.md).

## What is in this repo

| Path | What it is |
|---|---|
| `Design/adr/` | Accepted ADRs that govern the kit |
| `docs/` | Kit documentation |
| `skills/` | Source of the Claude Code skills shipped by the kit |
| `templates/` | Starter templates rendered into target projects |
| `examples/` | Planning-path walkthroughs and a gallery of end-to-end [worked projects](examples/README.md) |
| `notes/` | Working notes for building the kit |

See [`docs/repo-structure.md`](docs/repo-structure.md) for the full map of
what lives in the kit versus what gets generated inside a target project.

## Status

Milestones M1–M5 shipped. v1 is feature-complete for the "new project only"
scope (see [ADR-002](Design/adr/adr-002-new-project-only-scope.md)); further
work is tracked in `notes/feature-ideas.md` and as issues under future
milestones.

## License

Not yet specified. A `LICENSE` file will be added before v1 is announced
externally — see `notes/feature-ideas.md` for open questions.
