# Workflow Kit Three-Project Evaluation — 2026-06-06

## Purpose

This report captures the parallel dogfood/evaluation run of the Claude Code Workflow Kit against three different new-project shapes. The goal was to test whether the kit's installer, generated project rules, design artifacts, issue workflow, and verification expectations work beyond the kit repository itself.

## Source run

- Evaluation workspace: `/Users/hermes/workflow-kit-project-evals/20260606-035611`
- Kit source used by the evals: `/Users/hermes/workflow-generator-takumi-m5`
- Projects evaluated:
  - `web-task-board` — long-running stateful HTTP service
  - `cli-expense-tool` — stateless batch CLI/package
  - `data-quality-pipeline` — file-in/artifacts-out data quality gate

## Executive summary

The kit successfully bootstrapped and guided three materially different project types. The installer path worked in non-interactive mode, copied the expected skills/templates/docs, handled local-only GitHub metadata by rendering `_TBD_`, and supported real implementation work with tests.

The most important finding was not that the kit can generate files; it can. The useful finding was that the workflow held up across different execution models:

- A web service where verification means starting a server, probing HTTP routes, and checking persistence across restart.
- A command-line tool where verification means stdout/stderr, JSON output, and exit-code behavior.
- A data pipeline where verification means schema-driven validation, generated report artifacts, row counts, and CI-friendly quality gates.

## Cross-project findings

### What worked

- **Installer behavior was reliable.** All three projects installed with `--with-docs --non-interactive` and created the expected workflow surface.
- **The generated `CLAUDE.md` files were useful.** They carried project-specific run/test commands, workflow rules, GitHub conventions, and definitions of done.
- **The design-first workflow transferred well.** PRDs, MVP/design docs, ADRs, state files, and issue prompts gave each project enough structure without requiring a heavy framework.
- **Stdlib-only constraints were workable.** All three evals intentionally avoided third-party runtime dependencies, and the kit did not fight that constraint.
- **Verification adapted to project shape.** The workflow did not force a single testing model; it allowed web smoke tests, CLI checks, unit tests, and artifact checks.

### Friction / bugs to carry forward

- **Stale path/casing references need strict checks.** Earlier dogfood work found stale `Design` references after the `Design/` → `design/` migration. This class of issue should be caught by release/self-test checks.
- **Placeholder behavior is acceptable but should stay explicit.** Rendering `_TBD_` for missing GitHub owner is correct for local evals, but docs should keep explaining how to replace it.
- **Target-project docs can be heavy.** Copying the full kit docs with `--with-docs` is useful for self-contained projects, but generated projects should make the boundary between local project docs and kit reference docs obvious.
- **Workflow success depends on good project-specific verification commands.** The kit should continue pushing agents to write exact run/test commands into `CLAUDE.md` and state files.

## Recommendation

Keep this evaluation as design evidence that the kit supports more than one toy path. Use these three projects as regression fixtures when changing installer behavior, generated `CLAUDE.md`, workflow docs, ADR conventions, or self-test/release checks.

---

## Full per-project reports


---

# Appendix: web-task-board

_Source report: `/Users/hermes/workflow-kit-project-evals/20260606-035611/web-task-board/EVAL_DONE.md`_


## Workflow Kit Evaluation — Web Task Board

**Project type:** single-process web app (HTTP routes, server-side HTML
templates, local JSON persistence)
**Date:** 2026-06-06
**Evaluator role:** acting as a real first-time user of the Claude Code
Workflow Kit
**Kit source:** `/Users/hermes/workflow-generator-takumi-m5`

---

### 1. Project summary & why it is a different project type

**Web Task Board** is a private, self-hosted kanban board: three columns
(To Do / Doing / Done), server-side-rendered HTML, a JSON read API, and
local JSON-file persistence — all on the Python **standard library**, no
pip dependencies.

Routes:

| Method | Path | Purpose |
|---|---|---|
| GET | `/` | board (HTML) |
| GET | `/api/tasks` | tasks as JSON |
| GET | `/healthz` | liveness probe |
| POST | `/tasks` | create (`title`, `note`) |
| POST | `/tasks/{id}/move` | move (`column`) |
| POST | `/tasks/{id}/delete` | delete |

**Why this is a distinct project type from the other two evals:** it is a
*long-running, stateful HTTP service*. Its defining concerns are request
routing, an HTTP request/response lifecycle, server-side HTML rendering,
post/redirect/get semantics, a background-process deployment model, and
durable on-disk state that must survive a restart. That stresses the kit
differently from a batch CLI or a static-artifact/library project: the
"deployment" is a server you must boot, bind to a port, probe over the
wire, and shut down — not a command that runs and exits. The ADR that
mattered here (storage engine choice) and the smoke test (curl against a
live socket, plus a restart-persistence check) are both shaped by the
service nature of the project.

The app is real, not a stub: 6 routes, atomic JSON writes, input
validation, and a 13-case stdlib `unittest` suite (store unit tests +
live-server integration tests), all green.

---

### 2. Kit install command & outcome

Command (run exactly as specified):

```bash
/Users/hermes/workflow-generator-takumi-m5/bin/install-workflow-kit \
  --target "/Users/hermes/workflow-kit-project-evals/20260606-035611/web-task-board" \
  --project-name "Web Task Board" \
  --with-docs --non-interactive
```

**Outcome: success.** The installer copied 22 skills, runtime templates,
the ADR-index helper, `.github/pull_request_template.md`, a target
`.gitignore`, the ADR README, rendered `CLAUDE.md`, copied the full kit
docs to `docs/workflow-kit/`, and made an initial commit
(`chore: install workflow kit (project-local)`). It ran its own `git init`
path cleanly on the pre-initialized repo. Exit status 0.

