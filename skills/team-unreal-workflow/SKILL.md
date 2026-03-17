---
name: team-unreal-workflow
description: Project-specific wrapper skill for UnrealMCPHub-based game development. Use when working on this fork's Unreal workflow and you need team rules, sandbox boundaries, benchmark ladder selection, task templates, review checklists, or controlled next-step planning on top of use-unrealhub.
---

# Team Unreal Workflow

Use this skill as the project-facing layer on top of:
- [use-unrealhub](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\use-unrealhub\SKILL.md)

Do not use this skill to modify Hub internals. For Hub source changes, use:
- [unrealhub-developer](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\unrealhub-developer\SKILL.md)

## Role

This skill is the project-level control layer for this fork.

Its job is to turn generic Hub and UE runtime capabilities into a team-usable workflow with:
- sandbox boundaries
- validation expectations
- benchmark ladder selection
- task and review templates
- controlled next-step planning

It should not become a dump of historical notes or Hub implementation details.

## Default Behavior

1. Treat `use-unrealhub` as the engine-facing runtime layer.
2. Default to sandboxed work unless the task explicitly allows broader scope.
3. Require a small execution plan before edits.
4. Require validation and a change summary after edits.
5. Prefer benchmark ladder progression over jumping directly to the heaviest scenario.

## Load These References As Needed

- For the current playbook reading order, including `Current / Snapshot / Archive`:
  [README.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\README.zh-CN.md)
- For workflow sequence and task loop:
  [workflow.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\team-unreal-workflow\references\workflow.md)
- For safety boundaries:
  [rules.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\team-unreal-workflow\references\rules.md)
- For choosing the right benchmark stage:
  [benchmark-ladder.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\team-unreal-workflow\references\benchmark-ladder.md)
- For phase-based rollout and next-step planning:
  [execution-todo.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\team-unreal-workflow\references\execution-todo.md)
- For low-overhead execution, preflight, branch placement, and runtime validation:
  [implementation-guide.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\team-unreal-workflow\references\implementation-guide.md)
- For standardized benchmark outputs:
  [benchmark-artifact-template.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\team-unreal-workflow\references\benchmark-artifact-template.md)
- For benchmark completion reporting and artifact boundaries:
  [vampire-survivors-benchmark-pass.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\vampire-survivors-benchmark-pass.zh-CN.md)
  [benchmark-artifact-guidelines.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\benchmark-artifact-guidelines.zh-CN.md)
- For capability showcase planning and gym structure:
  [unreal-capability-gym.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\unreal-capability-gym.zh-CN.md)
- For common task prompts and templates:
  [task-templates.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\team-unreal-workflow\references\task-templates.md)
- For final review expectations:
  [review-checklist.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\team-unreal-workflow\references\review-checklist.md)

## Capability Gym Placement

`Capability Gym` currently lives in the playbook docs instead of this skill's references.

That is intentional:
- today it is still a showcase and feasibility framework
- it benefits from flexible iteration by domain and report format
- it is not yet a stable day-to-day execution contract

If gym task templates, readiness scoring, and reporting structure stabilize, the execution-facing subset can later move into this skill as first-class references.

## Operating Modes

- Read-only analysis
- Sandbox prototype
- Restricted feature work
- Benchmark lite
- Full benchmark preparation

## Decision Rule

Use the lightest mode that can complete the task safely:

1. If the task is exploratory, stay read-only.
2. If the task creates new gameplay or UI ideas, use sandbox prototype mode.
3. If the task touches a real module, switch to restricted feature work.
4. If the goal is evaluation, choose a scenario from the benchmark ladder instead of defaulting to the largest benchmark.

## Mandatory End State For Editing Tasks

An editing task is not complete unless it includes:
- what changed
- where it changed
- what validation ran
- what is still risky
- what the next smallest step should be
