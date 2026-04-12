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

## Organization

Because APF is a framework, it can be confusing to understand the role of each file.
So this is illuminated here for key folders and files.

### Folders

1. `distribution/`:  Files copied as-is into the user project
2. `templates/`:  Files instantiated by the preparation process into the user project
3. `.claude/`:  Entities for Claude Code (definitions of commands, skills, agents, hooks, etc.)
   Some of them are used only during development of APF itself,
   and some of them are useful for both APF and the user project
   - so the latter are placed under an `apf` sub-folder (e.g. `commands/apf/consistency-review.md`)
4. `installation`:  Installation script that is used by the user to install APF in the user project,
   as well as for updating to a newer version of APF
5. `docs/`:  Documents about APF
6. `tests/`:  Testing code of APF
7. `sandbox/`:  Experimentation. You can ignore this folder

### Central Files

1. `README.md`:  This file, a starting point for the Agentic Programming Framework.
2. `distribution/README.apf.md`:  A subsidiary README file to be copied to the user project.
   Explains how APF helped create the user's project.
3. `templates/README.tmpl.md`:  An optional README template the user can choose to use.
   The user may also choose to follow a different format,
   but should still mention that README.apf.md has info
   specifically about using APF for creating and maintaining the project.
4. `CLAUDE.md`:  Instructions for Claude Code / OpenCode for the APF project itself.
   This is separate from the user project's `CLAUDE.me`.
5. `CLAUDE.apf.tmpl.md`: Specific instructions for Claude Code,
   in addition to the instructions the user may choose to put in their project's main `CLAUDE.md`.
   (The user's `CLAUDE.md` file should mention `CLAUDE.apf.tmpl.md`)
6. `dist/.apf/.apf.yaml`:  A configuration file for APF. E.g. includes the APF version number.

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
dist/                            — Files copied as-is into the user project
├── .apf
├── .claude
├── rules
├── docs-and-agents-process.md
└── README.apf.md

templates/                       — Files instantiated per project
├── docs/                        — Templates for the project's documents
│   ├── PRD/                     — PRD template + instructions
│   ├── TSD/                     — TSD template + instructions
│   ├── implementation-plan/     — Implementation plan template + instructions
│   └── test-plan/               — Test plan template + instructions
├── .claude/
│   └── agents/                  — Agent definition templates
├── rules
├── STATE
├── CLAUDE.tmpl.md
├── PROJECT-STRUCTURE.tmpl.md
└── README.tmpl.md

.claude/                         — Entities for Claude Code
│                                  either for this project, not to be copied to the user project
│                                  or for both this project and the user project
│                                  - these are placed under "apf" subfolder.
│                                  Entities that are only for the user project and not APF itself
│                                  sit under dist/.claude/ and templates/.claude/
├── commands                     — Slash commands
├── scripts                      — Python scripts backing the slash commands
├── skills                       — Skills
└── ...                          — APF-only config — not copied to user project

installation/
├── apf_install.bat              — Windows launcher for the installer
└── apf_install.py               — Copies dist/ files into user project

docs/                            — Docs about APF
tests/                           — Tests for APF scripts
```

## Template Conventions

- Templates use placeholders to be filled during an iterative interview with the user.
- A template filename is `X.tmpl.md`.
- Some templates `X.tmpl.md` have a companion `X.instructions.md` file
  that tells the LLM how to fill the template.

## How to Use

### Download

To install APF in your new or existing project, download [this file](https://github.com/iddolev/apf/blob/main/installation/apf_install.bat) and run it,
or download it using `curl`:

```bash
curl -O https://raw.githubusercontent.com/iddolev/apf/main/installation/apf_install.bat
```

Running this script fetches `apf_install.py` and runs it.

There are several arguments you can pass to the `apf_install.bat` script you downloaded:

- `--version` — Show the installed APF version and the latest available version, then exit
- `--target FOLDER` — Install into FOLDER instead of the current directory
- `--dry-run` — Show what would be done without touching any files
- `--yes` / `-y` — Skip the confirmation prompt
- `--force` — Reinstall even if already at the latest version
- If you run it without any flag, the local version will be updated
  only if there is a newer version available in the GitHub repo.

### Run

[TBD: Improve this section]

Once download is complete, give an LLM (Cursor with Claude Sonnet, or Claude Code) the prompt:

> Follow the instructions in docs-and-agents-process.md

## Demo

To help you better understand how APF works,
you can look at the [apf-demo](https://github.com/iddolev/apf-demo) repo.
This repo is the result of installing APF into it, and running it to create a small toy project.

## Installation vs. Preparation

**Installation:** This is a rare event in which you either first install APF in your project,
or update the installed APF to a newer version (when a new version is made available).
This process is governed by the script `apf_install.bat` which you should run 
from the shell in the root folder of your project.

**Preparation:** This is a workflow completely separate and different from "installation."
It is governed by the command `/apf:preparation` which you should run after starting
the Claude Code or OpenCode session. It goes through preparation of the project's documents,
including the PRD and TSD as well as agnets creation / updating.

## Rationale

See the [rationale](https://github.com/iddolev/apf/blob/main/docs/rationale/rationale.md) page
for explanations about the rationale of various parts of the APF.
