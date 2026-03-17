# Gym-01 Combat Modify

## 状态

- `Domain`: `combat`
- `Task Type`: `modify`
- `Status`: `in-progress`
- `Project Form`: external Unreal sandbox benchmark project

## 目标

用一个已经存在的战斗样本作为 showcase 载体，完成一次局部战斗修改，并输出一份可进入图文报告的证据包。

这次任务不追求“重做完整战斗系统”，而是验证：
- AI 是否能在已有 Unreal combat loop 上做安全、可见、可验证的局部修改
- 这种修改是否足够形成前后对比
- 修改结果是否能进入图文可行性报告

## 当前选定载体

当前默认使用已经跑通 `vampire-survivors-v1` 风格 benchmark 的外部 Unreal sandbox 项目作为载体。

已知可复用的基础：
- benchmark arena
- player auto-attack loop
- enemy spawn loop
- experience and level-up loop
- packaged benchmark evidence

选择原因：
- 它是当前本机最轻量、同时又已经具备完整 combat 主循环的 showcase 载体
- 相比从引擎模板重新搭战斗样本，它能更快产出 before/after 证据
- 相比等待更重型 demo 项目，它更适合立即开工

与官方样本策略的关系：
- 当前不阻塞后续按需安装 `Lyra`、`Stack O Bot`、`GASP`
- 但第一轮 Gym-01 不依赖这些重型样本
- 先把第一份 combat showcase 证据跑出来，再决定是否需要切到更重的官方载体

## 第一轮修改范围

第一轮只做局部 combat modify，不做系统重构。

优先候选：
- 调整敌人组合或刷怪节奏
- 增加一条轻量攻击变化
- 增强命中反馈或受击可读性

第一轮默认推荐：
- 保留当前玩家和成长主循环
- 只增强“敌人节奏 + 命中反馈”这两部分

轻量化原则：
- 尽量复用现有 C++ combat loop 和 arena
- 不引入新的重型系统
- 不要求更换 showcase 工程
- 优先做参数、局部行为和反馈级修改

## 成功标准

至少满足：

1. 有清晰的局部战斗修改
2. 有前后对比证据
3. 有运行或日志验证
4. 有风险结论
5. 有 readiness 判断

## 最小证据包

- 同场景前后对比图
- 修改点列表
- 一段运行或日志证据
- 风险说明
- readiness 结论

## 图文报告骨架

### 1. 任务定义

- 任务名称：Gym-01 Combat Modify
- 目标：在已有 benchmark combat loop 上完成一次局部战斗修改

### 2. Showcase 载体

- 使用的外部 Unreal 测试项目
- 选择原因

### 3. 修改前

- 当前战斗循环摘要
- 关键问题或待增强点
- “before” 截图位置

### 4. 修改内容

- 修改了什么
- 为什么先改这一块
- 是否涉及代码、蓝图、地图或参数

### 5. 修改后

- “after” 截图位置
- 运行或日志证据
- 肉眼可见的变化点

### 6. 结论

- 这次修改是否成功
- 是否适合作为 showcase
- 还存在哪些边界和风险
- readiness：`research-only` / `showcase-ready` / `repeatable`

## 下一步

当前下一步默认是：
- 打开外部 Unreal benchmark 工程
- 选定第一轮具体 modify 点
- 产出第一版 before/after 证据

当前推荐的第一轮具体任务：

1. 调整 `WaveDirector` 的局部刷怪节奏
2. 增强一次命中反馈
3. 保持玩家主循环和升级主循环不变

这样能用最小改动做出最明显的 combat showcase 差异。

## 执行策略

第一轮采取“轻量 modify”策略：

- 不更换工程
- 不新增大型系统
- 不追求重新设计 combat loop
- 只做最小、最可见、最易验证的局部修改

推荐先做：

### Modify A: 节奏增强

- 提高局部波次压力
- 调整敌人组合或刷怪频率
- 目标是让战斗节奏有可见变化

### Modify B: 命中反馈增强

- 强化一次受击、击杀或命中反馈
- 可以是尺寸、颜色、亮度、短暂效果或日志/计数层面的更清晰信号

### 第一轮不做

- 不做新武器系统
- 不做新敌人种类扩张
- 不做 UI 大改
- 不做新的 showcase 工程迁移
