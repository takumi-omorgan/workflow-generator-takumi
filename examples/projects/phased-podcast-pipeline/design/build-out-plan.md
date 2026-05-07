# phased-podcast-pipeline — Build-Out Plan

**Last updated:** 2026-04-30

## Objective

Ship a tool that turns a writer's research notes into a publishable
podcast feed. The build is sequenced into three phases so each can
deliver standalone value: foundation (storage format and ingestion),
publishing (turning a note into an episode), distribution (RSS feed
and platform submission).

## Build strategy

1. Settle storage format and ingestion (Phase 1).
2. Build the note → episode pipeline (Phase 2).
3. Distribute via RSS and platform-specific feeds (Phase 3).

## Scope

- In scope: end-to-end note-to-feed pipeline for a single writer.
- Out of scope: multi-writer / team accounts, paid hosting, monetisation,
  analytics dashboards.
- Assumptions: writer has access to a Markdown editor, hosts notes in
  one folder, owns a domain for the feed URL.

## Success criteria

The plan is complete when a writer can:

1. Drop a Markdown note into `~/podcast/notes/`.
2. Run `pipeline publish <note>` to produce an episode MP3 plus a
   feed entry.
3. Subscribe to the resulting RSS feed in any podcast client.

## Phases

<!-- Each phase below is a delivery unit. issue-planner creates one
     GitHub milestone per phase; /release treats one phase as the
     default release boundary. -->

### Phase 1: Foundation

- **Goal:** the writer can ingest Markdown notes into a structured
  store ready for downstream processing.
- **Scope:**
  - Decide storage format (filesystem vs SQLite)
  - Implement ingest CLI (`pipeline ingest <path>`)
  - Validate note structure against a documented schema
- **ADR dependencies:** ADR-001 (storage format)
- **Deliverables:** `pipeline ingest` command; `notes.db` (or
  filesystem layout); schema doc.
- **Exit criteria:** ingesting 50 sample notes round-trips without
  loss; v0.1.0 tag is cut.

### Phase 2: Publishing

- **Goal:** the writer can turn an ingested note into a published
  audio episode with metadata.
- **Scope:**
  - TTS pipeline for note → MP3
  - Metadata extraction (title, summary, duration)
  - Local feed entry generation
- **ADR dependencies:** ADR-002 (publishing pipeline)
- **Deliverables:** `pipeline publish <note>` command; per-episode
  metadata JSON; local RSS draft.
- **Exit criteria:** publishing one note produces a playable MP3 and
  a valid metadata record; v0.2.0 tag is cut.

### Phase 3: Distribution

- **Goal:** the writer can serve the RSS feed at a public URL and
  submit to major directories.
- **Scope:**
  - RSS 2.0 feed generation with iTunes namespace
  - Static-site upload pipeline for the feed and MP3 assets
  - Submission helper for Apple Podcasts and Spotify
- **ADR dependencies:** ADR-003 (distribution channels)
- **Deliverables:** `pipeline serve` command; deployment docs; submission
  checklist.
- **Exit criteria:** the writer's feed is live, validates against
  W3C feed validator, and is accepted by both Apple Podcasts and
  Spotify; v1.0.0 tag is cut.

## Milestone recommendation

| Milestone | Focus |
|---|---|
| Phase 1 — Foundation | storage format, ingest CLI |
| Phase 2 — Publishing | TTS, metadata, local feed entry |
| Phase 3 — Distribution | RSS 2.0, hosting, platform submission |

## Initial issue backlog

### Phase 1 — Foundation

- Decide and document storage format
- Implement `pipeline ingest <path>`
- Validate note schema on ingest

### Phase 2 — Publishing

- TTS pipeline for note → MP3
- Metadata extraction from note frontmatter
- Generate local RSS feed entry per episode

### Phase 3 — Distribution

- Generate RSS 2.0 feed with iTunes namespace
- Static-site upload pipeline (S3 or similar)
- Submission helper for Apple Podcasts + Spotify

## Testing strategy

Each phase has a fixture corpus: 50 sample notes for Phase 1, 5 sample
episodes for Phase 2, one full feed for Phase 3. End-to-end tests
verify the round-trip at each phase boundary.

## Risks and mitigations

### Risk 1 — TTS quality

Mitigation: ship Phase 2 behind a flag; allow human-recorded MP3
override for any episode.

### Risk 2 — Platform-submission turnaround time

Mitigation: Phase 3's exit criterion is "accepted," not "live with
listeners." Submission delays do not block other phases.

## Acceptance criteria for this document

This build-out plan is acceptable when it:

- matches the MVP statement,
- sequences work in three realistic phases with clear exit criteria,
- identifies one ADR per phase, and
- produces a practical milestone and issue structure.
