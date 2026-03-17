# Benchmark Lite 计划

## 目标

在正式跑 `vampire-survivors-v1` 之前，先建立一个可重复、可比较、可诊断的轻量 benchmark。

## 为什么要先做 Lite

因为当前最大的风险不是“AI 一定做不出完整游戏”，而是：

- 客户端不稳定
- MCP 链路偶发失效
- 工具能力边界不清楚
- 任务太重时失败原因不容易拆分

Lite 的价值是先把这些问题拆开。

## 推荐测试包

### Lite-0：连接与状态

使用：
- [smoke-connectivity-v1.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\ue-benchmark\scenarios\smoke-connectivity-v1.md)

通过标准：
- 连接成功
- 状态读取成功
- 最小调用成功

### Lite-1：安全写入

使用：
- [sandbox-prototype-v1.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\ue-benchmark\scenarios\sandbox-prototype-v1.md)

通过标准：
- sandbox 内创建成功
- 有验证
- 有总结

### Lite-2：小型 C++ 回路

使用：
- [cpp-gameplay-loop-v1.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\ue-benchmark\scenarios\cpp-gameplay-loop-v1.md)

通过标准：
- C++ 编译成功
- PIE 中有真实行为
- 输出变更摘要和限制

## 记录模板

每次 Lite run 建议至少记录：

- 客户端
- MCP 连接方式
- 工程路径
- 使用场景
- 是否成功
- 失败点
- 人工干预次数
- 后续修复建议

## 升级规则

只有 Lite-0、Lite-1、Lite-2 都相对稳定后，再进入正式 benchmark。
