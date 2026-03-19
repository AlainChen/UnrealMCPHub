# Unreal Capability Gym Status Summary

## Summary

当前 `Unreal Capability Gym` 已经形成一条比较完整的 `Baseline Track`。

截至目前：
- `Gym-01` 到 `Gym-04` 已经完成 baseline 级别验证
- `Gym-05` 已完成 brief 和 boundary finding，但还没有正式通过
- `RemoteMCP` 已完成支撑这些 baseline 的一轮 `P0 / P0.5 / P1 lighting foundation`

这意味着：
- Gym 已经不再是纯概念或文档规划
- 前四个能力域已经拿到了结构化工具驱动的有效 evidence
- 后续最值得做的不是继续硬扩数量，而是开始整理 figure-rich feasibility report，并为 `Gym-05` 准备更合适的角色/动画 showcase 条件

## Baseline Track Snapshot

### Gym-01 `3D Lighting Readability`

当前定位：
- `baseline-ready`

核心结论：
- lighting foundation、controlled scene、camera-anchored capture、baseline automation path 已验证
- `Gym-01` 更适合被表述为一次 **baseline infrastructure validation**
- 不应过度表述成“最终 hero showcase lighting comparison”

主要价值：
- 证明了 structured lighting workflow 和 camera-safe evidence path 可行
- 为 `Gym-02` 及之后的 Gym 提供了基础 capture / lighting 链路

当前保留意见：
- showcase-quality 的视觉差异仍可继续优化，但不再阻塞 baseline 结论

### Gym-02 `3D Space Readability`

当前定位：
- `baseline-ready`

核心结论：
- controlled scene reset、fixed capture camera、neutral lighting、actor transform modify、camera-anchored evidence capture 已验证
- `Gym-02` 证明了一个局部 3D 空间可以通过自动化修改变得更易读，并且变化能稳定出现在截图中

主要价值：
- 证明了“空间组织变化”已经可以被 MCP 工具链稳定表达
- 为后续 feedback / encounter 场景打下了场景构造与证据采集基础

### Gym-03 `3D Gameplay Feedback`

当前定位：
- `baseline-ready`

核心结论：
- 轻量 `Actor / Trigger` 路线已验证
- camera-anchored capture 和 viewport refresh 对 interaction-oriented scene 非常关键
- 第一轮 baseline 不需要先上重型 Blueprint graph 修改

主要价值：
- 证明了最小 `trigger -> visible response` 场景可以通过 structured MCP tools 跑通
- Blueprint 不再被当成第一轮阻塞项，而是合理的 follow-up path

### Gym-04 `3D Combat Encounter`

当前定位：
- `baseline-ready`

核心结论：
- static encounter proxy 路线可行
- 通过 proxy 布局、cover、objective marker、supporting light，可以让 encounter 从弱/中性读图变成更明确的 combat-style 场景
- baseline 不需要先引入行为树、damage 系统或完整 AI loop

主要价值：
- 证明了 combat baseline 可以先做 encounter readability，而不是一开始就做动态 combat simulation
- 暴露并修复了 repeated scene construction 里 static mesh 命名冲突的问题

### Gym-05 `3D Animation / Locomotion`

当前定位：
- `brief-ready`
- `boundary-known`
- `not yet passed`

核心结论：
- 当前底座已经足够支撑前四项 Gym
- 但 fresh 工程里没有一个足够轻量、足够真实、又能代表 locomotion 能力的标准 showcase 对象

主要价值：
- 明确了 `Gym-05` 的缺口不是“完全没有工具”，而是“缺合适角色/动画 showcase 载体”
- 后续引入标准角色资产或更适合的 sample 工程后，`Gym-05` 就有机会升级成正式 baseline pass

## What Was Actually Proven

截至目前，Gym 真正已经证明的不是“AI 已经会做完整 Unreal 游戏”，而是：

1. 结构化 MCP 工具已经足够支撑多种 3D baseline modify 任务
2. camera-anchored capture 已经成为有效证据路径
3. controlled scene / testbed construction 已经可以反复复用
4. baseline Gym 不需要一上来就退回长 `run_python_script`
5. 轻量能力域可以先用 proxy / readability / feedback 路线验证，再逐步进入更复杂的系统

## Important Tooling Learnings

### From `RemoteMCP P0 / P0.5`

已建立：
- map lifecycle
- scene/testbed construction
- evidence capture
- health baseline
- session-disrupting map semantics
- 初始核心错误码：
  - `map_unsaved`
  - `map_not_found`
  - `map_already_exists`

### From `RemoteMCP P1 Lighting Foundation`

已建立：
- `find_lighting_rig`
- `ensure_basic_lighting_rig`
- `set_directional_light`
- `set_skylight`
- `set_exponential_height_fog`
- `apply_time_of_day_preset`

### From repeated Gym execution

已明确的重要修复与原则：
- capture 应以 camera anchoring 为主，而不是依赖“当前活动视口”
- repeated run 不能强依赖 raw object name
- viewport refresh 是证据链的一部分，而不是 UI 小细节
- map transition 现在应视为 `session-disrupting`

## Operational Boundaries

当前已经明确的边界包括：

1. 一个工程一次只应有一个活跃 editor 实例参与 baseline validation
2. map transition 不应再被假设为 seamless，需要 reconnect 语义
3. tool success 不等于 evidence 有效，截图和场景 sanity check 仍是 Gym 的一部分
4. animation / locomotion 需要更合适的 asset 或 sample 支撑，不能只靠 proxy 假装通过

## Recommended Positioning For Reporting

如果现在对外描述这条 Gym 线，比较准确的说法是：

- `Gym-01` 到 `Gym-04` 已完成 baseline validation
- 这些 baseline 证明了 AI + structured MCP tools 在 Unreal 里的多种 3D modify 任务已经可用
- 当前还没有把这套能力夸张成 production-finished content generation
- `Gym-05` 明确记录了角色/动画 showcase 条件缺口，为下一轮扩展提供了边界

## Near-Term Next Steps

近期最值得做的事：
- 产出第一版 figure-rich feasibility report
- 决定是否把 Gym 从临时 benchmark/fresh map 迁到独立 `__Gym` 资产根
- 继续把 `RemoteMCP` 的 map/session semantics 回接到 Hub workflow 示例
- 为 `Gym-05` 选择一个标准角色资产或 sample 工程
- 评估稳定 external runner，减少临时 PowerShell client 的重复劳动

## Long-Term Direction

更远期的方向包括：
- durable external MCP client/runtime boundary
- typed outer control layer（`Go` 优先，`TypeScript` 备选）
- source-built Unreal workflow support
- 更工业化的权限、审计、回滚和多用户协作模式

## Overall Reading

整体上，这条 Gym 线已经从“方法论探索”推进到了“前四项 baseline 已成立、第五项边界已明确”的阶段。

这说明当前最重要的变化已经不是：
- 能不能做

而是：
- 怎么把这套 baseline 结果整理成更清晰、更可信、更适合人类阅读和团队沟通的可用性报告。
