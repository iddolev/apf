# GSD vs. UltraWork (oh-my-opencode) — Systematic Comparison

## 1. Identity & Target

| | **GSD (Get Shit Done)** | **UltraWork (oh-my-opencode / OmO)** |
|---|---|---|
| **Claims to be** | "Lightweight meta-prompting, context engineering, and spec-driven development system" | "The Best AI Agent Harness — batteries-included OpenCode plugin" |
| **Primary target** | **Claude Code** (also supports OpenCode, Gemini CLI, Codex) | **OpenCode** (a fork/competitor of Claude Code) |
| **Philosophy** | Anti-enterprise. Solve "context rot" via orchestration | Break model lock-in via multi-provider orchestration |
| **Stars** | ~29,800 | ~39,900 |
| **License** | MIT (fully open) | Sustainable Use License (free for personal/non-commercial; restrictive for commercial redistribution) |
| **Installation** | `npx get-shit-done-cc@latest` → copies markdown files into `.claude/` | `bunx oh-my-opencode install` → npm package + OpenCode plugin config |

---

## 2. Architecture Philosophy

| | **GSD** | **UltraWork** |
|---|---|---|
| **Instruction format** | **152 markdown files** — human-readable, editable, in `.claude/` | **Single 3.4 MB compiled JS bundle** — prompts baked into TypeScript |
| **Distribution** | Files copied to project directory — fully transparent | npm package loaded as OpenCode plugin — opaque |
| **Editability** | Open any `.md` file and modify | Must fork repo & rebuild to change prompts |
| **Runtime** | Node.js CLI (`gsd-tools.cjs`, 592 lines) + Claude Code subagent spawning | OpenCode plugin API (65 hooks, 26 tools, 3 MCP servers) |
| **State management** | Filesystem: `STATE.md`, `ROADMAP.md`, plan/summary/verification files | In-memory + filesystem: `.sisyphus/` directory, `boulder.json`, `ralph-loop.local.md` |
| **Extension model** | Edit markdown files directly; add commands/workflows/templates | Load skills (`SKILL.md`), configure `oh-my-opencode.json`, write AGENTS.md rules |

---

## 3. Agent Systems

| | **GSD (7 agents)** | **UltraWork (11 agents)** |
|---|---|---|
| **Orchestrator** | *Implicit* — commands/workflows ARE the orchestration | **Sisyphus** — explicit primary orchestrator agent |
| **Planner** | **gsd-planner** — creates PLAN.md with frontmatter, must-haves, waves | **Prometheus** — interview → Metis consultation → plan generation → Momus review |
| **Executor** | **gsd-executor** — atomic commits, deviation rules, checkpoints | **Hephaestus** (GPT-only deep worker) + **Sisyphus Junior** (lightweight tasks) |
| **Verifier** | **gsd-verifier** — goal-backward, 3-level artifact checks, gap detection | **Momus** (plan review) + Ralph Loop (iteration verification) |
| **Debugger** | **gsd-debugger** — scientific method, hypothesis testing, persistent sessions | *No dedicated debugger* — Oracle handles debugging consultation |
| **Researcher** | **gsd-phase-researcher** — produces RESEARCH.md | **Librarian** (external docs) + **Explore** (codebase patterns) |
| **Plan checker** | **gsd-plan-checker** — validates plans against goals before execution | **Metis** (pre-planning gap analysis) + **Momus** (post-plan review) |
| **Roadmapper** | **gsd-roadmapper** — milestone/phase hierarchy creation | *No equivalent* — planning is task-scoped, not project-scoped |
| **Advisor** | *No equivalent* | **Oracle** — architecture, strategy, debugging (GPT-native) |
| **Todo orchestrator** | *No equivalent* | **Atlas** — plan execution coordination |
| **Visual analyzer** | *No equivalent* | **Multimodal-Looker** — image/screenshot analysis |

---

## 4. Planning Pipeline

| Aspect | **GSD** | **UltraWork** |
|---|---|---|
| **Trigger** | `/gsd:plan-phase {N}` command | Tab key → Prometheus mode, or `ultrawork` keyword |
| **Pre-planning** | `/gsd:discuss-phase` captures user decisions → CONTEXT.md (locked/deferred/discretion) | Prometheus Phase 0: intent classification (trivial/refactoring/build/architecture/research) |
| **Research** | gsd-phase-researcher → RESEARCH.md (confidence levels, standard stack, pitfalls) | Parallel explore + librarian agents in background |
| **Plan format** | Markdown PLAN.md with YAML frontmatter (`phase`, `wave`, `depends_on`, `must_haves`, `requirements`) | Markdown in `.sisyphus/plans/{name}.md` with task dependency graph + parallel execution waves |
| **Plan validation** | gsd-plan-checker validates requirement coverage, dependency correctness, scope sanity (max 3 revision iterations) | Metis (gap analysis) + optional Momus review (executability, blocking issues) |
| **Scope control** | Tasks: 15-60 min, 2-3 per plan, ~50% context budget | Category-based delegation with model-specific context budgets |
| **Project hierarchy** | **Milestones → Phases → Plans → Tasks → Waves** (full project lifecycle) | **Plans → Tasks** (session-scoped, no project-level hierarchy) |