One non-fatal warning was emitted (expected, documented behavior):

```
warning: required placeholder {{GITHUB_OWNER}} has no default;
         rendered as _TBD_ (use --set GITHUB_OWNER=VALUE)
```

This is correct for a local-only eval with no GitHub remote — the
installer degraded gracefully rather than prompting or failing.

---

### 3. Files / artifacts generated by the kit

Counts from the install (verified on disk):

- **`.claude/skills/` — 22 skills** (adr-writer, audit-milestone,
  changelog, check-plan, clarify, claude-issue-executor,
  complete-milestone, feature-prd, idea-to-prd, issue-planner,
  milestone-summary, pause, planning, pr-review-packager, prd-normalizer,
  prd-to-mvp, prepare-issue, release, resume, review-pr, start,
  workflow-docs), each with `SKILL.md` + supporting `example.md` /
  `reference.md`.
- **`.claude/bin/sync-adr-index`** — local ADR-index regenerator.
- **`templates/`** — 12 runtime templates (adr, prd, mvp, state,
  planning, build-out-plan, issue, pr, decisions, readme, ai-summary,
  milestone-summary).
- **`docs/workflow-kit/`** — 15 docs (install, tutorial, workflow-guide,
  workflow-control, skills, ai-review, receipts, self-test,
  repo-structure, troubleshooting, github-setup, agent-contract,
  claude-code-guide, README).
- **`CLAUDE.md`** — rendered project rules (one intentional `_TBD_`:
  GITHUB_OWNER).
- **`design/adr/README.md`** — ADR index with marker fences.
- **`.github/pull_request_template.md`**, **`.gitignore`**,
  **`prompts/_template.md`**.

What the kit deliberately does **not** scaffold (you create these from
the templates): `design/prd.md`, `design/mvp.md`, `design/state.md`,
`design/build-out-plan.md`. The skills (`/start`, `/resume`) are written
to tolerate their absence.

---

### 4. Workflow steps exercised

Acting as a real user, following the kit's own conventions:

1. **Read `CLAUDE.md` + key skills** (`start`, `idea-to-prd`,
   `prepare-issue`) and the templates to learn the intended flow.
2. **Authored a PRD** at `design/prd.md` following
   `templates/prd-template.md` (all hard-required fields filled; open
   questions left non-empty as the template encourages).
3. **Authored the MVP cut** at `design/mvp.md` (in-scope / out-of-scope /
   acceptance criteria), the artifact `/prd-to-mvp` would produce.
4. **Recorded an ADR** — `design/adr/adr-001-json-file-persistence.md`
   from `templates/adr-template.md` (JSON file vs SQLite, with
   consequences), the decision that governs `app/store.py`.
5. **Ran the kit's local validation surface**:
   `.claude/bin/sync-adr-index` regenerated the ADR index table inside
   the marker fences; `--check` then reported "index is in sync" (exit 0).
6. **Created a session-continuity `design/state.md`** from
   `templates/state-template.md`, filling the fenced zones (phase,
   in-flight, recent, blockers, continue-here, machine-readable
   `next-action` YAML).
7. **Wrote a per-issue prompt** at
   `prompts/issue-001-task-editing.md` using the canonical
   `prompts/issue-NNN-*.md` convention from `prompts/_template.md` and
   the `prepare-issue` skill.
8. **Filled the `CLAUDE.md` placeholders** (stack, run, testing, code
   style, structure, test commands, definitions of done) as a real user
   would after the project settles.
9. **Built, tested, deployed, and smoke-tested** the app (sections 5–6).

GitHub-dependent stages (`/issue-planner`, `/pr-review-packager`,
`/release`, `/review-pr`) were **not** exercised — correctly out of reach
for a local-only eval with no remote; `state.md`'s `next-action` records
this as a blocker rather than a failure.

---

### 5. Deployment & smoke-test commands + results

**Deployment target:** local HTTP server on an ephemeral port, verified
with `curl` for `GET /` plus API/action paths.

Boot on an ephemeral port (`PORT=0`), in the background, capturing the
chosen port from startup output:

```
$ PORT=0 HOST=127.0.0.1 python3 -u -m app
Web Task Board listening on http://127.0.0.1:60679
```

Smoke test (exact results):

```
===== 1. GET / (board HTML) =====
HTTP 200  1608 bytes
<title>Web Task Board</title>
columns rendered: 3

===== 2. GET /api/tasks (empty board) =====
{ "tasks": [] }        HTTP 200

===== 3. POST /tasks (create — action path) =====
HTTP 303 (redirect)    x2  (created "Write eval report", "Deploy the board")

===== 4. GET /api/tasks (after create) =====
2 tasks returned, ids 1 & 2, column "todo"

===== 5. POST /tasks/1/move -> done =====
HTTP 303 ; /api/tasks shows task 1 column == "done"

===== 6. board HTML =====
Done <span class="count">(1)   # card moved into Done column

===== 7. error handling =====
POST /tasks (blank title) -> HTTP 400
GET  /nope                -> HTTP 404

===== 8. PERSISTENCE (restart process) =====
kill server; data/tasks.json (319 bytes) on disk
restart -> port 60693 -> GET /api/tasks -> count = 2, task 1 still "done"
```

Every assertion passed. Automated suite: `python3 -m unittest discover -s
test` → **13 tests, OK**. Server shut down cleanly; runtime `data/` and
`__pycache__` removed; git state clean.

---

### 6. What worked well

1. **Single-command install is genuinely turnkey.** One invocation with
   four flags produced a complete, committed scaffold. `--non-interactive`
   never blocked, and `--with-docs` putting the full guide set in-tree
   meant I never had to leave the project to learn the workflow.
