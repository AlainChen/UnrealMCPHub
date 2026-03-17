# Unreal AI TODO

## Goal

Establish a project-specific Unreal AI workflow on top of:
- [use-unrealhub](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\use-unrealhub\SKILL.md)

This TODO intentionally starts with workflow and safety, then moves toward stronger autonomy and benchmark usage.

## P0 Environment And Connectivity

- [ ] Confirm the preferred client can connect to `RemoteMCP` directly.
- [ ] Confirm the preferred client can connect through UnrealMCPHub.
- [ ] Verify `ue_status` and `get_unreal_state` in the test project.
- [ ] Verify one simple `ue_run_python` call end to end.
- [ ] Record the team's canonical MCP client configuration.

## P1 Sandbox Setup

- [ ] Create `/Game/__Sandbox/` as the default AI content root.
- [ ] Create `/Game/__Sandbox/Maps/AI_TestMap`.
- [ ] Decide whether any additional restricted prototype roots are allowed.
- [ ] Document the default allowed and forbidden paths in project docs.

## P2 Safety And Review

- [ ] Adopt [rules.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\rules.md) as the default policy.
- [ ] Define who acts as technical owner for AI tasks.
- [ ] Define which task types require explicit human approval.
- [ ] Define the minimum change summary format for every AI task.
- [ ] Define the minimum validation checklist for assets, maps, and code changes.

## P3 Minimal Capability Verification

- [ ] Ask AI to read current Unreal project state and summarize it.
- [ ] Ask AI to create one sandbox blueprint actor.
- [ ] Ask AI to place one object in the sandbox test map.
- [ ] Ask AI to run PIE and report success or failure.
- [ ] Ask AI to create one minimal prototype widget without touching production UI.

## P4 Task Templates

- [ ] Create a template for "sandbox actor prototype".
- [ ] Create a template for "prototype widget".
- [ ] Create a template for "read-only project analysis".
- [ ] Create a template for "restricted feature task".
- [ ] Create a template for "failure report and retry plan".

## P5 Team Wrapper Skill

- [ ] Decide whether to keep the team layer as docs or turn it into a real skill.
- [ ] If creating a skill, name it something like `team-unreal-workflow`.
- [ ] Put workflow, safety rules, and templates into references under that skill.
- [ ] Validate that the team skill narrows `use-unrealhub` instead of duplicating it.

## P6 Benchmark Preparation

- [ ] Finish the first three minimal capability tasks without leaving sandbox scope.
- [ ] Define a lightweight internal benchmark before using the full framework.
- [ ] Choose one scenario from [ue-benchmark](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\ue-benchmark\SKILL.md).
- [ ] Decide what counts as a successful dry run before formal scoring.
- [ ] Record token and task logs consistently.

## P7 Longer-Term Engineering

- [ ] Decide whether the team needs Hub source changes.
- [ ] If yes, use [unrealhub-developer](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\unrealhub-developer\SKILL.md) for those changes.
- [ ] Identify missing UE-side tools that would reduce unsafe Python fallbacks.
- [ ] Identify missing audit or reporting hooks for binary asset work.
- [ ] Revisit workflow rules after the first benchmark cycle.

## P8 Productionization Backlog

- [ ] Define a "safe validation path" that prefers cold compile, package verification, and log evidence over long PIE automation scripts.
- [ ] Add explicit failure categories for benchmark and validation runs, such as connectivity, metadata-only, execution timeout, editor unhealthy, and package failure.
- [ ] Formalize working modes as `read-only`, `sandbox-prototype`, `restricted-edit`, and `high-trust maintenance`.
- [ ] Define a standard end-of-task summary that always records assets changed, validation run, remaining risks, and next smallest step.
- [ ] Add a binary asset audit template for `.uasset` and `.umap` changes.
- [ ] Add an asset-reference change review template so Unreal changes are not reviewed as raw binaries only.
- [ ] Record agent/client/model identity in every benchmark artifact to avoid mixing results across different runtimes.
- [ ] Define which benchmark artifacts are allowed in this repo and which must remain in an external Unreal test project.
- [ ] Turn benchmark-lite into a repeatable regression gate for future workflow changes.
- [ ] Plan a lightweight health check or scheduled validation pass for MCP connectivity, tool usability, and package viability.

## P9 Long-Term Platform Direction

- [ ] Plan support for source-built Unreal Engine workflows in addition to Launcher-based validation.
- [ ] Define how the Hub should detect and manage multiple engine layouts, including project engine forks and team-specific engine roots.
- [ ] Research crash, symbol, and packaging workflows for source-built engine projects.
- [ ] Design an intermediate change representation for AI work, so intent and review data can exist before Unreal binary assets are touched.
- [ ] Explore map, asset, and gameplay change summaries that are more structured than raw Git diffs.
- [ ] Evaluate whether a middleware gameplay layer would reduce direct AI pressure on binary assets and low-level C++.
- [ ] Compare candidate middleware layers such as AngelScript, Lua, project-specific DSLs, or other script-facing gameplay runtimes.
- [ ] Define what "industrialized adoption" means for this workflow in a large project: permissions, auditability, reproducibility, rollback, and multi-user operation.

## Immediate Next Actions

- [ ] Review [skill-system.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\skill-system.md) with the team.
- [ ] Confirm the sandbox root and test map naming.
- [ ] Run one read-only task and one sandbox write task using the new workflow.
- [ ] Capture the first change summary as the baseline template.
