# GSD vs. UltraWork (oh-my-opencode) — Systematic Comparison

## Philosophy & Identity

| Dimension | GSD (Get Shit Done) | UltraWork (oh-my-opencode) |
|-----------|--------------------|-----------------------------|
| **Core metaphor** | Project manager — structured phases, milestones, roadmaps | Workshop foreman — mythological specialists working in parallel |
| **Design goal** | Replace PM overhead for solo devs while keeping discipline & traceability | Turn Claude Code into a multi-model parallel development team |
| **Work model** | Waterfall-ish cycles: Plan → Execute → Verify per phase | Agent swarm: classify intent → dispatch specialists → iterate until done |
| **Completion strategy** | Goal-backward verification against success criteria | Ralph Loop — self-referential iteration until completion promise detected |
| **Agent naming** | Descriptive (`gsd-planner`, `gsd-verifier`) | Mythological (`Sisyphus`, `Prometheus`, `Hephaestus`, `Oracle`, `Momus`, `Metis`) |

---

## Architecture

| Aspect | GSD | UltraWork |
|--------|-----|-----------|
| **Agents** | 12 specialized (planner, executor, verifier, researcher, etc.) | 8+ specialists (orchestrator, craftsman, planner, reviewer, debugger, librarian, etc.) |
| **State files** | `PROJECT.md`, `STATE.md`, `ROADMAP.md` + per-phase `PLAN.md`, `SUMMARY.md`, `VERIFICATION.md` | `.sisyphus/boulder.json` (active work), `.sisyphus/plans/*.md`, `ralph-loop.local.md` |
| **Config** | `.planning/config.json` + `.claude/settings.json` | `.opencode/oh-my-opencode.jsonc` (Zod-validated schema) |
| **Commands** | 40+ slash commands (`/gsd:*` namespace) | ~10 commands (`/start-work`, `/ralph-loop`, `/ulw-loop`, `/init-deep`, `/refactor`, etc.) |
| **Compiled core** | `gsd-tools.cjs` (CLI tool for state/phase ops) | `index.js` (3.4MB compiled plugin) |
| **Extension model** | Agent definitions as markdown files | Plugin interface with hooks, MCPs, tools, skills |

---

## Planning

| Aspect | GSD | UltraWork |
|--------|-----|-----------|
| **Pre-planning** | Optional research phase (`gsd-phase-researcher`) produces `RESEARCH.md` | **Metis** pre-consultant classifies intent, flags AI-slop risks, generates clarifying questions |
| **Plan creation** | `gsd-planner` creates `PLAN.md` with tasks, waves, dependencies | **Prometheus** runs 4-phase workflow: intent classification → analysis → questions → plan generation |
| **Plan validation** | `gsd-plan-checker` verifies plan achieves goal before execution | **Momus** reviewer — pragmatic bias (approve by default), max 3 blocking issues, iterates until "OKAY" |
| **Plan structure** | Frontmatter (phase, wave, depends_on) + 2-3 tasks per plan | Markdown with checkboxes, file references, QA scenarios with tool+steps+assertions |
| **Granularity** | Milestone → Phase → Plan → Task (4 levels) | Plan → Task (2 levels, flatter) |
| **Requirements tracing** | Explicit requirement IDs mapped to phases, traceability matrix | Intent-based — no formal requirement IDs |

---

## Execution

| Aspect | GSD | UltraWork |
|--------|-----|-----------|
| **Parallelism** | Wave-based: group independent plans into waves, execute in parallel | Agent swarm: 5+ specialist agents dispatched simultaneously from Phase 1 |
| **Atomic commits** | Per-task git commits during execution | Supported via `git-master` skill |
| **Deviation handling** | 4 explicit rules: auto-fix bugs (R1), critical missing (R2), blockers (R3), escalate architecture (R4) | Agent autonomy — Sisyphus delegates, Hephaestus works independently |
| **Checkpoints** | 3 types: human-verify (90%), decision (9%), human-action (1%) | Completion promise detection in Ralph Loop |
| **Continuation** | `<completed_tasks>` with commit hashes for context-reset survival | Session ID chaining in boulder state; ralph-loop iteration tracking |
| **Branching** | Configurable: none / phase / milestone branch strategies | Git worktree per work session |
| **Auto-mode** | Auto-approve checkpoints (except human-action) | Ralph Loop runs until `<promise>VERIFIED</promise>` |

