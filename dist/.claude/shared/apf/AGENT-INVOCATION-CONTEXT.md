---
version: 2026-03-19
author: Iddo Lev
comment: |
  This file contains instructions for an agent on how to log its invocations in a log file.
  In any agent you wish to log, add the following line to the agent's description .md file:
  > Do the instructions in @.claude/shared/AGENT-INVOCATION-CONTEXT.md 
---

## Log Instructions

**Whenever you receive focus (either directly from the human user or when you are invoked by another agent)**, 
run the following and capture the output as `INVOCATION_ID`:

```
INVOCATION_ID=$(.claude/scripts/apf/log_agent_invocations.bat "<your-agent-name>" "agent-start" "<brief description of the task and input you received>" "invocation-id")
```

**Whenever you are about to relinquish your execution (when you return focus to whoever called you)**, pass `$INVOCATION_ID` as the final argument:

```
.claude/scripts/apf/log_agent_invocations.bat "<your-agent-name>" "agent-stop" "<brief summary of what you did and the outcome so far>" "invocation-id" "$INVOCATION_ID"
```

The summary you write to these commands should be brief (1-2 sentences). If logging is disabled, `$INVOCATION_ID` will be empty — pass it anyway, the script handles it gracefully.

---
