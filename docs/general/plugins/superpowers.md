# Superpowers Plugin — How It Works

A Q&A walkthrough of the Superpowers Claude Code plugin: its installation, skill system, hooks, and runtime behavior.

---

## Where is the brainstorming skill installed?

The skill is located at:

```
C:\Users\Iddo\.claude\plugins\cache\claude-plugins-official\superpowers\5.0.6\skills\brainstorming
```

There is also a `5.0.5` version in the same path — the active one is `5.0.6`.

---

## Files in the brainstorming skill

```
scripts/frame-template.html
scripts/helper.js
scripts/server.cjs
scripts/start-server.sh
scripts/stop-server.sh
SKILL.md
spec-document-reviewer-prompt.md
visual-companion.md
```

| File | Purpose |
|------|---------|
| `SKILL.md` | Main skill definition — the 9-step checklist, process flow, principles, and visual companion overview |
| `visual-companion.md` | Detailed guide for the browser-based visual companion (when/how to use it, the server loop, CSS classes, event format) |
| `spec-document-reviewer-prompt.md` | Template for dispatching a subagent to review the written spec document |
| `scripts/server.cjs` | Node.js HTTP + WebSocket server that watches a directory and serves HTML screens to the browser |
| `scripts/start-server.sh` | Shell script to start the server, handling platform differences (Windows, Codex, Gemini, macOS/Linux) |
| `scripts/stop-server.sh` | Shell script to kill the server and clean up ephemeral `/tmp` sessions |
| `scripts/helper.js` | Client-side JS injected into every page — manages WebSocket connection, click event capture, and `toggleSelect` |
| `scripts/frame-template.html` | HTML/CSS frame template wrapping content fragments with header, theme, and indicator bar |

---

## Are skills automatically loaded, or only on explicit request?

### Session start — automatic injection of `using-superpowers` only

When every session starts, a `SessionStart` hook runs (`hooks/session-start`). It reads `skills/using-superpowers/SKILL.md` and injects its **full content** into Claude's context automatically, inside `<EXTREMELY_IMPORTANT>` tags.

### All other skills — listed by name/description only

Every other skill (brainstorming, TDD, debugging, etc.) is listed in Claude's context as a short entry like:
> `- superpowers:brainstorming: You MUST use this before any creative work...`

That's just the name + one-line description. The full skill content is **not** loaded — it's a stub/pointer.

### Full skill content — loaded on demand via `Skill` tool

When Claude (or the user via `/skill-name`) invokes a skill through the `Skill` tool, the full content of that skill's `SKILL.md` is loaded into context at that moment.

### Summary

| Question | Answer |
|----------|--------|
| Is the plugin active every session? | Yes — `using-superpowers` is fully injected on every session start via hook. |
| Are other skills auto-loaded? | No — only their name + description is listed, not the full content. |
| Can Claude proactively activate a skill? | Yes. The `using-superpowers` skill instructs Claude to invoke relevant skills proactively — even at 1% chance of relevance. |
| Is activation only on explicit user request? | No. Claude is supposed to self-trigger skills based on what you ask. |

---

## Is skill activation visible or silent?

Always visible. Two layers:

1. **The `Skill` tool call is visible** — like any tool call (Read, Bash, Grep), invoking the `Skill` tool shows up in the UI.
2. **The skill requires an explicit announcement** — from the `using-superpowers` flow: `"Invoke Skill tool" -> "Announce: 'Using [skill] to [purpose]'"`. Claude must say something like *"Using brainstorming to explore your feature idea"* before doing anything else.

---

## How does Claude know which skills exist?

The root registration file is:

```
C:\Users\Iddo\.claude\plugins\installed_plugins.json
```

Claude Code reads this at startup to know which plugins are installed and where their files are. From there it finds each plugin's `hooks/hooks.json`, which declares the `SessionStart` hook and what command to run.

---

## How does the SessionStart hook work?

### `hooks/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|compact",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start",
            "async": false
          }
        ]
      }
    ]
  }
}
```

This tells Claude Code: on session start, run `run-hook.cmd session-start`.

### `hooks/run-hook.cmd` — a polyglot script

`run-hook.cmd` is a single file that executes correctly as both a Windows `.cmd` batch file AND a Unix bash script.

**When Windows runs it (cmd.exe):**
- The `:<< 'CMDBLOCK'` line is a no-op label in cmd.exe, so it falls through to the batch code
- It looks for `bash.exe` in standard Git for Windows locations, or falls back to `bash` on PATH
- Once found, runs: `bash "<hook-dir>\session-start"`
- If no bash found, exits silently (plugin still loads, just without context injection)

**When bash runs it (Linux/macOS/Git Bash):**
- `:<< 'CMDBLOCK'` is a here-document redirect to a no-op — everything until `CMDBLOCK` is discarded
- After `CMDBLOCK`, bash resolves its own directory and calls `exec bash "${SCRIPT_DIR}/session-start"`

**Why `session-start` has no extension:**
Intentional. If it were named `session-start.sh`, Claude Code on Windows would auto-prepend `bash` to the command, conflicting with the wrapper's own logic. Extensionless avoids that.

| Platform | What runs `run-hook.cmd` | What it does with `session-start` |
|----------|--------------------------|-----------------------------------|
| Windows | `cmd.exe` | Finds Git Bash, calls `bash session-start` |
| Linux/macOS | bash directly | Discards batch block, calls `exec bash session-start` |

Works on both platforms.

---

## What does `session-start` do when run?

### Step 1 — Locate the plugin root

```bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
```

`SCRIPT_DIR` = the `hooks/` folder. `PLUGIN_ROOT` = one level up = the superpowers plugin root (`5.0.6/`).

### Step 2 — Check for legacy skills (optional warning)

```bash
legacy_skills_dir="${HOME}/.config/superpowers/skills"
if [ -d "$legacy_skills_dir" ]; then
    warning_message="...⚠️ WARNING: move custom skills to ~/.claude/skills..."