---

## 5. Execution Model

| Aspect | **GSD** | **UltraWork** |
|---|---|---|
| **Parallelization** | **Wave-based**: independent plans in same wave run parallel; waves execute sequentially | **Background tasks**: fire 5+ agents simultaneously; category-based routing to optimal models |
| **Executor agent** | gsd-executor with fresh 200K context per plan | Hephaestus (GPT-only, deep) or Sisyphus Junior (lightweight) per task |
| **Atomic commits** | Per-task: `feat(phase-plan): description` | Per-task via git-master skill: ceil(N/3) commits minimum |
| **Deviation handling** | 4 rules: auto-fix bugs (R1), auto-add critical functionality (R2), auto-fix blockers (R3), ask for architectural changes (R4) | Sisyphus prompt: "Fix minimally. NEVER refactor while fixing." + 3-failure escalation to Oracle |
| **Checkpoints** | 3 types: `human-verify` (90%), `decision` (9%), `human-action` (1%) with auto-advance mode | TodoWrite tracking with manual QA mandate; no formal checkpoint protocol |
| **Context strategy** | Fresh 200K per subagent; orchestrator stays at 10-15%; paths passed, not file contents | Category-based model selection; session_id for continuation; preemptive compaction hooks |
| **Model routing** | Profile-based: quality/balanced/budget → Opus/Sonnet/Haiku per agent role | Category-based: 8 categories → specific models (Gemini for visual, GPT-5.3-codex for ultrabrain, Haiku for quick) |

---

## 6. Verification

| Aspect | **GSD** | **UltraWork** |
|---|---|---|
| **Philosophy** | **Goal-backward**: "Does codebase deliver what phase promised?" (not "did tasks complete?") | **Evidence-based**: lsp_diagnostics (types) + manual QA (functional) + test suite |
| **Artifact checking** | 3 levels: exists → substantive (not stub) → wired (imported/used) | lsp_diagnostics for type errors; manual execution for functional bugs |
| **Stub detection** | Explicit patterns: `return null`, empty onClick, fetch without await | Not formalized — relies on agent judgment |
| **Gap closure** | VERIFICATION.md with YAML gaps → `/gsd:plan-phase --gaps` creates targeted fix plans | Ralph Loop: iterative verification with configurable max iterations |
| **UAT** | `/gsd:verify-work` — conversational testing, one test at a time, auto-diagnosis | Manual QA mandate in prompts; evidence files in `.sisyphus/evidence/` |
| **Re-verification** | Loads previous VERIFICATION.md, focuses on failed items, checks for regressions | Ralph Loop re-runs with iteration counter; boulder state tracks remaining tasks |

---

## 7. Continuation & State

| Aspect | **GSD** | **UltraWork** |
|---|---|---|
| **Cross-session state** | `STATE.md` (project memory) + `ROADMAP.md` + per-phase PLAN/SUMMARY/VERIFICATION files | `.sisyphus/boulder.json` (active plan) + `.sisyphus/ralph-loop.local.md` (loop state) |
| **Session resumption** | Re-run command → discovers completed summaries → skips done plans → resumes from first incomplete | `session_id` parameter preserves full conversation context; boulder injects remaining tasks |
| **Continuation model** | Fresh agent with explicit state passed in (avoids context serialization issues) | Session continuation: same agent resumes with full context preserved |
| **Project memory** | STATE.md tracks: position, metrics, decisions, blockers, velocity trends | Boulder tracks: active plan, session IDs, agent type, worktree path |

---

## 8. Model Support

| | **GSD** | **UltraWork** |
|---|---|---|
| **Primary model** | Claude (Opus/Sonnet/Haiku) | Claude Opus 4.6 (Sisyphus optimized) |
| **Multi-provider** | Limited — 3 profiles (quality/balanced/budget) mapping to Anthropic models | Extensive — 7 providers: Anthropic, OpenAI, Google, Kimi, GLM, Venice, OpenCode Zen |
| **Model-per-agent** | Per-role overrides via model profiles (planner=Opus, executor=Sonnet) | Per-agent fallback chains + per-category model assignment |
| **Prompt variants** | Claude-optimized only | Dual prompts for Claude + GPT; Gemini-specific variants for some agents |
| **GPT support** | Not architecturally supported | First-class: Hephaestus (GPT-only), Oracle (GPT-preferred), GPT-specific prompt variants |

