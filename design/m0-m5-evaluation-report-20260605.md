# M0–M5 Evaluation Report — 2026-06-05

**Report type:** full re-run of the [M0–M5 Evaluation Plan](m0-m5-evaluation-plan.md)
on the latest `main` lineage.
**Run mode:** offline-first, non-mutating. No live GitHub writes, no provider
API calls, no destructive operations. Read-only `gh` was used only to verify
PR merge status; every functional eval ran offline (no key, `gh` hidden where
the plan's gate concerns the `gh`-absent path).
**Verdict:** **56 PASS · 1 FAIL · 12 NOT RUN** across 69 evals
(M0–M5 + E2E + NEG).

---

## 1. Executive summary

The kit is healthy on every automatable, offline-runnable evaluation. All M0
integrity checks, the full M2 agent-contract surface, the M3 deterministic
`bin/*` surfaces, the entire M4 reliability/validation/self-test gate, and the
complete M5 offline AI-review suite pass. The canonical pre-release gate
(E2E-04) prints `RELEASE-READY`. Every negative/failure-mode eval that can run
offline correctly refuses or fails loudly with the documented exit code.

One eval is marked **FAIL**: **M3-E10 (granularity bands)** — not because the
feature is broken, but because the *evaluation plan's own PASS gate contradicts
the shipped implementation*. The plan asserts the `coarse` band is `[3,5]`
phases; the shipped `prd-to-mvp`/`planning` skills document `coarse` as `1–3`.
An honest run of M3-E10 as written would false-FAIL a correct coarse
decomposition of 1–2 phases. This is a defect in the plan, surfaced exactly as
the task instructed (mark FAIL when an eval exposes a real plan/repo issue), and
left unfixed pending maintainer decision.

Two additional findings worth a maintainer's attention, neither of which fails
its parent eval:

- **`bin/check-state-cap` does not validate `--cap`'s value.** Passing a
  non-numeric cap (`--cap=abc`) leaks a raw bash error
  (`integer expression expected`) and returns exit **1** with a nonsensical
  "over cap abc" message, instead of exit **2** for an invocation error — which
  its own header (line 20) promises. This is *out of scope* for M4-E08 (which
  covers only envelope-using scripts; `check-state-cap` does not source
  `json-envelope.sh`), so M4-E08 still PASSes on its documented probes, but the
  behaviour is a genuine robustness bug.
- **M1-E03 leaves 2 raw `{{…}}` tokens** in the generated `CLAUDE.md`. Both are
  documented *free-form prose hints* (template line 60), not unresolved
  substitution variables; zero `{{UPPER_SNAKE}}` substitution tokens survive.
  The eval's literal "0 raw tokens" gate over-counts these by design; recorded
  PASS on the meaningful gate with the deviation noted.

The 12 NOT-RUN evals are all `[M]`/live or agent-driven slash-command flows
(real GitHub writes, real provider keys, or interactive model behaviour) that
the task scoped out. Where the plan defines a safe offline/structural substitute
(skills exist, handoff graph closes, docs anchor present), that substitute was
run and recorded.

---

## 2. Environment and commit info

| Item | Value |
|---|---|
| Date | 2026-06-05 |
| Host | Darwin 25.3.0, arm64 (macOS, **case-insensitive** filesystem) |
| Working dir | `/Users/hermes/workflow-generator-takumi-m5` |
| Branch | `design/m0-m5-evaluation-report` |
| HEAD at run start | `663ba52b9770ddf33b2463358f2359b052fba1e9` |
| `git describe` | `v4.0.0-31-g663ba52` |
| `kitVersion` (kit.json) | `4.1.0` |
| bash | `3.2.57(1)-release` (system) |
| python3 | `3.9.6` |
| jq | `jq-1.7.1-apple` |
| gh | authenticated as `takumi-omorgan` (used **read-only**, for PR status only) |
| `.claude/skills/` symlinks | **not present** — irrelevant to this run, because all evals invoke skills as `skills/<name>/` source or `bin/*` directly, never as live slash commands |

**Tooling deviations from plan §2.1.** The plan lists `bash (4+)`. The host ships
bash `3.2.57`. No eval failed for a bash-version reason — every `bin/*` script
passed `bash -n` (M0-E03) and ran correctly. The kit's `bin/*` scripts target
POSIX/bash-3-compatible syntax. Noted as an environment fact, not a failure.

**Filesystem caveat.** macOS is case-insensitive. Two evals (M0-E01's `Design/`
check, M0-E06/NEG-10's casing guard) cannot truly catch the historical
`Design`→`design` regression here; that requires a case-sensitive FS
(Linux/CI). Both were run and verified against **git** (the source of truth),
which tracks only lowercase `design/`. See the per-eval notes.

---

## 3. PR #6 / PR #7 merge verification

Verified with read-only `gh pr view` and `git merge-base --is-ancestor`:

| PR | Title | State | Merge commit | Merged at | Ancestor of HEAD? |
|---|---|---|---|---|---|
| #6 | M5: AI PR review integration (Issues 22-28, ADR-051) | **MERGED** | `34f6ef7ee141af56cb7edad9c1539ea0c02d71e9` | 2026-06-05T14:13:42Z | ✅ yes |
| #7 | design: M0–M5 evaluation plan | **MERGED** | `663ba52b9770ddf33b2463358f2359b052fba1e9` | 2026-06-05T14:43:12Z | ✅ yes |

Both merge commits are on the `main` lineage that this report's branch is based
on. Corroborating artifacts present on disk: `design/adr/adr-051-operator-driven-ai-pr-review.md`,
`design/prd-addenda/001-ai-pr-review.md`, `design/m0-m5-evaluation-plan.md`.

---

## 4. Methodology

1. **Fresh start.** The prior interrupted run was ignored except as background.
   The plan was re-read in full (1238 lines) and every eval re-derived from it.
2. **Offline-first.** Every functional eval ran with no provider API key and no
   reliance on live `gh`. For evals whose gate concerns the `gh`-absent path
   (M2-E04, NEG-11), `gh` was hidden from `PATH` (a shim dir ahead of a minimal
   `PATH` that still exposed `python3`/`jq`) to force the documented exit-3
   degraded path deterministically.
3. **Safety.** No PR was merged. No real GitHub write was issued. The installer
   evals ran into a throwaway `mktemp` target, never the kit repo. Negative
   evals mutated only temp copies (kit.json + skills/ copied into `mktemp -d`),
   never tracked files. The criteria-drift eval (M3-E09) restored the touched
   template's mtime afterward.
4. **Verdict discipline.** Each eval recorded ID, status, the exact command(s),
   exit code(s), key evidence, and any deviation. Where an eval's literal gate
   was crude or out of sync with the implementation, the *meaningful* gate was
   evaluated and the deviation documented; where an eval exposed a real
   plan/repo issue, it was marked FAIL (M3-E10) rather than silently fixed.
5. **Substitutes for `[M]`/live evals.** Agent-driven slash-command flows and
   live-network evals were marked NOT RUN with a clear reason, and the plan's
   defined offline substitute (skill presence, handoff-graph closure via
   `bin/check-consistency`, documented-anchor inspection, reference-artifact
   presence) was executed and recorded.

Exit-code contract reference (plan §2.5): `0` success · `1` domain failure ·
`2` invocation error · `3` auth/service failure · `4` approval failure.
`bin/check-plan` and other non-envelope scripts are documented exceptions.

---

## 5. Aggregate counts

| Status | Count | Eval IDs |
|---|---|---|
| **PASS** | **56** | M0-E01…E09 (9); M1-E01/E03/E04 (3); M2-E01…E06 (6); M3-E01/E02/E04/E05/E07/E08/E09 (7); M4-E01…E08 (8); M5-E01…E11 (11); E2E-04 (1); NEG-01…NEG-11 (11) |
| **FAIL** | **1** | M3-E10 |
| **NOT RUN** | **12** | M1-E02/E05/E06; M3-E03/E06/E11/E12; M5-E12/E13; E2E-01/E02/E03 |
| **Total** | **69** | |

By milestone: **M0** 9/0/0 · **M1** 3/0/3 · **M2** 6/0/0 · **M3** 7/1/4 ·
**M4** 8/0/0 · **M5** 11/0/2 · **E2E** 1/0/3 · **NEG** 11/0/0
(PASS/FAIL/NOT RUN).

Automation note: every `[A]` eval that the plan marks per-PR/CI-eligible passed.
The single FAIL and all 12 NOT-RUN are `[M]`/`[SM]` (live or agent-driven),
except M3-E10 whose *structural* half exposed a plan defect.

---

## 6. Per-eval detailed results

Legend: ✅ PASS · ❌ FAIL · ⏭️ NOT RUN. "rc" = exit code.

### 6.1 M0 — Foundation / integrity

| ID | Status | Evidence |
|---|---|---|
| M0-E01 | ✅ | Structure loop printed no `MISSING:` line; all of `skills/ bin/ bin/lib/ templates/ docs/ design/adr/ schemas/ ai-review/ prompts/` and `kit.json/CLAUDE.md/README.md` present. The `test -d Design` branch fired a false positive on macOS case-insensitivity; verified against git: `git ls-files \| grep '^Design/'` → none; only lowercase `design/` is tracked. **Deviation:** the `test -d Design` probe is unreliable on case-insensitive FS — see Follow-ups. |
| M0-E02 | ✅ | `python3 -c "import json; json.load(open('kit.json'))"` → rc 0, no traceback. |
| M0-E03 | ✅ | `bash -n` over all `bin/*`+`bin/lib/*` shell scripts and `ast.parse` over `bin/lib/*.py` → `rc=0`. |
| M0-E04 | ✅ | Front-door gate (per `notes/baseline-health.md`): 233 local links across `README.md`, `CLAUDE.md`, `docs/*.md` → **0 broken**. The all-tracked superset flags ~52 links, all documented illustrative/template/target-context false positives (baseline-health row 11: "533 links, 51 flagged… 2 genuine defects [fixed in M0]"). **Deviation:** the gate is scoped to front-door docs per the baseline resolver's exclusion rule. |
| M0-E05 | ✅ | `bin/sync-adr-index --check` → rc 0, "index is in sync". |
| M0-E06 | ✅ | Throwaway target install: `git ls-files design/adr/README.md` lists it; `git status --porcelain design/` empty. **Caveat:** macOS case-insensitive — the real regression needs a case-sensitive FS (CI). |
| M0-E07 | ✅ | `bin/install-workflow-kit --target=$T --project-name=demo --non-interactive` → rc 0; `.claude/skills` = **22**; `CLAUDE.md`, `design/adr/`, `.gitignore` all present. |
| M0-E08 | ✅ | After baseline commit, rerun with `--force` → rc 0; `git status --porcelain` empty (fully idempotent; empty allow-list met). |
| M0-E09 | ✅ | `python3 notes/skills-audit-2026-05-07/audit.py` → rc 0; CSV has 22 rows, **0** over any budget flag (`desc_over_1024`/`over_500_lines`/`over_5k_tokens_est` all 0). Tree not dirtied (CSV regenerates identically). |

### 6.2 M1 — Front door / PRD intake

| ID | Status | Evidence |
|---|---|---|
| M1-E01 | ✅ | README Quick Start offers exactly one recommended command (`bash <(curl …bootstrap-workflow-kit) --project-name=…`). Alternatives (inspect-first, manual install) are deferred to `docs/install.md` behind a `>` aside. **Zero** `ADR-NNN` citations in README. (`[M]` prose; objective anchor met.) |
| M1-E02 | ⏭️ | `[M]`, live GitHub flow — NOT RUN (real scratch-repo writes). **Substitute run:** all five tutorial skills exist in handoff order — `prd-normalizer`, `prd-to-mvp`, `issue-planner`, `claude-issue-executor`, `pr-review-packager`. |
| M1-E03 | ✅* | Generated `CLAUDE.md`: **0** `{{UPPER_SNAKE}}` substitution tokens survive (all resolved or rendered `_TBD_`; `GITHUB_OWNER`→`_TBD_` per installer warning); `_TBD_` count = 28. **Deviation:** 2 raw `{{…}}` remain — both *documented free-form prose hints* (template line 60: "Free-form slots use `{{prose hints}}`"), at template lines 78 & 126. PASS on the meaningful gate (0 unresolved substitution tokens); the literal "0 raw tokens" gate needs the refinement noted in Follow-ups. |
| M1-E04 | ✅ | `docs/troubleshooting.md` is symptom-organised with 5 symptom-titled `##` sections covering: autocomplete, skills-not-discovered, GitHub project creation, stale prompt, installer rerun. The 6th required symptom (unresolved placeholders) is covered with a concrete remedy at line 107 ("Unexpected `{{PLACEHOLDER}}` or `_TBD_` values?") as a sub-bullet under the installer-rerun section rather than its own heading. Not undocumented; page stays symptom-first → does not hit the FAIL gate. **Minor note:** maintainer may promote it to its own heading. |
| M1-E05 | ⏭️ | `[M]`, agent/model-driven artifact generation — NOT RUN. **Substitute run:** intake skills `idea-to-prd`, `prd-normalizer`, `prd-to-mvp` all present. |
| M1-E06 | ⏭️ | `[M]`, agent/model-driven planning — NOT RUN. **Substitute run:** `planning` and `issue-planner` skills present. |

### 6.3 M2 — Machine-readable agent contract

| ID | Status | Evidence |
|---|---|---|
| M2-E01 | ✅ | `bin/validate-kit-json` → rc 0, "in sync (22 skills; kit.json and frontmatter agree)". |
| M2-E02 | ✅ | Parsed YAML frontmatter of all 22 `skills/*/SKILL.md`; every skill has all 6 required keys (`name`, `description`, `permission-category`, `inputs`, `outputs`, `next`) non-empty. rc 0. |
| M2-E03 | ✅ | `validate-kit-json`, `check-consistency`, `review-eval` each emit valid JSON with `.skill and .status`; `validate-kit-json --format json` has all 6 envelope keys (`skill, version, status, outputs, next, errors`). |
| M2-E04 | ✅ | `gh`-hidden path: `bin/prepare-issue --issue 27 --format json` → rc **3**, `status:"degraded"`, `errors:[{code:"gh-unavailable",…}]` (no traceback). Documented `outputs` fields all present; `promptPath` resolved, `stale:null`, `next`→`claude-issue-executor`. `git status` unchanged (wrote nothing). Live `gh` path not exercised (read-only by design; offline gate met). |
| M2-E05 | ✅ | `bin/validate-kit-json` rc 0 (resolves `next[].skill`, confirmed at script lines 112–115) **and** `bin/check-consistency` rc 0 (C2 verb-layer). Handoff graph closed. |
| M2-E06 | ✅ | `docs/agent-contract.md` references all four parts (`kit.json`, frontmatter, envelope, `prepare-issue`). `docs/github-setup.md` has a "Required scopes" table (`repo`, `read:org`, `project`, `workflow`) and a "Preflight checklist" section (line 77, with `gh auth status`). (`[M]`; enumerated items met.) |

### 6.4 M3 — Unified workflow control

| ID | Status | Evidence |
|---|---|---|
| M3-E01 | ✅ | `docs/workflow-control.md` documents the closed, case-insensitive token set **exactly**: `approve approved yes go proceed lgtm` (line 102), and states near-misses do not advance (line 108). (`[SM]`; deterministic doc anchor verified. The interactive behavioural half — exact token vs near-miss in a live skill run — was not interactively exercised.) |
| M3-E02 | ✅ | Mode×category matrix (lines 39–43): cat-3 requires explicit approval in **all** modes ("No mode ever relaxes cat-3"); cat-2 under assisted/autonomous proceeds with a mandatory written acknowledgement (lines 52–55). Matches ADR-048. (`[SM]`; matrix anchor verified; live per-mode exercise not interactively run.) |
| M3-E03 | ⏭️ | `[SM]`, agent-driven `/start` routing across constructed states — NOT RUN. **Substitute:** `skills/start/SKILL.md` exists and reads `state.md`/`next-action`. |
| M3-E04 | ✅ | `bin/check-consistency` rc 0 (C2 maps every verb to a real underlying skill). |
| M3-E05 | ✅ | `design/state.md` has all six marker-fenced zones (phase, in-flight, recent, blockers, continue-here, next-action). The `next-action` block parses and contains all four fields (`skill`, `args`, `preconditions`, `blocked-by`) in both `state.md` and `templates/state-template.md`. |
| M3-E06 | ⏭️ | `[SM]`, agent-driven `/pause`→`/resume` round-trip — NOT RUN. **Substitute:** `pause` and `resume` skills present. |
| M3-E07 | ✅ | `bin/check-plan --criteria-set adr` → good ADR (adr-050) rc **0**; deliberately-incomplete `/tmp/bad-adr.md` (no Context/Decision/Consequences) rc **1** (ADR-C1/C2 FAIL). |
| M3-E08 | ✅ | `bin/check-plan --criteria-set prompt` → good prompt (issue-027) rc **0**; stripped temp prompt rc **1** (PROMPT-C6/C1/C2 FAIL). `--format json` output is valid JSON (legacy shape `{criteria-set, result, criteria}` — grandfather exception, no envelope `.status`). |
| M3-E09 | ✅ | `bin/check-plan-criteria-drift --check` → clean tree rc **0**; after touching `templates/adr-template.md` newer than `criteria.md` rc **1** ("criteria may be stale"). mtime restored; post-restore rc 0; tree clean. |
| M3-E10 | ❌ | **Behavioural phase-count run NOT RUN** (`[SM]`, agent/model-driven). **Structural inspection exposed a plan↔repo defect:** the plan's PASS gate says `coarse ∈ [3,5]` (lines 634, 639), but the shipped `prd-to-mvp` skill documents `coarse` as **1–3** (SKILL.md lines 54, 79–80, 95–96); `planning` defers to the same bands. `standard` (5–8) and `fine` (8–12) agree. Marked FAIL per the task's "expose a real plan/repo issue" rule — the plan's coarse gate would false-FAIL a correct 1–2-phase coarse run. Not fixed (awaiting maintainer decision on which band is canonical). |
| M3-E11 | ⏭️ | `[SM]`, agent-driven lifecycle chain (`/audit-milestone`→`/milestone-summary --dry-run`→`/complete-milestone --dry-run`) — NOT RUN. **Substitute:** all three skills present; `milestone-summary` and `complete-milestone` document `--dry-run` (6 mentions each); `audit-milestone` is read-only by design (no `--dry-run` needed). |
| M3-E12 | ⏭️ | `[SM]`, agent-driven `/feature` addendum — NOT RUN. **Substitute:** `feature-prd` skill present; reference example `design/prd-addenda/001-ai-pr-review.md` present. |

### 6.5 M4 — Reliability / validation / receipts / self-test

| ID | Status | Evidence |
|---|---|---|
| M4-E01 | ✅ | `bin/self-test` rc 0 → "ok — 13/13 steps passed in 1s; no friction"; `--format json` `status:"ok"`. |
| M4-E02 | ✅ | `bin/validate-carry-forward` (tracked) rc **0** ("no design-questions blocks found in 7 file(s)" — all tracked notes deliberately omit the block). Properly-fenced bad block missing `target-issue` → rc **1** ("missing required field 'target-issue'"); bad `target-issue` pattern (`"5"`) → rc **1** (pattern `^#[0-9]+$`). |
| M4-E03 | ✅ | Temp `--dir`: write rc **0**, find-existing rc **0**, find-missing rc **1**; written `demo__k1.json` has all required fields (`schema, version, skill, key, status, timestamp`). |
| M4-E04 | ✅ | `bin/check-consistency` rc 0 → "consistent (22 skills; docs and metadata agree)"; JSON `outputs.problems: []`. |
| M4-E05 | ✅ | `bin/check-state-cap --check` rc **0** (state.md 68 lines ≤ 100); `--cap=5 --check` rc **1** (fires). |
| M4-E06 | ✅ | `schemas/receipt.v1.yaml` declares required `[schema, version, skill, key, status, timestamp]` and status enum `[started, completed, failed, partial]`. |
| M4-E07 | ✅ | `.github/workflows/kit-checks.yml` present with `permissions: contents: read`, no secrets, "gh intentionally not used". All 8 steps present: tool versions, `bash -n`, `kit.json` parse, `validate-kit-json`, `validate-carry-forward`, `check-consistency`, `check-state-cap --check`, `self-test`. (File-inspection verdict; the live CI run is observable on the PR opened for this report.) |
| M4-E08 | ✅ | Documented probes: `validate-carry-forward --not-a-flag` → **2**; `publish-review --artifact /tmp/missing` → **2**; `validate-kit-json --nope` → **2**. All envelope-using scripts return the documented code. **Finding (out of M4-E08 scope):** `check-state-cap --cap=abc` → **1** (should be 2) — but `check-state-cap` does not source `json-envelope.sh`, so it is not an "envelope-using script" per §2.5. Reported in §7. |

### 6.6 M5 — AI PR review integration (all offline, no key, no `gh`)

| ID | Status | Evidence |
|---|---|---|
| M5-E01 | ✅ | No key + no `--mock`: `bin/review-pr … --config /tmp/cfg.json` → rc **3** + setup message naming `$OPENROUTER_API_KEY`, points to `docs/ai-review.md`, warns "NEVER paste the key". `config.example.json` holds no literal secret, only `apiKeyEnv`. |
| M5-E02 | ✅ | Mock run → rc **0**; `$OUT` has `pr-1-e958c428.json` + `pr-1-e958c428.md` (correct `pr-1-<hash>.{json,md}` naming); fully offline, no `gh` call. |
| M5-E03 | ✅ | `jq -e` both pass: top-level `schema=="ai-review-artifact"`, `version==1`, `findings` array, `stats`; every finding has `classification/severity/category/commentable`. |
| M5-E04 | ✅ | strict/balanced/lightweight each record their requested `profile` in the artifact. (Offline half; live finding-breadth comparison is `[M]`, not run.) |
| M5-E05 | ✅ | `bin/review-eval --format json` → rc 0; all 4 fixtures `pass:true, problems:[]` (docs-only, simple-bugfix, risky-change, large-noisy). |
| M5-E06 | ✅ | `bin/publish-review --artifact … --pr 1` (no `--confirm`) → rc **0**, shows "re-run with: --confirm publish-pr-1", no receipt written. |
| M5-E07 | ✅ | `--confirm wrong-token --mock` → rc **4**; `--confirm publish-pr-1 --mock` → rc **0**. |
| M5-E08 | ✅ | first rc **0**, second rc **1** (dup refused), `--force` rc **0**; receipt `publish-review__pr-1.json` present after first run. |
| M5-E09 | ✅ | large-noisy with small `maxDiffBytes` → `outputs.truncated == true`, `status:"ok"` (rc 0). |
| M5-E10 | ✅ | risky-change commentable count = **2** (≥1); publish preview routes **inline:2, topLevel:0** (no broken inline location); recompute-against-diff validated by the harness (M5-E05 risky-change commentable bounds pass). |
| M5-E11 | ✅ | `bin/review-eval` → rc 0; "4/4 fixtures passed" + "duplicate-publish prevention — first post ok, duplicate refused (exit 1)". |
| M5-E12 | ⏭️ | `[M]`, live `/review-pr --publish` to a real scratch PR — NOT RUN. **Substitute:** `skills/review-pr` present; offline protocol behaviours (dry-run-first, exact preview, token gate, no-secret-in-chat) verified piecewise via M5-E01/E02/E06/E07. |
| M5-E13 | ⏭️ | `[M]`, live provider call + real `gh api …/reviews` post — NOT RUN (spends real quota, posts to a real PR). This is the one eval that exercises the un-mocked network paths; it remains unverified end-to-end (as the plan itself notes the live paths were `bash -n`-clean but never executed). |

### 6.7 Cross-milestone end-to-end

| ID | Status | Evidence |
|---|---|---|
| E2E-01 | ⏭️ | `[M]`, full PRD→PR→review→release on a live scratch repo + provider key — NOT RUN. **Substitute:** verb→skill handoff graph closes (`bin/check-consistency` + `bin/validate-kit-json` both rc 0). |
| E2E-02 | ⏭️ | `[M]`, live follow-up-feature flow — NOT RUN. **Substitute:** `feature-prd` present, reference addendum present (see M3-E12). |
| E2E-03 | ⏭️ | `[SM]`, agent-driven session continuity (`/pause`→new session→`/resume`) — NOT RUN. **Substitute:** see M3-E05/E06. |
| E2E-04 | ✅ | `self-test && review-eval && check-consistency && validate-kit-json && validate-carry-forward && check-state-cap --check` → prints **`RELEASE-READY`**, chain rc 0. Mirrors the CI surface (M4-E07). |

### 6.8 Negative / failure-mode

| ID | Status | Evidence |
|---|---|---|
| NEG-01 | ✅ | Temp copy with `changelog` removed from kit.json → `validate-kit-json` rc **1** ("skill changelog exists in skills/ but is missing from kit.json"). |
| NEG-02 | ✅ | Temp copy with frontmatter `name: changelog-renamed` → `validate-kit-json` rc **1** ("frontmatter name=… does not match directory"). |
| NEG-03 | ✅ | Temp copy with a `next[].skill` set to `no-such-skill-xyz` → `validate-kit-json` rc **1** ("lists next.skill=no-such-skill-xyz which is not in the index"). (First attempt used a malformed mutation — `next` is a list of `{skill,when}` objects, not strings — corrected and re-run.) |
| NEG-04 | ✅ | Covered by M4-E02 bad half: missing `target-issue` → rc 1, field named. |
| NEG-05 | ✅ | Covered by M4-E05: `check-state-cap --cap=5 --check` → rc 1. |
| NEG-06 | ✅ | `echo 'not json' \| review-pr --mock …` → rc **1** ("no JSON object found in model output"); no artifact written to the out dir. |
| NEG-07 | ✅ | Covered by M5-E08 second run → rc 1 without `--force`. |
| NEG-08 | ✅ | Covered by M5-E07 wrong-token run → rc 4, nothing posted. |
| NEG-09 | ✅ | Covered by M5-E01 no-key run → rc 3 + setup message, no traceback. |
| NEG-10 | ✅ | Covered by M0-E06: `git status --porcelain design/` empty after fresh install. **Caveat:** case-insensitive FS — needs CI to catch the real regression. |
| NEG-11 | ✅ | `gh`-hidden substitute for "logged out": `publish-review … --confirm publish-pr-1` (no `--mock`) → rc **3** ("gh CLI not found; cannot post"); no receipt, nothing posted. **Deviation:** the plan specifies `gh` logged-out; the `gh`-absent path exercises the same exit-3 auth/service-failure branch without disturbing the user's `gh` session. |

---

## 7. Failures and risks

### 7.1 FAIL — M3-E10 granularity-band gate contradicts the implementation

- **What:** Plan PASS gate `coarse ∈ [3,5]` vs shipped skill `coarse 1–3`.
- **Evidence:** `design/m0-m5-evaluation-plan.md:634,639` ("coarse 3–5"…"coarse ∈ [3,5]") vs `skills/prd-to-mvp/SKILL.md:54` ("`coarse` aims for 1–3 phases"), `:79–80`, `:95–96` ("`coarse` 1–3"). `skills/planning/SKILL.md` defers to the same bands.
- **Impact:** Anyone running M3-E10 as written would mark a correct 1–2-phase coarse decomposition as FAIL. `standard`/`fine` bands are consistent and unaffected.
- **Disposition:** Not fixed — choosing the canonical band (relax the plan to `[1,5]`/`1–3`, or change the skill) is a maintainer decision, not a typo. The behavioural eval itself remains NOT RUN (agent-driven).

### 7.2 Finding — `bin/check-state-cap` does not validate `--cap`

- **What:** `bin/check-state-cap --cap=abc --check` → exit **1** with a leaked
  bash error (`bin/check-state-cap: line 57: [: abc: integer expression expected`)
  and a nonsensical message ("over cap abc"), instead of exit **2** for an
  invocation error.
- **Evidence:** `bin/check-state-cap:34` parses `--cap=*` without numeric
  validation; line 57's `[ "$LINES" -le "$CAP" ]` fails on non-integer `$CAP`.
  The script's own header (line 20) promises "2 invocation error".
- **Scope:** *Out of scope for M4-E08*, which the plan limits to envelope-using
  scripts; `check-state-cap` does not source `bin/lib/json-envelope.sh`. So
  M4-E08 PASSes, but the bug is real.
- **Suggested fix:** validate `--cap` is a non-negative integer and `exit 2`
  with a clean message otherwise.

### 7.3 Risk — M1-E03 literal gate over-counts deliberate prose hints

- The "0 raw `{{…}}` tokens" gate counts the 2 documented free-form prose hints
  (template line 60). Recommend the gate read "0 unresolved `{{UPPER_SNAKE}}`
  substitution tokens" (which passes), and assert exactly the known prose hints
  remain. Recorded PASS on the meaningful gate.

### 7.4 Risk — M0-E01/E06/NEG-10 casing checks are blind on macOS

- `test -d Design` (M0-E01) is a false positive on case-insensitive FS, and the
  casing-regression guards (M0-E06/NEG-10) cannot catch the original bug here.
  Verified via **git** instead (only lowercase `design/` tracked). These evals
  must run at least once on a case-sensitive FS (Linux/CI) to be meaningful.

### 7.5 Risk — M5-E13 live network paths remain unverified

- The real provider call and real `gh api …/reviews` post are still
  `bash -n`-clean-but-never-executed. The offline suite proves the harness +
  normalisation; it cannot prove the un-mocked network payload/response paths.
  Pre-release, run M5-E13 once on a scratch PR.

---

## 8. Not-run rationale

All 12 NOT-RUN evals require an action the task scoped out (real GitHub writes,
real provider keys, human prose/UX judgement, or interactive agent-driven
slash-command behaviour). None has a fully-offline path defined by the plan.
For each, the plan's offline/structural substitute was executed (recorded
inline in §6):

| ID | Why not run | Substitute executed |
|---|---|---|
| M1-E02 | Live GitHub tutorial flow | 5 tutorial skills present, in handoff order |
| M1-E05 | Agent/model-driven artifact generation | intake skills present |
| M1-E06 | Agent/model-driven planning | planning skills present |
| M3-E03 | Agent-driven `/start` routing | `start` skill reads `state.md` |
| M3-E06 | Agent-driven `/pause`→`/resume` | both skills present |
| M3-E11 | Agent-driven lifecycle (+ dry-run) | 3 skills present; dry-run documented |
| M3-E12 | Agent-driven `/feature` | `feature-prd` + reference addendum present |
| M5-E12 | Live `/review-pr --publish` to a real PR | protocol verified piecewise offline |
| M5-E13 | Real provider + real `gh api` post | none possible offline (un-mocked paths) |
| E2E-01 | Full live flow | verb/handoff graph closes |
| E2E-02 | Live follow-up feature flow | addendum machinery present |
| E2E-03 | Agent-driven session continuity | state zones validated |

The interactive behavioural halves of M3-E01 and M3-E02 (`[SM]`) were likewise
not interactively driven, but their objective documented anchors (token set,
mode×category matrix) were verified, so those two are recorded PASS.

---

## 9. Generated artifacts

All ephemeral, under `mktemp -d` (auto-cleaned by the OS); no tracked file was
mutated. Representative paths from this run:

| Artifact | Path (this run) | Eval |
|---|---|---|
| Throwaway install target | `…/tmp.G3W5JvryWv/demo` | M0-E06/E07/E08, M1-E03 |
| M5 review out dir | `…/tmp.Y3X4cHe0F3` (`pr-1-e958c428.{json,md}`) | M5-E02/E03/E04/E06/E07/E08/E10 |
| Temp receipts dirs | `mktemp -d` per eval (`demo__k1.json`, `publish-review__pr-1.json`) | M4-E03, M5-E07/E08 |
| Temp kit.json/skills copies | `mktemp -d` per NEG eval | NEG-01/02/03 |
| Bad fixtures | `/tmp/bad-adr.md`, `/tmp/bad-prompt.md`, `/tmp/bad-block.md`, `/tmp/bad-pattern.md`, `/tmp/bad-resp.txt` | M3-E07/E08, M4-E02, NEG-06 |
| Skills-audit CSV (regenerated in place, identical) | `notes/skills-audit-2026-05-07/skills-audit.csv` | M0-E09 |

The only tracked file this report adds is itself:
`design/m0-m5-evaluation-report-20260605.md`.

---

## 10. Follow-ups and recommendations

1. **Resolve the M3-E10 band conflict (FAIL).** Decide the canonical `coarse`
   band and align plan ↔ skills. Recommended: change the plan gate to match the
   shipped `coarse 1–3` (the implementation is the source of truth), or add a
   superseding note in the plan.
2. **Harden `bin/check-state-cap` (§7.2).** Reject a non-numeric `--cap` with
   `exit 2` and a clean message; add `--cap=<non-numeric>` to M4-E08's probe
   matrix so the contract is guarded.
3. **Refine the M1-E03 gate wording (§7.3)** to "0 unresolved `{{UPPER_SNAKE}}`
   substitution tokens" and enumerate the expected prose hints.
4. **Make the casing evals FS-aware (§7.4).** Replace `test -d Design` with a
   git-based check (`git ls-files | grep -q '^Design/'`) and mark M0-E06/NEG-10
   as CI-only (case-sensitive FS) in the plan.
5. **Schedule M5-E13 pre-release (§7.5)** to exercise the un-mocked
   provider/`gh api` paths once on a scratch PR.
6. **Optional:** promote the troubleshooting "unresolved placeholders" remedy
   (M1-E04) to its own symptom heading.

None of 1–6 blocks the kit's offline health: the per-PR/CI surface and the
`RELEASE-READY` gate are green.

---

## 11. Validation commands run after writing this report

The following were run from the kit root after the report was written, to
confirm the report's claims and leave the tree healthy. Results appended below
on commit (see PR):

```bash
# 1. Report exists and path/structure sanity
test -f design/m0-m5-evaluation-report-20260605.md && wc -l design/m0-m5-evaluation-report-20260605.md
grep -c '^## ' design/m0-m5-evaluation-report-20260605.md          # expect 11 top-level sections

# 2. Internal links in the report resolve (it links the plan)
#    front-door-style resolver over the report only
python3 - <<'PY'
import re,os
f='design/m0-m5-evaluation-report-20260605.md'; d=os.path.dirname(f); bad=[]
for i,l in enumerate(open(f),1):
    for m in re.finditer(r'\]\(([^)]+)\)', l):
        t=m.group(1).split()[0]
        if t.startswith(('http','#','mailto:')): continue
        p=t.split('#',1)[0]
        if p and not os.path.exists(os.path.normpath(os.path.join(d,p))): bad.append((i,t))
print('broken report links:', bad)
PY

# 3. Kit-wide gates still green (report adds only a tracked .md; must not perturb)
bin/check-consistency
bin/self-test
bin/validate-kit-json
bin/check-state-cap --check

# 4. Working tree contains only the new report
git status --porcelain
```
