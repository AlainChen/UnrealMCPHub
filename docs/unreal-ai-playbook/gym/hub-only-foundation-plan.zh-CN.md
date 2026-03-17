# Hub-Only Foundation Plan

## 目的

这份文档回答一个很现实的问题：

在当前 **只 fork 了 `UnrealMCPHub`、还没有 fork `UnrealRemoteMCP`** 的前提下，
我们还能怎样继续推进 Gym 的基础能力建设，同时控制复杂度不上升过快。

它不讨论插件侧如何实现工具，只讨论：
- 当前仓库里还能做什么
- 哪些动作值得优先做
- 哪些事应该先记录为边界，而不是现在就硬实现

## 当前原则

当前阶段的目标不是“把所有 Gym 工具都实现完”，而是：

1. 把 Gym 的 **baseline 自动化能力** 跑清楚
2. 把 **可用路径** 和 **边界路径** 记录清楚
3. 把未来真正需要插件侧支持的能力，先收敛成清晰的 `P0` 工具清单

换句话说，当前阶段更像：

- Hub 侧继续做控制面
- Gym 侧继续做边界测绘
- 工具缺口先收敛，不急着马上开第二个仓库

## Hub 侧还能继续推进的内容

### 1. Gym 任务编排

在当前仓库里，最值得继续推进的是：

- baseline / advanced track 的层级定义
- 每个 Gym 任务的 brief
- before / after 证据包格式
- readiness 评分与边界结论
- 安全路径与高风险路径的区分

这部分不依赖插件侧改造，而且会直接提升后续所有 showcase 的可复用性。

### 2. 运行前后验证

Hub 侧已经有能力继续完善：

- `benchmark-preflight`
- `benchmark-lite`
- gym 边界记录
- local artifact 归档规范
- packaged build 证据链

这些能力虽然不能直接补齐 UE 内部工具，但能让我们更快发现：
- 哪条路径稳定
- 哪条路径不稳定
- 哪种自动化链路值得继续投资

### 3. 工具缺口管理

在当前仓库里，我们还可以继续把缺口管理做清楚：

- Gym Tooling Backlog
- MCP Tooling Review
- Hub 与 RemoteMCP 的边界文档
- P0 / P1 优先级列表

这一步很重要，因为它能避免“还没想清楚就 fork 第二个仓库”。

### 4. 低风险编排试验

在不修改插件的前提下，仍然可以继续做一些低风险试验：

- 短链路的自动化操作验证
- 单步 property change
- 轻量 map load / query / save / screenshot 组合
- “哪些组合稳定、哪些组合高风险”的矩阵化记录

重点不是继续堆长 Python，而是：
把 **稳定链路** 和 **不稳定链路** 区分出来。

## 当前不建议在 Hub 侧硬实现的内容

下面这些内容，理论上还可以继续用 `run_python_script` 硬拼，
但当前阶段不建议再把它们当作 Hub 侧的主要推进方向：

- 稳定建图
- 模板地图复制
- 最小 testbed 场景搭建
- lighting rig / preset
- capture camera 管理
- before / after 证据采集
- Post Process Volume 安全访问

原因不是它们不重要，而是：

- 它们都发生在 UE 编辑器内部
- 高频依赖 UObject / Actor / Component 访问
- 很容易沦为长 Python 脚本拼装
- 我们已经有证据表明这会推高崩溃概率

## P0：当前阶段最值得做的事

`P0` 的目标不是实现工具，而是把基础能力推进路径收敛清楚。

### P0-1 记录稳定路径

把当前已经跑通的轻量自动化链路继续留档：

- load map
- actor query
- single property change
- save
- screenshot
- reload + modify + save + screenshot

### P0-2 记录边界路径

把当前已知边界和高风险路径整理成稳定结论：

- PostProcessVolume 属性反射边界
- 默认模板地图复制/创建路径
- 长 `run_python_script` 串联操作
- 编辑器崩溃触发条件的共性

### P0-3 固定 Baseline Track

继续把 Gym 的第一阶段当作课程式 baseline：

- `Gym-01` Lighting Readability
- `Gym-02` 3D Space Readability
- `Gym-03` Gameplay Feedback
- `Gym-04` Combat Encounter
- `Gym-05` Animation / Locomotion

目标是先铺开能力图，而不是马上做 advanced showcase。

### P0-4 收敛插件侧缺口

把将来最可能需要插件侧支持的能力维持成清晰列表：

1. map lifecycle
2. scene/testbed construction
3. lighting rig / preset
4. capture helpers
5. Post Process wrapper

## P1：如果继续只做 Hub，可以怎么做

如果短期内明确不 fork `RemoteMCP`，那 `P1` 最值得做的是：

### P1-1 强化 Gym 管理层

- 统一 Gym artifact 模板
- 统一 before / after 命名与留档
- 统一 risk / readiness 结论格式
- 把 baseline gym 的每一次试验都写成可回顾记录

### P1-2 强化运行时判断

- 把 high-risk automation path 标成 `known-risk`
- 在 preflight / benchmark-lite 思路上，为 Gym 增加最小可用性检查
- 让“现在值不值得继续自动化压测”更容易判断

### P1-3 强化 backlog 决策质量

- 不急着实现更多临时脚本
- 优先判断每个需求到底属于 Hub 还是 RemoteMCP
- 让未来如果要 fork 第二个仓库时，能直接拿 P0 清单开工

## 当前推荐顺序

在不 fork `RemoteMCP` 的前提下，建议按这个顺序推进：

1. 完善 Gym baseline brief 和 evidence 结构
2. 继续测轻量稳定自动化链路
3. 记录边界与崩溃模式
4. 固定插件侧 `P0` 工具缺口
5. 再决定是否值得进入第二个仓库

## 一句话结论

当前只靠 `UnrealMCPHub`，我们依然可以把：

- Gym 的 baseline 路线
- 自动化可用性边界
- 证据链
- backlog 优先级

继续推进得很清楚。

但如果目标变成“真正补齐稳定的 UE 内结构化工具入口”，
那未来大概率还是要走到 `RemoteMCP` 这一侧。