---

## Verification & Quality

| Aspect | GSD | UltraWork |
|--------|-----|-----------|
| **Post-execution verification** | `gsd-verifier` — 3-level check: exists → substantive → wired | **Oracle** reviews whether work is truly done; emits `<promise>VERIFIED</promise>` |
| **Stub detection** | Explicit patterns (empty returns, TODO/FIXME, unhandled fetch, placeholder JSX) | Comment checker (`@code-yeongyu/comment-checker`) flags AI slop |
| **Test generation** | `gsd-nyquist-auditor` generates behavioral tests for requirement gaps | QA scenarios embedded in plans (tool + steps + expected result) |
| **Integration testing** | `gsd-integration-checker` verifies cross-phase wiring (exports→imports, API→DB) | Not a separate concern — handled within execution |
| **Gap closure** | Verification gaps feed back into planning cycle | Loop continues until Oracle verification passes |
| **Milestone auditing** | `/gsd:audit-milestone` before archiving | No formal milestone concept |

---

## Model Strategy

| Aspect | GSD | UltraWork |
|--------|-----|-----------|
| **Profiles** | 3 profiles: quality (Opus-heavy), balanced (mixed), budget (Sonnet/Haiku) | Per-category model assignment with fallback chains |
| **Model diversity** | Claude-only (Opus, Sonnet, Haiku) | Multi-provider: Claude, GPT-5.3/5.4-codex, Kimi K2.5, GLM-5 |
| **Override granularity** | Per-agent model overrides | Per-agent AND per-category overrides with temperature, thinking, reasoning_effort |
| **Fallback** | Not built-in | Automatic fallback chains per agent |

---

## Unique Strengths

### GSD excels at:
- **Traceability** — requirement IDs → phases → plans → tasks → commits → verification. Full audit trail.
- **Goal-backward thinking** — everything derives from "what must be TRUE?", not "what tasks to do"
- **Structured state management** — `STATE.md` provides session-to-session continuity with metrics, velocity tracking
- **Milestone lifecycle** — plan → execute → verify → audit → archive → next milestone
- **Predictability** — rigid workflow with well-defined quality gates at every stage

### UltraWork excels at:
- **Multi-model orchestration** — delegates to the best model per task category (code gen → GPT-5.3-codex, architecture → Opus, research → Librarian)
- **Agent parallelism** — 5+ specialists dispatched simultaneously from the start
- **Intent intelligence** — Metis pre-analysis prevents misclassified work before tokens are spent
- **Tooling depth** — LSP integration, AST-grep, hash-anchored edits for IDE-level precision
- **Autonomous persistence** — Ralph Loop iterates up to 100 times without human intervention
- **Flexibility** — flatter structure adapts to varied task types without ceremony

---

## Key Trade-offs

| You want... | Choose |
|-------------|--------|
| Full audit trail & requirement traceability | GSD |
| Maximum autonomous velocity | UltraWork |
| Structured milestones with formal verification | GSD |
| Multi-model cost optimization across providers | UltraWork |
| Predictable, repeatable workflows | GSD |
| Minimal ceremony for varied task types | UltraWork |
| Cross-phase integration checking | GSD |
| IDE-level code intelligence (LSP, AST) | UltraWork |
| Session continuity with metrics & velocity | GSD |
| Self-healing execution loops | UltraWork |

---

## Bottom Line

**GSD** is a *project management framework* — it imposes structure (milestones, phases, requirements, verification) and rewards disciplined execution. It's strongest when you have well-defined goals and want provable completeness.

**UltraWork** is an *agent orchestration harness* — it imposes less structure but provides more raw power through multi-model delegation, parallel specialists, and relentless iteration. It's strongest when you want to throw a task at it and walk away.

They're complementary philosophies: GSD asks "did we build the right thing?" while UltraWork asks "is the thing built yet?"

---

## Gaps & Weaknesses

### GSD — Where It Falls Short

#### 1. Ceremony overhead for small tasks
GSD's 4-level hierarchy (Milestone → Phase → Plan → Task) plus mandatory state documents (`PROJECT.md`, `STATE.md`, `ROADMAP.md`, `REQUIREMENTS.md`) means even a 30-minute bug fix passes through planning, execution, and verification stages. The `/gsd:quick` command exists as an escape hatch, but it's an admission that the core workflow is too heavy for routine work. There's no smooth continuum — you're either in full GSD mode or bypassing it.