fi
```

If an old-style skills directory exists from a previous superpowers version, builds a warning message to inject.

### Step 3 — Read the `using-superpowers` skill content

```bash
using_superpowers_content=$(cat "${PLUGIN_ROOT}/skills/using-superpowers/SKILL.md")
```

Reads the full text of `SKILL.md` into a variable.

### Step 4 — Escape it for JSON embedding

```bash
s="${s//\\/\\\\}"   # backslashes
s="${s//\"/\\\"}"   # double quotes
s="${s//$'\n'/\\n}" # newlines
s="${s//$'\r'/\\r}" # carriage returns
s="${s//$'\t'/\\t}" # tabs
```

All special characters escaped with bash string substitution so the content can be embedded in a JSON string value.

### Step 5 — Build the context string

Wraps the escaped skill content in `<EXTREMELY_IMPORTANT>` tags:

```
<EXTREMELY_IMPORTANT>
You have superpowers.

**Below is the full content of your 'superpowers:using-superpowers' skill...**

[full SKILL.md content]
</EXTREMELY_IMPORTANT>
```

### Step 6 — Output the correct JSON format for the platform

```bash
if [ -n "${CURSOR_PLUGIN_ROOT:-}" ]; then
    printf '{ "additional_context": "%s" }\n' "$session_context"
elif [ -n "${CLAUDE_PLUGIN_ROOT:-}" ]; then
    printf '{ "hookSpecificOutput": { "hookEventName": "SessionStart", "additionalContext": "%s" } }\n' "$session_context"
else
    printf '{ "additional_context": "%s" }\n' "$session_context"
fi
```

Different platforms expect different JSON shapes:
- **Cursor** uses `additional_context`
- **Claude Code** uses `hookSpecificOutput.additionalContext`
- **Other** falls back to `additional_context`

Claude Code reads the output of this script and injects the `additionalContext` value into Claude's context at session start. It appears in the system metadata of the first user turn — visible to Claude but not shown as a standalone chat message in the UI.

### The full flow in one line

`hooks.json` triggers → `run-hook.cmd` finds bash → bash runs `session-start` → reads `SKILL.md` → escapes it → prints JSON → Claude Code injects it into Claude's context.

---

## The `using-superpowers` skill — what it does

Three files:

### `SKILL.md` — the meta-skill

This is injected at session start. Its job is to bootstrap Claude with the rules for *how to use all other skills*.

**`<SUBAGENT-STOP>`** — Subagents dispatched to do a specific task skip this skill entirely.

**`<EXTREMELY-IMPORTANT>` block** — Core rule: if there's even a 1% chance a skill applies, Claude MUST invoke it. Non-negotiable.

**Instruction priority:**
1. User's explicit instructions (CLAUDE.md etc.) — always win
2. Superpowers skills — override Claude's defaults
3. Claude's built-in system prompt — lowest priority

**Decision flowchart** — On every message:
- Is a skill relevant? → invoke it via `Skill` tool
- Announce what Claude is doing
- If the skill has a checklist → create tasks for each item
- Follow the skill exactly

**Red flags table** — Rationalizations Claude might use to skip invoking a skill, each countered. e.g. *"This is just a simple question"* → *"Questions are tasks. Check for skills."* Anti-laziness guardrailing.

**Skill types:**
- **Rigid** (TDD, debugging): follow exactly
- **Flexible** (patterns): adapt to context

### `references/codex-tools.md`

Tool name mapping for OpenAI Codex users, since skills use Claude Code tool names. Includes a workaround for Codex not having a named agent registry.

### `references/gemini-tools.md`

Tool name mapping for Gemini CLI. Notable: Gemini has no subagent support, so skills relying on parallel subagents fall back to single-session execution.

`using-superpowers` is a **meta-skill** — it doesn't do any work itself. Its sole job is to establish the rules for using all other skills.

---

## The brainstorming `SKILL.md` — walkthrough

### `<HARD-GATE>`

```
Do NOT invoke any implementation skill, write any code, scaffold any project,
or take any implementation action until you have presented a design and
the user has approved it.
```

The most important single rule. No code until a design exists and the user approves. This is a **rigid** skill — not adaptable.

### Anti-Pattern block

Addresses the rationalization *"this is too simple to need a design."* The answer: every project goes through this process. Even a single-function utility. The design can be short, but it must exist and be approved.

### The 9-step checklist

Claude must create a task for each item and complete them in order:

1. **Explore project context** — read files, docs, recent commits before asking anything
2. **Offer visual companion** — if the topic will involve visual questions, offer the browser companion *in its own message, nothing else*
3. **Ask clarifying questions** — one at a time, purpose/constraints/success criteria
4. **Propose 2-3 approaches** — with trade-offs and a recommendation
5. **Present design** — section by section, get approval after each section
6. **Write design doc** — saved to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`, committed to git
7. **Spec self-review** — inline check for placeholders, contradictions, ambiguity, scope issues
8. **User reviews written spec** — explicit gate: ask user to read the file before proceeding
9. **Transition to implementation** — invoke `writing-plans` skill and *only* that skill

