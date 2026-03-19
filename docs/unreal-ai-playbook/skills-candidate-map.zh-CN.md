# Skills Candidate Map

## Purpose

本文档用于回答：
- 哪些内容已经足够稳定，适合进一步沉淀成 skills 或 references
- 哪些内容还处在 Gym / feasibility 阶段，暂时不适合过早 skillize

## Skill Candidates

### 1. Gym Baseline Workflow

适合沉淀位置：
- `team-unreal-workflow/references/`

原因：
- 已经跨 `Gym-01` 到 `Gym-04` 反复验证
- 核心步骤稳定：
  - controlled scene
  - fixed camera
  - before/after
  - execution summary
  - risk / readiness

### 2. Evidence Capture Rules

适合沉淀位置：
- `team-unreal-workflow/references/`

原因：
- camera-anchored capture
- viewport refresh
- one-editor-instance discipline
- evidence validity vs tool success

这些已经是横跨多个 Gym 的共性规则。

### 3. RemoteMCP Safe Usage Guide

适合沉淀位置：
- `team-unreal-workflow/references/`

原因：
- `RemoteMCP P0/P0.5` 的 session / reconnect / risk_tier 语义已经比较稳定
- 已经足够指导 agent 和人类协作流程

### 4. Gameplay Feedback Baseline Pattern

适合沉淀位置：
- `team-unreal-workflow/references/`

原因：
- `Gym-03` 已证明 `Actor / Trigger` 路线是可复用的 baseline 模板
- Blueprint follow-up 的定位也已明确

### 5. Encounter Readability Baseline Pattern

适合沉淀位置：
- `team-unreal-workflow/references/`

原因：
- `Gym-04` 已证明 static encounter proxy 路线成立
- 这条路线可作为以后 combat-facing showcase 的稳定第一步

## Not Yet Ready For Skillization

### Gym-05 Animation / Locomotion

当前状态：
- `brief-ready`
- `boundary-known`
- `not yet passed`

原因：
- 还缺标准角色资产或更合适的 sample 工程
- 现在过早 skillize 会把“缺 showcase 载体”的问题隐藏掉

### Figure-Rich Feasibility Report

原因：
- 当前已经有第一版正式报告框架
- 但还在继续积累更适合正式引用的图和证据

### Heavy Blueprint / Dynamic Combat / Animation Graph Work

原因：
- 这些还没有形成稳定 baseline
- 当前更适合作为 follow-up tracks，而不是默认 skill 入口

## Recommended Order

建议后续按这个顺序逐步下沉：

1. `Gym baseline workflow`
2. `Evidence capture discipline`
3. `RemoteMCP safe usage`
4. `Gameplay feedback baseline pattern`
5. `Encounter readability baseline pattern`

等 `Gym-05` 有正式 baseline 后，再考虑：
- `Animation / locomotion baseline pattern`
