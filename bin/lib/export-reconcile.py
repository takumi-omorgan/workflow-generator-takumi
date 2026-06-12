#!/usr/bin/env python3
"""export-reconcile.py — drop dangling references to the pruned public-export
tooling from a staging tree (issue #16, ADR-056).

The export tooling (bin/export-public, bin/check-public-export, bin/export-eval,
their lib helpers and fixtures, and docs/publishing.md) is source-repo only and
is pruned from the public artifact by bin/export-public. This step removes the
metadata that would otherwise dangle and fail the in-export validation gates:

  - kit.json: drop the bin[] entries for the pruned scripts (else
    check-consistency C3 flags a registered path with no file), and drop
    contract pointers into excluded private paths (the contract's `adr`
    points at the kit's own design/adr set, which never ships)
  - bin/self-test: drop the `export-eval` step (else a public self-test calls
    a script that no longer ships)
  - docs/README.md: drop the publishing.md index row (else a dangling link)

Deterministic and idempotent. Usage: export-reconcile.py STAGING_DIR
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_paths import is_excluded  # noqa: E402

DEST = sys.argv[1]

PRUNED_BIN_PATHS = {
    "bin/check-public-export",
    "bin/export-public",
    "bin/export-eval",
}


def reconcile_kit_json():
    path = os.path.join(DEST, "kit.json")
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as fh:
        kit = json.load(fh)
    before = kit.get("bin", [])
    kit["bin"] = [b for b in before if b.get("path") not in PRUNED_BIN_PATHS]
    contract = kit.get("contract")
    if isinstance(contract, dict):
        kit["contract"] = {
            k: v for k, v in contract.items()
            if not (isinstance(v, str) and is_excluded(v))
        }
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(kit, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def drop_lines(path, predicate):
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    kept = [ln for ln in lines if not predicate(ln)]
    if kept != lines:
        with open(path, "w", encoding="utf-8") as fh:
            fh.writelines(kept)


reconcile_kit_json()
# self-test step line, e.g.:  step "export-eval"  0 bin/export-eval
drop_lines(os.path.join(DEST, "bin", "self-test"),
           lambda ln: "bin/export-eval" in ln)
# docs/README.md index row for the pruned runbook
drop_lines(os.path.join(DEST, "docs", "README.md"),
           lambda ln: "publishing.md" in ln)
