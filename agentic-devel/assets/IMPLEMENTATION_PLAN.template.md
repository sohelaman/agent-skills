<!--
Placeholders:
  {{PROJECT_NAME}}
  {{SPEC_PATH}}          e.g. docs/PRD.md, docs/RFC.md — delete the whole "Source of truth" row
                         and any reference to it if there is no separate spec document (i.e. this
                         plan file *is* the spec).
  {{TASK_ID_SCHEME}}     e.g. "T-<phase>.<n>", "TASK-<n>"
  {{STATE_PATH}}
  {{AGENT_HARNESS}}      Name of the coding agent/harness this is written for (e.g. "Claude Code").
  {{REPO_LAYOUT}}        A text-tree sketch of where the scaffolding lives in this specific repo
                         (paths may differ from the defaults below — reflect what bootstrap
                         actually created here).
  {{PARALLEL_MAP_OR_NOTE}}
                         Either a real parallelization table (see §4 shape below) or, if this
                         project's tasks are all strictly sequential, a one-line note saying so.
  Everything under "Task Cards" is a worked example of the card format — replace the phase/task
  content with this project's real decomposition. Keep the card FIELD NAMES (Goal/Spec/Depends/
  Build/Accept/Verify) even if you rename phases/tasks, so the {{STATE_PATH}} rows and the /task
  skill's parsing logic stay predictable across projects.
-->
# {{PROJECT_NAME}} — Implementation Plan for Coding Agents

| Field | Value |
|---|---|
| **Source of truth** | {{SPEC_PATH}} |
| **Task ID scheme** | `{{TASK_ID_SCHEME}}` |
| **Primary agent** | {{AGENT_HARNESS}} |

---

## 1. How This Plan Works

This plan decomposes the spec into **agent-sized tasks**: each is designed to be completed in a
single session with fresh context, and carries everything the agent needs — goal, spec trace,
dependencies, deliverables, accept criteria, and shell-verifiable checks.

**Ground rules:**

1. **One task per session.** Context bloat is the primary cause of quality drift — start each
   task in a clean session.
2. **Plan first.** Review the plan for a task before letting the agent execute it, for anything
   non-trivial.
3. **Verification is the contract.** A task is done only when its `Verify` commands pass. Never
   accept "should work."
4. **Strict order within a phase** unless the parallelization map (§4) says otherwise.
5. **The spec wins.** If a task card and the spec disagree, the spec is authoritative; the agent
   must stop and report instead of improvising.
6. **State is externalized.** Progress lives in `{{STATE_PATH}}`, not in anyone's memory (human or
   model).

---

## 2. Repository layout for the agent harness

```text
{{REPO_LAYOUT}}
```

Commit the whole `.claude/` (or equivalent harness) directory — it's team infrastructure. Never
place secrets in the memory file, harness config, or prompts.

---

## 3. Progress Ledger

Template: `{{STATE_PATH}}` — see `STATE.template.md` in this skill's assets for the row format.

---

## 4. Parallelization Map

{{PARALLEL_MAP_OR_NOTE}}

Parallel work needs separate git worktrees + separate agent sessions to avoid workspace
collisions.

---

## 5. Task Cards

Card format — **Goal** (what exists when done) · **Spec** (traceability) · **Depends** ·
**Build** (key deliverables) · **Accept** (binary criteria) · **Verify** (commands).

---

### Phase 0 — <name this project's first phase>

#### <task-id> — <short title>
- **Goal:** <what exists when this task is done, in one sentence>
- **Spec:** <section/FR/issue reference> · **Depends:** —
- **Build:** <the concrete deliverables — files, endpoints, migrations, whatever applies>
- **Accept:** <binary, checkable criteria — not "works well," but "returns 200 for X and 404 for Y">
- **Verify:** `<exact shell command(s) that prove Accept is met>`

<!-- Repeat per task, grouped into phases. Keep cards small enough that a fresh-context agent
     session can finish one without running out of room to think. -->
