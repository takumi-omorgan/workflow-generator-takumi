# M0–M5 Evaluation Plan

**Status:** active evaluation plan
**Scope:** every feature shipped in milestones M0 through M5 of the Claude
Code Workflow Kit, plus cross-milestone end-to-end and negative scenarios.
**Audience:** any maintainer or agent who needs to verify the kit still
behaves as designed — before a release, after a refactor, or when accepting
a new contribution.

This document is the **specification for an evaluation suite**, not the
suite itself. It defines *what* to evaluate and *how to decide pass or
fail*. It deliberately does not add new executable tests: most evals reuse
the kit's own `bin/*` validators and offline fixtures, and the few manual
evals are scripted as numbered steps a human (or an agent in interactive
mode) can follow without reading any conversation history.

It is distinct from the retrospective per-milestone notes under
`notes/eval-m*.md` (which record what was checked *during* each milestone's
implementation). This plan is forward-looking and re-runnable: the same
eval IDs should produce the same verdicts on every future commit.

---

## 1. How to read this plan

### 1.1 Eval ID scheme

| Prefix | Meaning |
|---|---|
| `M0-Exx` … `M5-Exx` | A milestone-scoped evaluation run. |
| `E2E-xx` | A cross-milestone end-to-end scenario. |
| `NEG-xx` | A negative / failure-mode evaluation (the kit must *refuse* or *fail loudly*). |

Each eval is written against one template (§1.4). Every eval has an
explicit **PASS gate** and an explicit **FAIL gate** stated as concrete,
observable conditions — usually an exit code, a file's presence/absence, or
a counted property of an artifact. Where a verdict needs human judgement
(prose quality, UX clarity), the eval says so and gives a rubric, not a
vibe.

### 1.2 Automation levels

| Level | Symbol | Meaning |
|---|---|---|
| Automated | `[A]` | Runs as one or more `bin/*` commands; verdict is an exit code or a parsed field. CI-eligible. |
| Scripted-manual | `[SM]` | A fixed sequence of commands a human runs and compares against stated expectations. Reproducible, but the verdict needs a human to read output. |
| Manual | `[M]` | Requires human judgement of prose/UX, or a live external action (GitHub write, real provider call). Not CI-eligible. |

### 1.3 Cadence

| Cadence | When to run |
|---|---|
| **per-PR** | On every pull request and push to `main` (the CI surface; see M4-E07). |
| **pre-release** | Before tagging a release or running `/complete-milestone --release`. |
| **on-change** | When the feature's implementing files change (listed per eval). |
| **quarterly** | Slow-moving manual evals (front-door UX, tutorial timing). |

### 1.4 Per-eval template

Every eval below uses this structure:

- **ID / name**
- **Feature area** — milestone + the specific feature/issue/ADR under test
- **Purpose** — the exact behaviour being evaluated
- **Setup / inputs / fixtures**
- **Execution** — exact command(s) or numbered steps
- **Observe** — artifacts/output to capture
- **PASS** — explicit success gate
- **FAIL** — explicit failure gate
- **Automation / cadence / risk** — level, when to run, what could make the eval itself misleading

---

## 2. Test environment and shared setup

These preconditions are assumed by every `[A]` and `[SM]` eval unless an
eval overrides them.

### 2.1 Tooling

| Tool | Required by | Check |
|---|---|---|
| `bash` (4+) | all `bin/*` | `bash --version` |
| `python3` (3.8+) | validators, review helpers | `python3 --version` |
| `jq` | JSON envelope inspection | `jq --version` |
| `gh` (authenticated) | only live GitHub evals (M2 prepare-issue live, M5 live publish, E2E live) | `gh auth status` |

All offline evals (the large majority) must pass **without `gh` and without
any provider API key**. An eval that silently degrades when `gh` is missing
is a defect in the eval — state the degraded behaviour explicitly.

### 2.2 Working directory

Run from the **kit repository root** unless an eval says otherwise. The kit
dogfoods its own skills via `~/dotfiles/claude-config/bin/link-skills`
(symlinks `skills/<name>/` into the gitignored `.claude/skills/`); slash-command
evals assume that link has been run once.

### 2.3 Throwaway target project (for installer / front-door evals)

Several evals install the kit into a fresh target. Standard setup:

```bash
TARGET="$(mktemp -d)/demo"
bin/install-workflow-kit --target="$TARGET" --project-name=demo --non-interactive
```

Tear down by deleting the temp dir. **Never** run installer evals against
the kit repo itself.

### 2.4 Shared offline fixtures

| Fixture set | Path | Used by |
|---|---|---|
| AI-review diffs/responses/expectations | `ai-review/eval/fixtures/{docs-only,simple-bugfix,risky-change,large-noisy}/` | M5 evals, NEG-06 |
| Carry-forward producer blocks | `notes/eval-issue-*.md` (`### design-questions` blocks) | M4-E02 |
| Provider config template | `ai-review/config.example.json` | M5-E01 |

Evals that need a *malformed* fixture (negative evals) create it in a temp
dir — they must never mutate a tracked fixture.

### 2.5 Exit-code contract (kit-wide)

Every `bin/*` script that sources `bin/lib/json-envelope.sh` obeys this
contract (M2 Issue 8). Many PASS/FAIL gates below are stated directly in
these codes:

| Code | Meaning |
|---|---|
| `0` | success / in-sync / conforms / preview shown |
| `1` | domain failure (drift, non-conformant data, duplicate, validation fail) |
| `2` | invocation error (bad flags, unreadable input, not at kit root) |
| `3` | auth / service failure (missing credential, `gh` missing, provider call failed) |
| `4` | user cancellation / approval failure (e.g. wrong `--confirm` token) |

`bin/check-plan` is the documented grandfather exception (it predates the
envelope; it uses `0` pass / `1` fail / `2` invocation only).

---

## 3. M0 — Foundation, kit integrity, baseline

**What M0 shipped (PR #2, issues M0-1…M0-5):** a baseline health and drift
audit establishing the invariants the kit must continuously satisfy — repo
structure, `kit.json` validity, syntax cleanliness, link integrity, ADR
index sync, installer correctness and idempotency, and skill-metadata
budgets. M0 produced no new runtime feature; it produced the *definition of
healthy*. These evals operationalise that definition as standing checks.

Key artifacts: `notes/baseline-health.md`, `notes/dogfood-baseline-report.md`,
`notes/installer-idempotency-audit.md`, `docs/repo-structure.md`.

---

### M0-E01 — Repository structure integrity
- **Feature area:** M0 baseline (repo layout, `docs/repo-structure.md`); ADR-045 (lowercase `design/`).
- **Purpose:** the kit's canonical directory layout (kit-source vs.
  target-project surfaces) is intact: `skills/`, `bin/`, `bin/lib/`,
  `templates/`, `docs/`, `design/adr/`, `schemas/`, `ai-review/` all exist
  with their expected contents.
- **Setup:** kit root, clean tree.
- **Execution:**
  ```bash
  for d in skills bin bin/lib templates docs design/adr schemas ai-review prompts; do
    test -d "$d" || echo "MISSING: $d"
  done
  test -f kit.json && test -f CLAUDE.md && test -f README.md || echo "MISSING top-level file"
  ```
- **Observe:** any `MISSING:` line.
- **PASS:** command prints nothing; every expected directory and top-level
  file present; `design/` is lowercase (no `Design/` directory exists).
- **FAIL:** any `MISSING:` line, or a `Design/` (capitalised) directory
  exists (ADR-045 regression).
- **Automation:** `[A]` · **Cadence:** per-PR · **Risk:** the directory
  list is hand-maintained here — update it when the kit adds a top-level
  surface, or this eval gives false confidence.

### M0-E02 — `kit.json` is well-formed JSON
- **Feature area:** M0 baseline; M2 machine-readable contract.
- **Purpose:** the machine-readable index parses as JSON (the precondition
  for every agent that reads the contract).
- **Execution:** `python3 -c "import json; json.load(open('kit.json'))"`
- **PASS:** exit 0, no traceback.
- **FAIL:** non-zero exit / JSON decode error.
- **Automation:** `[A]` (already a CI step) · **Cadence:** per-PR · **Risk:** none.

### M0-E03 — Shell and Python syntax cleanliness
- **Feature area:** M0 baseline (syntax drift).
- **Purpose:** no `bin/*` shell script or Python helper has a syntax error.
- **Execution:**
  ```bash
  rc=0
  for f in bin/* bin/lib/*; do
    [ -f "$f" ] || continue; case "$f" in *.md) continue ;; esac
    if head -1 "$f" | grep -q '^#!.*sh'; then bash -n "$f" || rc=1; fi
  done
  for p in bin/lib/*.py; do python3 -c "import ast,sys; ast.parse(open('$p').read())" || rc=1; done
  echo "rc=$rc"
  ```
- **PASS:** `rc=0`.
- **FAIL:** `rc=1` (any syntax error).
- **Automation:** `[A]` (CI runs the bash half) · **Cadence:** per-PR · **Risk:** none.

