# Scenario: C++ Gameplay Loop

## Goal

Verify that an agent can implement a small C++ gameplay loop and validate it without jumping directly to the full `vampire-survivors-v1` scenario.

## Suggested Target

Implement a minimal loop such as:
- a simple pawn or actor
- one spawnable enemy or target
- one interaction, hit, or overlap rule
- one visible state update or log proof

## Success Criteria

- C++ code compiles
- the gameplay loop can be demonstrated in PIE
- the agent summarizes files changed, validation run, and remaining gaps

## Standard Prompt

```text
In the current Unreal C++ project, implement one minimal gameplay loop that is small but real.

Requirements:
1. Use C++ for the core logic.
2. Keep the scope intentionally narrow and easy to validate.
3. Compile the project after the implementation.
4. Prove the loop in PIE or through the smallest equivalent runtime validation.
5. Summarize code files changed, validation results, known limitations, and whether the project is ready for a heavier benchmark.
```
