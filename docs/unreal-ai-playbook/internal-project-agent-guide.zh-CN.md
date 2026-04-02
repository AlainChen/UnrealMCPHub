# Internal Project Agent Guide

## 目的

当你需要把一个内部 Unreal 项目接入 `UnrealMCPHub + UnrealRemoteMCP` 时，这份文档回答：

- 应该给 agent 准备什么知识层
- skill、topic、memory 应该怎么分
- quickstart 里必须写什么
- topic 应该怎么拆
- 第一版最小落地应该交付什么

**这份文档是写给"搭建项目知识层的人"看的，不是 agent 在工作中自动加载的 skill。**

---

## 何时用这份文档

| 场景 | 是否适用 |
|------|---------|
| 第一次把某个内部项目接入 Hub，不知道从哪开始 | ✅ |
| 想知道 quickstart 里必须包含哪些内容 | ✅ |
| 想拆 topic，不确定按什么维度分 | ✅ |
| 想知道哪些内容放 skill，哪些放 memory | ✅ |
| 想理解 Hub 全局 skill 和项目 skill 的边界 | ✅ |
| 日常使用已有项目知识层完成具体任务 | ❌ 请回到 `project-quickstart/SKILL.md` |

---

## 核心模型：两层入口

```
project-quickstart     ←  agent 首次进入项目时读这个
    └─ topics/         ←  agent 遇到具体问题时读这个
```

**不要只给一份超长总文档**（读取成本高、维护成本高、命中率低）。

**也不要只有 topics，缺少入口**（agent 不知道首次读哪几个，不知道默认操作边界）。

两层入口缺一不可。

---

## 推荐知识分层

| 层级 | 存放位置 | 负责什么 |
|------|----------|---------|
| 产品全局 skill | `UnrealMCPHub/skills/` | Hub + RemoteMCP 通用工作流 |
| 团队全局 skill | `UnrealMCPHub/skills/`（标注 team） | 跨项目可复用的团队约定 |
| 项目 quickstart | `<ProjectRoot>/.unrealhub/skills/project-quickstart/` | 这个项目怎么开始 |
| 项目 topics | `<ProjectRoot>/.unrealhub/topics/` | 这个项目的专项知识 |
| 项目 memory seeds | `<ProjectRoot>/.unrealhub/memory-seeds/` | 这个项目的稳定事实 |

口诀：**skill 存方法，topic 存专项知识，memory 存事实。**

---

## 常见误区

| 误区 | 正确做法 |
|------|---------|
| 把所有知识塞进一个 quickstart.md | quickstart 只写入口与边界，深层知识留给 topic |
| 把项目 skill 放进 RemoteMCP 插件仓库 | 项目 skill 跟着项目走，放在 `.unrealhub/` |
| 把"每次编译先 clean"这类工作流写进 memory | 工作流写进 skill 或 reference，memory 只存事实 |
| 把"sandbox 地图是 AI_TestMap"写进 skill | 这是事实，应该进 memory seed |
| 只有 quickstart，没有任何 topic | 碰到具体任务 agent 无处深入 |

---

## Quickstart 必须写的 8 类内容

### 1. 项目身份

```
项目名：
主 .uproject 路径：
引擎版本：
主要目标（Game / Editor / Server）：
```

### 2. 默认目标

agent 在这个项目里最常做的事。示例：

- 读状态和排查问题优先
- sandbox 原型优先
- 编译和启动通过 Hub 完成
- 默认不动 production map

### 3. 默认边界（最关键）

必须明确写清楚：

| 边界 | 具体规定 |
|------|---------|
| 默认可写目录 | 例：`/Game/__Sandbox/` |
| 默认禁止目录 | 例：`/Game/Maps/Production/`、`/Game/UI/Core/` |
| 必须请示才能动的 | 例：共享插件、引擎配置 |
| 是否允许直接改 C++ | 是 / 否 / 需要审批 |
| 是否允许删除资产 | 是 / 否 / 需要审批 |

### 4. 首轮上手流程

固定的工具调用顺序，让 agent 不用猜：

```
1. get_project_config
2. hub_status
3. discover_instances → manage_instance
4. ue_status → ue_list_domains
5. 根据上面的结果决定：读状态 / 编译 / 启动 / 分析
```

### 5. 常见任务入口（5–8 个）

