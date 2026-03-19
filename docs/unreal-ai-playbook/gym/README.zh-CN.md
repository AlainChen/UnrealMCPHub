# Unreal Capability Gym Instances

这个目录存放的是已经从 Gym 模板进入“具体执行”的实例。

每个实例至少应包含：
- 一个任务 brief
- 一个证据或报告骨架
- 一组最小验证项

## 当前默认路线

当前 Gym 的默认推进方式是 `Baseline Track`：
- 先完成 `Gym-01`
- 再启动 `Gym-02`
- 再为 `Gym-03` 到 `Gym-05` 补齐 baseline brief

阅读建议：
1. 先读 [..\README.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\README.zh-CN.md)
2. 再读 [..\unreal-capability-gym.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\unreal-capability-gym.zh-CN.md)
3. 然后按当前实例顺序进入具体 Gym 文档
4. 只有在需要核对截图、JSON 结果或边界证据时，再进入 `..\artifacts\`

## 当前实例

- [showcase-selection.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\showcase-selection.zh-CN.md)
- [gym-project-engineering.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-project-engineering.zh-CN.md)
- [gym-01-lighting-readability-modify.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-01-lighting-readability-modify.zh-CN.md)
- [gym-01-baseline-findings.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-01-baseline-findings.zh-CN.md)
- [gym-02-space-readability-modify.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-02-space-readability-modify.zh-CN.md)
- [gym-02-baseline-findings.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-02-baseline-findings.zh-CN.md)
- [gym-03-gameplay-feedback-modify.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-03-gameplay-feedback-modify.zh-CN.md)
- [gym-tooling-backlog.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\gym-tooling-backlog.zh-CN.md)
- [mcp-tooling-review.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\mcp-tooling-review.zh-CN.md)
- [hub-vs-remotemcp-boundary.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\hub-vs-remotemcp-boundary.zh-CN.md)
- [hub-only-foundation-plan.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\hub-only-foundation-plan.zh-CN.md)

## 上传注意

如果后续要对外上传 Gym 文档或图文报告：
- 本地绝对路径应统一做 mask
- 本机端口、用户名、机器特征不要直接保留在对外材料里

## Artifacts

`artifacts/` 目录当前承担的是运行证据和边界留档：
- 本地截图
- JSON 结果
- preflight / benchmark-lite / gym 的阶段性输出

它不是 Gym 主文档本身。

推荐做法：
- Gym brief、结论、方法论写在 `docs/unreal-ai-playbook/` 和 `gym/`
- `artifacts/` 只保留配套证据
- 对外整理报告时，只挑需要的证据引用，不把整个 `artifacts/` 当阅读入口

## Archive

已归档的探索版本：
- [archive/gym-combat-modify-exploration.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\gym\archive\gym-combat-modify-exploration.zh-CN.md)
