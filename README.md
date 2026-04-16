# UnrealMCPHub

Central management platform for Unreal Engine MCP instances — bridge between AI agents and UE across the full development lifecycle.

Works with **[RemoteMCP](https://github.com/blackplume233/UnrealRemoteMCP)** (UE Editor plugin that exposes engine capabilities via MCP protocol). The Hub manages everything around it: install the plugin, compile, launch the editor, detect crashes, and transparently proxy all tool calls — so the AI agent only needs one MCP endpoint.

```
AI Agent ──► UnrealMCPHub ──► UE Editor + RemoteMCP plugin
              (this repo)       (blackplume233/UnrealRemoteMCP)
                                    └── ECABridge (238+ atomic commands)
```

> **RemoteMCP** runs **inside** UE Editor and provides 22+ tools across 7 domains (level, blueprint, umg, edgraph, behaviortree, slate, eca).
> **ECABridge** is an engine-level experimental plugin providing 238+ C++ atomic commands, accessed through RemoteMCP's `eca` domain.
> **UnrealMCPHub** runs **outside** UE Editor and can compile, launch, monitor, and proxy — even when UE is not running.

## How It Works

`UnrealMCPHub` and `UnrealRemoteMCP` are complementary layers, not competing projects.

- **UnrealRemoteMCP** lives inside Unreal Editor and exposes engine-facing tools.
- **ECABridge** (engine built-in) provides 238+ atomic C++ commands for Mesh, Niagara, Material, BlueprintLisp, MVVM, WidgetTree, etc.
- **UnrealMCPHub** lives outside Unreal Editor and manages the development lifecycle around those tools.

In practice, the flow looks like this:

1. The AI client connects to `UnrealMCPHub`.
2. The Hub configures the Unreal project, installs or verifies the plugin, compiles, and launches the editor when needed.
3. Once the editor is ready, the Hub forwards UE-facing requests to `UnrealRemoteMCP`.
4. `UnrealRemoteMCP` executes the actual in-editor work (including ECA commands) and returns results through the Hub.

In short: `UnrealRemoteMCP` is the in-editor capability layer, `ECABridge` is the atomic command library, and `UnrealMCPHub` is the control plane around them.

## About This Fork

This fork keeps upstream UnrealMCPHub as the base, adding:

- **ECA Bridge awareness** — `hub_status` shows ECA availability, `help(topic="eca")` provides usage guide
- **Team workflow docs** under [`docs/unreal-ai-playbook/`](./docs/unreal-ai-playbook/)
- **Benchmark framework** under [`skills/ue-benchmark/`](./skills/ue-benchmark/) with scenario-based evaluation
- **Enhanced Skills** — Part 10 (ECA Bridge) added to `use-unrealhub` SKILL.md

Branch roles:

- `main`: stable fork baseline tracking upstream + fork-approved changes
- `feature/eca-awareness`: Sprint 3 — Hub ECA integration (tool descriptions, hub_status, SKILL.md)

## Features

- **Project setup** – Configure `.uproject` once; engine auto-detected from registry
- **Build & launch** – Compile via UBT, launch editor, wait for MCP readiness
- **Plugin install** – One-click RemoteMCP installation (local copy or GitHub download)
- **Instance discovery** — Two-phase port scan + serverInfo verification + psutil process matching
- **UE tool proxy** — `ue_run_python`, `ue_call`, `ue_list_tools`, `ue_list_domains` with domain dispatch
- **ECA awareness** — `hub_status` shows ECA Bridge status (238+ commands, 19 categories)
- **Crash resilience** — PID watcher, crash guard racing, crash log retrieval, restart flow
- **Multi-instance** — Switch between multiple UE editors via `manage_instance`
- **Session notes** — Persist context for crash recovery
- **One-click overview** — `hub_status` shows project, plugin, instances, ECA, and watcher state
- **Help system** — `help(topic)` with 10 topics including ECA guide

## Quick Install

### Option A: One-line install from PyPI (recommended)

```bash
# uv (recommended)
uv tool install unrealhub

# or pip
pip install unrealhub
```

Then add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "unrealhub",
      "args": ["serve"]
    }
  }
}
```

### Option B: Zero-install (auto-fetch on first launch)

No download, no clone, no install. Paste this single block into `.cursor/mcp.json` and restart Cursor:

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "uvx",
      "args": ["unrealhub", "serve"]
    }
  }
}
```

> Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) (`pip install uv` or `winget install astral-sh.uv`). Cursor will auto-fetch the Hub on first launch.

### Option C: Standalone executable (no Python needed)

Download the latest executable for your platform from [GitHub Releases](https://github.com/blackplume233/UnrealMCPHub/releases), then:

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "/path/to/unrealhub",
      "args": ["serve"]
    }
  }
}
```

| Platform | File |
|----------|------|
| Windows x64 | `unrealhub-windows-amd64.exe` |
| macOS ARM | `unrealhub-macos-arm64` |
| Linux x64 | `unrealhub-linux-amd64` |

### Option D: Clone for development

```bash
git clone https://github.com/blackplume233/UnrealMCPHub.git
cd UnrealMCPHub
uv sync          # or: pip install -e .
```

```json
{
  "mcpServers": {
    "unrealhub": {
      "command": "uv",
      "args": ["--directory", "/path/to/UnrealMCPHub", "run", "unrealhub", "serve"]
    }
  }
}
```

## Quick Start

### For AI Clients (Cursor / Claude / CodeBuddy / Codex / etc.)

This is the primary use case. Add UnrealMCPHub as an MCP server in any MCP-capable AI client, then let the agent handle the Unreal workflow through natural language.

**Step 1: Install & Configure MCP** (see [Quick Install](#quick-install) above)

**HTTP mode** (for shared / remote / multi-client use):

```bash
unrealhub serve --http --port <hub-port>
```

```json
{
  "mcpServers": {
    "unrealhub": {
      "url": "http://<hub-host>:<hub-port>/mcp"
    }
  }
}
```

**Step 2: Talk to the agent**

Once configured, the AI agent has full access to all Hub tools. Example conversations:

```
You: "帮我编译并启动 UE 项目 D:/Projects/MyGame/MyGame.uproject"
Agent: [calls setup_project, build_project, launch_editor automatically]

