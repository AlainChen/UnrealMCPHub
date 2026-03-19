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

具体任务形态：
- 在受控小场景中建立唯一 lighting rig
- 使用固定相机拍摄 `neutral_day -> golden_hour` 这类明确 preset 差异
- 验证“调光操作是否真的出现在可复用截图证据里”

这项任务的对外意义：
- 它证明 AI 不只是“调用了灯光工具”
- 而是已经能在一个受控场景里完成最小 lighting/readability modify，并留下可复用证据

### Gym-02 `3D Space Readability`

状态：
- `baseline-ready`

结论：
- controlled scene 和 camera-anchored evidence 已经足以支撑局部空间可读性修改
- `before/after` 已经可以有效反映空间变化

具体任务形态：
- 从一个弱构图的中性场景开始
- 通过 block、pillar、路径锚点等几何体重组 focal hierarchy
- 使用固定相机拍出空间组织变化

这项任务的对外意义：
- 它证明 AI 已经能做局部 3D space modify
- 重点不是美术风格，而是“空间更容易被读懂”

### Gym-03 `3D Gameplay Feedback`

状态：
- `baseline-ready`

结论：
- 轻量 `Actor / Trigger` 路线已经可行
- Blueprint 应视为 follow-up path，而不是第一轮阻塞项

具体任务形态：
- 在受控场景中放置 target、trigger marker、supporting prop/light
- 通过 transform、visible support 或 light turn-on 做出一个清晰的反馈变化
- 用 before/after 表达“反馈发生了”

这项任务的对外意义：
- 它证明 AI 已经能做最小 player-facing feedback modify
- 不是完整 gameplay system，但已经是一个可信的交互展示切片

### Gym-04 `3D Combat Encounter`

状态：
- `baseline-ready`

结论：
- static encounter proxy 路线已经可行
- combat baseline 可以先验证 encounter readability，而不是完整 combat simulation

具体任务形态：
- 用 player proxy、enemy proxy、cover、objective marker、supporting light 组成最小 encounter
- 通过敌方位置、cover、目标锚点和局部光照强化 threat direction
- 用 before/after 证明 encounter 更像“战斗场景”而不是中性摆场

这项任务的对外意义：
- 它证明 AI 已经能做局部 combat encounter readability modify
- 不是完整动态 combat，但已经是一个可信的 combat-facing baseline

### Gym-05 `3D Animation / Locomotion`

状态：
- `brief-ready`
- `boundary-known`
- `not yet passed`

结论：
- 当前缺少合适的角色/动画 showcase 载体
- 不应为了“形式上完成”而伪造 locomotion 结果

具体任务形态：
- 目标应当是角色起点/终点、朝向、路径变化、capture camera 四者的明确对应
- 但当前工程还没有足够轻量又真实的 locomotion showcase 资产

这项任务的对外意义：
- 它不是“做不出来”
- 而是当前非常清楚地说明了：要继续验证 animation / locomotion，需要更标准的角色资产或 sample 工程

## What Has Been Proven

当前已经被验证的核心能力包括：

- structured MCP tools 已经足够支撑多种 3D baseline modify 任务
- controlled scene / testbed construction 已可复用
- camera-anchored capture 已形成稳定证据路径
- baseline Gym 不需要依赖重型长 `run_python_script`
- readability、feedback、encounter proxy 这些域已经能通过轻量自动化验证

更具体地说，当前已被验证的 3D modify 任务包括：
- lighting/readability modify
- local space readability modify
- gameplay feedback modify
- combat encounter readability modify

这些都不是纯分析或只读评审，而是：
- 有场景输入
- 有结构化修改
- 有 before/after 证据
- 有边界说明

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

如果要更具体一点，可以补一句：

> 目前已经有证据支撑的能力包括：lighting readability、局部空间重组、最小 feedback 变化、以及 static combat encounter readability。它们都已经能通过结构化工具链稳定地产生 `before/after` 证据。

## Near-Term Recommendations

- 基于 `Gym-01` 到 `Gym-04` 整理第一版 figure-rich report
- 明确 `artifacts/` 中哪些截图和 JSON 可以被正式引用
- 决定 Gym 是否迁移到独立 `__Gym` 资产根
- 为 `Gym-05` 引入标准角色资产或合适 sample 项目
- 收敛 external runner，减少临时 PowerShell MCP client 依赖

## Skillization Opportunities

当前最适合总结成 skills 或 references 的内容，不是单个 showcase 本身，而是可复用的执行模式。

### 可以优先沉淀成 skill / reference 的

1. `Gym Baseline Workflow`
- 如何从受控 map 开始
- 如何固定相机
- 如何定义 before/after
- 如何记录 risk / readiness

2. `Evidence Capture Discipline`
- camera-anchored capture
- viewport refresh
- one-editor-instance rule
- evidence validity checklist

3. `RemoteMCP Safe Usage`
- 什么时候用结构化工具
- 什么时候避免长 `run_python_script`
- map transition 后如何 reconnect

4. `Gameplay Feedback Baseline Pattern`
- `Actor / Trigger` first
- Blueprint as follow-up

5. `Encounter Readability Baseline Pattern`
- player proxy
- enemy proxy
- cover / objective marker
- supporting light

### 暂时不建议直接做成 skill 的

- `Gym-05 locomotion`
  还缺标准 showcase 载体
- 完整 figure-rich report
  还在积累更多可正式引用的证据
- 更重的 Blueprint graph / combat behavior / animation state-machine 路线
  目前还没形成稳定默认工作流

## Long-Term Recommendations

- 建立 durable external MCP client/runtime boundary
- 评估 typed outer control layer（`Go` 优先，`TypeScript` 备选）
- 支持 source-built Unreal workflows
- 引入更工业化的权限、审计、回滚与多用户协作规则
