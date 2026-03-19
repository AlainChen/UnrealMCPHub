# Gym-03 Gameplay Feedback Modify

## Status

- `Domain`: `3d-gameplay-feedback`
- `Task Type`: `modify`
- `Track`: `Baseline`
- `Status`: `baseline-started`

## Goal

`Gym-03` 的目标不是直接进入重型 gameplay loop，也不是一上来就做复杂蓝图图结构改造。

这一项 baseline 更关注：
- AI 能否通过结构化工具搭出一个最小交互场景
- AI 能否在 3D 场景里制造一个清晰、可见、可截图的反馈变化
- AI 能否把 `trigger -> visible response` 这条链跑成有效证据

换句话说，`Gym-03` 测的是 `interactive readability` 和 `player-facing feedback`，不是完整系统设计。

## Recommended Scenario

当前推荐的 baseline 场景是一个很轻量的 `Actor / Trigger` 场景：

- 一个受控测试场
- 一个可见目标
- 一个简单触发点或近似 trigger 的交互锚点
- 一段清晰的可视反馈

推荐的最小反馈可以是：
- `visibility toggle`
- `scale punch`
- `color / material swap`
- `supporting point light turn-on`
- `supporting prop spawn`

## Recommended Implementation Path

### Path A: Actor / Trigger First

第一条 baseline 路线优先走 `Actor / Trigger`。

原因：
- 更轻
- 更容易拿到有效 `before/after`
- 更容易判断问题是在 feedback 本身，还是在更重的 Blueprint graph 操作

这条路径适合先验证：
- 场景 reset
- 目标 actor 改变
- supporting light 或 prop 的出现
- capture camera 证据链

### Path B: Blueprint Logic Follow-Up

Blueprint 能力是 `Gym-03` 很自然的 follow-up path，但不建议作为第一步。

更合理的顺序是：
1. 先把 `Actor / Trigger` baseline 跑通
2. 再把 Blueprint 作为推荐验证路径加入

适合 Blueprint 的 follow-up 内容包括：
- overlap event
- simple trigger logic
- timer-driven feedback
- Widget / prompt glue logic

## First Baseline Path

当前第一轮 baseline 已选择 `Actor / Trigger` 路线。

第一轮的目标是：
- 保持场景和工具链尽量简单
- 只做一次清晰的反馈修改
- 重点验证自动化能力，而不是追求复杂玩法

推荐结构：
- 一个 `Gym03_TriggerMarker`
- 一个 `Gym03_Target`
- 一个 `Gym03_FeedbackLight`
- 一个 `Gym03_FeedbackPillar`

然后通过结构化工具完成：
- `before`：中性状态
- `after`：目标放大或移动，同时补一个 supporting light / pillar

## Scope

允许修改：
- trigger 或 trigger-like actor
- visible target 的 transform / visibility / supporting response
- supporting point light
- supporting prop
- 局部 readability 支撑变化

当前不做：
- 完整 combat loop
- 重型 AI 行为
- 复杂 animation state machine
- 大型 UI 流程
- 大范围 Blueprint graph reconstruction

## Relationship To Earlier Gyms

- `Gym-01`
  重点是 lighting readability 和 evidence baseline
- `Gym-02`
  重点是 space readability 和局部空间组织
- `Gym-03`
  重点是 interactive readability 和 player-facing response

所以 `Gym-03` 是从“空间和光照可读性”继续走向“交互反馈可读性”的桥。

## Recommended Tool Path

`Gym-03` 当前优先依赖已经验证过的结构化能力：

- `RemoteMCP P0` scene/testbed construction
- `RemoteMCP P0` evidence capture
- `RemoteMCP P0` health / reconnect baseline
- `RemoteMCP P1` lighting baseline 支撑

不建议第一轮就退回长 `run_python_script`。

## Baseline Pass

### Modify A: Trigger Feedback Pass

用一个最小 trigger-like 场景，验证：
- target 是否发生清晰变化
- 变化是否能通过固定相机稳定拍到

### Modify B: Readability Support Pass

在反馈发生后，用 supporting light 或 supporting prop 增强可见性，确保变化不只是逻辑存在，而是视觉证据也成立。

## Evidence Bundle

每次 `Gym-03` baseline 至少保留：

- task brief
- `before` image
- `after` image
- execution summary
- interaction / feedback note
- risk note
- readiness conclusion

如果后续进入 Blueprint path，再额外补：
- modified blueprint name
- modified event / logic area
- whether the change remained local or expanded beyond baseline scope

## Success Criteria

`Gym-03` baseline 通过的标准是：

1. 有一个清晰的 `trigger / feedback` 场景
2. 有一组有效的 `before/after`
3. `after` 能体现真实可见的反馈变化
4. 工具链以结构化 MCP 工具为主，而不是长 Python 脚本

## Current Reading

当前对 `Gym-03` 的理解应写成：

- baseline 已启动
- 第一轮选择的是更轻的 `Actor / Trigger` 路径
- Blueprint 是推荐 follow-up path，而不是第一步阻塞项

## Hand-Off

后续如果继续推进，优先顺序是：

1. 先收束第一轮 `Actor / Trigger` findings
2. 再决定是否把 Blueprint path 拉进第二轮验证
3. 如果第一轮证据稳定，再把它写进更正式的图文可用性报告
