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
