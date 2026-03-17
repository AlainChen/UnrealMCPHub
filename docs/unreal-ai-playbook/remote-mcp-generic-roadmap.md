# Remote MCP Refactor Roadmap

This document is a generic knowledge base for refactoring a "Remote MCP" style editor plugin.

It is intentionally written without project-specific assumptions so that another agent or workspace can use it as a starting point.

## Goal

Refactor a plugin that currently depends heavily on remote script execution into an editor-side tooling layer that is:

- structured
- stable
- auditable
- composable
- suitable for long-running agent automation

In short:

Move from "run arbitrary scripts remotely" to "call stable tools with contracts."

## Problem Model

Many Remote MCP systems start with this shape:

- one generic script execution entry point
- long scripts for higher-level tasks
- reflection-based or dynamic property access
- no checkpoint or rollback for multi-step operations
- low-level exceptions instead of structured errors
- weak evidence capture and poor reproducibility

This usually creates six recurring problems:

1. Long scripts are fragile
2. Editor state is hard to reason about
3. Property access is unstable
4. Multi-step tasks are hard to recover
5. Errors are hard to classify
6. Results are hard to archive and audit

## Design Principles

### 1. Tool first, script second

High-frequency actions should become structured tools instead of staying as long scripts.

### 2. Stabilize single steps before multi-step orchestration

Make atomic operations reliable before building workflows on top of them.

### 3. Be editor-safe before agent-friendly

Prevent crashes and invalid editor states first; optimize agent ergonomics second.

### 4. Return structured results

Every tool should return structured data, not only free-form status strings.

### 5. Prefer idempotent tools

Tools that can be safely called multiple times should be prioritized.

## Capability Layers

## Layer 0: Session and Health

This is the foundation.

Suggested tools:

- `ping`
- `get_editor_state`
- `get_project_state`
- `get_current_level`
- `list_open_maps`
- `get_selection`
- `is_busy`
- `begin_session`
- `end_session`

Purpose:

Let the agent know whether the editor is healthy and whether it is safe to continue.

## Layer 1: Map and Scene Lifecycle

This is usually the first layer that should be structured.

Suggested tools:

- `create_blank_map`
- `create_map_from_template`
- `load_map`
- `save_current_map`
- `save_map_as`
- `duplicate_map`
- `delete_map`
- `reset_testbed`

Purpose:

Stop depending on fragile script chains for creating, loading, and saving scenes.

## Layer 2: Object and Actor Construction

This is the second core layer.

Suggested tools:

- `spawn_actor`
- `spawn_static_mesh_actor`
- `destroy_actor`
- `find_actor_by_name`
- `find_actors_by_prefix`
- `set_actor_transform`
- `set_actor_visibility`
- `tag_actor`
- `delete_actors_by_tag`

Purpose:

Turn "scene construction" into structured operations instead of ad hoc scripts.

## Layer 3: Domain Toolkits

High-level domain tools should sit on top of object-level operations.

### Lighting

- `create_basic_lighting_rig`
- `apply_time_of_day_preset`
- `set_directional_light`
- `set_skylight`
- `set_fog`
- `apply_readability_pass`

### Camera and Capture

- `create_camera`
- `set_editor_camera`
- `look_at_target`
- `capture_viewport`
- `capture_before_after`

### Post Process

- `ensure_post_process_volume`
- `set_post_process_overrides`
- `apply_mood_preset`

### UI and Feedback

- `spawn_ui_test_widget`
- `set_hud_text`
- `toggle_debug_overlay`

### Gameplay and Encounter

- `spawn_test_target`
- `spawn_encounter_set`
- `reset_encounter`
- `run_behavior_probe`

Purpose:

Move from object-level automation to domain-level automation.

## Layer 4: Transaction and Recovery

This layer determines whether long-running agent workflows are realistically usable.

Suggested tools:

- `begin_task`
- `record_step`
- `checkpoint`
- `rollback`
- `end_task`
- `export_task_report`

Purpose:

Make multi-step automation traceable, recoverable, and auditable.

## Generic TODO

## P0 Must-Have

### Editor state and session

