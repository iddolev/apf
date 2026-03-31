# context7 Plugin

## How to install

Official plugin (Claude Code comes with the ability to install it using `/plugin` manager).

## Is context7 installed?

Yes — context7 is installed and active. It's listed in the MCP servers and its tools are available:

- `mcp__plugin_context7_context7__resolve-library-id`
- `mcp__plugin_context7_context7__query-docs`

## Where are the plugin definition files?

Plugin definitions live at:

```
C:\Users\Iddo\.claude\plugins\
```

Key locations:
- **Cache (full plugin files):** `~/.claude/plugins/cache/claude-plugins-official/<plugin-name>/<version>/`
- **context7 specifically:** `~/.claude/plugins/cache/claude-plugins-official/context7/unknown/`
  - `plugin.json` — plugin metadata
  - `.mcp.json` — MCP server config
- **Installed plugins registry:** `~/.claude/plugins/installed_plugins.json`
- **Enabled plugins config:** `~/.claude/settings.json` (the `enabledPlugins` key)

## Is context7 a remote server or locally installed?

It runs locally via `npx` — it downloads and executes the `@upstash/context7-mcp` npm package on your machine each time it's invoked. So it's not a persistent remote server, but it's also not pre-installed — it's fetched from npm on demand (and cached by npm after the first run).

`.mcp.json` config:

```json
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"]
  }
}
```

## How is the server invoked?

Claude Code reads the `.mcp.json` config and spawns the server as a **stdio subprocess** when a session starts:

```
npx -y @upstash/context7-mcp
```

Claude Code communicates with it over **stdin/stdout** using the MCP protocol (JSON-RPC). When a tool like `mcp__plugin_context7_context7__query-docs` is called, Claude Code sends a JSON-RPC request to that process and reads the response.

The `-y` flag tells npx to skip the install confirmation prompt. After the first run, npm caches the package locally.

## What kind of files define the server?

The server implementation is **compiled JavaScript** (`.js` files in a `dist/` folder), originally written in TypeScript. The cached copy is at:

```
C:\Users\Iddo\AppData\Local\npm-cache\_npx\eea2bd7412d4593b\node_modules\@upstash\context7-mcp\dist\
```

Key files:
- `index.js` — entry point / MCP server setup
- `lib/api.js` — calls out to Upstash's remote API to fetch docs
- `lib/types.js`, `utils.js`, etc. — supporting code

The server runs **locally as a Node.js process**, but makes **HTTP calls to Upstash's remote API** to actually retrieve documentation. It's a thin local proxy for a remote service.

## What kind of documentation is retrieved?

It retrieves **library and framework documentation** via two tools:

1. **`resolve-library-id`** — searches Upstash's database for a library by name and returns metadata: library ID, description, number of code snippets, source reputation, benchmark score, and available versions.

2. **`query-docs`** — fetches actual documentation content for a specific library ID, ranked/filtered by your query. Returns text including API syntax, configuration options, code examples, etc.

The content comes from Upstash's own curated index at `context7.com` — they crawl and index official docs for popular libraries (React, Next.js, Express, Django, etc.) and serve back relevant excerpts matched to your specific question.

## What triggers Claude to consult context7?

A few things drive that decision:

1. **The MCP server's own instructions** — loaded into Claude's system context at session start:
   > *"Use this server to fetch current documentation whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service — even well-known ones like React, Next.js... Use even when you think you know the answer."*

2. **Claude's own judgment** — more likely to consult it when:
   - The question is about specific API syntax or configuration details
   - The library has been changing rapidly (e.g. Next.js App Router)
   - The question involves version-specific behavior
   - There's uncertainty about whether training data is current

3. **What Claude might skip it for** — general conceptual questions, well-understood stable APIs, or when fairly confident the answer hasn't changed since training cutoff.

## Can I force Claude to consult context7?

Not in a hard technical sense, but you can make it very likely:

1. **Explicitly ask for it:** "Use context7 to look up how to use useEffect in React."
2. **Mention a specific version:** "How does useEffect work in React 19?" — version-specific questions make training data unreliable.
3. **Frame it as needing current docs:** "Check the latest React docs for useEffect."

The instructions say Claude *should* use it proactively for library questions, but Claude's own confidence in its training data competes with that instruction. Explicitly requesting it removes the ambiguity.
