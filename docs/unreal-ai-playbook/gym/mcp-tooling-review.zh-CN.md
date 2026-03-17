# MCP Tooling Review For Gym

## 目的

这份文档回答两个问题：
- 当前 `UnrealMCPHub + RemoteMCP` 这套工具，对于 Gym 来说好不好用
- 如果要继续推高自动化边界，优先该改哪些地方

## 当前优点

### 1. 接入层已经够用

当前已经证明：
- Hub 侧项目配置、发现、preflight、benchmark-lite 是可用的
- RemoteMCP 的基本链路是稳定的
- 工具枚举、基础 metadata、基础 execution 都能跑

这说明：
- 这套工具不是“不能做 Gym”
- 它已经足够支持 baseline 级别的自动化验证

### 2. 现有工具对“查状态”很有帮助

比如：
- `get_unreal_state`
- `get_dispatch`
- `search_domain_tools`
- `call_dispatch_tool`

这类工具让我们可以比较快地判断：
- 当前实例是否健康
- 某个 domain 是否真的在线
- 当前更适合做什么级别的自动化

### 3. 轻量自动化链路可用

最近的 Gym-01 测试已经证明：
- map load
- actor query
- property change
- save
- screenshot
- 多轮 loop  
在轻量场景里是可以工作的

## 当前缺口

### 1. 太依赖 `run_python_script`

这是当前最大问题。

一旦需要：
- 新图
- 场景搭建
- lighting rig
- 截图
- Post Process  
很多事情都只能回退到长 Python 脚本

结果就是：
- 自动化路径很强
- 但结构化程度不足
- 一旦崩，难以定位

### 2. 场景和 lookdev 缺少高频封装

当前缺的是：
- map 工具
- testbed 搭建工具
- lighting preset 工具
- capture 工具
- PPV 工具

也就是说：
当前工具更像“通用接线板”，还不像“面向 Gym 的操作面”

### 3. 对 Python 反射边界暴露过多

典型例子：
- `PostProcessVolume`
- 某些 editor-only 属性
- 模板建图签名

这些对 AI 来说是糟糕边界，因为：
- 调用前无法预知属性名是否可写
- 报错偏底层
- 很容易把试验变成“猜 API”

### 4. 缺少任务级事务与 checkpoint

现在如果一段 Gym 脚本做：
- create
- modify
- save
- screenshot

失败后：
- 没有天然 checkpoint
- 没有 rollback
- 很难快速缩边界

## 当前最需要改什么

### P0

- 把高频 Gym 操作从长 Python 脚本里抽出来
- 先补 map / scene / lighting / capture 四类结构化工具

### P1

- 给高风险对象加安全 wrapper
  - 比如 PPV
  - atmosphere
  - fog

### P2

- 给多步操作加最小 checkpoint / step log

## 对 MCP 工具本身的建议

我当前的判断是：

### 保持不变的

- `benchmark-preflight`
- `benchmark-lite`
- discovery / probe / status 这类基础设施

这些已经是当前 workflow 的强项，不应该轻易推翻。

### 需要增强的

- 结构化 scene/build tools
- 结构化 capture tools
- Gym preset tools
- 更好的错误分级
- 更清晰的对象属性 introspection

### 可能要改思路的

- 不要再把所有“高级编辑器能力”都默认压到 `run_python_script`
- 对 Gym 来说，更合适的是：
  - 少量稳定、可组合、可重复的专用工具
  - 再由文档和模板把它们编排起来

## 当前结论

如果问这套 MCP 工具“好不好用”：

- 对 benchmark 和基础自动化来说：好用
- 对 Gym baseline 来说：已经够用
- 对 Gym 高阶展示和独立场景编排来说：还缺一层结构化工具

所以现在最应该做的不是“换工具”，而是：

**在当前 MCP 之上补一层面向 Gym 的结构化工具入口。**
