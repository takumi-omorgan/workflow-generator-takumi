#!/usr/bin/env python3
"""Validate model output, build + write the review artifact (bin/review-pr).

Reads the unified diff from stdin and the raw model reply from $MODEL_RAW.
Validates/coerces it to ai-review-artifact v1 (recomputing commentability
against the diff), writes <OUT_DIR>/pr-<PR>-<hash>.{json,md}, and prints a
JSON result object the calling bash renders as envelope / text / md.

Env: PR, PROVIDER, MODEL, PROFILE, MAXDIFF, OUT_DIR, TS, MODEL_RAW.
Exit non-zero on unparseable/invalid model output (bash maps to domain fail).
"""
import os
import sys
import json
import hashlib

import review_common as rc


def main():
    diff = sys.stdin.read()
    raw = os.environ.get("MODEL_RAW", "")
    pr = int(os.environ["PR"])
    provider = os.environ.get("PROVIDER") or None
    model = os.environ.get("MODEL") or None
    profile = os.environ.get("PROFILE") or None
    out_dir = os.environ.get("OUT_DIR", "ai-review/artifacts")
    ts = os.environ.get("TS")
    try:
        max_diff = int(os.environ.get("MAXDIFF", "200000"))
    except ValueError:
        max_diff = 200000

    truncated = len(diff.encode("utf-8")) > max_diff

    digest = hashlib.sha256(
        (diff + "\x00" + (provider or "") + "\x00" + (model or "")).encode("utf-8")
    ).hexdigest()
    artifact_hash = "sha256:" + digest
    short = digest[:8]

    try:
        obj = rc.extract_json(raw)
    except Exception as e:
        sys.stderr.write("review-render: %s\n" % e)
        sys.exit(1)

    try:
        artifact = rc.normalize_artifact(
            obj, diff, pr=pr, provider=provider, model=model, profile=profile,
            generated_at=ts, artifact_hash=artifact_hash, truncated=truncated)
    except Exception as e:
        sys.stderr.write("review-render: %s\n" % e)
        sys.exit(1)

    json_path = os.path.join(out_dir, "pr-%d-%s.json" % (pr, short))
    md_path = os.path.join(out_dir, "pr-%d-%s.md" % (pr, short))
    md = rc.render_markdown(artifact)
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(artifact, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(md)
        if not md.endswith("\n"):
            fh.write("\n")

    st = artifact["stats"]
    commentable = sum(1 for f in artifact["findings"] if f["commentable"])
    outputs = {
        "pr": pr,
        "artifactJson": json_path,
        "artifactMarkdown": md_path,
        "artifactHash": artifact_hash,
        "summary": artifact["summary"],
        "stats": st,
        "findingCount": len(artifact["findings"]),
        "commentableCount": commentable,
        "truncated": truncated,
    }
    nxt = [{
        "skill": "publish-review",
        "args": "--artifact %s --pr %d" % (json_path, pr),
        "when": "you have reviewed the artifact and want to publish (requires explicit approval)",
    }]
    text = (
        "review-pr: wrote %s\n"
        "  summary:     %s\n"
        "  findings:    %d blocking, %d non-blocking, %d question, %d praise\n"
        "  commentable: %d (high-confidence, located, inline-eligible)%s\n"
        "  next:        bin/publish-review --artifact %s --pr %d   (dry-run preview; never posts without --confirm)"
        % (json_path, artifact["summary"],
           st["blocking"], st["non-blocking"], st["question"], st["praise"],
           commentable, "  [diff truncated]" if truncated else "",
           json_path, pr)
    )
    print(json.dumps({"status": "ok", "outputs": outputs, "next": nxt,
                      "errors": [], "text": text, "md": md}, ensure_ascii=False))


if __name__ == "__main__":
    main()
