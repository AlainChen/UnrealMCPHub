# Gym-02 Baseline Findings

## Purpose

This note records the main conclusions from the first `Gym-02` baseline pass.

It is intended to support later feasibility and usability reporting by separating:
- validated conclusions
- failed or misleading intermediate results
- the practical automation boundary discovered during the pass

## Recommended Positioning

`Gym-02` should currently be described as:

- a successful **baseline space-readability validation**
- not yet a polished level-design showcase

This means:
- the automated space-readability pipeline is working
- the resulting before/after pair is valid enough for baseline reporting
- further polish is optional rather than blocking

## What Was Validated

The following capability layers were validated:

- controlled scene reset and reconstruction
- fixed capture camera reuse
- stable neutral lighting preset as a baseline visual condition
- actor transform changes as the main mechanism for local space-readability edits
- automated `before/after` evidence capture that reflects actual scene changes

## Key Successful Capabilities

The following tool groups were practically proven useful during `Gym-02`:

- testbed reset
- static-mesh actor spawning
- capture camera creation / reuse
- actor transform updates
- camera-anchored viewport capture

These are enough to support a minimal `space/readability` baseline without requiring a large authored level or a heavyweight sample project.

## Main Reading Of The Pass

`Gym-02` demonstrated that a local 3D scene can be reorganized in a way that is visible in captured evidence.

The important point is not that the final scene is artistically impressive, but that:

- the scene starts from a controlled, intentionally weak composition
- a small sequence of automated spatial edits improves focal hierarchy and local readability
- the captured images now reflect the scene modifications rather than remaining visually identical

## Invalid Or Rejected Intermediate Results

Some earlier `Gym-02` outputs should be treated as invalid.

### Rejected Evidence A: Identical before/after captures

Earlier pairs where `before` and `after` had different tool logs but identical image hashes should be discarded.

Reason:
- the scene update path was not yet forcing a reliable viewport refresh

### Rejected Evidence B: Empty or misleading before frame

Earlier attempts where the scene modifications were known to exist, but the `before` or `after` frame still failed to show the expected anchors, should also be treated as invalid.

Reason:
- the capture path had not yet been fully synchronized with scene updates

## Important Boundary Findings

`Gym-02` exposed several practical boundaries that matter for later Gym work.

### Boundary 1: Viewport refresh must be part of the tool path

It is not enough for scene tools to succeed logically.

If the level viewport is not explicitly refreshed after scene mutations, the screenshot path may capture stale frames.

Implication:
- viewport refresh is part of the evidence pipeline, not just UI polish

### Boundary 2: Capture-camera idempotency matters

`ensure_capture_camera` must behave safely under repeated runs.

During this pass, a non-idempotent camera creation path caused an editor crash when a supposedly reusable camera was recreated after reset.

Implication:
- naming and actor reuse semantics are critical for automated Gym tasks

### Boundary 3: Baseline validation does not require a hero environment

`Gym-02` proved that a baseline pass does not need a full authored level.

A controlled, minimal scene is enough if:
- geometry anchors are clear
- the camera is fixed
- the spatial change is intentional

## Why Gym-02 Counts As Baseline-Ready

The core baseline question for `Gym-02` was:

- can we use structured automation to make a small, readable spatial improvement and capture valid evidence of it?

The answer is now:

- yes

This does not mean `Gym-02` is finished as a final showcase piece.
It means the baseline infrastructure and evidence path are strong enough to support later Gym reporting and follow-up domains.

## Reporting Guidance

When referenced in later reports, the recommended wording is:

- `Gym-02 baseline space-readability pass validated`
- `controlled-scene spatial modify path validated`
- `camera-anchored before/after evidence validated`
- `showcase polish remains optional follow-up work`

Avoid stronger wording such as:

- `Gym-02 completed as a final level-design showcase`
- `Gym-02 demonstrates production-quality encounter layout work`

That would overstate what this pass was designed to prove.

## Recommended Follow-Up Use

The main value of `Gym-02` is that it unlocks the next layer of Gym work:

- `Gym-03 3D Gameplay Feedback`
- later blueprint-supported interaction validation
- more convincing figure-rich baseline reporting

It should therefore be treated as:

- a validated baseline automation pass
- a reference for scene-mutation evidence rules
- a bridge from purely visual readability into interaction-oriented Gym tasks
