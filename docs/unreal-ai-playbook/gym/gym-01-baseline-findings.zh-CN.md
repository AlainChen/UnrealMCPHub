# Gym-01 Baseline Findings

## Purpose

This note records the main conclusions from the first `Gym-01` baseline pass.

It is intended to support later usability and feasibility reporting, so it focuses on:
- what was actually validated
- which evidence should be treated as invalid
- where the practical automation boundary was found
- how `Gym-01` should be described in follow-up reports

## Recommended Positioning

`Gym-01` should currently be described as:

- a successful **baseline infrastructure validation**
- not yet a final **hero showcase lighting comparison**

In other words:
- the automation path is good enough to support later Gym work
- the final visual storytelling quality of the before/after pair can still be improved

## What Was Validated

The following points are considered validated:

- `RemoteMCP P1 lighting foundation` is sufficient for a baseline lighting workflow
- a controlled Gym map can be used instead of a noisy benchmark map
- camera-anchored capture is the correct evidence path for Gym screenshots
- a fully automated baseline pass can be assembled from structured tools rather than long `run_python_script` chains

More concretely, `Gym-01` validated these capability layers:

- lighting tool capability
- controlled scene construction
- fixed-camera evidence capture
- baseline-ready automation flow

## Key Successful Capabilities

The following capability groups were proven useful during `Gym-01`:

- map lifecycle and map/session semantics from `RemoteMCP P0/P0.5`
- minimal scene/testbed construction
- capture camera creation and camera-anchored screenshots
- first-pass lighting rig and preset application

These capabilities are enough to support later baseline Gym items even if `Gym-01` itself is not yet an ideal portfolio-style visual comparison.

## Invalid Or Rejected Evidence

Some early evidence from `Gym-01` should be treated as invalid and should not be reused in later reporting.

### Rejected Evidence A: Early viewport screenshots

Earlier screenshots that showed a black editor grid or an obviously incorrect view should be treated as invalid.

Reason:
- the capture path was not yet reliably anchored to the intended camera or level viewport

### Rejected Evidence B: Identical before/after images

Earlier `before/after` pairs that turned out to be byte-identical should also be treated as invalid.

Reason:
- the tool calls executed, but the captured viewport frame did not reflect the intended scene or lighting update
- in some cases the scene was not sufficiently controlled
- in some cases multiple lights or an unintended viewport state interfered with the result

### Rejected Evidence C: Uncontrolled default scene results

Any result taken from a map with competing default lights, unclear scene ownership, or duplicate editor instances should not be used as formal Gym evidence.

Reason:
- the visual output cannot be confidently attributed to the Gym tool chain

## Important Boundary Findings

`Gym-01` also exposed several important operational boundaries.

### Boundary 1: Map transition is not seamless

Map-changing operations should currently be treated as `session-disrupting`, not seamless.

Implication:
- follow-up calls may require reconnect logic
- this is a lifecycle issue, not just a screenshot issue

### Boundary 2: One project should have one active editor instance during validation

Multiple editor instances against the same project are unsafe for Gym validation.

Implication:
- evidence becomes ambiguous
- viewport selection and MCP session state become harder to reason about
- ports and active viewport assumptions can become invalid

### Boundary 3: Tool success does not automatically mean evidence validity

Even if a tool returns success, the resulting evidence may still be unusable.

Implication:
- image comparison and scene sanity checks are part of Gym validation
- a successful command log is necessary but not sufficient

## Why Gym-01 Still Counts As Baseline-Ready

`Gym-01` still counts as baseline-ready because the core question of the first pass was:

- can we automate a controlled Unreal lighting/readability pass end-to-end using structured tools?

The answer is now:

- yes, at baseline level

What remains open is not the baseline path itself, but the quality of the final visual delta.

## Reporting Guidance

When this work is referenced in later usability reports, the recommended wording is:

- `Gym-01 baseline automation path validated`
- `camera-anchored evidence capture validated`
- `controlled-scene lighting workflow validated`
- `showcase-quality before/after pair remains an optional improvement item`

Avoid wording such as:

- `Gym-01 fully completed as a final showcase`
- `Gym-01 produced final best-in-class visual evidence`

Those statements would overclaim what has actually been proven so far.

## Recommended Follow-Up Use

The practical value of `Gym-01` is that it de-risks the next items:

- `Gym-02 3D Space Readability Modify`
- later lighting/readability follow-up work
- future figure-rich feasibility reporting

It should therefore be treated as:

- a baseline infrastructure milestone
- a reference case for tool-chain maturity
- a cautionary example for evidence validation rules
