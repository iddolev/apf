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
run this command and **remember the value it outputs** as your `INVOCATION_ID` for this invocation:

```
.claude/scripts/apf/log_agent_invocation.bat "<your-agent-name>" "agent-start" "<brief description of the task and input you received>" "invocation-id"
```

**Whenever you are about to relinquish your execution (when you return focus to whoever called you)**, 
substitute the exact value you captured above into this command:

```
.claude/scripts/apf/log_agent_invocation.bat "<your-agent-name>" "agent-stop" "<brief summary of what you did and the outcome so far>" "invocation-id" "<the INVOCATION_ID value you captured>"
```

The summary you write to these commands should be brief (1-2 sentences). 

---