| 任务 | 优先工具 | 最少验证 |
|------|---------|---------|
| 编译与启动 | `build_project`, `launch_editor` | 编译日志无 error |
| PIE 验证 | `ue_call` + PIE 工具 | PIE 开启 + 截图 |
| sandbox 原型 | `ue_call` 创建 Blueprint | 编译 + 存在确认 |
| 日志排查 | `hub_status`, `ue_status` | 日志摘要输出 |
| UI 调试 | RemoteMCP UMG 工具 | PIE 截图对比 |

### 6. 验证最小集合

```
内容任务：Blueprint 编译 + 资产存在确认 + 日志无 error
代码任务：编译通过 + 至少一项功能验证
session-disrupting 操作后：ping → get_editor_state → get_current_level
```

### 7. 停止条件

agent 遇到以下情况必须停下、不得继续自主操作：

- 需要写入 production map
- 需要修改共享插件
- 需要重构公共 C++ 模块
- 需要处理不确定的版本迁移
- 合法操作路径不明确

### 8. Topic 索引

quickstart 最后一定要列出 topic 清单，附一句话说明用途：

```
- compile-and-launch.md   — 编译失败、启动问题、日志看哪里
- pie-and-validation.md   — PIE 怎么开，验证最小集合，截图留证
- scope-and-rules.md      — 哪里能写，哪里不能碰，shared asset 规则
- lua-runtime.md          — Lua reload 路径，入口，绑定机制（如适用）
```

---

## Topic 分拆建议

按 agent **任务形态**拆，不按部门目录拆。

| Topic | 核心内容 | 触发场景 |
|-------|---------|---------|
| `project-overview` | 目标、模块、主地图、玩法循环、路径约定 | 首次了解项目 |
| `scope-and-rules` | 可写范围、禁区、shared 资源规则 | 任何写操作前 |
| `compile-and-launch` | 编译方法、启动、常见失败、日志位置 | 编译 / 启动问题 |
| `pie-and-validation` | PIE 开启、验证集合、截图留证 | 验证任务 |
| `content-conventions` | 资产命名、目录规范、sandbox 约定 | 创建新资产 |
| `gameplay-hotspots` | 最常被改动的系统入口列表 | 功能开发 |
| `ui-debug` | UMG / Slate / HUD 专项说明 | UI 相关任务 |
| `handoff` | 任务结束时交付格式、验证结论、风险标注 | 每次任务结束 |

**每个 topic 建议统一格式：**

```md
## 适用场景
## 先做什么
## 推荐工具顺序
## 常见坑
## 验证最小集合
## 不要做什么
```

---

## 推荐目录结构

```
<ProjectRoot>/
  .unrealhub/
    skills/
      project-quickstart/
        SKILL.md
        references/
          scope-and-rules.md
          compile-and-launch.md
          pie-and-validation.md
          content-conventions.md
          gameplay-hotspots.md
          ui-debug.md
          handoff.md
    topics/           ← 可选，与 references/ 内容相同但按需单独引用
    memory-seeds/
      stable-facts.json         ← sandbox 路径、已验证事实
      known-risks.json          ← 禁区、high-risk 资产
      benchmark-baselines.json  ← 已通过 benchmark 基线
```

---

## 第一版最小落地清单

不要一次写太多。第一版只需要交付这 5 份：

| 文件 | 作用 |
|------|------|
| `project-quickstart/SKILL.md` | 项目身份 + 边界 + 首轮流程 + topic 索引 |
| `scope-and-rules.md` | 可写目录、禁区、审批规则 |
| `compile-and-launch.md` | 编译 / 启动 / 常见失败 |
| `pie-and-validation.md` | 验证路径 + 截图 + 最小集合 |
| `handoff.md` | 任务结束交付格式 |

**这 5 份足够让 agent 在内部项目里安全开工。**

---

## 内容放置原则速查

| 内容类型 | 放哪里 |
|---------|-------|
| Hub / RemoteMCP 通用工作流 | `UnrealMCPHub/skills/` 全局 skill |
| 项目首次进入流程 | `.unrealhub/skills/project-quickstart/SKILL.md` |
| 项目专项知识（编译、PIE、UI…） | `.unrealhub/topics/` 或 `references/*.md` |
| sandbox 路径、已验证事实 | `.unrealhub/memory-seeds/stable-facts.json` |
| 已知禁区、high-risk 资产 | `.unrealhub/memory-seeds/known-risks.json` |
| 编辑器工具能力说明 | `UnrealRemoteMCP`（不在这里） |
| 过程性实验记录、Gym 笔记 | 不应进入 quickstart，放 archive |
