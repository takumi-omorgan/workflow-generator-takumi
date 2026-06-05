# Self-test log

Results of the workflow self-test (see [`docs/self-test.md`](../docs/self-test.md)),
newest first. Two kinds of entry:

- **Automated** — one line appended by `bin/self-test --append-log`:
  `status`, steps passed/total, elapsed seconds. Regression signal for the
  non-mutating validation surface.
- **Manual** — a short block from the full idea→first-PR walk: elapsed
  wall-clock time, number of skills/commands invoked, and friction points.

The most recent results of each kind are summarised in release notes so
the kit's friction can be tracked release over release.

## Automated

- 2026-06-05T09:56:30Z — status=ok, 9/9 steps, 1s elapsed (M4 baseline:
  validate-kit-json, validate-carry-forward, check-consistency,
  check-state-cap, bash -n across bin/, and the carry-forward/receipt stub
  self-checks all green).

## Manual

_No manual full-flow run recorded yet._ The first should be taken on a
throwaway repo when M4 (or the next release) is prepared, following
[`docs/self-test.md` §2](../docs/self-test.md). Record elapsed time,
commands invoked, and friction here.
