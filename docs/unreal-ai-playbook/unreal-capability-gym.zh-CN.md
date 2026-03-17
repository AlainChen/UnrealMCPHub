# Unreal Capability Gym

## 定位

`Unreal Capability Gym` 不是另一个单点 benchmark。

它的目标是建立一套按能力域组织的 showcase 与验证框架，用来回答：
- AI 在不同 Unreal 3D 能力域里能做到什么程度
- 这些能力更适合 `observe`、`modify` 还是 `create`
- 哪些能力已经适合展示，哪些还处在研究和试错阶段

Gym 更像一张能力地图，而不是一个单独分数。

## 当前作用

Gym 当前承担 4 个作用：

1. 展示作用  
   用高质量 3D 场景、sample 或内部测试工程，做可视化的前后对比。

2. 替代性测试  
   测试 AI 在 `lighting`、`space`、`feedback`、`combat`、`animation` 等域里的协作和局部替代能力。

3. 任务分层  
   把任务拆成 `observe / modify / create`，避免一开始就只测试“从零生成”。

4. 图文报告输入  
   为后续图文可行性报告提供统一的证据结构。

## 为什么当前放在 Docs

Gym 现在更适合放在 `docs/unreal-ai-playbook/`，而不是直接做成独立 skill。

原因是：
- 现在它更像研究框架和展示框架
- 能力域、showcase 选型、报告结构还在快速迭代
- 还没有收敛成稳定的执行入口

更合理的演进方式是：
1. 先在 docs 里稳定 Gym 的结构、brief 和证据格式
2. 等某些 Gym 任务变成高频、稳定、可复用的执行入口
3. 再把执行层内容吸收到 `team-unreal-workflow` 的 references 里

## Gym 结构

### 能力域

当前第一批核心域固定为 5 个：
- `3d-lighting-readability`
- `3d-space-readability`
- `3d-gameplay-feedback`
- `3d-combat-encounter`
- `3d-animation-locomotion`

这 5 个构成当前的 `Baseline Track`。

### 任务层次

每个域按三层组织：
- `observe`
  只读分析、拆解、总结、评审
- `modify`
  在已有高质量场景上做局部修改
- `create`
  在明确约束下做新的小范围内容或功能

当前阶段优先 `modify`。

### 证据结构

每个 Gym 任务至少要沉淀：
- 一句任务定义
- 所属能力域
- `observe / modify / create`
- 使用的工程或场景
- 一组 before / after 图
- 一段验证结果
- 一段风险说明
- 一个 readiness 判断

## Baseline Track

当前默认路线是 `Baseline Track`。

它的原则是：
- 先把核心 3D 能力域都跑一遍
- 每个域先做一个轻量、可复用、可展示的 baseline
- 先建立广度，再决定哪些域值得 advanced
- 在至少 3 个 baseline 跑通之前，不进入重型 advanced 路线

当前顺序：
1. `Gym-01` `Lighting Readability Modify`
2. `Gym-02` `3D Space Readability Modify`
3. `Gym-03` `3D Gameplay Feedback Micro Pass`
4. `Gym-04` `3D Combat Encounter Modify`
5. `Gym-05` `3D Animation / Locomotion Modify`

这样做的原因：
- 更容易形成完整能力地图
- 不会把 Gym 绑死在某一个 benchmark 原型上
- 更利于控制机器负载和验证风险

## 第一阶段目标

当前第一阶段目标很明确：

1. 完成 `Gym-01` 的第一份 before / after 证据包
2. 启动 `Gym-02`
3. 为 `Gym-03` 到 `Gym-05` 补齐 baseline brief
4. 等至少 3 个域有第一版 showcase 之后，再评估 `Advanced Track`

## 图文可行性报告结构

建议后续每次 Gym 报告都按这 5 段来组织：

1. 总览  
   本次验证了什么能力域。

2. Showcase 载体  
   用了哪个项目或场景，为什么选它。

3. 任务与修改  
   做了哪些 `modify`，改动边界是什么。

4. 证据  
   before / after、日志、运行结果、验证结论。

5. 判断  
   readiness、风险、是否适合继续 advanced。

## 与 Team Workflow 的关系

- `team-unreal-workflow`
  负责日常工作规则、安全边界、验证方式、任务模板。

- `Capability Gym`
  负责不同能力域的 showcase、试验、图文报告和 readiness 判断。

两者是上下游关系，不是重复关系：
- team workflow 负责“怎么安全地做”
- gym 负责“在哪些 3D 能力域里做到了什么程度”
