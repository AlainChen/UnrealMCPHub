# Gym-01 Lighting Readability Modify

## 状态

- `Domain`: `3d-lighting-readability`
- `Task Type`: `modify`
- `Status`: `ready-to-start`

## 目标

在一个已有 3D 场景上完成一次轻量的 lighting / readability 修改，并生成第一份真正适合展示的 Gym 证据包。

这次任务的重点是：
- 轻量
- 可见
- 容易前后对比
- 对当前 workflow 友好

## 推荐载体

优先顺序：

1. 一个现成的稳定 3D 场景
2. 当前外部 benchmark 工程里的 arena 或稳定测试图
3. 如果后续安装了更成熟的官方 sample，再切到更强 showcase 载体

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

## 推荐任务

### Modify A: Time-of-Day Shift

把当前场景从默认白天切到黄昏或夜景版本。

### Modify B: Readability Pass

增强一个 focal area、战斗区或进入区的可读性。

## 成功标准

1. 有一组同机位 before / after
2. 场景 mood 和 focal readability 有明显变化
3. 没有破坏当前加载和展示稳定性
4. 有一条 readiness 结论

## 最小证据包

- before 截图
- after 截图
- lighting intent 说明
- 风险说明
- readiness 结论
