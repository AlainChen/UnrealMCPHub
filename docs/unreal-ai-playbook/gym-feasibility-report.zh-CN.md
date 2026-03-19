# Unreal Capability Gym Feasibility Report

## Executive Summary

当前 `Unreal Capability Gym` 已经完成前四项 baseline 验证，并为第五项动画/位移能力明确了边界。

这意味着：
- Gym 已从“概念和方法论”推进到了“有真实证据支撑的可用性验证”
- `RemoteMCP` 已经具备支撑多种 3D baseline modify 的基础能力
- 后续重点应从“继续证明能不能做”转向“整理图文报告、统一证据口径、选择更合适的下一批 showcase 载体”

## Scope

本报告覆盖：
- `Gym-01` 到 `Gym-05` 的当前状态
- 支撑 Gym 的 `RemoteMCP P0 / P0.5 / P1 lighting foundation`
- 当前最重要的边界、风险和后续机会

## Current Gym Status

### Gym-01 `3D Lighting Readability`

状态：
- `baseline-ready`

结论：
- lighting foundation、controlled scene、camera-anchored capture 已验证
- 更适合作为 baseline infrastructure validation 引用

### Gym-02 `3D Space Readability`

状态：
- `baseline-ready`

结论：
- controlled scene 和 camera-anchored evidence 已经足以支撑局部空间可读性修改
- `before/after` 已经可以有效反映空间变化

### Gym-03 `3D Gameplay Feedback`

状态：
- `baseline-ready`

结论：
- 轻量 `Actor / Trigger` 路线已经可行
- Blueprint 应视为 follow-up path，而不是第一轮阻塞项

### Gym-04 `3D Combat Encounter`

状态：
- `baseline-ready`

结论：
- static encounter proxy 路线已经可行
- combat baseline 可以先验证 encounter readability，而不是完整 combat simulation

### Gym-05 `3D Animation / Locomotion`

状态：
- `brief-ready`
- `boundary-known`
- `not yet passed`

结论：
- 当前缺少合适的角色/动画 showcase 载体
- 不应为了“形式上完成”而伪造 locomotion 结果

## What Has Been Proven

当前已经被验证的核心能力包括：

- structured MCP tools 已经足够支撑多种 3D baseline modify 任务
- controlled scene / testbed construction 已可复用
- camera-anchored capture 已形成稳定证据路径
- baseline Gym 不需要依赖重型长 `run_python_script`
- readability、feedback、encounter proxy 这些域已经能通过轻量自动化验证

## Tooling Foundation

### RemoteMCP P0 / P0.5

已建立：
- map lifecycle
- scene/testbed construction
- evidence capture
- health / reconnect baseline
- session-disrupting map semantics
- 核心错误码起步：
  - `map_unsaved`
  - `map_not_found`
  - `map_already_exists`

### RemoteMCP P1 Lighting Foundation

已建立：
- lighting rig lookup / ensure
- directional light / skylight / fog 设置
- time-of-day preset
- camera-safe capture workflow

## Key Boundaries

当前最重要的边界包括：

1. map transition 仍应视为 `session-disrupting`
2. 一个工程应保持一个活跃 editor 实例参与 baseline validation
3. tool success 不自动等于 evidence 有效
4. animation / locomotion 需要更合适的角色资产或 sample 载体

## Practical Reading

如果要对团队或合作方解释当前 Gym 状态，建议这样表述：

> 当前 Gym 已完成前四项 baseline 验证，证明了 AI + structured MCP tools 在 Unreal 里的多种 3D modify 任务已经可用；第五项动画/位移能力的缺口也已明确，下一步重点将转向更完整的图文可用性报告以及更适合 locomotion 的标准 showcase 载体。

## Near-Term Recommendations

- 基于 `Gym-01` 到 `Gym-04` 整理第一版 figure-rich report
- 明确 `artifacts/` 中哪些截图和 JSON 可以被正式引用
- 决定 Gym 是否迁移到独立 `__Gym` 资产根
- 为 `Gym-05` 引入标准角色资产或合适 sample 项目
- 收敛 external runner，减少临时 PowerShell MCP client 依赖

## Long-Term Recommendations

- 建立 durable external MCP client/runtime boundary
- 评估 typed outer control layer（`Go` 优先，`TypeScript` 备选）
- 支持 source-built Unreal workflows
- 引入更工业化的权限、审计、回滚与多用户协作规则
