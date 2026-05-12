# Refactoring Ideas Notepad

Lightweight capture for kit-internal refactoring — naming conventions,
file and folder organisation, supersession follow-ups, technical debt,
and other plumbing-shaped changes that aren't bugs and aren't new
capabilities.

This file is **kit-repo-only** (per `notes/README.md`) — it is not
copied into target projects and is not part of the convention the kit
teaches.

**Scope distinction:**

- `bug-fixes.md` — something is broken or wrong; the kit doesn't behave
  as documented.
- `feature-ideas.md` — a new capability the kit doesn't yet offer.
- `refactoring-ideas.md` — the kit works, but its internals are
  inconsistent, awkward, or out of step with its own conventions.

**How to use:**

- Capture the trigger, the current state, the proposed change, and the
  blast radius. The point is to make later filing as a GitHub issue
  cheap, not to design the refactor here.
- Keep entries short — a few sentences per field is plenty.
- Mark status inline: `idea` → `ready-for-issue` → `filed-#N` →
  `shipped` or `dropped`.
- Refactoring usually files as a small docs-or-convention-cleanup
  issue. Use ADR only when the refactor changes a kit convention that
  target projects depend on (e.g. a directory rename like `design/` →
  `design/`).
- When an entry is filed as a GitHub issue, move it into the **Filed**
  section below with the issue number.

---

## Entry template

```markdown
### {{Short title}}

**Status:** idea
**Captured:** {{YYYY-MM-DD}}

**Trigger:** {{What surfaced this — a session, a review, a dogfooding observation?}}

**Current state:** {{What's inconsistent or under-organised today. Cite paths.}}

**Proposed change:** {{Concrete refactor — paths affected, conventions changed.}}

**Blast radius:** {{Files touched, conventions broken, downstream impact. Order-of-magnitude estimate is fine.}}

**Open questions:** {{What needs deciding before filing as an issue. "None" is a valid answer.}}
```

---

## Unfiled

_Most recent first._

### 11. Issue-drafter skill for non-ADR refactor issues

**Status:** idea
**Captured:** 2026-05-07

**Trigger:** Filed #83 and #84 by hand from entries #2 and #9 — the HTML comment at the top of each draft (`Draft GitHub issue body for X. Source: notes/refactoring-ideas.md entry #N`) is already the de-facto template, but no skill operationalises it. Surfaced while answering the question "should I have used `/adr-writer` or `/issue-planner` for #83 and #84?" — the answer was "neither," exposing a gap between `/idea-to-prd`, `/adr-writer`, and `/issue-planner`.

**Current state:** Three adjacent skills cover related shapes — `/idea-to-prd` (rough idea → PRD draft), `/adr-writer` (decision topic → ADR), `/issue-planner` (MVP + build-out plan → batch of issues at project setup). None drafts a single GitHub issue body from a `notes/refactoring-ideas.md` entry. The gap is filled today by manual drafting following the shape of #83 / #84: source-line HTML comment, Summary, ADR section (often "None required"), Why with evidence, Scope (sometimes phased), Tasks, Acceptance criteria, Scope and constraints (plan-mode policy, batching, no new tooling), Out of scope, Notes.

**Proposed change:** Add `/issue-drafter` taking an entry number (`/issue-drafter 11`), optionally with a sizing/audit folder under `notes/`. Differs from siblings on four dimensions:

1. **Input** — reads a `notes/refactoring-ideas.md` entry plus any sized audit harness output, not MVP/ADR/build-out plan.
2. **Output** — writes `notes/issue-NN-draft.md` to disk for review; user files via `gh issue create --body "$(cat ...)"`. Does *not* file the issue itself.
3. **ADR gate** — applies the kit's actual test ("does this change a kit convention that target projects depend on?") and either bails out with "run `/adr-writer` first" or auto-writes the `## ADR` section with `None required` + reasoning.
4. **Auto-sizing + plan-mode policy** — counts touched files / hunks from any audit output, applies the standing plan-mode threshold heuristic, auto-writes `## Scope and constraints` with the right plan-mode recommendation, batching policy, and tooling-promotion stance.

