# Unreal AI Safety Rules

## Scope

These rules constrain AI-driven work performed through:

- [use-unrealhub](../../skills/use-unrealhub/SKILL.md)

They are intended to reduce project pollution in Unreal projects where many important assets are binary and hard to diff directly.

---

## Core Principles

1. **Bounded over broad.** Prefer bounded changes over broad edits.
2. **New over modified.** Prefer new sandbox assets over modifying shared assets.
3. **Explicit over silent.** Prefer explicit review points over silent autonomous changes.
4. **Binary assets are high risk.** Treat binary assets as high-risk unless scope is narrowly controlled.

---

## Default Allowed Scope

### Allowed By Default

- Read project status and logs
- Inspect tool availability
- Create or modify assets under the sandbox content root
- Use a dedicated test map
- Run validation commands
- Produce and attach change summaries

### Not Allowed By Default

The following require explicit approval before the agent proceeds:

| Forbidden Action | Why |
|-----------------|-----|
| Modify production maps | High blast radius, binary diff is difficult |
| Delete existing shared assets | Irreversible without version control recovery |
| Rename shared assets | Breaks references across the project |
| Change project-wide config | Affects all targets and platforms |
| Change plugins or engine settings | Can break compile or runtime behavior |
| Modify shared base blueprints | Cascading effect on all child classes |
| Perform large-scale migration or refactor | Cannot be reviewed atomically |

---

## Recommended Sandbox Boundaries

These defaults apply unless the project defines its own sandbox config.

| Boundary | Default Value |
|----------|--------------|
| Default content root | `/Game/__Sandbox/` |
| Default test map | `/Game/__Sandbox/Maps/AI_TestMap` |
| Optional UI prototype root | `/Game/UI/Prototype/` |
| Optional gameplay prototype root | `/Game/Gameplay/Prototype/` |

---

## Change Control Rules

### Rule 1: Plan Before Edit

Before any write action, the agent must state:

- **Target paths** — exact directories and asset names
- **Asset or code types** — Blueprint, C++, DataAsset, map, config, etc.
- **Validation plan** — what will be checked after the change

Do not begin edits until this plan is declared.

### Rule 2: Stay Inside Approved Paths

The agent may only modify paths explicitly approved for the task.

If completing the task requires leaving the approved path:
- **Stop immediately**
- Report what additional scope would be needed
- Wait for explicit human approval before proceeding

### Rule 3: Do Not Delete By Default

Do not delete assets, files, or maps unless:

1. The task explicitly requires deletion, **and**
2. A reviewer has approved that operation

When in doubt, archive or rename instead of delete.

### Rule 4: Treat Shared Assets As High Risk

High-risk assets include:

- Shared blueprint parents
- Main HUD or menu widgets
- Production maps
- Data assets referenced by multiple systems
- Project settings and config files
- Content referenced from packaging targets

These require **explicit approval** and **post-change review** including reference impact audit.

### Rule 5: Prefer Additive Work

| Prefer | Over |
|--------|------|
| Creating a new child blueprint | Modifying a shared base |
| Adding a new prototype widget | Rewriting a shared component |
| Creating a sandbox copy | Editing an in-use asset |
| Subclassing an existing class | Modifying the parent class |

Additive work is reversible. Shared asset changes are not.

### Rule 6: Validate After Every Task Unit

At minimum, validate one or more of:

- Blueprint compilation
- Map load without error
- PIE start and stop
- Expected asset existence
- Log sanity check

Do not declare a task complete without at least one validation step.

### Rule 7: Always Produce A Change Summary

Every editing task must end with a structured summary including:

| Field | Required Content |
|-------|----------------|
| Created assets | Full paths |
| Modified assets or files | Full paths |
| Validation performed | What was checked and result |
| Known limitations | What was not verified |
| Follow-up recommendation | Next step for human reviewer |

---

## Binary Asset Audit Strategy

`.uasset` and `.umap` files cannot be diffed directly. Audit binary changes through:

- **Path-level scope control** — was the write inside the approved path?
- **Asset list delta** — what was added, removed, or renamed?
- **Reference impact review** — did any shared reference change?
- **Validation logs** — did the asset compile and load without error?
- **Task-level operation summary** — can a reviewer understand what changed and why?

Do not rely only on raw binary diffs. Validate through behavior, not file contents.

---

## Human Review Required

Human review is **mandatory** before merging when any of the following occurred:

- Changes outside sandbox
- Production map edits
- Project config edits
- Plugin or build setting changes
- C++ module changes
- Shared asset changes
- Migrations or large batch edits
- Any change the agent flagged as uncertain or risky

---

## Reviewer Checklist

Use this checklist before approving any AI-driven task:

- [ ] Did the task stay inside the approved scope?
- [ ] Were only approved maps or directories touched?
- [ ] Were any shared assets changed? If so, was the reference impact reviewed?
- [ ] Did validation actually run? Is there a log or compile output to confirm?
- [ ] Is the change summary complete enough to audit independently?
- [ ] Can the result be merged, or should it remain sandbox-only?
- [ ] Are there any unresolved risks in the summary that need follow-up?

---

## Failure Handling

If validation fails:

1. **Stop.** Do not continue broadening scope.
2. **Gather evidence** — collect logs, screenshots, error output.
3. **Summarize the failure** — what was tried, what error occurred, what was not checked.
4. **Propose the smallest corrective step** — a targeted fix, not a broader retry.

Do not keep retrying the same destructive or high-risk operation without a revised plan and explicit approval.
