# 2026-06-23 — Codex review of public release (v5.0.0)

## What was reviewed

Codex adversarially reviewed the **public** kit repo
(`olivermorgan2/claude-workflow-kit`, released at **v5.0.0**) and filed 7
findings. We verified each against the **source** repo
(`takumi-omorgan/workflow-generator-takumi`), not the reviewer's `/private/tmp`
copy.

> **Correction (2026-06-23, second pass).** The first-pass verdict below was
> written against a stale read of the source tree (assumed `v4.0.0`, with the
> v5 command model, docs, and validation scripts "absent from source"). That
> is **wrong for current source**: `kit.json` is at `kitVersion 5.0.0`, the
> `start` router skill exists under `skills/start/`, and `docs/architecture.md`,
> `docs/workflow-control.md`, `docs/workflow-guide.md`,
> `docs/claude-code-guide.md`, plus `bin/self-test`, `bin/validate-kit-json`,
> `bin/validate-carry-forward`, and `bin/check-consistency` all exist in source.
> The findings are therefore **mostly source-content/doc polish and false
> positives**, not transform-created divergence. The re-verified dispositions
> and the fixes actually shipped are in **[Corrected dispositions](#corrected-dispositions-second-pass)**
> below; the original first-pass text is retained beneath it as an audit trail.

## Corrected dispositions (second pass)

Re-verified against current source (`kit.json` 5.0.0). Net: **4 of 7 are
source-actionable doc/content fixes (now fixed), 3 are confirmed false
positives.** None are transform-created.

- **Finding 1 (`jq` prerequisite) — VALID, fixed.** The first pass called this
  invalid ("only `gh --jq`"). Wrong: standalone `jq` is used in shipped,
  target-installed helpers — `bin/fence`, `bin/adr-alloc`,
  `bin/changelog-collect`, `bin/release-suggest`, `bin/pr-context`,
  `bin/docs-render` (the installer's `DEFAULT_BIN` set, copied into a target's
  `.claude/bin/`), and `bin/self-test` literally gates on `for tool in python3
  jq bash`. `jq` is a real runtime prerequisite. **Fix:** added `jq` to the
  prerequisites table + verify block in `docs/install.md` and to the
  prerequisites line in `README.md`.
- **Finding 7 (`docs/github-setup.md`) — VALID, fixed.** "What's next" marked
  `workflow-guide.md` and `claude-code-guide.md` as "coming in a later issue"
  (both exist) and linked a non-existent `adr-guide.md`. **Fix:** turned the
  two existing docs into live links, dropped the "coming later" hedging, and
  replaced the `adr-guide.md` line with `docs/skills.md` (which covers
  `/adr-writer`). Also fixed the stale `olivermorgan2/workflow-generator` repo
  name in the labels note → `olivermorgan2/claude-workflow-kit`.
- **Findings 2 + 3 (verb/alias ambiguity) — VALID as a doc-clarity issue,
  fixed.** Not "commands that don't exist": `/start` **is** an installed router
  skill (`skills/start/`) and `docs/workflow-control.md` already documents the
  verb→skill map precisely (only `/start`/`/next`, `/feature-prd`, `/review-pr`
  are new slash commands; `/decide`, `/backlog`, `/work`, `/ship` are
  documentation aliases for existing skills). `README.md` and
  `docs/architecture.md` presented all six verbs flatly, implying each is an
  installed command. **Fix:** clarified both to distinguish the installed
  `/start` router from the documentation-alias verbs, pointing at
  `workflow-control.md`.
- **Findings 4 + 6 — FALSE POSITIVE, no change.** Finding 4: the release SKILL
  anchor matches its heading's GitHub slug. Finding 6: the flagged links are
  inside fenced code blocks, so they render literally, not as clickable links.
- **Finding 5 ("example links 404") — FALSE POSITIVE in substance, no change.**
  The URLs are inside code blocks (illustrative example output, not active
  links users follow) and the only live install/bootstrap commands in
  `README.md` / `docs/install.md` are already correct
  (`olivermorgan2/claude-workflow-kit` @ `v5.0.0`). The naming/version was
  already reconciled in current source; the remaining `olivermorgan2/workflow-generator`
  / `v3.3.0` strings live only in historical `CHANGELOG.md` entries, internal
  `design/`/`notes/`/`prompts/` material (stripped from the public export), the
  `bin/export-eval-fixtures/stale-version/` test fixture (intentionally stale),
  and skill `example.md` illustrations — all correctly left untouched per the
  "don't rewrite historical/example content" rule.

## Verdict (first pass — superseded by the correction above)

Codex's automated checks on the public repo passed (`bin/self-test` 20/20,
`validate-kit-json`, `validate-carry-forward`, `check-consistency`,
`check-state-cap`, `bash -n`, release v5.0.0 latest, bootstrap asset 200).
**But:** the reviewed public state has diverged from this source — see
[risks.md](../risks.md) R2 and [open-questions.md](../open-questions.md) Q2.
Most findings have no source counterpart.

