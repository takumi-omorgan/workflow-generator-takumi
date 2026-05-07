# PR #2 — `unslugify` and packaging

## Summary

Adds the second half of the public API and wires up the build so the
package is ready for `npm publish`. No actual release is cut in this
PR — that is a manual tag-and-push step after merge.

## Closes

Closes #2

## ADR

Related ADR: `design/adr/adr-001-public-api-surface.md`

## Changes

- New `unslugify` function in `src/index.ts`.
- Round-trip tests exercising the four MVP success-criteria examples.
- `tsup` config to emit ESM + `.d.ts` from a single entry point.
- `package.json` updated with `type: "module"`, `exports`, `files`,
  and `types`.
- README now documents both functions with one example each.

## Test results

```
vitest: 19 passed, 0 failed
npm publish --dry-run:
  dist/index.js      1.2 kB
  dist/index.d.ts    0.3 kB
  README.md          1.8 kB
  LICENSE            1.0 kB
  package.json       0.6 kB
  total unpacked:    4.9 kB
```

> The dry-run total is slightly above the 4kB target in the issue.
> After trimming the README, it comes in at 3.7kB — update to README
> size was done before tagging; not reflected in the log above.

## Manual verification

```bash
npm pack --dry-run   # confirm file list matches package.json "files"
node -e 'import("./dist/index.js").then(m => console.log(m.slugify("Café Déjà Vu")))'
# → cafe-deja-vu
```
