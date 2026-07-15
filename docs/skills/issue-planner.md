# issue-planner — operator reference

Rationale, parsing edge-cases, and background for the `issue-planner` skill.
The agent operates from `skills/issue-planner/SKILL.md` (and the co-installed
`example.md`); it never reads this file. Anything needed to produce a correct
result stays in the body — this file is for the human operator.

## Why this skill exists

It comes from
[ADR-011](../../design/adr/adr-011-issue-planner-skill.md) (the hybrid
draft-approve-create flow) and
[ADR-012](../../design/adr/adr-012-github-projects-integration.md) (a GitHub
Projects board baked into issue creation). The naming convention `<repo> —
<milestone>` and the default board columns (Todo / In Progress / Review /
Done) come from ADR-012.

## What this skill does not do

- Does not write ADRs — that is `adr-writer`.
- Does not open PRs, create branches, or run the executor — those are the
  executor skill and `pr-review-packager`.
- Does not modify `design/mvp.md`, `design/build-out-plan.md`, or any ADR
  file in place. If the plan needs changing, re-run `prd-to-mvp`.
- Does not silently bulk-create issues. Human approval is mandatory.
- Does not work against an arbitrary repo. It targets the current working
  repo as resolved by `gh`.

## Parsing — tolerated drift and legacy paths

The skill parses by **heading hierarchy**, not regex or YAML, because humans
write these files; tolerate minor formatting drift.

**Phase-driven path.** When the build-out plan contains `### Phase N: <name>`
blocks (post-ADR-032) or `### Phase N — <name>` (legacy), create **one
milestone per phase** named "Phase N — <name>" and assign each issue to its
phase's milestone. An issue's phase is determined by, in order: the
`**Phase:**` frontmatter on its linked ADR; else the phase whose **Scope** or
**Deliverables** bullets best match the issue title; else the user's
confirmation at approval. The `## Milestone recommendation` table, when
present, can override the default per-phase milestone name.

**Single-phase fallback.** A plan with exactly one `### Phase` block, or no
`### Phase` headings at all, is one implicit phase: one milestone for the
whole project (named from the `## Milestone recommendation` table or prompted).

**Backlog-section fallback (legacy).** If `## Initial issue backlog` is
missing or empty, derive issues from each phase's **Deliverables** bullets,
and warn the user that this fallback is in use.

Tolerated drift:

- Milestone short names may be prefixed (`M1`, `M1 - name`, `Milestone 1`).
  Normalise to the `## Milestone recommendation` table's form if present,
  else use the text as-is.
- Bullets may use `-` or `*` — accept both.
- A backlog subheading with zero bullets is skipped with a warning.
- A malformed heading (e.g. `###Phase 1` with no space) is skipped and
  reported at the end as a parsing warning.

The `## Milestone recommendation` table maps milestone short names (M1, M2, …)
to a focus description used in the milestone's GitHub description field.

From `design/mvp.md`: pull the **product name** from `# <name> — MVP` for the
board name; mention a **product principle** in an issue body only when
directly relevant (keep terse); use the **In scope / Out of scope** lists to
sanity-check the backlog (warn at approval if a draft maps to an out-of-scope
item). From `design/adr/`: parse each `# ADR-NNN: Title`; attach a link when
a draft mentions the number, topic, or a close title match; else write `none`
with a one-line reason.

`design/planning.md` (optional): when present, its sequencing-rationale
section informs phase ordering and its requirement IDs (`R1`, `R2`, …) are
referenced in issue bodies for traceability; when absent, phase order comes
from `build-out-plan.md` alone.

## Edge cases

- **Missing `design/mvp.md` or `design/build-out-plan.md`:** stop cleanly;
  print which file is missing and the prerequisite skill (`prd-to-mvp`).
- **Plan files exist but backlog section is empty:** fall back to `## Phases`
  deliverables (above) and warn.
- **Malformed headings:** skip the malformed section, collect as warnings,
  show them at approval.
- **No milestones parsable:** prompt for a single default milestone name and
  reuse it for the batch.
- **`gh` not authenticated:** stop and print `gh auth login` instructions.
- **Not inside a GitHub-backed repo:** `gh repo view` fails — stop cleanly
  and ask the user to check their remote.
- **User is in this kit repo itself:** `design/mvp.md` /
  `design/build-out-plan.md` do not exist here, so the skill correctly stops
  at the missing-plan-files check. Expected — the skill runs in target
  projects.
- **Draft maps to an "Out of scope" item:** warn at approval but allow
  creation (the user may be planning a future milestone).
- **`--force` on a repo with pre-existing matches:** proceed, but remind the
  user in the preflight summary that duplicates will be created.

## Worked example

See [`../../skills/issue-planner/example.md`](../../skills/issue-planner/example.md)
for a worked run on a small Pace Drift build-out plan.
