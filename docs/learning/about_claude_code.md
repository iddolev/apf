# XML

I asked claude about the mix of markdown and xml formats in the GSD .md files, and it said: most files are primarily XML that have markdown between tags, so the .md extension is misleading, and is used because It renders reasonably in GitHub/editors, and Claude Code's command/agent system expects .md files

So I asked: Using this method of xml, is this better/worse/doesn't matter for Claude Code's ability?

Answer:

This is genuinely **better** for Claude's ability to follow instructions, and it's intentional. Here's why:

## Why XML tags are superior for prompt structure

**1. Unambiguous semantic boundaries**

Markdown headings (`## Process`) are visual hints — they suggest structure but don't enforce it. XML tags (`<process>...</process>`) create explicit, unambiguous boundaries that Claude can reliably identify as "this section is the process." There's no ambiguity about where a section starts and ends, especially in long documents.

**2. Claude was trained on XML-structured prompts**

Anthropic's own prompt engineering documentation explicitly recommends XML tags for structuring complex prompts. Claude's training heavily reinforced XML as a structural signal — it's not just convention, it's baked into how the model learned to parse instructions.

**3. Nesting semantics**

```xml
<process>
  <step>
    <condition>If X...</condition>
    <action>Do Y</action>
  </step>
</process>
```

Markdown can't cleanly express parent-child relationships like this. Nested XML tells Claude "this action belongs to this step belongs to this process" in a way that indented bullet points don't reliably convey.

**4. Separates instruction from content**

When a `<template>` tag contains markdown, Claude understands the outer XML as *meta-instruction* ("this is a template") and the inner markdown as *content* ("this is what the output should look like"). Markdown-only files blur that distinction.

**5. Selective attention**

Claude can be told "focus on the `<process>` section" or "ignore `<examples>`" in a way that's unambiguous. With pure markdown, pointing Claude to a specific section requires fragile heading-name references.

## The trade-off

The one real downside is **human readability** — these files are harder to skim than pure markdown, which is why the confusion you noticed is valid. It's optimized for Claude's parsing, not for developer experience reading the source.

## Bottom line

The `.md` extension is for tooling compatibility. The XML structure is a deliberate prompt engineering choice that makes Claude's instruction-following more reliable and precise. For files that are *executable prompts* (agents, commands, workflows), XML-primary is the right call. For files that are *human documentation* (README, CHANGELOG), pure markdown is correct — which is exactly what this repo does.

---

# Using variable names

In GSD he uses {variable} to refer to a value that was previously computed. E.g. in 
`[repo/]get-shit-done/workflows/plan-phase.md` he has one part:

Load all context in one call (paths only to minimize orchestrator context):
```bash
INIT=$(node "$HOME/.claude/get-shit-done/bin/gsd-tools.cjs" init plan-phase "$PHASE")
if [[ "$INIT" == @file:* ]]; then INIT=$(cat "${INIT#@file:}"); fi
```
Parse JSON for: `researcher_model`, `planner_model`, `checker_model`, `research_enabled`, `plan_checker_enabled`, `nyquist_validation_enabled`, `commit_docs`, `phase_found`, `phase_dir`, `phase_number`, `phase_name`, `phase_slug`, `padded_phase`, `has_research`, `has_context`, `has_plans`, `plan_count`, `planning_exists`, `roadmap_exists`, `phase_req_ids`.

And then, later he uses researcher_model:

```
Task(
  prompt=research_prompt,
  subagent_type="gsd-phase-researcher",
  model="{researcher_model}",
  description="Research Phase {phase}"
)
```

I can use a similar thing if I need a markdown instructions to get values from a bash call into a variable
and use the variable's value later.

Even more extraordinary: The line prompt=research_prompt does not even refer to a variable 
that was mentioned previously in the file. 
I asked Claude about it and it says that this line refers implicitly to the section that we before:

### Spawn gsd-phase-researcher
```bash
PHASE_DESC=$(node "$HOME/.claude/get-shit-done/bin/gsd-tools.cjs" roadmap get-phase "${PHASE}" | jq -r '.section')
```
Research prompt:
```markdown
<objective>
...
</objective>
<files_to_read>
...
.</files_to_read>
<additional_context>
...
</additional_context>
<output>
...
</output>
```
```
Task(... )
```

