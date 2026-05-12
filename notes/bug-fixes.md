# Bug Fixes Notepad

Lightweight triage holding pen for bugs identified during dev / eval / dogfooding.
Entries graduate to GitHub issues (or directly to PRs for trivial fixes).

**How to use:**

- Capture as you find them. Triage weekly or per-release-prep.
- For urgent + well-scoped bugs, skip this file — `gh issue create` directly. This file is a triage tool, not a mandatory step.
- GitHub issues are canonical. This file is short-half-life: capture → triage → file → mark filed → eventually delete.
- Mark severity inline: `low` (cosmetic / typo / single-line fix), `medium` (parser gap / contract mismatch), `high` (cluster of related findings or kit-wide impact).
- Mark status inline: `unfiled` → `filed-#N` → `fixed`. Use `dropped` for entries de-escalated after re-evaluation (e.g. found to be a feature, not a bug; or found to be fixture-internal, not a kit issue).
- Optional `Cluster:` field for grouping bugs that should land as a single issue (e.g. installer-cluster bugs → one consolidated installer fix).
- Optional `Related:` field cross-references entries in `feature-ideas.md` (when a bug is against a shipped feature whose original ideation block is recorded there).

---

## Entry template

```markdown
### {{Short title}}

**Status:** unfiled
**Severity:** low | medium | high
**Captured:** {{YYYY-MM-DD}}
**Source:** {{eval (fixture-name) | dogfooding | user-report | …}}
**Cluster:** {{optional grouping label}}
**Related:** {{optional cross-ref to feature-ideas.md entry, e.g. "#3 (Installer script)"}}

**Symptom:** {{What goes wrong, in one sentence.}}

**Repro:** {{One-line repro path, or pointer to where it surfaced.}}

**Proposed fix:** {{One-line direction. If unclear, leave as "TBD".}}
```

---

## Active

Ordered by severity (high → low) then capture date.

### `notes/` folder cleanup — promote templates out, refresh references

**Status:** resolved-#89 — placeholder-mapping salvage collapsed into `prompts/_template.md` header; standalone `docs/issue-prompt-guide.md` deleted (2026-05-12)
**Severity:** low
**Captured:** 2026-05-06
**Source:** dogfooding

**Symptom:** Two follow-up steps deferred from the phase-1 archive of `notes/` (the issue/prompt/setup artefacts were moved to `notes/archive/phase-1/`):

1. Promote `notes/issue-prompt.md` → `templates/issue-prompt.md` and `notes/issue-prompt-sample.md` → `examples/issue-prompt-sample.md`. They are reusable artefacts, not scratch.
2. Update the ~10 files referencing the old `notes/` paths: `docs/issue-prompt-guide.md`, `docs/claude-code-guide.md`, `generic-project-workflow.md`, `examples/{idea-only,standard-prd,custom-prd}-example.md`, and skill fallback paths in `claude-issue-executor` / `issue-planner`. Skip `templates/claude-md-template.md` (refers to target-project `notes/`, not kit-internal).

**Repro:** `grep -rln "notes/issue-prompt" --include="*.md"` from repo root.

**Proposed fix (now superseded):** Do (1) and (2) in one PR. Deferred — user is mid-flight on the referencing files.

**Why superseded (2026-05-06):** Step (1) is no longer the right move. Comparing the legacy `notes/issue-prompt.md` (78 lines) against the current `prompts/_template.md` (111 lines) showed the legacy file is a stale earlier evolution — pre-ADR-008, unaware of ADR-031/032/033/035 and the content-boundary rules. The two legacy files have been deleted rather than promoted; the docs-update work in step (2) carries forward via the feature-ideas entry above.

---

## Filed

_Move entries here when filed as gh issues. Includes issue # for cross-reference._

---

### Installer cluster — missing files in `bootstrap-workflow-kit`

**Status:** filed-#60
**Severity:** high
**Captured:** 2026-05-06
**Source:** eval (md-notes + podcast-pipeline + research-tracker — all three fixtures)
**Cluster:** installer
**Related:** #3 (Installer script, ADR-009)

**Symptom:** `bootstrap-workflow-kit` ships without several files that downstream skills expect to find. Eight separate findings across the v3.3.0 baseline trace to this single root cause:

- `templates/mvp-template.md`, `templates/build-out-plan-template.md` — expected by `/prd-to-mvp`
- `templates/adr-template.md` — expected by `/adr-writer`
- `templates/pr-template.md` — expected by `/pr-review-packager`
- `templates/state-template.md` — expected by `/pause` / `/resume`
- `templates/milestone-summary-template.md` — expected by `/milestone-summary`
- `templates/readme-template.md`, `templates/ai-summary-template.md` — expected by `/workflow-docs`
- `.github/pull_request_template.md` — referenced by `CLAUDE.md` template
- `.gitignore` — minimal default missing
- `design/adr/README.md` — required (with marker fences) by `bin/sync-adr-index`; first run errors with *"sync-adr-index: no design/adr/README.md found"*

Skills currently graceful-degrade by hand-rendering to canonical shapes, but the install-side fix removes the friction entirely.

**Repro:** Run `bootstrap-workflow-kit --project-name=foo --license=mit --license-holder="…" --with-docs` on an empty repo. Then invoke `/prd-to-mvp` (or any skill in the dependent set above) and observe the missing-template warning + hand-render fallback.

