#!/usr/bin/env python3
"""Build the chat/completions request payload for bin/review-pr (M5, ADR-051).

Reads the unified diff from stdin and writes the request JSON to the path
given as argv[1]. Assembles system + rubric + active-profile + user messages
from the prompt pack under $KIT_ROOT/ai-review/prompts/. Truncates the diff to
$MAXDIFF bytes with an explicit notice rather than failing on huge diffs.

Env: KIT_ROOT, MODEL, PROFILE, MAXDIFF, PR, TITLE, BODY.
"""
import os
import sys
import json


def read_prompt(kit_root, name):
    path = os.path.join(kit_root, "ai-review", "prompts", name)
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except Exception:
        return ""


def profile_block(profiles_md, profile):
    """Extract the active profile's section from profiles.md (## <profile>)."""
    lines = profiles_md.split("\n")
    out = []
    capturing = False
    for ln in lines:
        low = ln.strip().lower()
        if ln.startswith("## "):
            name = low[3:].split("(")[0].strip()
            capturing = (name == profile)
            if capturing:
                out.append(ln)
            continue
        if capturing:
            out.append(ln)
    return "\n".join(out).strip()


def main():
    out_path = sys.argv[1]
    kit_root = os.environ.get("KIT_ROOT", ".")
    model = os.environ.get("MODEL", "openai/gpt-4o-mini")
    profile = os.environ.get("PROFILE", "balanced")
    try:
        max_diff = int(os.environ.get("MAXDIFF", "200000"))
    except ValueError:
        max_diff = 200000

    diff = sys.stdin.read()
    truncated = False
    if len(diff.encode("utf-8")) > max_diff:
        diff = diff.encode("utf-8")[:max_diff].decode("utf-8", "ignore")
        truncated = True

    system = read_prompt(kit_root, "system.md")
    rubric = read_prompt(kit_root, "rubric.md")
    profiles_md = read_prompt(kit_root, "profiles.md")
    profile_text = profile_block(profiles_md, profile)

    system_msg = "\n\n".join(x for x in [
        system,
        "# Review rubric\n\n" + rubric if rubric else "",
        "# Active profile: %s\n\n%s" % (profile, profile_text) if profile_text else "",
    ] if x)

    user_parts = ["Review the following pull request."]
    if os.environ.get("PR"):
        user_parts.append("PR: #%s" % os.environ["PR"])
    if os.environ.get("TITLE"):
        user_parts.append("Title: %s" % os.environ["TITLE"])
    if os.environ.get("BODY"):
        user_parts.append("Description:\n%s" % os.environ["BODY"])
    if truncated:
        user_parts.append("NOTE: the diff below was truncated to fit a size budget; "
                          "review only what is shown and do not assume the rest.")
    user_parts.append("Unified diff:\n\n```diff\n%s\n```" % diff)
    user_msg = "\n\n".join(user_parts)

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh)


if __name__ == "__main__":
    main()
