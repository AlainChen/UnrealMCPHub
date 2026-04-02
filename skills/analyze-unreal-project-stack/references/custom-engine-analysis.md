# Custom Engine Analysis

## 目标

判断一个 Unreal 项目是：

- 仅使用标准引擎
- 运行在源码引擎工作区中
- 强依赖某个 licensee / forked engine 分支
- 真的存在 engine-side 修改

结论应基于证据分层，而不是单点猜测。

## 证据优先级

### A. 强证据

这些通常足以支持“实际引擎魔改”判断：

- `Engine/Source` 下存在项目特有修改或新增 engine module
- `Engine/Plugins` 下存在项目强依赖的自定义 engine plugin
- `Build.version` 显示自定义 branch 且项目工作流明确依赖该分支
- `BuildGraph`、`Horde`、`AutomationTool`、`UBT`、`UAT` 有项目专属修改
- engine core class 或 subsystem 明显被替换
- 项目配置明确依赖 engine-side class 或 engine-side patched behavior

### B. 中证据

这些说明项目与自定义引擎高度耦合，但不一定足以证明 engine source 已改：

- 完整源码引擎工作区结构
- `IsLicenseeVersion=1`
- 自定义引擎分支名
- 项目必须从源码工作区编译和启动
- 预编译插件、工具链、CI 明显绑定该引擎分支

### C. 弱证据

这些不能单独证明“实际引擎魔改”：

- `Plugins/` 很多
- 项目是大型项目
- 有二进制插件
- 有很多 `Config/*.ini`
- 有 GameFeatures、Lua、Wwise、Horde

## 分析步骤

### 1. 确认工作区形态

检查：

- 是否存在 `Engine/`
- 是否存在 `GenerateProjectFiles.*`
- 是否存在 `Setup.*`
- 是否存在 `.ugs`
- `Build.version` 是否可读

### 2. 确认项目是否依赖源码引擎

检查：

- `.uproject` 的 `EngineAssociation`
- 是否需要显式 `engine_root`
- `Target.cs`、CI 配置、Horde 配置是否引用本地 `Engine`

### 3. 区分项目层扩展与引擎层扩展

区分下面几类：

- `project modules`
- `project plugins`
- `engine plugins`
- `engine source changes`

项目里插件很多，不等于引擎被改。

### 4. 找运行时耦合点

特别看这些地方是否指向 engine-side 特性：

- `AssetManagerClassName`
- 自定义 viewport / local player / game settings / world settings
- build scripts / package pipeline
- 自定义 editor 工具或引擎命令

### 5. 明确结论等级

建议只在证据充足时使用“实际魔改引擎”。

更保守的表述优先级：

1. `standard project`
2. `source-engine workspace`
3. `engine-coupled project`
4. `actual engine modification observed`

## 输出建议

建议输出三段：

### 1. 观察到的证据

列出文件、配置、目录结构和工具链证据。

### 2. 结论等级

给出四档结论之一，并说明置信度。

### 3. 对 MCP 的影响

明确指出这对 `Hub` 和 `RemoteMCP` 的影响，例如：

- `setup_project` 是否必须显式传 `engine_root`
- 是否不应依赖注册表解析
- 是否应该默认把 engine/plugin 修改当高风险区

## 常见误判

- 把 licensee version 直接等同于 engine source 已经大改
- 把二进制插件当成 engine modifications
- 把项目层 GameFramework 替换误判成 engine core 修改
- 在没有 `Engine/Source` 证据时直接断言“这项目就是魔改引擎”