2. **Graceful degradation without a GitHub remote.** The one required
   value it couldn't derive (GITHUB_OWNER) became a clearly-labeled
   `_TBD_` with a remediation hint, instead of a prompt or a hard error.
   A local-only project installs fine.
3. **`CLAUDE.md` is high-quality and self-documenting.** It explains the
   `_TBD_` convention inline, separates rules from spec/roadmap/summary,
   and the placeholders map cleanly onto a real stack. Filling it felt
   like answering a good checklist, not fighting a template.
4. **Templates are faithful and well-commented.** Each template's header
   comment states who fills it, where the output goes, and which skill
   consumes it. The PRD template even tells you which fields are
   hard-required — I could author a valid PRD without running any skill.
5. **The marker-fence pattern is robust.** `state.md`, `decisions`, and
   the ADR README all use `<!-- ...:start/end -->` fences so generators
   rewrite only their region and preserve editorial prose. Clean design.
6. **`sync-adr-index` works exactly as documented.** It picked up ADR-001,
   wrote the table, and `--check` confirmed sync. A real, useful local
   tool that needs no network.
7. **Skill metadata is rich and routable.** `SKILL.md` front matter
   (inputs/outputs/`next`/`permission-category`) makes the intended graph
   between skills legible; `/start`'s `next:` block reads like a usable
   state machine.

---

### 7. Friction, bugs & unclear guidance

1. **[MEDIUM — doc bug] `CLAUDE.md` points to the wrong prompt
   location.** The rendered `CLAUDE.md` says *"Per-issue prompts live in
   `notes/issueNN-prompt.md`"* and lists `notes/` in both the project-tree
   example and "See also". But every other artifact — the `prepare-issue`
   skill, `prompts/_template.md`, the `start` skill, and
   `state-template.md` — uses `prompts/issue-NNN-short-title.md`, and the
   installer creates `prompts/` (not `notes/`). A user trusting
   `CLAUDE.md` would create files in a directory the skills never read.
   The two conventions even disagree on the filename shape
   (`issueNN-prompt.md` vs `issue-NNN-short-title.md`).

2. **[LOW — UX] `sync-adr-index` returns exit code 1 on the common
   "rewrote" path.** Its first successful run (which *did* the useful
   work) exits 1; only a subsequent no-op `--check` exits 0. The script
   documents this, but exit 1 conventionally signals failure, so a naive
   CI step (`run sync-adr-index && ...`) would treat a normal rewrite as
   an error. A distinct code (e.g. 0 = success/changed, 2 = drift under
   `--check`) would be safer.

3. **[LOW — onboarding gap] Nothing in the installed tree tells a
   *brand-new* project where to start.** The kit copies templates and
   docs but scaffolds none of `design/prd.md` / `mvp.md` / `state.md`. A
   first-timer who opens the project sees a filled `CLAUDE.md` referencing
   `design/mvp.md` and `design/ai-summary.md` that **don't exist yet**.
   The intended answer ("run `/start` / `/idea-to-prd`") is only
   discoverable by reading `docs/workflow-kit/tutorial.md`. A one-line
   "Next: open Claude Code and run `/start`" banner in the rendered
   `CLAUDE.md` or a top-level `GETTING-STARTED` would close the gap.

4. **[LOW — placeholder leakage] `CLAUDE.md` ships dangling links to
   not-yet-existing files.** "See also" points at `design/mvp.md` and
   `design/ai-summary.md` unconditionally; on a fresh install these 404
   in an editor. Not wrong long-term, but momentarily confusing.

5. **[INFO — not a kit bug] Server stdout is line-buffered when piped**,
   so the "listening on port N" line didn't appear until I added
   `python3 -u`. This is a Python/my-app concern, not the kit's, but worth
   noting for anyone scripting an ephemeral-port deploy: read the port
   with unbuffered output or bind explicitly.

No crashes, no data loss, no destructive behavior, no broken skills
encountered. The friction is documentation-consistency, not function.

---

### 8. Severity-ranked recommendations

| # | Severity | Recommendation |
|---|---|---|
| 1 | **MEDIUM** | Fix the `notes/` vs `prompts/` contradiction in `templates/claude-md-template.md`. Change the "Issue-by-issue" rule, the project-tree example, and "See also" to `prompts/issue-NNN-short-title.md` so `CLAUDE.md` agrees with the skills, templates, and installer. Single source of truth for the prompt path. |
| 2 | **LOW** | Make `sync-adr-index` exit 0 on a successful rewrite (reserve non-zero for genuine errors and for `--check` drift). Update its header doc accordingly so it composes safely in CI/`&&` chains. |
| 3 | **LOW** | Add a one-line "Next step" pointer to the rendered `CLAUDE.md` (or a generated `GETTING-STARTED.md`): *"New project? Open Claude Code and run `/start`."* Closes the cold-start discovery gap. |
| 4 | **LOW** | Render the "See also" links in `CLAUDE.md` conditionally, or annotate them as "created later by the workflow", so fresh installs don't show dead links to `design/mvp.md` / `ai-summary.md`. |
| 5 | **INFO** | In `docs/workflow-kit/`, add a short note for HTTP-service projects on reading an ephemeral port for smoke tests (unbuffered stdout / explicit bind). Helps the exact "deploy on an ephemeral port and curl it" workflow this project type needs. |

---

### 9. Final verdict

#### GOOD

The kit installed in one command, degraded gracefully with no GitHub
remote, and gave me a coherent, well-documented set of conventions
(PRD → MVP → ADR → state → per-issue prompt) that I could follow to
produce real planning artifacts for a real, deployed, tested web service.
The templates are faithful and well-annotated, the marker-fence
generators are robust, and the one local validation tool I could run
(`sync-adr-index`) worked exactly as documented. Nothing broke, nothing
was destructive, and the app it helped me plan and build deploys and
passes a meaningful live smoke test (including persistence across a
restart).

