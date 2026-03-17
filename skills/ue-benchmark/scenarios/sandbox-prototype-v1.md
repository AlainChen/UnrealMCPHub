# Scenario: Sandbox Prototype

## Goal

Verify that an agent can perform one safe Unreal write task end to end inside sandbox boundaries.

## Success Criteria

- work stays under `/Game/__Sandbox/`
- one new sandbox asset or actor is created
- the change is validated
- the agent reports what changed and what remains risky

## Standard Prompt

```text
Using the current Unreal project, complete one safe sandbox prototype task.

Requirements:
1. Work only under `/Game/__Sandbox/`.
2. Create one small prototype asset or actor.
3. If relevant, place it in `/Game/__Sandbox/Maps/AI_TestMap`.
4. Run the smallest useful validation, such as asset existence, map load, or PIE verification.
5. Output a structured summary of created assets, validation results, risks, and the next recommended step.
```

## Notes

This scenario is intended to prove bounded write capability before any larger benchmark.
