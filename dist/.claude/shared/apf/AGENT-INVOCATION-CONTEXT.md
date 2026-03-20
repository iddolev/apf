---
version: 2026-03-19
author: Iddo Lev
comment: |
  This file contains instructions for an agent on how to log its invocations in a log file.
  In any agent you wish to log, add the following line to the agent's description .md file:
  > Do the instructions in @.claude/shared/AGENT-INVOCATION-CONTEXT.md 
---

## Log Instructions

**Whenever you receive focus (either directly from the human user or when you are invoked by another agent)**, run:

```
.claude/scripts/apf/log_agent_invocations.bat "<your-agent-name>" "agent-start" "<brief description of the task and input you received>"
```

**Whenever you are about to relinquish your execution (when you return focus to whoever called you)**, run:

```
.claude/scripts/apf/log_agent_invocations.bat "<your-agent-name>" "agent-stop" "<brief summary of what you did and the outcome so far>"
```

The summary you write to these commands should be brief (1-2 sentences). 

---
