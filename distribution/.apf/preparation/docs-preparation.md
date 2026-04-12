---
last_update: 2026-03-21
author: Iddo Lev
LLM-co-author: claude-Opus-4.6
comment: |
  This script is meant to be copied to the user's project.
  Do not run it in the APF agentic-programming project itself.
---

# Documents Preparation and Instantiation

This document describes a section of the main preparation process file (`preparation.md`).

## Project Documents

Look for files matching the pattern `.apf/STATE-v{version}.md`.
According to the content of the highest version STATE file, go to the appropriate stage
below and follow the relevant instructions.
After completing each item, mark its checkbox as `[v]` in the STATE file before proceeding.

1. PRD: using `.apf/preparation/templates/docs/PRD/PRD.instructions.md`
2. TSD: using `.apf/preparation/templates/docs/TSD/TSD.instructions.md`
3. Implementation Plan: using
   `.apf/preparation/templates/docs/implementation-plan/implementation-plan.instructions.md`
4. Test Plan: using `.apf/preparation/templates/docs/test-plan/test-plan.instructions.md`

<a id="rules-and-templates"/>

## Instantiating Rule Templates and Other Files

### Instantiation Instructions

Instantiate each template below using information from the documents created
above (PRD, TSD, implementation plan, test plan). 
In all the files mentioned below:

1. You need to instantiate them according to the instructions in the `<!-- ADAPT: ...->` tags.
2. After that, remove all `<!-- ADAPT -->` markers from the output.
3. Fill in `[TBD]` placeholders
4. Keep all non-ADAPT sections unchanged.
5. A template `<X>.tmpl.md` should be instantiated to a file `<X>.md` and placed 
   according to the instructions.

### The Files

1. `PROGRAMMING-PRINCIPLES`: Instantiate
   `.apf/preparation/templates/rules/PROGRAMMING-PRINCIPLES.tmpl.md` according to its
   `<!-- ADAPT -->` markers, using information from the PRD and TSD. Place the
   result at `.apf/rules/PROGRAMMING-PRINCIPLES.md`.
2. `PROJECT-RULES`: Instantiate
   `.apf/preparation/templates/rules/PROJECT-RULES.tmpl.md` — derive
   rules from the TSD and PRD, then confirm each rule with the user. Place the
   result at `.apf/rules/PROJECT-RULES.md`.
3. `SECURITY-CONVENTIONS`: If the project has
   security conventions beyond `PROGRAMMING-PRINCIPLES.md`, then instantiate
   `.apf/preparation/templates/rules/SECURITY-CONVENTIONS.tmpl.md` and
   place the result at `.apf/rules/SECURITY-CONVENTIONS.md`.
4. `GIT-RULES`: Instantiate
   `.apf/preparation/templates/rules/GIT-RULES.tmpl.md` — confirm the
   commit message format, branch naming, agent permissions etc. with the user. Place
   the result at `.apf/rules/GIT-RULES.md`.
5. `PROJECT-STRUCTURE`: Instantiate
   `.apf/preparation/templates/PROJECT-STRUCTURE.tmpl.md` —
   derive from the TSD's architecture and the implementation plan's work breakdown.
   Place the result at `docs/PROJECT-STRUCTURE.md`.
6. `README`: Offer to auto-generate the project's README.md based on the docs, and ask for
   approval.
   If yes, then instantiate `.apf/preparation/templates/README.tmpl.md` according to its
   `<!-- ADAPT -->` markers, using information from the other documents.
   Place the result as `README.md` in the project root folder.

## CLAUDE.md files

### CLAUDE.apf.md

Instantiate the file `.apf/preparation/templates/CLAUDE.apf.tmpl.md` according to the instructions in it.
Put the result in `.apf/CLAUDE.apf.md`.

### CLAUDE.md

The APF framework deliberately does not create a CLAUDE.md file, 
in order to allow the user to have their own `CLAUDE.md` file.

However, APF requires the user's `CLAUDE.md` to mention `CLAUDE.apf.md`.
This is accomplished by adding the following text inside the user's `CLAUDE.md`,
if it's not already there:

<!-- DO NOT REMOVE: This is required for APF -->
Read also the instructions in `.apf/CLAUDE.apf.md`.
<!-- END OF DO NOT REMOVE: This is required for APF -->

So your instruction is to check whether `CLAUDE.md` already exists in the project's root folder.
If yes, tell the user that the above section needs to be appended to `CLAUDE.md`
and ask for permission to do so. If there is no `CLAUDE.md` file, 
then simply create it with the required section.
