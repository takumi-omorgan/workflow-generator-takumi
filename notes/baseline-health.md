# Baseline health note — M0-1

**Date:** 2026-06-05
**Branch:** `m0-baseline-health-and-drift`
**Issue:** M0-1 (Run and document baseline self-check)
**Scope:** Record the current pass/fail/not-run status of every check,
script, and smoke test in the kit before roadmap feature work begins.
This is an inspect-and-document task — no feature work, no redesign.

## How to reproduce

All commands run from the repo root on `main` (kit-development checkout,
with skills symlinked via `link-skills` per CLAUDE.md dogfooding rules).
Platform: macOS (darwin), `bash`, `python3` available; `shellcheck` not
installed.

## Results summary

| # | Check | Command | Result |
|---|---|---|---|
| 1 | Bash syntax — all `bin/` scripts | `bash -n bin/*` (+ `bin/lib/*.sh`) | **PASS** (7/7) |
| 2 | shellcheck lint | `shellcheck -S warning bin/*` | **NOT RUN** — `shellcheck` not installed |
| 3 | Python syntax — audit harness | `python3 -m py_compile notes/skills-audit-2026-05-07/*.py` | **PASS** (3/3) |
| 4 | `check-plan-criteria-drift` | `bin/check-plan-criteria-drift --check` | **PASS** (exit 0, no drift) |
| 5 | `check-state-cap` | `bin/check-state-cap --check` | **PASS** (`design/state.md` 55 lines, cap 100) |
| 6 | `check-plan` (ADR criteria) | `bin/check-plan --criteria-set adr --input design/adr/adr-045-*.md` | **PASS** (5 pass, 1 documented WARN: ADR-C6 semantic check deferred by design) |
| 7 | `check-plan` (prompt criteria) | `bin/check-plan --criteria-set prompt --input prompts/issue-080-*.md --format json` | **PASS** (result: pass) |
| 8 | Skills audit metrics | `python3 notes/skills-audit-2026-05-07/audit.py` | **PASS** (19 rows; all within budget — see M0-2 audit) |
| 9 | ADR index sync | `bin/sync-adr-index --check` | **PASS** (index in sync) |
| 10 | Internal markdown links — front-door docs | link resolver over `README.md`, `CLAUDE.md`, `docs/*.md` | **PASS** (115 local links, 0 broken) |
| 11 | Internal markdown links — all tracked `.md` | link resolver over `git ls-files '*.md'` | **PASS with caveats** (533 links, 51 flagged — almost all illustrative/target-context false positives; 2 genuine defects, see below) |
| 12 | Installer fresh-install smoke | `install-workflow-kit --target=$TMP --project-name=demo --non-interactive` | **PASS with 1 defect** (installs cleanly; initial commit omits `design/` — see M0-3) |
| 13 | Installer idempotent rerun | rerun + `--force` rerun against same target | **PASS** (reruns skip existing files; "nothing to commit"; no duplicate commits) |

### Not tested (explicit gaps)

- **`shellcheck` lint (check #2).** Not installed on this host. `bash -n`
  confirms syntactic validity but not style/quoting lint. Gap recorded;
  no CI runs shellcheck today either (see below).
- **`bin/check-plan` reserved criteria sets** — `changelog`,
  `milestone-summary`, `pr-body` are stubbed to exit 2 by design
  (reserved for follow-up issues per the script header). Not a failure.
- **`verify.py` third-party verification** — requires `OPENROUTER_API_KEY`
  and spends tokens against an external API. Deliberately not run in an
  autonomous M0 pass (no credentials in scope; external cost).
- **No automated test suite or CI workflow exists.** `.github/` contains
  only issue/PR templates — there is no `.github/workflows/`. The kit has
  no `Makefile`, `package.json`, or test runner. All "checks" are the
  hand-run `bin/` scripts and the audit harness above. This is the single
  largest baseline gap; the roadmap already plans to close it (M4 Issue 19
  "workflow self-test", Issue 20 "consistency checks"). Recorded here, not
  fixed in M0.
- **`bootstrap-workflow-kit` remote-fetch path** — not exercised. It
  clones a pinned release tag from `olivermorgan2/workflow-generator`
  (the upstream the kit was forked from); exercising it would hit the
  network and depend on a published release. Local installer
  (`install-workflow-kit`) was tested directly instead, which is the code
  path `bootstrap` ultimately invokes. See M0-3 for the repo-coordinate
  drift note.

## Findings (low-risk defects surfaced)

Full detail and classification live in the dedicated audit notes; the
two **fixed-in-this-PR** items and the one **high-severity-but-deferred**
item are summarised here so the baseline is self-contained.

1. **[deferred to M1 — confirmed defect] Installer initial commit omits
   `design/`.** `bin/install-workflow-kit` creates `design/adr/` (lowercase)
   but its `git add` list names `Design` (capital, line 552). On a
   case-sensitive checkout the `git add` silently no-ops (`2>/dev/null ||
   true`), so the seeded `design/adr/README.md` is left **untracked** after
   the "initial commit". Reproduced from a fresh install (`?? design/adr/README.md`
   persists across reruns). This is the most material M0 finding.
   **Not fixed in M0** because the open M1 PR (`m1-front-door-simplification`,
   PR #1) already rewrites this `git add` block to use lowercase `design`,
   and M1 substantially refactors the same file — an M0 edit would collide.
   Captured in `notes/bug-fixes.md` (installer cluster) and detailed in
   `notes/installer-idempotency-audit.md`.

2. **[fixed in this PR] Dead link in shipped skill content.**
   `skills/pause/SKILL.md` linked to
   `notes/handoff-2026-04-30-v-next-batch-resume.md`, which does not exist
   in the repo (no `notes/handoff-*` files are tracked). De-linked while
   preserving the descriptive sentence. See M0-4.

3. **[fixed in this PR] Stale ADR filename link.**
   `notes/feature-ideas.md` linked to `adr-014-claude-issue-executor.md`;
   the actual file is `adr-014-claude-issue-executor-skill.md`. Corrected.
   See M0-4.

4. **[already captured] `examples/*.md` broken refs to deleted
   `notes/issue-prompt*` files.** ~9 broken links across three example
   walk-throughs. Already drafted as a follow-up issue in
   `notes/issue-draft-examples-broken-refs.md` (out-of-scope for #89). Not
   re-fixed here; pointer retained.

5. **[deferred — doc freshness] Stale parenthetical framing in some
   skills.** e.g. `(future issue #19)` in `changelog`, `(Issue #6/#7/#15/#20)`
   in `idea-to-prd` / `issue-planner` — references to planned work that has
   since shipped. Low-risk; belongs to the broader freshness pass already
   tracked in `notes/refactoring-ideas.md`. See M0-2.

## Verdict

The kit is **healthy enough to proceed** with roadmap work. Every
runnable check passes. There are no broken front-door doc links, the ADR
index is in sync, all 19 skills are within metric budgets, and the
installer is idempotent. The one material defect (installer commit omits
`design/`) is already being fixed by the open M1 PR; the two trivial doc
defects are fixed in this PR. The dominant gap is the **absence of any
automated test/CI layer**, which the roadmap already schedules for M4.
