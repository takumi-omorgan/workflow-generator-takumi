<!--
  Document: runtime-asset manifest
  Filled by: humans (this is hand-curated; not generated)
  Used by: bin/check-manifest (validator); bin/list-runtime-assets
    (parser, planned) and through it the installer, the upgrade
    planner, and profile selection.
  Source-of-truth status: this file IS the source of truth for what
    the kit installs into a target project and who owns each file
    afterwards, per
    design/adr/adr-061-runtime-asset-manifest.md. Adding a runtime
    asset = appending a row here; renaming an id is FORBIDDEN — use
    a new id instead.
-->

# Runtime-asset manifest

schemaVersion: 1

One row per asset `bin/install-workflow-kit` writes into a target
project. The manifest and its validator/parser ship in the kit tree the
installer runs *from* and are deliberately not listed here — the
manifest does not describe itself.

Columns:

- **id** — stable asset ID (lowercase kebab). Consumers join on it;
  never rename one.
- **source** — path in the kit tree, relative to the kit root. A
  trailing `/` marks a directory copied recursively.
- **dest** — install path, relative to the target project root.
- **required** — `required` assets are installed on every default run;
  a missing *source* is a fail-fast installer error. `optional` assets
  are flag-gated (`--with-ai-review`, `--with-docs`, `--license`); a
  missing source warns and continues.
- **profiles** — closed vocabulary, currently exactly `full`. New
  values require an ADR amending ADR-061's column vocabulary.
- **ownership** — closed vocabulary `kit-owned | generated |
  user-seeded`. `kit-owned` files may be replaced by a kit upgrade when
  unmodified; `generated` files are rendered from a template at install
  time and never touched again; `user-seeded` files are seeded once and
  belong to the target project thereafter.
- **since-version** — kit version at which the asset appeared.
  Informational only; nothing validates it beyond presence and nothing
  may branch on it. Assets predating this manifest are recorded at the
  manifest's introduction baseline (`5.0.1`).

