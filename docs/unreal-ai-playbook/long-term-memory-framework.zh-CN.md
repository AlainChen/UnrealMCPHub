# Unreal 长期记忆框架设计

最后更新：2026-03-23

本文基于当前 `UnrealMCPHub + UnrealRemoteMCP` 的公开设计来规划一版长期记忆框架，并同时回答：

- 长期记忆应该放在哪里
- 哪些能力属于 `Hub`
- 哪些能力属于 `RemoteMCP`
- 全局 skill 和项目 skill 应该怎么分层
- skill 与 memory 应该怎样协作，而不是互相替代

本文的核心结论是：

- **长期记忆应由 `UnrealMCPHub` 主持久化与检索**
- **`UnrealRemoteMCP` 应只负责提供编辑器内证据、快照、原子事实与结构化工具**
- **skill 是程序化工作流知识，不是事实数据库**
- **项目 skill 应贴着目标 Unreal 项目放置，Hub 负责发现、索引和调度**

---

## 1. 现有边界回顾

基于当前仓库设计，系统边界应保持如下：

### 1.1 UnrealRemoteMCP

定位：

- 运行在 Unreal Editor 内
- 提供 editor-native capability
- 负责游戏线程内工具执行
- 提供结构化读写能力、健康检查、地图/场景/截图等基础能力

适合承载：

- 结构化编辑器工具
- 编辑器内快照
- 编辑器内状态查询
- 证据采集
- 最小健康语义

不适合承载：

- 跨会话长期记忆
- 项目级知识库
- 团队工作流编排
- 大量策略逻辑
- team/project skill 注册中心

### 1.2 UnrealMCPHub

定位：

- 运行在 Unreal Editor 外
- 负责项目配置、编译、启动、发现、恢复、代理、跨会话状态
- 是 AI client 看到的主入口

适合承载：

- 长期记忆存储
- 跨项目索引
- 证据归档
- 检索与排序
- 记忆写入策略
- skill 注册与优先级解析
- benchmark / artifact / report 归档
- 访问控制与 policy

### 1.3 Skill

定位：

- 是 workflow knowledge，不是 engine capability
- 是“如何使用现有 tool/resource 完成某类任务”的操作说明
- 本质上是程序化经验，而不是事实本体

适合承载：

- 任务分解
- 推荐工具顺序
- 写入前检查
- 验证步骤
- 风险约束
- 证据采集规范

不适合承载：

- 当前地图事实
- 当前项目状态
- 已验证 benchmark 结果明细
- 资产依赖关系
- 运行时日志本体

---

## 2. 设计目标

长期记忆框架应首先服务于以下现实目标：

1. 让 agent 在多会话、多实例、多天跨度下保持项目上下文连续性。
2. 让 benchmark、验证、截图、日志、风险结论可以沉淀，而不是只停留在聊天历史。
3. 让记忆可审计、可追溯、可失效，而不是不断堆积“似是而非”的事实。
4. 让项目 skill 可以读取项目事实，但不直接替代事实层。
5. 让 `RemoteMCP` 继续保持“编辑器能力层”的简洁边界，不把长期 orchestration 再塞回插件里。

---

## 3. 非目标

第一版长期记忆框架不应追求以下内容：

- 把所有聊天都自动转成长期记忆
- 在 `RemoteMCP` 内直接维护 knowledge graph
- 让 skill 成为万能插件系统
- 做一个重型向量数据库平台先于工作流价值落地
- 让 agent 无审查地把运行时观察全部固化为真相

---

## 4. 记忆分层模型

建议把记忆严格分为五层，而不是混成一个桶。

### 4.1 Session Memory

范围：

- 当前 agent 会话
- 当前 UE 实例
- 当前任务窗口

内容：

- 临时笔记
- 当前假设
- 当前操作 history
- 短期待办

现状映射：

- 当前 `StateStore.notes`
- 当前 `call_history`

保存位置建议：

- 继续留在 Hub 的状态层
- 但需要增加“可晋升”为长期记忆候选项的机制

### 4.2 Instance Memory

范围：

- 某个项目实例
- 某个 editor 进程或 MCP endpoint

内容：

- crash 记录
- 异常重连模式
- 某实例近期不稳定特征

保存位置建议：

- 仍由 Hub 管理
- 与 `InstanceState` 绑定，但不要和全局长期记忆混写

### 4.3 Project Memory

范围：

- 某一个 `.uproject`
- 某团队对这个项目的长期知识

内容：

- 安全 sandbox 路径
- 已知危险目录
- 推荐测试地图
- 已验证 capture 机位
- benchmark 基线
- 常见故障和修复策略
- 已确认的约束和决策

这是最重要的一层。

### 4.4 Global Memory

范围：

