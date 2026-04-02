---
name: output-template
description: 项目分析结构化输出模板，供 analyze-unreal-project-stack skill 最终产出使用。避免散文总结，强制关键字段全覆盖。
---

# Output Template

## 目标

强制输出结构化结论，杜绝只写散文总结。

每个字段必须有具体内容。如果某字段没有足够证据，写 `⚠️ 证据不足，待补充` 而不是留空或跳过。

## 何时用完整版 vs 短版

| 场景 | 用哪个版本 |
|------|-----------|
| 初次接入一个未知项目 | 完整版（9段） |
| 已有项目画像，只是更新某个判断 | 短版（5段） |
| 用户只问"这项目能不能用 Hub" | 短版，只展开第 5 段 |
| 生成 project quickstart 草案 | 完整版 + 第 8 段展开 |

---

## 完整版（9 段）

### 1. Project Fingerprint

> 收集事实，不下结论。

| 字段 | 值 |
|------|----|
| 工作区类型 | `源码引擎工作区` / `单项目（Launcher 风格）` / `混合` |
| 主 .uproject | `ProjectName.uproject`（路径） |
| 引擎版本 | `5.3.2` / `5.1-licensee-branch-xxx` |
| EngineAssociation | `{GUID}` / `../../../Engine` / `自定义注册表项` |
| IsLicenseeVersion | `0` / `1` |
| 主要顶层目录 | `Source/`、`Plugins/`、`Config/`、`Content/`... |
| 插件分布 | 内置 N 个 / 项目 N 个 / Marketplace N 个 / 二进制 N 个 |
| 能力重心 | 主模块 / 插件 / Lua / DataAsset / 配表 |

---

### 2. Stack Summary

> 快速告诉读者这个项目在哪几层有实质内容。

| 层 | 状态 | 备注 |
|----|------|------|
| Gameplay (C++) | 薄 / 中 / 厚 | 例：主要靠 GAS + LyraExperience 驱动 |
| UI | Slate / UMG / 混合 | |
| Scripting | 无 / Lua / Python / 混合 | |
| Data / Config | ini 主导 / DataAsset 主导 / 配表主导 | |
| Audio | 标准 / Wwise / MetaSound | |
| CI / Build | 标准 UAT / Horde / 自定义 | |

---

### 3. Custom Engine Assessment

> 给结论等级，附证据清单和置信度。

**结论等级**（选一个）：

- `standard engine` — 仅项目层扩展，无源码引擎依赖迹象
- `source-engine workspace` — 依赖源码编译，但暂无 engine-side 改动证据
- `engine-coupled project` — 明显绑定 licensee 分支或构建链
- `actual engine modification observed` — 有明确 engine source / build graph 改动证据

**证据清单**：

```
A 级（强）：
  - ...
B 级（中）：
  - ...
C 级（弱 / 排除）：
  - ...
```

**置信度**：`高` / `中` / `低（需要 runtime 补证）`

---

### 4. Runtime Center of Gravity

> 说明逻辑真正在哪几层，而不只是"有什么"。

| 层 | 占比估计 | 备注 |
|----|---------|------|
| project modules (C++) | 低 / 中 / 高 | |
| project plugins | 低 / 中 / 高 | |
| game feature plugins | 有 / 无 | |
| Blueprint | 薄 / 中 / 厚 | |
| Lua / script runtime | 无 / 存在 / 主导 | |
| generated bindings | 无 / 自动生成 | |
| data assets / tables | 辅助 / 主导 | |

**结论**：运行时重心在 ___，次要层在 ___。主工程很薄的原因是 ___。

---

### 5. Config and Source-of-Truth Map

> 对每类配置都标 canonical source，不要只列文件名。

| 领域 | Canonical Source | Generated Mirror | Runtime Consumer | 验证路径 |
|------|-----------------|-----------------|-----------------|--------|
| 引擎版本 / 启动 | `.uproject` + `DefaultEngine.ini` | — | UBT / 启动器 | 编译通过 |
| Gameplay 框架 | `ExperienceDefinition` / `DataAssets` | — | AssetManager | PIE 启动 |
| 脚本入口 | `Content/Script/Main.lua` | — | Lua runtime | reload + log |
| Designer 数据 | `DesignerConfigs/*.xlsx` | `Content/Script/Gen/` | gameplay systems | regen + compare |
| UI 配置 | `*.ini` / DataAsset | — | UMG | PIE 截图 |

**不应直接修改的层**：

- `Content/Script/Gen/` — 自动生成，改了会被覆盖
- `Engine/Config/` — 引擎层，应走 ini override 机制

---

### 6. MCP Compatibility

| 层 | 兼容度 | 说明 |
|----|--------|------|
| Hub | 高 / 中 / 低 | 能否用标准 `setup_project`，是否需要显式 `engine_root` |
| RemoteMCP | 高 / 中 / 低 | editor-native 原语覆盖率，PIE / 资产 / UMG 可观测性 |
| Project Skill | 需要 / 可选 / 暂不需要 | 哪些地方标准 skill 覆盖不到 |

**关键限制**：

- `setup_project` 是否必须传 `engine_root`：是 / 否
- 是否应跳过注册表解析：是 / 否
- 哪些能力需要 project-specific skill 补充：...

---

### 7. Safe Default Workflow

> 告诉 agent 默认应该怎么开始，默认不碰什么。

1. 先做 ___ （例：静态分析 + 指纹收集）
2. 确认 `engine_root` / `project_root` 后再做 ___
3. 以下区域**默认只读**，不主动修改：___
4. 首次验证用这些工具：`ue_status` / `ue_list_domains` / 日志

---

### 8. Recommended Topics or Skills

> 列出应该为这个项目沉淀哪些 topic / skill，附理由。

| 名称 | 优先级 | 原因 |
|------|--------|------|
| `project-overview` | 高 | 项目基础画像，所有任务共用 |
| `scope-and-rules` | 高 | 安全边界、命名约束 |
| `lua-runtime-and-reload` | 中 | Lua 是一等运行时，需要专项知识 |
| `designer-config-and-generation` | 中 | 配表生成链非标准，需要专项文档 |
| `gamefeatures-and-experiences` | 低 / 按需 | 仅当 GAS+Lyra 模式明显时 |
| `pie-and-validation` | 中 | PIE 验证路径不标准 |

---

### 9. Open Questions

> 明确说明哪些结论依据不足，避免过度自信。

| 问题 | 缺什么证据 | 建议的补证手段 |
|------|-----------|--------------|
| 插件 X 内部实现未知 | 无源码 | 读 `.uplugin` + 运行时观测 |
| Lua reload 路径未验证 | 未运行 PIE | `ue_call` 查 reload 入口 |
| engine source 修改情况 | Engine/Source 未可见 | 需要 engine workspace 访问 |

---

## 短版（5 段）

适合已有基本了解、只需要更新关键结论时使用：

**1. 项目是什么**
一句话描述类型、引擎版本、主要技术栈。

**2. 是否依赖自定义引擎**
给出等级 + 一句置信度说明。

**3. 真正的运行时重心**
1-2 句说明逻辑集中在哪几层，主工程薄的原因。

**4. 配置和数据从哪里来**
列出 canonical source，和不应手改的层。

**5. 对 Hub / RemoteMCP / project skill 的影响**
用三行给出兼容度结论和关键限制。
