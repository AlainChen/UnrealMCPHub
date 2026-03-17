# Gym-01 Lighting Readability Modify

## 状态

- `Domain`: `3d-lighting-readability`
- `Task Type`: `modify`
- `Track`: `Baseline`
- `Status`: `in-progress`

## 目标

在一个已有 3D 场景上完成一次轻量的 lighting / readability 修改，并形成第一份适合展示的 Gym 证据包。

本轮重点是：
- 轻量
- 可见
- 容易做 before / after
- 对当前 workflow 友好
- 全自动

## Baseline Definition

`Gym-01` 是 baseline，不是 advanced lighting showcase。

它应该验证的是：
- AI 能否通过当前自动化链路完成一次最小 lighting/readability 修改
- 修改是否足够可见、可复现、可归档

它不应该一开始就承担：
- 完整天气系统
- 复杂 post process 组合
- 重型 day-night cycle 系统
- 长链路截图、保存、视口控制、效果修改全部混在一次自动化里

## 推荐载体

优先顺序：
1. 一个现成的稳定 3D 场景
2. 当前外部 benchmark 工程里的稳定 arena 或测试图
3. 未来如果装了更成熟的官方 sample，再切到更强 showcase 载体

## 第一轮范围

允许改动：
- directional light
- skylight
- post process
- fog / atmosphere
- 少量直接服务于可读性的 scene lighting 设置

本轮不做：
- 大范围关卡改造
- 新 gameplay 系统
- 新 UI 系统
- 重资产迁移
- 对外部插件的依赖
- advanced weather pipeline
- 高风险长链路自动化编排

## Baseline Pass

这一轮 baseline 只做两件事，而且都必须保持全自动：

### Modify A: Time-of-Day Shift

把当前场景从默认白天切到黄昏、傍晚或夜景版本。

### Modify B: Readability Pass

强化一个 focal area、进入区或关键展示区的可读性。

## 成功标准

1. 有一组同机位 before / after
2. 场景 mood 和 focal readability 有明确变化
3. 修改流程可以通过低风险自动化路径重复执行
4. 有一条 readiness 结论

## 最小证据包

- before 截图
- after 截图
- lighting intent 说明
- 风险说明
- readiness 结论

## 完成后的交接

如果这轮 baseline 成功，下一步应该：
- 归档 before / after 证据
- 写一段结果摘要
- 再启动 `Gym-02 3D Space Readability Modify`
