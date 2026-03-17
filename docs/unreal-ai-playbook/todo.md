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

## Active TODO

### Workflow Hardening

- [ ] define the default safe validation path that prefers cold compile, package checks, and log evidence over long PIE automation chains
- [ ] add a small failure taxonomy for benchmark runs: connectivity, metadata-only, execution timeout, editor unhealthy, package failure
- [ ] formalize the four operating modes: `read-only`, `sandbox-prototype`, `restricted-edit`, `high-trust maintenance`
- [ ] standardize the end-of-task summary format across docs and artifacts

### Audit And Review

- [ ] add a binary asset audit template for `.uasset` and `.umap` changes
- [ ] add an asset-reference review template so Unreal changes are not reviewed as raw binaries only
- [ ] require agent/client/model identity in every benchmark artifact
- [ ] keep the repo/external-project artifact boundary documented and enforced

### Regression And Reproducibility

- [ ] turn benchmark-lite into a repeatable regression gate
- [ ] add one packaged-build smoke-check example to the playbook
- [ ] define a lightweight periodic health check for MCP reachability, tool usability, and package viability

### Capability Gym

- [x] lock the first two pilot domains for showcase work
- [x] write task templates for `combat/modify` and `lighting/modify`
- [x] define the evidence bundle for every gym task: before/after image, validation note, risk summary, readiness score
- [x] start the first live gym instance for `combat/modify`
- [ ] produce the first 图文可行性报告 from two successful gym pilots
- [ ] decide when stable gym templates should move from docs into `team-unreal-workflow` references

## Long-Term Direction

- [ ] support source-built Unreal Engine workflows in addition to Launcher-based validation
- [ ] define how Hub should detect and manage multiple engine layouts and project engine forks
- [ ] research crash, symbol, and packaging workflows for source-built engine projects
- [ ] design an intermediate change representation so AI intent can be reviewed before Unreal binary assets are touched
- [ ] explore structured gameplay/map/asset change summaries beyond raw Git diffs
- [ ] evaluate whether a middleware gameplay layer would reduce direct AI pressure on binary assets and low-level C++
- [ ] compare candidate middleware layers such as AngelScript, Lua, project-specific DSLs, or other script-facing runtimes
- [ ] define what industrialized adoption means for a large project: permissions, auditability, reproducibility, rollback, and multi-user operation

## Next Review Trigger

Update this file whenever one of these happens:
- a new gym domain becomes active
- a benchmark validation path becomes stable enough to standardize
- a process moves from experimentation into team default practice
