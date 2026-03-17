# Benchmark Artifact 模板

这份模板用于规范化每一轮 benchmark 产出，避免只留下零散聊天记录。

## 1. 基本信息

- 运行日期
- benchmark 等级
- scenario 名称
- agent 或客户端名称
- 模型标识
- 项目标识
- 环境标识

不要直接写入：
- 本地绝对路径
- 私有仓库地址
- 个人机器标识
- 原始 token、账号名、主机名

## 2. Preflight 结果

至少记录：

- MCP 是否可达
- 是否识别到活动 Unreal 实例
- metadata 查询是否成功
- execution 查询是否成功
- 本轮是否允许继续 benchmark

## 3. 工具可用性概况

至少记录：

- 顶层工具列表
- domain 列表
- 每个 domain 的工具数量

## 4. 运行时验证矩阵

对每个采样工具记录：

- domain
- tool 名称
- sample call
- 状态：`validated` / `unvalidated` / `known-risk`
- 结果摘要
- 超时或失败说明

## 5. 结果总结

至少记录：

- 本轮达到的 benchmark 等级
- 主要 blocker
- 人工干预次数
- 推荐的下一个 benchmark 等级
- 推荐的下一步最小修复

## 6. 脱敏规则

保存 artifact 前检查：

- 本地路径已脱敏
- 本地地址或 loopback 信息只保留必要描述
- 机器特有标识已泛化
- 只保留比较 benchmark 所需的最小环境信息

## 7. 可直接复用的表格骨架

### Preflight

| 项目 | 结果 | 备注 |
|---|---|---|
| MCP 可达 |  |  |
| 活动实例识别 |  |  |
| metadata 查询 |  |  |
| execution 查询 |  |  |
| 允许继续 benchmark |  |  |

### Validation Matrix

| Domain | Tool | Sample Call | 状态 | 结果摘要 | 备注 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

### Outcome

| 项目 | 内容 |
|---|---|
| benchmark 等级 |  |
| major blockers |  |
| 人工干预次数 |  |
| 推荐下一等级 |  |
| 推荐下一步修复 |  |
