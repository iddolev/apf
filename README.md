# Agentic Programming Framework (APF)

A methodology toolkit for AI-assisted software development. This repo contains templates,
instruction files, and agent templates that guide LLMs through a structured software
engineering workflow — from product requirements all the way to test planning and agent setup.

This is not a codebase. No application code lives here.
The code here includes only Python and Windows scripts to be copied into the user project
which is using the agentic programming framework here.
The purpose is that everyone
can benefit from the highest quality of agentic programming framework instead of
trying to figure this out by themselves or manually following instruction guides.

## The Document Chain

The core of this toolkit is a four-document pipeline, where each document derives from the previous
one:

1. **PRD** (Product Requirements Document) — defines *what* to build and *why*
2. **TSD** (Technical Specifications Document) — defines *how* to build it
3. **Implementation Plan** — defines *in what order* to build it
4. **Test Plan** — defines *how to verify* it was built correctly

Each document has a **template** (the fill-in structure) and an **instructions file**
(how the LLM should fill it). The entry point `starting-point.md` orchestrates walking
through this pipeline in order, with state tracking for resumption.

After the documents are complete, the toolkit also guides creation of
**agent definitions** for agentic programming environments like Claude Code.

## Structure

```
.claude/
├── commands/apf/                — Slash commands (format-markdown, log-claude-code-hook-event)
├── scripts/apf/                 — Python scripts backing the slash commands
└── ...                          — APF-only config (agents, settings) — not copied to user projects

installation/
├── apf_install.bat              — Windows launcher for the installer
└── apf_install.py               — Copies dist/ files and instantiates templates/ into user project

dist/                            — Files copied as-is into user projects (currently empty)

templates/
└── CLAUDE.template.md           — CLAUDE.md template, instantiated per project

instructions/
├── docs-and-agents-process.md   — Entry point and orchestration
├── rules/
│   ├── PROGRAMMING-PRINCIPLES.md       — Practical coding standards for agents
│   ├── SOFTWARE-ENGINEERING-PRINCIPLES.md — Theoretical foundations for reviewers
│   └── ADVERSARIAL-THINKING.md         — Adversarial mode overlay for any agent
├── creating-docs/
│   ├── PRD/                     — PRD template + instructions
│   ├── TSD/                     — TSD template + instructions
│   ├── implementation-plan/     — Implementation plan template + instructions
│   ├── test-plan/               — Test plan template + instructions
│   ├── README/                  — README template
│   ├── project-rules/           — Templates for git rules, project rules, security conventions
│   └── project-structure/       — Project structure template
├── initialization/              — First-time framework setup scripts and instructions
└── state/                       — State tracking for the preparation workflow

docs/                            — Design rationale and ADR documentation
tests/                           — Framework tests
```

## Template Conventions

- Templates use placeholders to be filled during an iterative interview with the user.
- Some templates have a companion `.instructions.md` file that tells the LLM how to fill the template.

## How to Use

### Download

Download this file and run it:

```bash
https://github.com/iddolev/apf/blob/main/installation/apf_install.bat
```

This will download a python script and run it. 
There are several arguments you can pass to the script you downloaded:

- `--version` — Show the installed APF version and the latest available version, then exit
- `--target FOLDER` — Install into FOLDER instead of the current directory
- `--dry-run` — Show what would be done without touching any files
- `--yes` / `-y` — Skip the confirmation prompt
- `--force` — Reinstall even if already at the latest version
- If you run it without any flag, the local version will be updated 
  only if there is a newer version available

### Run

Once download is complete, give an LLM (Cursor with Claude Sonnet, or Claude Code) the prompt:

> Follow the instructions in docs-and-agents-process.md

## Rationale

See the [rationale](https://github.com/iddolev/apf/blob/main/docs/rationale.md) page
for explanations about the rationale of various parts of the APF.
