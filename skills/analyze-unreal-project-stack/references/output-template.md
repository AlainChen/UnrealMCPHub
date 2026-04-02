# Output Template

## 目标

用固定结构输出项目分析结果，避免只写成长篇散文。

## 推荐结构

### 1. Project Fingerprint

- 工作区类型：源码引擎 / 单项目 / 混合
- 主 `.uproject`
- 引擎版本
- 主要目录层次
- 主模块与插件分布

### 2. Stack Summary

- gameplay stack
- UI stack
- scripting stack
- data/config stack
- audio / pipeline / CI stack

### 3. Custom Engine Assessment

- 结论等级：`standard engine` / `source-engine workspace` / `engine-coupled project` / `actual engine modification observed`
- 证据
- 置信度

### 4. Runtime Center Of Gravity

说明真正的运行时重心在哪几层：

- project modules
- plugins
- GameFeatures
- Blueprint
- Lua / script runtime
- generated bindings
- data assets / tables

### 5. Config And Source-Of-Truth Map

至少列出：

- 启动配置
- runtime config
- script entry
- data generation source
- generated outputs
- 不应直接修改的层

### 6. MCP Compatibility

按三层给结论：

- `Hub`
- `RemoteMCP`
- `project skill/topic`

建议用：

| 层 | 兼容度 | 说明 |
|----|--------|------|
| Hub | 高/中/低 | 项目配置、编译、分析、artifact 视角 |
| RemoteMCP | 高/中/低 | editor-native 观测与操作视角 |
| Project Skill | 需要/可选/暂不需要 | 项目专项知识层 |

### 7. Safe Default Workflow

默认建议：

- 先做什么
- 默认只读还是可 sandbox 写
- 哪些地方不要碰
- 先用哪些工具验证

### 8. Recommended Topics Or Skills

列出建议新增的项目 topic，例如：

- `project-overview`
- `scope-and-rules`
- `lua-runtime-and-reload`
- `designer-config-and-generation`
- `gamefeatures-and-experiences`
- `pie-and-validation`

### 9. Open Questions

明确哪些判断仍缺证据，例如：

- 插件源码不可见
- engine source 未审
- reload 路径未验证
- 运行时 feature state 未观测

## 简短输出模板

如果用户只要短版，可以压成下面这 5 段：

1. 项目是什么
2. 是否真的依赖自定义引擎
3. 真正的运行时重心在哪
4. 配置和数据从哪里来
5. 这对 Hub / RemoteMCP / project skill 有什么影响
