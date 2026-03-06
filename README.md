# UnrealMCPHub

Central management platform for Unreal Engine MCP instances — bridge between AI agents and UE across the full development lifecycle.

Even when UE Editor is **not running**, the Hub can compile, install plugins, and launch the editor. Once UE is up, it transparently proxies all MCP tools to the running instance.

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

## Installation

```bash
cd UnrealMCPHub

# using uv (recommended)
uv sync

# or pip
pip install -e .
```

## Quick Start

### For AI Agents (Cursor / Claude / etc.)

This is the primary use case. Add UnrealMCPHub as an MCP server in your AI tool, then the agent handles everything through natural language.

**Step 1: Configure MCP**

Add to Cursor MCP settings (`.cursor/mcp.json`):

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

Or HTTP mode (for shared / remote use):

```json
{
  "mcpServers": {
    "unrealhub": {
      "url": "http://127.0.0.1:9422/mcp"
    }
  }
}
```

Then start the server manually:

```bash
uv run unrealhub serve --http --port 9422
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
# Install with dev dependencies
uv sync --extra dev

# Run tests (129 tests)
uv run pytest tests/ -v
```

## Requirements

- Python >= 3.11
- Unreal Engine 5.x with [RemoteMCP](https://github.com/blackplume233/UnrealRemoteMCP) plugin

## License

MIT
