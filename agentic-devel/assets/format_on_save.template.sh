#!/usr/bin/env bash
# PostToolUse hook: auto-formats the file just edited/written, by extension.
#
# Only wire this into .claude/settings.json if the stack actually has a formatter AND you've
# verified the command below works in this repo (run it by hand against a scratch edit first —
# don't ship a guessed formatter invocation). If no formatter applies, delete the PostToolUse
# block from settings.json entirely rather than leaving a no-op hook.
#
# Why format only the touched file, not the whole repo: formatting unrelated files turns every
# task's diff into unrelated churn, which is exactly what "single commit, no unrelated file
# churn" (the definition-of-done rule) is meant to prevent.
#
# Delete the branches this project doesn't need; add others per references/stack-commands.md.

set -euo pipefail

FILE="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))' 2>/dev/null || true)"
[ -z "$FILE" ] && exit 0
[ -f "$FILE" ] || exit 0

case "$FILE" in
  *.cs)
    command -v dotnet >/dev/null 2>&1 && dotnet format --include "$FILE"
    ;;
  *.php)
    # Laravel projects usually have Pint (./vendor/bin/pint); older PHP projects use php-cs-fixer.
    if [ -x "./vendor/bin/pint" ]; then
      ./vendor/bin/pint "$FILE"
    elif [ -x "./vendor/bin/php-cs-fixer" ]; then
      ./vendor/bin/php-cs-fixer fix "$FILE"
    fi
    ;;
  *.py)
    command -v ruff >/dev/null 2>&1 && ruff format "$FILE"
    ;;
  *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.md)
    command -v prettier >/dev/null 2>&1 && npx --no-install prettier --write "$FILE"
    ;;
  *.go)
    command -v gofmt >/dev/null 2>&1 && gofmt -w "$FILE"
    ;;
  *.rs)
    command -v rustfmt >/dev/null 2>&1 && rustfmt "$FILE"
    ;;
esac

exit 0
