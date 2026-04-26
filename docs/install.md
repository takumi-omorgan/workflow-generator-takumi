# Install Guide

How to install the Claude Code Workflow Kit into a **new** project. The
kit is project-agnostic (per [ADR-028](../Design/adr/adr-028-workflow-agnostic-framing.md))
— software, research, content, curriculum, or any other structured
project that fits the kit's three assumptions: a git repo, GitHub, and
Claude Code.

> **Before you start:** the kit is for **new projects only**. It does
> not adapt or migrate existing repositories. If you want to add the
> workflow to an existing codebase, this kit is not the right fit —
> see [What this kit does not support](#what-this-kit-does-not-support) below and
> [ADR-002](../Design/adr/adr-002-new-project-only-scope.md).

The kit uses a **project-local installation model**: each new target
project gets its own copy of the skills under `.claude/skills/`. There is
no global install. See [ADR-001](../Design/adr/adr-001-project-local-installation-model.md)
for the reasoning.

---

## 1. Prerequisites

Install these once per machine. The kit assumes macOS or Linux; commands
are cross-platform where possible.

| Tool | Purpose | Install |
|---|---|---|
| **Git** | Version control | Ships with macOS (Xcode CLT) or `brew install git` |
| **GitHub CLI (`gh`)** | Repo, issue, and PR operations from the terminal | `brew install gh` then `gh auth login` |
| **Claude Code** | AI-assisted development | `npm install -g @anthropic-ai/claude-code` |
| **SSH key** | Passwordless git over SSH | `ssh-keygen -t ed25519` then add the public key to GitHub |

### Verify the setup

```bash
git --version          # any recent 2.x is fine
gh --version           # any recent 2.x is fine
gh auth status         # should report "Logged in to github.com"
claude --version       # confirms Claude Code is on your PATH
ssh -T git@github.com  # "Hi <user>! You've successfully authenticated"
```

If any of these fail, fix the failing tool before continuing — the rest of
the guide assumes they all pass.

---

## 2. Choose your target project

Pick **one** of these two paths. The rest of the guide assumes you end up
inside the target project directory.

**A. Create the repo on GitHub first** (recommended):

```bash
gh repo create my-project --public --clone   # use --private if appropriate
cd my-project
```

**B. Start locally, add the remote later:**

```bash
mkdir my-project && cd my-project
git init
```

---

## 3. Install the kit into the target project

You have two options:

- **Automated install** (recommended) — run `bin/install-workflow-kit` from
  the kit clone. See [3A](#3a-automated-install-recommended) below.
- **Manual install** — a small, explicit copy flow. See
  [3B](#3b-manual-install-alternative) below. The manual flow is the
  documented fallback and remains fully supported.

Either path produces the same target-project layout described in
[`docs/repo-structure.md`](repo-structure.md).

### 3A. Automated install (recommended)

Once you have cloned the kit (see [3B.1](#3b1-clone-the-kit-somewhere-outside-the-target-project)
for the one-time clone step), the installer scaffolds the target project in
a single command. It is implemented per
[ADR-009](../Design/adr/adr-009-installer-script.md) and
[ADR-010](../Design/adr/adr-010-optional-with-docs-flag.md).

```bash
cd my-project                                              # target project root
~/src/workflow-generator/bin/install-workflow-kit \
  --project-name=my-project
```

What it does, in order:

1. Creates `Design/adr/`, `prompts/`, `notes/`, and `.claude/skills/` in
   the target project.
2. Copies every skill from the kit's `skills/` into `.claude/skills/`.
3. Seeds `prompts/_template.md` so new per-issue prompts stay consistent
   (ADR-008).
4. Renders `CLAUDE.md` from `templates/claude-md-template.md` (ADR-007).
   You are prompted for any `{{UPPER_SNAKE}}` placeholder not provided on
   the command line, unless `--non-interactive` is set.
5. `git init`s the target if it is not already a git repo, then creates
   an initial commit `chore: install workflow kit (project-local)`.

Useful flags:

| Flag | What it does |
|---|---|
| `--target=PATH` | Target project directory (default: current dir) |
| `--project-name=NAME` | Value for `{{PROJECT_NAME}}` in `CLAUDE.md` |
| `--set KEY=VALUE` | Provide a value for any other `{{UPPER_SNAKE}}` placeholder. Repeatable. |
| `--with-docs` | Also copy kit docs to `docs/workflow-kit/` in the target (ADR-010) |
| `--force` | Overwrite existing `CLAUDE.md` and re-copy skills |
| `--no-commit` | Skip the initial commit |
| `--non-interactive` | Never prompt; fall back to defaults |
| `-h`, `--help` | Show full usage |

The script is idempotent: running it again on an already-installed target
skips files that already exist and makes no commit if nothing changed.
Pass `--force` if you want to re-render `CLAUDE.md` or re-copy the skills.

If the automated path does not fit your setup — e.g. you want to tweak a
step, or your project already has a conflicting layout — fall through to
the [manual install](#3b-manual-install-alternative).

### 3B. Manual install (alternative)

The manual flow is the explicit, do-it-yourself version of what the
installer does. Use it when you want full visibility, or as a diagnostic
reference if the installer misbehaves.

#### 3B.1 Clone the kit somewhere outside the target project

```bash
git clone git@github.com:olivermorgan2/workflow-generator.git ~/src/workflow-generator
```

You only need one clone of the kit per machine. You can reuse it for
every new project.

#### 3B.2 From inside the target project, copy the skills

```bash
cd my-project                                   # target project root
mkdir -p .claude/skills Design/adr prompts notes
cp -R ~/src/workflow-generator/skills/* .claude/skills/
cp ~/src/workflow-generator/prompts/_template.md prompts/_template.md
```

The `prompts/` folder holds one filled session brief per GitHub issue
(`issue-NNN-short-title.md`), copied from `_template.md`. Freeform
working notes stay in `notes/`. See [ADR-008](../Design/adr/adr-008-dedicated-prompts-folder.md).

This is the step that makes the install **project-local**: the skills now
live under the target project's own `.claude/skills/`, tracked in the
target project's git history. The kit clone is no longer required for
those skills to work.

The `prompts/` folder is where per-issue session briefs live (ADR-008).
Seed it with the reusable template from the kit:

```bash
cp ~/src/workflow-generator/notes/issue-prompt.md prompts/_template.md
```

#### 3B.3 Render the starter `CLAUDE.md`

`CLAUDE.md` at the project root is Claude Code's primary rules file for
the project. Copy the template and fill in the project-specific fields by
hand:

```bash
cp ~/src/workflow-generator/templates/claude-md-template.md CLAUDE.md
```

The template uses `{{PLACEHOLDER}}` tokens (ADR-007). Open `CLAUDE.md`
and replace each one with real values, starting with `{{PROJECT_NAME}}`.
The automated installer above does this substitution for you.

#### 3B.4 Commit the install

```bash
git add .claude CLAUDE.md Design prompts notes
git commit -m "chore: install workflow kit (project-local)"
```

---

## 4. Verify the install

After step 3 the target project should look like this (trimmed):

```
my-project/
  CLAUDE.md
  .claude/
    skills/
      idea-to-prd/          # plus the other skills shipped by the kit
  Design/
    adr/
  prompts/
    _template.md            # blank template; copy to start an issue session
  notes/
```

A quick check:

```bash
ls .claude/skills          # should list the skill directories
ls prompts                 # should list _template.md
cat CLAUDE.md | head -20   # should show your project rules, not this kit's
```

For the full expected layout and which artifacts originate where, see
[`docs/repo-structure.md`](repo-structure.md).

---

## 5. Pick a starting path

The kit supports three ways to start planning, defined in
[ADR-003](../Design/adr/adr-003-prd-intake-model.md). Pick the one that
matches what you have in hand:

| You have… | Use this skill | Status |
|---|---|---|
| A rough idea, no PRD | `idea-to-prd` | Issue #5 |
| A standard PRD | `prd-normalizer` → `prd-to-mvp` | Issue #6, #7 |
| Mixed notes / custom PRD format | `prd-normalizer` → `prd-to-mvp` | Issue #6, #7 |

Run the chosen skill inside the target project using Claude Code. For
how to invoke skills, use plan mode, and follow the approve-then-implement
loop, see [`claude-code-guide.md`](claude-code-guide.md). Each skill's
own `SKILL.md` remains the authoritative spec for its inputs and outputs.

---

## What this kit does not support

The kit intentionally does **not** include:

- **Retrofitting existing repositories.** The kit assumes a clean slate.
  Pointing it at an established codebase will not produce useful output.
- **A global install.** Every target project gets its own copy of the
  skills. This is a design choice, not a limitation (see ADR-001).
- **Team/multi-repo features.** The kit is scoped to a solo author or
  small team working on a single project at a time.
- **Non-GitHub providers.** The workflow is GitHub-first
  ([ADR-004](../Design/adr/adr-004-github-first-workflow-model.md)).
  GitLab, Bitbucket, and others are not supported.
- **Non-Claude AI tools.** The skills target Claude Code specifically
  ([ADR-006](../Design/adr/adr-006-claude-code-execution-model.md)).

If any of the above is a hard requirement for your project, this release
is not the right fit — revisit after Phase 2.

---

## Troubleshooting

**`gh: command not found`**
Install the GitHub CLI (`brew install gh` on macOS) and run `gh auth login`.

**`gh auth status` reports you are logged out**
Run `gh auth login`. Choose SSH as the git protocol to match the clone
command in step 3B.1.

**`cp: ~/src/workflow-generator/skills/*: No such file or directory`**
The kit was cloned to a different path than the guide assumes. Either
re-clone to `~/src/workflow-generator` or substitute your actual path in
step 3B.2 (or pass the correct path to `bin/install-workflow-kit`).

**`install-workflow-kit: error: kit skills/ not found`**
The installer resolves its sources relative to its own location. Run it
directly from the kit clone (e.g. `~/src/workflow-generator/bin/install-workflow-kit`),
not via a copy detached from the kit repo.

**Claude Code does not see the skills**
Confirm you are running Claude Code from the **target project's root**.
Project-local skills are discovered relative to the current working
directory. If you `cd` into a subdirectory, skills still resolve, but if
you run Claude Code from an unrelated directory they will not.

**I already have a `Design/` or `.claude/` in the target project**
The copy commands in step 3 use `mkdir -p` and directory-level `cp -R`,
so they will not overwrite files that already exist with different
names. If you want to replace them wholesale, remove them first.

---

## What's next

- [`docs/workflow-guide.md`](workflow-guide.md) — end-to-end flow from idea to shipped release
- [`docs/repo-structure.md`](repo-structure.md) — how the kit is laid out and what it generates
- [`docs/github-setup.md`](github-setup.md) — GitHub labels, milestones, and branch conventions