- [ ] Add editor health check tools
- [ ] Add current map / selection / busy-state tools
- [ ] Standardize tool responses with `ok / data / warnings / error_code`

### Map lifecycle

- [ ] Implement `create_blank_map`
- [ ] Implement `load_map`
- [ ] Implement `save_current_map`
- [ ] Implement `save_map_as`
- [ ] Implement `create_map_from_template`

### Actor and scene construction

- [ ] Implement `spawn_actor`
- [ ] Implement `spawn_static_mesh_actor`
- [ ] Implement `destroy_actor`
- [ ] Implement `find_actors_by_prefix`
- [ ] Implement `reset_testbed`

### Evidence capture

- [ ] Implement `set_editor_camera`
- [ ] Implement `capture_viewport`
- [ ] Implement `capture_before_after`

### Safe property access

- [ ] Add safe setters for frequently touched objects
- [ ] Avoid requiring agents to guess reflection property names
- [ ] Add wrappers or schema access for complex objects

## P1 Should-Have

### Domain toolkits

- [ ] Add lighting preset tools
- [ ] Add post process preset tools
- [ ] Add lightweight UI / HUD debug tools
- [ ] Add basic gameplay test-actor tools

### Error system

- [ ] Define structured error taxonomy
- [ ] Distinguish editor-state, property, map, capture, and asset errors
- [ ] Return remediation hints where possible

### Transaction and recovery

- [ ] Add task session support
- [ ] Add step logs
- [ ] Add checkpoint support
- [ ] Add rollback or reload strategy

## P2 Nice-To-Have

### Advanced presentation

- [ ] Weather presets
- [ ] Atmosphere presets
- [ ] Multi-camera captures
- [ ] Shot-list capture automation

### Productionization

- [ ] Permission modes
- [ ] Operation allowlists
- [ ] Explicit confirmation for risky tools
- [ ] Periodic health and regression checks

## Implementation Path

## Phase 1: Minimum Safe Closed Loop

Target:

- create or load a scene
- build a minimal test setup
- modify a few key properties
- save
- capture evidence

Do not start with:

- large task templates
- advanced weather systems
- heavy UI systems
- complex batch workflows

Success condition:

One minimal automated showcase can be reproduced reliably.

## Phase 2: Domain Encapsulation

Target:

Move common workflows like lighting, capture, and post process from low-level property access to semantic domain tools.

Success condition:

An agent no longer needs to guess low-level property names and call order for common tasks.

## Phase 3: Transactional Stability

Target:

Add task logs, checkpoints, and recovery behavior.

Success condition:

When a workflow fails, it is possible to identify the failed step and recover cleanly.

## Phase 4: Operational Readiness

Target:

Make the plugin suitable for long-term automation rather than one-off demos.

Success condition:

- regression checks exist
- error taxonomy exists
- basic permission model exists
- artifact export is stable

## Tool Contract Recommendation

A tool should ideally return a structure like:

```json
{
  "ok": true,
  "data": {},
  "warnings": [],
  "error_code": null,
  "message": "..."
}
```

For failures:

```json
{
  "ok": false,
  "data": null,
  "warnings": [],
  "error_code": "map_not_found",
  "message": "Target map does not exist."
}
```

Avoid returning only strings like:

- `"success"`
- `"done"`
- `"failed"`

## Recommended Priority Order

If you are implementing this roadmap, keep the order tight:

1. editor state
2. map lifecycle
3. scene construction
4. capture
5. lighting
6. post process
7. transaction and rollback
8. advanced presets
9. permissions and policy

Why:

- The first four layers already support many baseline automation workflows
- The later layers become much easier once the core foundation is stable

## When It Is Worth Starting

It is worth starting this refactor when all of these are true:

- recurring automation failures come from missing structured editor-side tools, not from weak orchestration
- the needed tool gaps are already clear
- one or two baseline tasks are repeatedly blocked by the same missing capabilities
- you are ready to absorb the complexity of plugin-side implementation

## Summary

The right refactor path for a Remote MCP plugin is not:

"expose more remote scripting"

It is:

"build structured editor-side foundations first, then domain toolkits, then recovery and operational layers."