- 跨项目复用
- 通用 Unreal/Hub/RemoteMCP 工作规律

内容：

- 通用 reconnect 规律
- 通用证据采集规范
- 通用 build / launch / popup 经验
- 通用 benchmark 验证准则

它不应包含项目私有事实。

### 4.5 Artifact-backed Memory

这是“记忆有证据”的关键层。

内容：

- 日志文件引用
- 截图引用
- before/after 对比
- crash dump / report 索引
- benchmark 结果文件
- 运行摘要 JSON

长期记忆本身应尽量轻量；大对象保存在 artifact 目录，memory 只保存引用和摘要。

---

## 5. Skill 分层模型

建议把 skill 分为三层，而不是只有“全局”和“项目”二分。

### 5.1 Product Global Skills

由 `UnrealMCPHub` 仓库直接提供。

作用：

- 代表产品级稳定工作流
- 面向多数项目通用
- 与 Hub 工具表面保持同步

现有例子：

- `use-unrealhub`
- `team-unreal-workflow`
- `ue-benchmark`

存放位置建议：

- `UnrealMCPHub/skills/`

### 5.2 Team Global Skills

不一定属于产品默认分发，但属于组织级可复用能力。

作用：

- 团队约定
- 组织内部工作流
- 可跨多个 Unreal 项目复用

存放位置建议：

- 优先仍由外层工作区或专门 skill 仓库存放
- 如果要随 Hub 维护，也应放在 `skills/`，但标注为 team-oriented

### 5.3 Project Skills

只对某个具体 Unreal 项目成立。

作用：

- 项目目录约束
- 项目特有 map 流程
- 项目 benchmark 规则
- 项目 asset 命名和危险区说明

**关键判断：项目 skill 不应放在 `RemoteMCP` 插件仓库内作为 canonical 位置。**

原因：

- 插件仓库是 editor capability 层，不是项目知识层
- plugin sync 不应裹挟项目私有工作流
- 项目 skill 应随目标项目走，而不是随插件版本走

建议 canonical 位置：

- `<ProjectRoot>/.unrealhub/skills/<skill-name>/SKILL.md`

备选兼容入口：

- `<ProjectRoot>/Docs/AI/skills/`
- `<ProjectRoot>/Skills/`

但第一版应只定义一个 canonical 位置，避免歧义。

---

## 6. Memory 与 Skill 的关系

推荐用下面这句话约束：

**memory 存事实，skill 存方法。**

更细一点：

- memory 记录“这个项目是什么样”
- skill 记录“面对这种情况应如何做”

### 6.1 memory 不应替代 skill

以下内容不应被错误地写成长期记忆：

- “修蓝图时先 compile 再截图再验证”
- “地图切换后先 reconnect”
- “benchmark 先跑 preflight 再跑 capture”

这些是 workflow，应放在 skill 或 reference 中。

### 6.2 skill 不应替代 memory

以下内容不应只写在 skill 里：

- 本项目安全 map 是哪几个
- 哪个 capture camera 已验证通过
- 哪个 benchmark baseline 最近一次通过
- 哪个目录不可写

这些是事实，应进入项目记忆层。

### 6.3 skill 可以消费 memory

正确关系是：

- skill 读取 memory
- skill 根据 memory 决定流程
- skill 可产生“记忆候选”
- Hub 决定是否固化为长期记忆

---

## 7. 建议的数据模型

第一版不要直接上重型 graph 系统，建议用“结构化记录 + 可选关系边”模型。

### 7.1 MemoryRecord

建议字段：

```json
{
  "id": "mem_...",
  "scope": "global | project | instance | session",
  "kind": "fact | constraint | decision | hazard | workflow_hint | validation_result | benchmark_baseline | artifact_index",
  "status": "candidate | validated | stale | retired",
  "project_key": "MyGame",
  "instance_key": "MyGame:8422",
  "title": "Sandbox map list",
  "summary": "Allowed maps for AI sandbox work.",
  "content": {},
  "tags": ["sandbox", "map", "policy"],
  "source": "manual_note | tool_result | benchmark_report | imported_doc | skill_emit",
  "source_ref": "tool:get_editor_state",
  "evidence_refs": ["art_...", "art_..."],
  "related_skills": ["team-unreal-workflow", "project-sandbox-rules"],
  "engine_version": "5.5",
  "plugin_version": "remote-mcp@...",
  "branch": "main",
  "created_at": "...",
  "updated_at": "...",
  "expires_at": null,
  "confidence": 0.95,
  "author": "agent | human | imported",
  "review_required": false
}
```

### 7.2 ArtifactRecord

建议字段：

```json
{
  "id": "art_...",
  "kind": "log | screenshot | report | json | video | crash",
  "project_key": "MyGame",
  "instance_key": "MyGame:8422",
  "path": "...",
  "sha256": "...",
  "summary": "...",
  "created_at": "...",
  "producer": "Hub | RemoteMCP | benchmark-skill"
}
```

