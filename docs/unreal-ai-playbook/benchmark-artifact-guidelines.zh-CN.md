# Benchmark Artifact 说明

## 目标

这份说明用于明确：

- 什么是 benchmark artifact
- 哪些 artifact 适合进入仓库
- 哪些 artifact 只能留在本地或外部工程
- 如何在不泄露敏感信息的前提下保存“已跑通”证据

## Artifact 分层

建议把 benchmark artifact 分成三层。

### 1. 仓库内 artifact

这类 artifact 适合进入 `UnrealMCPHub` 仓库：

- preflight JSON
- benchmark-lite JSON
- 脱敏后的 runtime validation matrix
- benchmark 路线图
- benchmark 完成报告
- artifact 模板
- 失败原因分类和方法总结

这些内容的特点是：

- 与具体个人机器弱绑定
- 能被复用
- 不包含大体积二进制
- 不暴露本地路径、账号、主机名

### 2. 外部工程 artifact

这类 artifact 应留在 Unreal 测试工程或单独 demo 仓库中：

- `.uproject`
- `Source/`
- `.umap`
- `.uasset`
- 具体 benchmark 地图和玩法代码

这些内容属于“验证样本工程”，不应直接混入工具仓库。

### 3. 本地证据 artifact

这类 artifact 一般不提交，只作为本地证明材料：

- 包体目录
- 本地运行日志原文
- CrashReporter 原始文件
- 本机截图、录屏原文件
- Cook 和 package 的大体积中间产物

## 推荐提交到仓库的内容

建议提交：

- 一份 benchmark 结果报告
- 一份 artifact 说明
- 一份 benchmark-lite 或 preflight 样本 JSON
- 一份脱敏后的关键日志摘要

不建议提交：

- 完整包体
- 完整运行日志原文
- 外部测试工程源码
- 本地绝对路径快照

## 脱敏规则

在保存或提交 artifact 前，至少检查下面这些项：

- 本地绝对路径已脱敏
- 用户名、主机名已脱敏
- 本地 loopback 地址只保留“本地端点”语义，不保留不必要细节
- 登录标识、账户标识、token、设备信息不进入仓库
- Crash 日志只保留必要问题摘要，不直接贴原文

## 本次 benchmark 推荐保留的证据形式

针对这次 `vampire-survivors-v1` benchmark，最推荐保留的是：

1. 跑通报告
2. benchmark artifact 说明
3. preflight / benchmark-lite 样本
4. 一段脱敏后的关键运行日志摘录
5. 包体成功生成这一事实说明

## 本次 benchmark 不推荐直接并入仓库的内容

不建议直接提交到 `UnrealMCPHub` fork：

- 外部 Unreal sandbox 测试工程
- 该工程中的 C++ gameplay 原型代码
- map 与资源文件
- package 结果目录
- 原始本地日志

原因是这些内容会把：

- 工具仓库
- 测试游戏工程
- 本地实验痕迹

混在一起，后续维护会变得很重。

## 推荐目录策略

### 仓库内

建议继续放在：

- `docs/unreal-ai-playbook/`
- `docs/unreal-ai-playbook/artifacts/`

### 仓库外

建议保留在：

- 外部 Unreal sandbox 工程
- 单独的 benchmark demo 项目
- 或单独的演示归档目录

## 一个简化判断标准

如果某个 artifact 满足下面任一条件，就不要直接进这个仓库：

- 体积大
- 强依赖某台机器
- 是具体游戏样本工程内容
- 包含本地敏感信息
- 未来上游仓库不可能接受

## 本次结论

本次 benchmark 的正确沉淀方式应当是：

- 仓库内保留“方法、模板、报告、脱敏 artifact”
- 仓库外保留“具体 Unreal 工程、包体和原始运行证据”
