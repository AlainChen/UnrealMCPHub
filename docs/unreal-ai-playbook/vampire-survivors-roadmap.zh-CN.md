# 通往 `vampire-survivors-v1` 的推进路线

## 当前判断

现在不适合直接把 `vampire-survivors-v1` 当成一次性任务去跑。

更现实的路径是先让下面几条能力稳定：

- `benchmark-preflight` 稳定
- `benchmark-lite` 能稳定产出 artifact
- `L1 sandbox` 能完成受控写入和验证
- `L2` 能完成一个最小真实 gameplay loop
- 运行时矩阵能说明哪些域和工具是真的可用

## 路线分层

### Stage 0: 环境前门稳定

目标：
- benchmark 前置检查可重复
- artifact 可保存
- 结果可比较

通过标准：
- preflight 连续多次返回结构化结果
- 失败时能明确是 connectivity、timeout 还是 environment

### Stage 1: L0 Smoke

目标：
- 证明链路通

重点：
- MCP 可达
- metadata 查询成功
- 至少一个 execution 查询成功

通过标准：
- `benchmark-lite --level L0 --scenario smoke-connectivity-v1` 能产出 artifact
- `recommended_next_level` 能明确给出 `L1` 或维持 `L0`

### Stage 2: L1 Sandbox Prototype

目标：
- 证明 agent 可以在边界内完成一次小改动

重点：
- 只在 `/Game/__Sandbox/` 内工作
- 创建一个最小资产或 Actor
- 做最小验证
- 输出结构化总结

通过标准：
- 有真实改动
- 有验证
- 没越界
- 有 artifact

### Stage 3: L2 Restricted Gameplay Loop

目标：
- 证明 agent 能完成一个真实但很小的 Unreal gameplay loop

重点：
- 一段极小 C++ 或真实运行逻辑
- 一个敌人或目标
- 一个命中、重叠或状态变化
- 一条可验证反馈

通过标准：
- 编译成功
- PIE 中能证明行为
- artifact 中能记录文件、验证和剩余风险

### Stage 4: 拆分 Heavy Benchmark

不要直接做完整 `vampire-survivors-v1`，而是先拆成模块：

- `3C`
- `combat`
- `wave`
- `progression`
- `ui`
- `cook/package`

每个模块都先做最小可通过版本。

### Stage 5: 整合成 `vampire-survivors-v1`

当下面条件成立时，再冲完整 heavy benchmark：

- `L0` 稳
- `L1` 稳
- `L2` 稳
- runtime validation matrix 已经不是大面积 `known-risk`
- benchmark artifact 链可复用

## 最小执行顺序

1. 先把 `benchmark-preflight` 和 `benchmark-lite` 跑顺。
2. 做一次真实 `L1 sandbox`。
3. 再做一次最小 `L2 gameplay loop`。
4. 再把 `vampire-survivors-v1` 拆成子任务。
5. 最后才合成完整 heavy benchmark。

## 当前最优先的阻塞点

1. execution query 的稳定性
2. domain 真实可调用能力与静态工具列表之间的落差
3. 本机性能导致的低吞吐问题
4. artifact 和 benchmark 结果还需要更多标准化样本

## 结论

当前最合理的推进方式不是“直接做 Vampire Survivors”，而是：

`preflight -> benchmark-lite -> sandbox -> gameplay loop -> heavy benchmark modules -> final integration`

## Long-Term

在当前这套 Launcher 版本验证链之外，更远期的规划应当单独看待，不和短期 benchmark 收口混在一起。

### 1. 从 Launcher Workflow 走向 Source Engine Workflow

当前验证主要建立在 Launcher 版 Unreal 上，但大型项目里更常见的是：

- 自编译 Unreal Engine
- 项目级 engine fork
- 团队维护的 engine patch
- 更复杂的编译、符号和 crash 分析路径

长期需要补齐的方向包括：

- source-built engine 的识别与配置
- 多引擎版本与多引擎布局管理
- 针对源码版引擎的 compile / cook / package 流程
- 针对源码版引擎的 crash、symbol 与日志分析

### 2. 从二进制资产操作走向中间表示与结构化审查

当前工作流已经能约束 AI 在 Unreal 中做事，但大型项目里还需要一层更可审计的结构：

- 任务意图表示
- 资产变更摘要
- 引用关系变化摘要
- 地图或 gameplay 结构变化摘要
- 比 Unreal 二进制 diff 更稳定的中间数据结构

长期目标不是让 AI 直接改所有二进制资产，而是先产生结构化意图和变更摘要，再映射到 Unreal 内容。

### 3. 从直接触碰 C++/资产走向 Middleware Gameplay Layer

大型项目里，AI 未必适合长期直接操作：

- 低层 C++
- 蓝图二进制资产
- 复杂地图状态

更现实的远期方向可能是：

- C++ 负责底层系统
- Unreal 资产负责承载与表现
- 中间脚本层负责高频玩法逻辑

可探索的方向包括：

- AngelScript
- Lua
- 项目自定义 DSL
- 其他适合 gameplay iteration 的脚本层

这样做的价值在于：

- 更容易 diff
- 更容易 review
- 更容易回滚
- 更适合 AI 高频生成和重构

### 4. 工业化采用的真正目标

远期目标不只是“benchmark 能跑通”，而是：

- 多项目可复用
- 多成员可复制
- 权限边界清晰
- 变更审查可执行
- benchmark 能作为回归门槛
- 失败可恢复，结果可归档

也就是说，当前 benchmark 验证链是入口，而不是终点。