### 7.3 SkillRecord

这是 Hub 侧的 skill 索引，不是 skill 内容本体。

建议字段：

```json
{
  "id": "project-sandbox-rules",
  "tier": "product-global | team-global | project",
  "project_key": "MyGame",
  "root_path": "...",
  "skill_path": ".../SKILL.md",
  "display_name": "Project Sandbox Rules",
  "description": "...",
  "tags": ["sandbox", "write-scope"],
  "priority": 100,
  "extends": ["team-unreal-workflow"],
  "required_domains": ["level", "blueprint"],
  "updated_at": "..."
}
```

### 7.4 RelationEdge

如果需要图关系，可增加轻量 edge 表：

```json
{
  "from_id": "mem_...",
  "to_id": "mem_...",
  "relation": "depends_on | supersedes | evidenced_by | recommends_skill | applies_to"
}
```

---

## 8. 存储实现建议

### 8.1 第一版存储选型

建议：

- **SQLite** 做主索引与结构化查询
- **filesystem** 做 artifact 存储

理由：

- 当前 Hub 已经用本地文件持久化 `config.json` 和 `state.json`
- SQLite 比继续堆 JSON 更适合做检索、过滤、迁移和并发读写
- 不需要第一版就引入远程数据库和向量库

### 8.2 目录建议

Hub 侧新增：

```text
~/.unrealhub/
  config.json
  state.json
  memory/
    knowledge.db
    artifacts/
    exports/
```

### 8.3 代码放置建议

在 `UnrealMCPHub` 中新增：

```text
src/unrealhub/memory/
  __init__.py
  models.py
  store.py
  retrieval.py
  promotion.py
  artifact_store.py
  skill_registry.py
  migrations.py
```

在 `src/unrealhub/tools/` 中新增：

```text
memory_tools.py
skill_tools.py
```

建议的 Hub 工具：

- `memory_add_candidate`
- `memory_validate`
- `memory_search`
- `memory_get`
- `memory_retire`
- `memory_attach_artifact`
- `skill_list`
- `skill_resolve`
- `skill_status`

注意：

- 第一版不一定要把所有工具都暴露给外部 agent
- 其中一部分可以先作为内部库被 `session_tools`、benchmark skill、workflow skill 调用

---

## 9. RemoteMCP 该做什么，不该做什么

### 9.1 RemoteMCP 应新增的内容

RemoteMCP 不应承载长期记忆库，但应补齐“证据源”和“可结构化读取对象”。

建议新增两类能力：

#### A. 观察/快照类工具

- `get_editor_selection_snapshot`
- `get_world_outliner_snapshot`
- `get_map_snapshot`
- `get_blueprint_graph_snapshot`
- `get_pie_snapshot`

这些是**事实采样器**。

#### B. 证据采集类工具

- `capture_editor_view`
- `capture_pie_view`
- `collect_runtime_log_excerpt`
- `collect_compile_result`
- `collect_validation_summary`

这些是**artifact 生产器**。

### 9.2 RemoteMCP 不应新增的内容

不建议在 RemoteMCP 内做：

- 全局 knowledge DB
- 项目记忆检索排序
- 全局 skill registry
- 团队规则引擎
- 大量长期状态迁移逻辑

原因很简单：

- 插件的运行时生命周期短
- UE runtime Python 环境更脆弱
- map 切换与 session disruption 会让长期状态管理复杂化
- 这些工作更适合稳定的 Hub 侧执行

---

## 10. Skill 发现与优先级解析

建议在 Hub 侧实现统一 skill 解析，而不是让各层各自找文件。

### 10.1 发现顺序

建议优先级：

1. 显式指定的 skill
2. 项目 skill
3. team global skill
4. product global skill

### 10.2 解析规则

建议：

- project skill 可以 `extends` 全局 skill
- project skill 允许覆盖流程约束，但不允许篡改 Hub/RemoteMCP 工具契约
- 相同主题下，project skill 优先于全局 skill

### 10.3 Hub 的 canonical 发现位置

#### Product Global Skills

- `UnrealMCPHub/skills/`

#### Project Skills

- `<ProjectRoot>/.unrealhub/skills/`

#### Project References

- `<ProjectRoot>/.unrealhub/references/`

理由：

- 这和当前 Hub 可通过 `uproject_path` 推导项目根目录的设计天然匹配
- 不依赖 Unreal Editor 必须运行
- 不把团队工作流塞进插件分发目录

---

## 11. 记忆写入策略

长期记忆最危险的问题不是“记不住”，而是“记错了还一直信”。

所以建议引入三段式写入：

### 11.1 Observation

