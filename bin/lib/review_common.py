"""Shared helpers for the AI PR review surfaces (M5, ADR-051).

Imported by bin/lib/review-render.py and bin/lib/review-publish.py (both run
as `python3 <path>` with this lib dir on sys.path[0], so `import
review_common` resolves). Pure stdlib — no third-party dependency, matching
the kit's "no new runtime dependency" rule.

Provides:
  - parse_diff_lines(diff): map repo-relative new-file path -> set of new
    line numbers present in the diff hunks (added + context lines).
  - extract_json(text): pull the first JSON object out of a model reply,
    tolerating ```json fences or leading/trailing prose.
  - normalize_artifact(obj, diff, ...): validate + coerce a model artifact to
    ai-review-artifact v1, recomputing `commentable` against the actual diff.
  - render_markdown(artifact): a human-readable review report.
"""

import json
import re

CLASSIFICATIONS = ("blocking", "non-blocking", "question", "praise")
SEVERITIES = ("high", "medium", "low")
CONFIDENCES = ("high", "medium", "low")
CATEGORIES = ("correctness", "security", "data-loss", "regression",
              "test-coverage", "api-compat", "maintainability", "docs", "style")


def parse_diff_lines(diff):
    """Return {path: set(new_line_numbers)} for lines present in the diff."""
    files = {}
    path = None
    new_line = None
    # Drop only the single trailing-newline artifact so it is not mistaken for
    # a blank content line; keep genuine interior blank lines.
    if diff.endswith("\n"):
        diff = diff[:-1]
    for raw in diff.split("\n"):
        # Structural lines: never hunk content.
        if raw.startswith("diff --git") or raw.startswith("index ") \
                or raw.startswith("--- ") or raw.startswith("old mode") \
                or raw.startswith("new mode") or raw.startswith("similarity") \
                or raw.startswith("rename ") or raw.startswith("copy ") \
                or raw.startswith("deleted file") or raw.startswith("new file"):
            new_line = None
            continue
        if raw.startswith("+++ "):
            p = raw[4:].split("\t", 1)[0].strip()
            if p == "/dev/null":
                path = None
            else:
                if p.startswith("b/") or p.startswith("a/"):
                    p = p[2:]
                path = p
                files.setdefault(path, set())
            new_line = None
            continue
        if raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            new_line = int(m.group(1)) if m else None
            continue
        # Inside a hunk only: classify by the first character.
        if path is None or new_line is None:
            continue
        if raw.startswith("+"):
            files[path].add(new_line)
            new_line += 1
        elif raw.startswith("-"):
            pass  # removed line: present in old file only
        elif raw == "" or raw.startswith(" "):
            # Context line. A blank context line is " " in canonical git output,
            # but editors/tools often strip it to "". Treat both as context so a
            # whitespace-stripped diff still maps lines correctly.
            files[path].add(new_line)
            new_line += 1
        else:
            # "\ No newline at end of file" or any non-hunk prefix: end the hunk.
            new_line = None
    return files


def extract_json(text):
    """Best-effort: return the first top-level JSON object in `text`."""
    text = text.strip()
    # strip a leading ```json / ``` fence if present
    fence = re.match(r"^```[a-zA-Z0-9]*\s*(.*?)\s*```$", text, re.DOTALL)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except Exception:
        pass
    # fall back: scan for the first balanced {...}
    start = text.find("{")
    if start == -1:
        raise ValueError("no JSON object found in model output")
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
            continue
        if c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("unbalanced JSON object in model output")


def _enum(val, allowed, default):
    return val if val in allowed else default


