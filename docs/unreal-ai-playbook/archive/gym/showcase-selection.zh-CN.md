# Showcase Selection Notes

## 当前机器上的可用载体

当前本机可发现的 Unreal 项目里，最适合用于 Gym showcase 的有两类：

### 1. 当前外部 benchmark 工程

- `F:\MCPtest\TestMCP\TestMCP.uproject`

优点：
- 已经跑通 `vampire-survivors-v1` 风格 benchmark
- 已经有 combat arena、敌人、波次、XP、升级和 HUD
- 已经有 package 证据
- 后续修改成本最低

限制：
- 视觉表现更偏 benchmark prototype，而不是 Epic 官方高保真 demo

### 2. 引擎自带模板

例如：
- `TP_TopDownBP`
- `TP_ThirdPersonBP`
- `TP_FirstPersonBP`
- `TP_UEIntro_BP`

优点：
- 更标准化
- 更容易复刻

限制：
- 当前本机没有现成的重型 showcase sample，例如 Lyra 或 Stack O Bot
- 如果从模板重新搭 combat showcase，前期成本会高于直接复用 `TestMCP`

## 按需安装的重型官方样本

当前更现实的策略不是一次性全装，而是按 Gym 域逐步引入。

### `GASP` / Game Animation Sample

可获取性：
- 官方文档说明可从 Fab 下载，并在 Epic Games Launcher 的 Library/Vault 中创建项目。

当前 workflow 友好度：
- 较高
- 更适合后续 `animation`、`locomotion`、`gameplay feel`、`traversal` 类 showcase
- 不太适合作为当前 `combat` 的首个 showcase 载体

原因：
- 它的优势是高保真移动与动作系统
- 与当前已经跑通的 combat benchmark 主循环相比，切入成本更高

### `Stack O Bot`

可获取性：
- 官方文档说明可从 Fab 添加到库后在 Launcher/Fab Library 创建项目。
- 官方文档还给出了推荐 PC 规格，说明它是正式可分发 sample。

当前 workflow 友好度：
- 中高
- 更适合 `level-design`、`lighting`、`interaction`、`traversal` 类 modify showcase

原因：
- 比 Lyra 轻，更适合展示空间和关卡层面的局部修改
- 但对当前 `Gym-01 Combat Modify` 来说，仍然不如直接复用 `TestMCP` 划算

### `Lyra`

可获取性：
- 官方文档说明同样通过 Fab + Launcher 获取。

当前 workflow 友好度：
- 当前阶段偏低，但长远价值高

原因：
- 它更重，也更系统化
- 更适合后面做正式 combat/system/UI/ability 方向的 Gym
- 不适合当前“轻量、快速出第一份 showcase 证据”的目标

## 当前推荐策略

当前优先顺序：

1. 先用轻量、稳定、可反复修改的 3D 场景完成 `Gym-01 Lighting Readability Modify`
2. 再用同类稳定场景推进 `Gym-02 Space Readability Modify`
3. 后续若做动作表现类 Gym，再按需安装 `GASP`
4. 若做更正式的空间/关卡 showcase，再按需安装 `Stack O Bot`
5. 若进入更正式的 combat/system showcase，再考虑 `Lyra`

这样可以同时满足：
- 轻量启动
- 尽量复用已有成果
- 先铺开 baseline track
- 只在需要时引入更重的官方样本

## 当前选择

当前阶段，`Gym-01` 和 `Gym-02` 的默认载体应优先满足：

- 3D 场景稳定
- before/after 机位容易固定
- 适合小范围 modify
- 不强依赖复杂 gameplay loop

这也是为什么当前更推荐：
- 先完成 `lighting/readability`
- 再完成 `space/readability`
- 不把第一批 baseline 直接绑在 combat benchmark 上

## 后续扩展策略

如果后续本机增加了更成熟的 Unreal sample，可按下面顺序扩展：

1. 继续用 `TestMCP` 做轻量 combat/showcase 验证
2. 用引擎模板做 `lighting`、`ui` 这类更轻的 modify 任务
3. 如果安装了 Lyra、Stack O Bot 或其他高质量 sample，再把 Gym 拓展到更强展示载体

## 参考来源

- [Game Animation Sample Project in Unreal Engine](https://dev.epicgames.com/documentation/unreal-engine/game-animation-sample-project-in-unreal-engine)
- [Stack O Bot sample game documentation](https://dev.epicgames.com/documentation/zh-cn/unreal-engine/stack-o-bot-sample-game-in-unreal-engine)
- [Lyra Sample Game in Unreal Engine](https://dev.epicgames.com/documentation/es-mx/unreal-engine/lyra-sample-game-in-unreal-engine)
- [Samples and Tutorials for Unreal Engine](https://dev.epicgames.com/documentation/unreal-engine/samples-and-tutorials-for-unreal-engine)
