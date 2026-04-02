# Unreal 长期记忆框架测试用例

最后更新：2026-03-23

本文对应：

- [长期记忆框架设计](./long-term-memory-framework.zh-CN.md)

测试目标：

- 验证 `UnrealMCPHub` 侧长期记忆存储、检索、skill 解析与 artifact 归档
- 验证 `UnrealRemoteMCP` 只作为事实与证据来源，而不承担长期状态中心
- 验证全局 skill / 项目 skill 的发现、优先级与协作关系

---

## 1. 测试分层

建议测试分为四层：

1. **Unit**
   - 模型、存储、排序、状态迁移、skill 发现
2. **Integration**
   - Hub memory 与 state/config/session 的联动
   - Hub 与 RemoteMCP 结果的接线
3. **Workflow**
   - benchmark、验证、证据沉淀、skill 决策
4. **Failure / Safety**
   - 版本漂移、证据缺失、污染、跨项目串台、stale 失效

---

## 2. Unit 测试用例

### MEM-001 创建 candidate memory

目标：

- 验证最小 candidate 记录可写入

前置：

- 初始化空 `MemoryStore`

步骤：

1. 调用 `add_candidate(scope="project", kind="fact", ...)`
2. 不附加 evidence

预期：

- 写入成功
- `status == "candidate"`
- 自动补齐 `id / created_at / updated_at`
- `review_required == false` 或按默认规则设置

### MEM-002 candidate 缺少 source 被拒绝

目标：

- 防止无来源事实进入长期记忆

步骤：

1. 写入 candidate，但 `source` 为空

预期：

- 校验失败
- 不落库

### MEM-003 artifact record 写入与哈希记录

目标：

- 验证 artifact 元数据与文件引用正确保存

步骤：

1. 写入一个 screenshot artifact
2. 附带 path 与 sha256

预期：

- artifact 表中存在记录
- path、kind、sha256 正确

### MEM-004 validated memory 必须可追溯 source

目标：

- 防止“无证确认”

步骤：

1. 直接创建 `status="validated"` 的记录
2. 不提供 source 或 evidence

预期：

- 被拒绝，或自动降级为 candidate

### MEM-005 memory 状态迁移

目标：

- 验证 `candidate -> validated -> stale -> retired`

步骤：

1. 写入 candidate
2. 调用 validate
3. 调用 mark_stale
4. 调用 retire

预期：

- 状态按顺序变化
- 各次变更更新时间被刷新

### MEM-006 supersede 关系

目标：

- 新结论替代旧结论时关系正确

步骤：

1. 写入旧 baseline
2. 写入新 baseline
3. 建立 `supersedes` 关系

预期：

- edge 存在
- 旧记录可被标记为 stale 或 retired

### MEM-007 project scope 与 global scope 隔离

步骤：

1. 写入 `project=A` 的 memory
2. 写入 global memory
3. 检索 `project=A`

预期：

- 同时返回 project A 与 global
- 不返回其他 project 记录

### MEM-008 检索排序优先 project validated

步骤：

1. 写入 project validated
2. 写入 global validated
3. 检索同一 tag

预期：

- project validated 排在 global validated 前

### MEM-009 stale 排序低于 validated

步骤：

1. 写入一条 validated
2. 写入一条 stale
3. 检索同主题

预期：

- stale 排在后面
- stale 结果带 warning 标识

### MEM-010 branch 不匹配降低相关性

步骤：

1. 写入 `branch=main`
2. 当前查询上下文为 `branch=feature/x`

预期：

- 结果仍可命中
- 但排序分数下降并带 branch mismatch 提示

### MEM-011 engine version 不匹配触发 stale

步骤：

1. 写入 `engine_version=5.4`
2. 查询上下文为 `5.5`

预期：

- 若策略为严格失效，则标记 stale
- 若策略为软失效，则返回 warning

### MEM-012 relation edge 查询

步骤：

1. memory A 关联 skill S
2. memory A evidenced_by artifact B

预期：

- 可正确取回相关 skill 与 artifact

---

## 3. Skill 注册与解析测试

