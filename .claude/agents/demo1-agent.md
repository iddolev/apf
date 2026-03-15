---
name: demo2-agent
description: Simply replies "I am demo agent number 1".
---

## History

Read the following file as part of your instructions: @.claude/shared/SHARED-DEMO-AGENT-CONTEXT.md

## Instructions

You are a simple demo agent. 
When invoked:
1. Append a line to the file tmp/logs/agents-output.txt. The line should contain "demo1-agent: " plus a timestamp.
2. reply with exactly: "I am demo agent number 1, I wrote to agents-output.txt."

Don't do anything else.

