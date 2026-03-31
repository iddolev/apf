# Sequential Thinking MCP Server

Recommended by: https://www.youtube.com/watch?v=-O6MEtleOdA

## Installation

Ask Claude Code:

> please install sequential thinking mcp server

## How it was installed

The `@modelcontextprotocol/server-sequential-thinking` npm package was installed as an MCP server registered in the Claude config at `C:\Users\Iddo\.claude.json`.

**The config entry added:**
```json
"mcpServers": {
  "sequential-thinking": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
    "env": {}
  }
}
```

This is at the **user level** (in `~/.claude.json`), meaning it's available in all Claude Code sessions.

**How it works at runtime:** When Claude Code starts, it launches the MCP server as a child process via `npx`. It communicates over stdio using the MCP protocol. This is why `mcp__sequential-thinking__sequentialthinking` appears in the available deferred tools — it's provided by that server.

The actual server code is not stored locally; `npx -y` downloads and runs `@modelcontextprotocol/server-sequential-thinking` from npm on demand each time it's invoked.

---

## Where the config lives

**File:** `C:\Users\Iddo\.claude.json`

You can verify with:
```
grep -A8 "sequential-thinking" ~/.claude.json
```

(`-A8` means "show 8 lines After each match" — prints the full JSON block after the matching key.)

---

## What are "deferred tools"?

At the start of every session, Claude Code receives a hidden system-level message listing tools that are available but not yet loaded into context — these are called **deferred tools**. The full schema (parameters, description) of each tool hasn't been loaded yet to save space. To use one, Claude first calls `ToolSearch` to fetch its schema, then can invoke it.

The `mcp__sequential-thinking__sequentialthinking` entry in that list confirms the MCP server is running and registered successfully. The naming convention is `mcp__<server-name>__<tool-name>`.

This system message is not visible to the user in the UI — only Claude sees it.

---

## How to activate it

**Option 1 — Ask Claude directly:**

> "Use sequential thinking to plan X"

**Option 2 — Claude invokes it itself** when it judges a problem is complex enough and benefits from step-by-step reasoning.

---

## What it does upon activation

It's a structured reasoning tool — instead of generating an answer in one shot, the tool lets Claude work through a problem as a **chain of numbered thoughts**, where each thought can:

- Build on the previous one
- Revise or backtrack on an earlier assumption
- Branch into sub-problems

Each "thought" is a discrete step submitted to the tool, and Claude can keep adding steps until it reaches a conclusion.

**Example — without sequential thinking:**
> You ask a complex architectural question → Claude answers in one response, possibly missing edge cases

**Example — with sequential thinking:**
> Thought 1: "What are the constraints?" → Thought 2: "Given constraint A, option X won't work..." → Thought 3: "Wait, I missed dependency B, revising..." → Thought N: Final answer

---

## When it's actually useful

- Multi-step planning with dependencies
- Problems where you want to see the reasoning, not just the conclusion
- Cases where Claude might otherwise jump to a wrong answer confidently

In most day-to-day coding tasks it's overkill — a single response is faster and sufficient.
