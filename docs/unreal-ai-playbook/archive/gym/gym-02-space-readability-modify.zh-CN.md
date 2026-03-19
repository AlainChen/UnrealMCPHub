# Gym-02 Space Readability Modify

## Status

- `Domain`: `3d-space-readability`
- `Task Type`: `modify`
- `Track`: `Baseline`
- `Status`: `baseline-ready`

## Current State

- `Gym-02` now has a valid automated baseline pass on a controlled scene
- `before/after` images are no longer identical and reflect an actual space-readability change
- the validated path uses:
  - controlled scene construction
  - fixed capture camera
  - neutral lighting preset
  - actor transform changes for space hierarchy
- the current result is good enough to count as a baseline Gym validation
- remaining improvement is optional showcase polish rather than baseline viability

## Recorded Evidence

- `gym02-baseline-before-v4.png`
- `gym02-baseline-after-v4.png`

See also:
- `gym-02-baseline-findings.zh-CN.md` for the recorded findings, rejected evidence, and reporting guidance

## Goal

在一个稳定 3D 场景上，自动完成一次最小的空间可读性修改，并留下可归档的 before/after 证据。

`Gym-02` 不是完整关卡设计重做，也不是 encounter 系统重构。

它的目标是验证：
- AI 能否对局部空间、动线或 focal point 做清晰的 modify
- 当前 workflow 是否能承接这类 3D scene readability 任务
- 哪些修改可以作为之后 `Gym-03` 到 `Gym-05` 的前置能力

## Scope

允许修改：
- 局部 path / entry rhythm
- 一处 focal point 或 POI 的可读性
- 一组小范围遮挡、引导或空间层级
- 直接服务于局部空间理解的少量 lighting/supporting props

本轮不做：
- 大范围关卡重建
- 完整 traversal 系统
- 新的重型 gameplay loop
- 复杂 narrative setpiece

## Relationship To Gym-01

`Gym-01` 偏向画面与 focal readability。

`Gym-02` 偏向：
- 空间组织
- 局部路径清晰度
- POI / focal hierarchy
- 玩家观察时的一眼可读性

推荐顺序：
1. 先完成 `Gym-01`
2. 再启动 `Gym-02`

## Recommended Tool Path

仍然优先依赖已经完成验证的 `RemoteMCP` P0/P0.5：

- map lifecycle
- scene/testbed construction
- evidence capture
- health / reconnect baseline

推荐执行顺序：

1. health check
2. load or verify the target scene
3. query current focal actors or key scene anchors
4. perform one small readability pass
5. capture before/after
6. summarize risk and readiness

## Baseline Pass

本轮 baseline 默认只做两个动作：

### Modify A: Local Path Clarity

调整一小段入口、路径或局部通道，让空间导向更清楚。

### Modify B: Focal Hierarchy Pass

强化一个 POI、入口、目标区或展示区的空间层级，让视线优先级更清晰。

## Evidence Bundle

最小证据包固定为：

- task brief
- before image
- after image
- execution summary
- readability note
- risk note
- readiness conclusion

## Known Dependencies

`Gym-02` 成功与否，高度依赖：
- `Gym-01` 证明的 before/after capture 流程
- scene/testbed construction 是否足够稳定
- 是否能在不大幅重建场景的情况下做小范围空间修改

## Success Criteria

本轮完成的最低标准：

1. 有一组同机位 before/after
2. 局部 path 或 focal hierarchy 有明确变化
3. 修改范围局限在 baseline 允许的最小空间
4. 有一条 readiness 结论

## Hand-Off

完成后应回填：

- 结果摘要
- 证据链接或文件名
- 风险结论
- 是否准备进入 `Gym-03`
