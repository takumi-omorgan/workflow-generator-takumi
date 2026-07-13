# Open Questions

Unresolved questions awaiting an answer, a decision, or external input.
Resolve a question by recording the decision (here or in an ADR) and
linking it, then moving the entry to "Resolved".

## Open

### Q3 — Should the workflow layer grow a Hermes-side Kanban view?

Raised (2026-07-13) as a **future workflow-layer consideration only**: a
Hermes-side Kanban/board view over in-flight issues and PRs, to make
supervision state visible at a glance.

**Direction settled (2026-07-13); build decision still deferred.**
If a Hermes Kanban is built, it stays **external / orchestrator-only**. Nothing
is implemented, and it remains a dependency of no current or planned work.

The agreed shape, should it be built:

- **GitHub stays canonical** for issues, PRs, and milestones. The kit ships no
  board, queue, or database runtime, and this answer does not add one.
- **Hermes Kanban mirrors GitHub** — it is a read/dispatch view over the
  canonical source, never a second source of truth.
- **Dispatch inputs come from the fence-parseable zones in
  [`design/state.md`](../design/state.md)** — `state:in-flight` and
  `state:next-action` — which already exist and are machine-readable.
- **Backlog import** from ADR/backlog entries, if wanted, is **Hermes-side
  only**.
- **No Hermes-specific board internals leak into the public kit** unless that
  is explicitly scoped in a later ADR.

Left open: whether to build it at all, and its design/acceptance criteria.
What is now settled is only *where it may live* — outside the kit.

Note this is distinct from [ADR-012](../design/adr/adr-012-github-projects-integration.md)
(accepted), which covers GitHub Projects boards *inside a target project* as a
kit feature. Q3 is about the **supervision layer around the kit**, not the kit's
shipped surface. Do not conflate the two, and do not treat Q3 as a reason to
revisit ADR-012.

## Resolved

### Q1 — What specifically needs tightening in the public release protocol?

**Resolved (2026-07-13): exactly one thing — post-publish verification.**
The weaknesses were finally enumerated by *auditing the live public repo*
rather than by speculation, and most of the feared ones do not exist.

At the published HEAD (`1c0eba3`), the tree is exactly the 258 files
`bin/export-public` produces: no leaked `design/adr/`, `notes/`, `archive/`,
or `.hermes/`; `prompts/` reduced to `_template.md`; the `CLAUDE.md`
contributor section stripped; and the install-surface identity strings
(`README.md`, `docs/install.md`, `bin/bootstrap-workflow-kit`) all naming the
repo they ship in. The leak/identity/stale-version fears this question was
opened for are **being correctly handled** by the ADR-056 export contract.

The one real weakness is the seam this question already suspected — *"the
protocol for keeping that identity consistent across exports, not a concrete
outstanding defect."* `bin/export-public` never pushes (ADR-056 Decision 1),
so publishing is a manual human step, and nothing verifies afterwards that the
live remote matches the artifact the export verified. That gap is now governed
by
[ADR-057](../design/adr/adr-057-public-export-integrity-gate.md) (accepted),
which decides `bin/verify-published` as a post-publish gate.

Mitigation is **decided, not yet built** — see [risks.md](risks.md) (R1), which
stays open until the script ships. Review receipt, including the falsified
premises that nearly sent this the wrong way:
[reviews/2026-07-13-adr-057-review.md](reviews/2026-07-13-adr-057-review.md).

### Q2 — How does the source repo relate to the public v5.0.0 release?

**Resolved (2026-06-23, second pass): no divergence.** The first pass
assumed source was at `v4.0.0` with the v5 command model/docs/validation
scripts absent. That read was stale — current source is at `kit.json`
`kitVersion 5.0.0`, the `start` router skill exists, and the docs and
validation scripts the question listed all exist in source. There is no
"forward-port vs. re-export" decision to make; the Codex findings are
ordinary source-content/doc items, 4 of which were fixed this pass (the
rest false positives). See [risks.md](risks.md) (R2, retired) and the
corrected dispositions in
[reviews/2026-06-23-public-release-codex-findings.md](reviews/2026-06-23-public-release-codex-findings.md).
