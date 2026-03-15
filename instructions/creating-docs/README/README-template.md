---
date: 2026-03-06
author: "Iddo Lev"
LLM-author: claude-Opus-4.6
---

# [TBD — Product / Feature Name]

<!-- ADAPT: Fill in a 1-2 sentence description from the PRD's Executive Summary. -->

## Prerequisites

<!-- ADAPT: List required runtimes, tools, and system dependencies
     (e.g., Node.js >= 20, Python 3.12, Docker, specific CLIs).
     Derive from the TSD's Technology Stack section. -->

- [TBD]

## Environment Setup

<!-- ADAPT: List required environment variables and how to obtain them
     (e.g., API keys, database URLs, secrets).
     Derive from the TSD's Configuration Management section. -->

- Copy `.env.example` to `.env` and fill in the values:

```
[TBD]
```

## Installation

<!-- ADAPT: Fill in the install commands for this project. -->

```bash
[TBD]
```

## Running the App

<!-- ADAPT: Fill in commands to start the app in dev and production modes.
     Remove any lines that don't apply. -->

- **Dev mode:** `[TBD]`
- **Production:** `[TBD]`

## Testing

<!-- ADAPT: Fill in commands to run tests and linting.
     Derive from the test plan's Test Strategy section.
     Remove any lines that don't apply. -->

- **Unit tests:** `[TBD]`
- **Integration tests:** `[TBD]`
- **Linting:** `[TBD]`

## Project Structure

See `docs/PROJECT-STRUCTURE.md`.

## Documentation

- **PRD:** `docs/specs/PRD_v[TBD].md`
- **TSD:** `docs/specs/TSD_v[TBD].md`
- **Implementation Plan:** `docs/plans/implementation-plan_v[TBD].md`
- **Test Plan:** `docs/plans/test-plan_v[TBD].md`

## Agentic Programming

This project is built using our company's standardized **agentic-programming** framework --
a methodology toolkit that guides AI-assisted development through a structured pipeline:
PRD, TSD, Implementation Plan, Test Plan, and agent setup.

The framework lives in the `agentic-programming/` sub-folder and provides:

- Templates and instructions for creating spec and planning documents
- Agent definitions for Claude Code (tech lead, backend specialist, etc.)
- Shared context and knowledge files that keep all agents aligned

For details on the framework itself, see `agentic-programming/README.md`.
