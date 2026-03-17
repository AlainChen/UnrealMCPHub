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
