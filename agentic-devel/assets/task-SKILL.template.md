<!--
Placeholders to fill before writing this file to <target-repo>/.claude/skills/task/SKILL.md:
  {{PROJECT_NAME}}        e.g. "the billing service", "the claims portal API"
  {{PLAN_PATH}}           e.g. docs/IMPLEMENTATION_PLAN.md
  {{STATE_PATH}}          e.g. docs/agent/STATE.md
  {{MEMORY_FILE}}         e.g. CLAUDE.md or AGENTS.md
  {{TASK_ID_EXAMPLE}}     e.g. T-5.2, TASK-42
  {{SPEC_REF_CLAUSE}}     e.g. "and every PRD section (FR/NFR IDs) it references" — delete the
                          clause entirely if there's no separate spec doc beyond the plan itself.
  {{COVERAGE_CLAUSE}}     e.g. " with the coverage gate" — delete if the project has no coverage
                          gate.
  {{SECURITY_REVIEW_CLAUSE}}
                          e.g. " For tasks tagged [SEC], also run the security-reviewer subagent."
                          — delete this whole sentence if bootstrap determined no security
                          subagent is needed for this project.
  {{COMMIT_FORMAT_CLAUSE}}
                          e.g. " in the org format: `[CODE GEN][100][Claude][Default] <type>(scope): summary`"
                          — or " using Conventional Commits (`<type>(scope): summary`)" if no org
                          prefix applies.
-->
---
name: task
description: Execute one {{PROJECT_NAME}} implementation task by ID from {{PLAN_PATH}}, following the session protocol in {{MEMORY_FILE}}.
argument-hint: [task-id e.g. {{TASK_ID_EXAMPLE}}]
---

Execute task $ARGUMENTS.

1. Read {{STATE_PATH}} — confirm $ARGUMENTS is not done and all its `Depends` tasks are done. If not, STOP and report.
2. Read the $ARGUMENTS card in {{PLAN_PATH}}{{SPEC_REF_CLAUSE}}.
3. Present a short implementation plan (files, tests, risks) and wait for approval if in interactive mode.
4. Implement exactly the card's scope — no unrelated cleanup or extras. Write tests in the same change. Obey all {{MEMORY_FILE}} rules.
5. Run the card's Verify commands plus the full test suite{{COVERAGE_CLAUSE}}. Iterate until green.
6. Ask the code-reviewer subagent to review the diff; apply valid findings.{{SECURITY_REVIEW_CLAUSE}}
7. Update {{STATE_PATH}} (status=done, date, commit ref, notes/deviations).
8. Make ONE commit{{COMMIT_FORMAT_CLAUSE}}, referencing the task ID (and spec IDs, if any) in the body. Do not push unless asked.