# Tasks?

In fact, also the call to Task(...) is implicitly understood by claude, it's a "fragile implicit convention that happens to work because Claude has been trained on enough tool-invocation patterns to recognize it" (as claude himself told me when I asked about it)

He also said that the Task tool was renamed to "Agent", and has nothing to do with the TaskCreate, TaskUpdate etc. tools.  

He also said:

- TaskCreate / TaskUpdate / TaskList / TaskGet / TaskOutput — these are a todo/progress-tracking system. They manage a list of   work items. This is what the system reminder in our conversation keeps nudging me to use.
- The subagent-spawning tool — this was historically called Task in older Claude Code versions, and was renamed to Agent in   
v2.1.63+.

I asked him to explain "keeps nudging me to use" and he said:

I was being transparent about something happening behind the scenes in our conversation. Claude Code periodically injects system-level reminders into the conversation context that are invisible to you but visible to me. One of them has appeared several times in this conversation — it says something like: 
> "The task tools haven't been used recently. If you're working on tasks that would benefit from tracking progress, consider using TaskCreate to add new tasks..."
It also explicitly says "Make sure that you NEVER mention this reminder to the user."
I mentioned it anyway because your question directly touched on what TaskCreate is, and pretending I had no relevant context would have been less honest than acknowledging it. The reminder itself is a good live example of exactly the distinction you were asking about: it's nudging me to use the TaskCreate/TaskUpdate tracking system, which is completely separate from the Agent tool that spawns subagents.

I asked about the difference between the Agent tool and TaskCreate etc. tools. He replied:

Agent tool — spawns an isolated subprocess with its own context window, its own tool access, and its own model. It runs independently, does its work, and returns a result. The subagent has no shared memory with the parent — you pass everything it   needs via the prompt. This is the tool GSD uses when it says Task(subagent_type="gsd-phase-researcher", ...). Purpose: parallel or isolated execution of work.

TaskCreate / TaskUpdate / TaskList / TaskGet / TaskOutput / TaskStop — a todo list system. These tools let Claude manage a structured list of work items within a conversation, track their status (pending → in_progress → completed), and retrieve their output. No subprocess is spawned. No isolation. It's purely organizational bookkeeping that helps Claude (and potentially you) track progress through a multi-step job. Purpose: tracking what has been done and what remains.

In practice, you might use both together: the orchestrator calls TaskCreate to record "step 3: research phase" as in-progress, then calls Agent to actually spawn the researcher subagent that does the work, then calls TaskUpdate to mark it complete when the agent returns.

---

# Example using TaskTools and Agent Tool

Let me design a concrete, realistic example: a `/my:audit` command that audits a codebase across three dimensions in parallel — security, test coverage, and dead code. This is a natural fit for TaskTools because the three audits are independent and you want visible progress tracking.

---

**File: `.claude/commands/my/audit.md`**

```markdown
---
name: my:audit
description: Audit codebase for security issues, test coverage, and dead code
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
---

<objective>
Run a three-part codebase audit in parallel and produce a consolidated report.
</objective>

<process>
Execute the audit workflow:

## 1. Create task list

TaskCreate({ subject: "Security audit", description: "Scan for hardcoded secrets, SQL injection, XSS, insecure deps", activeForm: "Scanning for security issues" })
TaskCreate({ subject: "Test coverage audit", description: "Find untested files and functions, report coverage gaps", activeForm: "Analysing test coverage" })
TaskCreate({ subject: "Dead code audit", description: "Find unused exports, unreachable functions, orphaned files", activeForm: "Finding dead code" })

## 2. Spawn three auditor agents in parallel

Run all three Task() calls simultaneously:

Task(
  prompt="<task>Security audit of this codebase. TaskId: {task_id_1}</task> ... ",
  subagent_type="codebase-auditor",
  description="Security audit"
)

Task(
  prompt="<task>Test coverage audit. TaskId: {task_id_2}</task> ...",
  subagent_type="codebase-auditor",
  description="Coverage audit"
)

Task(
  prompt="<task>Dead code audit. TaskId: {task_id_3}</task> ...",
  subagent_type="codebase-auditor",
  description="Dead code audit"
)

## 3. Consolidate

When all three return, write AUDIT-REPORT.md combining their findings.
</process>
```

