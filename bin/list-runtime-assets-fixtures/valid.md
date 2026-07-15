<!-- Fixture: a minimal well-formed manifest. Sources are real kit-root
     files so source-existence passes when run from the kit root
     (bin/self-test). Used to prove the parser emits the profile-filtered
     asset list and exits 0. -->

# Fixture manifest — valid

schemaVersion: 1

| id | source | dest | required | profiles | ownership | since-version |
|---|---|---|---|---|---|---|
| fixture-kit-json | kit.json | .claude/kit.json | required | full | kit-owned | 5.0.1 |
| fixture-readme | README.md | .claude/README.md | optional | full | kit-owned | 5.0.1 |
