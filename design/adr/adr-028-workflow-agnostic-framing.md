# ADR-028: Reframe the kit as workflow-agnostic, not software-only

**Status:** accepted
**Date:** 2026-04-26

## Context

The kit's README and several supporting docs describe it as a tool for
"software development" — for example, `README.md`'s opening framing
talks about "software projects" as if that were the only valid use
case. This framing is narrower than the kit's actual capabilities.

The kit's workflow primitives are: define the problem (PRD), scope
the first cut (MVP), decide on architecture and approach (ADRs),
break work into issues, drive execution through disciplined Claude
Code sessions, review via PR. None of these primitives assume code.
None of them assume a programming language, a test runner, or a
deployment target. The skills operate on text artefacts — markdown
documents, structured planning files, ADR records — and orchestrate
git/GitHub state. They do not know or care what the project is
producing.

The kit does assume:

- A **git repository** (branch/commit/PR conventions).
- **GitHub** for issues, milestones, labels, PRs (per ADR-004).
- **Claude Code** as the LLM driver.

It does **not** assume:

- A specific programming language or stack.
- That deliverables are code (markdown-only repos work fine).
- A test runner or package manager.
- A deployment system or release pipeline beyond what the kit
  provides via its own `/release` skill.

This means the kit is a good fit for any structured project where
explicit decisions, planning, and incremental work matter — not only
software. Examples that fit cleanly:

- **Research projects.** PRD = research proposal. MVP = first complete
  draft. ADRs = methodological decisions. Issues = chapter sections.
  `claude-issue-executor` drives drafting per section.
- **Technical writing / books.** PRD = book proposal. MVP = first
  publishable cut. ADRs = structural decisions.
- **Curriculum design.** PRD = course outline. MVP = first deliverable
  module. ADRs = pedagogy decisions.
- **Content projects** (newsletters, podcasts, video series). Editorial
  decisions become ADRs; episode plans become issues.
- **Design system docs.** Token decisions, component scope, layout
  rules — all natural ADR candidates.
- **Internal-policy documents.** HR handbooks, security procedures,
  compliance manuals — anything where decisions need to be recorded
  and revisited.
- **Software, of course.** The kit was originally framed around
  software projects and remains a strong fit there.

The kit's vocabulary leans software — "product," "user stories,"
"capabilities," "MVP." For non-software projects, those terms still
map cleanly: a research paper has a "product" (the paper itself) and
an "audience" (its users); a curriculum has "capabilities" (what
students can do after); a book has "user stories" (reader-shaped
journeys through the material). The metaphor stretches without
breaking.

This ADR records the broader applicability so that the README, docs,
and any future framing discussions reflect the kit's real scope. The
change is a stance clarification — no kit behaviour changes.

## Options considered

### Option A: Keep the software-only framing

- Pros: matches the kit's original framing and existing
  example-projects gallery (kb-lookup CLI, slug-utils library); no
  README rewrite needed.
- Cons: actively misleads users with non-software projects who could
  benefit from the kit; understates the kit's actual capabilities;
  contradicts the workflow-primitive-level reality.

### Option B: Rebrand entirely (rename, restructure for generic use)

- Pros: signals the broader scope unmistakably.
- Cons: invalidates existing references (CHANGELOG, ADRs, links);
  breaks SEO and any links from the wider community; over-corrects
  for a framing fix that doesn't require renaming.

### Option C: Reframe in docs without renaming

- Pros: signals broader scope without breaking references; only the
  README and a few docs change; existing example projects (CLI,
  library) remain valid because software is still in scope.
- Cons: a rebrand might surface new issues (heading-level mismatch
  between filename `Design/mvp.md` and a non-software MVP concept) —
  judged minor and acceptable.

## Decision

Adopt **Option C**. Reframe the kit as workflow-agnostic in the
README and supporting docs without renaming the project, files, or
skills. Specifically:

- Rewrite `README.md`'s opening framing to describe the kit as
  applying to "any project that benefits from a structured workflow"
  (or similar wording), with software as one major use case among
  several.
- Add a short "What this is good for" section listing the kinds of
  projects that fit, including non-software examples.
- Acknowledge the kit's three actual assumptions (git, GitHub,
  Claude Code) and what it does **not** assume.
- Keep all existing skill names, template names, file paths, ADR
  references, and example projects unchanged. Existing software
  example projects (`examples/projects/kb-lookup`,
  `examples/projects/slug-utils`) remain valid and demonstrate the
  software flow; they are not exhaustive.
- Update `docs/install.md` and `docs/repo-structure.md` lightly if
  they make software-specific claims; do not overhaul.
- Optionally add one non-software example project to
  `examples/projects/` in a follow-up release; not in scope for
  this ADR's implementation.

This ADR explicitly does **not** rename:

- The `prd-to-mvp` skill (it stays — "MVP" is widely understood
  beyond software).
- The MVP template's filename `Design/mvp.md` (per ADR-024's
  filename-stays clause).
- Any skill or template by reframing.

## Consequences

- The README's framing matches the kit's real capabilities. Users
  with non-software projects no longer have to read between the
  lines.
- The kit's example projects gallery (`examples/projects/`) currently
  shows only software cases. Adding a non-software example
  (research-project or curriculum-shaped) becomes a logical
  follow-up; tracked as a new feature-ideas entry if not already
  there.
- Vocabulary in templates and skills (`product`, `user stories`,
  `capabilities`, `MVP`) stays software-leaning but maps cleanly to
  non-software projects without modification. Future revisions may
  refine if specific friction emerges.
- Kit assumptions are now explicit: git, GitHub, Claude Code. Anyone
  using a non-GitHub host, non-git VCS, or non-Claude LLM is
  out-of-scope by the kit's current ADRs (ADR-004, ADR-006), and
  ADR-028 does not change that.
- ADR-028 is a stance/framing ADR. It involves doc changes only — no
  kit behaviour, no skill behaviour, no template structure changes.
- This rewrite also covers related README quality issues raised at
  the same time: ongoing-development coverage (ADR creation as
  decisions arise during a project, not only at bootstrap), the
  one-time setup section adding a "skip if already done" note, and
  the stale "Milestones M1–M5 shipped" status line. These are
  natural by-products of the rewrite, not separate decisions.
- Per ADR-026, this change is **PATCH** in isolation (docs only).
  It ships in v3.2.0 as part of a MINOR release alongside ADR-029
  (per-project remote install) and ADR-030 (installer license flag).
