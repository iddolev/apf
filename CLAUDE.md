---
date: 2026-03-07
author: "Iddo Lev"
description: |
  This file is meant to be read by Claude Code only when developing the agentic programming itself, 
  and not when the framework is used in another project.
---

# CLAUDE.md — Agentic Programming

> **STOP — This file is for developers of APF (Agentic Programming Framework) itself.**
> In a project that _uses_ this framework, this file should not appear.

## Rules

- After modifying a markdown file, run `/apf:format-markdown <file>` on it.
- Do not make templates project-specific. Templates must remain generic with placeholders — 
  they are filled in by the LLM when used in an actual project.
- The `sandbox/` and `tmp/` folders contain experiments and drafts. 
  You should completely ignore their contents in your thinking,
  and you must never reference them, as if they do not exist.
