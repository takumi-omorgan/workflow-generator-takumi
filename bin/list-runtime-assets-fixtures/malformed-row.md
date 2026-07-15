<!-- Fixture: a malformed row (6 cells, missing the since-version column).
     The parser must HARD-ERROR naming the row, never silently drop it. -->

# Fixture manifest — malformed row

schemaVersion: 1

| id | source | dest | required | profiles | ownership | since-version |
|---|---|---|---|---|---|---|
| fixture-kit-json | kit.json | .claude/kit.json | required | full | kit-owned |
