# Gym-04 Baseline Findings

## Purpose

This note records the main conclusions from the first `Gym-04` baseline pass.

It is intended to support later feasibility and usability reporting by separating:
- validated conclusions
- newly exposed tool-chain boundaries
- useful encounter-design learnings from the first lightweight pass

## Recommended Positioning

`Gym-04` should currently be described as:

- a successful **baseline combat-encounter readability validation**
- not yet a dynamic combat showcase

This means:
- a static encounter proxy is sufficient for the first baseline
- the current tool chain is already strong enough to assemble and capture a minimal combat-style scene
- richer behavior and gameplay logic remain follow-up work

## What Was Validated

The following capability layers were validated:

- controlled static combat-proxy scene construction
- fixed capture-camera evidence path under repeated runs
- encounter readability improvement through proxy layout changes
- local cover and focal-marker placement as part of the baseline modify
- supporting point-light usage to reinforce combat focal hierarchy

## Key Successful Capabilities

The following tool groups were practically useful during `Gym-04`:

- static mesh spawning
- actor transform updates
- point-light spawning
- fixed camera capture
- baseline lighting preset reuse

These are enough to support a first encounter-readability pass without requiring live AI behavior or damage systems.

## Main Reading Of The Pass

`Gym-04` showed that the next Gym step after readability and feedback can still remain lightweight.

The important point is not that the scene already simulates combat.
The important point is that:

- the `before` scene reads as weak or neutral
- the `after` scene reads more clearly as a combat encounter
- that shift can be produced by structured, repeatable tool calls

## Important Boundary Findings

### Boundary 1: Static encounter baseline is the right first step

The first useful `Gym-04` pass did not need behavior trees, AI movement, or a combat loop.

Implication:
- baseline should focus on encounter readability first
- more dynamic combat logic is better treated as a later follow-up

### Boundary 2: Spawn naming still matters beyond cameras

This pass exposed that `spawn_static_mesh_actor` had the same kind of naming hazard that earlier affected capture cameras.

The validated fix was:
- stop forcing a raw object name at spawn time for static mesh actors
- keep the human-readable label semantics for later lookup

Implication:
- repeated Gym runs need idempotent naming behavior for all high-frequency scene-construction tools, not only for cameras

### Boundary 3: Client/runtime compatibility still affects Gym velocity

This pass again surfaced that:
- temporary PowerShell clients are still workable
- but protocol details such as `Accept` headers and version differences in JSON helpers can slow iteration

Implication:
- a more stable external runner still remains a worthwhile near-term TODO

## Why Gym-04 Counts As Baseline-Ready

The core baseline question for `Gym-04` was:

- can we make a static combat encounter read more clearly through structured automated edits and capture valid evidence of that change?

The answer is now:

- yes

This does not mean `Gym-04` is finished as a full combat benchmark.
It means the baseline path is good enough to support later follow-up work that adds behavior, targeting, or Blueprint-backed logic.

## Reporting Guidance

When referenced in later reports, the recommended wording is:

- `Gym-04 baseline combat-encounter readability pass validated`
- `static encounter proxy path validated as the first Gym-04 route`
- `camera-safe encounter evidence capture validated`
- `dynamic combat behavior remains follow-up work`

Avoid wording such as:

- `Gym-04 completed as a final combat benchmark`
- `Gym-04 proves full AI-driven combat authoring`

Those statements would overclaim what this pass was designed to prove.

## Recommended Follow-Up Use

The practical value of `Gym-04` is that it opens the door to:

- behavior-backed combat follow-up work
- Blueprint-supported encounter glue logic
- more credible combat sections in a future figure-rich feasibility report

It should therefore be treated as:

- a validated baseline automation pass
- a reference case for encounter readability as a first combat step
- a reminder that naming/idempotency rules matter across all repeated scene-construction tools
