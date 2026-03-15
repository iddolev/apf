---
Date: 2026-03-06
Author: Iddo Lev
---

# SHARED-AGENT-CONTEXT.md Template

<!-- Note: The following sentence should not remain in the instantiated SHARED-AGENT-CONTEXT.md file -->
This is a template for a SHARED-AGENT-CONTEXT.md file,
to be instantiated by the agentic programming setup process for a new project.

## What is this file?

This file contains information gleaned from the project's PRD and TSD documents, which all
sub-agents need to know about.

This file should be read by each sub-agent upon spawning it.

## History

The project maintains a running log `logs/agents_invocations_log.jsonl` of agent invocations during a claude session. 
Each line is a JSON record with a timestamp, actor name, and message.

You, as an agent, are instructed to add entries to this log file, 
so that the human user can review what really happened during a Claude Code session.

### Instructions

**Whenever you receive focus (either directly from the human user or when you are invoked by the tech lead agent)**, run:

```
python .claude/scripts/log_agent_invocations.py "<your-agent-name>" "agent-start" "<brief description of the task and input you received>"
```

**Whenever you are about to relinquish your execution (when you return focus to whoever called you)**, run:

```
python .claude/scripts/log_agent_invocations.py "<your-agent-name>" "agent-stop" "<brief summary of what you did and the outcome so far>"
```

Keep messages short (1-2 sentences). 

## Project description

<!-- ADAPT: Fill this section with a brief explanation of what the project does. -->

## Tech stack

<!-- ADAPT: Fill this section -->

## Architecture

<!-- ADAPT: Fill this section with the ASCII diagram from the TSD -->

## Key file/directory structure

<!-- ADAPT: Fill this section -->

## Key Documentation

<!-- ADAPT: Replace [TBD] with the current version number (e.g., v0.1). -->

Always read the following files:

- @docs/PROJECT-STRUCTURE.md — key directories and their purposes
- @rules/GIT-RULES.md — git workflow, permissions, and prohibited operations

Read any of the following files only if needed:

- Read only the PRD of the latest version ([TBD]) (in the folder: @docs/specs/)
- Read only the TSD of the latest version ([TBD]) (in the folder: @docs/specs/)
- Read only the implementation-plan of the latest version ([TBD]) (in the folder: @docs/plans/)
- If you decide it's needed, read only the test-plan of the latest version ([TBD]) (in the folder: @docs/plans/)

## Operating Modes

You can be activated in one of two modes:

- **Normal mode** — the default. You operate collaboratively, using your domain
  expertise to complete the task you were given.
- **Adversarial mode** — activated explicitly by the user or the tech-lead
  agent. In this mode, your goal shifts from building to critiquing. You apply
  a deliberately hostile lens to find what is wrong, what could go wrong, and
  what hasn't been considered — while still using your domain expertise to focus
  the critique where it matters most.

When activated in adversarial mode, read and follow
@rules/ADVERSARIAL-THINKING.md. That file defines the mindset, principles,
behavioral rules, and output structure for adversarial review.

Detect which mode you're in from context: if you were explicitly told to
operate in adversarial mode (or similar phrasing such as "stress-test this,"
"find what's wrong," "devil's advocate"), you're in adversarial mode. Otherwise,
you're in normal mode.

## Agent Memory

<!-- NOTE to Claude: It is not your responsibility now to create this memory folder.
     This will be done automatically by the agent itself. -->

You have a persistent memory directory at
@.claude/agent-memory/your_name/.
Its contents persist across conversations.

Consult your memory files before starting work.
Update them as you discover information worth preserving across sessions.

**What to record:**

The following aspects only if they are relevant for your work:

- Project structure and module responsibilities
- Naming conventions and coding patterns established
- Configuration patterns and environment variable usage
- Error handling conventions already in use
- SDK quirks or workarounds discovered
- Test fixtures and mocking strategies in use
- Deviations from spec docs and why they exist

**What NOT to record:**

- Session-specific context or in-progress work
- Anything that duplicates information already somewhere else that you have access to
- Speculative conclusions from reading a single file
