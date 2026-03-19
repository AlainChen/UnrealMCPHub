# Gym-04 Combat Encounter Modify

## Status

- `Domain`: `3d-combat-encounter`
- `Task Type`: `modify`
- `Track`: `Baseline`
- `Status`: `baseline-started`

## Goal

`Gym-04` 的 baseline 目标不是直接证明完整战斗系统，也不是一上来就做角色行为、伤害计算和 AI 决策。

这一项更关注：
- AI 能否自动搭出一个最小 encounter 场景
- AI 能否通过局部修改，让 encounter 的威胁方向、目标层级和玩家读图能力更清晰
- AI 能否在不依赖复杂行为逻辑的前提下，做出一组有效的 `before/after`

换句话说，`Gym-04` baseline 测的是 `combat encounter readability`，不是完整 combat simulation。

## Recommended Scenario

当前推荐的 baseline 场景是一个很轻量的静态 encounter proxy：

- 一个玩家 proxy
- 2 到 3 个敌方 proxy
- 少量 cover 或 lane-shaping 几何
- 一个 objective 或 focal marker
- 一个 supporting point light

这种结构的重点是：
- 玩家视角下能不能读出 threat direction
- encounter 是否有清晰的 focal point
- 场景修改是否能让战斗意图更容易理解

## Recommended Implementation Path

### Path A: Static Encounter Readability First

第一条 baseline 路线优先走静态 proxy 路线。

原因：
- 更轻
- 更容易做自动化搭场景和截图
- 更适合先验证 encounter 的空间和对抗关系，而不是行为脚本

适合第一轮的修改包括：
- 敌方 proxy 重新布局
- cover / blocker 加入
- objective marker 加入
- supporting light 强化 focal area

### Path B: Dynamic Follow-Up

后续如果这条 baseline 稳定，再逐步进入：
- movement
- pursuit
- hit reaction
- auto-attack 或 simple combat loop

这些更适合作为 follow-up，而不是第一轮阻塞项。

## First Baseline Path

当前第一轮 baseline 已选择：

- 中性 encounter 布局作为 `before`
- 通过敌方 proxy 重排、cover、objective marker 和 supporting light 构成 `after`

推荐的第一轮结构：
- `PlayerProxy`
- `EnemyA / EnemyB / EnemyC`
- `CoverA / CoverB`
- `ObjectiveMarker`
- `KeyLight`

## Scope

允许修改：
- 玩家和敌方 proxy 布局
- cover / blocker 几何
- objective / focal marker
- supporting light
- 局部 lighting 支撑

当前不做：
- 完整 AI 行为
- damage / health 系统
- weapon differentiation
- animation state machine
- Blueprint-heavy combat graph

## Relationship To Earlier Gyms

- `Gym-01`
  建立了 lighting/readability 和截图基础链
- `Gym-02`
  建立了 space/readability baseline
- `Gym-03`
  建立了 gameplay feedback baseline
- `Gym-04`
  在前三项基础上，开始验证“玩家是否能读懂一个最小 combat encounter”

## Recommended Tool Path

`Gym-04` 当前优先依赖：

- `RemoteMCP P0` scene/testbed construction
- `RemoteMCP P0` evidence capture
- `RemoteMCP P1` lighting baseline
- actor transform 和局部 prop/light 修改

第一轮不建议一开始就退回长 `run_python_script` 或重型 Blueprint graph 操作。

## Baseline Pass

### Modify A: Encounter Layout Pass

先从一个比较弱的中性布局开始，再通过重新布敌、拉开 threat lane、加入 objective 来增强 encounter readability。

### Modify B: Support Pass

再加入：
- cover
- focal marker
- key light

让 `after` 在视觉上更明确地读出“这里发生战斗”。

## Evidence Bundle

每次 `Gym-04` baseline 至少保留：

- task brief
- `before` image
- `after` image
- execution summary
- encounter reading note
- risk note
- readiness conclusion

## Success Criteria

`Gym-04` baseline 通过的标准是：

1. 有一个最小且可读的 encounter 场景
2. 有一组有效的 `before/after`
3. `after` 能体现更清晰的 threat / focal hierarchy
4. 修改主要通过结构化 MCP 工具完成

## Hand-Off

后续如果继续推进，优先顺序是：

1. 先收束第一轮 static encounter findings
2. 再决定是否进入更动态的 follow-up
3. 如果证据稳定，再把它纳入 figure-rich feasibility 报告