#### 2. Single-provider model lock-in
GSD only supports Claude models (Opus, Sonnet, Haiku). As model capabilities diverge across providers — with some excelling at code generation, others at reasoning — this limits the framework's ability to assign the best tool for each job. A coding task that GPT-5.3-codex handles in one shot may cost more Opus tokens and produce worse results.

#### 3. No model fallback or resilience
If a model call fails (rate limit, outage, quota), GSD has no built-in fallback chain. The executor simply fails. UltraWork's automatic fallback chains (e.g., Opus → Sonnet → Haiku, or cross-provider) make it more resilient in production use.

#### 4. Verification is pattern-matching, not behavioral
The 3-level verification (exists → substantive → wired) relies heavily on static analysis: grepping for TODO/FIXME, checking imports exist, verifying fetch calls aren't orphaned. It doesn't actually *run* the code to confirm behavior. The Nyquist auditor generates tests, but only for gap-filling — it's not the primary verification path. This means a component could pass all three levels while being functionally broken at runtime.

#### 5. State document bloat over long projects
Each phase generates `PLAN.md`, `SUMMARY.md`, `VERIFICATION.md`, and potentially `RESEARCH.md` and `CONTEXT.md`. A 10-phase milestone produces 30-50 planning documents. While archiving exists (`/gsd:cleanup`), the cognitive overhead of navigating `.planning/phases/` grows with project size. There's no automatic summarization or compression of historical phases.

#### 6. Rigid sequential phase ordering
Phases execute in numeric order with explicit dependencies. This works well for greenfield builds but poorly for maintenance work where multiple independent concerns (a bug, a feature request, a refactor) arrive simultaneously. Decimal insertion (`2.1`, `2.2`) is a workaround, not a solution — it still forces linear ordering on inherently parallel work.

#### 7. No IDE or language-server integration
GSD operates purely at the file/text level. It has no awareness of AST structure, type systems, or symbol references. Renaming a function means grepping for string matches, not leveraging the language server's rename capability. This increases the risk of incomplete refactors and makes the framework less precise than it could be.

#### 8. Limited adaptability to task type
The workflow is the same whether you're building a React frontend, writing a CLI tool, or configuring infrastructure. There's no task-type-aware behavior — no special handling for visual work (screenshots, design tokens), data pipelines (schema validation, migration safety), or DevOps (deployment verification). The one-size-fits-all approach means the framework is always either too much or not enough for specific domains.

#### 9. Weak handling of context window pressure
GSD tracks context usage via a monitor hook, but has no mechanism to proactively shed context, prioritize what stays in window, or split work when approaching limits. The 2-3 task limit per plan is a static hedge, not a dynamic response. Long execution phases can still exhaust context, with the only recovery being a full context reset and continuation via commit hashes.

#### 10. No external knowledge integration
GSD's research agents search the codebase and can do web searches, but there's no structured integration with documentation servers (like Context7), package registries, or API references. Research quality depends entirely on what the model already knows or can find via general web search.

---

### UltraWork — Where It Falls Short

#### 1. Opaque decision-making
Sisyphus delegates to specialists based on intent classification and category mapping, but the reasoning behind delegation choices is largely invisible. When the wrong agent gets a task or the wrong model is selected, diagnosing *why* requires reading through compiled `.d.ts` stubs and understanding implicit category→model mappings. There's no decision log equivalent to GSD's `STATE.md` trail.

#### 2. No requirements traceability
UltraWork has no concept of requirement IDs, traceability matrices, or formal success criteria derivation. Work is driven by intent classification, not requirement decomposition. This means you can't answer "which requirement does this code satisfy?" or "are all requirements covered?" — questions that matter for any project with external stakeholders or compliance needs.

#### 3. Uncontrolled token burn from agent swarm
Dispatching 5+ parallel agents from Phase 1 is powerful but expensive. Each agent consumes its own context window. If Metis misclassifies intent or Prometheus generates a plan that Momus rejects repeatedly, the token cost compounds without visible progress. There's no budget-aware throttling — the system spends aggressively by design.

