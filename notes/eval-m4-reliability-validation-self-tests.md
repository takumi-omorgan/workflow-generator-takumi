# Evaluation — Milestone M4 (Reliability, validation, and self-testing)

**Branch:** `m4-reliability-validation-self-tests`
**ADR:** ADR-050 (reliability layer)
**Roadmap:** `design/workflow-generator-roadmap-and-issues-20260605.md` §M4 — Issues 16, 17, 18, 19, 20

M4 was executed as **one reviewable PR**. The five issues form one
coherent reliability layer — the schema file is what the validator
enforces, the consistency checker guards that the file stays referenced,
and the self-test runs both validators (and the receipt logic) on a stub
as its own regression test — so splitting them would fragment a single
decision (the M2/M3 precedent: one ADR per coherent milestone).

## Plan and decisions

| Roadmap issue | Delivered as | Decision note |
|---|---|---|
| 16 — canonical carry-forward schema | `schemas/design-questions.v1.yaml` + `schemas/README.md`; §6 + 3 skills reference it | §6 stays the **human spec**; the file is its **machine-readable mirror** and the single source the validator reads. Versioned filename; a breaking change adds `.v2.yaml`. |
| 17 — `bin/validate-carry-forward` | standard-envelope validator (0/1/2) | Reads required fields / `target-issue` pattern / extra-field policy **from the schema file** — no second copy of the rules. Dependency-free block parser (no pyyaml). `--against` traces producer→PR-body/prompt. |
| 18 — idempotency receipts | `docs/receipts.md` + `schemas/receipt.v1.yaml` + `bin/write-receipt`; wired into 5 mutating skills | Receipt is a documented **JSON file** under `.claude/receipts/` the agent can write directly — works in any target with **no installer change, no dependency**. Helper is the deterministic reference writer/reader, not a hard requirement. cat-1 file-writers excluded (already idempotent) — documented boundary. |
| 19 — workflow self-test | `bin/self-test` + `docs/self-test.md` + `notes/self-test-log.md` | Automated half runs the **non-mutating** surface + a throwaway stub (which doubles as the validator/receipt regression test); manual half measures full idea→first-PR time. Release notes summarise recent results. |
| 20 — consistency checks + CI | `bin/check-consistency` + `.github/workflows/kit-checks.yml` | Doc↔metadata **umbrella** complementing `validate-kit-json` (skills.md, verb layer, bin registry, schema refs, category legend). CI runs the whole read-only surface — the wiring ADR-047 deferred to M4. |

### Why one ADR (ADR-050)

M2 set the precedent of one ADR (ADR-047) for a milestone's coherent
decision; M4 is one reliability layer whose parts reinforce each other, so
one ADR fits. ADR-050 is **additive**: it extends ADR-047 (envelope, the
deferred consistency/CI checks), ADR-040 (carry-forward schema now has a
machine mirror + validator), and ADR-035 (receipts complement the
`next-action` zone) without superseding any accepted ADR (CLAUDE.md rule).

### Backwards compatibility

No installer change and no new runtime dependency. New `bin/*` scripts are
kit-level (same posture ADR-047 took for `kit.json`). Receipts are an
agent-written file convention, so existing target-project installs gain
the convention via the skills' cross-references with nothing to migrate.
`.claude/receipts/` added to both the kit `.gitignore` and
`templates/gitignore.target`.

## Checks run

- `bin/self-test` → ok, 9/9 steps, 1s (surface + carry-forward/receipt stub self-checks green).
- `bin/validate-kit-json` → in sync (21 skills; kit.json ↔ frontmatter).
- `bin/check-consistency` → consistent (docs ↔ metadata agree).
- `bin/validate-carry-forward` → no blocks in real notes (this note has none); fixture tests: valid→exit 0, missing-field/bad-pattern/unknown-field→exit 1, `--against` missing `## Notes for #N`→exit 1.
- `bin/write-receipt` → write/find/status-filter round-trip; bad JSON / bad status → exit 2.
- `bin/check-plan --criteria-set adr` on ADR-050 → pass (C6 deferred warn only).
- `bin/sync-adr-index` → ADR-050 indexed; re-run shows no drift.
- `bin/check-state-cap --check` → ok.
- `bash -n` on all `bin/*` and `bin/lib/*` → clean.
- `python3 json.load(kit.json)` → valid.
- Relative-link check across new/edited markdown → all resolve.

## Dogfood friction (carried forward)

- **Carry-forward schema now has two homes** (§6 prose + the `.yaml`
  file). The validator reads the file and `check-consistency` requires §6
  to reference it, so drift is loud — but a *semantic* change still needs
  a human to keep the prose and file saying the same thing. Watch on the
  next schema change.
- **Receipts are written by agent instruction, not enforced.** The 5
  mutating skills cross-reference `docs/receipts.md`, but nothing fails CI
  if a skill forgets to write one (receipts are local/gitignored, so CI
  cannot see them). Acceptable for an idempotency aid; revisit if a
  duplicate-action incident shows the instruction is being skipped.
- **`check-consistency` C2 verb-layer parse is heuristic.** It flags
  backtick-quoted, dash-containing tokens in the §3 table as skill names;
  a future non-skill token of that shape could false-positive. Tighten to
  parse the "Underlying skill(s)" column explicitly if the table grows.

## Not in scope (left for later milestones)

- Shipping `write-receipt` and the validators into target projects via the
  installer (ADR-050 deferral — kept kit-level like `kit.json`).
- Extending receipts to cat-1 file-writing skills (documented boundary).
- Re-aligning the legacy `bin/check-plan` envelope (ADR-047/043 follow-up).
- Growing `validate-carry-forward` into an ADR-034 plan-checker rule.
- A first **manual** full-flow self-test run on a throwaway repo — seeded
  in `notes/self-test-log.md`, to be taken when M4/next release is prepared.
