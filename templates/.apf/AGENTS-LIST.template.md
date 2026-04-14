---
last_update: 2026-03-22
Author: Iddo Lev
---

# Agents List

<!-- Note: The following sentence should not remain in the instantiated AGENTS-LIST.md file -->
This is a template for a `AGENTS-LIST.md` file, to be instantiated by the agentic
programming setup process for a new project.

## What is this file?

This file contains the list of all available agents and their abilities.

### apf-tech-lead (workflow)

Note: `apf-tech-lead` is a workflow (not a sub-agent) located at `.apf/workflows/apf-tech-lead.md`.
It runs in the main conversation context so it can interact with the human user.
The specialist agents below run as Claude Code sub-agents under `.claude/agents/`.

Role: Task orchestrator and architectural authority

Location: `.apf/workflows/apf-tech-lead.md` (runs in the main conversation, not as a sub-agent)

When to Use: Use this workflow when a new task or request comes in that needs to be analyzed, broken down into subtasks,
and routed to the appropriate specialist agents.
This workflow serves as the primary entry point for all tasks, and orchestrates the
execution flow across multiple agents.

---

<!-- ADAPT: Fill this list with one entry for each of the agents.
     The field "When to Use" should be filled with the value of the `description` field
     from the agent's yaml frontmatter WITHOUT the examples there. -->

### [agent-name1 e.g. apf-backend-specialist]

Role: [role1 e.g. Backend developer]

When to Use: [description1]

### [agent-name2]

Role: [role2]

When to Use: [description2]
