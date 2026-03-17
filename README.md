# Agentic Programming

A methodology toolkit for AI-assisted software development. This repo contains templates,
instruction files, and agent definitions that guide LLMs through a structured software
engineering workflow — from product requirements all the way to test planning and agent setup.

This is not a codebase. No application code lives here. 
The code here includes only Python and Windows scripts to be copied into the user project
which is using the agentic programming framework here.
The purpose is that everyone
in our company can benefit from the highest quality of agentic programming framework instead of
trying to figure this out by themselves or manually following instruction guides.

## The Document Chain

The core of this toolkit is a four-document pipeline, where each document derives from the previous one:

1. **PRD** (Product Requirements Document) — defines *what* to build and *why*
2. **TSD** (Technical Specifications Document) — defines *how* to build it
3. **Implementation Plan** — defines *in what order* to build it
4. **Test Plan** — defines *how to verify* it was built correctly

Each document has a **template** (the fill-in structure) and an **instructions file**
(how the LLM should fill it). The entry point `starting-point.md` orchestrates walking
through this pipeline in order, with state tracking for resumption.

After the documents are complete, the toolkit also guides creation of
**agent definitions** for agentic programming frameworks like Claude Code.

## Structure

[TBD: Need to update this section to reflect new structure. 
 In particular, 
 dist - contains files to be copied as is. 
 templates - contains files to be instantiated based on specific info from the user's project.
 .claude - contains some general utils that are useful for both the APF project and the user project
    these exist either under an "apf" sub-folder (e.g. .claude/commands/apf/) or named with a prefix "apf-"
 .claude also contains entities that are relevant only for the APF project and not the user project,
    so they are not copied by apf_install.py to the user project.
]

```
instructions/
├── starting-point.md                             — Entry point and orchestration
├── rules/
│   └── PROGRAMMING-PRINCIPLES.md                 — Coding standards for agents that write/review code
├── creating-docs/
│   ├── PRD/                                      — PRD template + instructions
│   ├── TSD/                                      — TSD template + instructions
│   ├── implementation-plan/                       — Implementation plan template + instructions
│   └── test-plan/                                — Test plan template + instructions
├── claude/
│   ├── claude-preparation.md                      — Claude-specific agent setup workflow
│   ├── knowledge/                                 — Templates for CLAUDE.md, agent lists, shared context
│   └── agent-templates/                           — Agent role definitions (tech lead, backend, etc.)
└── state/
    └── FRAMEWORK-STATE-template.yaml            — State tracking for the preparation workflow
```

## Template Conventions

- Templates use `[TBD]` as placeholders to be filled during an iterative interview with the user.
- Each template has a companion `-instructions.md` file that tells the LLM how to fill it.
- Documents reference each other by relative path, maintaining traceability across the chain.

## How to Use

Clone this repo as a sub-folder in your project:

```bash
cd your-project
git clone git@gitlab.com:claude-code-experiments/agentic-programming.git
```

To update to the latest version:

```bash
cd agentic-programming
git pull
cd ..
```

Then give an LLM (Cursor with Claude Sonnet, or Claude Code) the prompt:

> Follow the instructions in @starting-point.md