#### 4. Ralph Loop can spin without converging
The self-referential loop (up to 100 iterations) assumes that repeated attempts will eventually solve the problem. For genuinely hard issues — architectural mismatches, missing dependencies, ambiguous requirements — iteration produces diminishing returns. The loop can burn significant tokens re-attempting approaches that won't work, with the only escape being the iteration cap or manual `/cancel-ralph`.

#### 5. Weak cross-session continuity
Boulder state tracks the active plan and session IDs, but there's no equivalent to GSD's `STATE.md` with velocity metrics, recent decisions digest, or blockers list. When resuming after a break, UltraWork relies on the boulder JSON and plan checkboxes — much thinner context than GSD provides. Knowledge accumulated during a session (discoveries, rejected approaches, partial insights) is lost on context reset.

#### 6. No milestone or long-term project structure
UltraWork operates at the task/plan level. There's no concept of milestones, multi-phase projects, or long-term roadmaps. This is fine for isolated tasks but becomes a liability for sustained multi-week projects where you need to track progress across many related work items, ensure cross-cutting concerns are addressed, and verify end-to-end integration.

#### 7. Multi-provider model dependency is a fragility risk
Relying on Claude, GPT-5.3-codex, Kimi K2.5, and GLM-5 means the system depends on multiple API providers, billing accounts, rate limits, and capability profiles. Provider outages, API changes, or model deprecations can break specific agent roles. The fallback chains mitigate this but add complexity — and the system needs to be reconfigured whenever a provider changes their model lineup.

#### 8. Compiled/opaque codebase
The 3.4MB compiled `index.js` and `.d.ts` type stubs make it difficult to understand, debug, or extend the system. GSD's markdown-based agent definitions are readable and modifiable by users. UltraWork's internals require reverse-engineering compiled output. This limits community contributions and makes troubleshooting harder when agents misbehave.

#### 9. Verification is subjective, not systematic
Oracle's verification emits `<promise>VERIFIED</promise>` based on the model's judgment that work is complete. There's no structured checklist, no static analysis of stub patterns, no integration wiring check. The quality of verification depends entirely on the Oracle model's ability to assess completeness — which varies by task complexity and model capability. A confident but wrong Oracle can mark broken work as verified.

#### 10. Comment checker is narrow quality assurance
The `@code-yeongyu/comment-checker` catches AI-generated comment slop, but that's a narrow slice of code quality. There's no equivalent to GSD's stub detection patterns (empty returns, orphaned fetches, placeholder components), no integration checker for cross-module wiring, and no test generation for coverage gaps. Quality assurance beyond "comments aren't AI slop" is left to the Oracle's subjective review.

#### 11. Steep configuration complexity
The Zod-validated config schema supports per-agent model overrides, per-category settings, disabled hooks/tools/skills/commands, experimental flags, Ralph Loop tuning, and thinking/reasoning parameters. This flexibility comes at the cost of a learning curve — misconfigured category mappings or agent overrides can silently degrade performance, and the interaction between settings isn't always predictable.

---

### Shared Weaknesses (Both Frameworks)

#### 1. Context window as fundamental bottleneck
Both frameworks ultimately run inside LLM context windows. GSD hedges with small plans (2-3 tasks) and continuation protocols. UltraWork hedges with parallel agents (each gets its own window). Neither truly solves the problem — complex tasks that require deep understanding of large codebases still hit walls. Both rely on the human to chunk work appropriately.

#### 2. No real-time collaboration or multi-human support
Both are designed for solo developer + AI workflows. Neither supports multiple developers working through the same framework simultaneously, shared state locking, or conflict resolution between parallel human+AI work streams.

#### 3. Git as the only persistence layer
Both assume git-based projects. Non-git workflows (monorepo tools like Bazel/Buck, design assets, infrastructure-as-code with state files) get second-class treatment. The atomic commit model central to both frameworks doesn't map cleanly to all development contexts.

#### 4. No cost visibility or optimization
Neither framework provides real-time token usage tracking, cost estimates per phase/plan, or budget controls. Users discover costs after the fact. For teams with API budgets, this lack of visibility is a significant operational gap.

#### 5. Dependent on model quality for meta-decisions
Both frameworks use LLMs to make meta-decisions (what to plan, how to verify, when work is done). These meta-decisions are only as good as the model making them. A model that confidently produces plausible but wrong plans, or that marks incomplete work as verified, undermines the entire framework — and neither system has a non-LLM fallback for these critical judgments.
