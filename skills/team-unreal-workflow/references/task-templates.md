# Task Templates

## Read-Only Analysis

Use when:
- learning project state
- diagnosing errors
- preparing a change plan

Template:
- inspect current project and editor state
- list available UE domains and tools relevant to the task
- summarize the current state
- propose the smallest safe next step

## Sandbox Actor Prototype

Use when:
- testing content creation flow

Template:
- create a new actor or asset only under `/Game/__Sandbox/`
- place it in `AI_TestMap` if needed
- validate asset existence and PIE behavior
- summarize created assets and results

## Prototype Widget

Use when:
- testing UI creation without touching production UI

Template:
- create or modify only sandbox or prototype UI assets
- verify creation and runtime attach path
- report any engine or tooling limitation encountered

## Restricted Feature Task

Use when:
- a real feature path is explicitly approved

Template:
- state approved path and forbidden paths
- implement the smallest useful change
- compile and validate
- summarize what changed and what still needs review

## Failure Report

Use when:
- task execution fails or stalls

Template:
- what was attempted
- what failed
- most likely cause
- smallest next corrective step
- whether scope should stay the same or be reduced

## Gym-01 Lighting Readability Modify

Use when:
- validating AI on lightweight 3D showcase work
- modifying an existing scene for mood, focus, and readability
- testing whether AI can make a visible scene pass without destabilizing the project

Scope:
- prefer an existing high-quality scene or stable showcase map
- keep the task in `modify`, not `create`
- change only the smallest lighting and presentation layer needed to produce a visible difference

Recommended changes:
- shift time-of-day from day to dusk or night
- run a focal readability pass
- create a small cinematic mood pass for a key area

Validation:
- capture matching before/after screenshots
- record the exact lighting changes
- verify the scene still loads and presents correctly
- note whether readability and focus improved

Output:
- task definition
- scene/sample used
- lighting intent
- before/after evidence
- validation note
- performance and risk note
- readiness score

## Gym-02 3D Space Readability Modify

Use when:
- validating AI on a lightweight 3D level or encounter readability task
- modifying an existing scene's local space, path, or point-of-interest readability
- testing whether AI can improve 3D readability without redesigning the full level

Scope:
- prefer an existing stable scene or benchmark map
- keep the task in `modify`, not `create`
- change only the local space and closely related readability cues unless explicitly approved

Recommended changes:
- adjust one local path or entry rhythm
- strengthen one focal point, POI, or readability zone
- improve one small encounter or traversal read

Validation:
- capture before/after screenshots from matching camera positions
- record which scene elements changed
- note impact on readability, path clarity, and local flow
- verify that the scene still loads and reads correctly

Output:
- task definition
- scene/sample used
- spatial intent
- before/after evidence
- validation note
- risk note
- readiness score
