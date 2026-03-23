# Playable Game Validation Plan

## Goal

Validate whether the current `UnrealMCPHub + RemoteMCP` workflow can support building a **small but genuinely playable Unreal game** rather than only isolated tool demos.

For this plan, "playable" means the project includes all of the following:

- at least one intentional level
- a real game loop
- a controllable 3C player character
- a clear game goal

This plan is not trying to prove that the stack can build a full production game end to end.
It is trying to prove that the stack can complete a bounded "vertical-slice-style" playable experience with stable workflow evidence.

## Working Definition Of Playability

A test game passes the minimum playability definition only if all four conditions are true:

1. `Level`
   - the player is placed in a designed play space rather than an empty tech map
   - the play space contains traversal, encounter, or objective-relevant composition

2. `GameLoop`
   - the player can enter play, act, progress, and reach either success or failure
   - the session is not just free roaming

3. `3C Character`
   - the player has a controllable character with:
     - character locomotion
     - camera
     - at least one core action

4. `Game Goal`
   - the game communicates what the player is trying to achieve
   - there is a measurable completion condition

## Recommended Official Sample Strategy

Use official Epic samples in layers instead of forcing one sample to answer every question.

### Primary Playable Validation Sample

`Stack O Bot`

Why:

- already structured as a traversable third-person sample
- easier to convert into a bounded "goal-driven level" test than Lyra
- good fit for:
  - level readability
  - traversal
  - objective placement
  - local game loop shaping

Use it for:

- first full playable-game validation pass
- level + traversal + objective loop

### Secondary Combat/System Validation Sample

`Lyra`

Why:

- stronger gameplay system foundation
- better for combat/system/UI ability validation
- more realistic for "game-feature" extension than a tiny sandbox

Use it for:

- combat-focused playable validation
- system-heavy objective/game-state tests

### Secondary 3C / Locomotion Validation Sample

`Game Animation Sample (GASP)`

Why:

- best fit for locomotion quality
- useful to prove 3C fidelity and movement readability
- not ideal as the only sample for complete game-goal validation

Use it for:

- movement/animation branch validation
- later 3C quality pass, not as the first full playable sample

### Reference-Only Sample

`Content Examples`

Why:

- good for learning isolated engine patterns
- weak fit for proving "a whole playable game"

Use it for:

- reference patterns
- isolated capability extraction

## Recommended Validation Order

The most practical order is:

1. `Stack O Bot`
   - prove first playable slice
2. `Lyra`
   - prove combat/system-heavy playable slice
3. `GASP`
   - prove upgraded 3C/locomotion fidelity branch

## Test Case Categories

The test suite should be organized by player-facing playability, not only by tool domain.

### Category A: Project Readiness

These cases validate whether the project can even support repeatable agent work.

#### TC-A1 Project Setup

- objective:
  - sample project can be configured through Hub workflow
- pass when:
  - project path is known
  - engine path is known
  - plugin is installed and enabled
  - MCP health passes

#### TC-A2 Runtime Readiness

- objective:
  - Unreal-side Python runtime dependencies are available
- pass when:
  - `ping`
  - `get_editor_state`
  - `get_current_level`
  all work without runtime import failures

### Category B: 3C Character

These cases validate the minimum controllable player pillar.

#### TC-B1 Character Spawn And Possession

- objective:
  - a valid playable character is spawned and possessed at start
- pass when:
  - entering play yields a controllable player pawn

#### TC-B2 Camera And Movement

- objective:
  - the player can move and camera framing is usable
- pass when:
  - traversal is controllable
  - camera is readable enough for play

#### TC-B3 Core Action

- objective:
  - the player has at least one meaningful action
- examples:
  - jump
  - interact
  - attack
  - use ability
- pass when:
  - the action can be executed reliably and matters to progression

### Category C: Level And Goal

These cases validate whether the project is more than a toy map.

#### TC-C1 Intentional Play Space

- objective:
  - the level contains designed focal points, paths, or gating
- pass when:
  - the player can identify where to go next

#### TC-C2 Objective Communication

- objective:
  - the game communicates a goal
- pass when:
  - the player can understand what success looks like

#### TC-C3 Objective Completion

- objective:
  - the level contains at least one real completion condition
- pass when:
  - the player can trigger a success state

### Category D: GameLoop

These cases validate real play structure.

#### TC-D1 Start To Goal Loop

- objective:
  - the session has a beginning, middle, and end
- pass when:
  - player starts
  - performs at least one meaningful action sequence
  - reaches success or failure

#### TC-D2 Retry Or Reset

- objective:
  - the loop can be replayed
- pass when:
  - player can restart or re-enter the objective cleanly

#### TC-D3 Feedback And State Change

- objective:
  - player actions change visible or gameplay state
- pass when:
  - triggers, interactables, enemies, pickups, doors, counters, or UI react meaningfully

### Category E: Validation And Packaging

These cases prove workflow reliability rather than only game content.

#### TC-E1 Evidence Capture

- objective:
  - before/after evidence can be captured for a development task
- pass when:
  - one valid evidence pair exists
  - execution summary exists
  - risk note exists

#### TC-E2 Buildability

- objective:
  - the project still compiles and launches after task completion
- pass when:
  - compile passes
  - editor launch remains healthy

#### TC-E3 Playable Package Gate

- objective:
  - the test game can cross a packaged viability threshold
- pass when:
  - packaging or packaged smoke-check passes

## First Concrete Validation Matrix

### Playable Slice 01

`Stack O Bot / Goal-Driven Traversal Slice`

Target:

- one bounded level
- one traversal route
- one objective gate
- one completion condition

Must pass:

- TC-A1
- TC-A2
- TC-B1
- TC-B2
- TC-B3
- TC-C1
- TC-C2
- TC-C3
- TC-D1
- TC-D2
- TC-D3
- TC-E1
- TC-E2

Stretch:

- TC-E3

### Playable Slice 02

`Lyra / Combat-Objective Slice`

Target:

- one combat-capable player
- one combat or interaction objective
- one win condition

Must pass:

- TC-A1
- TC-A2
- TC-B1
- TC-B2
- TC-B3
- TC-C2
- TC-C3
- TC-D1
- TC-D3
- TC-E1
- TC-E2

### Playable Slice 03

`GASP / 3C Fidelity Slice`

Target:

- stronger locomotion
- clearer 3C feel
- reused objective shell from another slice if needed

Must pass:

- TC-B1
- TC-B2
- TC-B3
- TC-D1
- TC-E1

## Recommended Development Sequence

Use the same Hub-centered workflow for each playable slice.

1. choose sample project and target slice
2. define sandbox map or bounded feature scope
3. run readiness checks
4. implement one test-case cluster at a time
5. capture evidence after each meaningful change
6. summarize:
   - what changed
   - what passed
   - what remains blocked

The recommended implementation order for the first slice is:

1. `A` readiness
2. `B` controllable character
3. `C` objective and level readability
4. `D` end-to-end loop
5. `E` evidence and package gate

## What Counts As Success

This validation plan succeeds when we can honestly say:

- at least one official Epic sample was extended into a real bounded playable slice
- the slice satisfies level + game loop + 3C + goal
- the slice was built through the Hub/MCP workflow rather than manual-only authoring
- the process leaves behind evidence, risks, and repeatable conclusions

At that point, the stack can be said to support more than isolated tool demos.
