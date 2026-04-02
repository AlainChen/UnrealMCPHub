# Internal Project Agent Guide

## 目的

当本地 agent 需要接入一个内部 Unreal 项目时，最缺的通常不是“再多一个工具”，而是：

- 这个项目是谁
- agent 默认能做什么，不能做什么
- 应该先从哪里开始
- 碰到常见任务时该查哪份文档

因此更推荐给 agent 一套“两层入口”：

1. 一页快速使用指南
2. 一组按 topic 拆开的项目文档

快速使用指南负责首轮上手，topic 文档负责按需深入。

---

## 核心建议

### 不要只给一份超长总文档

如果把所有内部项目知识都堆进一份大文档：

- agent 首次读取成本高
- 真正常用的信息不容易被优先命中
- 项目变化后维护成本高

更好的做法是：

- 用一份 `project-quickstart` 说明“先怎么做”
- 用 topic 文档说明“遇到这类问题时看什么”

### 也不要只给 topic，缺少入口

如果只有很多 topic，没有 quickstart：

- agent 会知道有很多资料
- 但不知道首次接项目时先读哪几个
- 也不知道默认允许的操作边界

所以 quickstart 仍然必须存在。

---

## 推荐分层

对于 `UnrealMCPHub + UnrealRemoteMCP`，我建议分成 5 层：

| 层级 | 存放位置 | 作用 |
|------|----------|------|
| 全局产品 skill | `UnrealMCPHub/skills/use-unrealhub/` | 教 agent 如何使用 Hub 与 RemoteMCP |
| 全局团队 workflow | `UnrealMCPHub/skills/team-unreal-workflow/` | 教 agent 在团队协作中如何收敛风险、验证、交付 |
| 项目 quickstart | `<ProjectRoot>/.unrealhub/skills/project-quickstart/` | 教 agent 如何开始使用某一个内部项目 |
| 项目 topics | `<ProjectRoot>/.unrealhub/topics/` 或 `<ProjectRoot>/.unrealhub/skills/project-quickstart/references/` | 给 agent 项目专项知识 |
| 项目记忆 / seed | `<ProjectRoot>/.unrealhub/memory-seeds/` | 存稳定事实，不存工作流方法 |

一句话：

- `skill` 负责方法
- `topic` 负责专项知识
- `memory` 负责事实

---

## Quickstart 里必须写什么

项目 quickstart 不应该是架构论文，而应该是一份 agent 首次接项目时的操作说明。

建议固定写这 8 类内容：

### 1. 项目身份

- 项目名
- 主 `.uproject` 路径
- 主要引擎版本
- 主要模块或游戏类型

### 2. 默认目标

告诉 agent 这个项目里最常见的工作是什么，例如：

- 读状态和排查问题优先
- Sandbox 原型优先
- 默认不动 production map
- 编译和启动通过 Hub 完成

### 3. 默认边界

这是最关键的一段。

至少要写清楚：

- 默认允许修改哪些目录
- 默认禁止修改哪些目录
- 哪些 map 只能读不能写
- 哪些操作必须先请人确认
- 是否允许直接改 C++

### 4. 首轮上手流程

给 agent 一个固定顺序，例如：

1. `get_project_config`
2. `hub_status`
3. `discover_instances`
4. `manage_instance`
5. `ue_status`
6. `ue_list_domains`
7. 再决定读状态、编译还是启动

### 5. 常见任务入口

建议列出 5 到 8 个项目里最高频的任务入口，例如：

- 编译与启动
- PIE 验证
- Sandbox 原型
- UI 调试
- Gameplay 日志排查
- 地图验证

每项只需要告诉 agent：

- 优先用哪些工具
- 验证最少要做什么

### 6. 验证最小集合

每个项目都应该告诉 agent：

- 内容任务最少验证什么
- 代码任务最少验证什么
- session-disrupting 操作后怎么 reconnect

### 7. 停止条件

告诉 agent 哪些情况不要继续硬做，例如：

- 碰到 production map 写入
- 要改共享插件
- 要重构公共 C++ 模块
- 要处理不确定的版本迁移

### 8. Topic 索引

quickstart 最后一定要列出 topic 名单，告诉 agent：

- 想看编译细节读哪个 topic
- 想看 UI 规则读哪个 topic
- 想看 benchmark 规则读哪个 topic

---

## Topic 应该怎么拆

我建议 topic 不按“部门目录”拆，而按 agent 任务形态拆。

更适合的 topic 集合通常是：

### 1. `project-overview`

项目目标、模块结构、主地图、主玩法循环、主要路径约定。

### 2. `scope-and-rules`

默认可写范围、禁区、共享资源规则、需要人工确认的场景。

### 3. `compile-and-launch`

如何编译、如何启动、常见失败、日志看哪里。

### 4. `pie-and-validation`

PIE 怎么开，验证最小集合是什么，截图和日志怎么留证据。

### 5. `content-conventions`

资产命名、目录规范、sandbox 约定、测试地图约定。

