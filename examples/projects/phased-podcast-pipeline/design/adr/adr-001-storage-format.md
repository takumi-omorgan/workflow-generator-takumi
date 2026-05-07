# ADR-001: Storage format for ingested notes

**Status:** accepted
**Date:** 2026-04-30
**Phase:** 1

## Context

Phase 1's ingest pipeline needs a place to put notes after parsing.
The choice affects every subsequent phase: Phase 2 reads from the
store to publish; Phase 3 references the store for feed metadata.
Two options carry equal weight in early scoping; pick one before
shipping `pipeline ingest`.

## Options considered

### Option A: SQLite database at `~/podcast/notes.db`

- Pros: structured queries; easy migrations; one file to back up;
  durable through ingest crashes.
- Cons: opaque to the writer's editor; needs a CLI to inspect.

### Option B: Filesystem layout at `~/podcast/store/`

- Pros: writer can `cat` and `grep` the store directly; integrates
  with their existing editor workflow; trivial to back up with rsync.
- Cons: schema migrations are awkward; no transactional guarantees on
  ingest.

## Decision

Adopt **Option B**. The writer values inspectability of their own
content over query speed; Phase 2's publishing pipeline does not need
SQL semantics. Document a versioned filesystem layout in
`docs/storage-format.md` and gate breaking changes via a top-level
`STORE_VERSION` file.

## Consequences

- Easier: writer can audit and edit ingested notes with their own tools;
  backups are `rsync ~/podcast/store/ <remote>`.
- Harder: schema changes need an explicit migration script; no
  cross-note queries beyond `find` and `grep`.
- Maintain: `STORE_VERSION` file and migration scripts under
  `bin/migrate/`.
- Deferred: indexing for fast lookup (Phase 3 if needed for
  large feeds).
