# Benchmark Ladder

Choose the lowest scenario that answers the current question.

## Levels

### L0 Smoke

Goal:
- prove that client, Hub, RemoteMCP, and Unreal are connected

Use:
- `smoke-connectivity-v1`

### L1 Sandbox Prototype

Goal:
- prove that the agent can create and validate a small Unreal change without human rescue

Use:
- `sandbox-prototype-v1`

### L2 Restricted C++ Gameplay Loop

Goal:
- prove that the agent can implement a small C++ gameplay loop with compile and PIE validation

Use:
- `cpp-gameplay-loop-v1`

### L3 Full Scenario Benchmark

Goal:
- evaluate full autonomous capability against a heavyweight target

Use:
- `vampire-survivors-v1`

## Promotion Rule

Do not move up a level until the current level can be repeated with:
- stable connectivity
- clear summaries
- bounded failures
- reproducible validation