来自：

- RemoteMCP tool result
- screenshot/log artifact
- human note
- benchmark output

此时只是观察，不是长期真相。

### 11.2 Candidate Memory

Hub 将 observation 转成 candidate。

要求：

- 必须带 source
- 必须带时间戳
- 能带 evidence 就必须带 evidence
- 默认不直接进入 validated

### 11.3 Validated Memory

满足下列任一条件后，才可进入 validated：

- 人工确认
- benchmark 验证通过
- 结构化工具重复验证通过
- 同一结论被多个证据源支持

### 11.4 Stale / Retired

以下情况应让记忆进入 stale：

- engine 版本变化
- 插件版本变化
- 分支大幅切换
- 证据缺失
- 长期未重验

retired 用于：

- 明确作废
- 被新结论 supersede

---

## 12. 记忆检索策略

### 12.1 默认检索顺序

对 active project 的任务，默认检索顺序建议为：

1. project validated memory
2. project stale memory
3. team global memory
4. product global memory
5. session memory

说明：

- session memory 不是最可信，但在当前任务中常最相关
- stale memory 不能直接当真，但应显示提示

### 12.2 排序因子

推荐排序因子：

- scope 匹配度
- status
- tag 匹配度
- engine/plugin/branch 匹配度
- recency
- evidence 完整度
- confidence

### 12.3 返回结构

检索结果不应只返回文本块，建议返回：

- summary
- why matched
- evidence refs
- stale warning
- recommended skills

---

## 13. 与 benchmark / validation 的结合

长期记忆最先落地的高价值场景，不是“全知全能项目脑”，而是 benchmark 与验证。

建议优先沉淀以下对象：

- benchmark baseline
- capture camera presets
- 已验证通过的 test map
- 常见失败模式
- 通过时的 artifact 索引
- 上次失败与本次修复的对照

这类信息天然适合长期记忆，因为：

- 跨会话复用强
- 证据清晰
- 可验证
- 易失真风险低于开放式推理结论

---

## 14. 推荐的第一期实现范围

### P0

- 在 Hub 内新增 `MemoryStore`
- 支持 `project/global/session` 三层 scope
- 支持 `candidate/validated/stale/retired`
- 支持 artifact 索引
- 支持项目 skill 发现
- 支持最小检索 API

### P0.5

- 支持 memory promotion
- 支持 stale 判定
- 支持 skill priority / extends
- 支持 benchmark 结果写入长期记忆

### P1

- 支持 relation edges
- 支持 richer retrieval ranking
- 支持 memory export / review UI
- 支持 memory 与 recommended skill 联动

---

## 15. 放在哪里

### 15.1 代码放在哪里

#### 长期记忆主实现

放在：

- `UnrealMCPHub/src/unrealhub/memory/`

#### skill 索引与解析

放在：

- `UnrealMCPHub/src/unrealhub/memory/skill_registry.py`
- 或单独 `src/unrealhub/skills/registry.py`

但第一版放在 memory 侧更容易统一实现。

#### 编辑器内快照与证据工具

放在：

- `UnrealRemoteMCP/Content/Python/tools/`
- 必要时配合 `Source/RemoteMCP` 的 C++ wrapper

### 15.2 文档放在哪里

此类框架文档应放在：

- `UnrealMCPHub/docs/unreal-ai-playbook/`

原因：

- 这是 workflow / orchestration / policy / team-facing 设计
- 不属于 RemoteMCP 的 editor-native 核心职责

### 15.3 项目 skill 放在哪里

推荐 canonical 目录：

- `<ProjectRoot>/.unrealhub/skills/`

### 15.4 项目记忆导入模板放在哪里

推荐：

- `<ProjectRoot>/.unrealhub/memory-seeds/`

用于：

- 初始 sandbox 规则
- 项目已知风险
- 默认 capture 机位
- benchmark baseline seed

---

## 16. 推荐的设计原则

最后用六条原则收束：

1. **Hub 管长期，RemoteMCP 管事实采样。**
2. **memory 存事实，skill 存方法。**
3. **项目知识跟项目走，不跟插件走。**
4. **没有证据的长期记忆，默认只算 candidate。**
5. **skill 可以读取 memory，但不应替代 memory。**
6. **先把 benchmark / validation / evidence 这条线做好，再扩展到更开放的项目知识图谱。**

---

## 17. 后续建议

如果按实现收益排序，下一步最值得做的是：

1. 在 Hub 里实现最小 `MemoryStore`
2. 在 Hub 里实现项目 skill 发现
3. 在 RemoteMCP 里补快照/证据工具
4. 让 benchmark workflow 开始把结果写入 project memory
5. 再做 richer retrieval 和 stale/invalidation

这条路线最符合当前项目边界，也最容易渐进落地。
