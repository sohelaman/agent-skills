<!--
Placeholders:
  {{PROJECT_NAME}}, {{PROJECT_ONE_LINER}}
  {{SPEC_PATH}}, {{PLAN_PATH}}, {{STATE_PATH}}
  {{BUILD_CMD}}, {{TEST_CMD}}, {{COVERAGE_CMD_BLOCK}} (delete if no coverage gate),
  {{LINT_CMD}}, {{FORMAT_CMD}}
  {{ARCHITECTURE_RULES}}      bullet list, this project's real layering/pattern rules — delete
                              the whole section if the project has none yet.
  {{CONVENTIONS}}             bullet list — naming, error handling, i18n, whatever recurring
                              cross-cutting concerns this project actually has.
  {{COMMIT_CONVENTION}}       e.g. "Conventional Commits: `<type>(scope): summary`" or an org
                              format string.
  {{SECURITY_GUARDRAILS_BLOCK}}
                              Delete entirely if 1.1.6 in SKILL.md determined this project has no
                              sensitive-data surface. Otherwise fill with the real constraints
                              (secret handling, auth requirements, injection/XSS defenses, etc.)
  {{TESTING_STACK}}           e.g. "Jest + Testing Library", "pytest + Testcontainers", "go test"
  {{COVERAGE_THRESHOLD_LINE}} delete if no coverage gate

This file is meant to be merged into (not replace) an existing CLAUDE.md/AGENTS.md if one already
exists — see SKILL.md §1.4.
-->
# {{PROJECT_NAME}}

{{PROJECT_ONE_LINER}}

**Source of truth:** `{{SPEC_PATH}}`. **Task plan:** `{{PLAN_PATH}}`. **Progress:** `{{STATE_PATH}}`.

## Session protocol (ALWAYS)

1. Read `{{STATE_PATH}}` first. Work ONLY on the task the user names. One task per session.
2. Open `{{PLAN_PATH}}`, locate the task, and follow its steps and accept criteria exactly.
   Cross-check against `{{SPEC_PATH}}` when in doubt — the spec wins over your assumptions.
3. Plan before coding (enter plan mode for anything non-trivial). Do not expand scope beyond the
   task card.
4. Finish = all accept criteria met + verify commands pass + `{{STATE_PATH}}` updated + a single
   commit.
5. If a task is impossible as written, STOP and report the conflict — do not silently improvise.

## Commands

```bash
{{BUILD_CMD}}
{{TEST_CMD}}
{{COVERAGE_CMD_BLOCK}}
{{LINT_CMD}}
{{FORMAT_CMD}}
```

## Architecture rules

{{ARCHITECTURE_RULES}}

## Conventions

{{CONVENTIONS}}

- Commits — {{COMMIT_CONVENTION}}. Body references the task ID (and spec IDs, if any).

{{SECURITY_GUARDRAILS_BLOCK}}

## Testing

- {{TESTING_STACK}}
- {{COVERAGE_THRESHOLD_LINE}}
- Never weaken, skip, or delete a failing test to make a gate pass. Fix the code or report the
  conflict.

## Definition of done (every task)

- [ ] Accept criteria on the task card met, mapped spec IDs satisfied
- [ ] Build clean, full test suite green{{COVERAGE_SUFFIX}}
- [ ] Lint/architecture checks green; no new suppressions without a justification note
- [ ] Cross-cutting conventions applied where the feature touches them
- [ ] `{{STATE_PATH}}` row updated (status, date, commit ref, notes)
- [ ] Single commit; no unrelated file churn
