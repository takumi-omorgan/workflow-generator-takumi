You are working in my `workflow-generator` repository.

Context:
- The Claude Code Workflow Kit ships skills, templates, and docs that
  install into target projects to govern a disciplined development
  workflow.
- Follow the rules in `CLAUDE.md`.
- The workflow model is described in `generic-project-workflow.md` and
  the ADRs under `Design/adr/`.

ADR:
- File: `Design/adr/adr-030-installer-license-flag.md`
- Decision: implement `--license=mit --license-holder=NAME` in
  `bin/install-workflow-kit`. Use a template file at
  `templates/licenses/mit.txt` with `{{YEAR}}` and
  `{{COPYRIGHT_HOLDER}}` placeholders. Default behaviour unchanged
  (no LICENSE auto-scaffolded). Closes the implementation gap from
  ADR-025.

GitHub Issue:
- Title: Implement installer --license flag (ADR-030)
- Number: #38
- Milestone: v3.2.0 — project-agnostic framing, remote install, license flag
- Labels: feature, docs

Goal
Wire the `--license=mit` and `--license-holder=NAME` flags into
the installer so the contract documented in ADR-025 is real.

Why it matters
ADR-025 documented the flags but the installer never learned them.
Users trying the flags today get "unknown argument" errors. The
gap is small but real — a contract / behaviour mismatch.

Requirements
- Create `templates/licenses/mit.txt` with the canonical SPDX MIT
  text. Use `{{YEAR}}` and `{{COPYRIGHT_HOLDER}}` placeholders.
  Do not modify the canonical license wording — license scanners
  must still recognise the rendered output as MIT.
- Update `bin/install-workflow-kit`:
  - Add `--license=VALUE` flag. Validate VALUE: only `mit` accepted
    initially; on invalid input, print a useful error listing
    supported identifiers and exit non-zero.
  - Add `--license-holder=NAME` flag. If absent and `--license` is
    set, fall back to `--project-name`. If both absent and
    `--license` is set, fall back to the target directory's
    basename.
  - Add a new `render_license()` (or similar) step that runs
    AFTER the existing skill copy / CLAUDE.md render steps and
    BEFORE the initial commit step.
  - Year is the current year (`date +%Y`).
  - Skip-if-exists for target's `LICENSE`. `--force` overwrites.
  - Help text (`--help` / usage block) documents the new flags.
- Update `docs/install.md`:
  - Flag table in Section 3A gains rows for `--license` and
    `--license-holder`.
  - Add a short example showing the flags in use.
- Update `templates/README.md` index with a row for
  `templates/licenses/` (or a row pointing at
  `templates/licenses/mit.txt` specifically — your call;
  whichever fits the existing table style).
- Run `bin/sync-adr-index` after the ADR lands.

Acceptance criteria
- `bin/install-workflow-kit --help` shows the two new flags with
  the documented defaults and fallbacks.
- A scratch test scaffolds a target with `--license=mit
  --license-holder="Jane Doe"` and produces a `LICENSE` file in
  the target containing `Copyright (c) <current-year> Jane Doe`
  followed by canonical MIT text.
- A scratch test without `--license` produces no `LICENSE` (default
  unchanged from ADR-025).
- A scratch test with `--license=mit` but no `--license-holder`
  uses the `--project-name` value as the holder.
- A scratch test with `--license=foo` errors out cleanly with a
  list of supported identifiers.
- A scratch test where the target already has a `LICENSE` skips
  without `--force` and overwrites with `--force`.
- ADR-030 is `accepted`; ADR index reflects that.

Scope and constraints
- Primary folders: `bin/`, `templates/`, `docs/install.md`,
  `Design/adr/`, `prompts/`.
- Folders to avoid: `skills/` (the installer is the only thing
  changing here), `examples/`, `notes/`.
- Do not modify the canonical MIT text. Do not auto-scaffold
  LICENSE without the flag (default behaviour from ADR-025
  stands).
- Bash 3.2+ compatibility (macOS).
- Do not introduce additional license identifiers in this issue
  (Apache-2.0, BSD, ISC). Those are future scope.

Evaluation & testing requirements
- Manual test against a scratch directory using `mktemp -d` for
  each acceptance criterion above.
- Verify the rendered `LICENSE` matches the SPDX-published MIT
  text byte-for-byte after substitution.
- Confirm `--help` output renders cleanly.
- All existing installer tests / behaviours pass.

Instructions for you
1. Read the relevant docs:
   - `CLAUDE.md`
   - `Design/adr/adr-025-license.md` (the parent decision)
   - `Design/adr/adr-030-installer-license-flag.md` (this
     issue's decision)
   - existing `bin/install-workflow-kit` (especially the flag
     parsing block, the render-CLAUDE.md step, and the
     initial-commit step)
   - existing `templates/README.md` index format
   - existing `docs/install.md` flag table format
2. Propose a short, step-by-step PLAN:
   - the exact MIT template file structure (placeholders, header
     comment, etc.),
   - flag parsing additions (where in the existing parse loop),
   - the render_license() function design (path resolution,
     skip-if-exists, --force handling),
   - the help-text additions,
   - the docs/install.md flag-table row additions and example,
   - the templates/README.md index row,
   - the manual test plan.
3. Wait for my approval of the plan before making any edits.
4. After I approve, implement the plan:
   - one logical commit per concern (template + ADR; installer
     code; docs/help updates),
   - each commit references ADR-030 and #38.
5. At the end, provide an evaluation summary:
   - the rendered LICENSE from one of the test runs,
   - the help output,
   - manual test results,
   - exact commands to verify.

Do not start editing files until I explicitly approve your plan.
