# Unreal MCP 运行时验证矩阵

## 快照信息

- 日期：2026-03-17
- 项目：`F:\MCPtest\TestMCP\TestMCP.uproject`
- UE 进程：`UnrealEditor` 运行中
- MCP 端点：`http://127.0.0.1:8422/mcp`
- 插件状态：编辑器内 `MCP.State` 先前已确认 `RemoteMCP Running`

## 本次验证方法

本次矩阵按两层验证：

1. 元数据层
   - 列出顶层工具
   - 调用 `get_dispatch`
   - 调用 `get_dispatch(domain=...)`
2. 执行层
   - 对顶层工具和每个 domain 选择一个最小调用做采样
   - 记录结果为 `validated` / `unvalidated` / `known-risk`

说明：
- `validated`：工具已列出，且真实调用成功
- `unvalidated`：工具已列出，但本轮还没做有效调用验证
- `known-risk`：工具已列出，但真实调用超时、失败，或当前环境明显不稳定

## 顶层工具概况

当前列出的顶层工具共 10 个：

- `run_python_script`
- `run_python_script_async`
- `search_console_commands`
- `run_console_command`
- `get_unreal_state`
- `reload_all_tool`
- `search_domain_tools`
- `get_dispatch`
- `call_dispatch_tool`
- `livecoding_compile_and_get_ubt_log`

结论：
- 工具枚举链路正常
- 说明 MCP 会话初始化和 metadata 读取正常
- 但不代表执行链路正常

## Domain 规模

| Domain | 工具数 | 当前判断 |
|---|---:|---|
| `level` | 10 | `known-risk` |
| `blueprint` | 16 | `known-risk` |
| `umg` | 6 | `unvalidated` |
| `edgraph` | 9 | `unvalidated` |
| `behaviortree` | 9 | `unvalidated` |
| `slate` | 22 | `known-risk` |

## 逐项验证

### 顶层工具

| 工具 | 采样结果 | 状态 | 备注 |
|---|---|---|---|
| `get_dispatch` | 成功 | `validated` | 成功返回 6 个 domain |
| `get_unreal_state` | 12 秒超时 | `known-risk` | metadata 正常但状态读取未返回 |
| `search_console_commands` | 12 秒超时 | `known-risk` | 当前环境下执行链路不稳 |

### `level`

- 已列出工具：`get_actors_in_level`、`spawn_actor`、`delete_actor`、`focus_viewport` 等
- 采样调用：`get_actors_in_level`
- 结果：12 秒超时
- 状态：`known-risk`

判断：
- `level` domain 已暴露
- 但当前实例下读取关卡 Actor 列表都超时，说明不适合直接进入重型 benchmark

### `blueprint`

- 已列出工具：`create_blueprint`、`compile_blueprint`、`add_component_to_blueprint` 等
- 采样调用：`compile_blueprint`
- 结果：12 秒超时
- 状态：`known-risk`

判断：
- `blueprint` domain 已暴露
- 当前环境下蓝图相关调用没有在低超时窗口内返回

### `umg`

- 已列出工具：`create_umg_widget_blueprint`、`add_text_block_to_widget`、`add_button_to_widget` 等
- 本轮采样：初次探针使用了错误工具名 `create_widget_blueprint`
- 结果：返回“tool not found”，暴露的真实工具名是 `create_umg_widget_blueprint`
- 状态：`unvalidated`

判断：
- `umg` domain 元数据正常
- 本轮没有完成一条有效的最小成功调用
- 需要后续用 sandbox widget 任务做二次验证

### `edgraph`

- 已列出工具：`edgraph_find_graphs_in_asset`、`edgraph_list_nodes`、`edgraph_connect_pins` 等
- 本轮采样：初次探针使用了错误工具名 `list_nodes`
- 结果：返回“tool not found”，暴露的真实工具名是 `edgraph_list_nodes`
- 状态：`unvalidated`

判断：
- `edgraph` domain 元数据正常
- 需要基于一个已知蓝图资产再做最小读操作验证

### `behaviortree`

- 已列出工具：`bt_get_graph`、`bt_create_asset`、`bt_list_graph_nodes` 等
- 本轮采样：初次探针使用了错误工具名 `get_all_behavior_trees`
- 结果：返回“tool not found”，说明当前域名工具集与预期探针不一致
- 状态：`unvalidated`

判断：
- `behaviortree` domain 元数据正常
- 需要对一个真实 BT/Blackboard 资产执行最小查询验证

### `slate`

- 已列出工具：`slate_get_active_window`、`slate_get_all_windows`、`slate_get_all_dock_tabs` 等共 22 个
- 采样调用：`slate_get_active_window`
- 结果：12 秒超时
- 状态：`known-risk`

判断：
- `slate` 能列出大量工具，但当前 UI 查询链路明显偏慢
- 不适合在当前机器上默认做大范围 Slate 树遍历

## 结论

本机当前更接近以下状态：

- metadata 链路：`validated`
- execution 链路：`degraded`

也就是说：

- 可以稳定读取顶层工具和 domain 结构
- 但真实执行调用大面积超时
- 当前更适合：
  - `L0 smoke`
  - 限制版 `L1 sandbox`
  - `low-overhead` 模式
- 当前不适合直接进入：
  - 大范围 UI/Slate 遍历
  - 重型关卡查询
  - 完整 `vampire-survivors-v1`

## 下一步建议

1. 把这份矩阵作为 `benchmark preflight` 的当前基线。
2. 先只补 3 条更精准的二次验证：
   - `umg.create_umg_widget_blueprint`
   - `edgraph.edgraph_find_graphs_in_asset`
   - `behaviortree.bt_get_graph` 或 `bt_list_graph_nodes`
3. 保持所有后续 benchmark 默认走 `low-overhead` 模式。
4. 只有当至少一个顶层执行工具和两个 domain 调用从超时变成成功后，再往 `L2` 提升。
