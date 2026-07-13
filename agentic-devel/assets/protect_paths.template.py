#!/usr/bin/env python3
"""PreToolUse hook: blocks agent Edit/Write to the spec file and secret files.

Placeholders to resolve before writing this file to <target-repo>/.claude/hooks/protect_paths.py:
  PROTECTED_SUFFIXES — glob-ish suffixes matched against the absolute file path (case-sensitive).
                       Defaults below cover the common cases (spec doc, .env files, secrets dir);
                       add the project's real spec path (e.g. "docs/PRD.md") and any other
                       hook-protected files this project needs.

Why this exists: an agent that can rewrite the spec it's supposed to be implementing against can
silently "fix" a disagreement between plan and spec instead of stopping to report it — which is
exactly the failure mode externalized state is meant to prevent. Same logic for secrets: a hook
is a guarantee that doesn't depend on the agent remembering the rule every single time.

This script reads the tool-call payload as JSON from stdin (the shape the harness provides for
PreToolUse hooks) and exits 2 with a message on stderr to block, 0 to allow.

Known gotcha (a real, easy-to-reintroduce mistake): match on the resolved absolute path, and be
precise about exact filenames vs prefixes — a naive substring check on ".env" also blocks
".env.example" (a file agents legitimately need to create/update, since it's the
documented-placeholder template committed to git, not a secret itself). The EXACT_NAMES /
PATH_PREFIXES split below exists so you don't reintroduce that bug.
"""
import json
import os
import sys

# Exact filenames (no wildcards) that must never be written, wherever they live in the repo.
EXACT_NAMES = {
    "PRD.md",       # replace with this project's real spec filename(s)
    ".env",
    ".env.local",
    ".env.production",
}

# Path prefixes (relative to repo root) that are entirely off-limits.
PATH_PREFIXES = [
    "secrets/",
]


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # fail open on malformed input — never block on a hook bug

    tool_input = payload.get("tool_input", {})
    raw_path = tool_input.get("file_path") or tool_input.get("path") or ""
    if not raw_path:
        return 0

    repo_root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    abs_path = os.path.normpath(os.path.join(repo_root, raw_path))
    rel_path = os.path.relpath(abs_path, repo_root)
    basename = os.path.basename(abs_path)

    if basename in EXACT_NAMES:
        sys.stderr.write(
            f"Blocked: agents may not write to protected file '{rel_path}'. "
            "If this file genuinely needs to change, ask the user to edit it directly.\n"
        )
        return 2

    for prefix in PATH_PREFIXES:
        if rel_path.startswith(prefix):
            sys.stderr.write(
                f"Blocked: agents may not write under protected path '{prefix}' ({rel_path}).\n"
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