It falls short of EXCELLENT because of one **MEDIUM** documentation
contradiction that would actively mislead a user (the `notes/` vs
`prompts/` prompt-location split between `CLAUDE.md` and every skill), a
mildly surprising exit-code convention in `sync-adr-index`, and a
cold-start onboarding gap where a fresh install references design files
that don't exist yet with no in-tree pointer to `/start`. All are
low-effort doc/UX fixes, not architectural problems — hence a confident
**GOOD**, knocking on EXCELLENT once recommendation #1 lands.

---

READY_FOR_AGGREGATION


---

# Appendix: cli-expense-tool

_Source report: `/Users/hermes/workflow-kit-project-evals/20260606-035611/cli-expense-tool/EVAL_DONE.md`_


## Workflow Kit Evaluation — CLI Expense Tool

**Date:** 2026-06-06
**Evaluator:** Claude Code (Opus 4.8)
**Project type:** Command-line application / package (Python, stdlib-only)
**Kit source:** `/Users/hermes/workflow-generator-takumi-m5`
**Target:** `/Users/hermes/workflow-kit-project-evals/20260606-035611/cli-expense-tool`

---

### 1. Project summary & why it is a different project type

The **CLI Expense Tool** (`expense`) is a zero-dependency Python 3.9+
command-line application that:

1. **Imports** a transaction CSV (configurable column names),
2. **Categorizes** each row via ordered keyword→category rules
   (first-match-wins, `Uncategorized` fallback), and
3. **Summarizes** spend per category (count, total, percent + grand total),
   rendered as a human table or machine-readable JSON.

It also has a `categorize` subcommand that echoes input rows with an added
`category` column.

**Why it is a distinct project type for kit testing:** This is a *batch
CLI / library* — no server, no long-running process, no UI, no network,
no external services. Its "deployment" is process invocation with
**exit-code semantics** as a first-class contract (0 = success, non-zero =
bad input). That stresses different parts of the kit than a web service or
a content/research project would: the design artifacts revolve around data
shape and failure modes rather than endpoints or prose, and the smoke test
is "run the binary, assert stdout + exit code" rather than "curl a route."
Among the three eval projects this is the stdlib-only, stateless,
exit-code-driven member of the set.

---

### 2. Kit install command & outcome

**Command (run verbatim as instructed):**

```bash
/Users/hermes/workflow-generator-takumi-m5/bin/install-workflow-kit \
  --target "/Users/hermes/workflow-kit-project-evals/20260606-035611/cli-expense-tool" \
  --project-name "CLI Expense Tool" \
  --with-docs --non-interactive
```

**Outcome:** ✅ Success. The installer:

- copied 22 skills into `.claude/skills/`,
- copied the `.claude/bin/sync-adr-index` helper and `prompts/_template.md`,
- copied 12 runtime templates into `templates/`,
- created `.github/pull_request_template.md`, `.gitignore`,
  `design/adr/README.md`,
- rendered `CLAUDE.md` from the template,
- copied all kit docs into `docs/workflow-kit/` (because of `--with-docs`),
- and created an initial git commit `chore: install workflow kit
  (project-local)`.

**One non-fatal warning was emitted (correctly):**

```
warning: required placeholder {{GITHUB_OWNER}} has no default; rendered as _TBD_
         (use --set GITHUB_OWNER=VALUE)
```

This is good behavior — it degrades gracefully to `_TBD_` rather than
failing, and tells you exactly how to fix it. Exit code of the installer
was 0.

---

### 3. Files / artifacts generated by the kit

| Path | What it is |
|---|---|
| `CLAUDE.md` | Project rules for Claude Code, rendered from template (with `_TBD_`/`{{…}}` placeholders to fill) |
| `.claude/skills/` (22 skills) | The full verb-layer workflow: `start`, `idea-to-prd`, `prd-normalizer`, `prd-to-mvp`, `planning`, `adr-writer`, `issue-planner`, `prepare-issue`, `claude-issue-executor`, `pr-review-packager`, `review-pr`, `audit-milestone`, `milestone-summary`, `complete-milestone`, `feature-prd`, `release`, `changelog`, `check-plan`, `clarify`, `pause`, `resume`, `workflow-docs` |
| `.claude/bin/sync-adr-index` | Script to regenerate the ADR index table in `design/adr/README.md` |
| `templates/` (12 files) | Runtime templates: prd, mvp, planning, adr, state, decisions, issue, pr, milestone-summary, build-out-plan, ai-summary, readme |
| `design/adr/README.md` | ADR index with marker-fenced auto-generated table |
| `.github/pull_request_template.md` | PR template |
| `.gitignore` | Sensible defaults (macOS, editors, `.claude/` local state; Python ignores present but **commented out**) |
| `docs/workflow-kit/` (14 docs) | Full doc set: install, workflow-guide, skills, tutorial, agent-contract, repo-structure, workflow-control, self-test, receipts, ai-review, github-setup, troubleshooting, claude-code-guide, README |
| `prompts/_template.md` | Per-issue prompt template |

**Artifacts I authored using the kit's conventions/templates:**

- `design/prd.md` (from `templates/prd-template.md`)
- `design/mvp.md` (from `templates/mvp-template.md`)
- `design/adr/adr-001-stdlib-only-rule-based-categorization.md` (from `templates/adr-template.md`)
- `design/state.md` (from `templates/state-template.md`, with marker fences)
- `notes/issue01-prompt.md` (per-issue planning prompt, kit convention)