You: "用 Blueprint Lisp 给 BP_Player 加一个 BeginPlay 事件"
Agent: [calls ue_call with domain="eca", uses lisp_to_blueprint]

You: "UE 崩溃了怎么办"
Agent: [calls get_log(source="crash"), shows crash info, offers launch_editor(action="restart")]
```

**Step 3: What happens behind the scenes**

```
Agent → Hub (setup_project)     # One-time project config, persisted
Agent → Hub (build_project)     # Compiles via UBT, even without UE running
Agent → Hub (launch_editor)     # Starts UE, waits for MCP readiness
Agent → Hub (ue_call)           # Hub forwards to UE's RemoteMCP
                ↓
        UE Editor (RemoteMCP endpoint)   # Executes tool, returns result
                ↓
        ECABridge (238+ commands)        # Accessed via RemoteMCP eca domain
```

The agent only needs to know about the Hub — it never talks to UE directly.

### AI Agent Decision Flow

```
Is project configured?
├── No  → Ask user for .uproject path → setup_project()
└── Yes → Is UE Editor online?
          ├── No  → launch_editor() (auto-compiles first)
          └── Yes → Use ue_* tools directly
                    ├── ue_list_domains() → discover available domains (incl. eca)
                    ├── ue_call(domain="eca", ...) → 238+ ECA commands
                    └── Crashed? → get_log(source="crash") → launch_editor(action="restart")
```

### For Humans (CLI)

```bash
unrealhub setup /path/to/MyProject.uproject    # Configure project
unrealhub serve                                 # Start MCP server (stdio)
unrealhub serve --http --port <hub-port>        # Start MCP server (HTTP)
unrealhub status                                # Show instance status
unrealhub discover                              # Discover running UE instances
unrealhub compile                               # Build active project
unrealhub launch                                # Launch editor
```

## Tool Reference

### Hub Management (always available, even without UE)

| Tool | Description |
|------|-------------|
| `setup_project` | One-stop project onboarding: configure + install plugin |
| `get_project_config` | View current project configuration |
| `remove_project` | Remove a project configuration |
| `hub_status` | One-stop overview: project, plugin, instances, ECA, watcher |
| `build_project` | Compile project via UBT (with streaming progress) |
| `launch_editor` | Start/stop/restart UE Editor, wait for MCP readiness |
| `discover_instances` | Two-phase port scan + auto-registration |
| `manage_instance` | Register/unregister/switch active instance |
| `get_instance_health` | Detailed health check (PID, CPU, memory, MCP probe) |
| `get_log` | Read UBT, editor, or crash logs |
| `add_note` / `get_session` | Session notes and call history for crash recovery |
| `help` | Usage guide by topic (compile, launch, pie, slate, eca, etc.) |

### UE Proxy Tools (forwarded to active UE instance)

| Tool | Description |
|------|-------------|
| `ue_status` | Active instance status |
| `ue_list_domains` | List all domains with descriptions (level, blueprint, ..., eca) |
| `ue_list_tools` | List tools from UE instance (MCP-level or domain-specific) |
| `ue_call` | Call any UE tool by name, with optional domain dispatch |
| `ue_run_python` | Execute Python script in UE Editor |

## Architecture

```
┌─────────────────┐     stdio/HTTP      ┌──────────────────┐
│  Cursor / Agent │ ◄─────────────────► │  UnrealMCPHub    │
└─────────────────┘                     │  (FastMCP Server) │
                                        └────────┬─────────┘
                                                 │
                 ┌───────────────────────────────┼───────────────────────────────┐
                 │                               │                               │
                 ▼                               ▼                               ▼
         ┌───────────────┐              ┌───────────────┐              ┌───────────────┐
         │ Project Mgmt  │              │ Lifecycle     │              │ UE Proxy      │
         │ setup_project │              │ build_project │              │ ue_run_python  │
         │ hub_status    │              │ launch_editor │              │ ue_call        │
         │ help          │              │ discover      │              │ ue_list_domains│
         └───────────────┘              └───────┬───────┘              └───────┬───────┘
                 │                              │                              │
                 ▼                              │  Streamable HTTP             │
         ┌───────────────┐              ┌──────▼──────────────────────────────▼────────┐
         │ ~/.unrealhub  │              │  UE Editor + RemoteMCP (port 8422)           │
         │ config.json   │              │  22+ tools across 7 domains                  │
         │ state.json    │              │  Domains: level, blueprint, umg, edgraph,    │
         └───────────────┘              │           behaviortree, slate, eca            │
                                        │                                              │
                                        │  ECABridge (engine built-in, port 3000)      │
                                        │  238+ atomic C++ commands, 19 categories     │
                                        │  Accessed via RemoteMCP eca domain           │
                                        └──────────────────────────────────────────────┘
```

## Development

```bash
git clone https://github.com/AlainChen/UnrealMCPHub.git
cd UnrealMCPHub
uv sync --extra dev      # Install with dev dependencies
uv run pytest tests/ -v  # Run tests (216 tests)
```

## Requirements

- Python >= 3.11
- Unreal Engine 5.x
- [RemoteMCP](https://github.com/blackplume233/UnrealRemoteMCP) — UE Editor plugin (Hub can auto-install it via `setup_project`)

## License

MIT
