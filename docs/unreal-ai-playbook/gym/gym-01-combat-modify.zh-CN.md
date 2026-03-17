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

## 第一轮修改范围

第一轮只做局部 combat modify，不做系统重构。

优先候选：
- 调整敌人组合或刷怪节奏
- 增加一条轻量攻击变化
- 增强命中反馈或受击可读性

第一轮默认推荐：
- 保留当前玩家和成长主循环
- 只增强“敌人节奏 + 命中反馈”这两部分

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
