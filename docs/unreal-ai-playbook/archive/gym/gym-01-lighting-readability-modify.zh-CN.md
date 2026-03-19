# Gym-01 Lighting Readability Modify

## Status

- `Domain`: `3d-lighting-readability`
- `Task Type`: `modify`
- `Track`: `Baseline`
- `Status`: `baseline-ready`

## Current State

- `camera-anchored capture` is now working and can capture the controlled scene reliably
- the baseline path is now sufficient to support the next Gym items
- the only remaining improvement is showcase quality: the current `neutral_day -> golden_hour` difference is not yet visually strong enough to count as an ideal hero before/after pair
- `Gym-01` should currently be treated as:
  - `lighting tool capability`: validated
  - `camera-anchored capture path`: validated
  - `baseline infrastructure`: validated
  - `showcase-quality evidence`: optional follow-up improvement

See also:
- `gym-01-baseline-findings.zh-CN.md` for the recorded findings, rejected evidence, and reporting guidance

## Goal

在一个轻量、稳定、可重复的 3D 场景上，自动完成一次最小 `lighting/readability` 修改，并留下可归档的 before/after 证据。

这不是 advanced lighting showcase，也不是完整天气系统验证。

它是第一条 baseline gym：
- 轻量
- 可见
- 全自动
- 可重复
- 可展示

## What This Pass Is Trying To Prove

`Gym-01` 需要回答三件事：

1. AI 能否通过当前 workflow 自动完成一次最小 lighting/readability modify
2. 这次 modify 是否足够可见，能作为 showcase 证据
3. 当前自动化链路的边界到底落在效果层、证据层，还是生命周期层

## Scope

允许修改：
- directional light
- skylight
- fog / atmosphere
- 少量直接服务于可读性的 scene presentation 参数

本轮不做：
- 完整天气系统
- 重型 post process lookdev
- 大范围关卡重做
- gameplay 系统新增
- 依赖重型 sample 的高级展示

## Recommended Tool Path

优先使用已经在 `RemoteMCP` 侧完成验证的 P0/P0.5 基础能力：

- map lifecycle
- scene/testbed construction
- evidence capture
- `ping / get_editor_state / get_current_level`

执行顺序建议：

1. health check
2. 确认当前 map / scene
3. 进行一轮最小 lighting modify
4. capture before/after
5. summarize risk and readiness

高风险长链 `ue_run_python` 只作为兜底，不作为默认路径。

## Baseline Pass

这一轮 baseline 默认只做两个动作：

### Modify A: Time-of-Day Shift

把当前场景从中性白天切到更有气氛感的时段版本，例如：
- golden hour
- late dusk
- cool overcast

### Modify B: Readability Pass

增强一个 focal area、入口区、主展示区或主要观察方向的可读性。

## Evidence Bundle

本轮最小证据包固定为：

- task brief
- before image
- after image
- execution summary
- validation note
- risk note
- readiness conclusion

如果执行失败，也需要留档：

- failure stage
- tool chain used
- whether the path is currently a known-risk path
- whether the issue belongs to effect logic, evidence capture, or session lifecycle

## Known Baseline Foundation

目前可以依赖的底座能力：

- `RemoteMCP` P0:
  - map lifecycle
  - scene/testbed construction
  - evidence capture
  - health baseline
- `RemoteMCP` P0.5:
  - `map_unsaved`
  - `map_not_found`
  - `map_already_exists`
  - schema-level invalid arguments decision

当前最关键的边界不是“完全没有工具”，而是：
- lighting preset 还没有正式结构化
- post process wrapper 还没有正式结构化
- map transition 是 `session-disrupting`，不是无缝操作

## Success Criteria

本轮完成的最低标准：

1. 有一组同机位 before/after
2. mood 或 focal readability 有明显变化
3. 自动化链路可复现
4. 有一条 readiness 结论

## Hand-Off

完成后应回填：

- 结果摘要
- 证据链接或文件名
- 风险结论
- 是否进入 `Gym-02`
