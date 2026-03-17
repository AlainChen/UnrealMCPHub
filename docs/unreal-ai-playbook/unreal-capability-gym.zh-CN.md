# Unreal Capability Gym

## 定位

`Unreal Capability Gym` 不是另一个单点 benchmark。

它的目标是建立一套按能力域组织的 showcase 和验证框架，用来回答：
- AI 在不同 Unreal 能力域里到底能做什么
- 它更适合 `observe`、`modify` 还是 `create`
- 哪些能力已经适合展示，哪些还只是研究阶段

它更像一张能力地图，而不是单个分数。

## 当前预期

Gym 当前承担 4 个作用：

1. 展示作用  
   用高质量 Unreal sample、showcase scene 或内部测试项目，做可视化前后对比。
2. 替代性测试  
   测试 AI 在 `combat`、`lighting`、`level-design`、`ui`、`technical-art`、`vfx` 等域里的替代或协作能力。
3. 任务分层  
   把任务拆成 `observe / modify / create`，避免一上来就只测“从零生成”。
4. 图文报告输入  
   为后续图文可行性报告提供统一结构和证据模板。

## 为什么它现在更适合放在 Docs

目前 Gym 更适合放在 `docs/unreal-ai-playbook/`，而不是单独做成 skill。

原因是：
- 它现在更像研究框架和展示框架
- 能力域、showcase 选型、报告结构还在快速迭代
- 还没有收敛成稳定的执行入口

更合理的演进方式是：

1. 先在 docs 里稳定 Gym 的结构、任务模板和证据格式
2. 等某些 Gym 任务变成高频、稳定、可复用的执行入口
3. 再把执行层子集吸收到 `team-unreal-workflow` 的 references 里

## 结构

### 一层：能力域

第一批建议聚焦这 6 个域：

- `3d-lighting-readability`
- `3d-space-readability`
- `3d-gameplay-feedback`
- `3d-combat-encounter`
- `3d-animation-locomotion`
- `3d-vfx-ta`

### 二层：任务类型

每个域都按三层任务组织：

- `observe`
  只读分析、结构拆解、风险总结
- `modify`
  在现有高质量样本上做局部修改
- `create`
  在约束下新增一个局部内容或功能

当前第一阶段建议优先做 `modify`，因为它最适合展示 AI 参与真实项目修改的能力，也更容易做前后对比。

### 三层：证据结构

每个 Gym 任务至少要沉淀：

- 一句话任务定义
- 所属能力域
- `observe / modify / create`
- 使用的 showcase 项目或场景
- 一张或多张前后对比图
- 一段验证结果
- 一段风险和边界说明
- 一个 readiness 判断

## 第一阶段实施建议

### Gym-01 Lighting Readability Modify

目标：
- 在一个已有 3D 场景中做一次局部灯光和可读性改造

推荐任务：
- 从白天切到黄昏或夜景
- 做一次 focal area readability pass
- 做一个小型 cinematic mood pass

最小证据包：
- 同机位前后对比图
- lighting intent 说明
- 场景可读性结论
- 性能或烘焙风险说明
- readiness 结论

### Gym-02 3D Space Readability Modify

目标：
- 在现有 3D 场景上做一次小范围空间、动线或 encounter readability 调整

推荐任务：
- 调整玩家视线引导
- 微调 cover、POI 或动线节点
- 强化某一段空间的可读性和进入节奏

最小证据包：
- 同路径或同机位前后对比图
- 修改点列表
- 可读性与动线结论
- 风险说明
- readiness 结论

### Gym-03 3D Gameplay Feedback Micro Pass

目标：
- 在不重做玩法系统的前提下，增强一个局部交互或状态反馈

### Gym-04 3D Combat Encounter Modify

目标：
- 在已有战斗样本上做一轮局部战斗或敌人节奏 modify

### Gym-05 3D Animation / Locomotion Modify

目标：
- 在已有 3D 样本上做一次动作、移动或 locomotion 层面的局部改造

## 图文可行性报告结构

建议结构：

1. 总览
   一句话说明本次报告验证了什么能力域。
2. Showcase 概览
   用了哪个 Unreal 项目或样本场景，为什么选它。
3. 任务矩阵
   每个域做了哪些 `observe / modify / create`。
4. 前后对比
   关键图像、运行结果、日志或 package 证据。
5. 结论
   哪些域已经适合展示，哪些域还只适合研究试错。

## 与 Team Workflow 的关系

- `team-unreal-workflow`
  负责日常工作的规则、验证和审查
- `Capability Gym`
  负责能力域展示、showcase 试验和报告框架

它们不是重复关系，而是上下游关系：
- team workflow 负责“怎么安全地做”
- gym 负责“我们在不同能力域里能做到什么程度”

## 当前第一阶段结论

当前已经锁定第一批 pilot domain：

- `3d-lighting-readability`
- `3d-space-readability`

下一步默认按这个顺序推进：

1. 先用 `Gym-01 Lighting Readability Modify` 形成第一份 showcase 任务和证据包
2. 再用 `Gym-02 3D Space Readability Modify` 形成第二份 showcase 任务和证据包
3. 最后把两者合并成第一版图文可行性报告
