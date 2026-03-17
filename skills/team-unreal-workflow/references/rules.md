# Rules

## Default Allowed Area

- `/Game/__Sandbox/`
- `/Game/__Sandbox/Maps/AI_TestMap`

## Default Forbidden Area

- production maps
- shared blueprint parents
- project settings and config
- plugin settings
- broad rename or delete operations

## Safe Change Style

- prefer additive work
- prefer new assets over shared asset mutation
- prefer bounded changes over broad edits

## Required Task Summary

Every editing task must end with:
- created assets or files
- modified assets or files
- validation performed
- unresolved risk
- recommended next step

## Binary Asset Audit Rule

Do not rely only on raw binary diffs. Audit using:
- path scope
- asset lists
- reference impact
- validation output
- task summary
