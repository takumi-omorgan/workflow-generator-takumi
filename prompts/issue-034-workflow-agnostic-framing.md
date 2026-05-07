You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development
  workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `design/adr/`.

ADR:
- File: `design/adr/adr-028-workflow-agnostic-framing.md`
- Decision: reframe the kit as workflow-agnostic — applies to any
  structured project (research, curriculum, content, design,
  technical writing, software). No skill/template renaming. Stance
  clarification only.

GitHub Issue:
- Title: Reframe the kit as workflow-agnostic; rewrite README (ADR-028)
- Number: #34
- Milestone: v3.2.0 — project-agnostic framing, remote install, license flag
- Labels: docs

Goal
Rewrite the README so its framing matches the kit's real
capabilities, and pick up several related README quality issues in
the same pass.

Why it matters
The current README tells non-software users the kit is not for them
when in fact the kit's primitives (PRD/MVP/ADRs/issues/executor/PR)
and skills are project-agnostic. Users with research projects,
curriculum design, content projects, design system docs, etc. would
benefit from the kit but currently bounce off the framing.

Requirements
- Rewrite the README's opening framing to describe the kit as
  applying to "any project that benefits from a structured
  workflow," with software as one strong use case among several.
- Add a short "What this is good for" section listing the kinds of
  projects that fit. Include both software (CLIs, libraries, web
  apps) and non-software (research papers, technical books,
  curriculum, content, design systems, internal-policy docs).
- State the kit's three assumptions explicitly: git, GitHub, Claude
  Code. Note what it does NOT assume (specific language, test
  runner, deployment system, that deliverables are code).
- Add ongoing-development coverage. The README currently centres on
  initial scaffolding — explain that ADRs and issues are created as
  decisions arise during the project's life, not only at bootstrap.
  Cover the `claude-issue-executor` flow at a high level.
- Add a "skip if already done" note to the one-time setup section.
- Update the Status section. Replace "Milestones M1–M5 shipped"
  (stale) with a non-stale version pointer or remove the
  milestone-numbered language entirely.
- Lightly update `docs/install.md` and `docs/repo-structure.md` if
  they make software-only claims.
- Mark feature-ideas: this work doesn't have a feature-idea entry,
  but if a non-software example project follows up, capture it as a
  new feature-ideas entry.

Acceptance criteria
- A non-software user reads the new README opening and recognises
  the kit as relevant.
- No skills, templates, files, or ADRs renamed.
- Status section reflects v3.2.0 (or generalised) and won't go
  stale on every release.
- One-time setup is explicitly marked as one-time and skippable
  if already done.
- ADR-028 status is `accepted` and the ADR index reflects that.

Scope and constraints
- Primary folders to touch: `README.md`, `docs/install.md`,
  `docs/repo-structure.md`, `design/adr/`, `notes/`.
- Folders to avoid: `templates/`, `skills/`, `examples/`, `bin/`.
- Do not rename anything (per ADR-028).
- Do not introduce new skills or templates as part of this issue.
- The rewrite is editorial. Do not change ADR references or
  workflow primitives.

Evaluation & testing requirements
- After the rewrite, walk through a hypothetical research-paper
  project using the kit: does the README's framing make it clear
  this is supported? does the workflow make sense applied to a
  paper rather than a CLI?
- Run `bin/sync-adr-index --check` to confirm ADR index stays in
  sync.
- All existing tests pass (none affected).

Instructions for you
1. Read the relevant docs:
   - `CLAUDE.md`
   - `design/adr/adr-028-workflow-agnostic-framing.md`
   - existing `README.md` end to end
   - `docs/install.md` and `docs/repo-structure.md`
   - `templates/adr-template.md`
2. Propose a short, step-by-step PLAN:
   - section-by-section list of README changes (replace / add / 
     leave unchanged),
   - the exact opening-paragraph reframe wording,
   - the new "What this is good for" section content,
   - the assumptions/non-assumptions list,
   - the ongoing-development section structure,
   - any docs/install.md / docs/repo-structure.md tweaks.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - logical commits per concern (README rewrite as one or two
     commits; supporting docs as separate commits),
   - each commit references ADR-028 and #34.
5. At the end, provide an evaluation summary:
   - the new README opening (quoted in full),
   - the new "What this is good for" section (quoted),
   - the new assumptions list,
   - any docs that changed,
   - exact commands to inspect the result.

Do not start editing files until I explicitly approve your plan.
