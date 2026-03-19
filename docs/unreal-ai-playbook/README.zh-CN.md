# Unreal AI Playbook

本目录按三层组织：
- `Current`
  当前仍然有效、应优先阅读和维护的文档
- `Snapshot`
  某一阶段状态快照，保留上下文，但不作为唯一事实来源
- `Archive`
  过程稿、研究稿、已被吸收的中间版本

## Current

建议阅读顺序：
1. [workflow.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\workflow.md)
2. [rules.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\rules.md)
3. [todo.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\todo.md)
4. [unreal-capability-gym.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\unreal-capability-gym.zh-CN.md)
   当前 Gym 的默认推进路线是 `Baseline Track`
5. [gym/README.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\README.zh-CN.md)
   当前已经启动的 Gym 实例
6. [gym-feasibility-report.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym-feasibility-report.zh-CN.md)
   当前 Gym 的完整总结性报告
7. [skills-candidate-map.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\skills-candidate-map.zh-CN.md)
   当前哪些内容已经适合下沉成 skills / references

如果你的目标是继续改 `RemoteMCP` 或理解 Gym 自动化边界，建议在读完上面的 `Current` 后，再补读：
- [gym/hub-vs-remotemcp-boundary.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\hub-vs-remotemcp-boundary.zh-CN.md)
- [gym/gym-tooling-backlog.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-tooling-backlog.zh-CN.md)
- [gym/gym-status-summary.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-status-summary.zh-CN.md)

## Snapshot

- [snapshot/README.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\snapshot\README.zh-CN.md)
- [snapshot/fork-status-summary.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\snapshot\fork-status-summary.zh-CN.md)

如果 Snapshot 与当前状态冲突，应以当前 `README`、`todo` 和实际仓库状态为准。

## Artifacts

`artifacts/` 目录是本地运行证据和阶段性输出，不是主阅读路径的一部分。

阅读建议：
- 先读 `Current`
- 再按需进入 `gym/`
- 只有在需要核对运行截图、JSON 结果或边界测试证据时，再看 `artifacts/`

如果要对外分享：
- 先确认路径、端口、机器标识都已脱敏
- 不把本地临时截图和调试 JSON 当成长期文档入口

## Archive

`archive/` 保存的是早期过程稿和中间版本。

当前已归档：
- [archive/README.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\README.zh-CN.md)
- [archive/benchmark-research-report.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\benchmark-research-report.zh-CN.md)
- [archive/change-buckets-and-branching.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\change-buckets-and-branching.zh-CN.md)
- [archive/skill-system.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\skill-system.md)

## Team Workflow 与 Capability Gym

- `team-unreal-workflow`
  是项目级控制层，负责把通用 Hub 能力收敛成团队可执行、可审查、可复用的工作方式。

- `Capability Gym`
  当前更适合放在 playbook 文档层，而不是直接做成独立 skill。它本质上是能力域分类、showcase 设计和图文可行性报告框架。

后续如果 Gym 的任务模板、评分方式和执行入口稳定下来，再把执行层内容吸收到 `team-unreal-workflow` 的 references 里会更合理。