**Blast radius:** New `skills/issue-drafter/` (SKILL.md + example.md, ~300 lines L2). Small touch to `docs/skills.md` and `docs/workflow-guide.md` to position it. Sibling-of `/idea-to-prd` rather than under `/prepare-issue`'s wing — `/prepare-issue` runs after the issue exists; this runs before.

**Open questions:** Volume threshold to justify building — n=2 (#83, #84) is too thin; revisit after ~5+ refactor issues filed. Should the skill also draft from `bug-fixes.md` and `feature-ideas.md` entries (similar shape, different ADR-gate defaults), or is single-source scope cleaner? If multi-source, does the entry-number argument need a source qualifier (`/issue-drafter refactoring 11` vs `/issue-drafter 11`)? Does the skill need its own check-plan criteria, or does the existing issue-shape audit cover it?

---

### 1. Archive shipped prompts to `archive/issues/`

**Status:** idea
**Captured:** 2026-05-06

**Trigger:** Doc cleanup session realised every shipped issue's prompt still sits in `prompts/` alongside in-flight prompts, and each one references `generic-project-workflow.md` (now archived) — so the in-prompt links are stale.

**Current state:** `prompts/` mixes ~25 shipped prompts (issue-026 through issue-072) with any in-flight ones. The pattern in `archive/phase-1/` already exists for very-early prompts but hasn't been continued.

**Proposed change:** Move shipped prompts to `archive/issues/phase-2/` (mirror the phase-1 pattern). Reserve `prompts/` for in-flight only. Leave the stale `generic-project-workflow.md` references inside the moved files alone — they're historical, like phase-1.

**Blast radius:** ~25 file moves; one new directory; cosmetic — no skill consumes shipped prompts. Cleaner working tray.

**Open questions:** Flat `phase-2/` or further structured by milestone?

---

### 3. Auto-detect new-skill drift / ship `link-skills` inside the kit

**Status:** idea
**Captured:** 2026-05-06

**Trigger:** Hit a foot-gun in a recent session — 8 of 19 skills weren't linked into `.claude/skills/` because `~/dotfiles/claude-config/bin/link-skills` hadn't been re-run after `pause`, `resume`, `audit-milestone`, etc. were added.

**Current state:** `link-skills` lives in dotfiles, not the kit. CLAUDE.md mentions the dotfiles location but doesn't enforce running it. No drift detection between `skills/*/` (source) and `.claude/skills/*` (links). New skills sit unused until someone notices.

**Proposed change:** Ship a `bin/link-skills` inside the kit (in addition to or replacing the dotfiles one). Add a CI guard or pre-commit hook that diffs `skills/*/` against `.claude/skills/*` and warns on drift. Optionally have the installer auto-run `link-skills` so target projects never hit it.

**Blast radius:** New `bin/` script (small); CI workflow change (small); CLAUDE.md update. Removes a recurring foot-gun.

**Open questions:** Why is `link-skills` in dotfiles in the first place — intentional dogfooding philosophy, or just where it ended up? If shipped in the kit, should it overwrite an existing `.claude/skills/` or only add new symlinks?

---

### 4. Refresh `CLAUDE.md` (drop dated stub framing)

**Status:** idea
**Captured:** 2026-05-06

**Trigger:** While editing CLAUDE.md to reflect doc-cleanup work, noticed it still describes itself as "a stub added in Issue #1" and refers to "later issues" deferrals — anachronistic now that the kit has shipped 70+ issues.

**Current state:** CLAUDE.md still contains "## What this file is NOT" explaining it's a stub awaiting a fuller version. Lines like "This file is a stub added in Issue #1 so Claude Code has a minimal rules baseline ... A fuller `CLAUDE.md` ... will be written alongside the template work in later issues" no longer reflect reality.

**Proposed change:** Surgical removal of dated sections — the "stub" framing, the "What this file is NOT" footer, "later issues" deferrals. Keep load-bearing rules (plan-first per ADR-006, ADR-numbered commit messages, link-skills setup). Optionally rewrite from scratch using `templates/claude-md-template.md` as a starting point.

**Blast radius:** One file (CLAUDE.md). Cosmetic / framing only — rules unchanged.

**Open questions:** Keep the freshly-refreshed "Guiding documents" section, or move that index to a separate doc? How much should CLAUDE.md duplicate vs reference workflow-guide.md and skills.md?

---

### 5. End-to-end skill-chain regression tests on a fixture project

**Status:** idea
**Captured:** 2026-05-06

**Trigger:** No automated test catches drift between skills when one skill's output shape changes; relies entirely on PR review. Surfaced while thinking about post-MVP hardening.

**Current state:** Kit dogfoods itself but no CI exercises the chain `prd-to-mvp` → `adr-writer` → `issue-planner` → `prepare-issue` → `claude-issue-executor` → `pr-review-packager` against a fixture input. `examples/projects/` (kb-lookup, slug-utils, phased-podcast-pipeline) are static samples, not regression fixtures.

**Proposed change:** Build a fixture-based smoke test that runs the chain on a small canned input, snapshots produced artefacts, and diffs against committed expected output. Lives in `bin/` or `test/` with CI integration. Could also exercise `/check-plan` validation paths.

**Blast radius:** New harness directory; CI workflow change; ongoing fixture maintenance. Significant build cost; significant ongoing benefit.

**Open questions:** How to test skills that require user interaction (plan approval, blockers question) — mock or skip in test mode? How much variance between LLM runs is acceptable?

---

### 6. Examples freshness — refresh on major-release boundaries

**Status:** idea
**Captured:** 2026-05-06

**Trigger:** After 19 skills and 40+ ADRs of evolution, `examples/projects/` may reference outdated conventions / missing skills / stale paths. They're a primary onboarding surface — drift here misleads new users.

**Current state:** Three example projects (`examples/projects/kb-lookup`, `slug-utils`, `phased-podcast-pipeline`). No scheduled audit. Refreshes happen only when someone notices a discrepancy.

**Proposed change:** Refresh on **major-release boundaries only** (v3 → v4, v4 → v5). At each major bump, audit each example for: skill names still valid, file paths still match the repo structure, output samples reflect current template formats, ADR references point at correct ADR numbers. Document the audit cadence in `CLAUDE.md`. Optionally automate the structural checks (skill names, paths) so the manual audit covers content only.

**Blast radius:** Periodic small effort tied to release cadence. Three example projects audited per major. Optional new CI check for structural drift.

**Open questions:** Major-release-only, or also when underlying conventions change mid-release? Should examples be excluded from entry #5's regression tests, or *be* the fixture set?

---

### 10. Kit-wide token-economy framework — measure, budget, audit

**Status:** idea
**Captured:** 2026-05-06

**Trigger:** Entry #9 noted that SKILL.md token cost is paid every session — but that's only one of several token-paying surfaces in the kit. Without a kit-wide view, optimisation in one place is undone by drift in another. No instrumentation, no budgets, no audit cadence currently exist; trimming happens reactively when context feels heavy.

**Current state:** Three token-paying surfaces are largely untracked:

1. **Eager-load** — `CLAUDE.md` + all 19 SKILL.md descriptions + memory files. Paid every session regardless of what's invoked.
2. **On-demand** — when a skill runs, its full `SKILL.md` body, sibling `example.md` / `criteria.md`, and any templates it reads. Paid per invocation.
3. **Inter-skill artefacts** — prompts, `design/state.md`, `design/decisions.md`, ADR bodies. Paid by downstream skills that read them. ADR-038's content-boundary rule already addresses prompt-artefact bloat; nothing analogous exists for `state.md`, `decisions.md`, or templates.

**Proposed change:** Three-step framework, not a one-shot edit:

1. **Measure** — script under `bin/` that walks the kit and reports per-file token counts, total eager-load cost, per-skill on-demand cost, and growth between releases. Run on demand or wired into CI.
2. **Budget** — target ranges per surface (e.g. `SKILL.md` < 4k tokens, `CLAUDE.md` < 2k, memory entries < 500 each, generated artefacts referenced not restated per ADR-038). Document in a new `docs/token-budgets.md` or fold into the `skills/STYLE.md` from entry #9.
3. **Audit** — release-boundary cadence (or major-bump cadence per entry #6 examples-freshness) — re-run measurement, flag surfaces over budget, file refactor issues for hot spots.

**Blast radius:** New `bin/` script (small); one new docs page (small); ongoing audit step at release boundaries. Does not change any current files until the first audit fires. Subsumes entries #2 and #9 once budgets exist — the audit becomes the trigger mechanism for SKILL.md-style cleanups.

**Open questions:** How to measure tokens accurately — `tiktoken`, an Anthropic-specific counter, or rough character-count proxy? Hard limits (CI fails) or soft warnings? Overlap with entry #5 (end-to-end skill-chain regression tests) — same fixture project for both, or independent? What measurement granularity matters most: per-file, per-skill-chain, or per-session baseline?

---

## Filed

_Move entries here when filed as GitHub issues. Includes issue # for
cross-reference._

### 8. Finish the legacy `notes/issue-prompt.md` removal across the kit

**Status:** filed-#89
**Captured:** 2026-05-06
**Filed:** #89 (2026-05-12)

**Trigger:** Surfaced 2026-05-06 while cleaning up `notes/`. The legacy manual-fill template `notes/issue-prompt.md` and worked example were deleted in a partial cleanup, but four still-current docs were left referencing them — broken links until this is finished.

**Current state at filing:** Four docs reference the deleted files: `docs/issue-prompt-guide.md` (whole guide built around `notes/issue-prompt.md`), `docs/README.md:26`, `docs/claude-code-guide.md:147,291`, `docs/workflow-guide.md:1134`. Plus a now-superseded `bug-fixes.md` entry whose proposed plan ("promote to `templates/`") is wrong because `prompts/_template.md` (111 lines, ADR-008/031/032/033/035-aware) is the actual successor.

**Proposed change:** Update or delete the four docs. Make a deliberate call on `docs/issue-prompt-guide.md`'s fate — rewrite against `prompts/_template.md`, delete entirely, or collapse manual-fill guidance into the existing "How to use this file" block at the top of `prompts/_template.md`.

**Blast radius:** 4 docs to update + 1 bug-fixes entry to mark resolved. No skills or templates touched. Doing nothing leaves four broken links indefinitely.

**Path chosen:** Path C — collapse manual-fill guidance into `prompts/_template.md`'s header, delete the standalone guide. Considered: Path A (rewrite the guide; keeps two surfaces and risks future drift) and Path B (delete with no replacement; would retire manual-fill and warrant an ADR).

**Resolution of open questions:**

- *Is the manual-fill flow still a supported path, or has `/prepare-issue` made it vestigial?* Still supported, but relocated. The placeholder mapping table moves into `prompts/_template.md`'s existing `<!-- How to use this file -->` header block so the template self-documents; the standalone `docs/issue-prompt-guide.md` is deleted.
- *Does this need a tiny workflow-doc ADR, or is it a docs-cleanup issue?* Docs-cleanup only. The manual-fill flow is being relocated, not retired — no kit convention that target projects depend on changes shape. Path B (retiring manual-fill entirely) was considered and rejected for that reason.

---

### 9. Audit all SKILL.md files for structural consistency and token economy

**Status:** shipped-#86, #87, #88 (Phase 1, 2, 3 of issue #84)
**Captured:** 2026-05-06
**Filed:** #84 (2026-05-07)
**Shipped (Phase 1):** #86 (2026-05-07)
**Shipped (Phase 2):** #87 (2026-05-08)
**Shipped (Phase 3):** #88 (2026-05-08, closes #84)

**Trigger:** Skills are loaded into context every session — their length and structure directly affect token usage on every invocation. Without periodic audit, drift accumulates: some skills bloat with examples, others diverge in section structure, and noise (stale ADR attributions, restated conventions) reaccumulates.

**Current state:** 19 SKILL.md files. No formal style guide for skill structure. Length and structure vary skill-to-skill — some are concise, others have grown over multiple iterations. Token cost is paid every session because skills are loaded eagerly. Entry #2 of this file (prune type-3 ADR attributions) addresses one specific noise bucket; this entry is the broader audit.

**Proposed change:** Define a canonical SKILL.md structure (header order, what belongs in `SKILL.md` vs sibling `example.md` / `examples.md` / `criteria.md`, target length range), then audit each of the 19 skills against it. Trim sections that duplicate guidance from `CLAUDE.md` or `docs/workflow-guide.md`. Move long worked examples and edge-case walkthroughs out of `SKILL.md` into sibling files so the loaded surface stays lean. Optionally add a `skills/STYLE.md` style guide and a CI check for length / required sections.

**Blast radius:** 19 SKILL.md files; voice/structure-only — no behaviour change. Pairs with entry #2 (which it could naturally absorb when filed). May produce a `skills/STYLE.md` and a small CI guard.

**Pre-work (2026-05-07):** Initial audit run against the canonical Anthropic Skills guidance — see [`skills-audit-2026-05-07/findings-v2.md`](skills-audit-2026-05-07/findings-v2.md). Reusable deterministic script (`audit.py`), source-checked findings, re-scored per-skill judgment CSV, and an independent gpt-5.5 verification pass. Six prioritised findings; one outright budget violation (`claude-issue-executor`, 586 lines / ~6.7k tokens).

**Resolution of open questions:**

- *Target length per SKILL.md?* ≤500 lines / <5k tokens (Anthropic best-practices, verbatim).
- *Canonical section order applied uniformly?* Deferred per Finding #6 — cohort outline shape is "loosely consistent" but not drifted enough to justify a hard template at 19 skills. Revisit if cohort grows.
- *Style enforced by docs or linter / CI check?* Docs only for now. The audit harness (`audit.py`) is reusable but lives under `notes/` until evidence accumulates that the rules are violated by new skills.
- *Need an ADR?* No — internal kit style only; doesn't change a target-project-facing convention.
- *Merge entry #2 into entry #9 when filed?* No — kept separate. Entry #2 (#83) is a quick-win precursor focused on noise removal; this entry covers the broader cohort cleanup (descriptions, body slimming, sidecar consistency).

**Sibling issue:** #83 — Prune parenthetical ADR attributions from SKILL.md bodies (entry #2).

---

### 2. Prune type-3 ADR attributions across SKILL.md files

**Status:** shipped-#85
**Captured:** 2026-05-06
**Filed:** #83 (2026-05-07)
**Shipped:** #85 (2026-05-07)

**Trigger:** Recent `docs/workflow-guide.md` refactor removed ~22 "(per ADR-XXX)" parenthetical attributions and the resulting voice was markedly cleaner. The same noise pattern is present across the 19 SKILL.md files.

**Current state:** SKILL.md files include attribution-style ADR refs ("(ADR-014)", "implements ADR-035", "per ADR-038") that serve internal traceability but obscure the user-facing description. Type-1 canonical anchors and type-2 load-bearing schema cross-refs (ADR-040 carry-forward, ADR-041 permission contract) should stay.

**Proposed change:** Apply the same three-bucket audit per SKILL.md — keep type-1 / type-2, prune type-3. Estimate ~2-4 prunable per skill, ~50-80 edits total. Optionally add a one-line style-guide entry to `CLAUDE.md` so the noise doesn't reaccumulate.

**Blast radius:** 19 SKILL.md files; no behaviour change; voice/clarity-only.

**Pre-work (2026-05-07):** Detection script (`adr-audit.py`) run — see [`skills-audit-2026-05-07/adr-attributions.md`](skills-audit-2026-05-07/adr-attributions.md) for the full per-match listing. **71 high-confidence + 5 medium-confidence type-3 candidates** across 17 of 19 skills (`milestone-summary` and `resume` already clean). Confirms the original 50–80 estimate. Top by count: `claude-issue-executor` (21), `prepare-issue` (12), `adr-writer` (8), `check-plan` (5), `issue-planner` (5), `release` (5). Top by density per 100 lines: `adr-writer` (3.92), `claude-issue-executor` (3.58), `prepare-issue` (2.96). Dominant pattern: parenthetical `(per ADR-NNN)` (≈55% of matches).

**Resolution of open questions:**

- *Borderline cases like "per ADR-006" — drill-down or attribution?* Default prune; reformat to a markdown link in body text when the reader genuinely needs the ADR to do the task.
- *One-shot batch PR, per-skill PRs, or lazy-as-touched?* One-shot batch PR — voice-only, 17-file blast radius, partial state would drift back. The per-match listing in `adr-attributions.md` is the work plan.

**Sibling issue:** #84 — Apply 2026-05-07 skills-audit recommendations across the cohort (entry #9).

---

### 7. Rename `Design/` → `design/` for case consistency with other root directories

**Status:** shipped-#82
**Captured:** 2026-05-06
**Filed:** #80 (clarify pass + ADR-044 + ADR-045)
**Shipped:** #82 (2026-05-07, merged into v4.0.0)

**Trigger:** While reviewing root-directory casing — `Design/` was the only TitleCase top-level directory in a repo where everything else was lowercase.

**Current state at filing:** Root had `docs/`, `notes/`, `skills/`, `templates/`, `bin/`, `prompts/`, `examples/`, `archive/`, and `Design/`. The capitalised root *files* (`README.md`, `LICENSE`, `CHANGELOG.md`, `CLAUDE.md`) follow well-known external conventions — `Design/` had no analogous anchor; it was a project-internal choice that diverged from its peers.

**Proposed change:** Rename `Design/` → `design/` across the kit and the convention it teaches target projects. Touched `CLAUDE.md`, `README.md`, `CHANGELOG.md`, `docs/`, `templates/`, `skills/*/SKILL.md`, `bin/lib/check-plan-eval.sh`, `examples/projects/*/`, and the kit's own ADR bodies. Required a new ADR (ADR-044) authorising mechanical path-string rewrite inside accepted ADRs (otherwise blocked by the kit's "never edit accepted ADRs in place" rule).

**Blast radius (actual):** 1,186 occurrences across 179 files. Breaking change for every existing target-project install. Migration snippet (two-step `git mv` for case-insensitive FS + bulk `sed`) shipped in CHANGELOG v4.0.0 entry.

**Resolution of open questions:**

- *Which existing ADR established `Design/` and would need to be superseded?* ADR-005 — superseded by ADR-045 on the directory-casing question only.
- *Does mechanical path-string rewrite count as "editing in place" under the immutability rule?* No, per ADR-044 (drafted in #80, accepted in #81). ADR-044's six criteria carve a narrow exception: deterministic substitution, no sentence meaning changes, no altered decisions or rationale, no added/removed requirements, uniform application, scriptable and reproducible.
- *Migration helper or manual `git mv` step?* Manual snippet in CHANGELOG, no new tooling.
- *Is consistency worth the breaking change?* Yes — settled at the clarify gate.
- *Alternative names (`decisions/`, `planning/`)?* Rejected — would force splitting `state.md` and `ai-summary.md` out into a new home, doubling the blast radius.

**Lessons learned:** (1) macOS APFS case-insensitive default required a two-step rename via `_design_tmp` intermediate — caught at planning, not pre-merge. (2) Bulk `sed` corrupted three files (ADR-044, ADR-045, this entry) where the prose literally describes the rename — required editorial restoration. Future kit-wide renames should pre-flag any file whose body describes the rename itself for editorial-only handling.
