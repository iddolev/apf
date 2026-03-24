# Backlog

## More

1. sub-agents that verify implementation against the plan document. Catches what you'd normally
   miss.
2. Whenever running APF, automatically detect whether a newer version was released in GitHub,
   and offer the user to update.
3. Instructions to all coding agents, and especially reviewers: Always do research and check whether
   there is already a known library that does something, and use it.
   "Don't reinvent the wheel" (is this a common phrase in English?)
   E.g. if you need code that can compare a filepath against a .gitignore pattern,
   it's a very bad practice to try to implement it yourself, when there is already a known python
   package to do it.
   Always ask yourself: Is it likely that the required functionality has been implemented already
   by some known package, check, and if yes, then obtain it and use it rather than re-implementing.
4. Dependencies that are required by a script of APF (e.g. package that checks .gitignore pattern
   to skip files for format_markdown.py) need to be added to the user project's dependencies
5. E.g. the problem with google doc name vs what allowed on windows - it broke and I had to think
   of a better way than simply converting to unicode etc. so maybe such problems should be surfaced
   to the human to decide what to do, so (1) surface and not just try to solve itself (2) human
   thinks better

## Versioning and detecting new agentic framework version

1. For each file which is not simply copied to the user project but is a template to instantiate
   It has to have a version number in the frontmatter.
   The starting-point.md and the tech lead (both being the main entry points)
   need to compare the version of the instantiated file to the template version.
   If the template version is higher, then an appropriate update process should be done.
   E.g. if SHARED-AGENT-CONTEXT.tmpl.md is updated.
   Currently I am updating the files in the user project ad-hoc manually.

## Updates

1. Need to account for what happens if user makes changes in some phase that are different
   from what was planned - how to update the docs, leaving the original + adding more notes

## Next: MCP of tasks

1. Discuss what fields should be in a task, and in a test case, see if can use the same class
2. change server.py accordingly
3. setup installation copying etc.
4. tech lead - add access to t
5. he mcp server, so i can talk to the tech lead and ask:
   what's the next step and it looks up in the mcp server
5. and then do it, and then it needs to understand the description and
   spawn the appropriate agent
6. after one task like that works, and i see code files created,
   we'll discuss the loop

## Code Quality automation

Look at https://claude.ai/chat/552c86d1-4871-4fb7-be57-88d0e8cbf081 - create a process that uses
existing tools + suggestions + what cannot be modeled?

## Simple Tasks

1. Videos
   - https://x.com/trq212/status/2014480496013803643
   - https://www.youtube.com/watch?v=RpUTF_U4kiw
   - massive upgrade https://www.youtube.com/watch?v=lf2lcE4YwgI
2. Take the actual instantiated PRD and ask for LLM opinion in general,
   and then feedback -> what should be improved in the PRD template and instructions md
3. The possible colors are the following, so choose what makes sense for the agents: Red
      Blue
      Green
      Yellow
      Purple
      Orange
      Pink
      Cyan
4. Add "find inconsistencies" command/skill?
5. files say that Tech-lead agent should read only the Architecture & Scale section from
   SOFTWARE-ENGINEERING-PRINCIPLES
   when planning task decomposition and reviewing architectural decisions, but an agent cannot read
   only part of a file
   so need to refactor that part ?
6. Add in FRAMEWORK-STATE the timestamp of each important document.
   The user is not supposed to change anything manually in any doc,
   because doing so bypasses the framework and agents and causes Claude to not know about the
   change.
   But to partially mitigate it, this timestamp allows us to create automatic checks to detect
   cases where the user changed a file manually.
   Then we need some process to run occasionally to check for such changes,
   and if a change detected, then start a process of reconciliation.
7. Change the preparation process PRD stage to ask first if there is already a PRD that was prepared
   manually not using the framework, and if so where it is, and then start the interview but
   glean answers from that doc if possible
8. If we see that loggins each agent invocation is too much, add another HISTORY logger:
   STATE/HISTORY.jsonl, with the instruction: Do not log trivial actions, only important ones
   to understand the flow of what happened
