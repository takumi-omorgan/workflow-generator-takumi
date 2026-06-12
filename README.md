# Claude Code Workflow Kit

A toolkit of Claude Code skills, templates, and docs that gives any
**new, structured project** — software or not — a disciplined,
GitHub-first path from a rough idea to a tagged release. You install it
into your own project; it drives the flow through a PRD, recorded
decisions (ADRs), a continuously maintained architecture document, GitHub
issues, and pull requests.

## Who it's for

A solo founder, indie hacker, researcher, writer, or experienced
developer starting a **new** project who wants explicit decisions and
incremental, reviewable work without reinventing a workflow each time.
The primitives — define the problem, scope the first cut, record
decisions, break work into issues, review via PR — fit any structured
project: software, research papers, books, curricula, content, design
systems, internal policy. What the kit assumes (a git repo, GitHub,
Claude Code) and what it does not is spelled out in
[`docs/install.md`](docs/install.md).

> **Not for** existing repos (the kit is new-projects-only), non-GitHub
> providers, or non-Claude tooling.

## Quick start

**Prerequisites (once per machine):** Git, the GitHub CLI (`gh`,
authenticated), and Claude Code. Verification commands are in
[`docs/install.md`](docs/install.md#1-prerequisites).

**Install into a new project.** Replace `my-project` with your own
name — it becomes both the GitHub repo and the local folder:

```bash
gh repo create my-project --public --clone
cd my-project
bash <(curl -fsSL https://github.com/olivermorgan2/claude-workflow-kit/releases/download/v5.0.0/bootstrap-workflow-kit) \
  --project-name=my-project
```

That one command fetches the kit at a pinned version, copies the
skills into `.claude/skills/`, renders your `CLAUDE.md`, and makes the
first commit. It is idempotent — re-running skips existing files. Optional
AI PR review is off by default; add `--with-ai-review` if you want the
project-local `/review-pr` runtime installed under `.claude/`.
Verify the install from the terminal (`.claude/` is hidden in file
browsers):

```bash
ls .claude/skills     # → adr-writer  idea-to-prd  prd-normalizer  prd-to-mvp  …
```

> Prefer to inspect the script first, install manually, or pin a
> different version? Those paths are in
> [`docs/install.md`](docs/install.md#3-install-the-kit-into-the-target-project).

**Then build something.** Open Claude Code (`claude`) in the project
and follow the tutorial:

➡️ **[Your first PR in 15 minutes](docs/tutorial.md)** — from a
one-line idea to a merged pull request in five commands.

## The workflow in one minute

The kit is a small set of slash commands you run inside Claude Code.
The core loop — **scope → backlog → implement → ship** — repeats for
the life of the project:

| Stage | Commands | Output |
|---|---|---|
| Scope | `/idea-to-prd`, `/prd-normalizer`, `/prd-to-mvp` | PRD, MVP, build-out plan |
| Decide | `/adr-writer` | ADRs in `design/adr/` |
| Backlog | `/issue-planner` | GitHub issues + project board |
| Implement | `/prepare-issue`, `/claude-issue-executor` | feature branch, tests, commits |
| Ship | `/pr-review-packager`, `/changelog`, `/release`, `/workflow-docs` | PR, release notes, refreshed README/architecture/AI summary, tagged release |

Plan-first throughout: Claude Code proposes a plan, you approve, then
it implements. Work is scoped one GitHub issue per branch and PR,
following [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow).
The kit covers the whole lifecycle — not just scaffolding, but ongoing
ADRs, continuous architecture-document maintenance, issue-by-issue execution,
releases, and session continuity.

Not sure what to run? Type **`/start`** (or `/next`) and the kit
inspects your project and tells you the next step. The full command set
sits behind a small **verb layer** — `/start`, `/decide`, `/backlog`,
`/work`, `/ship`, `/release` — and three **operating modes**
(interactive, assisted, autonomous) that set how much the assistant does
without asking. See [workflow control](docs/workflow-control.md).

## What's in this repo

| Path | What it is |
|---|---|
| `skills/` | The Claude Code skills the kit ships |
| `templates/` | Starter templates rendered into your project |
| `docs/` | Install, architecture, tutorial, workflow, troubleshooting, skills |
| `examples/` | [Worked end-to-end projects](examples/README.md) |

See [`docs/repo-structure.md`](docs/repo-structure.md) for the full map
of what lives in the kit versus what gets generated in your project.

## Docs

- [Install guide](docs/install.md) — all install paths, prerequisites, manual flow
- [First PR in 15 minutes](docs/tutorial.md) — the fastest happy path
- [Architecture](docs/architecture.md) — how the kit itself is organized
- [Workflow guide](docs/workflow-guide.md) — idea to release, end to end
- [Workflow control](docs/workflow-control.md) — operating modes, the approval gate, the verb layer
- [Skills reference](docs/skills.md) — what every skill does
- [AI PR review](docs/ai-review.md) — dry-run AI review of a PR, then publish comments safely (`/review-pr`)
- [Troubleshooting](docs/troubleshooting.md) — fixes organized by symptom
- [GitHub setup](docs/github-setup.md) — labels, milestones, scopes

## Status and license

In active development; the latest release is on the
[releases page](https://github.com/olivermorgan2/claude-workflow-kit/releases).
Released under the [MIT License](LICENSE), which covers the **kit
itself** — the skills, templates, scripts, and docs here. It does not
propagate to projects you build with the kit: your `design/` docs,
prompts, and source code are yours to license as you choose.
