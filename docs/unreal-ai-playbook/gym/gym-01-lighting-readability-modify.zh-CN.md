# Gym-01 Lighting Readability Modify

## 状态

- `Domain`: `3d-lighting-readability`
- `Task Type`: `modify`
- `Track`: `Baseline`
- `Status`: `in-progress`

## Brief

### 任务一句话

在一个轻量 3D 场景上，自动完成一次最小 lighting/readability 修改，并留下可归档的 before/after 证据。

### 任务目标

- 轻量
- 可见
- 可重复
- 全自动
- 对当前 workflow 友好

### 当前不追求的事

- 完整天气系统
- 高复杂度 post process lookdev
- 大地图或重型 sample 迁移
- 一次脚本里串联所有高风险编辑器操作

## Baseline Definition

`Gym-01` 是 baseline，不是 advanced lighting showcase。

它要验证的是：
- AI 能否通过当前自动化链路完成一次最小 lighting/readability 修改
- 修改是否足够可见、可重复、可归档
- 当前自动化链路的边界落在哪里

## 推荐载体

优先顺序：
1. 一个现成的稳定 3D 场景
2. 当前外部 benchmark 工程里的稳定测试图
3. 未来如引入更成熟的官方 sample，再切到更强 showcase 载体

## 第一轮范围

允许改动：
- directional light
- skylight
- fog / atmosphere
- 少量直接服务于可读性的 lighting 设置

本轮不做：
- 大范围关卡改造
- 新 gameplay 系统
- 新 UI 系统
- 外部插件依赖
- advanced weather pipeline
- 高风险长链路自动化编排

## Baseline Pass

这一轮 baseline 只做两件事，而且都必须保持全自动：

### Modify A: Time-of-Day Shift

把当前场景从默认白天切到黄昏、傍晚或夜景版本。

### Modify B: Readability Pass

强化一个 focal area、入口区域或关键展示区的可读性。

## Evidence Bundle

`Gym-01` 的最小证据包固定为：

- 任务 brief
- before 截图
- after 截图
- 执行动作摘要
- 自动化链路说明
- 风险说明
- readiness 结论

如果某次运行失败，也仍然应留下：

- 失败阶段
- 失败链路
- 是否属于 known-risk path
- 是否值得继续在当前工具层尝试

## Boundary Notes

当前 `Gym-01` 已经测出的边界如下：

### 已通过的低风险链路

- `load map`
- `actor query`
- `single property change`
- `save`
- `screenshot`
- `reload + modify + save + screenshot`

### 已知边界

- `PostProcessVolume` 属性访问不稳定
- 默认模板地图复制 / 创建路径高风险
- 长 `run_python_script` 串联多步编辑器操作容易导致崩溃

### 当前结论

`Gym-01` 的关键问题已经不是“能不能做 lighting modify”，而是：
当前缺少稳定的结构化 UE 工具入口，导致 baseline Gym 仍要依赖高风险 Python 编排。

## 成功标准

1. 有一组同机位 before / after
2. 场景 mood 和 focal readability 有明确变化
3. 修改流程可以通过低风险自动化路径重复执行
4. 有一条 readiness 结论

## 完成后的交接

如果这轮 baseline 成功，下一步应当：
- 归档 before / after 证据
- 写一段结果摘要
- 回填边界结论
- 再启动 `Gym-02 3D Space Readability Modify`
