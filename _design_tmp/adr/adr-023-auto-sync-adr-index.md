# ADR-023: Auto-sync the ADR index in `Design/adr/README.md`

**Status:** accepted
**Date:** 2026-04-26

## Context

The ADR index in `Design/adr/README.md` repeatedly drifts from the
filesystem. As of 2026-04-26 it listed only ADR-001 through ADR-006
while the directory contained 21 ADRs; this was caught and backfilled
manually. Status transitions cause similar drift — when ADR-002 was
superseded by ADR-022, the index row needed a separate manual edit.

Index drift is a hygiene problem with two costs:

1. **Discoverability** — readers can't find ADRs by title or filter by
   status without scanning the directory directly.
2. **Authoring friction** — every new ADR or status change requires a
   second edit to the README, and that second edit is easy to forget.

This ADR establishes a regenerator that keeps the index in sync
automatically, removing the second-edit step from the author's
workflow. It applies to both the kit's own repo and target projects
that install the kit.

## Options considered

### Option A: Skill-level regeneration only (adr-writer)

- Pros: smallest change; fits the existing model (skills are the
  primary mutation path).
- Cons: only fires when the skill is the editor; manual ADR edits,
  status flips by hand, and out-of-band Claude sessions are missed.
  The drift problem partly persists.

### Option B: Regenerator script + skill integrations

- Pros: deterministic and idempotent; catches every Claude-driven
  path that touches ADRs (`adr-writer`, `claude-issue-executor`,
  `pr-review-packager`, `release`); reusable across the kit and
  target projects; runs cleanly in CI as a drift check.
- Cons: a small new piece of code to maintain (shell script, no
  runtime deps); marker fences in the README must stay intact.

### Option C: Option B plus an installer-managed git pre-commit hook

- Pros: catches manual commits where Claude is not involved; closes
  the last drift gap.
- Cons: git hooks are bypassable (`--no-verify`) and fragile across
  machines; installation increases scaffolding surface area; risk of
  blocking unrelated commits if the script ever errors.

### Option D: Fully generated README (no manual editorial)

- Pros: the simplest contract — the file is output.
- Cons: kills explanatory prose around the index; would force
  anything editorial into a separate file; rejected as overreach.

## Decision

Adopt **Option B** as the baseline. Build `bin/sync-adr-index`:

- Scans `Design/adr/adr-*.md`. Parses the title from `# ADR-NNN: ...`
  and the status from the first `**Status:**` line.
- Rewrites only the region between marker fences
  `<!-- adr-index:start -->` and `<!-- adr-index:end -->` in
  `Design/adr/README.md`. Editorial text outside the fence is
  preserved.
- Idempotent. Returns exit code `0` on no-op, `1` on changes written
  (so it can run as a CI/pre-commit drift check).
- Sorted by ADR number ascending. Status column reflects whatever the
  ADR file currently says, including supersession links.

Wire it into the four ADR-touching skills as a final pre-commit step:
`adr-writer` (after creating the ADR), `claude-issue-executor`,
`pr-review-packager`, and `release` (each: if any
`Design/adr/adr-*.md` is staged, run the script and re-stage
`Design/adr/README.md`).

The optional git pre-commit hook (Option C) is **deferred** to a
follow-up ADR if drift recurs from manual commits in practice. Start
with Option B; only escalate if real evidence shows Option B is
insufficient.

The script and the marker-fenced README are installed into target
projects by `install-workflow-kit`, so target projects get the same
hygiene.

## Consequences

- ADR adds and status changes no longer require a second edit to the
  README; index drift becomes structurally impossible for
  skill-driven flows.
- A small shell script and four skill SKILL.md edits to maintain.
  Script is parser-driven, so a malformed ADR header will produce a
  noisy row rather than silently corrupt the index — acceptable
  trade-off.
- Marker fences in `Design/adr/README.md` are now load-bearing;
  removing or renaming them breaks regeneration. The fence comment
  itself is the warning to future editors.
- CI can run `bin/sync-adr-index` as a drift check (exit 1 if it
  would change anything) to catch out-of-band edits.
- Manual `git commit` paths that bypass Claude still risk drift until
  Option C ships. Acceptable for now; revisit if observed.
- Target projects installed via `install-workflow-kit` inherit the
  script and the fenced README; the existing installer step that
  copies `Design/adr/README.md` needs the fence preserved (no
  regression risk — the fence is plain HTML comments).
