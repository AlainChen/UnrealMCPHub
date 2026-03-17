# `vampire-survivors-v1` Benchmark 跑通报告

## 结论

当前这套 Unreal benchmark 原型已经达到“可对外展示跑通”的程度。

这里的“跑通”指：

- 已完成 `L0 -> L1 -> L2` 的逐级推进
- 已完成一个可运行的 survival loop 原型
- 已通过一次冷编译
- 已通过一次 `BuildCookRun`
- 已生成可启动的 Windows 包体
- 已拿到包体运行日志中的玩法证据

这里的“跑通”不等于：

- 已达到最终 polished 产品质量
- 已完成正式交互式升级 UI
- 已完成长期稳定性和性能优化

## 范围说明

本次 benchmark 结果基于一个外部 Unreal 5 sandbox 测试工程完成。

为了避免把实验工程和 `UnrealMCPHub` 仓库混在一起：

- 具体游戏代码、地图资产、包体和本地日志保留在外部测试工程
- 本仓库只保留方法、流程、artifact 模板和结论文档

## 已完成的 benchmark 阶段

### 1. `L0` Connectivity Smoke

已验证：

- MCP 端点可达
- metadata 查询可用
- execution 查询可用
- preflight 可生成结构化 artifact

### 2. `L1` Sandbox Prototype

已验证：

- 可在 sandbox 目录中创建和修改 Unreal 内容
- 可在 sandbox map 中完成最小写入
- 可生成结构化 artifact

### 3. `L2` Restricted Gameplay Loop

已验证：

- C++ 基座工程可编译
- 可在 sandbox map 中运行最小 gameplay loop
- 已形成 survival 原型雏形

## 本次最终展示能力

包体和运行日志已经证明下面这些能力存在：

- 玩家自动攻击
- 敌人生成和追击
- 击杀计数
- 经验掉落与吸取
- 升级触发
- 升级项应用
- HUD 显示基础状态
- 死亡/重开框架

## 关键证据

本次 benchmark 完成状态主要依赖以下几类证据：

### 1. 冷编译成功

外部工程已完成一次冷编译通过，说明当前原型不只是 Live Coding 会话中的临时状态。

### 2. `BuildCookRun` 成功

已完成一次成功的：

- `build`
- `cook`
- `stage`
- `package`
- `archive`

这意味着 benchmark 的 hard gate 已经通过。

### 3. 包体可启动

已成功启动一次打包后的 Windows 可执行文件，并生成运行日志。

### 4. 运行日志证明 survival loop 在执行

运行日志中已经出现了这类关键行为：

- 刷怪
- 自动攻击击杀
- 经验球授予经验
- 升级触发
- 升级项应用

这些证据足以支持“benchmark 已跑通”的结论。

## 为何这次结果可以对外展示

因为它已经同时满足了三层要求：

1. 工程层：
   可冷编译、可打包、可启动

2. 玩法层：
   不只是静态场景，而是有真实生存循环

3. 证据层：
   有 preflight、benchmark-lite、运行日志和包体产物

## 当前仍然存在的限制

这版可以展示，但还不应该被称为“最终完成版”。

主要限制包括：

- 升级选择目前仍是轻量自动选择，不是真正交互式 `3 选 1`
- 玩家移动未接入，当前更偏 benchmark 自动演示版本
- 敌人与波次差异化还偏轻量
- 首次运行仍可能出现明显 PSO hitch
- `RemoteMCP + Python + PIE` 的长脚本验证链曾出现崩溃，不建议把它作为最终验证主路径

## 对仓库的意义

这次结果证明了：

- `UnrealMCPHub` 的 preflight / benchmark-lite / artifact 体系是有价值的
- 用“先轻后重”的梯度 benchmark 路线是正确的
- benchmark 结果应该以“文档 + artifact 说明 + 外部工程验证”方式沉淀，而不是把实验工程直接并入工具仓库

## 建议的后续收口方向

如果要把这套结果继续向“更像正式展示件”推进，优先级建议是：

1. 补玩家移动输入
2. 把升级选择从自动选择升级为真正交互式 `3 选 1`
3. 提升敌人和波次差异化
4. 增加截图、短录屏和演示脚本
5. 产出一份更正式的 benchmark 展示说明

## 建议的对外表述

可以使用下面这种表述：

> 已基于 `UnrealMCPHub` 跑通一套 `vampire-survivors-v1` 风格的 Unreal benchmark 验证链，完成了从 preflight、sandbox prototype、restricted gameplay loop 到可打包可运行 Windows 构建的完整闭环。
