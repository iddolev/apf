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

## Instantiating rules and project templates

Instantiate each template below using information from the documents created
above (PRD, TSD, implementation plan, test plan). Fill in `[TBD]` placeholders
and adapt `<!-- ADAPT -->` sections to match the project.

1. `PROGRAMMING-PRINCIPLES`: Instantiate
   `.apf/preparation/templates/rules/PROGRAMMING-PRINCIPLES.md.tmpl` according to its
   `<!-- ADAPT -->` markers, using information from the PRD and TSD. Place the
   result at `rules/PROGRAMMING-PRINCIPLES.md`.
2. `PROJECT-RULES`: Instantiate
   `.apf/preparation/templates/rules/PROJECT-RULES.md.tmpl` — derive
   rules from the TSD and PRD, then confirm each rule with the user. Place the
   result at `rules/PROJECT-RULES.md`.
3. `SECURITY-CONVENTIONS`: If the project has
   security conventions beyond `PROGRAMMING-PRINCIPLES.md`, then instantiate
   `.apf/preparation/templates/rules/SECURITY-CONVENTIONS.md.tmpl` and
   place the result at `rules/SECURITY-CONVENTIONS.md`.
4. `GIT-RULES`: Instantiate
   `.apf/preparation/templates/rules/GIT-RULES.md.tmpl` — confirm the
   commit message format, branch naming, agent permissions etc. with the user. Place
   the result at `rules/GIT-RULES.md`.
5. `PROJECT-STRUCTURE`: Instantiate
   `.apf/preparation/templates/PROJECT-STRUCTURE.md.tmpl` —
   derive from the TSD's architecture and the implementation plan's work breakdown.
   Place the result at `docs/PROJECT-STRUCTURE.md`.
6. `README`: Offer to auto-generate the project's README.md based on the docs, and ask for
   approval.
   If yes, then instantiate `.apf/preparation/templates/README.md.tmpl` according to its
   `<!-- ADAPT -->` markers, using information from the other documents.
   Place the result as `README.md` in the project root folder.