### SKILL-001 发现 product global skill

前置：

- `UnrealMCPHub/skills/use-unrealhub/SKILL.md` 存在

步骤：

1. 扫描内置 skills 目录

预期：

- 发现 `use-unrealhub`
- tier 为 `product-global`

### SKILL-002 发现 project skill

前置：

- `<ProjectRoot>/.unrealhub/skills/project-sandbox/SKILL.md` 存在

步骤：

1. Hub 根据 active project 推导 project root
2. 扫描项目 skills 目录

预期：

- 发现 `project-sandbox`
- tier 为 `project`
- `project_key` 正确

### SKILL-003 project skill 优先于 global skill

步骤：

1. 全局 skill 与项目 skill 命中相同主题
2. 调用 `skill_resolve(topic=...)`

预期：

- 优先返回项目 skill

### SKILL-004 skill extends 解析

步骤：

1. project skill 声明 `extends: team-unreal-workflow`

预期：

- registry 中关系可见
- resolve 时先取 project skill，再可追溯到父 skill

### SKILL-005 非法 project skill 不污染 registry

步骤：

1. 提供损坏 frontmatter 的 `SKILL.md`

预期：

- registry 记录错误
- 不将其视为有效 skill

### SKILL-006 project skill 不得覆盖 tool contract

目标：

- 防止 skill 越权改变工具语义

步骤：

1. project skill 中声明与真实 tool 参数不一致的要求

预期：

- skill 只作为工作流建议被索引
- 不影响 Hub/RemoteMCP tool schema

---

## 4. Hub 与 Memory 联动测试

### HUBMEM-001 从 session note 提升为 candidate memory

步骤：

1. `add_note("Sandbox map /Game/Maps/AI_Sandbox is safe")`
2. 调用 promotion 流程

预期：

- 生成 candidate memory
- `source=manual_note`

### HUBMEM-002 从 benchmark 结果生成 validated baseline

步骤：

1. 导入 benchmark 结果 JSON
2. 附带截图与日志 artifact
3. promotion 策略判定通过

预期：

- 写入 `kind=benchmark_baseline`
- `status=validated`
- evidence_refs 完整

### HUBMEM-003 从 crash 报告生成 hazard memory

步骤：

1. Hub 收到 crash log
2. 人工确认问题模式

预期：

- 写入 `kind=hazard`
- source 指向 crash artifact

### HUBMEM-004 记忆检索结果返回 recommended skills

步骤：

1. 某条 memory 关联 `team-unreal-workflow`
2. 执行检索

预期：

- 返回结构中包含 related skill 信息

### HUBMEM-005 active project 切换后检索范围切换

步骤：

1. active project = A，检索一次
2. 切换 active project = B，再检索

预期：

- 默认命中范围随 active project 改变
- 不串台

### HUBMEM-006 memory 导出

步骤：

1. 导出某项目 validated memory

预期：

- 输出 deterministic JSON 或 Markdown 摘要
- 含 source 与 evidence refs

---

## 5. RemoteMCP 集成测试

### RMMEM-001 RemoteMCP 快照工具只返回事实，不直接写长期记忆

步骤：

1. 调用 `get_map_snapshot`

预期：

- 仅返回 snapshot
- 不在插件内创建长期状态文件
- 由 Hub 决定是否写 memory

### RMMEM-002 capture 工具生成 artifact，Hub 负责归档

步骤：

1. RemoteMCP 生成 screenshot
2. Hub 接收并登记 artifact

预期：

- artifact 最终进入 Hub artifact store
- RemoteMCP 不负责长期索引

### RMMEM-003 map 切换后 session disruption 不破坏长期记忆

步骤：

1. 写入若干 project memory
2. 触发 `load_map`
3. 会话中断并重连

预期：

- MemoryStore 不受影响
- 仅 session/instance 短期状态变化

### RMMEM-004 结构化验证结果可被提升为 memory

步骤：

1. RemoteMCP 返回 `ok / data / message / risk_tier`
2. Hub 读取结果并做 promotion

预期：

- 生成 candidate memory
- provenance 包含 tool name 与 instance key

