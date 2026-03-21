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