### Process flow

The `digraph` encodes the decision tree. The terminal state is explicitly labelled: **invoking `writing-plans` is the only valid exit.** No jumping to `frontend-design` or any other implementation skill.

### The Process (detailed)

**Understanding the idea:**
- Scope check first — if the request covers multiple independent subsystems, decompose before asking details
- One question per message, multiple choice preferred
- Focus on: purpose, constraints, success criteria

**Exploring approaches:**
- Always propose 2-3 options, never jump to one solution
- Lead with the recommended option and explain why

**Presenting the design:**
- Scale section length to complexity
- Ask after each section: "does this look right so far?"
- Cover: architecture, components, data flow, error handling, testing

**Design for isolation:**
- Each unit should have one clear purpose, well-defined interfaces, independently testable
- Large files are a signal something is doing too much

**Existing codebases:**
- Explore structure first, follow existing patterns
- Include targeted improvements for problems that affect the work
- Don't propose unrelated refactoring

### After the design

**Spec self-review (4 checks):**
1. Placeholder scan — any TBD, TODO, incomplete sections?
2. Internal consistency — do sections contradict each other?
3. Scope check — focused enough for a single plan?
4. Ambiguity check — can any requirement be read two ways?

**User review gate — exact wording specified:**
> *"Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."*

Wait for user approval before proceeding.

### Key principles

- One question at a time
- Multiple choice preferred
- YAGNI ruthlessly — cut unnecessary features
- Always propose 2-3 approaches
- Incremental validation
- Go back and clarify when something doesn't make sense

---

## Does "I want to create X" necessarily trigger brainstorming?

**It should, but it's not mechanically guaranteed.**

**Why it should:** The `using-superpowers` skill says on every message Claude must check "might any skill apply?" before doing anything. The brainstorming skill's description reads: *"You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior."* "I want to create X" is unambiguously creative work.

**Why it's not mechanically guaranteed:** There's no code enforcing this. Unlike the `SessionStart` hook — which runs deterministically as a shell script — this is purely instruction-following by an LLM. The skill authors know this, which is why the language is so aggressive ("ABSOLUTELY MUST", "not negotiable, not optional", "you cannot rationalize your way out of this", the entire red flags table). All of that exists precisely *because* an LLM can always find a reason not to follow a rule. The stronger the framing, the more likely compliance — but it's still probabilistic, not deterministic.

**In short:** "I want to create X" should reliably trigger brainstorming because the match is obvious. Where it gets shakier is with ambiguous requests where the skill match isn't immediately obvious — that's the gap the red flags table tries to close.

---

## Code-reviewer Was Wrongly Called

When the "brainstorming" skill was running, at some point around spec review loop, 
claude decided to run the "code-reviewer" agent (which is defined as part of the superpowers plugin).

So I asked Claude: 
Explain why you invoked superpowers:code-reviewer now, before there is any code to review

### Claude answered

You're right to call that out. I shouldn't have.

  The brainstorming skill instructs me to "dispatch a spec-document-reviewer subagent" — that's a generic subagent I should have described and prompted from scratch, not
  superpowers:code-reviewer. That agent is meant for reviewing implemented code against a plan and coding standards, not for reviewing a design document.

  What I did worked incidentally — I gave the agent a clear spec-review prompt and it behaved reasonably — but I grabbed the wrong tool. I should have either:

  - Dispatched a plain general-purpose agent with a well-crafted spec-review prompt, or
  - Done the spec review inline myself, since the document was short enough

  I'll use superpowers:code-reviewer correctly going forward: only after code has been written.

### My opinion

Relying on the LLM to follow such instructions and know where to run which agent is not reliable.

---

## Actual behavior

### Unreasonably long/detailed plan

This thing produced a "plan" which is 1150 lines long all in one file. 
With a lot of snippets of long python code (instead of relying on a "coder" to write them).
It's not really a plan with steps (like in APF), but all or most "fleshed out".
No wonder it works so slowly.

### Took way too much time

Took a lot of time, even for steps that already had planned, 
plus Claude Code continuously stopped to ask yes/no questions. 
It's very unpractical. 

