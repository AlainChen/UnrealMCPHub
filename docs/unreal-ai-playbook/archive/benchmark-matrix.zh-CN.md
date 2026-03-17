# Benchmark 测试矩阵

## 目的

把 benchmark 从单一大场景，拆成一组可以逐步推进的测试矩阵。

## 维度

### 维度 A：连接稳定性

- MCP 是否稳定
- Hub 是否稳定
- discover 是否稳定
- 多次重复是否一致

### 维度 B：施工能力

- 只读分析
- sandbox 写入
- widget 原型
- 小型 C++ feature

### 维度 C：验证能力

- compile
- PIE
- logs
- package

### 维度 D：报告能力

- 是否有清晰 summary
- 是否说明风险
- 是否有后续建议

## 最小矩阵

| 编号 | 场景 | 重点 |
|------|------|------|
| M01 | smoke-connectivity-v1 | 链路 |
| M02 | sandbox-prototype-v1 | 安全写入 |
| M03 | cpp-gameplay-loop-v1 | 小型真实功能 |
| M04 | vampire-survivors-v1 | 完整重型 benchmark |

## 推荐顺序

1. `M01`
2. `M02`
3. `M03`
4. `M04`

不要跳级，除非目标就是压力测试。