---

### 4. Workflow steps exercised

I exercised the **MVP path** of the workflow manually (the kit is designed
to be driven by Claude Code skills inside an interactive session; in this
headless eval I followed the same artifact conventions the skills would
produce):

1. **Read the kit docs** — `install.md`, `workflow-guide.md`, `skills.md`,
   the templates, and the ADR README, to learn the intended flow
   (idea → PRD → normalize → MVP → ADRs → issues → execute → PR → release).
2. **PRD intake** (`/idea-to-prd` → `/prd-normalizer` shape) — wrote
   `design/prd.md` following the 11-ish-field template.
3. **MVP scoping** (`/prd-to-mvp` shape) — wrote `design/mvp.md` with
   explicit in/out-of-scope and success criteria.
4. **Decision capture** (`/adr-writer` shape) — wrote ADR-001, then ran the
   real installed tool `.claude/bin/sync-adr-index` to populate the ADR
   index table.
5. **State pointer** (`/pause`/`/resume` shape) — wrote `design/state.md`
   with the correct marker fences and a machine-readable `next-action` YAML
   block.
6. **Issue prep** (`/prepare-issue` shape) — wrote `notes/issue01-prompt.md`
   scoping the build with a Definition of Done.
7. **Implementation** — built the package, wrote tests, and filled in the
   `CLAUDE.md` placeholders (tech stack, run/test commands, structure).
8. **Validation surface** — ran the only validation surface the installer
   places in a target project, `sync-adr-index` (and its `--check` mode).

---

### 5. Deployment / smoke-test commands & results

**Deployment target:** run the CLI against sample CSV data and verify
output **plus** non-zero failure for bad input.

#### Build verification

```
$ python3 -m unittest discover -s tests
Ran 17 tests in 0.005s
OK
```

#### Smoke test — happy path (exit 0)

```
$ python3 -m expense_tool summary sample_data/expenses.csv
Category       Count       Total     Pct
----------------------------------------
Housing            1     1450.00   72.9%
Groceries          2      130.53    6.6%
Shopping           2      121.39    6.1%
Transport          3      110.75    5.6%
Utilities          1       79.00    4.0%
Dining             3       62.65    3.1%
Entertainment      2       27.48    1.4%
Uncategorized      1        8.50    0.4%
----------------------------------------
TOTAL                    1990.30  100.0%
exit=0
```

Category totals sum to the printed grand total (1990.30) ✅.

```
$ python3 -m expense_tool summary sample_data/expenses.csv --format json
{ "grand_total": 1990.3, "categories": [ … ] }   # parses cleanly, exit=0
$ python3 -m expense_tool categorize sample_data/expenses.csv | head -2
date,description,amount,category
2026-05-01,Whole Foods Market,84.20,Groceries          # exit=0
```

#### Smoke test — bad input (non-zero exit, the required failure case)

```
$ python3 -m expense_tool summary sample_data/malformed.csv
error: line 3: cannot parse amount 'not-a-number' as a number
exit=1

$ python3 -m expense_tool summary sample_data/missing_column.csv
error: required column 'description' not found in header ['amount', 'date', 'merchant']
exit=1

$ python3 -m expense_tool summary sample_data/does_not_exist.csv
error: file not found: sample_data/does_not_exist.csv
exit=1
```

**Result: PASS.** Valid input produces correct output with exit 0; all three
bad-input classes (unparseable amount, missing column, missing file) fail
loudly on stderr with exit 1 and print no wrong totals.

---

### 6. What worked well

- **Installer is clean and fast.** One non-interactive command produced a
  complete, coherent project scaffold and a tidy initial git commit. No
  manual cleanup needed. Clear, scannable log of every file it touched.
- **Graceful placeholder degradation.** The missing `GITHUB_OWNER` became
  `_TBD_` with an actionable warning instead of a hard failure, and the
  rendered `CLAUDE.md` carries an explicit note explaining what `_TBD_`
  means. No raw unresolved `{{PLACEHOLDER}}` *values* leaked into rendered
  required fields.
- **Documentation is genuinely excellent.** `--with-docs` ships a 14-file
  doc set. `workflow-guide.md`, `skills.md`, and the verb-layer table
  (`/start`, `/work`, `/ship`, …) make the intended flow obvious without
  reading every `SKILL.md`. `kit.json` is explicitly offered as the
  machine-readable inventory for agents — a thoughtful touch.
- **Templates are high quality.** Each template has a top comment block
  stating who fills it, where the output goes, and which skill consumes it.
  This made authoring the PRD/MVP/ADR/state artifacts unambiguous.
- **Marker-fence design is robust.** `design/state.md` and the ADR index use
  HTML-comment fences so tools rewrite only their zone and preserve human
  commentary. `sync-adr-index` correctly regenerated the index and is
  idempotent on re-run.
- **`sync-adr-index` is otherwise solid.** Correct table output, idempotent
  (second run exits 0 unchanged), and `--check` mode correctly reports
  in-sync (exit 0) vs. drift (exit 1).
- **Sensible `.gitignore`**, including correctly *not* ignoring
  `.claude/skills/` (the installed kit) while ignoring per-session
  `.claude/` state.

---

### 7. Friction / bugs / unclear guidance

1. **BUG — `sync-adr-index` returns exit 1 on a successful rewrite.**
   The normal (non-`--check`) path that *successfully rewrites* the index
   ends with `exit 1` (line 255 of `.claude/bin/sync-adr-index`), even
   though it prints `sync-adr-index: rewrote …`. So the very first time a
   user generates the ADR index — the common case — the command reports
   success in text but fails by exit code. Verified directly:
   - First generate (rewrite): prints "rewrote", **exit 1**.
   - Re-run when already in sync: **exit 0**.
   - `--check` in sync: exit 0; `--check` on drift: exit 1 (correct).
   The `--check` semantics (1 = drift) appear to have been copy-pasted onto
   the rewrite path. This will break any Makefile target, pre-commit hook,
   or CI step that runs `sync-adr-index` and checks `$?` — exactly the
   automation the marker-fence design invites. **Severity: HIGH** (silent
   `set -e`/CI failures on the happy path).