**Proposed fix:** Drop the missing files from the bootstrap installer. One PR closes 8 findings (F3, F5, F7, F8, F21, plus the meta-friction across `/prd-to-mvp`, `/adr-writer`, `/pr-review-packager`, `/workflow-docs`). **Highest-leverage v3.4 fix.** See `runs/kit-v3.3.0/baseline-verdict.md` § "Active findings worth fixing before v3.4" #2.

---

### `/changelog` parser gaps (F27, F29)

**Status:** filed-#61
**Severity:** medium
**Captured:** 2026-05-06
**Source:** eval (md-notes; F29 likely resolved on podcast-pipeline via label-based categorization — verify on next fixture or close out)
**Related:** #10 (Auto-generated changelog skill)

**Symptom:** Two parser gaps:

- **F27 — dedup gap.** When the same ADR is referenced in multiple commit messages within a release range, `/changelog` includes duplicate entries instead of deduplicating.
- **F29 — squash-merge → "Other" hierarchy inversion.** Squash-merged PRs whose commit subjects follow the kit's own-prescribed format (e.g. `feat(scope): subject (#N) (#M)`) land in the changelog's "Other" group instead of being categorized by the conventional-commit verb. Likely fixed on podcast-pipeline via label-based categorization — needs verification.

**Repro:** Run `/release` on a milestone where (a) one ADR is referenced from multiple commits, (b) PRs were squash-merged with the kit's `(#N) (#M)` suffix format. Inspect the generated CHANGELOG entries.

**Proposed fix:** F27 — dedup pass on ADR references before grouping. F29 — verify the label-based categorization fix from podcast-pipeline holds; if so, close. If not, align the parser's verb-extraction regex with the kit's squash-merge subject format.

---

### F34 — `**Exit criterion:**` (singular) vs `**Exit criteria:**` (plural) field-name mismatch

**Status:** filed-#62
**Severity:** low
**Captured:** 2026-05-06
**Source:** eval (podcast-pipeline + research-tracker — reproduced ×2 multi-phase fixtures, deterministic)
**Related:** #28 (Milestone lifecycle, ADR-037)

**Symptom:** Producer-consumer field-name drift between two skills' expectations of the same field:

- `/prd-to-mvp`'s build-out-plan template emits `**Exit criterion:**` (singular) on each phase block.
- `/audit-milestone`'s parser regex looks for `**Exit criteria:**` (plural).

`/audit-milestone` currently tolerates the drift (matches semantically and flags), but a future regex tightening would break the contract.

**Repro:** `grep -h "Exit crit" design/build-out-plan.md` on any kit project with a multi-phase plan.

**Proposed fix:** Align the producer (use plural in `/prd-to-mvp`'s build-out-plan template) OR the consumer (regex matches both forms in `/audit-milestone`). Two-character fix on either side. Producer-side is cleaner — singular is grammatically odd anyway when the field can hold a list.

---

### F-NEW — `infra` label vs conventional-commit verb mismatch

**Status:** filed-#63
**Severity:** low
**Captured:** 2026-05-06
**Source:** eval (research-tracker)
**Related:** #1 (CLAUDE.md template), #9 (`/pr-review-packager` skill)

**Symptom:** Cross-cluster kit-internal spec inconsistency:

- The kit's `CLAUDE.md` template's "GitHub conventions" section lists labels: `feature, bug, design, infra, security, docs`.
- `/pr-review-packager`'s commit-verb classifier recognizes only conventional-commit verbs: `feat, fix, docs, refactor, chore, test, perf, ci, build, style`.
- `infra` is in the label set but not in the verb classifier. Commits with `infra(scope):` prefix (which the kit's own canonical-shape encourages for infra-labeled issues) fall into the change-summary's "Other" group rather than being categorized.

md-notes / podcast-pipeline didn't surface this because their issues all used commit-conventional verbs. Research-tracker's issue #3 (smoke-test infra) used `infra(papers):` and surfaced the gap.

**Repro:** Open a PR with commit subject `infra(scope): add smoke-test example`. Run `/pr-review-packager`. Observe the change lands in "Other", and skill explicitly flags the verb mismatch in its audit-trail notes.

**Proposed fix:** Pick one — either (a) add `infra` to `/pr-review-packager`'s recognized verb list (simpler; `infra` becomes a kit-conventional verb), or (b) drop `infra` from the kit's CLAUDE.md spec label set and remap kit-shape `infra` issues to `chore` or `refactor` (cleaner conventional-commit alignment, but breaks downstream cross-fixture consistency since md-notes + podcast-pipeline + research-tracker all used `infra` labels). Recommend (a) — fewer breaking changes; codifies an existing pattern.

---

## Dropped

_Entries de-escalated after re-evaluation (found to be a feature, not a bug; or fixture-internal, not a kit issue; or already addressed)._

---

### ADR-001 grep-pattern bug in research-tracker fixture

**Status:** dropped
**Severity:** n/a
**Captured:** 2026-05-06
**Source:** eval (research-tracker)

**Reason for drop:** This is a **fixture-internal bug**, not a kit bug. The research-tracker fixture's ADR-001 prescribed a `#`-prefixed grep pattern for tag queries, but the paper-entry template (also from the research-tracker fixture) stored tags as YAML bare strings — the two don't agree. Filed as the fixture's own GitHub issue #15 (M2). The kit's `/adr-writer` and `/issue-planner` skills are not at fault; this was a content-level inconsistency the fixture's smoke-test issue surfaced (and the surfacing itself is a kit-positive signal, not a kit defect).
