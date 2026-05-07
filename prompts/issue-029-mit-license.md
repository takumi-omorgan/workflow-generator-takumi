You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `design/adr/`.

ADR:
- File: `design/adr/adr-025-license.md`
- Decision: License the kit under MIT, copyright `(c) 2026 Oliver Morgan`.
  Document the kit-vs-user-output boundary in `README.md` and ADR-025.
  Installer does not auto-scaffold a `LICENSE` into target projects;
  optional `--license=mit --license-holder=NAME` flag for users who
  want one.

GitHub Issue:
- Title: License the kit under MIT and clarify kit-vs-user-output
  boundary (ADR-025)
- Number: #29
- Milestone: v3.0.0 — kit hygiene and licensing
- Labels: docs

Goal
Add a `LICENSE` file at the repo root and update `README.md` to
clarify that MIT applies to the kit itself; user-built projects are
the user's own work and not subject to the kit's license.

Why it matters
Without an explicit license, default copyright applies — downstream
users technically cannot redistribute, modify, or fork the kit. For
a kit whose entire purpose is to be installed into other projects,
the absence of a license is the wrong default. It is also a soft
blocker on the public-distribution split tracked as feature-ideas
#19.

Requirements
- Write `LICENSE` at the repo root with the canonical, **unmodified**
  MIT text. Copyright `(c) 2026 Oliver Morgan`. Do not edit the
  canonical wording — license scanners (GitHub, npm, SPDX) need it
  to be recognizable.
- Update `README.md` License section. Replace the "Not yet specified"
  text with a concise section that:
  - links to `LICENSE` and references ADR-025 for rationale,
  - states the MIT license covers the **kit itself** (templates,
    skills, scripts, docs shipped in this repository),
  - states user-built projects are unambiguously the user's work —
    the user authors `design/mvp.md`, `design/prd.md`, individual
    ADRs, prompts, source code, tests, etc., and chooses their own
    license,
  - mentions the optional `--license=mit --license-holder=NAME`
    installer flag for users who want a starter LICENSE scaffolded
    in their target project (default behaviour: no LICENSE
    auto-scaffolded).
- Write `design/adr/adr-025-license.md` documenting:
  - context (no LICENSE today; need explicit license for adoption),
  - options considered (MIT, Apache 2.0, BSD, ISC, Unlicense/CC0,
    custom modified MIT) with pros/cons of each,
  - decision (MIT, with the kit-vs-user boundary documented in
    README and ADR but **not** in the LICENSE text),
  - consequences (LICENSE added, README updated, public-split
    unblocked, installer flag documented for future implementation,
    inbound=outbound contribution rule).
- Update `notes/feature-ideas.md` entry #18 status to `shipped` with
  the ADR link.

Acceptance criteria
- `LICENSE` file exists at repo root and validates as MIT (recognized
  by GitHub's license picker — visible on the repo homepage).
- `README.md` License section is rewritten — no longer says
  "Not yet specified."
- The kit-vs-user boundary is stated in plain English in **both**
  `README.md` and `ADR-025`.
- ADR-025 is `accepted` and the ADR index reflects that.
- Feature-ideas #18 marked `shipped` with ADR link.

Scope and constraints
- Primary folders to touch: repo root, `design/adr/`, `notes/`.
- Folders to avoid: `templates/`, `skills/`, `examples/`, `bin/`,
  `docs/`. (The installer's `--license` flag is documented but not
  implemented in this issue.)
- Do not modify the canonical MIT text. Do not write a "modified MIT"
  license — that defeats license-scanner recognition and creates
  legal ambiguity.
- Do not auto-scaffold `LICENSE` into example projects under
  `examples/projects/`. Those ship as part of the kit's source and
  are governed by the kit's MIT license.

Evaluation & testing requirements
- After commit, GitHub's repo homepage should display "MIT License"
  in the right-hand sidebar (visible after the next push).
- Read `README.md` end-to-end and confirm the license section is
  clear about the kit-vs-user boundary.
- Confirm `ADR-025` covers the rationale completely and references
  the rejected alternatives.
- All existing tests continue to pass (none affected).

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - existing `README.md`
   - `notes/feature-ideas.md` entry #18
   - `templates/adr-template.md` (for ADR-025 structure)
   - the canonical MIT license text (use the SPDX-listed version,
     unmodified)
2. Propose a short, step-by-step PLAN:
   - the LICENSE file content (copyright line + canonical text),
   - the README License section rewrite,
   - the ADR-025 outline (Context, Options A–F, Decision,
     Consequences),
   - the feature-ideas update.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - separate commits for: ADR draft, LICENSE + README update,
     feature-ideas update,
   - each commit references ADR-025 and #29.
5. At the end, provide an evaluation summary:
   - files changed,
   - the rendered License section in `README.md`,
   - any follow-up work for later issues (the installer
     `--license=mit` flag implementation is deferred),
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.

---

**Retrospective note (2026-04-26):** This prompt is the canonical
session brief that should have driven this work. The implementation
was performed interactively in a session that did not follow the
formal `/prepare-issue` → `/claude-issue-executor` flow. This file
is preserved as the audit trail and as an exemplar for future
licensing decisions.
