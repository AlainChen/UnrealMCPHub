# Scenario: Smoke Connectivity

## Goal

Verify that the full Unreal benchmark chain is alive before any content benchmark begins.

## Success Criteria

- the AI client connects to MCP
- the Unreal instance is identified correctly
- at least one read tool call succeeds
- at least one harmless write or execution call succeeds
- the run ends with a structured summary

## Standard Prompt

```text
Using the current Unreal project and MCP connection, verify the benchmark chain is alive.

Requirements:
1. Confirm project and editor status.
2. Confirm the active Unreal instance.
3. List available UE domains and relevant tools.
4. Call at least one read-only tool successfully.
5. Call one harmless execution or validation action successfully.
6. Summarize the environment state, any risks, and the recommended next benchmark level.
```

## Required Outputs

- project status
- instance status
- tool/domain summary
- proof of successful tool calls
- recommended next scenario