2. **Template guidance blocks (`{{…}}`) are left verbatim in rendered
   `CLAUDE.md`.** Two sections — "What this is" and "Project structure" —
   ship as multi-line `{{instruction text}}` rather than `_TBD_`. They are
   *guidance for a human to overwrite*, but unlike `_TBD_` (which the file
   explicitly explains) there is no in-file note that `{{…}}` blocks are
   placeholders. A new user could reasonably leave them in, and they read
   oddly. Consider rendering them as clearly-marked `<!-- FILL: … -->`
   comments, or `_TBD_`-style markers. **Severity: MEDIUM.**

3. **Python `.gitignore` entries ship commented out.** For a Python
   project, `__pycache__/` and `*.pyc` are commented out by default, so a
   test run immediately creates would-be-committed junk. The comment says
   "uncomment as your project requires," which is defensible language-
   agnostic behavior, but a `--lang python` hint (or auto-detection from a
   `pyproject.toml`) would remove a sharp edge. I uncommented them manually.
   **Severity: LOW.**

4. **No project-local validation/self-test surface.** `docs/workflow-kit/
   self-test.md` documents a great `bin/self-test` (validate-kit-json,
   check-consistency, etc.), but that script lives in the *kit repo* and is
   **not** installed into the target. The only executable validation a
   target project receives is `sync-adr-index`. A target-side
   `validate-design` (does `state.md` have all fences? do ADRs match the
   index? are required PRD fields non-empty?) would give users a local
   "is my workflow state healthy?" check. **Severity: LOW–MEDIUM.**

5. **Docs assume a GitHub remote; the local-only path is under-served.**
   `install.md`, `workflow-guide.md`, and `CLAUDE.md`'s GitHub-conventions
   section all assume `gh`, a remote, and PRs. That's the kit's stated model
   (ADR-002/ADR-028: git + GitHub + Claude Code), but for an offline eval or
   a purely local project there's no guidance on which steps degrade to
   "local only." Minor; the kit is upfront about its assumptions.
   **Severity: LOW.**

6. **Skills are agent-driven, so "running" them headlessly isn't
   possible.** This is by design (they're Claude Code skills, not CLI
   scripts), but worth noting for any automated evaluation: the only kit
   artifacts you can exercise non-interactively are the templates, the
   docs, and `sync-adr-index`. Everything else is exercised by Claude
   following the `SKILL.md`. Not a defect — a scoping note. **Severity:
   INFORMATIONAL.**

---

### 8. Severity-ranked recommendations

| # | Severity | Recommendation |
|---|---|---|
| 1 | **HIGH** | Fix `sync-adr-index` line 255: change `exit 1` to `exit 0` after a successful rewrite. The rewrite path is success, not drift. Add a regression test asserting `generate → $? == 0`. |
| 2 | **MEDIUM** | Render leftover `{{…}}` guidance blocks in `CLAUDE.md` (and any template) as explicitly-marked fill-in comments, or `_TBD_`-style markers, so they're visually distinct from real content and consistent with the `_TBD_` convention the file already documents. |
| 3 | **MED–LOW** | Ship a target-side `validate-design`/`self-test` so users get a local health check (fences present, ADR index in sync, required PRD/MVP fields filled) without the kit repo. |
| 4 | **LOW** | Add language/ecosystem awareness to the `.gitignore` step (e.g. detect `pyproject.toml`/`package.json`, or a `--lang` flag) and uncomment the matching ignores. |
| 5 | **LOW** | Add a short "local-only / no-GitHub" subsection to `install.md` or `workflow-guide.md` describing which steps are skippable when there's no remote. |

---

### 9. Final verdict

#### GOOD

The kit installed flawlessly, produced a coherent and well-documented
project scaffold, and its templates + docs made it genuinely easy to drive
a real CLI project from idea → PRD → MVP → ADR → implementation →
smoke-tested deploy. Documentation quality and the template/marker-fence
design are standout strengths.

It falls short of EXCELLENT because of one **HIGH-severity correctness bug**
in the single executable validation tool a target receives
(`sync-adr-index` returns failure on a successful rewrite — a real
CI/Makefile footgun), plus medium friction from unrendered `{{…}}`
guidance blocks in `CLAUDE.md` and the absence of a target-side validation
surface. None of these blocked building or deploying the project — the
final artifact builds, all 17 tests pass, and the smoke test meets the
deployment target exactly (correct output on valid input, exit 1 on three
classes of bad input) — but the `sync-adr-index` exit-code bug would bite a
real user wiring the kit into automation. Fixing recommendation #1 alone
would move this to the EXCELLENT boundary.

---

READY_FOR_AGGREGATION


---

# Appendix: data-quality-pipeline

_Source report: `/Users/hermes/workflow-kit-project-evals/20260606-035611/data-quality-pipeline/EVAL_DONE.md`_


## Workflow Kit Evaluation — Data Quality Pipeline

**Date:** 2026-06-06
**Evaluator project:** Data Quality Pipeline (`dqpipeline`)
**Kit source:** `/Users/hermes/workflow-generator-takumi-m5`
**Target:** `/Users/hermes/workflow-kit-project-evals/20260606-035611/data-quality-pipeline`

---

### 1. Project summary & why it is a different project type