### M0-E04 — Internal markdown link integrity
- **Feature area:** M0-4 (dead-link fixes); standing invariant.
- **Purpose:** no tracked markdown file links to a relative path that does
  not exist (the M0 audit fixed two such dead links).
- **Setup:** kit root.
- **Execution:** for every `*.md`, extract `](relative/path)` targets that
  are not URLs/anchors and assert the file exists. (Reference resolver: a
  short `python3`/`grep` script; one is described in
  `notes/baseline-health.md`.)
- **Observe:** list of `file:line -> missing-target`.
- **PASS:** zero missing internal targets.
- **FAIL:** ≥1 link points to a non-existent file.
- **Automation:** `[A]` · **Cadence:** per-PR · **Risk:** anchor-only and
  external links must be excluded or the eval produces noise; document the
  exclusion rule in the resolver.

### M0-E05 — ADR index is in sync
- **Feature area:** M0 baseline; ADR-023 (auto-sync ADR index).
- **Purpose:** the generated index table in `design/adr/README.md` matches
  the ADR files on disk (titles, statuses, the marker-fenced table).
- **Execution:** `bin/sync-adr-index --check`
- **PASS:** exit 0 (index already in sync).
- **FAIL:** exit 1 (index stale — an ADR was added/retitled/status-changed
  without re-running the sync).
- **Automation:** `[A]` · **Cadence:** per-PR + on-change (any `design/adr/*` edit) · **Risk:** none.

### M0-E06 — Design-directory casing on install
- **Feature area:** M0-3 / M1 Issue 5 (the `git add Design` vs `design/` bug); ADR-045.
- **Purpose:** after a fresh install + initial commit, `design/adr/README.md`
  is **tracked** (the historical defect left it untracked on case-sensitive
  filesystems because the installer staged `Design` not `design`).
- **Setup:** §2.3 throwaway target.
- **Execution:**
  ```bash
  cd "$TARGET" && git status --porcelain design/ ; git ls-files design/adr/README.md
  ```
- **PASS:** `git ls-files` lists `design/adr/README.md`; `git status` shows
  no untracked file under `design/`.
- **FAIL:** `design/adr/README.md` is absent from `git ls-files`, or any
  `design/` file is untracked after the installer's initial commit.
- **Automation:** `[SM]` · **Cadence:** pre-release + on-change (`bin/install-workflow-kit`) · **Risk:** macOS is case-insensitive; run at least once on a case-sensitive FS (Linux/CI) to catch the real regression.

### M0-E07 — Installer fresh-install smoke test
- **Feature area:** M0-3 (installer correctness); ADR-009.
- **Purpose:** a clean install into an empty target completes and produces
  the expected surfaces.
- **Setup:** §2.3.
- **Execution:** run the install; then in `$TARGET`:
  ```bash
  ls .claude/skills | wc -l ; test -f CLAUDE.md ; test -d design/adr ; test -f .gitignore
  ```
- **Observe:** skill count, presence of generated files, installer exit code.
- **PASS:** installer exits 0; `.claude/skills/` is non-empty; `CLAUDE.md`,
  `design/adr/`, `.gitignore` all present.
- **FAIL:** installer non-zero exit, or any expected surface missing.
- **Automation:** `[SM]` · **Cadence:** pre-release + on-change (installer) · **Risk:** depends on the host filesystem; pair with M0-E06.

### M0-E08 — Installer idempotency
- **Feature area:** M0-3 (`notes/installer-idempotency-audit.md`).
- **Purpose:** re-running the installer with `--force` over an existing
  install produces **no unexpected diffs** (it is safe to re-run).
- **Setup:** §2.3 (already installed once).
- **Execution:**
  ```bash
  cd "$TARGET" && git add -A && git commit -qm baseline
  bin/install-workflow-kit --target="$TARGET" --force --non-interactive
  git status --porcelain
  ```
- **Observe:** the porcelain diff after the second run.
- **PASS:** `git status --porcelain` is empty (or shows only documented,
  intentional refreshes — list them in the eval run log).
- **FAIL:** the rerun introduces uncommitted changes that are not on the
  documented allow-list (e.g. a placeholder re-expansion, a reshuffled file).
- **Automation:** `[SM]` · **Cadence:** pre-release + on-change (installer) · **Risk:** the "documented allow-list" must be kept current; an empty allow-list is the safest target.

### M0-E09 — Skill-metadata budgets
- **Feature area:** M0-2 (skill metadata / handoff drift audit, `notes/skills-audit-2026-05-07/`).
- **Purpose:** every `skills/*/SKILL.md` stays within the audited metric
  budgets (description length, body size tier, handoff fan-out) — no skill
  has silently bloated.
- **Setup:** the audit harness under `notes/skills-audit-2026-05-07/`.
- **Execution:** `python3 notes/skills-audit-2026-05-07/audit.py` (or its
  documented entry point).
- **Observe:** per-skill metric table; any over-budget flag.
- **PASS:** zero skills flagged over budget.
- **FAIL:** ≥1 skill exceeds a documented budget without an accompanying
  sidecar/justification.
- **Automation:** `[A]` · **Cadence:** on-change (any `skills/*/SKILL.md`) · **Risk:** budgets are conventions, not hard limits — treat a fail as "review needed," and update budgets via the audit, not ad hoc.

---

## 4. M1 — Front door, PRD intake, and the first-PR happy path

