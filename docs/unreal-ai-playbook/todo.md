# Unreal AI TODO

## Purpose

This file is the living management reference for this fork.

Use it to track:
- what is already established
- what still needs to be hardened
- what the next concrete gym and productionization steps are

## Completed Baseline

- [x] `RemoteMCP` and UnrealMCPHub connectivity validated on the local sandbox project
- [x] default sandbox root and `AI_TestMap` established
- [x] `team-unreal-workflow` created as the project-level wrapper skill
- [x] workflow, rules, benchmark ladder, artifact template, and implementation notes documented
- [x] `benchmark-preflight` implemented
- [x] `benchmark-lite` implemented
- [x] `L0`, `L1`, and `L2` ladder stages exercised in the external Unreal sandbox project
- [x] `vampire-survivors-v1` style benchmark reached a packaged, showcase-ready pass in the external Unreal project
- [x] `Baseline Track` defined as the current Gym progression path

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
- [ ] reduce reliance on ad-hoc PowerShell MCP clients by defining a stable external runner for gym and benchmark validation
- [ ] evaluate a typed outer control layer (`Go` first, `TypeScript` as an alternative) for session handling, reconnect, artifact collection, and reusable workflow runners

### Capability Gym

- [x] lock the first two pilot domains for showcase work
- [x] rewrite the first two pilot domains around 3D-readable showcase tasks instead of combat-first tasks
- [x] write task templates for `lighting/readability` and `space/readability`
- [x] define the evidence bundle for every gym task: before/after image, validation note, risk summary, readiness score
- [x] clarify that `Gym-01` is a baseline, fully automated pass rather than an advanced lighting showcase
- [x] summarize the first Gym tooling backlog and MCP review findings
- [x] document `Gym-01` as a full baseline brief with evidence and boundary sections
- [x] validate a `RemoteMCP` P0 baseline for map lifecycle, scene/testbed construction, evidence capture, and health/reconnect semantics
- [x] validate a `RemoteMCP` P0.5 baseline for `map_unsaved`, `map_not_found`, and `map_already_exists`
- [x] complete the baseline infrastructure pass for `Gym-01` `Lighting Readability Modify`
- [x] record `Gym-01` baseline findings so later usability reporting can distinguish validated conclusions from rejected evidence
- [ ] optionally improve `Gym-01` into a stronger showcase-quality before/after pair
- [x] define a baseline brief for `Gym-02` `3D Space Readability Modify`
- [x] start `Gym-02` `3D Space Readability Modify`
- [x] complete a baseline automated `Gym-02` pass with valid `before/after` evidence on a controlled scene
- [x] record `Gym-02` baseline findings so later reporting can distinguish validated conclusions from rejected intermediate evidence
- [x] define a baseline brief for `Gym-03` `3D Gameplay Feedback`
- [x] start `Gym-03` `3D Gameplay Feedback`
- [x] run the first `Gym-03` baseline via the lighter `Actor / Trigger` path before escalating to Blueprint graph edits
- [x] record `Gym-03` baseline findings so later reporting can distinguish validated conclusions from rejected intermediate evidence
- [x] define a baseline brief for `Gym-04` `3D Combat Encounter`
- [x] start `Gym-04` `3D Combat Encounter`
- [x] complete a first baseline automated `Gym-04` pass with valid `before/after` evidence on a controlled scene
- [x] record `Gym-04` baseline findings so later reporting can distinguish validated conclusions from rejected intermediate evidence
- [ ] define a baseline brief for `Gym-05` `3D Animation / Locomotion`
- [x] make `Blueprint Logic Modify` a recommended validation path inside `Gym-03` `3D Gameplay Feedback`
- [ ] decide whether to keep Gym on temporary benchmark maps or split a dedicated `__Gym` asset root
- [ ] produce the first figure-rich feasibility report from two successful gym pilots
- [ ] decide when stable gym templates should move from docs into `team-unreal-workflow` references

### Gym Tooling Backlog

- [x] define the Hub-side P0/P1/P2 tooling gap priorities for Gym
- [x] P0: add stable map lifecycle tools for blank-map creation, loading, and save-as
- [x] P0: add minimal scene/testbed construction tools for Gym maps
- [ ] P0: wire the validated `RemoteMCP` map/session semantics back into Hub-side gym workflows and examples
- [ ] P0: add structured lighting rig and preset tools
- [x] P0: add stable evidence capture helpers for before/after screenshots
- [ ] P1: add safe Post Process Volume wrappers instead of raw Python property guesses
- [ ] P1: reduce reliance on long `run_python_script` chains for Gym scenarios
- [x] document the Hub-only foundation plan before deciding whether to fork `RemoteMCP`

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
- a new gym domain becomes active
- a benchmark validation path becomes stable enough to standardize
- a process moves from experimentation into team default practice
