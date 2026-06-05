# Evaluation — Milestone M3 (Unified workflow control and feature expansion)

**Branch:** `m3-unified-workflow-control`
**ADRs:** ADR-048 (unified workflow control), ADR-049 (follow-up PRD workflow)
**Roadmap:** `design/workflow-generator-roadmap-and-issues-20260605.md` §M3 — Issues 11, 12, 13, 14, 15, 21

M3 was executed as **one reviewable PR** (the roadmap allotted 4–6).
The six issues form one coherent operating model, so splitting them
would reproduce the very fragmentation the milestone exists to remove.

## Plan and decisions

| Roadmap issue | Delivered as | Decision note |
|---|---|---|
| 11 — one canonical approval gate | `docs/workflow-control.md` §2 | One sequence (classify → require? → plan → token → proceed) with a **closed-set, case-insensitive approval token** (`approve/approved/yes/go/proceed/lgtm`). Skills cross-reference it; the executor's 8-step gate is the reference instance. |
| 12 — `/start` or `/next` meta-skill | `skills/start/` | One cat-1 router skill answering to both names; reads the `next-action` zone first, then artefacts; asks **one** question when ambiguous. |
| 13 — compress 19 skills into a verb layer | `docs/workflow-control.md` §3 + top of `docs/skills.md` | **Documentation aliases, not nine new skill files** — only `/start` and `/feature-prd` are new commands. Keeps the kit lightweight (CLAUDE.md "no speculative abstractions"); agents keep exact names in `kit.json`. |
| 14 — structured `next-action` zone | sixth `state.md` zone + writers/readers | Marker-fenced YAML (`skill`/`args`/`preconditions`/`blocked-by`). **Optional and back-compatible**: older `state.md` files are not malformed for lacking it. |
| 15 — three operating modes | `docs/workflow-control.md` §1 | `interactive`/`assisted`/`autonomous` as a **named session-level layer over** ADR-041's cat-1/2/3 — a mode × category matrix, not a replacement. No mode ever relaxes cat-3. |
| 21 — follow-up PRD workflow | ADR-049 + `skills/feature-prd/` + `templates/prd-addendum-template.md` | Additive `design/prd-addenda/NNN-*.md`; original PRD never overwritten; `/feature` verb. |

### Why two ADRs (not five, not one per issue)

M2 set the precedent of one ADR (ADR-047) for a milestone's coherent
decision. M3 splits cleanly along its own title: **ADR-048 = unified
workflow control** (Issues 11–15, which cannot be decided independently
without contradiction — a mode sets how the gate behaves, the router
reads the next-action zone, the verb layer fronts the same skills), and
**ADR-049 = feature expansion** (Issue 21, a separable product-workflow
decision). Both are additive: they *extend* ADR-006/035/039/041 (gate,
state, modes) and ADR-003 (intake) without superseding them — no
accepted ADR was edited in place (CLAUDE.md rule).

## Checks run

- `bin/validate-kit-json` → in sync (21 skills; kit.json ↔ frontmatter).
- `bin/sync-adr-index` → ADR-048/049 indexed; re-run shows no drift.
- `bin/check-plan --criteria-set adr` on both new ADRs → `pass`.
- `bin/check-state-cap` → exit 0 (live `design/state.md` 68 lines).
- `bash -n` on all `bin/*` and `bin/lib/*` → clean.
- `python3 json.load(kit.json)` → valid.
- Relative-link check across the 14 new/edited markdown files → all resolve.

## Dogfood friction (carried forward)

- **No machine enforcement of the new contracts.** The mode × category
  matrix and the approval-token set are protected by PR review only,
  joining the existing §6/§7 drift checks deferred to the M4
  plan-checker (issue #72). Expected, but worth re-checking after M4.
- **`next-action` written by five skills.** Each writer got a small,
  zone-scoped instruction rather than a shared helper; if a sixth writer
  appears, factor the zone-write rule into one place. Candidate M4
  consistency-check target alongside `kit.json`.
- **Verb layer lives only in docs.** If users start typing `/decide`,
  `/work`, etc. expecting real commands, revisit ADR-048 Option D
  (per-verb skills). Watch for this in the next dogfood pass.

## Not in scope (left for later milestones)

- Machine-readable session-mode state beyond `/start` stating it and a
  `CLAUDE.md` default line (ADR-048 deferral).
- Per-verb slash commands beyond `/start`/`/feature-prd` (ADR-048
  Option D, deferred).
- AI PR review (M5) — to be introduced as the first real `/feature-prd`
  addendum per the roadmap dogfood note on Issue 21.