---

## 9. Tooling & Extensibility

| | **GSD** | **UltraWork** |
|---|---|---|
| **Tools** | Standard Claude Code tools (Read, Write, Edit, Bash, Grep, Glob, WebFetch) + gsd-tools.cjs CLI | 26 custom tools: LSP (goto definition, find references, rename), AST-grep, hashline edit, session manager, delegate task, interactive bash, look_at |
| **MCP servers** | Uses Claude Code's built-in MCP support | 3 bundled: websearch (Exa), context7 (docs), grep_app (GitHub code search) |
| **Hooks** | 16 lifecycle events (SessionStart, PostToolUse, SubagentStart, etc.) via settings.json | **65 hooks**: context injection, error recovery, model fallback, compaction, rules injection, keyword detection, and more |
| **Skills** | Via Claude Code's native skill system (`.claude/skills/`) | Skill system with `SKILL.md` files, `load_skills` parameter, SkillMcpManager for MCP-based skills |
| **Commands** | 33 slash commands (`/gsd:plan-phase`, `/gsd:execute-phase`, etc.) | Slash commands: `/init-deep`, `/ralph-loop`, `/start-work`, `/refactor`, `/handoff` |

---

## 10. Key Strengths

| **GSD excels at** | **UltraWork excels at** |
|---|---|
| **Project-level orchestration** — milestones, phases, roadmaps | **Session-level orchestration** — quick delegation, parallel background agents |
| **Transparency** — every instruction is a readable markdown file | **Multi-model routing** — right model for each task type |
| **Goal-backward verification** — checks outcomes, not task completion | **Tool depth** — LSP, AST-grep, hashline edits unavailable in vanilla Claude Code |
| **Formal state management** — STATE.md, ROADMAP.md, structured gap closure | **Automatic continuation** — Ralph Loop + Boulder track progress without manual state files |
| **Checkpoint protocol** — structured human-in-the-loop at right moments | **Hook extensibility** — 65 hooks for almost any lifecycle event |
| **Scientific debugging** — hypothesis-driven investigation with persistent sessions | **Model-specific prompt optimization** — Claude, GPT, and Gemini each get tailored prompts |
| **Context rot mitigation** — explicit context budgets, fresh 200K per agent | **Speed** — background agents run in parallel without waiting |
| **Editability** — any user can modify agent behavior by editing .md files | **Provider diversity** — works across 7+ LLM providers |

---

## 11. Key Weaknesses

| **GSD weaknesses** | **UltraWork weaknesses** |
|---|---|
| Claude-centric — limited multi-model support | No project-level hierarchy (milestones, roadmaps, phases) |
| Heavyweight setup for small tasks — overkill for quick fixes | Opaque — can't read or edit agent prompts without forking |
| No dedicated architecture advisor (Oracle equivalent) | No formal checkpoint protocol — human-in-the-loop is ad-hoc |
| No LSP, AST-grep, or advanced code analysis tools | No dedicated debugger agent — Oracle consultation isn't the same as GSD's scientific debugging |
| Model selection limited to Claude variants | Verification less rigorous — no 3-level artifact checking or stub detection |
| ~152 separate files to manage | ~1 GB on disk for npm packages + cache |
| Tied to Claude Code's subagent architecture | Tied to OpenCode's plugin architecture |

---

## 12. Detailed Gap Analysis

### GSD — Where It Falls Short

**1. Model Monoculture**
GSD's prompts are Claude-optimized only. There are no GPT or Gemini prompt variants. The "model profiles" (quality/balanced/budget) just toggle between Opus, Sonnet, and Haiku — all Anthropic. If Claude has a bad day, you have no fallback to a fundamentally different model family. The gsd-executor gets a PLAN.md that's been written assuming Claude's instruction-following style — hand that to GPT-5.3-codex and the formatting assumptions break.

**2. Ceremony Tax on Small Tasks**
Need to fix a typo? GSD's lightest path is still: command → workflow → agent spawn → fresh context load → execution → summary → state update. There's no "just do it" equivalent to UltraWork's `ulw` keyword or `category="quick"` delegation. Every task goes through the same multi-file orchestration pipeline. This makes GSD feel heavyweight for the 60% of coding work that's small changes.