A **batch data-quality pipeline**: a stdlib-only Python CLI that validates CSV
records against a declarative JSON schema of column rules and emits quality
reports plus clean/rejected artifacts.

- **Inputs:** a CSV file + a JSON schema (`type`, `required`, `unique`,
  `min`/`max`, `enum`, `regex`, `primary_key`).
- **Outputs:** `report.json` (structured), `report.md` (human), `clean.csv`,
  `rejected.csv` (with an `_errors` column).
- **Contract:** exit `0` when pass rate ≥ `--fail-under`, `1` when the quality
  gate fails, `2` on usage error — so it works as a CI data gate.

**Why this is a distinct project type from a web app or a library:** it is a
**batch/ETL-style data tool**, not a service or an importable package. Its
defining surface is a *file-in → artifacts-out* transformation driven by a
non-code config (the schema), and its "deployment" is a process exit code in CI
rather than a running server or a published API. That exercises the kit against
a data-engineering workflow whose artifacts (schemas, fixtures, reports) and
success criteria (row counts, pass rates, exit codes) differ markedly from
request/response or function-call testing. Zero third-party dependencies also
stresses the kit's "minimal deps" path.

### 2. Kit install command & outcome

Command (run verbatim as instructed):

```bash
/Users/hermes/workflow-generator-takumi-m5/bin/install-workflow-kit \
  --target "/Users/hermes/workflow-kit-project-evals/20260606-035611/data-quality-pipeline" \
  --project-name "Data Quality Pipeline" \
  --with-docs --non-interactive
```

**Outcome: success.** The installer detected the existing git repo, copied
skills/templates/docs, rendered `CLAUDE.md`, and created its own commit
(`chore: install workflow kit (project-local)`). It correctly **skipped the
existing `.gitignore`** rather than clobbering it. One warning was emitted:

```
warning: required placeholder {{GITHUB_OWNER}} has no default;
rendered as _TBD_ (use --set GITHUB_OWNER=VALUE)
```

This is expected behaviour under `--non-interactive` (documented), not a failure.

### 3. Files / artifacts generated by the kit

| Path | What it is |
| --- | --- |
| `CLAUDE.md` | Rendered project-rules file (from `claude-md-template.md`) |
| `.claude/skills/` | 22 workflow skills (start, planning, idea-to-prd, prd-to-mvp, adr-writer, prepare-issue, claude-issue-executor, pr-review-packager, release, resume, pause, …) |
| `.claude/bin/sync-adr-index` | Executable that regenerates the ADR index table |
| `templates/` | 12 runtime templates (prd, mvp, adr, state, planning, pr, issue, …) |
| `design/adr/README.md` | ADR index with marker fences (from `adr-readme-template.md`) |
| `.github/pull_request_template.md` | PR template referenced by CLAUDE.md |
| `prompts/_template.md` | Per-issue prompt template |
| `notes/` | Working-notes directory |
| `docs/workflow-kit/` | 15 docs (agent-contract, workflow-guide, workflow-control, install, tutorial, skills, troubleshooting, …) via `--with-docs` |

**Artifacts I authored using the kit's conventions/templates:**

- `design/prd.md` — full PRD following `templates/prd-template.md` (all
  hard-required fields populated; open questions kept non-empty as the template
  advises).
- `design/adr/adr-001-declarative-json-schema.md` — ADR following
  `templates/adr-template.md` (context / 3 options / decision / consequences).
- `design/state.md` — session-continuity pointer from `templates/state-template.md`
  with all marker-fence zones filled.
- Filled in `CLAUDE.md` (stack, run/test commands, structure, conventions).

### 4. Workflow steps exercised

1. **Install** the kit (`--with-docs --non-interactive`) into a pre-existing repo.
2. **Inspect** generated `CLAUDE.md`, `.claude/skills/`, `docs/workflow-kit/`,
   `design/adr/`, and the templates.
3. **Read skills** as a user routing through the kit: `start` (the `/start`
   front door), `feature-prd` — to understand the intended PRD→MVP→issue flow.
4. **Author a PRD** (`design/prd.md`) using `prd-template.md` conventions.
5. **Write an ADR** (`adr-001`) using `adr-template.md` conventions.
6. **Run the ADR-index validation surface:** `.claude/bin/sync-adr-index`
   (rewrote index, exit 1) then `--check` (in sync, exit 0).
7. **Create `design/state.md`** from the state template (the `start`/`resume`
   router expects it; see friction §6).
8. **Fill `CLAUDE.md`** placeholders with real project values.
9. **Commit** kit artifacts, leaving a clean working tree.

### 5. Deployment / smoke-test commands & results

**Deployment target for this project:** run the pipeline on good and bad fixture
CSVs and verify report files are created with expected counts.

Unit tests (stdlib `unittest`, 10 tests):

```
$ python3 -m unittest discover -s tests
Ran 10 tests in 0.002s
OK
```

Smoke test — good fixture (expected: all valid, gate PASS, exit 0):

```
$ python3 -m dqpipeline validate fixtures/customers_good.csv \
    --schema schemas/customers.json --out-dir reports/good --fail-under 0.95
Validated 8 rows against schema 'customers'.
  valid:   8
  invalid: 0
  errors:  0
[PASS] pass_rate=100.0% (threshold 95.0%)
exit=0
```

Smoke test — bad fixture (expected: partition, gate FAIL, exit 1):

```
$ python3 -m dqpipeline validate fixtures/customers_bad.csv \
    --schema schemas/customers.json --out-dir reports/bad --fail-under 0.95
Validated 10 rows against schema 'customers'.
  valid:   2
  invalid: 8
  errors:  8
[FAIL] pass_rate=20.0% (threshold 95.0%)
exit=1
```

