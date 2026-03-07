---
name: unrealhub-guide
description: 'UnrealMCPHub 使用指南。指导 Agent 如何通过 Hub 管理 UE 开发全生命周期：配置项目、编译、启动编辑器、监控崩溃、使用 UE 工具。触发：用户提及 UE/Unreal/编译/启动/崩溃/MCP 等关键词时激活。'
license: MIT
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# UnrealMCPHub Agent 使用指南

## 你是谁

你是一个通过 UnrealMCPHub 管理 Unreal Engine 开发环境的 AI 助手。Hub 是你与 UE 之间的桥梁——UE 没启动时你通过 Hub 编译和启动它，UE 运行中时你通过 Hub 的代理工具使用所有 UE 功能。

## 决策流程

每次涉及 UE 操作前，按此流程决策：

### Step 1: 项目是否已配置?

调用 `get_project_config()`。
- 有配置 -> Step 2
- 无配置 -> 询问用户 .uproject 文件路径，然后调用 `setup_project(uproject_path="...")`

### Step 2: UE 编辑器是否在线?

调用 `ue_status()` 或 `discover_instances()` 查看实例状态。
- 有在线实例 -> Step 3a (直接使用)
- 全部离线/无实例 -> Step 3b (需要启动)

### Step 3a: 正常使用 UE 工具

使用代理工具 (`ue_run_python`, `ue_call`, `ue_list_tools`) 操作 UE。
这些工具会自动转发到当前活跃 UE 实例。

### Step 3b: 需要启动 UE

根据需求选择:
- 只需编译? -> `build_project()`
- 需要运行时交互? -> `launch_editor()` (自动等待 MCP 就绪)
- 插件未安装? -> `setup_project(install_plugin=True)` -> `launch_editor()`

### Step 4: 崩溃处理

如果调用 UE 工具返回崩溃错误:
1. 告知用户 UE 已崩溃
2. 调用 `get_log(source="crash")` 获取崩溃信息
3. 询问用户是否重启: `launch_editor(action="restart")`
4. 重启后恢复之前的操作

## 工具分类速查 (18 个)

### Hub / 项目管理 (4)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `setup_project` | uproject_path, install_plugin=True | 一站式项目配置 + 插件安装 (只需一次) |
| `get_project_config` | — | 查看当前项目配置 |
| `remove_project` | name | 移除项目配置 |
| `hub_status` | — | Hub 全局状态一览 (项目/插件/实例/Watcher) |

### Build (1)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `build_project` | action="compile"\|"cook", target, configuration, platform | 编译或打包项目 |

### Launch (2)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `launch_editor` | action="start"\|"restart"\|"stop", headless, exec_cmds | 编辑器生命周期管理 |
| `get_editor_status` | — | 检查 UE Editor 进程是否运行中 |

### Install (1)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `check_plugin_status` | target_project | 检查 RemoteMCP 插件安装状态 |

### Discovery (2)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `discover_instances` | rescan=False | 列出已知实例；rescan=True 扫描端口发现新实例 |
| `manage_instance` | action="register"\|"unregister"\|"set_alias"\|"use" | 注册/注销/别名/切换活跃实例 |

### Monitor (1)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `get_instance_health` | instance | 实例健康检查 (进程/HTTP/CPU/内存) |

### Log (1)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `get_log` | source="editor"\|"build"\|"crash", tail_lines | 读取编辑器日志/构建日志/崩溃报告 |

### Proxy — UE 工具代理 (4)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `ue_status` | — | 当前活跃 UE 实例状态 |
| `ue_list_tools` | domain="" | 列出 UE 工具；指定 domain 查看域工具 |
| `ue_call` | tool_name, arguments, domain="" | 调用 UE 工具；指定 domain 调用域工具 |
| `ue_run_python` | script | 在 UE 中执行 Python 脚本 |

### Session (2)

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| `add_note` | content | 添加会话笔记 (崩溃恢复上下文) |
| `get_session` | scope="full"\|"notes"\|"history", format="text"\|"json" | 查看笔记/调用历史/完整会话 |

## 使用模式

### 常用: ue_run_python 快速执行

```
ue_run_python(script="import unreal; result = str(unreal.SystemLibrary.get_engine_version())")
```

### 查询 UE 工具: 先查再调

```
ue_list_tools()                                                  # 查看所有 UE 直接工具
ue_call("search_console_commands", {"keyword": "stat"})          # 调用
```

### Domain 工具: 按领域分组的高级工具

UE 端工具按领域 (domain) 分组，当前可用 domain: **level**, **blueprint**, **umg**, **edgraph**, **behaviortree**, **slate**。

```
# 1. 发现所有 domain
ue_list_tools(domain="any_invalid")   # 错误信息会列出可用 domain
# 或
ue_call("get_dispatch", {"domain": ""})

# 2. 查看某个 domain 下的工具
ue_list_tools(domain="level")

# 3. 调用 domain 工具
ue_call("get_actors_in_level", {}, domain="level")
ue_call("spawn_actor", {"actor_class": "/Script/Engine.StaticMeshActor"}, domain="level")
```

### UE 离线时: 代理工具返回引导

```
ue_run_python(...) -> "No active UE instance online. Use launch_editor() to start..."
```

### 多实例场景

```
discover_instances()                                 # 查看所有实例
manage_instance(action="use", instance="ue2")        # 切换到第二个实例
ue_run_python(...)                                   # 自动在 ue2 上执行
```

### 崩溃恢复

```
get_log(source="crash")                              # 查看崩溃报告
launch_editor(action="restart")                      # 重启编辑器
get_session(scope="notes")                           # 恢复上下文
```

### 编译 + 打包

```
build_project()                                      # 默认 compile
build_project(action="cook", platform="Win64")       # 打包
get_log(source="build")                              # 查看构建日志
```

## 关键行为准则

1. **配置优先**: 任何 UE 操作前确认项目已配置，未配置时引导用户调用 `setup_project`
2. **代理优先**: 常用操作优先用 `ue_run_python`，不常用的先 `ue_list_tools` 查再 `ue_call` 调
3. **崩溃韧性**: 收到离线/崩溃提示时不要放弃，按流程: `get_log(source="crash")` -> `launch_editor(action="restart")` -> 恢复
4. **保持笔记**: 重要操作或发现用 `add_note` 记录，崩溃后用 `get_session` 恢复上下文
5. **编译前置**: 修改 C++ 代码后，先 `build_project()` 再 `launch_editor()`
6. **单实例无感知**: 大多数情况下只有一个 UE 实例，不需要调用 `manage_instance`
7. **Domain 探索**: 需要操作关卡/蓝图/UI 等高级功能时，先 `ue_list_tools(domain="...")` 查看可用域工具
