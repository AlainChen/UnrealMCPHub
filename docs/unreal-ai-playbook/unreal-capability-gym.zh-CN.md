# Unreal Capability Gym

## 目标

`Unreal Capability Gym` 的目标不是替代单一 benchmark，而是补上一套更适合展示、比对和分域评估的能力框架。

它解决的是下面这类问题：

- 只跑一个 `vampire-survivors-v1`，很难看清 AI 在不同 Unreal 领域里的强弱
- 只做小型 benchmark，又不足以展示 Unreal 的复杂能力
- 大型项目里，团队更关心“AI 能在什么能力域里替代、协作或加速”，而不是只关心一个总分

所以 `Capability Gym` 更适合：

- 选用高质量 Unreal showcase 或 sample project
- 在样本上做局部修改、扩展和重构
- 按能力域测试 AI 的可替代性和协作性
- 形成一套可展示、可比较、可复用的能力地图

## 设计原则

### 1. 先按能力域分类，不按项目名分类

不要把 gym 做成“某几个 demo 项目的集合”，而要做成“能力域矩阵”。

推荐的一级能力域：

- `combat`
- `level-design`
- `level-art`
- `lighting`
- `technical-art`
- `vfx`
- `ui-ux`
- `animation`
- `ai-behavior`
- `tools-automation`
- `optimization`
- `integration`

### 2. 每个能力域按三层任务组织

每个能力域都拆成三种任务，而不是只做“从零生成”：

- `observe`
  只读分析与拆解
- `modify`
  在现有高质量样本上做局部修改
- `create`
  在约束下创建一个小型新增内容

这样更接近真实团队工作流，也更利于展示 AI 的上限和边界。

### 3. 先做 showcase-oriented benchmark，再谈统一评分

Capability Gym 的第一阶段重点不是全都打分，而是：

- 先证明哪些域可做
- 先形成可靠任务样本
- 先产出可展示的图文报告

评分可以后置。

## 推荐的第一批能力域

近期最适合先落的 6 个域：

### 1. `combat`

关注：

- 武器逻辑
- 命中反馈
- 敌人行为
- 生存循环

适合的 modify/create 样本：

- 新增一套攻击模式
- 调整敌人组合
- 改造伤害与击退反馈

### 2. `level-design`

关注：

- 路径组织
- 遭遇设计
- 空间引导
- 可玩性节奏

适合的 modify/create 样本：

- 改局部关卡路径
- 新增一段 encounter
- 调整 POI、cover、spawn 关系

### 3. `lighting`

关注：

- mood
- time-of-day
- readability
- composition

适合的 modify/create 样本：

- 改成黄昏或夜景版本
- 做一段 cinematic lighting pass
- 提升战斗区域可读性

### 4. `technical-art`

关注：

- shader / material 调整
- runtime 可视反馈
- procedural setup
- 工具化 TA 工作流

适合的 modify/create 样本：

- 改材质参数表现
- 做简单 procedural placement/variation
- 做 runtime visual feedback 原型

### 5. `vfx`

关注：

- 命中特效
- 技能特效
- 环境氛围特效
- 性能边界

适合的 modify/create 样本：

- 新增命中 FX
- 调整已有 Niagara 效果
- 给场景补局部氛围 FX

### 6. `ui-ux`

关注：

- HUD
- 交互反馈
- 信息层级
- prototype iteration

适合的 modify/create 样本：

- 改 HUD 结构
- 新增提示或交互层
- 做 benchmark/ability 专用调试 UI

## 每个能力域的标准记录结构

建议每个域都按同一个模板记：

### 1. 能力目标

- 这个域在 Unreal 项目里解决什么问题
- 为什么值得 AI 参与

### 2. Showcase 载体

- 使用哪个 Unreal sample / demo / test scene
- 为什么选择它

### 3. 任务类型

- `observe`
- `modify`
- `create`

### 4. 验证方式

- 编译/运行验证
- 截图对比
- 日志证据
- package/cook 结果
- 人工 review 结论

### 5. 风险点

- 是否容易碰二进制资产污染
- 是否依赖 PIE
- 是否容易遇到性能问题
- 是否需要更强人工审美判断

## 推荐的图文报告结构

Capability Gym 最后应该落成一份图文并茂的可行性报告，而不是只有文字清单。

推荐结构：

### 1. 总览页

- 一句话说明 Gym 是什么
- 一张能力矩阵图
- 三条关键结论

### 2. 能力地图

按能力域画成矩阵，例如：

| Domain | Observe | Modify | Create | Current Readiness |
|---|---|---|---|---|
| combat | yes | yes | partial | high |
| lighting | yes | partial | partial | medium |
| vfx | yes | partial | no | low |

### 3. 每个域的 showcase 页

每页至少包括：

- 目标
- showcase 项目或场景
- 一到两个典型任务
- 当前可行性判断
- 风险

### 4. 当前阶段结论

