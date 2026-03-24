---
last_update: 2026-03-06
Author: Iddo Lev
---

# CLAUDE.apf.md

## Inclusion

The following line should be included in the project's `CLAUDE.md` file, so that it refers to the content here:

> Read @.apf/CLAUDE.apf.md.

## What is CLAUDE.md?

CLAUDE.md is a file that Claude Code loads at the start of every new session with the human user.

> Important Note:
  Sub-agents receive only their own agent definition file as prompt
  (plus basic environment details like working directory),
  and NOT the full Claude Code system prompt in CLAUDE.md.

## Project Context

Read @README.md and @README.apf.md.

## Git Rules

Read and follow @rules/GIT-RULES.md -- it defines the commit message format, branch
naming, push policy, and which agents may use git.

## Agent Delegation

When a task requires specialist work, consult @.apf/AGENTS-LIST.md for the list of available agents and when to use each one.
