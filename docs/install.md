# Install Guide

How to install the Claude Code Workflow Kit into a **new** software project.

> **Before you start:** v1 of the kit is for **new projects only**. It does
> not adapt or migrate existing repositories. If you want to add the
> workflow to an existing codebase, this release is not the right fit —
> see [What v1 does not support](#what-v1-does-not-support) below and
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

The kit does not have an installer script in v1. Installation is a small,
explicit copy step so nothing is hidden.

### 3.1 Clone the kit somewhere outside the target project

```bash
git clone git@github.com:olivermorgan2/workflow-generator.git ~/src/workflow-generator
```

You only need one clone of the kit per machine. You can reuse it for
every new project.

### 3.2 From inside the target project, copy the skills

```bash
cd my-project                                   # target project root
mkdir -p .claude/skills Design/adr notes
cp -R ~/src/workflow-generator/skills/* .claude/skills/
```

This is the step that makes the install **project-local**: the skills now
live under the target project's own `.claude/skills/`, tracked in the
target project's git history. The kit clone is no longer required for
those skills to work.

### 3.3 Render the starter `CLAUDE.md`

`CLAUDE.md` at the project root is Claude Code's primary rules file for
the project. Copy the template and fill in the project-specific fields:

```bash
cp ~/src/workflow-generator/templates/claude-md-template.md CLAUDE.md
```

> The template will be added in Issue #4. Until then, you can hand-write
> a minimal `CLAUDE.md` using the stub in this kit's root as a reference.

### 3.4 Commit the install

```bash
git add .claude CLAUDE.md Design notes
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
  notes/
```

A quick check:

```bash
ls .claude/skills          # should list the skill directories
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

Run the chosen skill inside the target project using Claude Code.
Detailed usage guidance will live in `docs/claude-code-guide.md` (a later
issue). For now, each skill's own `SKILL.md` is the authoritative spec.

---

## What v1 does not support

Per [ADR-002](../Design/adr/adr-002-new-project-only-scope.md) and the
MVP spec, v1 intentionally does **not** include:

- **Retrofitting existing repositories.** The kit assumes a clean slate.
  Pointing it at an established codebase will not produce useful output.
- **A global install.** Every target project gets its own copy of the
  skills. This is a design choice, not a limitation (see ADR-001).
- **An installer script.** Installation is a documented copy flow in v1.
  Automation is a Phase 2 candidate.
- **Team/multi-repo features.** The kit is scoped to a solo developer or
  small team working on a single project at a time.
- **Non-GitHub providers.** The workflow is GitHub-first
  ([ADR-004](../Design/adr/adr-004-github-first-workflow-model.md)).
  GitLab, Bitbucket, and others are not supported in v1.
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
command in step 3.1.

**`cp: ~/src/workflow-generator/skills/*: No such file or directory`**
The kit was cloned to a different path than the guide assumes. Either
re-clone to `~/src/workflow-generator` or substitute your actual path in
step 3.2.

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

- [`docs/repo-structure.md`](repo-structure.md) — how the kit is laid out and what it generates
- [`docs/github-setup.md`](github-setup.md) — GitHub labels, milestones, and branch conventions
- `docs/workflow-guide.md` — end-to-end flow from idea to deploy (coming in a later issue)
