# Gym Project Engineering

## 目标

这份文档回答两个问题：

1. `Capability Gym` 现在应该挂在哪个 Unreal 工程里
2. 长期来看，Gym 应该如何与 benchmark 工程、正式项目和官方 sample 解耦

## 当前判断

当前阶段，Gym 不适合直接绑死在单一 benchmark 玩法工程里，也不适合一开始就依赖重型官方 sample。

更合理的工程策略是三层：

### 1. 临时载体层

用于快速启动单个 Gym pilot。

当前最合适的临时载体是：
- `F:\MCPtest\TestMCP\TestMCP.uproject`

原因：
- 已经打通 UnrealMCPHub/RemoteMCP 链路
- 已经有稳定 sandbox map
- 当前本机没有现成安装好的 Lyra / Stack O Bot / GASP 项目
- 立即启动成本最低

限制：
- 它本质上仍然是 benchmark 测试工程
- 不适合长期承载所有 Gym showcase

### 2. Gym Sandbox 层

这是中期最值得建立的一层。

建议形态：
- 单独一个 `Gym Sandbox` 工程
  或
- 在现有外部工程里建立明确隔离的 `/Game/__Gym/` 目录和独立 map 集

它负责：
- Gym showcase 场景
- 能力域 modify 任务
- before / after 对比
- 图文报告素材

它不负责：
- 正式 benchmark 验收
- 正式项目生产功能

### 3. 官方 Sample / 高质量载体层

这是后续按需引入的一层，而不是第一步。

候选：
- `GASP`
- `Stack O Bot`
- `Lyra`

作用：
- 提供更强展示性和更真实的 3D 项目结构
- 用于特定能力域的更高阶 showcase

不建议当前阶段的做法：
- 一开始就要求所有 Gym 都基于这些重型 sample

## 当前建议

### 短期

短期先这样做：

- 用 `TestMCP` 作为临时载体
- 但明确只在独立的 Gym map / Gym 区域里做 showcase
- 不把 Gym 等同于 benchmark

### 中期

中期建议建立：

- `Gym Sandbox` 外部 Unreal 工程
  或
- 在现有工程里明确新增：
  - `/Game/__Gym/`
  - `/Game/__Gym/Maps/`
  - `/Game/__Gym/Lighting/`
  - `/Game/__Gym/Space/`
  - `/Game/__Gym/Feedback/`

这样后续：
- benchmark 继续在 benchmark 区跑
- gym 在 gym 区跑
- 两者共享基础链路，但任务目标和资产边界分开

## Gym-01 的具体落点

在当前阶段，`Gym-01 Lighting Readability Modify` 建议使用：

- `TestMCP` 工程中的临时 Gym 载体

推荐落点：
- 新建或独立维护一张专门的 Gym lighting map
  或
- 以 `AI_TestMap` 为临时载体，但只做 lighting/readability 层面的局部展示改动

建议优先：
- 先复用 `AI_TestMap`
- 等 `Gym-01` 和 `Gym-02` 都有稳定成果后，再决定是否拆独立 `__Gym` 目录和 map

## 何时需要单独 Gym 工程

出现下面任一情况时，就值得从 benchmark 工程里拆出来：

- Gym showcase 数量明显增多
- benchmark 和 gym 开始争用同一批地图或资产
- showcase 需要更多高保真视觉场景
- 需要同时测试多个官方 sample
- 图文报告素材积累到需要长期维护

## 当前结论

当前最合理的工程策略不是：
- 继续把 Gym 绑在吸血鬼幸存者式 benchmark 上

而是：
- 短期借 `TestMCP` 启动 Gym
- 中期把 Gym 资产和 benchmark 资产解耦
- 长期按能力域引入官方 sample，形成更完整的 showcase 载体矩阵