9. Check C4: https://claude.ai/chat/8636118f-e9ad-43f0-8341-f217f73feb50
9. Autonomous Agentic SDLC: https://docs.google.com/document/d/1RNL6Art05I_1jQJpA97m-eXRQQLemHDfkGPaLvTYTko/edit?tab=t.0
10. more generally, general discussion with LLM what is the entire SDLC, and then how to model it
    assuming perfect agents, and then what are all the things that could possibly go wrong and how
    to mitigate with more processes and agents
11. there should never be a folder .claude/plusings under the project's root?
    https://claude.ai/chat/8e8541b9-b60f-4dd6-895e-352af75c479a +
    https://chatgpt.com/c/69a6d58c-f82c-838d-8e67-4f2897aa9e5b
12. if using plugins from a marketplace, how to update (how to bring the latest plugin, how to
    decide if in the project to move to this plugin version)
13. What can we take from https://claude.com/plugins/product-management ;
    https://claude.com/plugins-for/cowork (there is the same plugin in one of the anthropics github
    repos: https://github.com/anthropics/knowledge-work-plugins)
14. Is it possible to have e.g. GSD installed under gsd instead of .claude, so that gsd is cloned
    from GSD and I can modify it, and then pull update from GSD and merge the changes? Or maybe have
    a fork and not a clone and it will make it easier?
15. doc-coauthoring skill from anthropics/skills and more:
    https://claude.ai/chat/56eedc2d-d823-4233-a237-6c1d83064d6a
    1. also https://claude.ai/chat/ef167be9-3aa2-470a-ac78-50a0d4d95a45
16. .claude/rules/ !!! https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/ +
    https://claudelog.com/faqs/what-are-claude-rules/ +
    https://claude.ai/chat/09bb02c5-5b11-4c15-9e17-71d743fd19a5
17. https://github.com/snarktank/ai-dev-tasks/blob/main/create-prd.md

## Maybe

Should we enhance the document creation stage also with these?

- Analytics-tracking-plan
- Launch-runbook

## Skills?

What about skills, e.g. in
https://github.com/wshobson/agents/tree/main/plugins/security-scanning/skills

## Possibly to consider

Ask CC to inspect the URL suggestions at the bottom of each agent template to see
whether something general should be added to the template

## Implement ADR Support

Implement the ADR (Any Decision Record) system as described in `docs/ADR-rationale.md`.

### Templates to create

1. **`ADR-index.tmpl.md`** — template for `ADR-index.md`, a compact table
   (number, title, status, one-line summary) that is cheap for the tech lead to scan.
2. **`ADR-list.tmpl.md`** — template for `ADR-list.md`, the full ADR records
   with complete context, decision, and consequences sections.

Both templates should include instructions on the ADR format, when to create
a new record, and how to maintain the index alongside the list.

### SHARED-AGENT-CONTEXT update

Add instructions to `SHARED-AGENT-CONTEXT.tmpl.md` explaining the ADR system:

- The **tech lead** reads `ADR-index.md` when planning work or assigning tasks.
  When a relevant ADR is found, it reads the full record from `ADR-list.md`
  and includes the constraint in the task assignment to the specialist.
- **Specialist agents** do not routinely read ADR files. They receive relevant
  ADR constraints from the tech lead as part of task assignments.
- **The code reviewer** may read `ADR-index.md` before reviewing code
  that touches architectural or convention concerns.
- Any agent that makes a decision that constrains future work should write
  a new ADR entry (append to `ADR-list.md` and update `ADR-index.md`).

### Tech lead template update

Update the tech lead template to include ADR gatekeeper responsibilities.

### MCP server for ADR querying

Implement the ideal queryable ADR system as an MCP server. This would expose
`record_adr`, `check_adr`, and `list_adrs` tools that any agent can call
natively. The server handles persistence, numbering, and semantic retrieval.

See `docs/ADR-rationale.md` section "Implementation Path: MCP Server" for
the full design, resource costs, and semantic retrieval options (keyword
matching, embedding-based, or pass-through to the LLM).

The `framework-initial-install` step would install the server script and configure
the MCP entry in `.claude/settings.json`.

### See also

`docs/ADR-rationale.md` for full design rationale, including the MCP-based
implementation plan, and why the current file-based approach uses the tech
lead as gatekeeper.

## Next Enhancement

Instead of the naive approach of cloning this repo under the root folder of the user's project's,
convert this project to a plugin that can be installed as a Claude Code plugin.
This means all the files will sit under the user's folder ~/.claude/plugins/cache.
