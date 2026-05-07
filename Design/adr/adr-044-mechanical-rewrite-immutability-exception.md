
# ADR-044: Mechanical path-string rewrite as an exception to ADR immutability

**Status:** accepted
**Date:** 2026-05-07

## Context

The kit's standing rule is *"never edit accepted ADRs in place — supersede instead."* Its purpose is to protect the **meaning** of recorded decisions: a reader returning to ADR-007 a year from now should see the same claim the team accepted, not a quietly rewritten version. The rule appears in `CLAUDE.md` and is one of the kit's load-bearing conventions.

The rule, however, also blocks purely mechanical changes where the meaning of a sentence is unchanged. Concrete trigger: refactoring-ideas entry #7 (rename `Design/` → `design/`) would touch ~58 occurrences across 16 accepted ADRs without changing what any of those ADRs decided. The rename is a path-string substitution; the surrounding claims (e.g. *"Generate core docs into `Design/adr/`"* → *"Generate core docs into `design/adr/`"*) are identical in intent and decision content.

Without a defined exception, every directory rename or kit-wide identifier change forces a binary choice: either (a) abandon historical ADRs to read with stale paths indefinitely, with readers chasing supersession chains for trivial lookups, or (b) supersede 16+ ADRs at once for a single mechanical rewrite, drowning the supersession mechanism in noise it was not designed to carry. Both outcomes degrade the kit's documentation as it evolves.

## Options considered

### Option A: Authorise mechanical path-string rewrite as an explicit exception

- Pros: enables cleanup refactors (renames) without ADR cascade; preserves meaning-protection where it matters; defines "mechanical" precisely so the exception does not drift into editorial changes; pays forward for any future rename, not just the `Design/` → `design/` case.
- Cons: introduces an exception class to an otherwise simple rule; reviewers must verify each rewrite qualifies as mechanical before merging.

### Option B: No exception — leave the rule strict

- Pros: zero rule change; full strictness preserved; reviewer judgement never required.
- Cons: every rename either leaves stale path strings in historical ADRs (option a above) or triggers a supersession cascade (option b above); kit-wide consistency degrades as the kit evolves; the `Design/` → `design/` rename in particular is blocked or made unreasonably costly.

### Option C: Hybrid — top-of-file footnote in each affected ADR instead of body rewrite

- Pros: keeps body text untouched, closest to the letter of the rule.
- Cons: 16+ manual footnotes per rename; each new rename adds another footnote; ADR top-matter accumulates indefinitely; readers must mentally apply N path substitutions when reading older ADRs.

## Decision

Adopt **Option A**. Mechanical path-string rewrites are an explicit exception to the "never edit accepted ADRs in place" rule. A rewrite qualifies as mechanical when **all three** of the following hold:

1. Only path strings or identifier strings change (e.g. `Design/` → `design/`, `bin/foo.sh` → `bin/foo`, a renamed skill directory).
2. The surrounding prose's claim is unchanged — the ADR still decides what it decided, just with the new name.
3. Every occurrence in the ADR body changes uniformly (no partial rewrites that leave a mix of old and new strings within one ADR).

Editorial changes — anything that alters what an ADR decided, the rationale, the options weighed, or the consequences — still require supersession. `CLAUDE.md`'s immutability paragraph gains a one-line citation of this exception so the rule and its exception are read together.

## Consequences

- Renames (directory, file, kit-wide identifier) become possible without abandoning historical ADRs to stale paths or triggering a supersession cascade.
- The supersession mechanism stays reserved for genuine meaning changes — the rule's original purpose is preserved where it matters.
- `CLAUDE.md` gains a one-line citation of this exception alongside the immutability rule, so future contributors discover the exception when they read the rule.
- Reviewers must verify each rewrite satisfies criteria (1)–(3) above before merging; the kit trades a small enforcement cost for a much larger cascade cost avoided. PRs that perform mechanical rewrites should state in the description that they invoke this ADR and list the affected ADR numbers.