**Artifact verification (counts as expected):**

| Run | total | valid | invalid | clean.csv data rows | rejected.csv data rows | exit |
| --- | --- | --- | --- | --- | --- | --- |
| good | 8 | 8 | 0 | 8 | 0 | 0 (PASS) |
| bad | 10 | 2 | 8 | 2 | 8 | 1 (FAIL) |

The bad run's `report.json` `errors_by_rule` covers **every** rule kind:
`{required:1, type:2, min:1, max:1, enum:1, regex:1, unique:1}`. All four
artifacts (`report.json`, `report.md`, `clean.csv`, `rejected.csv`) were created
in each output dir. **Smoke test passed.**

### 6. What worked well

- **Install was clean and idempotent-aware.** It respected the existing repo and
  `.gitignore`, made a single scoped commit, and printed a clear per-file log.
- **`--non-interactive` did the right thing:** no hangs, sensible defaults, and
  an explicit warning naming the one unresolved placeholder *and* how to fix it
  (`--set GITHUB_OWNER=...`). Excellent operator ergonomics.
- **Templates are high quality.** The PRD and ADR templates have genuinely useful
  inline guidance (hard-required vs. soft fields, "keep open questions
  non-empty"), so authoring real artifacts was fast and unambiguous.
- **`sync-adr-index` is a real, working validation surface.** Marker-fence
  rewriting worked, `--check` gives a CI-friendly drift exit code, and exit-code
  semantics are documented in the script header.
- **Skills are well-specified.** Each `SKILL.md` has structured frontmatter
  (inputs/outputs/next/permission-category) that makes the intended routing
  legible without running anything.
- **`--with-docs` is worth it:** 15 docs including a troubleshooting guide and a
  workflow-control model gave me enough to self-serve.

### 7. Friction / bugs / unclear guidance

1. **`CLAUDE.md` ships with unresolved `{{...}}` mustache blocks.** The install
   log and the template's own preamble claim "a freshly rendered CLAUDE.md never
   carries unresolved `{{PLACEHOLDER}}` syntax," but the rendered file still
   contained multi-line `{{...}}` *guidance* blocks (the "What this is"
   paragraph and the project-structure tree, template lines 15–17 and 63–70).
   These are instructional braces, not single-token placeholders, but they read
   exactly like unfilled template syntax and contradict the stated guarantee.
   A reader can't tell "fill me in" from "rendering bug" without checking docs.
2. **`design/state.md` is not scaffolded, yet `start`/`/next`/`resume` read it.**
   The kit's front-door skill (`start`) says it "reads `design/state.md` (esp.
   the next-action zone)," but a fresh install only creates `design/adr/`. A user
   who runs `/start` first thing hits a missing file. It is *by design* (state.md
   is "filled by prepare-issue/executor/packager"), but nothing in the install
   output or CLAUDE.md tells a day-one user that, so the front door points at a
   file that doesn't exist yet.
3. **`CLAUDE.md` "See also" links to artifacts that don't exist on day one.** It
   links `design/mvp.md`, `design/ai-summary.md`, and `design/build-out-plan.md`
   as if present; all three are missing after a fresh install (they are skill
   outputs). On day one these are dead links.
4. **No top-level "what do I do next" pointer after install.** The installer's
   final line is just `done. target: …`. A one-line "next: run `/start` or fill
   `design/prd.md`" would close the loop between install and first use.
5. **Minor:** the rendered `CLAUDE.md` retains two `_TBD_` tokens *inside the
   explanatory note about `_TBD_`* — harmless, but a naive `grep _TBD_` "is it
   done?" check returns a false positive.

None of these are functional bugs in the installed software — the pipeline and
the one runnable kit surface (`sync-adr-index`) both work. They are
documentation/scaffolding-expectation gaps.

### 8. Severity-ranked recommendations

| # | Severity | Recommendation |
| --- | --- | --- |
| 1 | **High** | Reconcile the "no `{{ }}` after render" guarantee with reality. Either (a) strip/convert the `{{...}}` guidance blocks to plainly-marked TODO comments (e.g. `<!-- TODO: ... -->`) during render, or (b) fix the docs/log to say guidance braces *do* remain and are intentional. The current contradiction is the most confusing thing a new user meets. |
| 2 | **Medium** | Scaffold a minimal `design/state.md` from `state-template.md` at install time (or have `start`/`resume` degrade gracefully with "no state.md yet — run X"). The front-door skill should never point at a missing file. |
| 3 | **Medium** | Make `CLAUDE.md` "See also" links conditional on existence, or annotate them as "(created later by `prd-to-mvp` / `adr-writer`)" so they aren't dead links on day one. |
| 4 | **Low** | Add a final "Next steps" stanza to the installer output (run `/start`, fill `design/prd.md`, set `GITHUB_OWNER`). Cheap, high-value onboarding. |
| 5 | **Low** | Avoid leaving literal `_TBD_` inside the `_TBD_` explainer note, or use a different token there, so `grep _TBD_` completion checks aren't tripped. |

### 9. Final verdict

**GOOD.**

The kit installed cleanly into a real, dependency-free data-pipeline project,
its templates were high quality and directly usable to produce a genuine PRD,
ADR, and state file, and its one runnable validation surface (`sync-adr-index`)
worked correctly with sensible CI exit codes. It falls short of EXCELLENT only
because of day-one onboarding friction: a rendered `CLAUDE.md` that contradicts
its own "no leftover template syntax" guarantee, a front-door skill that reads a
file the installer doesn't create, and several dead "See also" links. All are
documentation/scaffolding gaps, not functional defects, and all are
straightforward to fix.

---

READY_FOR_AGGREGATION
