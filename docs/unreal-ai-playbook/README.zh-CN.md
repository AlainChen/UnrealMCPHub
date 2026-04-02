# Unreal AI Playbook

这个目录现在只保留三类内容：

- 当前仍然有效的工作流、规则和阶段总结
- 值得长期保留的 benchmark / capability validation 结论
- 值得继续下沉成 reference / skill 的稳定模式

更探索性、更过程化的 Gym 材料已经移出主阅读路径，统一放进 `archive/`。

另外，面向 Epic 官方示例工程的“可玩性验证”工作，已经迁移到独立 workspace：

- `C:\Users\alain\Documents\Playground\UnrealPlayableValidation`

这样 `UnrealMCPHub` 继续承担平台、流程、总结和参考资料的角色，不再混入新的 sample-specific 开发计划。

## Current

建议按下面顺序阅读：

1. `workflow.md`
2. `rules.md`
3. `todo.md`
4. `current-status-summary.zh-CN.md`
5. `skills-candidate-map.zh-CN.md`
6. [`../../skills/analyze-unreal-project-stack/SKILL.md`](../../skills/analyze-unreal-project-stack/SKILL.md)

其中：

- `workflow.md`
  说明当前默认工作流
- `rules.md`
  说明边界和约束
- `todo.md`
  说明近期、中期、长期待办
- `current-status-summary.zh-CN.md`
  说明当前已经完成了什么，以及 benchmark / MCP / playbook 到了什么阶段
- `skills-candidate-map.zh-CN.md`
  说明哪些内容已经适合沉淀成 reference 或 skill
- [`../../skills/analyze-unreal-project-stack/SKILL.md`](../../skills/analyze-unreal-project-stack/SKILL.md)
  说明如何分析内部 Unreal 项目的结构、技术栈、引擎耦合、配置流和 source-of-truth

## Snapshot

- `snapshot/README.zh-CN.md`
- `snapshot/fork-status-summary.zh-CN.md`

如果 `Snapshot` 与当前状态冲突，以 `Current` 和仓库实际状态为准。

## Archive

归档目录保存：

- 早期过程稿
- 已被吸收的中间版本
- 已移出主路径的 Gym 探索材料

入口：

- `archive/README.zh-CN.md`
- `archive/gym/README.zh-CN.md`

## Artifacts

`artifacts/` 是本地运行证据目录，不是长期主阅读路径的一部分。

使用建议：

- 先读 `Current`
- 只在核对截图、日志、JSON 结果或边界测试证据时再进入 `artifacts/`
- 对外共享前，确认本地绝对路径、端口和机器标识都已经脱敏
