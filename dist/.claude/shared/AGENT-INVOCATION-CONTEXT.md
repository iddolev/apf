---
version: 2026-03-19
author: Iddo Lev
---

## What is this file?

This file contains instructions for an agent on how to log its invocations in a log file.

In any agent you which to log, add the following line to the agent's description .md file:
> Add the contents of AGENT-INVOCATION-CONTEXT.md to your context, and follow the instructions there.

## Log

The project maintains a running log `logs/agents_invocations_log.jsonl` of agent invocations. 
Each line is a JSON record with a timestamp, agent name, and message.

You, as an agent, are to add entries to this log file using the following instructions, 
so that the human user can review what really happened during a session.

## Instructions

**Whenever you receive focus (either directly from the human user or when you are invoked by another agent)**, check whether .apf/:

```
.claude/scripts/apf/log_agent_invocations.bat "<your-agent-name>" "agent-start" "<brief description of the task and input you received>"
```

**Whenever you are about to relinquish your execution (when you return focus to whoever called you)**, run:

```
.claude/scripts/apf/log_agent_invocations.bat "<your-agent-name>" "agent-stop" "<brief summary of what you did and the outcome so far>"
```

Keep messages short (1-2 sentences). 
