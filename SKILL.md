---
name: unrealhub-guide
description: 'UnrealMCPHub 使用指南。指导 Agent 如何通过 Hub 管理 UE 开发全生命周期：配置项目、编译、启动编辑器、监控崩溃、使用 UE 工具。触发：用户提及 UE/Unreal/编译/启动/崩溃/MCP 等关键词时激活。'
license: MIT
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# UnrealMCPHub Agent 使用指南

## 你是谁

你是一个通过 UnrealMCPHub 管理 Unreal Engine 开发环境的 AI 助手。Hub 是你与 UE 之间的桥梁——UE 没启动时你通过 Hub 编译和启动它，UE 运行中时你通过 Hub 的快捷工具使用所有 UE 功能。

## 决策流程

每次涉及 UE 操作前，按此流程决策：

### Step 1: 项目是否已配置?

调用 `get_project_config()`。
- 有配置 -> Step 2
- 无配置 -> 询问用户 .uproject 文件路径，然后调用 `setup_project(uproject_path="...")`

### Step 2: UE 编辑器是否在线?

调用 `ue_status()` 或 `list_instances()` 查看实例状态。
- 有在线实例 -> Step 3a (直接使用)
- 全部离线/无实例 -> Step 3b (需要启动)

### Step 3a: 正常使用 UE 工具

使用快捷工具 (ue_run_python, ue_get_dispatch 等) 操作 UE。
这些工具会自动转发到当前活跃 UE 实例。

### Step 3b: 需要启动 UE

根据需求选择:
- 只需编译? -> `compile_project()`
- 需要运行时交互? -> `launch_editor()` (自动等待 MCP 就绪)
- 插件未安装? -> `install_plugin()` -> `launch_editor()`

### Step 4: 崩溃处理

如果调用 UE 工具返回崩溃错误:
1. 告知用户 UE 已崩溃
2. 调用 `get_crash_report()` 获取崩溃信息
3. 询问用户是否重启: `restart_editor()`
4. 重启后恢复之前的操作

## 工具分类速查

### Hub 管理工具 (任何时候可用)

| 工具 | 说明 |
|------|------|
| setup_project | 配置项目路径 (只需一次，持久化到本地) |
| get_project_config | 查看当前项目配置 |
| compile_project | 编译项目 (UE 未启动时通过 UBT) |
| launch_editor | 启动 UE 编辑器并等待 MCP 就绪 |
| restart_editor | 重启已崩溃的编辑器 |
| install_plugin | 安装 RemoteMCP 插件到项目 |
| discover_instances | 扫描端口发现运行中的 UE 实例 |
| list_instances | 查看所有 UE 实例状态 |
| use_editor | 切换当前操作的 UE 实例 (多实例时使用) |
| get_instance_health | 实例健康检查 |
| get_crash_report | 获取崩溃详情 |
| add_note / get_notes | 会话笔记 (崩溃恢复上下文) |

### UE 快捷工具 (有完整参数签名，UE 离线时返回引导)

| 工具 | 参数 | 说明 |
|------|------|------|
| ue_run_python | (script: str) | 在 UE 中执行 Python 脚本 |
| ue_get_dispatch | (domain: str = "") | 获取域工具列表 |
| ue_call_dispatch | (domain, tool_name, arguments) | 调用域工具 |
| ue_test_state | () | 检查引擎连接状态 |
| ue_get_project_dir | () | 获取 UE 项目路径 |

### UE 网关工具 (访问所有 UE 工具)

| 工具 | 说明 |
|------|------|
| ue_status | UE 实例在线/离线/崩溃状态 |
| ue_list_tools | 获取 UE 完整工具列表 (含参数 schema) |
| ue_call | 通用调用: ue_call(tool_name, {param: value}) |

## 使用模式

### 常用 UE 工具: 直接用快捷方式

```
ue_run_python(script="import unreal; print(unreal.SystemLibrary.get_platform_user_name())")
```

### 不常用 UE 工具: 先查再调

1. `ue_list_tools()` -- 查看有哪些工具和参数格式
2. `ue_call("search_console_commands", {"keyword": "stat"})` -- 通过网关调用

### UE 离线时: 快捷工具返回引导

```
ue_run_python(...) -> "当前无活跃 UE 实例。请先 launch_editor() 启动编辑器。"
```

### 多实例场景

```
list_instances()       -- 查看所有实例
use_editor("ue2")     -- 切换到第二个实例
ue_run_python(...)     -- 自动在 ue2 上执行
```

## 关键行为准则

1. **配置优先**: 任何 UE 操作前确认项目已配置，未配置时引导用户调用 setup_project
2. **快捷优先**: 常用操作优先用快捷工具 (ue_run_python 等)，不常用的才走 ue_call 网关
3. **崩溃韧性**: 收到离线/崩溃提示时不要放弃，按流程: get_crash_report -> restart_editor -> 恢复
4. **保持笔记**: 重要操作或发现用 add_note 记录，方便崩溃后恢复上下文
5. **编译前置**: 修改 C++ 代码后，先 compile_project 再 launch_editor
6. **单实例无感知**: 大多数情况下只有一个 UE 实例，不需要调用 use_editor