**What M1 shipped (PR #1, issues 1–5):** front-door simplification — a
README with a single recommended install path, a "first PR in ~15 minutes"
tutorial (`docs/tutorial.md`), a symptom-organised troubleshooting page,
placeholder reduction in the generated `CLAUDE.md`, and the `Design`→`design`
casing fix. The tutorial's happy path *is* the PRD-intake-to-first-PR flow
(`/prd-normalizer` → `/prd-to-mvp` → `/issue-planner` →
`/claude-issue-executor` → `/pr-review-packager`), so these evals cover both
the front-door UX and the PRD-intake/planning skills it routes through
(ADR-003 three intake paths).

---

### M1-E01 — README presents one install path
- **Feature area:** M1 Issue 1.
- **Purpose:** the README's happy path offers exactly one recommended
  install command and does not bury the reader in alternative paths or ADR
  citations.
- **Execution:** read `README.md`; locate the Quick Start.
- **PASS:** Quick Start contains a single recommended bootstrap/install
  command; no competing "or you can also…" install paths in the happy path;
  no ADR-NNN citations in the Quick Start.
- **FAIL:** more than one recommended install path in the happy path, or ADR
  citations reintroduced into the front door.
- **Automation:** `[M]` (prose judgement) · **Cadence:** quarterly + on-change (`README.md`) · **Risk:** subjective; the gate ("one recommended command") is the objective anchor.

### M1-E02 — Tutorial happy path completes end-to-end
- **Feature area:** M1 Issue 2 (`docs/tutorial.md`).
- **Purpose:** a new user following the tutorial verbatim reaches a first PR
  using the five documented slash commands, with no missing/renamed step.
- **Setup:** §2.3 throwaway target with a sample PRD; `gh` authenticated
  (this eval exercises the live GitHub flow) on a scratch repo.
- **Execution:** follow `docs/tutorial.md` step by step:
  `/prd-normalizer` → `/prd-to-mvp` → `/issue-planner` →
  `/claude-issue-executor` → `/pr-review-packager`.
- **Observe:** wall-clock time, any step where a command name/flag in the
  doc no longer matches the shipped skill, any dead checkpoint.
- **PASS:** all five commands exist and run in order; the flow ends with an
  open PR; every checkpoint in the doc is reachable. (Target ≤30 min, the
  tutorial demonstrates ~15.)
- **FAIL:** any documented command/skill is missing or renamed; the flow
  cannot reach a PR following the doc as written.
- **Automation:** `[M]` · **Cadence:** quarterly + on-change (tutorial or any of the 5 skills) · **Risk:** consumes a scratch GitHub repo; use a throwaway, never a real project.

### M1-E03 — Generated `CLAUDE.md` placeholder reduction
- **Feature area:** M1 Issue 3 (placeholder reduction; `_TBD_` for unknowns).
- **Purpose:** a freshly generated target `CLAUDE.md` contains only a small
  number of genuine unknowns; remaining optional fields render as `_TBD_`,
  not raw `{{…}}` tokens.
- **Setup:** §2.3 throwaway target.
- **Execution:**
  ```bash
  cd "$TARGET" && grep -c '{{' CLAUDE.md ; grep -c '_TBD_' CLAUDE.md
  ```
- **Observe:** count of unresolved `{{…}}` tokens.
- **PASS:** zero raw `{{…}}` tokens remain after install (the M0 baseline
  measured 25 before this work; the target is 0 unresolved, unknowns shown
  as `_TBD_`).
- **FAIL:** ≥1 raw `{{…}}` token survives into the generated `CLAUDE.md`.
- **Automation:** `[SM]` · **Cadence:** pre-release + on-change (`templates/claude-md-template.md`, installer) · **Risk:** the threshold is "0 raw tokens"; if a deliberate token is intentionally left for the user, document it and adjust the gate.

### M1-E04 — Troubleshooting covers the known symptoms
- **Feature area:** M1 Issue 4 (`docs/troubleshooting.md`, symptom-organised).
- **Purpose:** the page is organised by observable symptom and covers the
  baseline-known failure modes.
- **Execution:** confirm sections exist for, at minimum: slash command not
  autocompleting, skills not discovered, GitHub project creation failure,
  stale prompts, installer rerun changing files, unresolved placeholders.
- **PASS:** every listed symptom has a section with a concrete remedy;
  sections are titled by symptom (what the user *sees*), not by cause.
- **FAIL:** a known symptom from the baseline is undocumented, or the page
  reverts to cause-first organisation.
- **Automation:** `[M]` · **Cadence:** quarterly + on-change · **Risk:** the symptom list grows; treat new troubleshooting entries as additive.

### M1-E05 — PRD intake produces expected artifacts (three paths)
- **Feature area:** ADR-003 (three PRD intake paths); skills `idea-to-prd`,
  `prd-normalizer`, `prd-to-mvp`.
- **Purpose:** each supported intake path yields the expected `design/*`
  artifact a downstream skill can consume.
- **Setup:** §2.3 target; a one-paragraph idea and a rough draft PRD as inputs.
- **Execution (per path):**
  1. Raw idea → `/idea-to-prd` → expect `design/prd.md`.
  2. Existing rough PRD → `/prd-normalizer` → expect a normalised PRD artifact.
  3. Normalised PRD → `/prd-to-mvp` → expect `design/mvp.md` / build-out plan.
- **Observe:** artifact presence and that the next skill's documented input
  exists.
- **PASS:** each path writes its documented output artifact under `design/`;
  the artifact contains the template's required sections.
- **FAIL:** a path produces no artifact, or an artifact missing required
  sections such that the next skill cannot consume it.
- **Automation:** `[M]` (skills are agent-driven) · **Cadence:** quarterly + on-change (intake skills) · **Risk:** output quality is model-dependent; gate on *structure/presence*, not prose quality.

### M1-E06 — Planning flow yields a backlog
- **Feature area:** planning skills (`planning`, `issue-planner`); ADR-006.
- **Purpose:** from an MVP/build-out plan, the planning flow yields a
  decomposed backlog ready for issue creation.
- **Setup:** a `design/mvp.md` / build-out plan from M1-E05.
- **Execution:** `/planning` (writes `design/planning.md`) then `/issue-planner`.
- **PASS:** `design/planning.md` exists with decomposition + sequencing;
  `issue-planner` proposes a concrete, ordered issue list mapping to the plan.
- **FAIL:** no planning artifact, or the proposed issues do not trace to the
  plan's phases.
- **Automation:** `[M]` · **Cadence:** quarterly + on-change · **Risk:** model-dependent; gate on traceability not wording.

---

## 5. M2 — Machine-readable agent contract

**What M2 shipped (PR #3, issues 6–10):** the `kit.json` index, structured
skill frontmatter, the standard JSON envelope + exit-code convention
(`bin/lib/json-envelope.sh`), the read-only `bin/prepare-issue --format json`
surface, and centralised GitHub credential-scope docs — tied together by
`docs/agent-contract.md` and governed by ADR-047.

---

### M2-E01 — `kit.json` ↔ skill frontmatter agreement
- **Feature area:** M2 Issue 6/7; ADR-047. Validator: `bin/validate-kit-json`.
- **Purpose:** every skill in `skills/` appears in `kit.json` with matching
  name, permission category, and the `next` handoff targets all resolve.
- **Execution:** `bin/validate-kit-json`
- **PASS:** exit 0 (index and frontmatter in sync).
- **FAIL:** exit 1 (drift: a skill missing from the index, a name/category
  mismatch, or a dangling `next` target). Exit 2 = invocation error (treat
  as eval-setup bug).
- **Automation:** `[A]` (CI step) · **Cadence:** per-PR + on-change (`skills/*`, `kit.json`) · **Risk:** none.

### M2-E02 — Every skill carries complete structured frontmatter
- **Feature area:** M2 Issue 7.
- **Purpose:** each `skills/*/SKILL.md` declares `name`, `description`,
  `permission-category`, `inputs`, `outputs`, and `next`.
- **Execution:** for each `SKILL.md`, parse the YAML frontmatter and assert
  the six keys are present and non-empty.
- **PASS:** all skills have all six keys populated.
- **FAIL:** any skill missing a required frontmatter key.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change · **Risk:** overlaps M2-E01's name/category check; this one additionally covers `inputs`/`outputs` shape.

### M2-E03 — JSON envelope + exit-code conformance
- **Feature area:** M2 Issue 8 (`bin/lib/json-envelope.sh`).
- **Purpose:** each envelope-using `bin/*` script emits a well-formed
  envelope (`{skill, version, status, outputs, next, errors}`) under
  `--format json` and uses the standard exit codes (§2.5).
- **Setup:** run each script in a safe, read-only or `--mock`/`--dry-run` mode.
- **Execution (representative, offline):**
  ```bash
  bin/validate-kit-json --format json | jq -e '.skill and .status'
  bin/check-consistency --format json | jq -e '.skill and .status'
  bin/review-eval --format json       | jq -e '.skill and .status'
  ```
- **Observe:** JSON validity and presence of required envelope keys; exit codes.
- **PASS:** every tested script emits valid JSON with the required envelope
  keys and returns a documented exit code for the scenario.
- **FAIL:** malformed JSON, missing envelope key, or an undocumented exit
  code. (`bin/check-plan` is exempt — grandfathered shape.)
- **Automation:** `[A]` · **Cadence:** per-PR + on-change (`bin/lib/json-envelope.sh`, any `bin/*`) · **Risk:** keep the tested-script list current as `bin/` grows.

### M2-E04 — `bin/prepare-issue --format json` is read-only and correct
- **Feature area:** M2 Issue 9.
- **Purpose:** the programmatic issue-analysis surface emits the documented
  fields (`issue`, `promptPath`, `promptExists`, `stale`, `adrReferences`,
  `gaps`, `next`) and **writes nothing**.
- **Setup:** kit root; pick an issue number with a known prompt under `prompts/`.
- **Execution:**
  ```bash
  git stash list >/tmp/before
  bin/prepare-issue --issue <N> --format json | jq -e '.outputs.promptPath, .outputs.stale, .next'
  git status --porcelain   # must be unchanged
  ```
- **PASS:** exit 0; JSON contains the documented fields; `git status` is
  unchanged (no files written). When `gh` is unavailable the script exits 3
  with a setup message (not a traceback).
- **FAIL:** missing fields, any file written/modified, or a stack trace on
  missing `gh`.
- **Automation:** `[A]` (offline field check) / `[SM]` (live `gh` path) · **Cadence:** per-PR + on-change · **Risk:** the live path needs `gh`; run the field-shape check offline against a fixture prompt.

### M2-E05 — Handoff graph is closed
- **Feature area:** M2 Issue 6/7; M3 verb layer.
- **Purpose:** every `next` target named in any skill frontmatter / `kit.json`
  resolves to a real skill (no dangling handoff).
- **Execution:** `bin/validate-kit-json` (covers `next` resolution) +
  `bin/check-consistency` C2 (verb-layer → underlying skills).
- **PASS:** both exit 0.
- **FAIL:** either reports a dangling target / undefined underlying skill (exit 1).
- **Automation:** `[A]` · **Cadence:** per-PR · **Risk:** none.

### M2-E06 — Agent-contract entry point and credential docs are complete
- **Feature area:** M2 Issue 10 (`docs/github-setup.md`); `docs/agent-contract.md`.
- **Purpose:** an agent has a single documented entry point describing the
  four contract parts + the validator + `bin/prepare-issue`, and the GitHub
  credential scopes (`repo`, `project`, `workflow`) are documented in one place.
- **Execution:** read `docs/agent-contract.md` and `docs/github-setup.md`.
- **PASS:** `agent-contract.md` references `kit.json`, frontmatter, the JSON
  envelope, and `bin/prepare-issue`; `github-setup.md` lists the required
  `gh` scopes and a preflight checklist.
- **FAIL:** the contract doc omits one of the four parts, or the scope list
  is absent/incomplete.
- **Automation:** `[M]` · **Cadence:** quarterly + on-change · **Risk:** prose; gate on the enumerated items.

---

## 6. M3 — Unified workflow control

**What M3 shipped (PR #4, issues 11–15, 21):** a single canonical approval
gate, three operating modes (interactive/assisted/autonomous) crossed with
the three permission categories, the `/start` router, a human-facing verb
layer over the underlying skills, a structured `next-action` zone in
`design/state.md`, `/pause` + `/resume` session continuity, the
programmatic `bin/check-plan` surface (ADR-043), granularity control
(ADR-036), the milestone lifecycle skills (ADR-037), and the follow-up PRD
workflow (`/feature-prd`, ADR-049). Governing ADR: ADR-048.

---

### M3-E01 — Approval-gate token set is deterministic
- **Feature area:** M3 Issue 11; ADR-048; `docs/workflow-control.md`.
- **Purpose:** the approval gate proceeds only on the closed, documented set
  of tokens (`approve`, `approved`, `yes`, `go`, `proceed`, `lgtm`, matched
  case-insensitively) and not on near-misses ("maybe", "sounds good").
- **Setup:** read `docs/workflow-control.md` §approval gate.
- **Execution:** confirm the documented token set; in a scripted skill run,
  supply (a) an exact token and (b) a near-miss; observe behaviour.
- **PASS:** an exact token (any case) advances; a non-token reply does not
  advance — the agent re-prompts or holds.
- **FAIL:** a non-token phrase advances a cat-2/cat-3 action, or a documented
  token fails to advance.
- **Automation:** `[SM]` (interactive skill behaviour) · **Cadence:** on-change (`docs/workflow-control.md`, skill plan-mode files) · **Risk:** behavioural; the deterministic token list is the objective anchor.

### M3-E02 — Operating-mode × permission-category matrix holds
- **Feature area:** M3 Issue 15; ADR-048; ADR-041 (permission contract).
- **Purpose:** no mode relaxes a cat-3 action's approval; `assisted` and
  `autonomous` still emit the mandatory cat-2 acknowledgement line.
- **Execution:** for each mode, exercise a cat-1, cat-2, and cat-3 action and
  observe the gate.
- **PASS:** cat-3 always requires explicit approval in every mode; cat-2 in
  assisted/autonomous emits the acknowledgement line; cat-1 may proceed
  without approval.
- **FAIL:** any mode auto-executes a cat-3 action, or omits the cat-2
  acknowledgement where required.
- **Automation:** `[SM]` · **Cadence:** on-change · **Risk:** behavioural; cross-check against the ADR-048 matrix table.

### M3-E03 — `/start` router recommends the correct next action
- **Feature area:** M3 Issue 12 (`skills/start`).
- **Purpose:** `/start` reads `design/state.md` (and PRD/plan/branch state)
  and recommends the right next skill; it never *invokes* a cat-3 skill, it
  names the approval gate instead.
- **Setup:** construct target states: (a) no PRD, (b) PRD but no plan, (c)
  open in-flight branch, (d) populated `next-action` zone.
- **Execution:** run `/start` in each state.
- **PASS:** (a)→recommends PRD intake; (b)→recommends planning/issue
  decomposition; (c)→recommends resuming the in-flight work; (d)→proposes
  exactly the `next-action` zone's skill. Cat-3 recommendations are named,
  not auto-invoked.
- **FAIL:** wrong recommendation for a state, or `/start` directly invokes a
  cat-3 skill.
- **Automation:** `[SM]` · **Cadence:** on-change (`skills/start`) · **Risk:** state fixtures must be realistic; reuse `design/state.md` zone markers.

### M3-E04 — Verb layer maps to real underlying skills
- **Feature area:** M3 Issue 13; `docs/workflow-control.md` §verb layer.
- **Purpose:** every human-facing verb (`/work`, `/ship`, `/decide`,
  `/backlog`, `/finish-milestone`, …) maps to underlying skills that exist
  in `kit.json`.
- **Execution:** `bin/check-consistency` (C2 enforces this).
- **PASS:** exit 0 — every verb's underlying skill resolves.
- **FAIL:** exit 1 — a verb references an undefined skill.
- **Automation:** `[A]` · **Cadence:** per-PR · **Risk:** none.

### M3-E05 — `state.md` `next-action` zone schema
- **Feature area:** M3 Issue 14; ADR-035; `templates/state-template.md`.
- **Purpose:** the `next-action` zone is a marker-fenced YAML block with
  fields `skill`, `args`, `preconditions`, `blocked-by`.
- **Setup:** `design/state.md` (kit's own) and `templates/state-template.md`.
- **Execution:** parse the `<!-- state:next-action:start -->`…`:end` block as YAML.
- **PASS:** the block parses; contains `skill`, `args`, `preconditions`
  (list), `blocked-by`; all six state zones (phase, in-flight, recent,
  blockers, continue-here, next-action) are present and marker-fenced.
- **FAIL:** the zone is missing a field, is not valid YAML, or a marker
  fence is malformed/missing.
- **Automation:** `[A]` · **Cadence:** on-change (`templates/state-template.md`, `design/state.md`) · **Risk:** none.

### M3-E06 — `/pause` → `/resume` round-trip
- **Feature area:** M3 (ADR-035); `skills/pause`, `skills/resume`.
- **Purpose:** `/pause` refreshes the state zones; `/resume` reconstructs an
  accurate session brief from them (falling back to `gh` if state is
  absent/suspect).
- **Setup:** a target with a known in-flight issue + recent PRs.
- **Execution:** `/pause` → inspect `design/state.md` → start a fresh session
  → `/resume`.
- **PASS:** `/pause` updates the marker-fenced zones to reflect current
  state; `/resume`'s brief names the correct phase, in-flight issue, recent
  PRs, blockers, and next action. With `state.md` deleted, `/resume` still
  produces a brief from `gh`.
- **FAIL:** the brief omits/contradicts the in-flight issue, or `/resume`
  errors when `state.md` is absent.
- **Automation:** `[SM]` · **Cadence:** on-change · **Risk:** the `gh` fallback path needs auth; the primary path is offline.

### M3-E07 — `bin/check-plan --criteria-set adr` pass/fail
- **Feature area:** M3 Issue 11; ADR-043; `bin/check-plan`.
- **Purpose:** the ADR criteria set passes a well-formed ADR and fails one
  missing required sections.
- **Setup:** a known-good ADR (e.g. `design/adr/adr-050-*.md`) and a
  deliberately incomplete ADR in a temp file.
- **Execution:**
  ```bash
  bin/check-plan --criteria-set adr --input design/adr/adr-050-reliability-validation-self-test.md ; echo "good=$?"
  bin/check-plan --criteria-set adr --input /tmp/bad-adr.md ; echo "bad=$?"
  ```
- **PASS:** `good=0` and `bad=1` (note: `check-plan` uses 0 pass / 1 fail /
  2 invocation — the grandfather exception).
- **FAIL:** the good ADR fails, or the incomplete ADR passes, or either
  returns exit 2 (invocation error — eval setup bug).
- **Automation:** `[A]` · **Cadence:** per-PR + on-change (`bin/check-plan`, `bin/lib/check-plan-eval.sh`, ADR criteria) · **Risk:** the "bad" fixture must omit a genuinely required section.

### M3-E08 — `bin/check-plan --criteria-set prompt` pass/fail
- **Feature area:** M3 Issue 11; ADR-043.
- **Purpose:** the prompt criteria set passes a complete issue prompt and
  fails an incomplete one.
- **Execution:** as M3-E07 but `--criteria-set prompt` against a
  `prompts/issue-*.md` (good) and a stripped temp prompt (bad). Add
  `--format json` to confirm the (legacy) machine output is parseable.
- **PASS:** good prompt → 0, bad prompt → 1.
- **FAIL:** good → non-zero, or bad → 0.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change · **Risk:** same as M3-E07.

### M3-E09 — Criteria-drift detection
- **Feature area:** M3 (ADR-043); `bin/check-plan-criteria-drift`.
- **Purpose:** the drift detector flags when a criteria template is newer
  than its criteria definition (the two have diverged).
- **Execution:** `bin/check-plan-criteria-drift --check` on the clean tree;
  then `touch` a criteria template to make it newer and re-run.
- **PASS:** clean tree → exit 0; after touching the template → exit 1.
- **FAIL:** drift not detected after the template is made newer, or a false
  positive on the clean tree.
- **Automation:** `[A]` · **Cadence:** per-PR · **Risk:** mtime-based — the
  touch step must actually change mtime; restore mtime after the eval.

### M3-E10 — Granularity control bands
- **Feature area:** M3 (ADR-036); `--granularity` on `prd-to-mvp` / `planning`.
- **Purpose:** the granularity knob changes phase count within the
  documented bands (coarse 3–5, standard 5–8, fine 8–12) and records the
  chosen band for re-run consistency.
- **Setup:** one MVP/build-out plan input.
- **Execution:** run `/planning --granularity coarse|standard|fine`; count
  phases in each output.
- **PASS:** coarse ∈ [3,5], standard ∈ [5,8], fine ∈ [8,12]; the chosen band
  is recorded in the plan metadata.
- **FAIL:** a band produces a phase count outside its range, or the band
  isn't recorded.
- **Automation:** `[SM]` · **Cadence:** on-change (planning skills) · **Risk:** model-dependent; the bands are tolerances, judge against the range.

### M3-E11 — Milestone lifecycle chain
- **Feature area:** M3 (ADR-037); `audit-milestone`, `milestone-summary`, `complete-milestone`.
- **Purpose:** the lifecycle skills chain correctly: audit gates on exit
  criteria, summary writes the milestone doc, complete closes the GitHub
  milestone (cat-3, only on approval).
- **Setup:** a milestone with a known mix of open/closed issues; use
  `--dry-run` to avoid live GitHub writes where supported.
- **Execution:** `/audit-milestone <m>` → `/milestone-summary <m> --dry-run`
  → `/complete-milestone <m> --dry-run`.
- **PASS:** audit reports pass only when all issues closed + ADRs linked +
  exit criteria met; `milestone-summary` (dry-run) shows the doc it *would*
  write to `design/milestones/`; `complete-milestone --dry-run` describes
  the GitHub close without performing it.
- **FAIL:** audit passes with open issues, summary writes nothing/incomplete,
  or `--dry-run` performs a live GitHub mutation.
- **Automation:** `[SM]` · **Cadence:** pre-release + on-change · **Risk:** `complete-milestone` is cat-3 — only the `--dry-run` path is safe to run unattended.

### M3-E12 — Follow-up PRD workflow
- **Feature area:** M3 Issue 21 (ADR-049); `skills/feature-prd`; `design/prd-addenda/`.
- **Purpose:** `/feature` drafts a numbered addendum under
  `design/prd-addenda/NNN-*.md` from the template, without rewriting the
  original PRD.
- **Setup:** a target with `design/prd.md` and zero or more existing addenda.
- **Execution:** `/feature "add X capability"`; inspect the new addendum.
- **PASS:** a new `design/prd-addenda/NNN-*.md` is created with the next
  sequential number; it contains the template sections (Context, Problem,
  Goals, Non-goals, What changes, What does not change, Affected assumptions,
  ADR impact, …); `design/prd.md` is unchanged.
- **FAIL:** the original PRD is modified, the numbering collides/skips, or
  required sections are missing. (Reference real example:
  `design/prd-addenda/001-ai-pr-review.md`.)
- **Automation:** `[SM]` · **Cadence:** on-change (`skills/feature-prd`, template) · **Risk:** model-dependent prose; gate on file path, numbering, and section presence.

---

## 7. M4 — Reliability, validation, receipts, state caps, self-test

**What M4 shipped (PR #5, issues 16–20, ADR-050):** the canonical
carry-forward schema (`schemas/design-questions.v1.yaml`) and its validator
(`bin/validate-carry-forward`), the idempotency receipts system
(`docs/receipts.md`, `schemas/receipt.v1.yaml`, `bin/write-receipt`), the
consistency checker (`bin/check-consistency`, C1–C5), the state-cap guard
(`bin/check-state-cap`), the workflow self-test (`bin/self-test`), and the
CI wiring (`.github/workflows/kit-checks.yml`).

---

### M4-E01 — Self-test is green
- **Feature area:** M4 Issue 19; `bin/self-test`.
- **Purpose:** the non-mutating self-test surface (all read-only validators +
  `bash -n` + tool presence + throwaway stub regressions) passes.
- **Execution:** `bin/self-test` (and `bin/self-test --format json` to inspect steps).
- **Observe:** step count, pass count, friction list, elapsed seconds.
- **PASS:** exit 0; text reads `self-test: ok …` or `degraded …` (degraded =
  only optional tools like `gh` missing); zero friction entries.
- **FAIL:** exit 1 (`FAIL` with a friction list — a step returned an
  unexpected exit), or exit 2 (not at kit root / bad flags).
- **Automation:** `[A]` (CI step) · **Cadence:** per-PR + pre-release · **Risk:** `degraded` is a pass — don't treat optional-tool absence as failure.

### M4-E02 — Carry-forward validator: conformant and non-conformant
- **Feature area:** M4 Issues 16/17; `schemas/design-questions.v1.yaml`, `bin/validate-carry-forward`.
- **Purpose:** the validator passes well-formed `### design-questions`
  blocks and fails ones violating the schema (missing required field, bad
  `target-issue` pattern, forbidden extra field).
- **Setup:** the tracked `notes/eval-issue-*.md` blocks (conformant); a temp
  file with a deliberately broken block (non-conformant).
- **Execution:**
  ```bash
  bin/validate-carry-forward ; echo "tracked=$?"
  bin/validate-carry-forward --file /tmp/bad-block.md ; echo "bad=$?"
  ```
- **PASS:** `tracked=0` and `bad=1`.
- **FAIL:** tracked blocks fail (0 expected), or the broken block passes
  (1 expected), or exit 2 (invocation error).
- **Automation:** `[A]` (tracked half is a CI step) · **Cadence:** per-PR + on-change (schema, validator) · **Risk:** the bad fixture must violate a rule the schema actually enforces.

### M4-E03 — Receipt write/find round-trip
- **Feature area:** M4 Issue 18; `bin/write-receipt`, `schemas/receipt.v1.yaml`.
- **Purpose:** a receipt can be written and then found by key; a non-existent
  key reports not-found; the written file conforms to the receipt schema.
- **Setup:** a temp receipts dir: `RDIR="$(mktemp -d)"`.
- **Execution:**
  ```bash
  bin/write-receipt --skill demo --key k1 --status completed --dir "$RDIR" ; echo "write=$?"
  bin/write-receipt --find --skill demo --key k1 --dir "$RDIR" ; echo "found=$?"
  bin/write-receipt --find --skill demo --key nope --dir "$RDIR" ; echo "missing=$?"
  ```
- **Observe:** the written `.json` file's fields.
- **PASS:** `write=0`, `found=0`, `missing=1`; the written file has the
  required schema fields (`schema`, `version`, `skill`, `key`, `status`,
  `timestamp`).
- **FAIL:** write fails, an existing receipt isn't found, a missing key
  returns 0, or the file omits a required field.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change (`bin/write-receipt`, schema) · **Risk:** always use a temp `--dir`; never write into the repo's `.claude/receipts/`.

### M4-E04 — Consistency checker C1–C5
- **Feature area:** M4 Issue 20; `bin/check-consistency`.
- **Purpose:** doc↔metadata consistency holds across all five checks:
  C1 skills.md↔kit.json, C2 verb layer→skills, C3 bin registry integrity,
  C4 schema↔prose-home references, C5 permission-category legend.
- **Execution:** `bin/check-consistency` (and `--format json` to see which
  check failed).
- **PASS:** exit 0 (all five consistent).
- **FAIL:** exit 1 with the failing check identified.
- **Automation:** `[A]` (CI step) · **Cadence:** per-PR · **Risk:** C4 uses a
  hard-coded schema→home map (noted in `notes/eval-m5`); adding a schema
  requires updating that map or C4 false-fails.

### M4-E05 — State-cap guard
- **Feature area:** M4 (ADR-035 cap); `bin/check-state-cap`.
- **Purpose:** the guard passes when `design/state.md` is at/below the cap
  (default 100 lines) or absent, and fails when over.
- **Execution:**
  ```bash
  bin/check-state-cap --check ; echo "real=$?"
  # synthetic over-cap check, isolated from the repo file:
  bin/check-state-cap --cap=5 --check ; echo "tight=$?"   # current state.md > 5 lines → expect 1
  ```
- **PASS:** `real=0` (the kit's `state.md` is within 100); the tight `--cap=5`
  run returns 1 (demonstrates the guard fires).
- **FAIL:** `real` ≠ 0 with a within-cap file, or the tight cap doesn't fire.
- **Automation:** `[A]` (the `--check` form is a CI step) · **Cadence:** per-PR · **Risk:** the tight-cap demonstration depends on `state.md` having >5 lines; it does today (≈68).

### M4-E06 — Receipt schema document conformance
- **Feature area:** M4 Issue 18; `schemas/receipt.v1.yaml`.
- **Purpose:** the receipt schema declares the documented required fields and
  the `status` enum (`started|completed|failed|partial`).
- **Execution:** read `schemas/receipt.v1.yaml`; confirm required fields
  (`schema`, `version`, `skill`, `key`, `status`, `timestamp`) and the status
  enum.
- **PASS:** schema lists all required fields + the four-value status enum.
- **FAIL:** a required field or a status value is missing/renamed without a
  `.v2.yaml` bump.
- **Automation:** `[SM]` · **Cadence:** on-change (schema) · **Risk:** pair
  with M4-E03 (which exercises the schema in practice).

### M4-E07 — CI surface runs the full read-only gate
- **Feature area:** M4 Issue 20; `.github/workflows/kit-checks.yml`.
- **Purpose:** every push/PR runs the complete non-mutating validation gate
  (tool versions, `bash -n`, `kit.json` parse, `validate-kit-json`,
  `validate-carry-forward`, `check-consistency`, `check-state-cap --check`,
  `self-test`) and blocks on any failure.
- **Execution:** open a PR (or push) and read the `kit-checks` workflow run.
- **Observe:** each step's status.
- **PASS:** all eight steps green on a healthy branch; the workflow uses
  `permissions: contents: read` (no write, no secrets) and does not invoke `gh`.
- **FAIL:** a validator is dropped from the workflow, the workflow gains
  write permission or a secret, or a non-zero check fails to block.
- **Automation:** `[A]` (it *is* CI) · **Cadence:** per-PR · **Risk:** this
  eval also guards the workflow file itself against scope creep.

### M4-E08 — Exit-code semantics audit
- **Feature area:** M4 cross-cutting; §2.5 contract.
- **Purpose:** each envelope-using script returns the *documented* code for
  each failure class (not just 0/non-0).
- **Execution:** drive representative scripts into each class:
  invocation error (bad flag → 2), domain failure (bad input → 1), and where
  applicable auth (3) / approval (4). E.g.:
  ```bash
  bin/validate-carry-forward --not-a-flag ; echo "$?"   # expect 2
  bin/publish-review --artifact /tmp/missing.json ; echo "$?"  # expect 2
  ```
- **PASS:** every probed scenario returns its documented code.
- **FAIL:** a script collapses distinct failure classes into the wrong code
  (e.g. returns 1 for an invocation error).
- **Automation:** `[A]` · **Cadence:** on-change (any `bin/*`) · **Risk:** keep the probe matrix in sync with the script set.

---

## 8. M5 — AI PR review integration

**What M5 shipped (PR #6, issues 22–28, ADR-051, supersedes ADR-046; PRD
addendum `design/prd-addenda/001-ai-pr-review.md`):** an operator-driven,
provider-agnostic AI PR review capability — secret-free provider config
(`schemas/ai-review-config.v1.yaml`, `ai-review/config.example.json`), a
dry-run generator (`bin/review-pr`), safe publishing
(`bin/publish-review`), the rubric/prompt pack (`ai-review/prompts/*`,
`schemas/ai-review-artifact.v1.yaml`), an offline eval harness
(`bin/review-eval` + `ai-review/eval/fixtures/*`), and the `/review-pr`
skill. **Safe by default:** generation posts nothing; publishing needs the
deterministic `--confirm publish-pr-N` token and writes an idempotency
receipt.

All M5 offline evals run with **no API key and no `gh`** via `--diff`,
`--mock`, and `--dir <temp>`.

---

### M5-E01 — Provider config resolution and secret hygiene
- **Feature area:** M5 Issue 23; `schemas/ai-review-config.v1.yaml`, `ai-review/config.example.json`.
- **Purpose:** config resolves in the documented order (defaults →
  `ai-review/config.json` → `--config` → CLI flags), the API key is read
  only from the env var named by `apiKeyEnv`, and a missing key produces a
  setup message with exit 3 (not a traceback).
- **Setup:** copy `ai-review/config.example.json` to a temp config; unset the
  key env var.
- **Execution:**
  ```bash
  unset OPENROUTER_API_KEY
  bin/review-pr --pr 1 --diff ai-review/eval/fixtures/risky-change/input.diff --config /tmp/cfg.json ; echo "nokey=$?"
  grep -R "sk-" ai-review/config.example.json   # must find nothing
  ```
- **PASS:** with no `--mock` and no key, exit 3 + a setup message naming the
  env var; `config.example.json` contains no literal secret (only `apiKeyEnv`).
- **FAIL:** a stack trace instead of exit 3, or any committed config holds a
  literal key value.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change (config schema, `bin/review-pr`) · **Risk:** ensure the env var really is unset in the eval shell.

### M5-E02 — Dry-run generation writes local artifacts, posts nothing
- **Feature area:** M5 Issue 24; `bin/review-pr`.
- **Purpose:** an offline mock run validates the model output, writes a
  JSON+MD artifact, and performs no GitHub call.
- **Setup:** temp out dir `OUT="$(mktemp -d)"`.
- **Execution:**
  ```bash
  bin/review-pr --pr 1 \
    --diff ai-review/eval/fixtures/risky-change/input.diff \
    --mock ai-review/eval/fixtures/risky-change/mock-response.json \
    --out "$OUT" --format md ; echo "rc=$?"
  ls "$OUT"
  ```
- **Observe:** the two artifact files; the rendered markdown; absence of any
  network/GitHub activity.
- **PASS:** `rc=0`; `$OUT` contains `pr-1-<hash>.json` and `pr-1-<hash>.md`;
  no `gh` invocation occurs.
- **FAIL:** non-zero exit on a valid mock, missing artifact, or any GitHub
  call.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change · **Risk:** none (fully offline).

### M5-E03 — Artifact schema conformance
- **Feature area:** M5 Issue 24/26; `schemas/ai-review-artifact.v1.yaml`.
- **Purpose:** the generated artifact conforms to the v1 schema (top-level
  `schema/version/pr/provider/model/profile/artifactHash/summary/findings/stats`;
  each finding has `classification`, `severity`, `category`, `confidence`,
  `commentable`).
- **Setup:** an artifact from M5-E02.
- **Execution:**
  ```bash
  jq -e '.schema=="ai-review-artifact" and .version==1 and (.findings|type=="array") and .stats' "$OUT"/pr-1-*.json
  jq -e '[.findings[] | has("classification") and has("severity") and has("category") and has("commentable")] | all' "$OUT"/pr-1-*.json
  ```
- **PASS:** both `jq -e` expressions exit 0.
- **FAIL:** a required top-level key or per-finding key is absent / wrong type.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change (artifact schema, `review-render.py`) · **Risk:** none.

### M5-E04 — Profile behaviour differs (strict/balanced/lightweight)
- **Feature area:** M5 Issue 26; `ai-review/prompts/profiles.md`.
- **Purpose:** the same diff+model produces profile-appropriate output —
  `lightweight` ≤ `balanced` ≤ `strict` in finding breadth, and the
  `artifact.profile` field echoes the requested profile.
- **Note:** with `--mock` the model reply is fixed, so this eval validates
  that (a) `profile` is recorded correctly and (b) the *rendering/normalisation*
  honours the profile where it filters. Behavioural breadth differences are a
  live-model `[M]` eval.
- **Execution (recorded-profile check, offline):**
  ```bash
  for p in strict balanced lightweight; do
    bin/review-pr --pr 1 --diff ai-review/eval/fixtures/risky-change/input.diff \
      --mock ai-review/eval/fixtures/risky-change/mock-response.json \
      --profile "$p" --out "$OUT" --format json >/dev/null
    jq -r '.profile' "$OUT"/pr-1-*.json   # profile is recorded in the artifact, not the envelope
  done
  ```
- **PASS:** each run records its requested profile in the artifact; (live `[M]`)
  strict yields ≥ findings vs balanced ≥ lightweight on the same diff.
- **FAIL:** the `profile` field doesn't match the flag; (live) lightweight
  emits non-blocking/style findings that the profile forbids.
- **Automation:** `[A]` recorded-profile / `[M]` live-breadth · **Cadence:** on-change (profiles, `review-build-request.py`) · **Risk:** breadth comparison needs a live model; don't gate the automated half on breadth.

### M5-E05 — Rubric quality on fixtures
- **Feature area:** M5 Issue 26/27; the four fixtures + `bin/review-eval`.
- **Purpose:** the prompt pack + normalisation produce rubric-correct
  artifacts: docs-only ⇒ no invented code bugs / no blocking; simple-bugfix
  ⇒ flags missing test-coverage; risky-change ⇒ high-severity security
  blocking + commentable; large-noisy ⇒ finds the buried regression, stays
  quiet on whitespace, truncates safely.
- **Execution:** `bin/review-eval --format json | jq '.outputs.fixtures'`
- **PASS:** all four fixtures meet their `expectations.json` bounds
  (`minBlocking`/`maxBlocking`, `requireCategories`/`forbidCategories`,
  `requireSeverity`, `min/maxCommentable`, `truncated`).
- **FAIL:** any fixture violates its expectation (overall exit 1).
- **Automation:** `[A]` · **Cadence:** per-PR + on-change (prompts, fixtures, render/eval helpers) · **Risk:** the mock responses are canned — this tests the *harness + normalisation*, not live model quality; pair with M5-E12 live for real-model behaviour.

### M5-E06 — Publish preview posts nothing
- **Feature area:** M5 Issue 25; `bin/publish-review`.
- **Purpose:** without `--confirm`, publish previews the exact top-level body
  and inline comments and posts nothing.
- **Setup:** an artifact from M5-E02.
- **Execution:**
  ```bash
  bin/publish-review --artifact "$OUT"/pr-1-*.json --pr 1 ; echo "rc=$?"
  ```
- **PASS:** `rc=0`; output shows the exact comments + the next-command hint
  (`--confirm publish-pr-1`); no `gh` call; no receipt written.
- **FAIL:** any GitHub call, a receipt written, or non-zero exit on preview.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change · **Risk:** none.

### M5-E07 — Approval-token gate
- **Feature area:** M5 Issue 25 (deterministic approval, ADR-048).
- **Purpose:** publishing requires the exact token `publish-pr-<N>`; a
  missing or wrong token refuses with exit 4 and posts nothing.
- **Setup:** artifact from M5-E02; temp receipts dir.
- **Execution:**
  ```bash
  bin/publish-review --artifact "$OUT"/pr-1-*.json --pr 1 --confirm wrong-token --mock --dir "$RDIR" ; echo "wrong=$?"
  bin/publish-review --artifact "$OUT"/pr-1-*.json --pr 1 --confirm publish-pr-1 --mock --dir "$RDIR" ; echo "ok=$?"
  ```
- **PASS:** `wrong=4` (approval failure, nothing posted), `ok=0` (mock
  publish succeeds).
- **FAIL:** a wrong token posts/simulates a post, or returns a code other
  than 4.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change · **Risk:** use `--mock` so no real post is possible.

### M5-E08 — Idempotent publish (receipt dedup)
- **Feature area:** M5 Issue 25; ADR-050 receipts.
- **Purpose:** publishing the same artifact twice is refused (exit 1) unless
  `--force`; the receipt is keyed by PR + artifact hash.
- **Setup:** artifact from M5-E02; fresh temp receipts dir.
- **Execution:**
  ```bash
  bin/publish-review --artifact "$OUT"/pr-1-*.json --pr 1 --confirm publish-pr-1 --mock --dir "$RDIR" ; echo "first=$?"
  bin/publish-review --artifact "$OUT"/pr-1-*.json --pr 1 --confirm publish-pr-1 --mock --dir "$RDIR" ; echo "second=$?"
  bin/publish-review --artifact "$OUT"/pr-1-*.json --pr 1 --confirm publish-pr-1 --mock --dir "$RDIR" --force ; echo "forced=$?"
  ```
- **PASS:** `first=0`, `second=1` (duplicate refused), `forced=0`; a receipt
  exists under `$RDIR` after the first run.
- **FAIL:** the second run posts again without `--force`, or `--force` is
  refused.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change · **Risk:** the
  receipts dir must start empty.

### M5-E09 — Diff truncation safety
- **Feature area:** M5 Issue 24; `maxDiffBytes`.
- **Purpose:** an oversized diff is truncated with an explicit
  `truncated:true` flag (and a logged notice), never silently dropped.
- **Setup:** the `large-noisy` fixture (its `config.json` sets a small
  `maxDiffBytes`).
- **Execution:**
  ```bash
  bin/review-pr --pr 4 --diff ai-review/eval/fixtures/large-noisy/input.diff \
    --mock ai-review/eval/fixtures/large-noisy/mock-response.json \
    --config ai-review/eval/fixtures/large-noisy/config.json \
    --out "$OUT" --format json | jq -e '.outputs.truncated == true'
  ```
- **PASS:** the artifact's `truncated` field is `true`; the run still exits 0.
- **FAIL:** `truncated` is false/absent on an over-limit diff, or the run
  errors instead of truncating.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change · **Risk:** none.

### M5-E10 — Commentability recomputed against the diff
- **Feature area:** M5 Issue 24/25.
- **Purpose:** only findings whose `file`+`line` fall inside the diff's added
  hunks (and are high-confidence, non-praise) are marked `commentable:true`;
  publish routes non-commentable findings to the top-level body, never to a
  broken inline location.
- **Setup:** the `risky-change` artifact (expects ≥1 commentable).
- **Execution:**
  ```bash
  jq '[.findings[] | select(.commentable==true)] | length' "$OUT"/pr-1-*.json
  bin/publish-review --artifact "$OUT"/pr-1-*.json --pr 1 \
    --diff ai-review/eval/fixtures/risky-change/input.diff --format json \
    | jq '.outputs | {inline: .inlineComments, topLevel: .topLevelFindings}'
  ```
- **PASS:** commentable count ≥1 for risky-change; every inline comment's
  file+line lies within the diff; findings without a valid diff line appear
  in the top-level body, not inline.
- **FAIL:** an inline comment targets a line absent from the diff, or a
  praise/low-confidence finding is marked commentable.
- **Automation:** `[A]` · **Cadence:** per-PR + on-change (`review-render.py`, `review-publish.py`) · **Risk:** none.

### M5-E11 — Eval harness green + duplicate prevention
- **Feature area:** M5 Issue 27; `bin/review-eval`.
- **Purpose:** the harness runs all fixtures offline and verifies
  duplicate-publish prevention without touching a real PR (this is the
  single command that exercises M5-E05/E08/E09 together).
- **Execution:** `bin/review-eval`
- **PASS:** exit 0; text reports `N/N fixtures passed` and
  duplicate-prevention holds.
- **FAIL:** exit 1 (a fixture failed or the duplicate check didn't hold).
- **Automation:** `[A]` (also invoked by `bin/self-test`) · **Cadence:** per-PR + on-change · **Risk:** none.

### M5-E12 — `/review-pr` skill protocol (live)
- **Feature area:** M5 Issue 28; `skills/review-pr`.
- **Purpose:** the skill enforces dry-run-first, previews exactly, requires
  explicit approval before any GitHub write, and never asks for / commits a
  secret.
- **Setup:** a scratch repo with a real PR; a configured provider + key.
- **Execution:** `/review-pr <pr> --publish` and follow the protocol.
- **Observe:** the order of operations; whether a key is ever requested in chat.
- **PASS:** the skill generates a dry-run artifact first, shows the exact
  comments, asks for explicit approval, posts only after a deterministic
  approval, writes a receipt, and never requests a secret in chat (it points
  to `docs/ai-review.md` if the key is missing).
- **FAIL:** the skill posts before approval, asks the user to paste a key, or
  skips the preview.
- **Automation:** `[M]` · **Cadence:** pre-release + on-change (`skills/review-pr`) · **Risk:** real GitHub write — use a scratch repo/PR only.

### M5-E13 — Live provider + live publish path (optional)
- **Feature area:** M5 Issues 24/25 (the real network + `gh api` paths).
- **Purpose:** the code paths that the offline evals mock — a real provider
  call and a real `gh api … /reviews` post — actually work end-to-end.
  (These were `bash -n`-clean but never executed during M5 implementation.)
- **Setup:** configured provider + key; `gh` authenticated; a scratch PR.
- **Execution:** `bin/review-pr --pr <n> --profile balanced --format md`
  (live), then `bin/publish-review --artifact … --pr <n> --confirm publish-pr-<n>` (live).
- **PASS:** the live generation returns a schema-valid artifact; the live
  publish returns a GitHub review ID and writes a `completed` receipt.
- **FAIL:** the live call errors in a way the offline path masked (auth,
  payload shape, response parsing).
- **Automation:** `[M]` · **Cadence:** pre-release (when the live paths
  change) · **Risk:** spends real API quota and posts to a real PR — scratch
  repo only; this is the one eval that exercises the un-mocked network paths.

---

## 9. Cross-milestone end-to-end and negative scenarios

### 9.1 End-to-end happy paths

#### E2E-01 — PRD → first PR → review → release
- **Feature area:** the whole kit (M1 intake, M3 control, M2 contract, M5 review).
- **Purpose:** a single project goes from a PRD to a merged-ready, AI-reviewed
  PR using only documented verbs.
- **Setup:** §2.3 target on a scratch GitHub repo; `gh` authenticated;
  provider key set (for the review leg).
- **Execution:** `/start` → PRD intake (`/idea-to-prd` or `/prd-normalizer`)
  → `/prd-to-mvp` → `/planning` → `/issue-planner` (`/backlog`) →
  `/work` (`prepare-issue` → `claude-issue-executor`) → `/ship`
  (`pr-review-packager`) → `/review-pr <pr>` → `/release` (dry-run).
- **PASS:** each verb hands off to the next per `kit.json`; a PR is opened;
  `/review-pr` produces a dry-run artifact; `/release --dry-run` describes a
  coherent release. No step requires undocumented manual fixup.
- **FAIL:** a handoff breaks, a verb maps to a missing skill, or the flow
  stalls without a documented recovery.
- **Automation:** `[M]` · **Cadence:** pre-release + quarterly · **Risk:**
  long and model/GitHub-dependent; run on a scratch repo.

#### E2E-02 — Follow-up feature via addendum
- **Feature area:** M3 `/feature` (ADR-049) + M5 review.
- **Purpose:** an in-flight project adds a capability through the follow-up
  PRD workflow without rewriting the original PRD, then ships and reviews it.
- **Execution:** `/feature "new capability"` → `/decide` (`clarify` →
  `adr-writer` → `check-plan`) → `/backlog` → `/work` → `/ship` → `/review-pr`.
- **PASS:** a numbered addendum is created; ADRs (if any) pass `check-plan`;
  issues trace to the addendum; the PR is reviewed via `/review-pr`.
- **FAIL:** the original PRD is mutated, or the addendum doesn't drive the
  backlog.
- **Automation:** `[M]` · **Cadence:** pre-release · **Risk:** as E2E-01.

#### E2E-03 — Session continuity mid-flow
- **Feature area:** M3 `/pause` + `/resume`.
- **Purpose:** work paused mid-issue resumes accurately in a fresh session.
- **Execution:** start `/work` on an issue, `/pause` before finishing, open a
  new session, `/resume`, continue to PR.
- **PASS:** `/resume` reconstructs the correct phase/in-flight issue/next
  action; work continues without re-deriving context by hand.
- **FAIL:** the resumed brief is wrong or empty, forcing manual reconstruction.
- **Automation:** `[SM]` · **Cadence:** pre-release · **Risk:** none beyond
  scratch-repo hygiene.

#### E2E-04 — Release-readiness gate
- **Feature area:** M4 + M5 aggregate.
- **Purpose:** one composite command sequence proves the kit is releasable.
- **Execution:**
  ```bash
  bin/self-test && bin/review-eval && bin/check-consistency && bin/validate-kit-json && bin/validate-carry-forward && bin/check-state-cap --check && echo "RELEASE-READY"
  ```
- **PASS:** prints `RELEASE-READY` (all gates exit 0).
- **FAIL:** any gate exits non-zero (the chain stops).
- **Automation:** `[A]` · **Cadence:** pre-release (mirrors CI; run locally
  before tagging) · **Risk:** this is the canonical pre-release smoke gate —
  keep it identical to the CI surface (M4-E07) so local and CI verdicts agree.

### 9.2 Negative / failure-mode evaluations

These verify the kit **refuses** or **fails loudly** rather than corrupting
state. Each creates its malformed input in a temp location and never mutates
a tracked file.

#### NEG-01 — Malformed `kit.json` is rejected
- **Setup:** copy `kit.json` to a temp dir, delete a skill entry that exists
  in `skills/`.
- **Execution:** run `bin/validate-kit-json` against the broken copy (or in a
  temp checkout).
- **PASS:** exit 1 naming the drift. **FAIL:** exit 0 (drift undetected).
- **Automation:** `[A]` · **Cadence:** on-change · **Risk:** must run against a
  copy, not the real file.

#### NEG-02 — Skill ↔ index drift is caught
- **Setup:** in a temp checkout, rename a skill's frontmatter `name` without
  updating `kit.json`.
- **Execution:** `bin/validate-kit-json` and `bin/check-consistency`.
- **PASS:** at least one exits 1. **FAIL:** both exit 0.
- **Automation:** `[A]` · **Cadence:** on-change.

#### NEG-03 — Dangling handoff target is caught
- **Setup:** point a skill's `next` at a non-existent skill (temp checkout).
- **Execution:** `bin/validate-kit-json`.
- **PASS:** exit 1. **FAIL:** exit 0.
- **Automation:** `[A]` · **Cadence:** on-change.

#### NEG-04 — Non-conformant carry-forward block is rejected
- **Setup:** temp file with a `### design-questions` block missing
  `target-issue` (or with a bad pattern / forbidden extra field).
- **Execution:** `bin/validate-carry-forward --file /tmp/bad.md`.
- **PASS:** exit 1 with the offending field named. **FAIL:** exit 0.
- **Automation:** `[A]` · **Cadence:** on-change (covered by M4-E02's bad half).

#### NEG-05 — Over-cap state file is flagged
- **Setup:** none (use the tight-cap form).
- **Execution:** `bin/check-state-cap --cap=5 --check` (kit `state.md` > 5 lines).
- **PASS:** exit 1. **FAIL:** exit 0.
- **Automation:** `[A]` · **Cadence:** per-PR (covered by M4-E05).

#### NEG-06 — Invalid model output is rejected
- **Setup:** a temp mock response that is not valid JSON / not schema-shaped.
- **Execution:**
  ```bash
  echo 'not json' > /tmp/bad-resp.txt
  bin/review-pr --pr 1 --diff ai-review/eval/fixtures/docs-only/input.diff --mock /tmp/bad-resp.txt --out "$OUT" ; echo "$?"
  ```
- **PASS:** exit 1 (domain failure: unparseable/invalid output); no artifact
  written. **FAIL:** exit 0 or an artifact written from garbage.
- **Automation:** `[A]` · **Cadence:** on-change (`review-render.py`).

#### NEG-07 — Duplicate publish is refused
- Same as M5-E08's second run: **PASS** exit 1 without `--force`. `[A]`.

#### NEG-08 — Wrong approval token is refused
- Same as M5-E07's wrong-token run: **PASS** exit 4, nothing posted. `[A]`.

#### NEG-09 — Missing provider credential fails cleanly
- Same as M5-E01's no-key run: **PASS** exit 3 + setup message, no traceback. `[A]`.

#### NEG-10 — Installer leaves no untracked `design/` file
- **Feature area:** the M0/M1 casing regression (M0-E06 restated as a guard).
- **Execution:** fresh install (§2.3) + initial commit; `git status --porcelain design/`.
- **PASS:** empty output (everything under `design/` is tracked).
- **FAIL:** any untracked `design/` file (the casing bug regressed).
- **Automation:** `[SM]` (run on a case-sensitive FS) · **Cadence:** pre-release + on-change (installer).

#### NEG-11 — Live GitHub write requires authentication
- **Feature area:** M2/M5 `gh`-dependent surfaces.
- **Execution:** with `gh` logged out, run `bin/publish-review … --confirm publish-pr-1` (no `--mock`).
- **PASS:** exit 3 (auth/service failure) with a clear message; nothing posted.
- **FAIL:** a traceback, or a partial post.
- **Automation:** `[SM]` · **Cadence:** on-change (`publish-review`, `prepare-issue`) · **Risk:** must actually log `gh` out for the duration.

---

## 10. Coverage matrix

| Milestone / area | Evals | Primary automation |
|---|---|---|
| M0 foundation / integrity | M0-E01…E09, NEG-10 | mostly `[A]`; installer `[SM]` |
| M1 front door + PRD intake/planning | M1-E01…E06, E2E-01 | mostly `[M]`/`[SM]`; placeholder `[SM]` |
| M2 agent contract | M2-E01…E06, NEG-01/02/03/11 | `[A]` (+ live `[SM]`) |
| M3 unified workflow control | M3-E01…E12, E2E-02/03, NEG-05 | mixed `[A]`/`[SM]` |
| M4 reliability/validation/receipts/self-test | M4-E01…E08, E2E-04, NEG-04/05 | `[A]` (CI) |
| M5 AI PR review | M5-E01…E13, NEG-06/07/08/09 | `[A]` offline (+ live `[M]`) |
| Cross-milestone E2E | E2E-01…E04 | `[A]` (E2E-04) / `[M]` |
| Negative / failure modes | NEG-01…NEG-11 | mostly `[A]` |

Every M0–M5 issue and governing ADR is exercised by at least one eval:
M0 issues → M0-E0x; M1 issues 1–5 → M1-E01/E03/E04 + M0-E06; M2 issues 6–10
→ M2-E01…E06; M3 issues 11–15/21 → M3-E01…E12; M4 issues 16–20 → M4-E01…E08;
M5 issues 22–28 → M5-E01…E13.

---

## 11. Cadence summary and maintenance

| Cadence | Evals (automation-eligible shown first) |
|---|---|
| **per-PR (CI)** | M0-E01/E02/E03/E04/E05, M2-E01/E02/E03/E05, M3-E04/E07/E08/E09, M4-E01/E02/E03/E04/E05/E07, M5-E01…E11, NEG-04/05/07/08/09 (via the CI surface + `bin/review-eval` + `bin/self-test`). |
| **pre-release** | E2E-01…E04, M0-E06/E07/E08, M1-E03, M3-E11, M5-E12/E13, NEG-10/11. |
| **on-change** | the eval(s) whose implementing files changed (each eval lists them). |
| **quarterly** | M1-E01/E02/E04/E05/E06, M2-E06 (front-door & prose UX). |

**Keeping this plan honest:**

- When a new `bin/*` script or skill ships, add it to M2-E03's envelope
  probe list, M4-E08's exit-code matrix, and (if it has fixtures) a new
  M5-style eval — and to `kit.json` so M2-E01 covers it.
- The CI surface (M4-E07) and the local release gate (E2E-04) must list the
  **same** validators; if they drift, the eval that guards the workflow file
  is itself the fix.
- Negative evals must always operate on temp copies; an eval that mutates a
  tracked fixture is a defect in the eval.
- This plan does not duplicate model-quality judgement: offline M5 evals test
  the *harness and normalisation* with canned responses; real model behaviour
  is the live `[M]` evals (M5-E04 breadth, M5-E12/E13). Keep that boundary —
  it's what lets the bulk of the suite run in CI with no key and no network.
