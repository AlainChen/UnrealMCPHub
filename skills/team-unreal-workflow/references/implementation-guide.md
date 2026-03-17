# Implementation Guide

This guide turns the workflow into a small number of repeatable operating rules.

## 1. Low-Overhead Mode

Use `low-overhead` mode when:
- the local machine is unstable
- Unreal execution calls are timing out
- the goal is workflow validation rather than content scale

Rules:
- start with metadata queries before execution tools
- prefer `L0` and `L1` benchmark scenarios
- avoid large scene inspection, repeated PIE cycles, and broad UI tree scans
- keep task scope inside sandbox paths unless explicitly approved

Outputs:
- short task plan
- change summary
- validation result
- next smallest step

## 2. Benchmark Preflight

Run this before any benchmark beyond ad-hoc exploration.

Checklist:
- MCP endpoint reachable
- active Unreal instance identified
- domain metadata query succeeds
- one execution tool succeeds within timeout
- project path and sandbox target are confirmed
- agent/client/model information is recorded for the run

If preflight fails:
- stop the benchmark
- record the failing step
- classify failure as connectivity, timeout, environment, or tool issue

## 3. Branch Placement

Use branches as workflow lanes, not just storage.

- `main`
  - accepted fork baseline
- `codex/team-workflow`
  - workflow, rules, benchmark structure, project-facing docs
- `codex/lab`
  - wrappers, local experiments, troubleshooting, temporary process improvements
- `codex/benchmark`
  - benchmark-lite assets, run logs, validation matrices, scenario iteration
- `codex/pr-*`
  - small upstream-friendly fixes only

## 4. Runtime Validation Matrix

When validating Unreal MCP capability, classify findings with these states:

- `validated`
  - tool listed and a real call succeeded
- `unvalidated`
  - tool listed but not yet exercised
- `known-risk`
  - tool listed but timed out, failed, or has known instability

Record at least:
- agent name or client surface
- model identifier when known
- domain name
- tool name
- call attempted
- result status
- timeout or error notes
- environment notes

Expectation:
- different agents or models may enumerate the same tools but show different latency, tool selection, and recovery behavior
- compare benchmark results only when the agent setup is also recorded

## 5. Recommended Execution Order

1. Run benchmark preflight.
2. Choose the lowest benchmark level that answers the question.
3. Work inside `low-overhead` mode unless stability is already proven.
4. Record validation state by domain and tool.
5. Promote to a heavier benchmark only after repeatable success.
