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

## Gym-01 Combat Modify

Use when:
- validating AI on combat-focused showcase work
- modifying an existing battle sample, arena, or encounter setup
- testing whether AI can make a localized gameplay change without rebuilding the whole loop

Scope:
- prefer an existing combat scene, benchmark arena, or showcase sample
- keep the task in `modify`, not `create`
- change only the smallest part needed to produce a visible combat difference

Recommended changes:
- adjust enemy composition or spawn rhythm
- add one lightweight attack pattern or hit reaction
- tune damage, knockback, readability, or threat pacing

Validation:
- capture before/after screenshots or short run evidence
- record the exact combat change
- verify compile/runtime/package path appropriate to the project
- note whether the change improved readability, pressure, or feedback

Output:
- task definition
- scene/sample used
- assets or code touched
- validation evidence
- risk summary
- readiness score

## Gym-02 Lighting Modify

Use when:
- validating AI on lighting-oriented showcase work
- modifying an existing scene for mood, readability, or presentation
- testing whether AI can make a visible visual pass without destabilizing the level

Scope:
- prefer an existing high-quality sample scene or controlled benchmark arena
- keep the task in `modify`, not `create`
- change only the lighting and closely related presentation settings unless explicitly approved

Recommended changes:
- shift time-of-day from day to dusk or night
- run a combat readability lighting pass
- create a small cinematic mood pass for a focal area

Validation:
- capture before/after screenshots from matching camera positions
- record which lighting actors, settings, or post-process elements changed
- note impact on readability, mood, and potential performance risk
- verify that the scene still loads and presents correctly

Output:
- task definition
- scene/sample used
- lighting intent
- before/after evidence
- validation note
- performance and risk note
- readiness score
