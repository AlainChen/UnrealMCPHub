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
4. [vampire-survivors-benchmark-pass.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\vampire-survivors-benchmark-pass.zh-CN.md)
5. [benchmark-artifact-guidelines.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\benchmark-artifact-guidelines.zh-CN.md)
6. [benchmark-artifact-template.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\benchmark-artifact-template.zh-CN.md)
7. [unreal-capability-gym.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\unreal-capability-gym.zh-CN.md)
   当前 Gym 的默认推进路线是 `Baseline Track`
8. [vampire-survivors-roadmap.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\vampire-survivors-roadmap.zh-CN.md)
9. [gym/README.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\README.zh-CN.md)
   当前已经启动的 Gym 实例

## Snapshot

- [runtime-validation-matrix.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\runtime-validation-matrix.zh-CN.md)
- [fork-status-summary.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\fork-status-summary.zh-CN.md)

如果 Snapshot 与当前状态冲突，应以当前 `README`、`todo` 和实际仓库状态为准。

## Archive

`archive/` 保存的是早期过程稿和中间版本。

建议按这个顺序回看：
1. [archive/benchmark-research-report.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\benchmark-research-report.zh-CN.md)
2. [archive/benchmark-lite-plan.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\benchmark-lite-plan.zh-CN.md)
3. [archive/benchmark-matrix.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\benchmark-matrix.zh-CN.md)
4. [archive/change-buckets-and-branching.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\change-buckets-and-branching.zh-CN.md)
5. [archive/skill-architecture-v2.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\skill-architecture-v2.zh-CN.md)
6. [archive/skill-system.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\archive\skill-system.md)

## Team Workflow 与 Capability Gym

- `team-unreal-workflow`
  是项目级控制层，负责把通用 Hub 能力收敛成团队可执行、可审查、可复用的工作方式。

- `Capability Gym`
  当前更适合放在 playbook 文档层，而不是直接做成独立 skill。它本质上是能力域分类、showcase 设计和图文可行性报告框架。

后续如果 Gym 的任务模板、评分方式和执行入口稳定下来，再把执行层内容吸收到 `team-unreal-workflow` 的 references 里会更合理。
