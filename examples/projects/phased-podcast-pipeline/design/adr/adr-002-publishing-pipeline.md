# ADR-002: Publishing pipeline — note to MP3

**Status:** accepted
**Date:** 2026-04-30
**Phase:** 2

## Context

Phase 2 turns an ingested note into a playable audio episode. The
note → MP3 step is the most expensive part of the pipeline; choosing
the wrong tooling locks Phase 3 into specific hosting characteristics
(file size, codec, duration).

## Options considered

### Option A: Cloud TTS service (e.g. ElevenLabs, AWS Polly)

- Pros: high audio quality; natural prosody; minimal local compute.
- Cons: per-character cost; network dependency; vendor lock-in.

### Option B: Local TTS via piper or coqui

- Pros: zero per-episode cost; offline-capable; one-time model
  download; no vendor lock-in.
- Cons: lower audio quality on out-of-the-box models; needs a
  GPU-or-fast-CPU host for reasonable latency.

## Decision

Adopt **Option B** for the v0.2.0 release. The writer is the only
listener of the prototype output and can tolerate piper's quality. A
follow-up ADR can revisit cloud TTS once Phase 3 ships and listener
feedback is available. Wrap the TTS step behind a `tts.engine`
config so swapping later is a one-line change.

## Consequences

- Easier: zero per-episode cost; the writer can iterate on a note's
  prose and re-render without burning credits.
- Harder: audio quality is the bottleneck on early-listener experience;
  expect to revisit.
- Maintain: piper model file (~150 MB) under `~/.cache/podcast/`;
  document upgrade path.
- Deferred: human-recorded override path (already noted as a Phase 2
  risk mitigation).