| id | source | dest | required | profiles | ownership | since-version |
|---|---|---|---|---|---|---|
| skill-adr-writer | skills/adr-writer/ | .claude/skills/adr-writer/ | required | full | kit-owned | 5.0.1 |
| skill-audit-milestone | skills/audit-milestone/ | .claude/skills/audit-milestone/ | required | full | kit-owned | 5.0.1 |
| skill-changelog | skills/changelog/ | .claude/skills/changelog/ | required | full | kit-owned | 5.0.1 |
| skill-check-plan | skills/check-plan/ | .claude/skills/check-plan/ | required | full | kit-owned | 5.0.1 |
| skill-clarify | skills/clarify/ | .claude/skills/clarify/ | required | full | kit-owned | 5.0.1 |
| skill-claude-issue-executor | skills/claude-issue-executor/ | .claude/skills/claude-issue-executor/ | required | full | kit-owned | 5.0.1 |
| skill-complete-milestone | skills/complete-milestone/ | .claude/skills/complete-milestone/ | required | full | kit-owned | 5.0.1 |
| skill-feature-prd | skills/feature-prd/ | .claude/skills/feature-prd/ | required | full | kit-owned | 5.0.1 |
| skill-idea-to-prd | skills/idea-to-prd/ | .claude/skills/idea-to-prd/ | required | full | kit-owned | 5.0.1 |
| skill-issue-planner | skills/issue-planner/ | .claude/skills/issue-planner/ | required | full | kit-owned | 5.0.1 |
| skill-milestone-summary | skills/milestone-summary/ | .claude/skills/milestone-summary/ | required | full | kit-owned | 5.0.1 |
| skill-pause | skills/pause/ | .claude/skills/pause/ | required | full | kit-owned | 5.0.1 |
| skill-planning | skills/planning/ | .claude/skills/planning/ | required | full | kit-owned | 5.0.1 |
| skill-pr-review-packager | skills/pr-review-packager/ | .claude/skills/pr-review-packager/ | required | full | kit-owned | 5.0.1 |
| skill-prd-normalizer | skills/prd-normalizer/ | .claude/skills/prd-normalizer/ | required | full | kit-owned | 5.0.1 |
| skill-prd-to-mvp | skills/prd-to-mvp/ | .claude/skills/prd-to-mvp/ | required | full | kit-owned | 5.0.1 |
| skill-prepare-issue | skills/prepare-issue/ | .claude/skills/prepare-issue/ | required | full | kit-owned | 5.0.1 |
| skill-release | skills/release/ | .claude/skills/release/ | required | full | kit-owned | 5.0.1 |
| skill-resume | skills/resume/ | .claude/skills/resume/ | required | full | kit-owned | 5.0.1 |
| skill-review-pr | skills/review-pr/ | .claude/skills/review-pr/ | optional | full | kit-owned | 5.0.1 |
| skill-start | skills/start/ | .claude/skills/start/ | required | full | kit-owned | 5.0.1 |
| skill-workflow-docs | skills/workflow-docs/ | .claude/skills/workflow-docs/ | required | full | kit-owned | 5.0.1 |
| bin-sync-adr-index | bin/sync-adr-index | .claude/bin/sync-adr-index | required | full | kit-owned | 5.0.1 |
| bin-fence | bin/fence | .claude/bin/fence | required | full | kit-owned | 5.0.1 |
| bin-adr-alloc | bin/adr-alloc | .claude/bin/adr-alloc | required | full | kit-owned | 5.0.1 |
| bin-changelog-collect | bin/changelog-collect | .claude/bin/changelog-collect | required | full | kit-owned | 5.0.1 |
| bin-release-suggest | bin/release-suggest | .claude/bin/release-suggest | required | full | kit-owned | 5.0.1 |
| bin-pr-context | bin/pr-context | .claude/bin/pr-context | required | full | kit-owned | 5.0.1 |
| bin-docs-render | bin/docs-render | .claude/bin/docs-render | required | full | kit-owned | 5.0.1 |
| bin-check-plan | bin/check-plan | .claude/bin/check-plan | required | full | kit-owned | 5.0.1 |
| lib-json-envelope | bin/lib/json-envelope.sh | .claude/bin/lib/json-envelope.sh | required | full | kit-owned | 5.0.1 |
| lib-fences | bin/lib/fences.py | .claude/bin/lib/fences.py | required | full | kit-owned | 5.0.1 |
| lib-carryforward-read | bin/lib/carryforward_read.py | .claude/bin/lib/carryforward_read.py | required | full | kit-owned | 5.0.1 |
| lib-check-plan-eval | bin/lib/check-plan-eval.sh | .claude/bin/lib/check-plan-eval.sh | required | full | kit-owned | 5.0.1 |
| bin-review-pr | bin/review-pr | .claude/bin/review-pr | optional | full | kit-owned | 5.0.1 |
| bin-publish-review | bin/publish-review | .claude/bin/publish-review | optional | full | kit-owned | 5.0.1 |
| bin-review-eval | bin/review-eval | .claude/bin/review-eval | optional | full | kit-owned | 5.0.1 |
| bin-write-receipt | bin/write-receipt | .claude/bin/write-receipt | optional | full | kit-owned | 5.0.1 |
| lib-review-common | bin/lib/review_common.py | .claude/bin/lib/review_common.py | optional | full | kit-owned | 5.0.1 |
| lib-review-build-request | bin/lib/review-build-request.py | .claude/bin/lib/review-build-request.py | optional | full | kit-owned | 5.0.1 |
| lib-review-render | bin/lib/review-render.py | .claude/bin/lib/review-render.py | optional | full | kit-owned | 5.0.1 |
| lib-review-publish | bin/lib/review-publish.py | .claude/bin/lib/review-publish.py | optional | full | kit-owned | 5.0.1 |
| lib-review-eval-check | bin/lib/review-eval-check.py | .claude/bin/lib/review-eval-check.py | optional | full | kit-owned | 5.0.1 |
| ai-review-prompts | ai-review/prompts/ | .claude/ai-review/prompts/ | optional | full | kit-owned | 5.0.1 |
| ai-review-eval | ai-review/eval/ | .claude/ai-review/eval/ | optional | full | kit-owned | 5.0.1 |
| ai-review-readme | ai-review/README.md | .claude/ai-review/README.md | optional | full | kit-owned | 5.0.1 |
| ai-review-config-example | ai-review/config.example.json | .claude/ai-review/config.example.json | optional | full | kit-owned | 5.0.1 |
| schema-ai-review-config | schemas/ai-review-config.v1.yaml | .claude/schemas/ai-review-config.v1.yaml | optional | full | kit-owned | 5.0.1 |
| schema-ai-review-artifact | schemas/ai-review-artifact.v1.yaml | .claude/schemas/ai-review-artifact.v1.yaml | optional | full | kit-owned | 5.0.1 |
| prompt-template | prompts/_template.md | prompts/_template.md | required | full | kit-owned | 5.0.1 |
| template-adr | templates/adr-template.md | templates/adr-template.md | required | full | kit-owned | 5.0.1 |
| template-ai-summary | templates/ai-summary-template.md | templates/ai-summary-template.md | required | full | kit-owned | 5.0.1 |
| template-architecture | templates/architecture-template.md | templates/architecture-template.md | required | full | kit-owned | 5.0.1 |
| template-build-out-plan | templates/build-out-plan-template.md | templates/build-out-plan-template.md | required | full | kit-owned | 5.0.1 |
| template-decisions | templates/decisions-template.md | templates/decisions-template.md | required | full | kit-owned | 5.0.1 |
| template-issue | templates/issue-template.md | templates/issue-template.md | required | full | kit-owned | 5.0.1 |
| template-milestone-summary | templates/milestone-summary-template.md | templates/milestone-summary-template.md | required | full | kit-owned | 5.0.1 |
| template-mvp | templates/mvp-template.md | templates/mvp-template.md | required | full | kit-owned | 5.0.1 |
| template-planning | templates/planning-template.md | templates/planning-template.md | required | full | kit-owned | 5.0.1 |
| template-pr | templates/pr-template.md | templates/pr-template.md | required | full | kit-owned | 5.0.1 |
| template-prd | templates/prd-template.md | templates/prd-template.md | required | full | kit-owned | 5.0.1 |
| template-readme | templates/readme-template.md | templates/readme-template.md | required | full | kit-owned | 5.0.1 |
| template-state | templates/state-template.md | templates/state-template.md | required | full | kit-owned | 5.0.1 |
| github-pr-template | .github/pull_request_template.md | .github/pull_request_template.md | required | full | user-seeded | 5.0.1 |
| gitignore | templates/gitignore.target | .gitignore | required | full | user-seeded | 5.0.1 |
| adr-readme | templates/adr-readme-template.md | design/adr/README.md | required | full | user-seeded | 5.0.1 |
| claude-md | templates/claude-md-template.md | CLAUDE.md | required | full | generated | 5.0.1 |
| docs-workflow-kit | docs/ | docs/workflow-kit/ | optional | full | kit-owned | 5.0.1 |
| license-mit | templates/licenses/mit.txt | LICENSE | optional | full | generated | 5.0.1 |

Notes:

- `lib-json-envelope` is listed once even though the installer's
  default-helper and AI-review copy loops both name it: one dest, one
  row. It is `required` because the default helpers source it.
- The AI-review rows (`optional`) are gated by `--with-ai-review`,
  `docs-workflow-kit` by `--with-docs`, and `license-mit` by
  `--license=mit`. `skill-review-pr` installs only with
  `--with-ai-review`.
- `prompt-template`'s historical fallback source
  (`notes/issue-prompt.md`) is not listed; the canonical source is
  `prompts/_template.md`.
- `templates/prd-addendum-template.md` exists in the kit tree but is
  not currently installed by `bin/install-workflow-kit`, so it has no
  row. Adding it to the install contract is a one-row change here once
  the installer derives from this manifest.