- 哪些域适合近期重点推进
- 哪些域适合只做 observe/modify，不适合 create
- 哪些域对 AI 的价值更偏“协作”，而不是“替代”

## Showcase 选择标准

Capability Gym 不应该随便拿一个项目来测。

推荐的选择标准是：

### 1. 视觉或玩法质量足够高

样本项目最好本身就具有展示价值，这样 AI 的修改结果才有比较意义。

### 2. 结构清晰

优先选择：

- 模块边界清楚
- 地图规模可控
- 依赖不过度复杂

否则能力评估会被项目结构噪声淹没。

### 3. 支持局部修改

样本项目要允许我们做：

- 局部 relight
- 局部 combat tuning
- 局部 UI 调整
- 局部 FX 或 TA 任务

而不是每次都要全项目重构。

### 4. 适合生成图文证据

最好的 showcase 项目应该能方便产出：

- 前后截图
- 运行日志
- gameplay 片段
- package 结果

## 实施节奏

Capability Gym 不建议一口气全面铺开。

推荐按 3 个阶段推进。

### Phase A: 建立 Gym 框架

目标：

- 固定能力域
- 固定任务层级
- 固定 artifact 模板
- 固定展示报告结构

产出：

- capability gym 主文档
- 第一版能力矩阵
- 第一版 showcase 选择原则

### Phase B: 跑通第一批域

目标：

- 先在 3 到 5 个最有代表性的域里做出可靠样本

推荐顺序：

1. `combat`
2. `lighting`
3. `level-design`
4. `ui-ux`
5. `technical-art` 或 `vfx`

产出：

- 每个域至少 1 个 `modify` 任务样本
- 至少 1 份图文可行性结论
- 每个域的风险和 readiness 标记

### Phase C: 形成展示型能力地图

目标：

- 把若干 showcase 任务汇总成一套真正可展示的“AI Unreal 能力图”

产出：

- capability matrix
- showcase pages
- domain-by-domain readiness summary
- 对内决策或对外展示材料

## 近期推荐的第一批落地顺序

如果只选最值当的第一批，我建议按下面的次序来：

### Step 1

先完成 `combat` 和 `lighting`

原因：

- 一个偏玩法，一个偏画面
- 展示效果最直观
- 很容易体现 AI 的“修改能力”而不是只做分析

### Step 2

再做 `level-design` 和 `ui-ux`

原因：

- 这两个域很适合测试 AI 的结构化修改能力
- 又不会像大规模 TA/VFX 那样一开始就陷入复杂依赖

### Step 3

最后再补 `technical-art / vfx`

原因：

- 这两个域更依赖项目具体实现
- 更适合作为第二阶段扩展，而不是第一阶段入口

## 每个 Gym 任务的最小产出要求

建议每个任务都至少要有：

1. 一句任务定义
2. 一张前后对比图或一段运行证据
3. 一段结果摘要
4. 一条风险结论
5. 一个 readiness 判断

## Readiness 建议分级

建议对每个能力域用统一分级：

- `high`
  已能稳定做 observe 和 modify，且有清晰展示价值
- `medium`
  能完成部分任务，但稳定性或质量仍有明显波动
- `low`
  暂时只适合 explore 或 observe，不适合当展示主项

## 当前建议

如果现在要继续往前推进，不要先补更多总论，而是直接做：

1. `Gym-01 Combat Modify`
2. `Gym-02 Lighting Modify`
3. 用这两个任务先产出第一版 capability showcase 报告

## 近期可做的第一批 Gym 任务

这部分最适合直接放进 `codex/lab` 继续推进。

### Gym-01 Combat Modify

- 在当前生存循环原型上新增一套攻击变化
- 目标是看 AI 在 combat tuning 上的能力

### Gym-02 Lighting Modify

- 选一个简单 arena 或 sample map
- 让 AI 做一版 mood relight
- 验证结果用截图和运行效果说明

### Gym-03 Level Design Modify

- 让 AI 对一个现成样本场景做局部 encounter 或 flow 调整
- 重点不是重做地图，而是局部修改质量

### Gym-04 UI Modify

- 基于现有 HUD 做一轮 benchmark/ability 视角的 UI 调整
- 看 AI 在 UMG/调试信息组织上的表现

### Gym-05 TA / VFX Micro Task

- 选一个很小的 FX 或材质反馈任务
- 测试 AI 在技术美术配合上的上限和风险

## 当前最适合放在哪条分支

建议先放在：

- `codex/lab`

原因：

- 它明显属于实验层
- 会频繁迭代分类方式、样本项目和任务定义
- 现在还不应该过早固化进 `main`

## 后续演进方向

如果 Capability Gym 跑顺了，后面可以继续变成：

- team workflow 的一个正式参考章节
- benchmark 之外的能力地图
- 团队选型和岗位协作评估工具
- 对外展示 AI Unreal 能力范围的报告

## 一句话总结

`Unreal Capability Gym` 不是替代 benchmark，而是把 benchmark 从“单个任务验证”扩展成“按能力域组织的展示与评估体系”。
