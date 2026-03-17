# Gym Tooling Backlog

## 目的

这份 backlog 专门记录：
- 为了让 `Capability Gym` 自动化稳定运行，我们当前缺哪些结构化工具入口
- 哪些地方不该继续依赖长 `run_python_script`
- 哪些能力应优先补，才能把 Gym 从“能试”推进到“能稳定复现”

这份文档默认落在 `codex/lab`，因为它代表的是实验和能力边界推进，而不是稳定主线。

## 当前判断

`Gym-01` 的最近几轮测试已经说明：

- 轻量自动化链路是可用的
  - `load map`
  - `actor query`
  - `single property change`
  - `save`
  - `screenshot`
  - `reload + modify + save + screenshot`

- 真正的边界不在“有没有自动化”，而在：
  - 过度依赖 `run_python_script`
  - 新地图创建和模板复制缺少稳定的结构化入口
  - `PostProcessVolume` 等对象的属性访问缺少安全 schema

结论：
现在最值得做的不是继续堆更长 Python，而是补一层更结构化的 Gym 工具。

## 一级优先级：必须尽快补

### 1. 地图生命周期工具

问题：
- 新图创建、模板建图、保存地图目前都要靠 Python API 猜签名
- 这类操作一旦串联，很容易把编辑器推到高风险区

建议新增：
- `create_blank_map(asset_path)`
- `create_map_from_template(asset_path, template_path)`
- `load_map(asset_path)`  
  作为显式结构化工具，而不是只靠脚本
- `save_current_map()`
- `save_map_as(asset_path)`

Gym 价值：
- 支撑 Gym 独立 testbed
- 让 `__Gym` 资产根能稳定建立

### 2. 最小场景搭建工具

问题：
- 现在要搭一个 lighting baseline 场景，只能用 Python 手工 spawn mesh actor

建议新增：
- `spawn_static_mesh_actor(mesh_path, label, location, rotation, scale)`
- `delete_actors_by_prefix(prefix)`
- `reset_testbed(prefix_or_tag)`
- `ensure_capture_camera(label, location, target_or_rotation)`

Gym 价值：
- 让 baseline 场景搭建可重复
- 不用再把几何测试场景写成长脚本

### 3. Lighting Rig 工具

问题：
- 当前 lighting/readability pass 仍然太靠直接改属性

建议新增：
- `create_basic_lighting_rig()`
- `apply_time_of_day_preset(preset_name)`
- `apply_lighting_readability_pass(target_area, preset_name)`
- `set_directional_light(...)`
- `set_skylight(...)`
- `set_exponential_fog(...)`

Gym 价值：
- 让 `Gym-01` 不再依赖临时脚本
- 未来 `Gym-02`、`Gym-03` 也可以复用

### 4. 证据采集工具

问题：
- 机位、截图、路径、命名目前都靠脚本拼装

建议新增：
- `capture_viewport(image_path, camera_label=None)`
- `capture_before_after(prefix, camera_label, step_name)`
- `set_editor_camera(location, rotation_or_target)`
- `export_gym_artifact_stub(...)`

Gym 价值：
- before / after 采集标准化
- 图文报告输入更稳

## 二级优先级：应该尽快规划

### 5. Post Process 工具

问题：
- 目前 `PostProcessVolume` 反射接口就是 Gym-01 的第一条明确边界

建议新增：
- `ensure_post_process_volume(label, unbound=True)`
- `set_post_process_overrides(...)`
- `apply_mood_post_process_preset(preset_name)`

Gym 价值：
- Lighting baseline 可以更像真正 showcase
- 后续 mood / weather / readability 都会受益

### 6. 事务化多步操作

问题：
- 目前一段脚本里混：
  - 建图
  - 搭场景
  - 保存
  - 截图  
  失败后很难知道是哪一步炸

建议新增：
- `begin_gym_session(name)`
- `record_step(name, status, notes)`
- `checkpoint_map(label)`
- `rollback_to_checkpoint(label)`  
  即使是轻量版也值得先设计

Gym 价值：
- 更快定位边界
- 更适合写可用性报告

## 三级优先级：后续高级化

### 7. 天气 / 氛围预设工具

建议方向：
- `apply_weather_preset('golden_hour' | 'overcast' | 'night' | 'storm_prelude')`
- `apply_atmosphere_preset(...)`

用途：
- 让 lighting Gym 更展示化
- 后续也能给 `Advanced Track` 打基础

### 8. Gym 原生场景脚手架

建议方向：
- `create_gym_lighting_testbed(asset_path)`
- `create_gym_space_testbed(asset_path)`
- `create_gym_feedback_testbed(asset_path)`

用途：
- 让 Gym 逐步摆脱 benchmark map
- 形成真正独立的 Gym Sandbox

## 当前推荐顺序

1. 地图生命周期工具
2. 最小场景搭建工具
3. Lighting Rig 工具
4. 证据采集工具
5. Post Process 工具

## 这部分预期放在哪里实现

当前最合理的落点是：

- 文档与规划：
  - `docs/unreal-ai-playbook/gym/`

- 稳定后的执行模板：
  - `skills/team-unreal-workflow/references/`

- 真正的工具实现：
  - `src/unrealhub/` 下新的 Gym / scene / capture / lighting 工具模块
  - 或 `src/unrealhub/tools/` 下的结构化新工具入口

换句话说：
- 现在先在 docs 里定义 backlog
- 真正稳定后，应该进 Hub 的结构化工具层，而不是永远停留在脚本层
