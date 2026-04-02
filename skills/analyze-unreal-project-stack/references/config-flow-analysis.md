# Config Flow Analysis

## 目标

回答的不是“这个项目有哪些配置文件”，而是：

- 启动链从哪里开始
- 真正的 source-of-truth 在哪一层
- 哪些文件只是镜像、导出物或生成产物
- 改动某一层之后，正确的验证路径是什么

## 配置流分层

优先按六层来理解。

### 1. 启动与工程入口层

常见文件：

- `.uproject`
- `*.Target.cs`
- `Build.version`
- `DefaultEngine.ini`
- `DefaultGame.ini`

关注：

- 引擎版本与关联方式
- 默认 map
- GameInstance / AssetManager / ViewportClient / LocalPlayer / WorldSettings
- 插件启用状态

### 2. 插件与模块声明层

常见文件：

- `*.uplugin`
- `*.Build.cs`
- `*.Target.cs`

关注：

- 哪些模块只是项目层
- 哪些插件是 feature/pluginized gameplay
- 哪些插件是 marketplace/open-source
- 哪些插件只提供二进制

### 3. 运行时框架配置层

常见位置：

- `Config/*.ini`
- `Content/Gameplay/*`
- `DataRegistry`
- `PrimaryAssetTypesToScan`
- `ExperienceDefinition`
- `GameFeatureData`

关注：

- runtime config 是否主要由 asset 驱动
- feature activation 是否通过 `GameFeatures`
- gameplay 入口是否被 Experience / DataAsset 接管

### 4. 脚本运行时层

常见位置：

- `Content/Script/*`
- `DefaultUnLuaSettings.ini`
- `Main.lua`
- `Launcher.lua`
- `GameInstance` 绑定脚本

关注：

- 脚本是否是一等运行时
- reload 路径在哪里
- Blueprint 是否只是宿主而不是主要逻辑层

### 5. 外部数据与生成层

常见位置：

- `DesignerConfigs/*.xlsx`
- `DesignerConfigs/*.json`
- `Tools/Gen/*`
- `Tools/BatchFiles/*`
- `proto`、`cfg`、导表脚本

关注：

- Excel / JSON 哪个才是 source-of-truth
- 生成链生成了哪些 Lua/C++/json 产物
- 是否存在 server/client 双导出

### 6. 生成产物层

常见位置：

- `Content/Script/Gen/*`
- 自动生成的 API 绑定
- 自动生成 tags / proto types / editor data

默认规则：

- 先确认来源，再考虑修改
- 没有明确证据前，不要把生成产物当成手工入口

## 分析步骤

### 1. 先找启动链

按顺序追：

1. `.uproject`
2. `DefaultEngine.ini`
3. `DefaultGame.ini`
4. `GameInstance`
5. 项目脚本入口
6. AssetManager / GameFeaturePolicy / Experience

### 2. 再找运行时真正的组织层

判断项目更偏哪一类：

- C++ 主导
- Blueprint 主导
- Lua/脚本主导
- 数据资产主导
- 配表/生成链主导

多数大型项目是混合型，不要强行归成单一类别。

### 3. 标记 source-of-truth

对每一类配置都标注：

- canonical source
- generated mirror
- runtime consumer
- validation path

示例格式：

| 领域 | canonical source | generated mirror | runtime consumer | validation |
|------|------------------|------------------|------------------|------------|
| Lua API bindings | Tools/Gen | Content/Script/Gen | Lua runtime | reload + log |
| Gameplay config | DataAssets / Experience | none | AssetManager / systems | PIE + state |
| Designer data | DesignerConfigs/xlsx | exported json/lua/cfg | gameplay systems | regen + load |

### 4. 标记高风险误改区

尤其要标记：

- 生成目录
- 双向导出目录
- shared config
- project-wide settings
- engine-coupled config

## 对 MCP 的意义

### 对 Hub

Hub 更适合负责：

- 静态项目分析
- source-of-truth 识别
- quickstart/topic 生成
- 构建、启动、artifact 汇总

### 对 RemoteMCP

RemoteMCP 更适合负责：

- editor 状态
- asset / map / actor / ui / graph 的运行时观测
- PIE 验证
- 截图和日志证据

### 对 project skill/topic

当配置流明显依赖项目特有逻辑时，应生成：

- `lua-runtime-and-reload`
- `designer-config-and-generation`
- `gamefeatures-and-experiences`
- `pie-and-validation`

## 常见误判

- 只看 `.ini`，忽略 DataAsset / Experience / GameFeature
- 只看 Blueprint，忽略 Lua 或脚本层
- 只看 `Content/Script/Gen`，忽略真正的生成源
- 只看 `Config/`，忽略外部 Excel/JSON pipeline
