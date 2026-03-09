# UnrealMCPHub

Central management platform for Unreal Engine MCP instances — bridge between AI agents and UE across the full development lifecycle.

Works with **[RemoteMCP](https://github.com/blackplume233/UnrealRemoteMCP)** (UE Editor plugin that exposes engine capabilities via MCP protocol). The Hub manages everything around it: install the plugin, compile, launch the editor, detect crashes, and transparently proxy all tool calls — so the AI agent only needs one MCP endpoint.

```
AI Agent ──► UnrealMCPHub ──► UE Editor + RemoteMCP plugin
              (this repo)       (blackplume233/UnrealRemoteMCP)
```

> **RemoteMCP** runs **inside** UE Editor and provides 17+ tools across 6 domains (level, blueprint, umg, edgraph, behaviortree, slate).
> **UnrealMCPHub** runs **outside** UE Editor and can compile, launch, monitor, and proxy — even when UE is not running.

## Features

- **Project setup** — Configure `.uproject` once; engine auto-detected from registry
- **Build & launch** — Compile via UBT, launch editor, wait for MCP readiness
- **Plugin install** — One-click RemoteMCP installation (local copy or GitHub download)
- **Instance discovery** — Scan ports to find running UE editors
- **UE tool proxy** — `ue_run_python`, `ue_call`, `ue_list_tools` and domain dispatch
- **Crash resilience** — Crash detection, report retrieval, restart flow
- **Multi-instance** — Switch between multiple UE editors via `use_editor`
- **Session notes** — Persist context for crash recovery
- **One-click overview** — `hub_status` shows project, plugin, instances, and watcher state

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

### For AI Agents (Cursor / Claude / etc.)

This is the primary use case. Add UnrealMCPHub as an MCP server in your AI tool, then the agent handles everything through natural language.

**Step 1: Install & Configure MCP** (see [Quick Install](#quick-install-30-seconds) above)

**HTTP mode** (for shared / remote / multi-client use):

```bash
unrealhub serve --http --port 9422
```

```json
{
  "mcpServers": {
    "unrealhub": {
      "url": "http://127.0.0.1:9422/mcp"
    }
  }
}
```

**Step 2: Talk to the agent**

Once configured, the AI agent has full access to all Hub tools. Example conversations:

```
You: "帮我编译并启动 UE 项目 D:/Projects/MyGame/MyGame.uproject"
Agent: [calls setup_project, compile_project, launch_editor automatically]

You: "在 UE 里创建一个蓝图 Actor"
Agent: [calls ue_get_dispatch to find blueprint tools, then ue_call_dispatch]

You: "UE 崩溃了怎么办"
Agent: [calls get_crash_report, shows crash info, offers restart_editor]
```

**Step 3: What happens behind the scenes**

```
Agent → Hub (setup_project)     # One-time project config, persisted
Agent → Hub (compile_project)   # Compiles via UBT, even without UE running
Agent → Hub (launch_editor)     # Starts UE, waits for MCP readiness
Agent → Hub (ue_run_python)     # Hub forwards to UE's RemoteMCP
                ↓
        UE Editor (port 8422)   # Executes Python, returns result
```

The agent only needs to know about the Hub — it never talks to UE directly.

### AI Agent Decision Flow

```
Is project configured?
├── No  → Ask user for .uproject path → setup_project()
└── Yes → Is UE Editor online?
          ├── No  → Need plugin? → install_plugin() → compile_project() → launch_editor()
          └── Yes → Use ue_* tools directly
                    └── Crashed? → get_crash_report() → restart_editor()
```

### For Humans (CLI)

```bash
unrealhub setup /path/to/MyProject.uproject   # Configure project
unrealhub serve                                # Start MCP server (stdio)
unrealhub serve --http --port 9422             # Start MCP server (HTTP)
unrealhub status                               # Show instance status
unrealhub discover                             # Discover running UE instances
unrealhub compile                              # Build active project
unrealhub launch                               # Launch editor
```

## Tool Reference

### Hub Management (always available, even without UE)

| Tool | Description |
|------|-------------|
| `setup_project` | Configure project path (once, persisted to `~/.unrealhub`) |
| `get_project_config` | View current project configuration |
| `hub_status` | One-stop overview of everything |
| `compile_project` | Compile project via UBT |
| `launch_editor` | Start UE Editor, wait for MCP readiness |
| `restart_editor` | Restart a crashed editor |
| `install_plugin` | Install RemoteMCP plugin |
| `set_plugin_source` | Configure plugin download URL or local path |
| `discover_instances` | Scan ports for running UE instances |
| `use_editor` | Switch active UE instance (multi-instance) |
| `get_crash_report` | Get crash details |
| `add_note` / `get_notes` | Session notes for crash recovery context |

### UE Proxy Tools (forwarded to active UE instance)

| Tool | Description |
|------|-------------|
| `ue_run_python` | Execute Python script in UE |
| `ue_call` | Call any UE MCP tool by name |
| `ue_list_tools` | List all tools from UE instance |
| `ue_get_dispatch` | List domain tools (level, blueprint, umg, etc.) |
| `ue_call_dispatch` | Call a domain-specific tool |
| `ue_test_state` | Test connection to UE |
| `ue_status` | Get active instance status |

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
         │ setup_project │              │ compile       │              │ ue_run_python  │
         │ install_plugin│              │ launch/restart│              │ ue_call        │
         │ hub_status    │              │ discover      │              │ ue_list_tools  │
         └───────────────┘              └───────┬───────┘              └───────┬───────┘
                 │                              │                              │
                 ▼                              │  Streamable HTTP             │
         ┌───────────────┐              ┌──────▼──────────────────────────────▼────────┐
         │ ~/.unrealhub  │              │  UE Editor + RemoteMCP (port 8422)            │
         │ config.json   │              │  17+ tools: run_python, get_dispatch, etc.    │
         │ state.json    │              │  6 domains: level, blueprint, umg, edgraph,   │
         └───────────────┘              │             behaviortree, slate               │
                                        └──────────────────────────────────────────────┘
```

## Development

```bash
git clone https://github.com/blackplume233/UnrealMCPHub.git
cd UnrealMCPHub
uv sync --extra dev      # Install with dev dependencies
uv run pytest tests/ -v  # Run tests (129 tests)
```

## Requirements

- Python >= 3.11
- Unreal Engine 5.x
- [RemoteMCP](https://github.com/blackplume233/UnrealRemoteMCP) — UE Editor plugin (Hub can auto-install it via `install_plugin`)

## License

MIT
