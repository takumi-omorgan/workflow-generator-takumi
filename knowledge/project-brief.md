# Project Brief

## What the kit is

The **Claude Code Workflow Kit** is a GitHub-first, project-local Claude
Code workflow kit for **new** structured projects (software or not). It
ships skills, templates, and docs that a user installs into their own new
project under `.claude/skills/`. From a rough idea, it drives a disciplined
path to a tagged release through a PRD, recorded decisions (ADRs), GitHub
issues, and pull requests.

It is scoped to new projects only and assumes a git repo, GitHub, and
Claude Code. See `README.md`, `docs/repo-structure.md`, and the accepted
ADRs in `design/adr/` for the authoritative details.

## Lifecycle

The kit's core loop repeats for the life of a project:

**Scope → Decide → Backlog → Implement → Ship**

| Stage | What happens |
|---|---|
| **Scope** | Turn an idea into a PRD, normalize it, and carve out an MVP / build-out plan |
| **Decide** | Record durable decisions as ADRs |
| **Backlog** | Break the plan into GitHub issues on a project board |
| **Implement** | Plan-first, one issue per branch and PR: prepare the issue, execute, test, commit |
| **Ship** | Package the PR, write release notes, and tag a release |

Work is plan-first throughout (Claude proposes a plan, the human approves,
then it implements) and scoped one GitHub issue per branch/PR following
GitHub Flow.

## Public / private split

This kit is developed across two repositories:

- **Public** — `olivermorgan2/claude-workflow-kit`: the distributed kit
  (skills, templates, docs, installer, releases) that end users install.
- **Private / source** — `takumi-omorgan/workflow-generator-takumi`
  (this repo): the working source of truth where the kit is built.

Internal ADRs, evals, roadmaps, and source notes **stay in the private
repo** unless we deliberately promote a curated, public-ready version to
the public repo. Promotion is an explicit, reviewed act — nothing leaks to
public by default.

> **Naming note.** Some existing in-repo links (e.g. release URLs in
> `README.md`) reference `olivermorgan2/workflow-generator`. The
> public-repo name recorded here is the operating name supplied for this
> collaboration; reconcile the two before any public release. Tracked in
> [open-questions.md](open-questions.md).

## Collaboration protocol

We run an operating protocol **layered on top of** the kit. It is a way of
working, **not** a feature wired into the kit's skills, installer, or
runtime. The kit stays generic; this protocol governs how *we* build it.

### Roles

| Actor | Role |
|---|---|
| **Claude Code (Opus 4.8)** | Builder / planner / implementer / knowledge curator |
| **Codex** | Adversarial reviewer / scorer |
| **Hermes** | Orchestrator / verifier / closeout reporter |

### Gates

- **PRD gate** — Claude drafts the PRD; Codex reviews; Claude revises once;
  knowledge layer is updated.
- **Milestone / ADR gate** — Claude drafts the milestone or ADR; Codex
  reviews; Claude revises once; knowledge layer is updated.
- **PR quality gate** — Codex runs a scored review loop. Targets:
  **4/5 score**, **zero blockers**, **green validation**, and at most
  **3 review loops**.

### Knowledge curation

Claude curates this knowledge layer as it works: persisting decisions,
risks, open questions, distilled review findings, and glossary/domain
facts — while keeping out raw chat, temporary task state, stale PR
mechanics, and minor suggestions. The full rules live in
[SCHEMA.md](SCHEMA.md).
