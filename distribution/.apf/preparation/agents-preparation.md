---
last_update: 2026-03-21
author: Iddo Lev
LLM-co-author: claude-Opus-4.6
comment: |
  This script is meant to be copied to the user's project.
  Do not run it in the APF agentic-programming project itself.
---

# Agents Preparation

This document describes a section of the main preparation process file (`preparation.md`).

## Instantiation Instructions

Instantiate each template below using information from the documents created
above (PRD, TSD, implementation plan, test plan). 
In all the files mentioned below:

1. You need to instantiate them according to the instructions in the `<!-- ADAPT: ...->` tags.
2. After that, remove all `<!-- ADAPT -->` markers from the output.
3. Fill in `[TBD]` placeholders
4. Keep all non-ADAPT sections unchanged.
5. A template `<X>.tmpl.md` should be instantiated to a file `<X>.md` and placed 
   according to the instructions.

## Agents - Our General Approach

We have a general template for each agent under the folder
`.apf/preparation/templates/.claude/agents/`,
plus general instructions here explaining how to adapt the templates 
by creating specific agents tailor-made to this project.

### IMPORTANT NOTE: Upon New Version

Whenever starting a new version of an existing project, there is a new set of spec docs.
Therefore, it is necessary to review the agent definitions to make sure they are adapted to be
useful for the new specs and don't remain stuck with capabilities that are not good enough
for the new version.

## Creating Agent Files

1. Instantiate the file `.apf/preparation/templates/.claude/agents/apf-tech-lead.tmpl.md` 
   according to the instructions in it.
   It must be instantiated in ALL projects.
   Put the result file `apf-tech-lead.md` under the folder `.claude/agents/`.
   Mark the apf-tech-lead agent checkbox as `[v]` in the latest `.apf/STATE-v*.md` file.
2. For each agent template file `<X>.tmpl.md` in the folder 
   `.apf/preparation/templates/.claude/agents/` (excluding apf-tech-lead, already handled above), 
   decide whether it is required for the project based on:
   - Roles and responsibilities identified in the PRD and TSD
   - The technology stack (e.g. include a frontend-developer agent only if the project has a
     frontend)
   - Team structure
   If yes, then instantiate it according to the instructions in it,
   and put the result file `<X>.md` under the folder `/.claude/agents/`.
3. Finally, given all the agents you created in `.claude/agents/`,
   instantiate the file `.apf/preparation/templates/.apf/AGENTS-LIST.tmpl.md` 
   according to the instructions in it.
   Put the result at `.apf/AGENTS-LIST.md`.
