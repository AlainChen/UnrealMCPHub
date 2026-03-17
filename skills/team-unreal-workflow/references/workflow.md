# Workflow

## Standard Loop

1. Read the task.
2. Check project and editor status.
3. Confirm allowed scope.
4. State a short execution plan.
5. Perform bounded work.
6. Validate.
7. Summarize changes and risks.
8. Hand off for review when needed.

## Scope Selection

- Use read-only mode for analysis, debugging, and design proposals.
- Use sandbox mode for prototypes and experiments.
- Use restricted mode only when the task explicitly names a feature path or module.

## Tool Priority

1. `get_project_config`
2. `hub_status`
3. `discover_instances`
4. `manage_instance`
5. `ue_status`
6. `ue_list_domains`
7. `ue_list_tools`
8. `ue_call` or `ue_run_python`

## Validation Minimums

For content tasks:
- asset existence
- map load
- PIE start or stop when relevant
- log sanity

For code tasks:
- compile result
- target behavior proof
- relevant log review

## Escalation Cases

Escalate to review before proceeding when:
- leaving sandbox paths
- touching shared assets
- touching production maps
- touching config or plugins
- changing C++ modules used outside the task scope
