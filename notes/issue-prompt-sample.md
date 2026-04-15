<!--
  Sample filled Claude Code session prompt.
  Project: Pace Drift (the running example used across this kit's
  skill examples — see skills/idea-to-prd/example.md through
  skills/adr-writer/example.md).
  Issue: the first issue from Pace Drift's M1 — implement the GPX parser.
  This sample shows what notes/issue-prompt.md looks like once filled.
-->

You are working in my `pace-drift` repository.

Context:
- A web app that shows where my race pace drifted from a target pace, loaded from a single GPX file.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `Design/build-out-plan.md`.
- AI-readable summary is at `Design/ai-summary.md`.

ADR:
- File: `Design/adr/adr-001-gpx-parsing-location.md`
- Decision: Parse GPX files in the browser, not on a server.

GitHub Issue:
- Title: Implement GPX parser (ADR-001)
- Number: #11
- Milestone: M1 - Foundation
- Labels: feature

Goal
Build a browser-side GPX parser that takes one GPX file and returns the
ordered list of track points with their time, position, and elevation.
Phase-1 input to the drift-computation module that comes next.

Why it matters
Phase 1 of the build-out plan is "GPX in, drift numbers out, no UI."
The parser is the first half of that — without it, the drift module
has nothing to consume and nothing in Phase 1 can be validated end-to-end.

Requirements
- Parse a single `.gpx` file (single track, single segment).
- Return an ordered array of track points with `{ time, lat, lon, elevation }`.
- Reject malformed input with a clear error rather than silently producing
  nonsense.
- Run entirely in the browser; no Node-only APIs.

Acceptance criteria
- Given a real race GPX (one of the test fixtures), the parser returns
  the expected number of track points and the first/last points match
  hand inspection.
- Given a malformed GPX (truncated, wrong root element, missing
  timestamps), the parser throws a typed error naming what is wrong.
- The parser module exports a single `parseGpx(input: string)` function
  with a documented return type.

Scope and constraints
- Primary folders to touch: `src/parser/`, `test/parser/`, `test/fixtures/`
- Folders to avoid unless absolutely necessary: `src/ui/`, `src/drift/`, `Design/`
- Browser-only — no Node-specific imports. ADR-001 is the constraint source.

Evaluation & testing requirements
- Every new module or significant function MUST have unit tests.
- Tests go in `test/` mirroring `src/`.
- Cover at minimum: happy path, edge cases, error handling.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing code:
   - `CLAUDE.md`
   - `Design/adr/adr-001-gpx-parsing-location.md`
   - `Design/ai-summary.md`
   - any existing modules under `src/parser/`
   - any existing tests related to the modules you will change
2. Propose a step-by-step implementation PLAN, including:
   - new files/modules to create,
   - existing files to modify,
   - key functions/classes and their structure,
   - your test plan: which test files, what scenarios, what edge cases.
3. Wait for my approval before making any edits.
4. After I approve, implement the plan:
   - write tests alongside the implementation, not as an afterthought,
   - keep changes focused on this issue's scope,
   - commit incrementally with messages that reference the ADR and issue
     (e.g. "Add GPX parser (ADR-001, #11)").
5. At the end, provide the evaluation summary specified in
   docs/issue-prompt-guide.md.

Do not start editing files until I explicitly approve your plan.
