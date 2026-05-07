You are working in my `workflow-generator` repository.

Context:
- A toolkit of Claude Code skills, templates, and workflow docs that gives any structured project a disciplined, GitHub-first delivery flow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `docs/workflow-guide.md`.

ADR:
- File: `Design/adr/adr-044-mechanical-rewrite-immutability-exception.md`
- Decision: Mechanical path-string rewrites are an explicit exception to the "never edit accepted ADRs in place" rule, qualifying when (a) only path/identifier strings change, (b) the prose claim is unchanged, and (c) every occurrence in the ADR body changes uniformly. Editorial-meaning changes still require supersession.

GitHub Issue:
- Title: Accept ADR-044 and cite mechanical-rewrite immutability exception in CLAUDE.md (ADR-044)
- Number: #79
- Milestone: none
- Labels: feature

Goal
Flip ADR-044's status from `proposed` to `accepted` and add a one-line citation of the new exception to `CLAUDE.md`'s immutability rule so the rule and its exception are read together.

Why it matters
The kit's standing rule is "never edit accepted ADRs in place — supersede instead." Its purpose is to protect the **meaning** of recorded decisions, but the rule also blocks purely mechanical changes (e.g. directory renames) where the sentence meaning is unchanged. Without a defined exception, every rename either leaves stale path strings in historical ADRs or triggers a multi-ADR supersession cascade — both outcomes degrade the docs as the kit evolves. Issue #80 (rename `Design/` → `design/`, ADR-045) is the immediate consumer of this exception: it rewrites ~58 occurrences across 16 accepted ADRs and cannot proceed until ADR-044 is `accepted`. CLAUDE.md is the load-bearing rules file Claude reads at the top of every session, so the citation belongs alongside the immutability rule itself, not just inside ADR-044's body.

Requirements
- Edit `Design/adr/adr-044-mechanical-rewrite-immutability-exception.md` and change `**Status:** proposed` to `**Status:** accepted`. Do not change any other line in the ADR.
- Edit `CLAUDE.md` and add a one-line citation of ADR-044 to the immutability rule paragraph. The citation must reference ADR-044 by number and link to its filename; it must not rewrite or paraphrase the immutability rule itself.

Acceptance criteria
- ADR-044's `**Status:**` line reads `accepted`; no other content in the ADR has changed.
- `CLAUDE.md`'s immutability rule is followed (in the same paragraph or as an immediately-adjacent line) by a citation pointing at ADR-044, naming it as the mechanical-rewrite exception. The citation is one line and does not restate the criteria from ADR-044's body.
- `bin/sync-adr-index` runs clean (exit 0 — no rewrite needed, since the index already lists ADR-044; the status field in the index updates only if the index references status, which it does per `Design/adr/README.md`'s table).
- `bin/check-plan --criteria-set adr --input Design/adr/adr-044-mechanical-rewrite-immutability-exception.md` still passes after the status flip.

Scope and constraints
- Primary folders to touch: `Design/adr/` (one file: `adr-044-mechanical-rewrite-immutability-exception.md`), `CLAUDE.md` (root file).
- Folders to avoid unless absolutely necessary: `skills/`, `bin/`, `templates/`, `prompts/`, `docs/`, `examples/`, `archive/`, `notes/`. None of these need touching for this issue.
- This issue establishes a kit-wide rule but ships only two file edits. Resist scope creep — do not begin the `Design/` → `design/` rename here (that is #80 and is blocked by this issue).

Evaluation & testing requirements
- After the ADR-044 status flip, run `bin/check-plan --criteria-set adr --input Design/adr/adr-044-mechanical-rewrite-immutability-exception.md` and confirm exit 0 with all deterministic criteria passing.
- After the CLAUDE.md edit, eyeball the immutability paragraph to confirm: (a) the original rule text is unchanged, (b) the citation is one line, (c) the citation links to or names `Design/adr/adr-044-mechanical-rewrite-immutability-exception.md` clearly enough that a reader can find the ADR.
- Run `bin/sync-adr-index` after the ADR status change. The index in `Design/adr/README.md` should update ADR-044's status from `proposed` to `accepted` (a 1-line change). Stage the index alongside the ADR change in the same commit per ADR-023.
- All existing tests must continue to pass.
- If a change cannot be unit tested, document the manual verification.

Instructions for you
1. Read the relevant docs and existing files:
   - `CLAUDE.md`
   - `Design/adr/adr-044-mechanical-rewrite-immutability-exception.md`
   - `Design/adr/README.md` (to see how index entries are formatted)
   - any existing ADRs in `Design/adr/` that have already passed from `proposed` to `accepted` (for the status-flip pattern)
2. Propose a short, step-by-step implementation PLAN for this issue, including:
   - the exact lines to change in ADR-044 (status field only),
   - the exact wording and placement of the new citation line in CLAUDE.md,
   - whether the index needs a manual edit or `bin/sync-adr-index` will handle it,
   - your verification or test plan (the three commands above).
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - keep changes focused on this issue's scope (two files plus the regenerated index — nothing else),
   - commit incrementally with messages referencing the ADR and issue (e.g. "feat(adr): accept ADR-044 immutability exception (ADR-044, #79)").
5. At the end, provide an evaluation summary:
   - what changed,
   - verification steps performed (paste the `bin/check-plan` and `bin/sync-adr-index` exit codes),
   - any follow-up work needed for later issues (specifically: #80 is now unblocked),
   - exact commands I should run to inspect the result myself.

Do not start editing files until I explicitly approve your plan.
