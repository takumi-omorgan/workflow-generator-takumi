#!/usr/bin/env python3
"""check-public-export.py — deterministic public-export contract checker.

Pure function of a staging directory's contents (issue #16, ADR-056). Reads
the tree, never writes. Emits a JSON object on stdout:

    {"exit": 0|1, "status": "...", "outputs": {...}, "text": "..."}

Configured via environment (set by the bin/check-public-export wrapper):
    STAGING          path to the staging tree (required)
    VERSION          release version being exported, e.g. v4.1.0 (optional)
    SOURCE_OWNER     old source owner that must not leak (e.g. takumi-omorgan)
    SOURCE_REPO      old source repo owner/name (e.g. takumi-omorgan/workflow-generator-takumi)
    OLD_PUBLIC_REPO  superseded public repo owner/name (e.g. olivermorgan2/workflow-generator)
    PUBLIC_REPO      the new public repo owner/name (allowed)

The check IDs (A..L) mirror the wrapper's header.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_paths import (  # noqa: E402
    PIN_CONTEXT_RE, PRIVATE_SECTION_HEADINGS, VERSION_TAG_RE, classify_link,
    gitignore_line_is_private, heading_anchor, is_excluded, is_export_fixture,
    link_target_relpath,
)

STAGING = os.environ["STAGING"]
VERSION = os.environ.get("VERSION", "").strip()
SOURCE_OWNER = os.environ.get("SOURCE_OWNER", "").strip()
SOURCE_REPO = os.environ.get("SOURCE_REPO", "").strip()
OLD_PUBLIC_REPO = os.environ.get("OLD_PUBLIC_REPO", "").strip()
PUBLIC_REPO = os.environ.get("PUBLIC_REPO", "").strip()

# Top-level entries permitted in a public export. Anything else at the root
# is a leak (e.g. design/, notes/, archive/, .hermes/ that the prune missed).
ALLOWED_TOPLEVEL = {
    "README.md", "LICENSE", "CLAUDE.md", "kit.json", "CHANGELOG.md",
    ".gitignore", ".github", "ai-review", "bin", "docs", "examples",
    "prompts", "schemas", "skills", "templates",
}

# Files we scan as text for string-leak checks (E/F). Binary/large dirs are
# skipped by extension. Kept deterministic via sorted walks.
TEXT_EXTS = {
    ".md", ".py", ".sh", ".json", ".yaml", ".yml", ".txt", ".toml",
    ".cfg", ".ini", ".gitignore",
}

problems = []  # each: {"check": "A".."G", "path": str, "detail": str}


def add(check, path, detail):
    problems.append({"check": check, "path": path, "detail": detail})


def rel(p):
    return os.path.relpath(p, STAGING)


def walk_files():
    """Yield every regular file under STAGING, sorted, repo-relative."""
    out = []
    for root, dirs, files in os.walk(STAGING):
        dirs.sort()
        for name in sorted(files):
            full = os.path.join(root, name)
            if os.path.isfile(full) and not os.path.islink(full):
                out.append(full)
    return out


def is_text(path):
    base = os.path.basename(path)
    if base == ".gitignore":
        return True
    _, ext = os.path.splitext(path)
    if ext in TEXT_EXTS:
        return True
    # extensionless scripts (bin/*) are text if they start with a shebang
    try:
        with open(path, "rb") as fh:
            return fh.read(2) == b"#!"
    except OSError:
        return False


def read(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except (UnicodeDecodeError, OSError):
        return None


def exists(relpath):
    return os.path.exists(os.path.join(STAGING, relpath))


# ---- A: allowlisted top-level content only --------------------------------
for entry in sorted(os.listdir(STAGING)):
    if entry == ".git":
        continue  # a working .git is export plumbing, not shipped content
    if entry not in ALLOWED_TOPLEVEL:
        add("A", entry, "unexpected top-level entry not on the public allowlist")

# ---- B: excluded private/source paths absent ------------------------------
# Root-anchored: these must not exist at the export root. Example-project
# trees (examples/projects/*/design/...) are deliberately NOT matched here.
if os.path.isdir(os.path.join(STAGING, "design", "adr")):
    add("B", "design/adr", "kit's own ADR set must not ship (excluded; see docs/architecture.md)")
if os.path.isdir(os.path.join(STAGING, "design", "prd-addenda")):
    add("B", "design/prd-addenda", "internal PRD addenda must not ship")
# root-level design/*.md reports (eval plans, roadmaps, state.md, …)
design_root = os.path.join(STAGING, "design")
if os.path.isdir(design_root):
    for name in sorted(os.listdir(design_root)):
        if name.endswith(".md") and os.path.isfile(os.path.join(design_root, name)):
            add("B", "design/%s" % name, "internal root design document must not ship")
for d in ("notes", "archive", ".hermes"):
    if os.path.exists(os.path.join(STAGING, d)):
        add("B", d, "internal directory must not ship")
if os.path.isfile(os.path.join(STAGING, "ai-review", "config.json")):
    add("B", "ai-review/config.json", "local provider config must not ship")
if os.path.isdir(os.path.join(STAGING, "ai-review", "artifacts")):
    add("B", "ai-review/artifacts", "generated review artifacts must not ship")
# prompts/: only _template.md may ship
prompts_dir = os.path.join(STAGING, "prompts")
if os.path.isdir(prompts_dir):
    for name in sorted(os.listdir(prompts_dir)):
        full = os.path.join(prompts_dir, name)
        if os.path.isfile(full) and name != "_template.md":
            add("B", "prompts/%s" % name,
                "only prompts/_template.md may ship; this internal prompt must not")

# ---- C: required public artifacts present ---------------------------------
if not exists("docs/architecture.md"):
    add("C", "docs/architecture.md", "required public architecture document is missing")
if not exists("prompts/_template.md"):
    add("C", "prompts/_template.md",
        "required template is missing (installer/prepare-issue depend on it)")

# ---- D: markdown links must not point at excluded private/source paths ----
# A relative link is flagged only when it RESOLVES (root-relative) into an
# excluded private/source path — the kit's own design/adr, notes/, archive/,
# root design reports, internal prompts, etc. This is the precise contract
# ("links do not point at excluded private/source paths"): it catches a
# doc/skill/example linking into the excluded kit ADR set, while leaving
# example-project ADR links (which resolve to examples/.../design/adr, NOT
# excluded) and illustrative template placeholders (mvp.md, CLAUDE.md) alone.
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for path in walk_files():
    if not path.endswith(".md"):
        continue
    md_rel = rel(path)
    if is_export_fixture(md_rel):
        continue  # opaque test data: deliberate orphan links live here
    text = read(path)
    if text is None:
        continue
    for m in LINK_RE.finditer(text):
        raw = m.group(1).strip()
        # strip optional markdown link title:  (path "title")
        if " " in raw and not raw.startswith("<"):
            raw = raw.split(" ", 1)[0]
        if classify_link(raw) != "relative":
            continue
        resolved = link_target_relpath(md_rel, raw)
        if resolved is None:
            continue
        if is_excluded(resolved):
            add("D", md_rel,
                "markdown link points at an excluded private/source path: %s "
                "(resolves to %s)" % (raw, resolved))

# ---- E: no stale old-owner / old-repo URL strings -------------------------
# Order matters: the new PUBLIC_REPO legitimately contains the owner, so we
# match the full old forms, plus bare repo slugs that are unambiguous.
leak_strings = []
if SOURCE_REPO:
    leak_strings.append((SOURCE_REPO, "old source repo reference"))
if OLD_PUBLIC_REPO and OLD_PUBLIC_REPO != PUBLIC_REPO:
    leak_strings.append((OLD_PUBLIC_REPO, "superseded public repo reference"))
if SOURCE_OWNER:
    leak_strings.append((SOURCE_OWNER, "old source owner reference"))
# bare old repo basenames (the slug after the slash), if they differ from
# the public slug — catches `workflow-generator-takumi` style mentions
for full in (SOURCE_REPO, OLD_PUBLIC_REPO):
    if "/" in full:
        slug = full.split("/", 1)[1]
        pub_slug = PUBLIC_REPO.split("/", 1)[1] if "/" in PUBLIC_REPO else PUBLIC_REPO
        if slug and slug != pub_slug and slug.endswith("-takumi"):
            leak_strings.append((slug, "old source repo slug"))

for path in walk_files():
    if not is_text(path) or is_export_fixture(rel(path)):
        continue
    text = read(path)
    if text is None:
        continue
    for needle, why in leak_strings:
        if needle and needle in text:
            line_no = text[: text.index(needle)].count("\n") + 1
            add("E", "%s:%d" % (rel(path), line_no), "%s: %r" % (why, needle))

# ---- F: no absolute local / temp / audit paths ----------------------------
# Target real personal/temp paths, not anonymized illustrative ones like
# "/Users/.../my-project" that legitimately appear in example output.
PATH_LEAKS = [
    ("/Users/hermes", "personal macOS home path"),
    ("/home/hermes", "personal Linux home path"),
    ("~/dotfiles", "personal dotfiles path"),
    ("~/src/workflow-generator", "personal source-checkout path"),
    ("/private/var/folders", "macOS temp path"),
    ("/tmp/audit", "temp audit path"),
]
for path in walk_files():
    if not is_text(path) or is_export_fixture(rel(path)):
        continue
    text = read(path)
    if text is None:
        continue
    for needle, why in PATH_LEAKS:
        if needle in text:
            line_no = text[: text.index(needle)].count("\n") + 1
            add("F", "%s:%d" % (rel(path), line_no), "%s: %r" % (why, needle))

# ---- G: no stale version literal in install-surface files -----------------
# Whole-file scan (not just pin-context lines): install surfaces must be
# version-neutral except for the version actually being exported, so a stale
# tag cannot ship even in prose. Beyond the install surfaces, any shipping
# text file's PIN-CONTEXT lines (releases/download, --branch=, …) must carry
# only the export version — the same scope the transform rewrites — so a
# stale pin outside the install surfaces cannot silently ship either.
# examples/ are exempt from blind rewrites and so exempt here too.
if VERSION:
    norm = VERSION if VERSION.startswith("v") else "v" + VERSION
    install_surfaces = ["README.md", "docs/install.md", "bin/bootstrap-workflow-kit"]
    for relpath in install_surfaces:
        full = os.path.join(STAGING, relpath)
        if not os.path.isfile(full):
            continue
        text = read(full)
        if text is None:
            continue
        for lineno, line in enumerate(text.split("\n"), 1):
            for tag in VERSION_TAG_RE.findall(line):
                if tag != norm:
                    add("G", "%s:%d" % (relpath, lineno),
                        "stale version pin %s (export version is %s)" % (tag, norm))
    for path in walk_files():
        relpath = rel(path)
        if relpath in install_surfaces or relpath.startswith("examples/"):
            continue
        if not is_text(path) or is_export_fixture(relpath):
            continue
        text = read(path)
        if text is None:
            continue
        for lineno, line in enumerate(text.split("\n"), 1):
            if not PIN_CONTEXT_RE.search(line):
                continue
            for tag in VERSION_TAG_RE.findall(line):
                if tag != norm:
                    add("G", "%s:%d" % (relpath, lineno),
                        "stale version pin %s on an install/pin-context line "
                        "(export version is %s)" % (tag, norm))

# ---- H: public changelog is curated ----------------------------------------
# The public CHANGELOG.md carries only the current release section, and no
# commit/issue/pull deep links — they point at history the public repo does
# not have. ALLOWED_CHANGELOG_LINK_RES is the explicit policy escape hatch:
# add a compiled regex here to permit a specific deep-link shape.
ALLOWED_CHANGELOG_LINK_RES = ()
DEEP_LINK_RE = re.compile(
    r"https?://github\.com/[^/\s)]+/[^/\s)]+/(?:commit|issues|pull)/\S+")
changelog_path = os.path.join(STAGING, "CHANGELOG.md")
if os.path.isfile(changelog_path):
    text = read(changelog_path)
    if text is not None:
        for lineno, line in enumerate(text.split("\n"), 1):
            for m in DEEP_LINK_RE.finditer(line):
                url = m.group(0).rstrip(")")
                if any(r.search(url) for r in ALLOWED_CHANGELOG_LINK_RES):
                    continue
                add("H", "CHANGELOG.md:%d" % lineno,
                    "deep link into repo history must not ship: %s" % url)
        if VERSION:
            norm = VERSION if VERSION.startswith("v") else "v" + VERSION
            heads = [ln for ln in text.split("\n")
                     if re.match(r"^## v\d+\.\d+\.\d+\b", ln)]
            if len(heads) != 1 or not heads[0].startswith("## %s" % norm):
                found = ", ".join(h.split(" ", 2)[1] for h in heads) or "none"
                add("H", "CHANGELOG.md",
                    "public changelog must carry exactly one version section "
                    "for %s; found: %s" % (norm, found))

# ---- I: no private dogfooding sections -------------------------------------
# The export transform removes these sections wholesale (see
# export_paths.PRIVATE_SECTION_HEADINGS); neither the headings nor any
# link to their anchors may survive into the artifact.
for relpath, heading in PRIVATE_SECTION_HEADINGS:
    full = os.path.join(STAGING, relpath)
    if not os.path.isfile(full):
        continue
    text = read(full)
    if text is None:
        continue
    for lineno, line in enumerate(text.split("\n"), 1):
        if line.startswith(heading):
            add("I", "%s:%d" % (relpath, lineno),
                "private dogfooding section must not ship: %r" % heading)
PRIVATE_ANCHORS = ["#" + heading_anchor(h) for _, h in PRIVATE_SECTION_HEADINGS]
for path in walk_files():
    if not path.endswith(".md") or is_export_fixture(rel(path)):
        continue
    text = read(path)
    if text is None:
        continue
    for lineno, line in enumerate(text.split("\n"), 1):
        for anchor in PRIVATE_ANCHORS:
            if anchor in line:
                add("I", "%s:%d" % (rel(path), lineno),
                    "link to a removed private section must not ship: %s"
                    % anchor)

# ---- J: kit CLAUDE.md names no excluded private guiding-doc paths ----------
# The top-level CLAUDE.md is the kit's OWN repository rules — it never
# describes a target project, so any code-span path it names (e.g.
# `design/adr/`, `archive/`, `notes/`) is a kit-private path. Those dirs are
# excluded from the export, so naming them in the shipped CLAUDE.md points
# public users at material that does not ship. Private-only guidance belongs
# in a PRIVATE_SECTION_HEADINGS section (removed wholesale by check I); this
# catches a bare reference that leaks outside such a section. Reuses
# is_excluded() so the boundary never drifts from checks B/D. Scoped to
# CLAUDE.md alone: elsewhere a `design/adr/` mention is legitimately the
# TARGET project's generated path, not the kit's.
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
claude_md = os.path.join(STAGING, "CLAUDE.md")
if os.path.isfile(claude_md):
    text = read(claude_md)
    if text is not None:
        for lineno, line in enumerate(text.split("\n"), 1):
            for m in CODE_SPAN_RE.finditer(line):
                span = m.group(1).strip()
                if "/" not in span and span not in ("notes", "archive"):
                    continue  # not a path-like span
                if is_excluded(span):
                    add("J", "CLAUDE.md:%d" % lineno,
                        "kit CLAUDE.md names an excluded private path that "
                        "does not ship: `%s` (move it into a source-repo-only "
                        "section)" % span)

# ---- K: kit.json contract points only at shipped files ---------------------
# kit.json's `contract` object holds repo paths agents are told to read (the
# governing ADR, the human doc, the validator). Skill artefact paths describe
# TARGET-project layouts and are exempt; the contract describes THIS repo, so
# every entry must name a file that ships — not an excluded private path (the
# reconcile step drops those) and not a missing file.
kit_json = os.path.join(STAGING, "kit.json")
if os.path.isfile(kit_json):
    text = read(kit_json)
    try:
        kit = json.loads(text) if text is not None else None
    except json.JSONDecodeError as e:
        kit = None
        add("K", "kit.json", "not valid JSON: %s" % e)
    contract = (kit or {}).get("contract")
    if isinstance(contract, dict):
        for key, value in sorted(contract.items()):
            if not isinstance(value, str):
                continue
            if is_excluded(value):
                add("K", "kit.json",
                    "contract.%s points at an excluded private/source path "
                    "that does not ship: %s" % (key, value))
            elif not exists(value):
                add("K", "kit.json",
                    "contract.%s points at a file missing from the export: %s"
                    % (key, value))

# ---- L: shipped .gitignore references no private paths ----------------------
# The exported .gitignore must not carry ignore patterns for — or comments
# about — source-only private tooling (notes/, archive/, .hermes); the
# transform scrubs those blocks, and none may survive.
gitignore = os.path.join(STAGING, ".gitignore")
if os.path.isfile(gitignore):
    text = read(gitignore)
    if text is not None:
        for lineno, line in enumerate(text.split("\n"), 1):
            if gitignore_line_is_private(line):
                add("L", ".gitignore:%d" % lineno,
                    "references a kit-private path that does not ship: %r"
                    % line.strip())

# ---- assemble -------------------------------------------------------------
by_check = {}
for p in problems:
    by_check.setdefault(p["check"], []).append(p)

CHECK_NAMES = {
    "A": "top-level allowlist",
    "B": "excluded paths absent",
    "C": "required artifacts present",
    "D": "markdown links resolve",
    "E": "no old owner/repo URLs",
    "F": "no absolute/temp paths",
    "G": "no stale version pins",
    "H": "changelog curated",
    "I": "no private dogfooding sections",
    "J": "kit CLAUDE.md names no excluded paths",
    "K": "kit.json contract paths ship",
    "L": ".gitignore references no private paths",
}

checks = []
for cid in sorted(CHECK_NAMES):
    items = by_check.get(cid, [])
    checks.append({
        "id": cid,
        "name": CHECK_NAMES[cid],
        "ok": not items,
        "problems": [{"path": i["path"], "detail": i["detail"]} for i in items],
    })

if problems:
    status, exit_code = "leak", 1
    lines = ["check-public-export: FAIL — %d violation(s) in %s:" % (len(problems), STAGING)]
    for c in checks:
        if c["ok"]:
            continue
        lines.append("  [%s] %s:" % (c["id"], c["name"]))
        for pr in c["problems"]:
            lines.append("    - %s — %s" % (pr["path"], pr["detail"]))
    text = "\n".join(lines)
else:
    status, exit_code = "clean", 0
    text = ("check-public-export: clean — %s satisfies the public export "
            "contract (%d checks passed)" % (STAGING, len(CHECK_NAMES)))

outputs = {
    "staging": STAGING,
    "version": VERSION or None,
    "violationCount": len(problems),
    "checks": checks,
}

print(json.dumps({"exit": exit_code, "status": status, "outputs": outputs, "text": text},
                 ensure_ascii=False))
