# Unreal Capability Gym 现状总结

## 一句话结论

目前 `Unreal Capability Gym` 已经完成了前四项 baseline 验证，`Gym-05` 也已经明确了边界和缺口。  
也就是说，这条线已经从“概念和规划”进入了“有真实证据支撑的可用性验证阶段”。

## 当前状态

### 已完成 baseline 的项目

- `Gym-01` `Lighting Readability`
  - 证明了 lighting baseline、controlled scene、camera-anchored capture 是可行的
  - 更适合被表述为“基础链路验证通过”，而不是最终 hero showcase

- `Gym-02` `3D Space Readability`
  - 证明了局部 3D 空间可以通过自动化修改变得更易读
  - `before/after` 证据已经有效

- `Gym-03` `3D Gameplay Feedback`
  - 证明了轻量 `Actor / Trigger` 路线可行
  - feedback 场景已经可以通过结构化工具跑出真实可见差异

- `Gym-04` `3D Combat Encounter`
  - 证明了 static encounter proxy 路线可行
  - 即使不做完整 combat system，也可以先验证 combat encounter readability

### 已定义但尚未通过的项目

- `Gym-05` `3D Animation / Locomotion`
  - brief 已定义
  - 当前边界已明确
  - 但还缺一个更合适的角色/动画 showcase 载体

## 这条线真正证明了什么

当前 Gym 真正证明的不是“AI 已经会完整做 Unreal 游戏”，而是：

- 结构化 MCP 工具已经足够支撑多种 3D baseline modify 任务
- controlled scene + camera-anchored capture 已经形成一条可复用证据路径
- 轻量 baseline 可以先通过 readability、feedback、encounter proxy 这些路径验证，而不需要一开始就做重系统
- animation / locomotion 这类更贴近角色体验的域，需要更合适的标准资产或 sample 工程支撑

## 当前最重要的工具层结论

目前已经跑通并反复验证过的底座包括：

- map lifecycle
- scene/testbed construction
- evidence capture
- health / reconnect baseline
- lighting foundation

同时也已经明确了一些重要边界：

- map transition 应视为 `session-disrupting`
- 一个工程应保持一个活跃 editor 实例参与 baseline 验证
- tool success 不等于 evidence 有效，截图和场景 sanity check 仍然重要

## 为什么这很重要

因为这意味着我们现在已经不只是“能把工具接起来”，而是已经开始拥有：

- 可复用的 Gym baseline 路线
- 可描述的能力边界
- 可积累的证据结构
- 后续撰写可用性报告的稳定输入

## 近期最值得做的事

- 整理第一版 figure-rich feasibility report
- 给 `Gym-05` 找一个标准角色资产或更合适的 sample 工程
- 继续把 `RemoteMCP` 的稳定语义回接到 Hub workflow 和 gym 示例里
- 逐步减少临时 PowerShell client，收敛成更稳定的 external runner

## 对外可用的表述方式

如果要给团队或外部合作者快速说明当前状态，最准确的说法是：

> `Unreal Capability Gym` 已经完成前四项 baseline 验证，证明了 AI + structured MCP tools 在 Unreal 里的多种 3D modify 任务已经可用；第五项动画/位移能力的边界也已明确，下一步重点将转向更完整的图文可用性报告与更合适的 locomotion showcase 载体。
