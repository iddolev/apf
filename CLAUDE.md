---
date: 2026-03-07
author: "Iddo Lev"
description: This file is meant to be read by Claude Code only when developing the agentic programming itself, and not
when the framework is used in anohter project.
---

# CLAUDE.md — Agentic Programming

> **STOP — This file is for developers of the agentic-programming framework itself.**
> If you are a project that _uses_ this framework (e.g. you were told to follow `starting-point.md`),
> **ignore this entire file**. None of the rules below apply to your project.

## Rules

- After modifying a markdown file, run `/format-markdown <file>` on it.
- Do not add application code to this repo. It contains only markdown templates, instruction files, and YAML state
  files.
- Do not make templates project-specific. Templates must remain generic with `[TBD]`
  placeholders — they are filled in by the LLM when used in an actual project.
- The `sandbox/` and `tmp/` folders contain experiments and drafts. Do not treat their contents as authoritative or reference them
  from instruction files.
