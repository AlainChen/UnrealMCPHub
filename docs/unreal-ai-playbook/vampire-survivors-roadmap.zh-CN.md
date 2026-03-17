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