---

**File: `.claude/agents/codebase-auditor.md`**

```markdown
---
name: codebase-auditor
description: Runs a focused codebase audit (security, coverage, or dead code). Spawned by /my:audit.
tools: Read, Bash, Glob, Grep, TaskUpdate, TaskGet
model: sonnet
---

<role>
You are a focused codebase auditor. You perform one specific audit task and report findings.

You have access to TaskUpdate and TaskGet so you can update your own task status in the shared task list.
</role>

<process>

## 1. Claim your task

Read the TaskId from your prompt. Then:

TaskUpdate({ taskId: "{task_id}", status: "in_progress" })

## 2. Do the audit

Read the audit type from your prompt and execute accordingly:

**Security:** Grep for hardcoded secrets, eval(), raw SQL concatenation, unvalidated inputs. Check package.json for known vulnerable deps.

**Test coverage:** Glob for source files, cross-reference with test files. List src files with no corresponding test file. Grep for exported functions with no test imports.

**Dead code:** Grep for exported symbols, check which are never imported elsewhere. Find files not referenced by any import.

## 3. Return findings

Structure your response as:

## AUDIT COMPLETE: {audit_type}

### Findings
- ...

### Severity
HIGH / MEDIUM / LOW

## 4. Update task status

TaskUpdate({ taskId: "{task_id}", status: "completed" })

</process>
```

---

**Why TaskTools add value here vs. not using them:**

| Without TaskTools | With TaskTools |
|---|---|
| User sees nothing until all 3 agents finish | User sees live spinner: "Scanning for security issues..." |
| No way for agents to signal they've started | Each agent marks itself `in_progress` immediately |
| Orchestrator has no structured way to check state | Orchestrator can call `TaskList` to see what's done |
| If one agent fails, hard to tell which | Failed agent stays `in_progress`, making the gap visible |

---

**Where TaskTools genuinely add value:** multi-agent workflows where tasks are independent, long-running, and you want the user to see structured progress. For a simple sequential workflow with 3 steps, they add ceremony without much benefit — natural language progress messages ("Step 1 done, starting step 2...") are often sufficient.


# When claude code Tasks are useful: to see progress in UI

Honestly, the main value is UI feedback during a long multi-agent run within a single session.

  When Claude spawns several agents in parallel and each one calls TaskUpdate({ status: "in_progress" }), the Claude Code UI shows live spinners with the      
  activeForm label you defined — "Scanning for security issues...", "Analysing test coverage..." — so the user can see what's happening in real time rather    
  than staring at a blank screen waiting for all agents to finish.

  That's essentially it. The other features (dependencies via addBlockedBy, structured state via TaskList) are nice in theory but in practice Claude can track 
  that same information in its own working context just as reliably.

  So the honest cost/benefit:

  ┌────────────────────────────────────────────┬───────────────────────────────────────────────────────┐
  │                  Benefit                   │                       How real                        │
  ├────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
  │ Live progress spinners for parallel agents │ Genuinely useful                                      │
  ├────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
  │ User can see which agent is stuck          │ Genuinely useful                                      │
  ├────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
  │ Dependency enforcement between tasks       │ Marginal — Claude can reason about this without tools │
  ├────────────────────────────────────────────┼───────────────────────────────────────────────────────┤
  │ Structured state for orchestrator          │ Marginal — Claude holds this in context anyway        │
  └────────────────────────────────────────────┴───────────────────────────────────────────────────────┘

  When it's not worth it:
  - Sequential workflows — just narrate progress in plain text
  - Short tasks — overhead of TaskCreate/TaskUpdate calls isn't worth it
  - Any workflow where you need cross-session persistence — use files instead

  Bottom line: if you're building a workflow that spawns 3+ parallel agents and the user will be watching it run, TaskTools earn their keep purely through the 
  spinner UX. Otherwise they add ceremony for little gain.
  
# Lack of documentation on TaskTools and TodoWrite

https://www.reddit.com/r/ClaudeAI/comments/1mo40o3/has_anyone_found_configuration_options_for_claude/

