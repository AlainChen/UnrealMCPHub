# Hub vs RemoteMCP Boundary

## 目的

这份文档回答一个很实际的问题：

为了把 `Capability Gym` 推到更高自动化边界，我们接下来该继续改哪里？

当前有两个可能的落点：
- `UnrealMCPHub` fork
- `UnrealRemoteMCP` 插件仓库

因为当前只 fork 了 `UnrealMCPHub`，所以必须先把边界说清楚，避免同时开两个项目导致复杂度失控。

## 一句话结论

- `UnrealMCPHub` 更适合做：控制面、编排面、验证面、文档面
- `UnrealRemoteMCP` 更适合做：UE 编辑器内部的结构化工具能力

也就是说：

如果目标是继续优化 workflow、benchmark、Gym 报告和能力边界，当前只改 Hub 仍然有价值。  
如果目标是补齐稳定的建图、搭场景、lighting rig、capture、PPV 等结构化工具，那么最终大概率需要改 `RemoteMCP`。

## 当前仍可在 Hub 推进的内容

这些内容不必立刻 fork 第二个项目，也仍然值得继续做：

### 1. Workflow 与 Gym 编排

- baseline / advanced track 定义
- gym task brief
- evidence bundle 结构
- readiness 标准
- low-overhead / safe-path 规则

### 2. 验证与留档

- `benchmark-preflight`
- `benchmark-lite`
- gym 边界记录
- local artifact 留档规范
- 图文可行性报告结构

### 3. Backlog 与能力评审

- Gym Tooling Backlog
- MCP Tooling Review
- 哪些能力已可用、哪些只是 listed、哪些已知高风险

### 4. Hub 层 orchestration

Hub 侧如果要继续增强，也更适合做：
- 运行前检查
- 调用顺序编排
- 失败分类
- artifact 聚合
- 报告生成

换句话说：
Hub 可以继续负责“怎么组织一次 Gym 运行”，但不适合长期负责“UE 内部能力本身怎么实现”。

## 当前不适合只靠 Hub 解决的内容

下面这些能力，理论上可以继续用 `run_python_script` 硬绕，但长期不应该这样做：

### 1. 地图生命周期工具

例如：
- `create_blank_map`
- `create_map_from_template`
- `save_map_as`
- `load_map`

问题：
- 现在这些能力只能通过 UE Python API 猜签名
- 失败时错误信息偏底层
- 很容易把 Gym 变成“调 Python 反射”

### 2. 场景搭建工具

例如：
- `spawn_static_mesh_actor`
- `reset_testbed`
- `delete_actors_by_prefix`
- `ensure_capture_camera`

问题：
- 这类操作频率高
- 如果没有结构化封装，就会一直写成长 Python

### 3. Lighting / Lookdev 工具

例如：
- `create_basic_lighting_rig`
- `apply_time_of_day_preset`
- `apply_readability_pass`
- `set_skylight`
- `set_fog`

问题：
- 这些本质上是编辑器内高频工具
- 更应该由 `RemoteMCP` 直接暴露

### 4. Capture / Evidence 工具

例如：
- `capture_viewport`
- `capture_before_after`
- `set_editor_camera`
- `ensure_capture_camera`

问题：
- 现在 screenshot 和 camera 控制已经反复出现在 Gym 边界里
- 它们应该是第一类结构化工具，而不是拼脚本

### 5. Post Process / 高风险对象包装

例如：
- `ensure_post_process_volume`
- `set_post_process_overrides`
- `apply_mood_post_process_preset`

问题：
- 当前最明显的边界之一就是 PPV 属性访问
- 这类对象最需要插件侧做安全 wrapper

## 为什么这些更像 RemoteMCP 的职责

因为这些能力都满足下面几个条件：

- 发生在 UE 编辑器内部
- 需要稳定访问 UObject / Actor / Component
- 需要了解属性名、类型、调用顺序
- 需要更好的错误分级和对象 introspection

这类能力如果放在 Hub 外层，只会越来越依赖：
- `run_python_script`
- 长脚本
- 运行时猜 API

这正是当前 Gym 崩溃和边界不断出现的根源。

## 当前最现实的建议

### 方案 A：继续只做 Hub

适合目标：
- 继续完善文档
- 继续跑 baseline 边界
- 暂时不增加多仓库负担

优点：
- 复杂度低
- 还可以继续积累需求和边界清单

缺点：
- 很多能力只能继续卡在 backlog
- Gym 自动化上限提升会比较慢

### 方案 B：先把需求收清，再 fork RemoteMCP

适合目标：
- 真的想把 Gym 做成稳定自动化能力验证框架

建议前提：
- 先有明确的 P0 工具清单
- 不要 fork 之后再临时想功能

优点：
- 能补结构化工具
- 能真正推高自动化边界

缺点：
- 多项目协作复杂度会明显上升

## 当前推荐

当前最合理的节奏是：

1. 继续在 Hub 里把：
   - baseline 定义
   - Gym backlog
   - MCP review
   - 边界记录
   收完整

2. 等 P0 工具清单稳定后，再决定是否 fork `RemoteMCP`

也就是说：
现在还不需要立刻 fork 第二个项目，  
但我们已经很明确：如果要真正补基础能力，最终大概率要走到那一步。

## 当前 P0 工具清单

如果未来决定 fork `RemoteMCP`，第一批最值得做的是：

1. 地图生命周期工具
2. 最小场景搭建工具
3. Lighting rig / preset 工具
4. Capture / before-after 工具
5. Post Process Volume 安全 wrapper

这 5 项就是目前最清晰的“插件侧结构化工具缺口”。
