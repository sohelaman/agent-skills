# agentic-devel

A methodology skill for running a backend web app build as agent-sized, independently verifiable
tasks. Tuned for `.NET` / `PHP`-Laravel / RDBMS-backed projects, but the process works for any
backend stack.

## How to use it

1. **Have a spec.** A PRD, RFC, or requirements doc — this is a prerequisite. It's the source of
   truth the plan gets traced back to.
2. **Ask the agent to generate an implementation plan.** Point it at the spec and say something
   like "use agentic-devel to generate a detailed implementation plan for coding agents." This
   bootstraps the task-card plan, the progress ledger, the `/task` runner skill, reviewer
   subagents, and the project memory file.
3. **Hand the plan to a coding agent.** Once the plan exists, just tell any coding agent which
   task to work on (e.g. `/task T-3.2`). It reads the ledger, implements that one task, verifies
   it, gets it reviewed, updates the ledger, and commits — one task per session.

See `SKILL.md` for the full methodology.
