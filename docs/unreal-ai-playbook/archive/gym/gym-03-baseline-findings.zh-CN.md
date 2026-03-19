# Gym-03 Baseline Findings

## Purpose

This note records the main conclusions from the first `Gym-03` baseline pass.

It is intended to support later feasibility and usability reporting by separating:
- validated conclusions
- useful engineering fixes
- rejected or misleading intermediate evidence
- the practical boundary that still remains

## Recommended Positioning

`Gym-03` should currently be described as:

- a successful **baseline gameplay-feedback validation**
- not yet a polished interaction showcase

This means:
- the lighter `Actor / Trigger` path is workable
- the `before/after` capture path now reflects real scene changes
- more expressive Blueprint-backed follow-up work is optional rather than blocking

## What Was Validated

The following capability layers were validated:

- controlled scene reset for a local interaction testbed
- fixed capture-camera reuse with non-colliding camera naming
- actor-based feedback mutation through structured tools
- camera-anchored screenshot capture that reflects the actual modified scene
- a minimal `before/after` chain that does not require complex Blueprint graph edits

## Key Successful Capabilities

The following tool groups were practically proven useful during `Gym-03`:

- testbed reset
- static-mesh actor spawning
- capture-camera creation and reuse
- actor transform updates
- actor-based supporting feedback props or lights
- camera-anchored viewport capture

These are enough to support a first gameplay-feedback baseline without immediately escalating to a heavyweight interaction system.

## Main Reading Of The Pass

`Gym-03` demonstrated that a minimal interactive-feeling scene can be built and modified with structured MCP tools.

The key point is not that the scene already behaves like a complete game mechanic.
The key point is that:

- the scene starts from a controlled neutral state
- a small automated sequence makes the result visually read as "feedback happened"
- the captured images now reflect the mutation instead of remaining identical

## Important Engineering Fixes

This pass also produced several constructive tool-chain fixes.

### Fix 1: Camera-anchored capture

`capture_viewport` now supports an optional `camera_name`, which lets the viewport align to a known capture camera before taking the screenshot.

Why this mattered:
- previous Gym evidence could succeed logically but still capture the wrong viewport frame
- camera anchoring made the screenshot path deterministic enough for baseline reporting

### Fix 2: Capture-camera idempotency

`ensure_capture_camera` was adjusted so repeated runs no longer rely on forcing the same actor object name at spawn time.

Why this mattered:
- earlier runs could crash the editor when an allegedly reusable camera name collided at spawn time
- reusing labels and explicit lookup semantics is safer for automation

### Fix 3: Viewport refresh on mutation paths

Viewport refresh was added to key mutation paths such as:
- actor transform updates
- static mesh spawning
- capture-camera setup
- lighting mutations
- screenshot capture preparation

Why this mattered:
- earlier runs could logically modify the scene while screenshots still showed stale viewport frames

## Invalid Or Rejected Intermediate Results

Some earlier `Gym-03` outputs should be treated as invalid.

### Rejected Evidence A: Crashy camera-recreation runs

Any early run that depended on recreating a same-name capture camera and then crashed the editor should be treated as invalid evidence.

Reason:
- the failure was caused by tool-chain instability, not by the intended gameplay-feedback content

### Rejected Evidence B: Any frame captured from an ambiguous or stale viewport

Any image captured before camera anchoring and forced viewport refresh were in place should not be reused as formal Gym evidence.

Reason:
- the screenshot may not correspond to the intended scene state

## Important Boundary Findings

### Boundary 1: Gameplay-feedback baseline does not need Blueprint first

The first useful `Gym-03` pass did not need heavy Blueprint graph edits.

Implication:
- Blueprint remains valuable
- but it is better treated as a follow-up validation path after the lighter Actor / Trigger baseline is stable

### Boundary 2: Evidence correctness depends on viewport correctness

For feedback-oriented Gym work, the screenshot path is part of the core functionality.

Implication:
- "tool returned success" is not enough
- the viewport must be aligned and refreshed before evidence is considered valid

### Boundary 3: Editor instance discipline still matters

As with earlier Gyms, one project should have one active editor instance during baseline validation.

Implication:
- duplicate instances can still make viewport ownership and MCP session state harder to reason about

## Why Gym-03 Counts As Baseline-Ready

The core baseline question for `Gym-03` was:

- can we use structured tools to produce a minimal, visible gameplay-feedback delta and capture it reliably?

The answer is now:

- yes

This does not mean `Gym-03` is finished as a final showcase piece.
It means the baseline infrastructure and evidence path are strong enough to support later Blueprint-backed or richer interaction follow-up work.

## Reporting Guidance

When referenced in later reports, the recommended wording is:

- `Gym-03 baseline gameplay-feedback pass validated`
- `camera-anchored evidence capture validated for interaction-oriented scenes`
- `Actor / Trigger path validated as the first Gym-03 baseline route`
- `Blueprint logic remains a recommended follow-up path rather than a blocking prerequisite`

Avoid wording such as:

- `Gym-03 completed as a final gameplay systems showcase`
- `Gym-03 proves full Blueprint interaction authoring at production quality`

Those statements would overstate what this pass was designed to prove.

## Recommended Follow-Up Use

The practical value of `Gym-03` is that it unlocks:

- Blueprint-backed feedback follow-up work
- richer trigger/interaction scenarios
- more convincing figure-rich feasibility reporting

It should therefore be treated as:

- a validated baseline automation pass
- a reference case for camera-safe evidence capture
- a bridge from readability-only Gym work toward interaction-aware showcase tasks
