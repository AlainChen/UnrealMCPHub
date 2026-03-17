# Fork 状态摘要

## 当前结论

当前这个 fork 已经形成了一套比较清晰的结构：

- `main` 作为稳定 fork 主线
- `codex/lab` 作为当前主要工作分支
- `codex/team-workflow` 作为文档与方法论起始分支
- `codex/pr-discovery-fallback` 作为面向上游的小型修复分支

同时，`vampire-survivors-v1` 风格 benchmark 已经达到“可展示跑通”的程度，并已在仓库内沉淀为文档、artifact 规范与 README 说明。

## 当前主要分支

### `main`

用途：

- 作为你的稳定 fork 主线
- 吃到上游同步
- 保留 fork 级别认可的 README、文档和结构调整

当前状态：

- 已同步上游 `upstream/main`
- 已包含最新 README fork/benchmark 说明

### `codex/lab`

用途：

- 作为当前主要开发与实验分支
- 承载 benchmark tooling、workflow runner、验证脚本、README 演进和实验性改动

当前状态：

- 已同步最新 `main`
- 已推送到你的 fork
- 适合作为后续继续工作的默认分支

### `codex/team-workflow`

用途：

- 作为 team workflow、规则、研究文档和项目分析的起始分支
- 更偏历史文档分支和方法论基线

当前状态：

- 内容已被后续主线和实验分支吸收
- 现在更适合作为参考分支保留，而不是高频继续开发

### `codex/pr-discovery-fallback`

用途：

- 保留 discovery fallback 相关的小型、上游友好修复
- 方便未来单独向上游提 PR

当前状态：

- 仍然有保留价值
- 不用于日常主要开发

## 可选分支

### `codex/benchmark`

用途：

- 只有在你明确想把 benchmark-only 的迭代单独隔离时才建议启用

当前状态：

- 目前不是主要工作分支
- 可继续保留，但无需强行使用

## 当前 benchmark 进度

已完成：

- `L0` preflight / connectivity
- `L1` sandbox prototype
- `L2` restricted gameplay loop
- 冷编译验证
- `BuildCookRun`
- Windows 包体启动验证

已沉淀到仓库中的内容：

- benchmark 路线图
- benchmark artifact 模板
- artifact 边界说明
- benchmark 跑通报告
- README 中的 benchmark status

没有并入仓库的内容：

- 外部 Unreal 测试工程
- benchmark gameplay 原型代码与地图
- 包体目录
- 原始本地日志

## 当前关键提交

### `main`

- `e84bc16` `docs: update README fork workflow and benchmark status`

### `codex/lab`

- `0f02ce1` `docs: update README fork workflow and benchmark status`
- `ea0f4e1` `merge: sync codex/lab with upstream main`
- `3df1659` `docs: add benchmark pass report and artifact guidelines`
- `3011fae` `feat: add benchmark lite runner and roadmap`
- `dc62ca2` `feat: save benchmark preflight artifacts`
- `86a3f17` `feat: add benchmark preflight runner`

## 推荐的后续默认工作方式

建议默认按照下面的方式继续：

1. 日常工作默认在 `codex/lab`
2. 稳定后再决定是否合回 `main`
3. 只有小而通用的修复，才考虑走 `codex/pr-discovery-fallback`
4. `codex/team-workflow` 保留为方法论参考，不必频繁继续堆改动

## 一句话总结

如果以后你只想记住一个默认入口，那就是：

`main` 是稳定基线，`codex/lab` 是当前主工作线，`codex/pr-discovery-fallback` 是上游小 PR 线。
