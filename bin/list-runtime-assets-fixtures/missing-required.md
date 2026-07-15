<!-- Fixture: a REQUIRED asset whose source does not exist in the kit
     tree. Default: fail-fast naming the row. With --allow-missing: the
     row is downgraded to a warning, omitted from output, and the parser
     exits 0 with a banner. -->

# Fixture manifest — missing required source

schemaVersion: 1

| id | source | dest | required | profiles | ownership | since-version |
|---|---|---|---|---|---|---|
| fixture-present | kit.json | .claude/kit.json | required | full | kit-owned | 5.0.1 |
| fixture-missing | does/not/exist.md | .claude/missing.md | required | full | kit-owned | 5.0.1 |
