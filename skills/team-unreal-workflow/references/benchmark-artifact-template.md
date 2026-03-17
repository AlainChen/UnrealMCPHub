# Benchmark Artifact Template

Use this template for repeatable benchmark outputs instead of free-form summaries.

## Header

- run date
- benchmark level
- scenario name
- agent or client surface
- model identifier when known
- project label
- environment label

Do not include:
- local absolute paths
- private repo URLs
- personal machine identifiers
- raw access tokens, hostnames, or account names

## Preflight

Record:
- MCP reachable: yes or no
- active Unreal instance identified: yes or no
- metadata query succeeded: yes or no
- execution query succeeded: yes or no
- benchmark allowed to continue: yes or no

## Tool Availability

Record:
- top-level tools listed
- domains listed
- per-domain tool counts

## Validation Matrix

For each sampled tool, record:
- domain
- tool name
- sample call
- status: `validated`, `unvalidated`, or `known-risk`
- result summary
- timeout or failure note

## Outcome

Record:
- benchmark level reached
- major blockers
- human intervention count
- recommended next benchmark level
- recommended next smallest fix

## Confidentiality Rule

Before saving the artifact:
- mask local paths
- mask local IP or loopback details if not necessary
- generalize machine-specific identifiers
- keep only the minimum environment context needed for comparison
