# Gym-05 Animation / Locomotion Modify

## Status

- `Domain`: `3d-animation-locomotion`
- `Task Type`: `modify`
- `Track`: `Baseline`
- `Status`: `baseline-defined`

## Goal

`Gym-05` 的 baseline 目标不是直接证明完整角色动画系统，也不是一上来就做复杂 Animation Blueprint、Motion Matching 或状态机调参。

这一项更关注：
- AI 能否在一个受控 3D 场景里，为角色移动/朝向/通行方向建立最小且可读的展示条件
- AI 能否自动识别当前工程是否已经具备可用的 locomotion showcase 资产
- 当资产或工具不足时，AI 能否明确记录边界，而不是伪造一个看似通过的结果

换句话说，`Gym-05` baseline 测的是 `animation / locomotion readiness`，不是完整角色动画制作。

## Recommended Scenario

当前推荐的 baseline 场景分成两档：

### Path A: Character-Ready Project

如果工程已经具备：
- 可用角色蓝图或 Pawn / Character 资产
- skeletal mesh / animation 相关可视资产
- 至少一条可展示的移动或朝向变化路径

那么 baseline 优先验证：
- 起点/终点可读性
- 角色朝向和移动方向是否一致
- 相机是否能稳定拍到位移前后差异

### Path B: Capability Boundary Pass

如果工程暂时不具备上面的资产或结构化工具，那么 baseline 不强行伪造 locomotion 结果，而是记录：
- 当前可用的 proxy 手段
- 当前缺失的 animation / locomotion 条件
- 哪些能力需要更合适的 sample 项目或后续工具补齐

## Recommended Implementation Path

### Path A: Locomotion Readiness First

第一条 baseline 路线优先验证最小 locomotion 场景是否成立。

推荐最小结构：
- 一个角色或角色代理
- 一条短路径或两点式移动目标
- 一个固定 capture camera
- 一组 before / after

### Path B: Blueprint Follow-Up

如果当前工程里已经有 Blueprint-friendly 的角色资产，后续再进入：
- Pawn / Character 属性调整
- 简单移动参数
- Blueprint glue logic

但这不作为第一轮 baseline 阻塞项。

## Scope

允许修改：
- 角色或角色代理的位置 / 朝向
- 路径锚点
- capture camera
- supporting readability prop 或 light

当前不做：
- 重型 Animation Blueprint 图结构改造
- Motion Matching 系统调整
- 复杂 input / controller / gameplay loop
- 多状态 locomotion 系统验证

## Relationship To Earlier Gyms

- `Gym-01`
  建立了 lighting / capture 基础链
- `Gym-02`
  建立了 space readability baseline
- `Gym-03`
  建立了 gameplay feedback baseline
- `Gym-04`
  建立了 encounter proxy baseline
- `Gym-05`
  用来判断当前链路是否已经足够进入“角色移动/动画展示”这个更贴近角色体验的能力域

## Recommended Tool Path

`Gym-05` 当前优先依赖：

- `RemoteMCP P0` scene/testbed construction
- `RemoteMCP P0` evidence capture
- `RemoteMCP P1` lighting baseline
- 如可用，再利用 Blueprint / Pawn 相关工具做局部角色设置

如果当前工程没有合适角色资产，不建议为了 baseline 退回重型长脚本或复杂 sample 接入。

## Baseline Success Criteria

`Gym-05` baseline 通过的标准是：

1. 当前工程确实存在可用的 locomotion showcase 条件
2. 有一组有效的 `before/after`
3. `after` 能体现角色移动、朝向或路径可读性的明确变化
4. 如果条件不足，能清晰记录边界和缺口，而不是伪造通过

## Current Reading

当前对 `Gym-05` 的理解应写成：

- baseline brief 已定义
- 是否真正开跑，取决于当前工程是否具备足够的角色 / animation showcase 资产
- 如果不具备，第一轮输出也可以是一个有价值的 baseline boundary finding

## Hand-Off

后续如果继续推进，优先顺序是：

1. 先判断 fresh 工程是否已经具备最小 locomotion showcase 条件
2. 如果不具备，记录 baseline boundary
3. 再决定是否引入更合适的 sample 项目或后续 animation-friendly 工程
