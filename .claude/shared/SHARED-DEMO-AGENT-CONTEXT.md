---
description: |
  This file contains instructions and information that all the project's agents need to know about.
  This file should be read by each sub-agent as part of its agent definition:
  This aim is achieved by adding an instruction at the top of each agent definition file:
  Read .claude/shared/SHARED-AGENT-CONTEXT.md
---

# History

The project maintains a running log `logs/agents_invocations_log.jsonl` of agent invocations during a claude session. 
Each line is a JSON record with a timestamp, actor name, and message.

You, as an agent, are instructed to add entries to this log file, 
so that the human user can review what really happened during a Claude Code or OpenCode session.
Here are instructions on how to do that: 

## Instructions

**Whenever you receive focus (either directly from the human user or when you are invoked by the tech lead agent)**, run:

```
python .claude/scripts/log_agent_invocations.py "<your-agent-name>" "agent-start" "<brief description of the task and input you received>"
```

**Whenever you are about to relinquish your execution (when you return focus to whoever called you)**, run:

```
python .claude/scripts/log_agent_invocations.py "<your-agent-name>" "agent-stop" "<brief summary of what you did and the outcome so far>"
```

Keep messages short (1-2 sentences). 