---

## 6. Workflow / Benchmark 测试

### FLOW-001 benchmark skill 读取 project memory

步骤：

1. project memory 中已有 sandbox map 与 camera preset
2. 运行 benchmark workflow

预期：

- skill 使用这些事实
- 不要求用户重复输入

### FLOW-002 workflow 生成新 validation_result memory

步骤：

1. skill 跑完一次验证
2. 输出通过、截图、日志、结论

预期：

- 生成 `validation_result` candidate 或 validated 记录

### FLOW-003 workflow 不把临时失败直接固化为 validated

步骤：

1. 一次验证失败
2. 无人工确认

预期：

- 最多生成 candidate / hazard candidate
- 不直接成为 validated 事实

### FLOW-004 同类 benchmark 多次通过后自动升格

步骤：

1. 同一 benchmark 在相同版本下连续多次通过

预期：

- promotion 策略可将其升级为 validated baseline

### FLOW-005 项目 skill 与 memory 配合进行写入前检查

步骤：

1. 项目 skill 指定只允许写入 sandbox 路径
2. memory 中记录禁写目录
3. 发起写操作

预期：

- 写入前检查失败
- 返回清晰阻断原因

---

## 7. Safety / Failure 测试

### SAFE-001 损坏数据库恢复

步骤：

1. 模拟 `knowledge.db` 损坏
2. 启动 Hub

预期：

- Hub 报错可读
- 不破坏现有 config/state
- 可进入只读降级模式或要求恢复

### SAFE-002 artifact 文件丢失

步骤：

1. 删除已登记 artifact 文件
2. 查询引用该 artifact 的 memory

预期：

- 结果显示 evidence missing
- memory 可自动进入 stale 或 warning 状态

### SAFE-003 项目切换后禁止读取其他项目私有 memory

步骤：

1. 项目 A 有私有 memory
2. 当前 active project 为 B

预期：

- 默认检索不返回 A 的私有记忆

### SAFE-004 外部导入 memory seed 格式错误

步骤：

1. 导入损坏的 seed 文件

预期：

- 记录失败原因
- 不污染正式 memory store

### SAFE-005 skill 与 memory 冲突

步骤：

1. 项目 skill 声称某 map 可安全写入
2. project memory 标记该 map 为 hazard

预期：

- resolve 阶段提示冲突
- 默认以 memory 中的 hazard 为高优先级阻断

### SAFE-006 版本升级导致 memory migration

步骤：

1. Memory schema 升级
2. 运行 migration

预期：

- migration 可重复执行
- 不丢记录
- 可记录旧 schema version 到新 schema version

### SAFE-007 stale 记忆不会默默当真

步骤：

1. 返回 stale memory

预期：

- 响应中必须显式标识 stale
- 不允许与普通 validated 结果无差别展示

### SAFE-008 大量低质量 candidate 不应拖垮检索

步骤：

1. 写入大量 candidate records
2. 执行常见检索

预期：

- 排序优先 validated
- 查询延迟可控

---

## 8. 建议新增自动化测试文件

在 `UnrealMCPHub/tests/` 中建议新增：

```text
test_memory_models.py
test_memory_store.py
test_memory_retrieval.py
test_memory_promotion.py
test_memory_artifact_store.py
test_skill_registry.py
test_memory_tools.py
test_skill_tools.py
test_memory_project_isolation.py
```

如果后续在 `RemoteMCP` 新增快照工具，建议新增：

```text
test_snapshot_tools.py
test_capture_tools.py
test_memory_provenance_contract.py
```

---

## 9. 最小验收标准

第一期框架可以认为“达到可用”时，至少满足：

1. Hub 可持久化 project/global/session 三层记忆
2. Hub 可发现内置 skill 与项目 skill
3. RemoteMCP 可提供至少一种快照工具和一种 artifact 工具
4. benchmark 结果可沉淀为 project memory
5. stale / validated / candidate 三种状态可清晰区分
6. 项目切换不会串记忆和 skill

如果这六项还未满足，就不应把系统描述为“长期记忆框架已完成”。
