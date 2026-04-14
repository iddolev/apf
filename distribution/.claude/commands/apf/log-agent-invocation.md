---
source: Agentic Programming Framework: https://github.com/iddolev/apf
author: Iddo Lev for
description: "Manage logging of agent invocation events. Required argument: status | on | off |
install"
last_update: 2026-03-19
allowed-tools: Bash(python *)
---

This command requires exactly one argument: `status`, `on`, `off`, or `install`.
The argument is: $ARGUMENTS

If the argument is empty or not one of `status`, `on`, `off`, or `install`, tell the user:
"Usage: /apf:log-agent-invocation <status|on|off|install>" and STOP.

1. If `.apf/.apf.yaml` does not exist, STOP (unless the argument is `install`).
2. Run the Python script with the argument:

```bash
python .claude/apf/scripts/log_agent_invocation.py --$ARGUMENTS
```

3. Report the result to the user.
