<!-- Fixture: a row naming a profile outside the closed vocabulary
     ({ full }). The parser must HARD-ERROR naming the row. `ship-loop`
     becomes legal only if an ADR amends ADR-061's column vocabulary. -->

# Fixture manifest — unknown profile

schemaVersion: 1

| id | source | dest | required | profiles | ownership | since-version |
|---|---|---|---|---|---|---|
| fixture-kit-json | kit.json | .claude/kit.json | required | ship-loop | kit-owned | 5.0.1 |