def normalize_artifact(obj, diff, pr=None, provider=None, model=None,
                       profile=None, generated_at=None, artifact_hash=None,
                       truncated=False):
    """Validate + coerce a model artifact to ai-review-artifact v1.

    Recomputes each finding's `commentable` against the actual diff lines:
    a finding is commentable only when it is high-confidence, not praise,
    and its file+line appear in the diff hunks.
    """
    if not isinstance(obj, dict):
        raise ValueError("artifact is not a JSON object")
    summary = obj.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        summary = "(no summary provided by the model)"
    raw_findings = obj.get("findings")
    if raw_findings is None:
        raw_findings = []
    if not isinstance(raw_findings, list):
        raise ValueError("artifact 'findings' must be a list")

    diff_lines = parse_diff_lines(diff)
    findings = []
    for i, f in enumerate(raw_findings, start=1):
        if not isinstance(f, dict):
            continue
        classification = _enum(f.get("classification"), CLASSIFICATIONS, "non-blocking")
        severity = _enum(f.get("severity"), SEVERITIES, "low")
        category = _enum(f.get("category"), CATEGORIES, "maintainability")
        confidence = _enum(f.get("confidence"), CONFIDENCES, "low")
        file = f.get("file") if isinstance(f.get("file"), str) else None
        line = f.get("line")
        line = line if isinstance(line, int) else None
        title = f.get("title") if isinstance(f.get("title"), str) else "(untitled finding)"
        detail = f.get("detail") if isinstance(f.get("detail"), str) else ""
        suggestion = f.get("suggestion") if isinstance(f.get("suggestion"), str) else None

        located = bool(file and line is not None and line in diff_lines.get(file, set()))
        commentable = (located and confidence == "high"
                       and classification != "praise")
        findings.append({
            "id": f.get("id") if isinstance(f.get("id"), str) else "f%d" % i,
            "classification": classification,
            "severity": severity,
            "category": category,
            "file": file,
            "line": line,
            "title": title,
            "detail": detail,
            "suggestion": suggestion,
            "confidence": confidence,
            "commentable": commentable,
        })

    stats = {c: 0 for c in CLASSIFICATIONS}
    for f in findings:
        stats[f["classification"]] += 1

    artifact = {
        "schema": "ai-review-artifact",
        "version": 1,
        "summary": summary.strip(),
        "findings": findings,
        "stats": stats,
    }
    if pr is not None:
        artifact["pr"] = pr
    if provider is not None:
        artifact["provider"] = provider
    if model is not None:
        artifact["model"] = model
    if profile is not None:
        artifact["profile"] = profile
    if generated_at is not None:
        artifact["generatedAt"] = generated_at
    if artifact_hash is not None:
        artifact["artifactHash"] = artifact_hash
    artifact["truncated"] = bool(truncated)
    return artifact


def render_markdown(artifact):
    """Render a human-readable Markdown review report from an artifact."""
    pr = artifact.get("pr")
    lines = []
    head = "# AI review" + (" — PR #%s" % pr if pr is not None else "")
    lines.append(head)
    meta = []
    if artifact.get("provider"):
        meta.append("provider `%s`" % artifact["provider"])
    if artifact.get("model"):
        meta.append("model `%s`" % artifact["model"])
    if artifact.get("profile"):
        meta.append("profile `%s`" % artifact["profile"])
    if meta:
        lines.append("")
        lines.append("_" + " · ".join(meta) + "_")
    if artifact.get("truncated"):
        lines.append("")
        lines.append("> ⚠️ The diff was truncated to fit the size budget; "
                     "review may be incomplete.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(artifact.get("summary", ""))

    st = artifact.get("stats", {})
    lines.append("")
    lines.append("**Findings:** %d blocking · %d non-blocking · %d question · %d praise"
                 % (st.get("blocking", 0), st.get("non-blocking", 0),
                    st.get("question", 0), st.get("praise", 0)))

    order = {"blocking": 0, "non-blocking": 1, "question": 2, "praise": 3}
    findings = sorted(artifact.get("findings", []),
                      key=lambda f: (order.get(f["classification"], 9),
                                     SEVERITIES.index(f["severity"]) if f["severity"] in SEVERITIES else 9))
    labels = {"blocking": "🛑 Blocking", "non-blocking": "💡 Non-blocking",
              "question": "❓ Question", "praise": "👍 Praise"}
    current = None
    for f in findings:
        if f["classification"] != current:
            current = f["classification"]
            lines.append("")
            lines.append("## %s" % labels.get(current, current))
        loc = ""
        if f.get("file"):
            loc = " — `%s%s`" % (f["file"], (":%d" % f["line"]) if f.get("line") else "")
        tags = "[%s/%s, confidence %s]" % (f["severity"], f["category"], f["confidence"])
        lines.append("")
        lines.append("### %s%s" % (f["title"], loc))
        lines.append("")
        lines.append(("%s (inline-commentable)" % tags) if f.get("commentable") else tags)
        if f.get("detail"):
            lines.append("")
            lines.append(f["detail"])
        if f.get("suggestion"):
            lines.append("")
            lines.append("**Suggested fix:** %s" % f["suggestion"])
    lines.append("")
    return "\n".join(lines)
