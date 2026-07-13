# Knowledge Layer — Index

A hand-maintained map of the internal knowledge layer for the
private/source workflow-kit repository. Start here.

See [SCHEMA.md](SCHEMA.md) for conventions and curation rules.

## Current state

The kit is **published**. Source is at `kit.json` kitVersion `5.0.1`; the
public kit lives at `olivermorgan2/claude-workflow-kit` with releases
`v5.0.0` (2026-06-12) and `v5.0.1` (2026-06-29, latest). The source repo is
post-release and carries the Hermes hardened-workflow overlay.

`design/state.md` is the session-continuity pointer for what to do next;
`gh` is canonical for issue and PR status. This line is the knowledge
layer's phase claim — it and [log.md](log.md) move together in a closeout.

## Contents

| File | What you'll find |
|---|---|
| [project-brief.md](project-brief.md) | What the kit is, its lifecycle, the public/private split, and the Claude/Codex/Hermes collaboration protocol |
| [risks.md](risks.md) | Active risks being tracked |
| [open-questions.md](open-questions.md) | Unresolved questions awaiting input or a decision |
| [log.md](log.md) | Dated, append-only log of knowledge updates |
| [reviews/](reviews/README.md) | Distilled findings from adversarial reviews |
| [SCHEMA.md](SCHEMA.md) | Conventions, file layout, and curation rules |

## Related (outside this layer)

- `design/adr/` — accepted Architecture Decision Records that govern the kit
- `docs/` — kit documentation (install, workflow, skills, troubleshooting)
- `notes/` — freeform working notes and per-issue eval summaries
- `CLAUDE.md` — Claude Code rules for working inside this repo