**3. No Code Intelligence Tools**
GSD agents use basic tools: Read, Write, Edit, Bash, Grep, Glob. There's no LSP (goto definition, find references, rename), no AST-grep (structural code search/replace), no hashline edit (content-verified line editing). The gsd-executor modifying a function signature has no way to find all call sites automatically — it greps and hopes. This means refactoring tasks are significantly more error-prone.

**4. Markdown-as-Code Fragility**
152 markdown files ARE the system. But markdown is loosely structured — a misplaced heading level, a broken YAML frontmatter block, or a missing `<step>` tag silently degrades behavior rather than throwing an error. There's no type system, no linter, no schema validation at parse time (beyond the gsd-tools.cjs frontmatter parser). The integrity manifest (`gsd-file-manifest.json` with SHA256 hashes) catches file tampering but not semantic errors.

**5. No Architecture Advisor**
GSD has no Oracle equivalent. When the gsd-planner faces an architectural crossroads (microservices vs. monolith? SQL vs. NoSQL?), it must make the call itself with whatever context it has. There's no dedicated high-IQ consultation agent for tradeoff analysis. The gsd-debugger does have scientific method debugging, but architecture decisions during planning have no specialist to consult.

**6. Fragile State Files**
STATE.md, ROADMAP.md, and per-phase files are plain markdown with YAML frontmatter. If a subagent writes malformed YAML, or two parallel executors update STATE.md simultaneously, the state corrupts silently. There's no locking mechanism, no conflict resolution, no transactional state updates. The `gsd-tools.cjs` CLI centralizes some operations, but agents can also write these files directly.

**7. No Parallel Background Research**
GSD's research phase (gsd-phase-researcher) runs as a single sequential agent. It can't fire 5 librarians in parallel to search docs, GitHub examples, and Stack Overflow simultaneously. Each research query runs one at a time in the researcher's 200K context. UltraWork's pattern of firing `explore` + `librarian` agents in background while continuing work is architecturally impossible in GSD's sequential workflow model.

**8. Verification Assumes Good Faith**
The 3-level artifact verification (exists → substantive → wired) is impressive but operates on heuristics. "Substantive" checking looks for patterns like `return null` or empty handlers, but a function that returns a hardcoded value instead of computing the real result passes all three levels. There's no functional testing layer built into verification — the gsd-verifier checks structure, not behavior. The `/gsd:verify-work` UAT is conversational (the human tests), not automated.

**9. Version Drift Risk**
When GSD updates, users run the installer again and files get overwritten. But if you've customized agent prompts (editing `gsd-planner.md` to add domain-specific knowledge), those customizations are lost. There's no merge mechanism — it's a full file replacement. The integrity manifest exists but doesn't support three-way merges between upstream changes and user customizations.

**10. No Multimodal Capability**
GSD has no visual analysis agent. It can't look at screenshots, design mockups, or UI renders. If a task involves "make this match the Figma design," the gsd-executor has no eyes — it can only read code. The gsd-verifier can check if a component renders without errors but can't verify it looks correct.

---

### UltraWork — Where It Falls Short

**1. No Project Memory**
UltraWork has no concept of milestones, phases, or roadmaps. Each session starts effectively fresh. The boulder state tracks the current active plan, but there's no equivalent of GSD's ROADMAP.md tracking which phases are done, which are next, what the overall project goal is. For a 2-week project with 8 phases, UltraWork has no mechanism to track "we finished phases 1-4, phase 5 is in progress, phases 6-8 are planned." You'd have to tell it every session.

**2. Opaque Prompt Engineering**
The system prompts are compiled into a 94,123-line JavaScript bundle. If Sisyphus gives bad advice (e.g., its delegation table misroutes visual tasks), you can't edit the prompt — you must fork the GitHub repo, modify TypeScript source, rebuild, and republish. Meanwhile, a GSD user just opens `gsd-planner.md` and changes a line. This creates a hard dependency on the oh-my-opencode maintainer for any behavioral tuning.

**3. Verification is Shallow**
UltraWork's verification relies on: (a) `lsp_diagnostics` for type errors, and (b) a "manual QA mandate" in the Sisyphus prompt telling the agent to actually run things. But there's no structured verification framework. No 3-level artifact checking, no stub detection patterns, no gap-closure pipeline. The Ralph Loop iterates, but each iteration is the same agent re-checking its own work — there's no independent verifier agent with fresh context and different perspective. It's like having the author proofread their own essay.

