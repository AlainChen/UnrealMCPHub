# Unreal AI TODO

## Purpose

This file is the living management reference for this fork.

Use it to track:
- what is already established
- what still needs to be hardened
- what the next practical platform and workflow steps are

## Completed Baseline

- [x] `RemoteMCP` and UnrealMCPHub connectivity validated on the local sandbox project
- [x] workflow, rules, benchmark ladder, artifact boundary, and implementation notes documented
- [x] `benchmark-preflight` implemented
- [x] `benchmark-lite` implemented
- [x] `L0`, `L1`, and `L2` ladder stages exercised in the external Unreal sandbox project
- [x] `vampire-survivors-v1` style benchmark reached a packaged, showcase-ready pass in the external Unreal project
- [x] `RemoteMCP` completed a validated `P0` baseline:
  - map lifecycle
  - scene/testbed construction
  - evidence capture
  - health baseline
  - session-disrupting map semantics
- [x] `RemoteMCP` completed the current `P0.5` baseline:
  - `map_unsaved`
  - `map_not_found`
  - `map_already_exists`
- [x] early capability-validation / Gym exploration produced enough evidence to inform current platform conclusions

## Important Non-Goals For This Phase

The following are intentionally **not** treated as completed in the current phase:

- [ ] seamless map transition inside one uninterrupted MCP session
- [ ] a stable typed external runner replacing the current ad-hoc PowerShell client
- [ ] full `P1` completion for `RemoteMCP`
- [ ] full post-process wrapper support
- [ ] source-built Unreal workflow support
- [ ] a finished long-term industrialized multi-user operating model
- [ ] a fully finalized figure-rich external report package
- [ ] locomotion / animation showcase validation with a proper standard asset or sample project

## Active TODO

### Workflow Hardening

- [ ] define the default safe validation path that prefers cold compile, package checks, and log evidence over long PIE automation chains
- [ ] add a small failure taxonomy for benchmark runs: connectivity, metadata-only, execution timeout, editor unhealthy, package failure
- [ ] formalize the four operating modes: `read-only`, `sandbox-prototype`, `restricted-edit`, `high-trust maintenance`
- [ ] standardize the end-of-task summary format across docs and artifacts
- [ ] improve local tooling ergonomics when Python is not on `PATH`

### Audit And Review

- [ ] add a binary asset audit template for `.uasset` and `.umap` changes
- [ ] add an asset-reference review template so Unreal changes are not reviewed as raw binaries only
- [ ] require agent/client/model identity in every benchmark artifact
- [ ] keep the repo/external-project artifact boundary documented and enforced
- [ ] ensure externally shared docs and reports mask local absolute paths, ports, and machine-specific identifiers

### Regression And Reproducibility

- [ ] turn benchmark-lite into a repeatable regression gate
- [ ] add one packaged-build smoke-check example to the playbook
- [ ] define a lightweight periodic health check for MCP reachability, tool usability, and package viability
- [ ] reduce reliance on ad-hoc PowerShell MCP clients by defining a stable external runner for validation and reporting
- [ ] evaluate a typed outer control layer (`Go` first, `TypeScript` as an alternative) for session handling, reconnect, artifact collection, and reusable workflow runners

### Capability Validation Follow-Up

- [ ] decide whether future showcase / gym work should live in a separate workspace or dedicated repo layer
- [ ] extract only the stable validation patterns from archived exploration into `team-unreal-workflow` references
- [ ] produce a clean no-image and figure-rich external report package based on the already validated baseline work
- [ ] keep benchmark and capability-validation conclusions summarized without restoring the entire Gym process trail into the main reading path
- [ ] run a first official-sample playable-game validation slice using the new `playable-game-validation-plan`
- [ ] start with `Stack O Bot` as the first full playable validation target, then branch to `Lyra` and `GASP`

### RemoteMCP Foundation Follow-Up

- [ ] wire the validated `RemoteMCP` map/session semantics back into Hub-side workflow examples
- [ ] add structured lighting rig and preset tools to the standard workflow examples
- [ ] add safe Post Process Volume wrappers instead of raw Python property guesses
- [ ] continue reducing reliance on long `run_python_script` chains in higher-level validation tasks
- [ ] formalize `RemoteMCP` project-side runtime dependency sync so upstream code sync does not still fail at Unreal Python import time

## Long-Term Direction

- [ ] support source-built Unreal Engine workflows in addition to Launcher-based validation
- [ ] define how Hub should detect and manage multiple engine layouts and project engine forks
- [ ] research crash, symbol, and packaging workflows for source-built engine projects
- [ ] design an intermediate change representation so AI intent can be reviewed before Unreal binary assets are touched
- [ ] explore structured gameplay/map/asset change summaries beyond raw Git diffs
- [ ] evaluate whether a middleware gameplay layer would reduce direct AI pressure on binary assets and low-level C++
- [ ] compare candidate middleware layers such as AngelScript, Lua, project-specific DSLs, or other script-facing runtimes
- [ ] define what industrialized adoption means for a large project: permissions, auditability, reproducibility, rollback, and multi-user operation
- [ ] design a durable external MCP client/runtime boundary so Unreal-internal Python, plugin-bundled dependencies, and outer orchestration can evolve independently
- [ ] define how future agent workflows should consume tool tiering (`risk_tier`, reconnect semantics, validation status) rather than rediscovering tool behavior ad hoc

## Next Review Trigger

Update this file whenever one of these happens:
- a benchmark validation path becomes stable enough to standardize
- a process moves from experimentation into team default practice
- a new platform-level capability becomes stable enough to document in `Current`
