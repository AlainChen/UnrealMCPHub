# Reference And Skill Candidates

## Purpose

本文档回答两个问题：

- 哪些内容已经足够稳定，适合沉淀成 reference 或 skill
- 哪些内容仍然更适合留在归档或后续专门 workspace 中继续演化

## Recommended Reference Candidates

### 1. RemoteMCP Safe Usage

建议沉淀位置：
- `team-unreal-workflow/references/`

理由：
- `RemoteMCP P0/P0.5` 的 `risk_tier`、`session-disrupting`、`reconnect_required` 等语义已经比较稳定
- 这部分已经足够指导人机协作和 agent workflow

### 2. Evidence Capture Discipline

建议沉淀位置：
- `team-unreal-workflow/references/`

理由：
- “tool success 不等于 evidence 有效”已经被多轮验证
- 固定机位、受控场景、单 editor 实例这些规则已经足够稳定

### 3. Benchmark Validation Discipline

建议沉淀位置：
- `team-unreal-workflow/references/`

理由：
- `benchmark-preflight`
- `benchmark-lite`
- packaged showcase-ready pass

这些已经构成了一套可复用的 benchmark 收口方法。

### 4. External Runner Design Notes

建议沉淀位置：
- `team-unreal-workflow/references/`

理由：
- 目前已经明确 PowerShell client 只是临时壳
- 后续外部 runner、typed client、Go/TypeScript 外层控制层都有明确方向

## Recommended Skill Candidates

当前最适合逐步转成 skill 或 skill reference 的有：

- `RemoteMCP safe usage`
- `Evidence capture discipline`
- `Benchmark validation discipline`

这些内容的特点是：

- 已经跨多次验证复用
- 不是一次性的实验结论
- 与具体某一个 Gym 实例解耦

## Not Ready Yet

以下内容当前不建议直接 skillize：

- figure-rich 报告本身
- 过程性的 Gym brief / findings
- animation / locomotion showcase 路线
- 更重的 Blueprint / dynamic combat / animation graph 路线

原因是这些内容仍然依赖：

- 特定 showcase 载体
- 特定 agent 路径
- 尚未稳定的展示资产或工程环境

## Practical Rule

如果一项内容同时满足下面三条，就可以考虑进入 reference 或 skill：

1. 已跨多次验证重复出现
2. 不依赖某个单一 showcase 场景
3. 对未来 workflow 有直接指导意义
