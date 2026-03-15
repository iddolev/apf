---
Date: 2026-03-06
Author: Iddo Lev
---

<!-- ADAPT: Delete the word Template from the following heading. -->

# CLAUDE.md Template

<!-- ADAPT: The following sentence should not remain in the instantiated CLAUDE.md file -->
This is a template for a CLAUDE.md file, to be instantiated by the agentic programming setup process for a new project.

## What is CLAUDE.md?

CLAUDE.md is a file that Claude Code loads at the start of every new session with the human user.

> Important Note:
  Subagents receive only their own agent definition file as prompt
  (plus basic environment details like working directory),
  and NOT the full Claude Code system prompt in CLAUDE.md.

## Project Context

1. Read @SHARED-AGENT-CONTEXT.
2. Read the project's @README.md file for build, test, and environment commands.

## Git Rules

Read and follow @rules/GIT-RULES.md -- it defines the commit message format, branch
naming, push policy, and which agents may use git.

## Agent Delegation

When a task requires specialist work, consult @.claude/knowledge/AGENTS-LIST.md for the list of available agents and when to use each one.
