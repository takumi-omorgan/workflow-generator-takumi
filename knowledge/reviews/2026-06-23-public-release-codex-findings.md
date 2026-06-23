# 2026-06-23 — Codex review of public release (v5.0.0)

## What was reviewed

Codex adversarially reviewed the **public** kit repo
(`olivermorgan2/claude-workflow-kit`, released at **v5.0.0**) and filed 7
findings. We verified each against the **source** repo
(`takumi-omorgan/workflow-generator-takumi`), not the reviewer's `/private/tmp`
copy.

## Verdict

Codex's automated checks on the public repo passed (`bin/self-test` 20/20,
`validate-kit-json`, `validate-carry-forward`, `check-consistency`,
`check-state-cap`, `bash -n`, release v5.0.0 latest, bootstrap asset 200).
**But:** the reviewed public state has diverged from this source — see
[risks.md](../risks.md) R2 and [open-questions.md](../open-questions.md) Q2.
Most findings have no source counterpart.

## Distilled findings (source disposition)

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

- **Verify findings against the source tree, not a copied review path** — line
  numbers and even whole files differ between public and source.
- **Code-fenced placeholders are not broken links.** Before flagging a link,
  check whether it is inside a fenced or inline code span, because those render
  literally.
- **`gh --jq` is not a `jq` dependency.** Distinguish gh's built-in flag from
  the standalone binary when auditing prerequisites.

## Resolution / disposition

- Finding 7: fix in source (`docs/github-setup.md`). Small, self-contained.
- Findings 1, 4, 6: no source change — invalid here. Re-verify on the public
  side if/when public re-syncs from source.
- Finding 5 + the stale/wrong bootstrap URL (`olivermorgan2/workflow-generator`
  @ v3.3.0): roll into the naming/version reconciliation (Q1).
- Findings 2, 3 and the divergence overall: blocked on Q2 (how source relates
  to public v5.0.0). No public-release fixes implemented this pass.
