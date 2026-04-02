---
name: analyze-unreal-project-stack
description: 分析 Unreal 项目的实际技术栈、项目结构、引擎定制依赖、插件与脚本分层、配置流和 source-of-truth。用于内部项目接入、项目画像、兼容性判断、project quickstart/topic 生成，以及判断某项目是否依赖源码引擎或实际魔改引擎时触发。
---

# Analyze Unreal Project Stack

## 概述

把这个 skill 当成 `Hub` 的项目分析层，而不是编辑器操作层。

目标不是立刻修改项目，而是先回答这些问题：

- 这是一个什么类型的 Unreal 项目
- 它到底依赖标准引擎、源码引擎，还是实际魔改引擎
- 真正的运行时重心在 C++、插件、Blueprint、Lua、数据生成链中的哪几层
- 配置和数据的 source-of-truth 在哪里
- `UnrealMCPHub + UnrealRemoteMCP` 对这个项目的默认兼容边界是什么
- 后续应该沉淀哪些 project skill、topic 或 memory seed

默认把产出收敛成：

- `project profile`
- `custom-engine assessment`
- `config/source-of-truth map`
- `MCP compatibility note`
- `recommended project topics / skills`

## 快速使用

先加载：

- [use-unrealhub](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\use-unrealhub\SKILL.md)
- [workflow.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\workflow.md)
- [internal-project-agent-guide.zh-CN.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\docs\unreal-ai-playbook\internal-project-agent-guide.zh-CN.md)

按下面顺序分析：

1. 建立项目指纹
2. 判断“实际魔改引擎”程度
3. 识别运行时分层
4. 识别配置流和 source-of-truth
5. 判断 Hub / RemoteMCP / project skill 的适配边界
6. 输出结构化分析结论

如果任务主要在“这个项目是不是标准 UE 项目、哪些地方真的是引擎层改动、配置到底从哪来”，优先使用这个 skill。

如果任务已经进入具体编辑器操作、编译、PIE、Slate、UMG 或工具调用，回到 `use-unrealhub`。

## 工作流

### 1. 建立项目指纹

先收集这些事实，不急着下结论：

- workspace 根是引擎工作区还是单一 `.uproject`
- `Engine/Build/Build.version` 是否存在，是否为 `IsLicenseeVersion=1`
- `.uproject` 的 `EngineAssociation`
- `Source/` 是否很薄，业务能力是否主要在 `Plugins/`
- `Plugins/` 中内置、项目、Marketplace、OpenSource 的分层
- `Config/`、`Content/Script/`、`DesignerConfigs/`、`Tools/Gen/`、`Horde/`、`UGS` 是否存在

优先回答：

- 这是源码引擎工作区，还是 Launcher 风格项目
- 项目的业务重心在主工程、插件、脚本、还是数据生成链
- 是否值得后续生成项目级 quickstart/topic

### 2. 判断实际魔改引擎程度

不要把“用了源码引擎”“有很多插件”“有预编译二进制”直接等同于“魔改引擎”。

把判断分成四档：

1. `standard engine`
只有普通项目层扩展，没有发现明显源码引擎依赖。

2. `source-engine workspace`
项目依赖源码引擎编译与工作区布局，但暂未发现明确的 engine-side 业务魔改证据。

3. `engine-coupled project`
项目明显耦合某个 licensee 分支、自定义引擎构建链、引擎级模块或 engine plugin，但当前快照未必能完全看到源码。

4. `actual engine modification`
有明确证据表明 engine source、build graph、editor/runtime core class、引擎子系统或引擎层资产管线已被改写。

遇到这一步时，读取：
- [custom-engine-analysis.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\analyze-unreal-project-stack\references\custom-engine-analysis.md)

### 3. 识别运行时分层

把项目拆成这些层来理解，而不是只看 `Source/`：

- engine / source-engine
- project modules
- project plugins
- game feature plugins
- Blueprint / assets
- script runtime，例如 Lua / Python
- generated bindings / generated data
- external config and content pipeline

要特别注意：

- 主工程很薄不代表项目简单，可能只是插件化程度高
- Blueprint 很少不代表逻辑少，可能被 Lua 或 DataAsset 接管
- 二进制插件看不到源码，不代表它们不重要

### 4. 识别配置流和 source-of-truth

项目分析里最容易误判的不是“有没有配置”，而是“真正该改哪一层”。

至少要区分：

- 启动配置：`.uproject`、`*.Target.cs`、`DefaultEngine.ini`、`DefaultGame.ini`
- 插件和模块配置：`*.uplugin`、模块依赖、feature policy
- 运行时配置：AssetManager、DataRegistry、PrimaryAssetTypes、DataAssets、Experience
- 脚本运行时入口：Lua / UnLua / 生成绑定 / reload 机制
- 数据生成链：Excel/JSON、proto、代码生成、打包前导出
- 生成产物：`Gen/*`、自动生成 Lua/C++/配置文件

遇到这一步时，读取：
- [config-flow-analysis.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\analyze-unreal-project-stack\references\config-flow-analysis.md)

### 5. 判断 MCP 兼容边界

按 `Hub / RemoteMCP / skill` 三层给结论，不要只说“兼容”或“不兼容”。

- `Hub`
  关注项目配置、源码引擎路径、编译、启动、实例发现、日志、artifact、项目分析
- `RemoteMCP`
  关注编辑器原语、关卡、Actor、资产、UMG、图结构、PIE 观测与验证
- `project skill/topic`
  关注项目特有的 Lua、GameFeatures、数据生成链、命名约束、验证路径

默认结论模板：

- `Hub`: 高/中/低兼容
- `RemoteMCP`: 高/中/低兼容
- `需要 project skill`: 是/否
- `需要 project-specific topic`: 哪几类

### 6. 输出结构化结论

最终不要只给一段散文总结。至少输出：

- 项目类型
- 引擎耦合等级
- 主要技术栈
- 运行时重心
- config/source-of-truth 结论
- 默认安全边界
- 推荐的 project topic / quickstart

需要统一格式时，读取：
- [output-template.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\analyze-unreal-project-stack\references\output-template.md)

## 关键边界

### 不要做的事

- 不要把 `licensee build` 自动等同于“已经看到实际引擎魔改”
- 不要把“插件很多”误判成“引擎很多改动”
- 不要把 `Gen/*`、生成 Lua、导出 JSON 直接当成手改入口
- 不要把 `EngineAssociation` 注册表解析结果当成源码引擎项目的唯一依据
- 不要忽略脚本层和数据生成链
- 不要在项目分析阶段直接修改工程

### 什么时候需要更深入的 runtime 证据

当静态文件分析还不足以解释项目行为时，再引入：

- `ue_status`
- `ue_list_domains`
- `ue_call` 查询 editor-side state
- 日志、截图、PIE 验证

先静态分析，后运行时补证，不要反过来。

## 推荐产物

这个 skill 最适合产出：

- 项目画像
- internal project quickstart 草案
- topic 建议清单
- Hub / RemoteMCP 兼容性说明
- 风险边界和默认 capability profile 建议

## References

- [custom-engine-analysis.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\analyze-unreal-project-stack\references\custom-engine-analysis.md)
- [config-flow-analysis.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\analyze-unreal-project-stack\references\config-flow-analysis.md)
- [output-template.md](C:\Users\alain\Documents\Playground\UnrealMCPHub\skills\analyze-unreal-project-stack\references\output-template.md)
