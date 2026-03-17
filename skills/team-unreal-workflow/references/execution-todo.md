# Execution TODO

Use this file to decide what to build next without over-expanding the workflow.

## Phase 1: Low-Overhead Default

Goal:
- make the default Unreal AI workflow usable on weaker local machines

Tasks:
- define a `low-overhead` operating mode
- default new benchmark runs to `L0` or `L1`
- avoid heavyweight scans, large map traversals, and unnecessary PIE loops
- require a short change summary after every editing task

Done when:
- the default workflow can complete smoke checks and sandbox prototype tasks reliably

Branch:
- `codex/lab`

## Phase 2: Benchmark Preflight

Goal:
- fail fast before expensive benchmark work starts

Tasks:
- add a standard preflight checklist
- verify MCP connectivity before edits
- verify at least one metadata query and one execution query
- record why a run stopped before moving to the next benchmark level

Done when:
- every benchmark run starts with the same lightweight checks

Branch:
- `codex/benchmark`

## Phase 3: Branch Operating Model

Goal:
- keep research, workflow, and upstream-facing fixes separated

Tasks:
- keep upstream-friendly fixes on `codex/pr-*`
- keep local wrappers and experiments on `codex/lab`
- keep project workflow and benchmark structure on `codex/team-workflow`
- move accepted fork baselines into `main`

Done when:
- each change has an obvious landing branch

Branch:
- `codex/team-workflow`

## Phase 4: Runtime Validation Matrix

Goal:
- distinguish between "listed", "callable", and "validated" Unreal tools

Tasks:
- capture domain and tool enumeration results
- test one or more real calls per domain
- mark tools as `validated`, `unvalidated`, or `known-risk`
- track whether failures are connectivity, timeout, or tool-specific

Done when:
- benchmark reports can say what was actually usable, not just what was advertised

Branch:
- `codex/benchmark`

## Promotion Rule

Do not expand the benchmark scope until:
- the current phase has a repeatable path
- failures are categorized
- the next phase has a named owner and output format

## Bottleneck Hypotheses

Use this section as a research backlog, not as confirmed diagnosis.

### Hypothesis 1: Per-call session setup is too expensive

Signals:
- metadata queries succeed but repeated execution calls time out
- each tool call opens a fresh MCP session

Check:
- compare single-call latency vs short batched validation runs

### Hypothesis 2: Unreal-side execution is blocked on the editor thread

Signals:
- tool enumeration works
- calls that touch actors, blueprints, or Slate stall together

Check:
- compare lightweight metadata calls against one minimal execution call after editor idle

### Hypothesis 3: Slate and world queries are too heavy for the local machine

Signals:
- `slate_*` and actor-list calls are much slower than simple metadata reads
- the machine is already under load while UnrealEditor is responsive but busy

Check:
- avoid broad UI tree traversal and full actor scans in low-overhead mode

### Hypothesis 4: Tool health differs by domain, not just by connection

Signals:
- some domains enumerate correctly but sample calls remain unvalidated
- tool naming and actual callable surface drift apart

Check:
- keep a per-domain validation matrix instead of assuming all listed tools are usable

### Hypothesis 5: Benchmark failures are caused by workflow overhead, not only tool failure

Signals:
- runs spend time on repeated discovery, repeated context rebuilding, and oversized summaries

Check:
- reduce preflight to the minimum stable checks
- keep benchmark artifacts short and structured