## Distilled findings (first pass — superseded; see corrected dispositions above)

- **Valid in source (1):** Finding 7 — `docs/github-setup.md` marks
  `workflow-guide.md` and `claude-code-guide.md` as "coming in a later issue"
  though both exist, and references a non-existent `adr-guide.md`.
- **Invalid in source (3):** Finding 1 — only `jq` use is `gh --jq` (a gh flag,
  not the binary); no source script needs standalone `jq`. Finding 4 — release
  SKILL anchor matches its heading's GitHub slug (em-dash between spaces yields
  the double hyphen). Finding 6 — placeholder links are inside fenced code
  blocks, so they render literally, not as clickable links.
- **Invalid-as-stated / partially valid (1):** Finding 5 — "example links 404":
  the URLs are inside code blocks (not clickable) and some SHAs are truncated;
  the real issue is the repo-name inconsistency, tracked under Q1.
- **Not applicable to source (2):** Findings 2 and 3 reference commands
  (`/start`, `/next`, `/decide`, `/backlog`, `/work`, `/ship`) and files
  (`agent-contract.md`, `architecture.md`, `workflow-control.md`) that do not
  exist anywhere in source history.

## Durable lessons

- **Verify findings against the source tree at its *current* HEAD, not a
  remembered version.** The first pass assumed `v4.0.0` and declared half the
  findings "absent from source"; current source is `v5.0.0` and the files all
  exist. Read `kit.json`/`git tag`/the tree before asserting divergence.
- **Code-fenced placeholders are not broken links.** Before flagging a link,
  check whether it is inside a fenced or inline code span, because those render
  literally. (Finding 5/6 — confirmed false positives.)
- **`gh --jq` is not the only `jq` in the kit.** The first pass stopped at
  `gh --jq` and missed the standalone `jq` in six target-installed helpers and
  in `bin/self-test`'s tool gate. When auditing a prerequisite, grep the whole
  shipped script set, not just the obvious call site.

## Resolution / disposition (corrected)

Implemented this pass as source fixes (no public re-export — user runs a fresh
export later):

- **Finding 1:** added `jq` to prerequisites in `docs/install.md` + `README.md`.
- **Finding 7:** de-staled `docs/github-setup.md` "What's next" (live links,
  dropped "coming later", replaced non-existent `adr-guide.md` with
  `docs/skills.md`) and fixed the stale repo name in the labels note.
- **Findings 2 + 3:** clarified the verb layer vs. installed `/start` router in
  `README.md` and `docs/architecture.md`.
- **Findings 4, 5, 6:** confirmed false positives — no change. The naming/version
  in active install commands was already correct (`claude-workflow-kit` @
  `v5.0.0`); remaining old strings are historical/internal/fixture/example and
  intentionally untouched.

The first-pass resolution (below, struck) deferred everything on Q2's
source↔public divergence, which no longer applies.

- ~~Finding 7: fix in source (`docs/github-setup.md`). Small, self-contained.~~
- ~~Findings 1, 4, 6: no source change — invalid here.~~
- ~~Finding 5 + stale bootstrap URL: roll into naming/version reconciliation (Q1).~~
- ~~Findings 2, 3 and the divergence overall: blocked on Q2.~~