**4. Hephaestus is GPT-Gated**
The deep worker agent (Hephaestus) is explicitly GPT-only. The hook `createNoHephaestusNonGptHook` blocks it with the message "Hephaestus is trash without GPT." If you don't have an OpenAI subscription, you lose the autonomous deep execution agent entirely. Sisyphus Junior is the fallback but it's described as "lightweight" — not the same caliber. This creates a pay-wall within an ostensibly multi-provider system.

**5. No Formal Checkpoint Protocol**
GSD has three checkpoint types (`human-verify`, `decision`, `human-action`) with explicit protocols for when to pause and what to ask. UltraWork has no equivalent. The agent decides ad-hoc when to ask the user, based on prompt instructions like "if multiple interpretations, 2x+ effort difference → MUST ask." But there's no structured mechanism to pause execution at a pre-defined point, collect a decision, and resume. For sensitive operations (deploying to production, deleting data), this is a real risk.

**6. No Scientific Debugging**
GSD's `gsd-debugger` follows a formal scientific method: gather symptoms → form hypotheses → test one at a time → maintain persistent debug state across sessions. UltraWork's approach is: Sisyphus tries to fix it, and if it fails 3 times, consults Oracle. Oracle is a read-only consultant that gives advice — it doesn't maintain debug state, doesn't track hypotheses, and doesn't persist across sessions. For complex bugs that span multiple files and sessions, GSD's approach is architecturally superior.

**7. Context Window Blindness**
GSD explicitly budgets context: "each plan should complete within ~50% context" and "quality degrades above 70%." UltraWork has preemptive compaction hooks that try to manage context automatically, but there's no explicit budget per task. A Sisyphus Junior delegated task could consume 90% of its context window before finishing, producing degraded output in the final 10% of work without any mechanism to detect or prevent this.

**8. Skill System is Underdeveloped**
UltraWork's skill system (`load_skills`, `SKILL.md`) is metadata-driven but thin. Skills are primarily instructions injected into prompts — they don't carry executable code, test suites, or validation logic. GSD's equivalent (Claude Code's native skill system) is similarly basic, but GSD compensates with its template/reference/workflow layers. UltraWork's skills are a single markdown file per skill with no composability or dependency management.

**9. Disk and Resource Footprint**
~1 GB total across npm packages (404 MB), cache (318 MB), and config (1.3 MB). That's substantial for what is essentially a prompt orchestration system. GSD's 152 markdown files total ~27,000 lines of text — kilobytes, not gigabytes. The difference is that UltraWork bundles its own copies of ast-grep, MCP SDK, Express, and other dependencies as npm packages. Each project using UltraWork shares the global install, but it's still a heavy footprint.

**10. Single-Maintainer Risk**
UltraWork is developed primarily by one developer (code-yeongyu) under the Sustainable Use License. The compiled, opaque distribution means the community can't easily contribute prompt improvements — they'd need to understand the TypeScript source, the build pipeline, and get changes merged upstream. GSD's MIT-licensed markdown files invite community contribution because anyone can read and edit them. If the UltraWork maintainer stops updating, the compiled bundle becomes a black box that can't evolve.

---

### Shared Weaknesses (Both Frameworks)

| Gap | Details |
|---|---|
| **No cross-framework interop** | Can't use GSD's planning with UltraWork's execution. Each is a complete, self-contained system. |
| **Agent hallucination risk** | Both delegate critical decisions to LLMs with no deterministic fallback. A bad plan from gsd-planner or Prometheus wastes an entire execution cycle. |
| **No cost tracking** | Neither tracks token usage, API costs, or provides cost estimates before execution. A complex plan could burn $50+ in API calls with no warning. |
| **No rollback mechanism** | Both make git commits, but neither has a structured "undo this entire phase/plan" operation. You'd need to manually `git revert` a series of commits. |
| **Testing is optional** | Neither enforces TDD. GSD supports it (TDD plans with `tdd="true"`), UltraWork's prompts mention it, but both allow agents to skip tests entirely if the plan doesn't include them. |

---

## TL;DR

**GSD** is a **project management framework** — it thinks in milestones, phases, and roadmaps. It's transparent (markdown files you can read and edit), has rigorous goal-backward verification, and excels at long-running multi-phase projects. But it's Claude-centric and has no advanced code analysis tools.

**UltraWork** is an **agent orchestration engine** — it thinks in tasks, categories, and model routing. It's powerful (65 hooks, 26 tools, 7 providers, LSP/AST-grep), fast (parallel background agents), and model-diverse. But it's opaque (compiled JS), lacks project-level planning hierarchy, and has less rigorous verification.

**Choose GSD** if you want structured project delivery with human checkpoints and transparent instructions.
**Choose UltraWork** if you want fast, model-diverse task execution with deep code analysis tools.