### 6. `gameplay-hotspots`

这个项目中最常被改动的系统入口，例如：

- Enemy
- Ability
- UI HUD
- Inventory
- Wave loop

### 7. `ui-debug`

UMG、Slate、HUD、Widget Blueprint 的专项说明。

### 8. `benchmark-or-demo`

如果项目带 benchmark、demo map、showcase 流程，就单独成 topic。

### 9. `handoff`

任务结束时该如何汇报：

- 要列哪些文件或资产
- 要给哪些验证结论
- 要标哪些风险

---

## 对 UnrealMCPHub + UnrealRemoteMCP 的具体落位建议

### 放在 Hub 里的内容

这些更适合放进 `UnrealMCPHub` 的全局 skill 或参考文档：

- Hub/RemoteMCP 边界
- 通用工作流
- 通用验证 discipline
- benchmark discipline
- crash/reconnect 常识
- 全局 help topic

原因：

- 这些是跨项目稳定复用的
- 不该随着单个项目变化而分叉

### 放在项目里的内容

这些更适合放进项目根目录下的 `.unrealhub/`：

- 项目 quickstart
- 项目 topic 文档
- sandbox 路径约定
- 特定 map 风险说明
- 特定模块热点说明
- 项目专项验证方法

原因：

- 这些是项目特有知识
- 可能带内部路径、命名约定、团队规范
- 不应该沉淀到全局公开 skill 中

### 放在 RemoteMCP 里的内容

不要把“项目使用指南”放进 `UnrealRemoteMCP`。

`RemoteMCP` 更适合承载：

- editor-native tool contract
- domain 能力说明
- session-disrupting 语义
- tool 参数与返回契约

项目 onboarding 不属于插件层。

---

## 推荐目录结构

```text
<ProjectRoot>/
  .unrealhub/
    skills/
      project-quickstart/
        SKILL.md
        references/
          project-overview.md
          scope-and-rules.md
          compile-and-launch.md
          pie-and-validation.md
          content-conventions.md
          gameplay-hotspots.md
          ui-debug.md
          handoff.md
    topics/
      project-overview.md
      scope-and-rules.md
      compile-and-launch.md
      pie-and-validation.md
      content-conventions.md
      gameplay-hotspots.md
      ui-debug.md
      handoff.md
    memory-seeds/
      stable-facts.json
      known-risks.json
      benchmark-baselines.json
```

如果你希望尽量复用现有 skill 结构，推荐优先用：

- `.unrealhub/skills/project-quickstart/SKILL.md`
- `.unrealhub/skills/project-quickstart/references/*.md`

如果你希望做更轻量的 topic 浏览，再补：

- `.unrealhub/topics/*.md`

---

## Quickstart 的建议写法

项目 quickstart 最好保持下面的结构：

```md
# Project Quickstart

## 项目是谁

## 默认目标

## 默认边界

## 首轮上手流程

## 常见任务入口

## 验证最小集合

## 必须停下来的场景

## Topics
```

关键原则：

- 尽量用短句
- 不写大段背景故事
- 优先写操作边界和首轮路径
- 把深层知识留给 topic

---

## Topic 的建议写法

每个 topic 最好都遵守同样的头部结构：

```md
# Topic Name

## 适用场景

## 先做什么

## 推荐工具顺序

## 常见坑

## 验证最小集合

## 不要做什么
```

这样 agent 读取 topic 时，能更快抓到真正可执行的信息。

---

## 如果以后想接到 help(topic)

现有 `UnrealMCPHub` 的 `help(topic)` 是从全局 [use-unrealhub](../../../skills/use-unrealhub/SKILL.md) 中拆 topic。

如果未来你想让 agent 能直接按项目 topic 查询，推荐的扩展方向是：

1. 先保留全局 `help(topic)` 语义不变
2. 再增加 project-aware 的入口，例如：
   - `project_help(topic="compile-and-launch")`
   - 或 `help(topic="project:compile-and-launch")`
3. 查询顺序建议为：
   - 先查项目 topic
   - 没有则回退到全局 topic

这样最稳，也不会破坏现在已有的全局帮助体系。

---

## 最小落地版本

如果你现在只想先快速落地，不要一次写太多。

第一版只需要准备：

1. `project-quickstart/SKILL.md`
2. `scope-and-rules.md`
3. `compile-and-launch.md`
4. `pie-and-validation.md`
5. `handoff.md`

这 5 份已经足够让本地 agent 在内部项目里“安全开工”。

---

## 一句话结论

最推荐的方案不是只给 agent 一份长指南，也不是只给零散 topic。

而是：

- 用 `project-quickstart` 解决首次进入项目的问题
- 用项目 topics 解决专项知识查询的问题
- 用 `UnrealMCPHub` 保持全局 workflow 和全局 help
- 用 `.unrealhub/` 承载项目私有知识

这样最符合 `UnrealMCPHub + UnrealRemoteMCP` 当前的边界，也最利于后续做 project-aware help、skill 和长期记忆。
